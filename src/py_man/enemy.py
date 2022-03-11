from random import choice, randint
from asciimatics.screen import Screen
import time
import config
x = config.x
y = config.y
class Enemy:
    x_pos = None
    y_pos = None
    enemy_direction = 0
    prev_enemy = time.monotonic()
    prev_rand = time.monotonic()
    enemy_letter = ''
    alive = False
    last_chr = 'H'
    isGameOver = False
    ways = [0,1,2,3]
    around = []
    score = 0
    def ignore(self):
        ignore = list(config.enemy_letters)
        ignore.append('#')
        return ignore

    def place_enemy(self,game_field, enemy_pos, enemy_letter):
        self.x_pos = enemy_pos[0]
        self.y_pos = enemy_pos[1]
        self.enemy_letter = enemy_letter
        self.alive = True
        self.last_chr = 'H'
        game_field[self.y_pos][self.x_pos] = self.enemy_letter
    def move_enemy(self, game_field):
        global x,y
        prev_pos = [self.x_pos, self.y_pos]
        enemy_direction = self.enemy_direction
        game_field[prev_pos[1]][prev_pos[0]] = self.last_chr
        #self.ways = []
        try:
            if enemy_direction == 0 and not (game_field[self.y_pos][self.x_pos-1] in self.ignore()):
                if (self.x_pos == 0):
                    self.x_pos = x-1
                self.x_pos-=1
        except:
            pass
        if enemy_direction == 1 and not (self.y_pos == 0) and not (game_field[self.y_pos-1][self.x_pos] in self.ignore()):
            self.y_pos-=1
        try:
            if enemy_direction == 2 and not (game_field[self.y_pos][self.x_pos+1] in self.ignore()):
                if (self.x_pos == x-1):
                    self.x_pos = 0
                else:
                    self.x_pos+=1
        except:
            pass    
        if enemy_direction == 3 and not (self.y_pos == y-1) and not (game_field[self.y_pos+1][self.x_pos] in self.ignore()):
            self.y_pos+=1    
        self.last_chr = game_field[self.y_pos][self.x_pos]
        game_field[self.y_pos][self.x_pos] = self.enemy_letter
    def rand_dir(self):
        self.enemy_direction = choice(self.ways)
    def check_collision(self,game_field, player_x,player_y):
        if self.x_pos == player_x and self.y_pos == player_y:
            if config.isPlayerInvincible:
                self.kill_enemy(game_field)
                self.alive = False
                self.score += 1000
            else:
                config.isGameOver = True

    def enemy_update(self,game_field,player_x,player_y):
        #self.around=[game_field[self.y_pos][self.x_pos-1],game_field[self.y_pos-1][self.x_pos],game_field[self.y_pos][self.x_pos+1],game_field[self.y_pos][self.x_pos+1]]
        if time.monotonic() - self.prev_enemy >= 0.3:
            if self.alive:
                self.move_enemy(game_field)
            else:
                self.kill_enemy(game_field)
            self.prev_enemy = time.monotonic()
        if time.monotonic() - self.prev_rand >= 1:
            self.rand_dir()
            self.prev_rand = time.monotonic()
        self.check_collision(game_field, player_x,player_y) 
    def kill_enemy(self,game_field):
        game_field[self.y_pos][self.x_pos] = self.last_chr
