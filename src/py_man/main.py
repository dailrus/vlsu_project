import os
from random import randint
import threading
from asciimatics.screen import Screen
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.effects import Cycle
import time
import enemy
import player
import winsound
## Карта ##
board = list("#############################............##............##.####.#####.##.#####.####.##P####.#####.##.#####.####P##..........................##.####.##.########.##.####.##......##....##....##......#######.##### ## #####.######     #.##          ##.#          #.## ###--### ##.#     ######.## # HHHH # ##.######      .   # HHHH #   .      ######.## # HHHH # ##.######     #.## ######## ##.#          #.##    $     ##.#     ######.## ######## ##.#######............##............##.####.#####.##.#####.####.##P..##................##..P####.##.##.########.##.##.####......##....##....##......##.##########.##.##########.##..........................#############################")
## Карта ##

enemy1 = enemy.Enemy()
enemy2 = enemy.Enemy()
enemy3 = enemy.Enemy()
player1 = player.Player()

##      Переменные      ##
x,y = 28, 24
game_field = [[board[i+28*(j)] for i in range(0,x)] for j in range(0,y)]
changed = False
moved = False
##########################


def reset_field():
    global game_field
    game_field = [[board[i+28*(j)] for i in range(0,x)] for j in range(0,y)]
    player1.place_player(game_field)

prev = time.monotonic()
def game_over_screen(screen):
    effects = [Cycle(screen, FigletText('GAME OVER', font='big'), int(screen.height /2 -8)),
    Cycle(screen, FigletText(str(player1.score), font='big'), int(screen.height / 2 + 3))
    ]
    screen.play([Scene(effects, 50)]) 
def lost_sound():
    winsound.PlaySound('game_over.wav', winsound.SND_FILENAME)
    os._exit(1)
def demo(screen):
    while True:
        global y_pos, x_pos, changed, lost
        lost = False
        for j in range(0,y):
            for q in range(0,x):
                if (j == enemy1.y_pos and q == enemy1.x_pos) or (j == enemy2.y_pos and q == enemy2.x_pos) or (j == enemy3.y_pos and q == enemy3.x_pos):
                    bg_col = 1
                    fn_col = 2
                elif j == player1.y_pos and q == player1.x_pos:
                    if player1.isGod:
                        bg_col = randint(0,7)
                    else:
                        bg_col = 2
                    fn_col = 3
                else:
                    bg_col = 5
                    fn_col = 7     
                screen.print_at(game_field[j][q],q+(screen.width // 2 - x//2),j+(screen.height // 2 - y//2),bg=bg_col,colour=fn_col)
            screen.print_at('',x+1,j)
        screen.print_at(player1.score,(screen.width // 2 - x//2)-3,(screen.height // 2 - y//2)-1)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        if ev == ord('w') and not (player1.y_pos == 0):
            changed = True
            player1.direction = 1
        if ev == (ord('s')) and not (player1.y_pos == y-1):
            player1.direction = 3
            changed = True
        if ev == (ord('d')) and not (player1.x_pos == x-1):
            player1.direction = 2
            changed = True
        if ev == (ord('a')) and not (player1.x_pos == 0): 
            player1.direction = 0
            changed = True
        if ev == (ord('r')):
            reset_field()
        if ev == (ord('k')):
            lost = True
        player1.update_position(game_field, x, y)
        enemy1.enemy_update(game_field,x,y)
        enemy2.enemy_update(game_field,x,y)
        enemy3.enemy_update(game_field,x,y)
        if enemy1.check_collision(player1.x_pos,player1.y_pos) or enemy2.check_collision(player1.x_pos,player1.y_pos) or enemy3.check_collision(player1.x_pos,player1.y_pos):
            lost = True
        if lost:
            break
        screen.refresh()
        time.sleep(0.03)



player1.place_player(game_field)
enemy1.place_enemy(game_field, 12,10,'w')
enemy2.place_enemy(game_field, 12,11,'t')
enemy3.place_enemy(game_field, 13,12,'i')
winsound.PlaySound('start.wav', winsound.SND_FILENAME)
Screen.wrapper(demo)



if lost:
    lost_thr = threading.Thread(target=lost_sound)
    lost_thr.start()
    Screen.wrapper(game_over_screen)