﻿**

## Игра - Space Odyssey

**

Техническое задание:
Создать шутер на Pygame с 
 - несколькими уровнями 
 - анимированными спрайтами  
 - подсчетом очков
 - главным меню
 - экранами завершения уровня

Для запуска игры необходимо установить библиотеку PyGame и запустить файл "game.py"

Цель игры - стрелять по приближающимся космическим кораблям, набирая очки за каждое успешное попадание, и(не на всех уровнях) уклоняться от огня вражеских кораблей
Каждый этап игры реализуется с помощью игровых состояний(state).
В игре имеется главное меню, с выбором уровней. При нажатии на кнопку с желаемым уровнем, вызывается соответствующее событие и состояние.
Во время игры ведется подсчет очков, и по ее окончании результат выводится на экран. Также на экран выводится лучшее количество очков, хранящееся в базе данных и, если оно меньше результата игры, то в базу данных сохраняется новое лучшее количество очков.
У игрока имеется здоровье, и при столкновении с вражескими кораблями оно снижается. Если столкновений произошло слишком много, то игрок умирает и выводится экран неудачи.

В игре два спрайта: космический корабль(и игрок, и вражеские корабли являются объектами одного класса, но в `_init_` передаются разные значения аргументов и поэтому поведение различается) и выстрел. FPS = 60.
 




