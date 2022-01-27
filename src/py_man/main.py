import os
import threading
from asciimatics.screen import Screen
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.effects import Cycle
import time
import enemy
import winsound
## Карта ##
board = list("#############################............##............##.####.#####.##.#####.####.##P####.#####.##.#####.####P##..........................##.####.##.########.##.####.##......##....##....##......#######.##### ## #####.######     #.##          ##.#          #.## ###--### ##.#     ######.## # HHHH # ##.######      .   # HHHH #   .      ######.## # HHHH # ##.######     #.## ######## ##.#          #.##    $     ##.#     ######.## ######## ##.#######............##............##.####.#####.##.#####.####.##P..##................##..P####.##.##.########.##.##.####......##....##....##......##.##########.##.##########.##..........................#############################")
## Карта ##


##      Переменные      ##
score = 0
x,y = 28, 24
game_field = [[board[i+28*(j)] for i in range(0,x)] for j in range(0,y)]
x_pos = 13
y_pos = 18
changed = False
changed2 = False
direction = 0
moved = False
##########################



def reset_field():
    global game_field
    game_field = [[board[i+28*(j)] for i in range(0,x)] for j in range(0,y)]
    place_player()

prev = time.monotonic()
def place_player():
    game_field[y_pos][x_pos] = 'O'
def update_position():
    global y_pos, x_pos, changed2, prev, direction, moved,score
    moved = False
    prev_pos = [x_pos, y_pos]
    if time.monotonic() - prev >= 0.5:
        prev = time.monotonic()
        if direction == 0 and not (x_pos == 0) and not (game_field[y_pos][x_pos-1]=='#'):
            x_pos-=1
            moved = True
            if game_field[y_pos][x_pos-1] == '.':
                score += 1
        if direction == 1 and not (y_pos == 0) and not (game_field[y_pos-1][x_pos]=='#'):
            y_pos-=1
            moved = True
            if game_field[y_pos-1][x_pos]=='.':
                score+=1
        if direction == 2:
            if (x_pos == x-1):
                x_pos = 0
                moved = True
            elif (game_field[y_pos][x_pos+1]=='#'):
                pass
            else:
                x_pos+=1
                moved = True
            if game_field[y_pos][x_pos+1]=='.':
                score+=1
        if direction == 3 and not (y_pos == y-1) and not (game_field[y_pos+1][x_pos]=='#'):
            y_pos+=1
            moved = True
            if game_field[y_pos+1][x_pos]=='.':
                score+=1   
        game_field[prev_pos[1]][prev_pos[0]] = ' '
        game_field[y_pos][x_pos] = 'O'
def game_over_screen(screen):
    effects = [Cycle(screen, FigletText('GAME OVER', font='big'), int(screen.height /2 -8)),
    Cycle(screen, FigletText(str(score), font='big'), int(screen.height / 2 + 3))
    ]
    screen.play([Scene(effects, 50)]) 
def lost_sound():
    winsound.PlaySound('game_over.wav', winsound.SND_FILENAME)
    os._exit(1)
def demo(screen):
    while True:
        global y_pos, x_pos, changed, direction, lost
        lost = False
        for j in range(0,y):
            for q in range(0,x):
                if j == enemy.y_pos and q == enemy.x_pos:
                    bg_col = 1
                    fn_col = 2
                elif j == y_pos and q == x_pos:
                    bg_col = 2
                    fn_col = 3
                else:
                    bg_col = 5
                    fn_col = 7     
                screen.print_at(game_field[j][q],q+(screen.width // 2 - x//2),j+(screen.height // 2 - y//2),bg=bg_col,colour=fn_col)
            screen.print_at('',x+1,j)
        screen.print_at(score,0,0)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        if ev == ord('w') and not (y_pos == 0):
            changed = True
            direction = 1
        if ev == (ord('s')) and not (y_pos == y-1):
            direction = 3
            changed = True
        if ev == (ord('d')) and not (x_pos == x-1):
            direction = 2
            changed = True
        if ev == (ord('a')) and not (x_pos == 0): 
            direction = 0
            changed = True
        if ev == (ord('r')):
            reset_field()
        if ev == (ord('k')):
            lost = True
        update_position()
        enemy.enemy_update(game_field,x,y,'w')
        screen.refresh()
        if x_pos == enemy.x_pos and y_pos == enemy.y_pos:
            lost = True
        if lost:
            break
        time.sleep(0.03)



place_player()
enemy.place_enemy(game_field, 12,11,'w')
winsound.PlaySound('start.wav', winsound.SND_FILENAME)
Screen.wrapper(demo)



if lost:
    lost_thr = threading.Thread(target=lost_sound)
    lost_thr.start()
    Screen.wrapper(game_over_screen)