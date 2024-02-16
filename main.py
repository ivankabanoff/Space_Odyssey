import pygame
import sys
import random
import sqlite3
from load_image import load_image
from animated_button import AnimatedButton
from laser_bolt import LaserBolt
from spaceship import Spaceship


def main():
    pygame.init()
    pixel_font_title = pygame.font.Font('data/Pixeltype.ttf', 100)
    pixel_font_buttons = pygame.font.Font('data/Pixeltype.ttf', 30)
    width = 1000
    height = 562
    screen = pygame.display.set_mode((width, height))

    shoot = False
    # Состояние игрока
    moving_up = False
    moving_down = False

    # Группы спрайтов
    small_enemies_group = pygame.sprite.Group()
    medium_enemies_group = pygame.sprite.Group()
    big_enemies_group = pygame.sprite.Group()
    laser_bolts_group = pygame.sprite.Group()
    groups = [small_enemies_group, medium_enemies_group, big_enemies_group, laser_bolts_group]

    # Создаем события
    mission_1_event = pygame.event.Event(3)
    mission_1_success = pygame.event.Event(4)
    exit_1 = pygame.event.Event(5)
    fail_event = pygame.event.Event(6)
    mission_2_event = pygame.event.Event(7)
    mission_2_success = pygame.event.Event(8)

    player_spaceship = Spaceship(screen, 9, 'player', 200, 300, 5, groups, fail_event)

    mm_background_surf = load_image('data/mm_bcknd.png')

    starfield_background = load_image('data/starfield.png')

    clock = pygame.time.Clock()

    # Игровые состояния
    main_menu_state = True
    mission_choice_state = False
    mission_1_state = False
    mission_1_success_state = False
    mission_fail_state = False
    mission_2_state = False
    mission_2_success_state = False

    # Загружаем изображения кнопок:
    blue_btn_image1 = load_image('data/buttons/btn_1.png')
    blue_btn_image2 = load_image('data/buttons/btn_2.png')
    blue_btn_image3 = load_image('data/buttons/btn_3.png')

    red_btn_image1 = load_image('data/buttons/red_btn_1.png')
    red_btn_image2 = load_image('data/buttons/red_btn_2.png')
    red_btn_image3 = load_image('data/buttons/red_btn_3.png')

    grey_btn_image1 = load_image('data/buttons/grey_btn_1.png')

    # Создаем кнопки:
    missions_btn = AnimatedButton(400, 160, blue_btn_image1, blue_btn_image2, blue_btn_image3, 4, screen)
    mission_1_btn = AnimatedButton(100, 250, red_btn_image1, red_btn_image2, red_btn_image3, 4, screen)
    mission_2_btn = AnimatedButton(400, 250, red_btn_image1, red_btn_image2, red_btn_image3, 4, screen)
    mission_3_btn = AnimatedButton(700, 250, grey_btn_image1, grey_btn_image1, grey_btn_image1, 4, screen)
    exit_btn = AnimatedButton(400, 450, blue_btn_image1, blue_btn_image2, blue_btn_image3, 4, screen)

    # Переменные, контролирующие время
    mission_1_time = 0
    mission_1_length = 75000

    mission_2_time = 0
    mission_2_length = 75000

    loop = 0  # Зацикленный фон

    # Время через которое появляются вражеские корабли
    pygame.time.set_timer(0, 2200)
    pygame.time.set_timer(1, 4200)
    pygame.time.set_timer(2, 4400)

    level_end_sound = pygame.mixer.Sound('data/sounds/level_end.wav')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Нажатие на клавиши во время игры
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    moving_up = True
                if event.key == pygame.K_s:
                    moving_down = True
                if event.key == pygame.K_SPACE:
                    shoot = True
                if event.key == pygame.K_ESCAPE:
                    pygame.event.set_allowed(6)
                    pygame.event.post(fail_event)
            # Клавиша отпущена
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    moving_up = False
                if event.key == pygame.K_s:
                    moving_down = False
                if event.key == pygame.K_SPACE:
                    shoot = False
            if event.type == 0 and mission_1_state or event.type == 0 and mission_2_state:
                small_enemy_spaceship = Spaceship(screen, 2, 'small_enemy', 1300,
                                                  random.randrange(10, 540), 4, groups,
                                                  fail_event, player=player_spaceship)
                small_enemies_group.add(small_enemy_spaceship)
            if event.type == 1 and mission_1_state or event.type == 1 and mission_2_state:
                medium_enemy_spaceship = Spaceship(screen, 2, 'medium_enemy', 1300,
                                                   random.randrange(10, 540), 5, groups, fail_event,
                                                   player=player_spaceship)
                medium_enemies_group.add(medium_enemy_spaceship)
            if event.type == 2 and mission_2_state:
                big_enemy_spaceship = Spaceship(screen, 2, 'big_enemy', 1300,
                                                random.randrange(10, 540), 5, groups, fail_event,
                                                player=player_spaceship, ai_enabled=True)
                big_enemies_group.add(big_enemy_spaceship)
            if event.type == 3:
                mission_choice_state = False
                mission_1_state = True
            if event.type == 4:
                mission_1_state = False
                mission_1_success_state = True
            if event.type == 5:
                mission_2_success_state = False
                mission_1_success_state = False
                mission_choice_state = True
            if event.type == 6:
                mission_1_state = False
                mission_2_state = False
                mission_fail_state = True
            if event.type == 7:
                mission_fail_state = False
                mission_choice_state = False
                mission_2_state = True
            if event.type == 8:
                mission_2_state = False
                mission_2_success_state = True

        if main_menu_state:
            screen.blit(mm_background_surf, (0, 0))
            game_title = pixel_font_title.render('Space Odyssey', False, (255, 255, 255))
            gt_rect = game_title.get_rect(center=(500, 80))
            screen.blit(game_title, gt_rect)

            missions_btn.draw(screen)
            missions_btn_txt = pixel_font_buttons.render('Missions', False, "Black")
            mbt_rect = game_title.get_rect(center=(695, 212))
            screen.blit(missions_btn_txt, mbt_rect)
            if missions_btn.is_pressed():
                main_menu_state = False
                mission_choice_state = True
        elif mission_choice_state:
            screen.blit(mm_background_surf, (0, 0))
            title = pixel_font_title.render('Choose a mission', False, (255, 255, 255))
            t_rect = title.get_rect(center=(500, 80))
            screen.blit(title, t_rect)

            mission_1_btn.draw(screen)
            mission_2_btn.draw(screen)
            mission_3_btn.draw(screen)

            mission_1_btn_txt = pixel_font_buttons.render('Mission 1', False, "White")
            m1bt_rect = title.get_rect(center=(410, 300))
            screen.blit(mission_1_btn_txt, m1bt_rect)

            mission_2_btn_txt = pixel_font_buttons.render('Mission 2', False, "White")
            m1bt_rect = title.get_rect(center=(710, 300))
            screen.blit(mission_2_btn_txt, m1bt_rect)

            mission_3_btn_txt = pixel_font_buttons.render('Mission 3', False, "White")
            m1bt_rect = title.get_rect(center=(1010, 300))
            screen.blit(mission_3_btn_txt, m1bt_rect)

            if mission_1_btn.is_pressed():
                pygame.event.set_allowed(3)
                pygame.event.post(mission_1_event)
                mission_1_time = pygame.time.get_ticks()
                small_enemies_group.empty()
                big_enemies_group.empty()
                medium_enemies_group.empty()
                laser_bolts_group.empty()
            if mission_2_btn.is_pressed():
                pygame.event.set_allowed(7)
                pygame.event.post(mission_2_event)
                mission_2_time = pygame.time.get_ticks()
                small_enemies_group.empty()
                big_enemies_group.empty()
                medium_enemies_group.empty()
                laser_bolts_group.empty()
        elif mission_1_state:
            screen.blit(starfield_background, (loop, 0))
            screen.blit(starfield_background, (width + loop, 0))
            if loop == - width:
                screen.blit(starfield_background, (width + loop, 0))
                loop = 0
            loop -= 2
            player_spaceship.update()
            player_spaceship.draw()

            small_enemies_group.update()
            small_enemies_group.draw(screen)

            medium_enemies_group.update()
            medium_enemies_group.draw(screen)

            laser_bolts_group.update(small_enemies_group, medium_enemies_group, big_enemies_group, player_spaceship,
                                     laser_bolts_group)
            laser_bolts_group.draw(screen)
            if player_spaceship.alive:
                if shoot:
                    player_spaceship.shoot()
                player_spaceship.move(moving_up, moving_down)
            if pygame.time.get_ticks() - mission_1_time > mission_1_length:
                pygame.event.set_blocked(3)
                pygame.event.set_allowed(4)
                pygame.event.post(mission_1_success)
                level_end_sound.play()
                con = sqlite3.connect("data/best_scores.sqlite")
                cur = con.cursor()
                current_best_score_1 = cur.execute("""SELECT level_1 FROM BestScore""").fetchone()[0]
                if player_spaceship.score > int(current_best_score_1):
                    new_score = str(player_spaceship.score)
                    action = cur.execute(f"""UPDATE BestScore SET level_1 = {new_score}""")
                    con.commit()
                    con.close()
        elif mission_1_success_state:
            screen.blit(starfield_background, (0, 0))
            end_score = pixel_font_title.render(f'Score: {player_spaceship.score}', False,
                                                (255, 255, 255))
            s_rect = end_score.get_rect(center=(500, 80))
            screen.blit(end_score, s_rect)

            best_score_1 = pixel_font_title.render(f'Best score: {current_best_score_1}', False,
                                                   (255, 255, 255))
            best_score_rect = end_score.get_rect(center=(410, 200))
            screen.blit(best_score_1, best_score_rect)

            exit_btn.draw(screen)
            exit_txt = pixel_font_buttons.render('Exit', False, "Black")
            exit_txt_rect = exit_txt.get_rect(center=(495, 480))
            screen.blit(exit_txt, exit_txt_rect)

            if exit_btn.is_pressed():
                pygame.event.set_blocked(4)
                pygame.event.set_allowed(5)
                pygame.event.post(exit_1)
                player_spaceship = Spaceship(screen, 9, 'player', 200, 300, 5,
                                             groups, fail_event)
        elif mission_fail_state:
            screen.blit(starfield_background, (0, 0))
            fail_message = pixel_font_title.render(f'Oops!', False, (255, 255, 255))
            f_rect = fail_message.get_rect(center=(500, 80))
            screen.blit(fail_message, f_rect)

            exit_btn.draw(screen)
            exit_txt = pixel_font_buttons.render('Exit', False, "Black")
            exit_txt_rect = exit_txt.get_rect(center=(495, 480))
            screen.blit(exit_txt, exit_txt_rect)

            if exit_btn.is_pressed():
                pygame.event.set_blocked(6)
                pygame.event.set_allowed(5)
                pygame.event.post(exit_1)
                player_spaceship = Spaceship(screen, 9, 'player', 200, 300, 5,
                                             groups, fail_event)
        elif mission_2_state:
            screen.blit(starfield_background, (loop, 0))
            screen.blit(starfield_background, (width + loop, 0))
            if loop == - width:
                screen.blit(starfield_background, (width + loop, 0))
                loop = 0
            loop -= 2
            player_spaceship.update()
            player_spaceship.draw()

            small_enemies_group.update()
            small_enemies_group.draw(screen)

            medium_enemies_group.update()
            medium_enemies_group.draw(screen)

            big_enemies_group.update()
            big_enemies_group.draw(screen)

            laser_bolts_group.update(small_enemies_group, medium_enemies_group, big_enemies_group, player_spaceship,
                                     laser_bolts_group)
            laser_bolts_group.draw(screen)
            if player_spaceship.alive:
                if shoot:
                    player_spaceship.shoot()
                player_spaceship.move(moving_up, moving_down)
            if pygame.time.get_ticks() - mission_2_time > mission_2_length:
                pygame.event.set_blocked(7)
                pygame.event.set_allowed(8)
                pygame.event.post(mission_2_success)
                level_end_sound.play()
                con = sqlite3.connect("data/best_scores.sqlite")
                cur = con.cursor()
                current_best_score_2 = cur.execute("""SELECT level_2 FROM BestScore""").fetchone()[0]
                if player_spaceship.score > int(current_best_score_2):
                    new_score = str(player_spaceship.score)
                    action = cur.execute(f"""UPDATE BestScore SET level_2 = {new_score}""")
                    con.commit()
                    con.close()
        elif mission_2_success_state:
            screen.blit(starfield_background, (0, 0))
            end_score = pixel_font_title.render(f'Score: {player_spaceship.score}', False,
                                                (255, 255, 255))
            s_rect = end_score.get_rect(center=(500, 80))
            screen.blit(end_score, s_rect)

            best_score_1 = pixel_font_title.render(f'Best score: {current_best_score_2}', False,
                                                   (255, 255, 255))
            best_score_rect = end_score.get_rect(center=(410, 200))
            screen.blit(best_score_1, best_score_rect)

            exit_btn.draw(screen)
            exit_txt = pixel_font_buttons.render('Exit', False, "Black")
            exit_txt_rect = exit_txt.get_rect(center=(495, 480))
            screen.blit(exit_txt, exit_txt_rect)

            if exit_btn.is_pressed():
                pygame.event.set_blocked(8)
                pygame.event.set_allowed(5)
                pygame.event.post(exit_1)
                player_spaceship = Spaceship(screen, 9, 'player', 200, 300, 5,
                                             groups, fail_event)
        pygame.display.update()
        clock.tick(60)
        print(mission_2_state)


if __name__ == '__main__':
    main()

