from random import randint
from asciimatics.screen import Screen
import time
x_pos = None
y_pos = None
enemy_direction = 0
prev_enemy = time.monotonic()
prev_rand = time.monotonic()
def place_enemy(game_field, x, y, enemy_letter):
    global x_pos, y_pos
    x_pos = x
    y_pos = y
    game_field[y_pos][x_pos] = enemy_letter
def move_enemy(game_field, x,y, enemy_letter):
    global x_pos, y_pos
    prev_pos = [x_pos, y_pos]
    if enemy_direction == 0 and not (x_pos == 0) and not (game_field[y_pos][x_pos-1]=='#'):
            x_pos-=1
    if enemy_direction == 1 and not (y_pos == 0) and not (game_field[y_pos-1][x_pos]=='#'):
            y_pos-=1
    if enemy_direction == 2:    
        if (x_pos == x-1):
                x_pos = 0
        elif (game_field[y_pos][x_pos+1]=='#'):
            pass
        else:
            x_pos+=1    
    if enemy_direction == 3 and not (y_pos == y-1) and not (game_field[y_pos+1][x_pos]=='#'):
        y_pos+=1    
    last_chr = game_field[y_pos][x_pos]
    game_field[prev_pos[1]][prev_pos[0]] = last_chr
    game_field[y_pos][x_pos] = enemy_letter
def rand_dir():
    global enemy_direction
    enemy_direction = randint(0,3)


def enemy_update(game_field,x,y, enemy_letter):
    global prev_enemy, prev_rand
    if time.monotonic() - prev_enemy >= 0.7:
        move_enemy(game_field,x,y,enemy_letter)
        prev_enemy = time.monotonic()
    if time.monotonic() - prev_rand >= 2:
        rand_dir()
        prev_rand = time.monotonic()        