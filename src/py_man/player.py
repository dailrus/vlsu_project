import time
class Player:
    score = 0
    x_pos = 13
    y_pos = 18
    direction = 0
    prev = 0
    op = False
    op_timer = 0
    isGod = False
    def place_player(self,game_field):
        game_field[self.y_pos][self.x_pos] = 'O'
        self.prev = time.monotonic()
    def op_handler(self):
        if self.op:
            self.op_timer = time.monotonic()
            self.op = False
        if time.monotonic() - self.op_timer >= 10:
            self.isGod = False
        else:
            self.isGod = True
    def update_position(self,game_field,x,y):
        global score
        moved = False
        direction = self.direction
        prev_pos = [self.x_pos, self.y_pos]
        if time.monotonic() - self.prev >= 0.5:
            self.prev = time.monotonic()
            if direction == 0 and not (self.x_pos == 0) and not (game_field[self.y_pos][self.x_pos-1]=='#'):
                self.x_pos-=1
                moved = True
                if game_field[self.y_pos][self.x_pos-1] == '.':
                    self.score += 1
                if game_field[self.y_pos][self.x_pos-1] == 'P':
                    self.op = True
            if direction == 1 and not (self.y_pos == 0) and not (game_field[self.y_pos-1][self.x_pos]=='#'):
                self.y_pos-=1
                moved = True
                if game_field[self.y_pos][self.x_pos]=='.':
                    self.score+=1
                if game_field[self.y_pos][self.x_pos] == 'P':
                    self.op = True
            if direction == 2:
                if (self.x_pos == x-1):
                    self.x_pos = 0
                    moved = True
                elif (game_field[self.y_pos][self.x_pos]=='#'):
                    pass
                else:
                    self.x_pos+=1
                    moved = True
                if game_field[self.y_pos][self.x_pos]=='.':
                    self.score+=1
                if game_field[self.y_pos][self.x_pos] == 'P':
                    self.op = True
            if direction == 3 and not (self.y_pos == y-1) and not (game_field[self.y_pos+1][self.x_pos]=='#'):
                self.y_pos+=1
                if game_field[self.y_pos][self.x_pos] == 'P':
                    self.op = True
                moved = True
                if game_field[self.y_pos][self.x_pos]=='.':
                    self.score+=1   
            game_field[prev_pos[1]][prev_pos[0]] = ' '
            game_field[self.y_pos][self.x_pos] = 'O'