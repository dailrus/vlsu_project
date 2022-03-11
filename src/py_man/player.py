import time
import config
class Player:
    score = 0
    x_pos = 13
    y_pos = 18
    direction = 0
    prev = 0
    op_trigger = False
    op_timer = 0
    def place_player(self,game_field):
        game_field[self.y_pos][self.x_pos] = config.player_character
        self.prev = time.monotonic()
    def GodMode_handler(self):
        if self.op_trigger:
            self.op_timer = time.monotonic()
            self.op_trigger = False
        if time.monotonic() - self.op_timer >= config.Invincibility_delay:
            config.isPlayerInvincible = False
        else:
            config.isPlayerInvincible = True
        return round(config.Invincibility_delay - (time.monotonic() - self.op_timer), 2)
    def update_position(self,game_field,default_field,x,y):
        global score
        direction = self.direction
        prev_pos = [self.x_pos, self.y_pos]
        if time.monotonic() - self.prev >= 0.4:
            self.prev = time.monotonic()
            if direction == 0 and not (default_field[self.y_pos][self.x_pos-1]=='#'):
                if not (self.x_pos == 0):
                    self.x_pos-=1
                else:
                    self.x_pos = x-1
            if direction == 1 and not (self.y_pos == 0) and not (default_field[self.y_pos-1][self.x_pos]=='#'):
                self.y_pos-=1
            if direction == 2 and not (game_field[self.y_pos][self.x_pos+1]=='#'):
                if (self.x_pos == x-1):
                    self.x_pos = 0
                else:
                    self.x_pos+=1   
            if direction == 3 and not (self.y_pos == y-1) and not (default_field[self.y_pos+1][self.x_pos] in ('#','-')):
                self.y_pos+=1
            if game_field[self.y_pos][self.x_pos] == 'P':
                self.op_trigger = True
            if game_field[self.y_pos][self.x_pos]=='.':
                self.score+=100   
            if game_field[self.y_pos][self.x_pos]=='$':
                self.score+=300
            game_field[prev_pos[1]][prev_pos[0]] = ' '
            game_field[self.y_pos][self.x_pos] = config.player_character