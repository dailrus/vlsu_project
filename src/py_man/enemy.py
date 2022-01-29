from random import randint
from asciimatics.screen import Screen
import time
is_Collide = False
class Enemy:
    x_pos = None
    y_pos = None
    enemy_direction = 0
    prev_enemy = time.monotonic()
    prev_rand = time.monotonic()
    enemy_letter = ''
    last_state = 'pick'
    alive = False
    last_chr = 'H'
    def place_enemy(self,game_field, x, y, enemy_letter):
        self.x_pos = x
        self.y_pos = y
        self.enemy_letter = enemy_letter
        self.alive = True
        game_field[self.y_pos][self.x_pos] = self.enemy_letter
    def move_enemy(self, game_field, x,y):
        prev_pos = [self.x_pos, self.y_pos]
        enemy_direction = self.enemy_direction
        game_field[prev_pos[1]][prev_pos[0]] = self.last_chr
        if self.last_state == 'pick':
            if enemy_direction == 0 and not (game_field[self.y_pos][self.x_pos-1] in ('#','w','t','i')):
                self.last_chr = game_field[self.y_pos][self.x_pos-1]
            if enemy_direction == 1 and not (game_field[self.y_pos-1][self.x_pos] in ('#','w','t','i')):
                self.last_chr = game_field[self.y_pos-1][self.x_pos]
            if enemy_direction == 2 and not (game_field[self.y_pos][self.x_pos+1] in ('#','w','t','i')):
                self.last_chr = game_field[self.y_pos][self.x_pos+1]        
            if enemy_direction == 3 and not (game_field[self.y_pos+1][self.x_pos] in ('#','w','t','i')):
                self.last_chr = game_field[self.y_pos+1][self.x_pos]
            self.last_state = 'pick'
            
        if enemy_direction == 0 and not (self.x_pos == 0) and not (game_field[self.y_pos][self.x_pos-1]=='#'):
                self.x_pos-=1
        if enemy_direction == 1 and not (self.y_pos == 0) and not (game_field[self.y_pos-1][self.x_pos]=='#'):
                self.y_pos-=1
        if enemy_direction == 2:    
            if (self.x_pos == x-1):
                    self.x_pos = 0
            elif (game_field[self.y_pos][self.x_pos+1]=='#'):
                pass
            else:
                self.x_pos+=1    
        if enemy_direction == 3 and not (self.y_pos == y-1) and not (game_field[self.y_pos+1][self.x_pos]=='#'):
            self.y_pos+=1    
        
        game_field[self.y_pos][self.x_pos] = self.enemy_letter
    def rand_dir(self):
        self.enemy_direction = randint(0,3)
    def check_collision(self, player_x,player_y):
        if self.x_pos == player_x and self.y_pos == player_y:
            return True  
    def enemy_update(self,game_field,x,y):
        if time.monotonic() - self.prev_enemy >= 0.7:
            if self.alive:
                self.move_enemy(game_field,x,y)
            else:
                self.kill_enemy(game_field)
            self.prev_enemy = time.monotonic()
        if time.monotonic() - self.prev_rand >= 2:
            self.rand_dir()
            self.prev_rand = time.monotonic() 
    def kill_enemy(self,game_field):
        game_field[self.y_pos][self.x_pos] = self.last_chr