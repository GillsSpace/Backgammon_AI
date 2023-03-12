import arcade
import Graphics_v4 as Graphics
import Logic_v4 as Logic
import random
import time

#Set Version:
Crit_Version = 4.1

#Convention: Player1 = 1, dark ,first list item // Player2 = 0, light, second list item, first AI player

#Main Game Control Class
class Game_Window(arcade.Window):
    def __init__(self):
        super().__init__(1200,800,"Backgammon")
        arcade.set_background_color(arcade.color.DARK_SCARLET)

        self.buttons_excited = [False] * 16
        
        self.game_type = "2P"
        self.game_settings = {"1P Inputs":"Generated","Sim Delay":5,"AI Lines":True,"Display AI Info":True,"AI Player":"Random"}    

        self.state = "Splash"
        self.last_state = "Splash"
        
        self.step = "main"

        self.game_winner = None
        self.Main_Board = None
        self.Current_Turn = None

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()

        if self.state == "Splash":
            Graphics.draw_Splash(self.buttons_excited,self.game_type,Crit_Version)
        if self.state == "Settings":
            Graphics.draw_Settings(self.buttons_excited,self.game_settings)
        if self.state == "2P_PreStart":
            Graphics.draw_2P_PreStart(self.buttons_excited)
        if self.state == "2P_GameStart":
            Graphics.draw_2P_GameStart(self.buttons_excited,self.Main_Board)
        if self.state == "2P_PreTurnP1":
            Graphics.draw_2P_PreTurnP1(self.buttons_excited,self.Main_Board)
        if self.state == "2P_PreTurnP2":
            Graphics.draw_2P_PreTurnP2(self.buttons_excited,self.Main_Board)
        if self.state == "2P_TurnP1":
            Graphics.draw_2P_TurnP1(self.buttons_excited,self.Main_Board,self.currentTurn)
            Graphics.draw_2P_Turn_Main(self.currentTurn.sprites_move_start) if self.step == "main" else Graphics.draw_2P_Turn_Branch(self.currentTurn.sprite_active,self.currentTurn.sprites_move_end)
        if self.state == "2P_TurnP2":
            Graphics.draw_2P_TurnP2(self.buttons_excited,self.Main_Board,self.currentTurn)
            Graphics.draw_2P_Turn_Main(self.currentTurn.sprites_move_start) if self.step == "main" else Graphics.draw_2P_Turn_Branch(self.currentTurn.sprite_active,self.currentTurn.sprites_move_end)


    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):

        if self.state == "Splash":
            self.buttons_excited[0] = True if 375 < x < 825 and 262 < y < 338 else False
            self.buttons_excited[1] = True if 475 < x < 725 and 112 < y < 188 else False
            self.buttons_excited[2] = True if 225 < x < 475 and 112 < y < 188 else False
            self.buttons_excited[3] = True if 725 < x < 975 and 112 < y < 188 else False
            self.buttons_excited[4] = True if 1085 < x < 1165 and 685 < y < 765 else False

        if self.state == "Settings":
            self.buttons_excited[0] = True if 25 < x < 175 and 700 < y <775 else False
            self.buttons_excited[1] = True if 650 < x < 750 and 675 < y < 705 else False
            self.buttons_excited[2] = True if 775 < x < 875 and 675 < y < 705 else False
            self.buttons_excited[3] = True if 650 < x < 680 and 625 < y < 655 else False
            self.buttons_excited[4] = True if 690 < x < 720 and 625 < y < 655 else False
            self.buttons_excited[5] = True if 730 < x < 760 and 625 < y < 655 else False
            self.buttons_excited[6] = True if 770 < x < 800 and 625 < y < 655 else False
            self.buttons_excited[7] = True if 810 < x < 840 and 625 < y < 655 else False
            self.buttons_excited[8] = True if 850 < x < 880 and 625 < y < 655 else False
            self.buttons_excited[9] = True if 650 < x < 750 and 475 < y < 505 else False
            self.buttons_excited[10] = True if 775 < x < 875 and 475 < y < 505 else False
            self.buttons_excited[11] = True if 650 < x < 750 and 425 < y < 455 else False
            self.buttons_excited[12] = True if 775 < x < 875 and 425 < y < 455 else False
            self.buttons_excited[13] = True if 650 < x < 750 and 375 < y < 405 else False
            self.buttons_excited[14] = True if 775 < x < 875 and 375 < y < 405 else False
            self.buttons_excited[15] = True if 900 < x < 1000 and 375 < y < 405 else False

        if self.state in {"2P_PreStart","2P_GameStart"}:
            self.buttons_excited[0] = True if 1025 < x < 1175 and 362 < y < 438 else False
            self.buttons_excited[1] = True if 20 < x < 80 and 720 < y < 780 else False
            self.buttons_excited[2] = True if 20 < x < 80 and 650 < y < 710 else False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        
        if self.state == "Splash":
            if 375 < x < 825 and 262 < y < 338:
                if self.game_type == "2P":
                    self.state = "2P_PreStart"
                #INCOMPLETE - need other 2 game types
                arcade.play_sound(Graphics.button_click)
            if 475 < x < 725 and 112 < y < 188:
                self.game_type = "0P"
                arcade.play_sound(Graphics.button_click)
            if 225 < x < 475 and 112 < y < 188:
                self.game_type = "1P"
                arcade.play_sound(Graphics.button_click)
            if 725 < x < 975 and 112 < y < 188:
                self.game_type = "2P"
                arcade.play_sound(Graphics.button_click)
            if 1085 < x < 1165 and 685 < y < 765:
                self.state = "Settings"
                self.last_state = "Splash"
                arcade.play_sound(Graphics.button_click)

        elif self.state == "Settings":
            if 25 < x < 175 and 700 < y <775:
                self.state = self.last_state
                arcade.play_sound(Graphics.button_click)
            if 650 < x < 750 and 675 < y < 705:
                self.game_settings["1P Inputs"] = "Generated"
                arcade.play_sound(Graphics.button_click)
            if 775 < x < 875 and 675 < y < 705:
                self.game_settings["1P Inputs"] = "Inputted"
                arcade.play_sound(Graphics.button_click)
            if 650 < x < 680 and 625 < y < 655:
                self.game_settings["Sim Delay"] = 1
                arcade.play_sound(Graphics.button_click)
            if 690 < x < 720 and 625 < y < 655:
                self.game_settings["Sim Delay"] = 3
                arcade.play_sound(Graphics.button_click)
            if 730 < x < 760 and 625 < y < 655:
                self.game_settings["Sim Delay"] = 5
                arcade.play_sound(Graphics.button_click)
            if 770 < x < 800 and 625 < y < 655: 
                self.game_settings["Sim Delay"] = 7
                arcade.play_sound(Graphics.button_click)
            if 810 < x < 840 and 625 < y < 655:
                self.game_settings["Sim Delay"] = 10
                arcade.play_sound(Graphics.button_click)
            if 850 < x < 880 and 625 < y < 655:
                self.game_settings["Sim Delay"] = 15
                arcade.play_sound(Graphics.button_click)
            if 650 < x < 750 and 475 < y < 505:
                self.game_settings["AI Lines"] = True
                arcade.play_sound(Graphics.button_click)
            if 775 < x < 875 and 475 < y < 505:
                self.game_settings["AI Lines"] = False
                arcade.play_sound(Graphics.button_click)
            if 650 < x < 750 and 425 < y < 455:
                self.game_settings["Display AI Info"] = True
                arcade.play_sound(Graphics.button_click)
            if 775 < x < 875 and 425 < y < 455:
                self.game_settings["Display AI Info"] = False
                arcade.play_sound(Graphics.button_click)
            if 650 < x < 750 and 375 < y < 405:
                self.game_settings["AI Player"] = "Random"
                arcade.play_sound(Graphics.button_click)
            if 775 < x < 875 and 375 < y < 405:
                self.game_settings["AI Player"] = "Tree"
                arcade.play_sound(Graphics.button_click)
            if 900 < x < 1000 and 375 < y < 405:
                self.game_settings["AI Player"] = "DRL"
                arcade.play_sound(Graphics.button_click)

        elif self.state == "2P_PreStart":
            if 1025 < x < 1175 and 362 < y < 438:

                self.state = "2P_GameStart"
                self.Main_Board = Logic.Board()
                self.Main_Board.setStartPositions()

                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "2P_PreStart"
                arcade.play_sound(Graphics.button_click)

        elif self.state == "2P_GameStart":
            if 1025 < x < 1175 and 362 < y < 438:
                startingPlayer = random.randint(0,1)
                self.currentTurn = Logic.Turn(startingPlayer,"Human",self.game_settings,First=True)
                self.currentTurn.updatePossibleMoves(self.Main_Board)
                self.currentTurn.formSpriteList(self.Main_Board)
                
                self.state = "2P_TurnP1" if startingPlayer == 1 else "2P_TurnP2"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "2P_GameStart"
                arcade.play_sound(Graphics.button_click)

        elif self.state == "2P_PreTurnP1":
            #If "ROLL" Button Pressed:
            if 1025 < x < 1175 and 313 < y < 388:
                self.currentTurn = Logic.Turn(1,self.Main_Board,self.game_settings)
                self.currentTurn.updatePossibleMoves(self.Main_Board)
                print("Possible Moves Updated") #DEBUG
                self.currentTurn.formSpriteList(self.Main_Board)
                self.state = "2P_TurnP1"
                arcade.play_sound(Graphics.dice_roll,3)

        elif self.state == "2P_PreTurnP2":
            #If "ROLL" Button Pressed:
            if 1025 < x < 1175 and 313 < y < 388:
                self.currentTurn = Logic.Turn(0,self.Main_Board,self.game_settings)
                self.currentTurn.updatePossibleMoves(self.Main_Board)
                print("Possible Moves Updated") #DEBUG
                self.currentTurn.formSpriteList(self.Main_Board)
                self.state = "2P_TurnP2"
                arcade.play_sound(Graphics.dice_roll,3)

        elif self.state == "2P_TurnP1":
            if self.step == "main":
                #When an possible move sprite is clicked:
                clicked_sprite = arcade.get_sprites_at_point((x,y),self.currentTurn.sprites_move_start)
                if clicked_sprite != []:
                    self.currentTurn.sprite_active = clicked_sprite[0]
                    self.currentTurn.sprites_move_end = Graphics.createMoveEndSprites(self.currentTurn.sprite_active,self.Main_Board,self.currentTurn.player)
                    self.step = "branch"

            elif self.step == "branch":
                self.step = "main"
                #When a possible sub-move sprite is clicked:
                clicked_sprite = arcade.get_sprites_at_point((x,y),self.currentTurn.sprites_move_end)
                if clicked_sprite != []:
                    arcade.play_sound(Graphics.checker_move,5)
                    self.Main_Board.updateWithMove(self.currentTurn.sprite_active.move[0],clicked_sprite[0].pos,1)
                    if self.Main_Board.calcPip()[0] == 0:
                        self.state = "GameOver"
                        self.game_winner = 1
                        return
                    roll = self.currentTurn.fromMoveToRoll(self.currentTurn.sprite_active.move[0],clicked_sprite[0].pos,self.currentTurn.availableRolls,1)
                    self.currentTurn.availableRolls.remove(roll)
                    if len(self.currentTurn.availableRolls) > 0:
                        self.currentTurn.updatePossibleMoves(self.Main_Board)
                        self.currentTurn.formSpriteList(self.Main_Board)
                    else:
                        self.currentTurn.sprites_move_start = arcade.SpriteList()

            if 1025 < x < 1175 and 362 < y < 438:
                arcade.play_sound(Graphics.button_click)
                self.state = "2P_PreTurnP1"

        elif self.state == "2P_TurnP2":
            if self.step == "main":
                #When an possible move sprite is clicked:
                clicked_sprite = arcade.get_sprites_at_point((x,y),self.currentTurn.sprites_move_start)
                if clicked_sprite != []:
                    self.currentTurn.sprite_active = clicked_sprite[0]
                    self.currentTurn.sprites_move_end = Graphics.createMoveEndSprites(self.currentTurn.sprite_active,self.Main_Board,self.currentTurn.player)
                    self.step = "branch"

            elif self.step == "branch":
                self.step = "main"
                #When a possible sub-move sprite is clicked:
                clicked_sprite = arcade.get_sprites_at_point((x,y),self.currentTurn.sprites_move_end)
                if clicked_sprite != []:
                    arcade.play_sound(Graphics.checker_move,5)
                    self.Main_Board.updateWithMove(self.currentTurn.sprite_active.move[0],clicked_sprite[0].pos,0)
                    if self.Main_Board.calcPip()[1] == 0:
                        self.state = "GAME-END"
                        self.game_winner = 0
                        return
                    roll = self.currentTurn.fromMoveToRoll(self.currentTurn.sprite_active.move[0],clicked_sprite[0].pos,self.currentTurn.availableRolls,0)
                    self.currentTurn.availableRolls.remove(roll)
                    if len(self.currentTurn.availableRolls) > 0:
                        self.currentTurn.updatePossibleMoves(self.Main_Board)
                        self.currentTurn.formSpriteList(self.Main_Board)
                    else:
                        self.currentTurn.sprites_move_start = arcade.SpriteList()

            #When the "End" button is pressed:
            if 1025 < x < 1175 and 362 < y < 438:
                arcade.play_sound(Graphics.button_click)
                self.state = "2P_PreTurnP1"

        print(f"states after click: state = {self.state} // step = {self.step}") #DEBUG


#Initial Run Setup:
def main():
    game = Game_Window()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()





