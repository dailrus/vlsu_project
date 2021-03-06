import os
from random import choice
import threading
from asciimatics.screen import Screen
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, BannerText
import time
import enemy
import player
import config
import winsound
## Карта ##

## Карта ##
##      Переменные      ##
x = config.x
y = config.y
isWin = False

##########################
enemies = []
for enmy in range(3):
    enmy = enemy.Enemy()
    enemies.append(enmy)
player1 = player.Player()
def score():
    total = player1.score
    for en in enemies:
        total += en.score
    return total
default_field = [[config.board[i+28*(j)] for i in range(0,x)] for j in range(0,y)]

def reset_field():
    global game_field
    game_field = [[config.board[i+28*(j)] for i in range(0,x)] for j in range(0,y)]
    player1.place_player(game_field)
prev = time.monotonic()
reset_field()
def game_over_screen(screen):
    effects = [Cycle(screen, FigletText('GAME OVER', font='big'), int(screen.height /2 -8)),
    BannerText(screen, FigletText('SCORE :  '+str(player1.score)), int(screen.height / 2 + 2),2),
    BannerText(screen, FigletText('Press "q" to exit',font='small'), int(screen.height - 6), 3)
    ]
    screen.play([Scene(effects, 200)])
    ev = screen.get_key()
    if ev == (ord('q')):
        os._exit(1)
def win_screen(screen):
    ev = screen.get_key()
    if ev == (ord('q')):
        os._exit(1)
def lost_sound():
    winsound.PlaySound('game_over.wav', winsound.SND_FILENAME)
def main_game(screen):
    while True:
        global y_pos, x_pos, changed, isWin
        prnt_tm = ''
        for i in range(len(enemies)):
            if not enemies[i].alive:
                enemies[i].place_enemy(game_field,config.enemies_pos[i],config.enemy_letters[i])
        for j in range(0,y):
            for q in range(0,x):
                if (j == enemies[0].y_pos and q == enemies[0].x_pos) or (j == enemies[1].y_pos and q == enemies[1].x_pos) or (j == enemies[2].y_pos and q == enemies[2].x_pos):
                    bg_col = 1
                    fn_col = 2
                elif j == player1.y_pos and q == player1.x_pos:
                    if config.isPlayerInvincible:
                        bg_col = choice([2,4])
                    else:    
                        bg_col = 2
                    fn_col = 3
                else:
                    bg_col = 5
                    fn_col = 7     
                screen.print_at(game_field[j][q],q+(screen.width // 2 - x//2),j+(screen.height // 2 - y//2),bg=bg_col,colour=fn_col)
            screen.print_at('',x+1,j)
        screen.print_at('Score: '+str(score()),(screen.width // 2 - x//2)-3,(screen.height // 2 - y//2)-1, bg=6,colour=7)
        if config.isPlayerInvincible:
            god_bg = 2
            prnt_tm = str(player1.GodMode_handler())
            screen.print_at('      ',(screen.width // 2)+17,(screen.height // 2 - y//2)-1,bg=0)
            screen.print_at('God Mode '+ prnt_tm,(screen.width // 2)+9,(screen.height // 2 - y//2)-1,bg=god_bg)
        else:
            god_bg = 1
            screen.print_at('God Mode',(screen.width // 2)+9,(screen.height // 2 - y//2)-1,bg=god_bg)
            screen.print_at('      ',(screen.width // 2)+17,(screen.height // 2 - y//2)-1,bg=0)
            
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
            config.isGameOver = True
        if ev == (ord('g')):
            player1.op_trigger = True
        if ev == (ord('o')):
            isWin = True
        player1.update_position(game_field,default_field, x, y)
        player1.GodMode_handler()
        for i in range(len(enemies)):
            enemies[i].enemy_update(game_field,player1.x_pos,player1.y_pos)
        if config.isGameOver:
            break
        if player1.score == 21300:
            isWin = True
            break
        screen.refresh()
        time.sleep(0.03)

player1.place_player(game_field)
#winsound.PlaySound('start.wav', winsound.SND_FILENAME)
Screen.wrapper(main_game)

if config.isGameOver:
    lost_thr = threading.Thread(target=lost_sound)
    lost_thr.start()
    Screen.wrapper(game_over_screen)
elif isWin:
    Screen.wrapper(win_screen)