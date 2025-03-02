import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
CARROT_INTERVAL = 20
START_SCENE = "start"
PLAY_SCENE = "play"
GAME_OVER_DISPLAY_TIMER = 60

class Carrot:
    def __init__(self, x, y, current_speed):
        self.x = x
        self.y = y
    def update(self):
        #carrotnya jatuh :D
        if self.y < SCREEN_HEIGHT:
            self.y += 5
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Haruka Not Carrot")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        self.reset_game()
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)
    
    def reset_game(self):
        self.current_screen = START_SCENE
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT * 4 // 5
        self.carrot = []
        self.is_collison = False
        self.current_speed = 1
        self.current_score = 0
        self.game_over_display_timer = GAME_OVER_DISPLAY_TIMER
        self.score_written = False
        try:
            with open("score.txt", "r") as f:
                self.high_score = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self.high_score = 0
    
    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.current_screen = PLAY_SCENE
    
    def update_play_scene(self):
        #Ular adalah Kunci
        if(not self.is_collison):
            if pyxel.btn(pyxel.KEY_A) and self.player_x > -4:
                self.player_x -= 3
            elif pyxel.btn(pyxel.KEY_D) and self.player_x < SCREEN_WIDTH - 12:
                self.player_x += 3
            if pyxel.btn(pyxel.KEY_S) and self.player_y < SCREEN_HEIGHT - 20:
                self.player_y += 3
            elif pyxel.btn(pyxel.KEY_W) and self.player_y > 0:
                self.player_y -= 3
            
            if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > -4:
                self.player_x -= 3
            elif pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < SCREEN_WIDTH - 12:
                self.player_x += 3
            if pyxel.btn(pyxel.KEY_DOWN) and self.player_y < SCREEN_HEIGHT - 20:
                self.player_y += 3
            elif pyxel.btn(pyxel.KEY_UP) and self.player_y > 0:
                self.player_y -= 3
            
            #Munculin carrotnya
            adjusted_interval = max(5, CARROT_INTERVAL - self.current_speed)
            if pyxel.frame_count % adjusted_interval == 0:
                self.carrot.append(Carrot(pyxel.rndi(0, SCREEN_WIDTH - 8), 0, self.current_speed))
                self.current_speed += 1  # Makin lama makin cepat

            #LALU KITA JATUHIN WAHHAHAHHAHA
            for carrot in self.carrot.copy():
                carrot.update()
            
                #ih kok makan carrot :(
                if (self.player_x <= carrot.x <= self.player_x + 8 and
                    self.player_y <= carrot.y < self.player_y + 8):
                    self.is_collison = True            
                
                #kalau carrotnya kabur yahaha
                if carrot.y >= SCREEN_HEIGHT and not self.is_collison:
                    self.current_score += 1
                    self.carrot.remove(carrot)      
                elif self.is_collison:
                    break
        else:
            if self.game_over_display_timer > 0:
                self.game_over_display_timer -= 1
            else:
                self.reset_game()
                self.current_screen = START_SCENE
            return  
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()   
        
        if self.current_screen == START_SCENE:
            self.update_start_scene()
        elif self.current_screen == PLAY_SCENE:
            self.update_play_scene()
    
    def draw_play_scene(self):
        pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)
        for carrot in self.carrot:
            carrot.draw()
        pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10, f'Score: {self.current_score}', pyxel.COLOR_PINK)
        #kalau maka carrot
        if self.is_collison:
            if not self.score_written:  
                 # Jika current_score lebih besar dari high_score, replace file
                if self.current_score > self.high_score:
                    with open("score.txt", "w") as f:
                        f.write(str(self.current_score))  
                        
                self.score_written = True  # Set flag agar tidak menulis lagi
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "EWWW carrot", pyxel.COLOR_BLACK)
    
    def draw_start_screen(self):
        pyxel.blt(0, 0, 0, 32, 0, 160, 120)
        pyxel.text(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2, "Haruka doesn't Like Carrot", pyxel.COLOR_BLACK)
        pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10 + 10, "Click to Start", pyxel.COLOR_PINK)
        pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10, f'highscore: {self.high_score}', pyxel.COLOR_WHITE)
    
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        if self.current_screen == PLAY_SCENE:
            self.draw_play_scene()
        elif self.current_screen == START_SCENE:
            self.draw_start_screen()
        
App( )