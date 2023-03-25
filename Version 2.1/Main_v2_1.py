import arcade
import Graphics_v2_1 as Graphics
import Logic_v2_1 as Logic
import AI_v2_1 as AI
import random

#Set Version:
Crit_Version = 2.1

#Convention: Player1 = 1, dark ,first list item // Player2 = 0, light, second list item, first AI player
#            Moves: 1001 = Bar and 2002 = off

#Main Game Control Class
class Game_Window(arcade.Window):
    def __init__(self):
        super().__init__(1200,800,"Backgammon")
        arcade.set_background_color(arcade.color.DARK_SCARLET)

        self.buttons_excited = [False] * 16
        
        self.game_type = "0P"
        self.game_settings = {"1P Inputs":"Generated","Sim Delay":5,"AI Lines":True,"Display AI Info":True,"AI Player":"PBP"}   
        self.TurnNumber = 0

        self.state = "Splash"
        self.last_state = "Splash"
        
        self.step = "main"
        self.inputFor = "Human"
        self.currentRollInputs = [0,0]
        self.aiMoves = []
        self.aiMoveData = [] 

        self.Game_Winner = None
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
            Graphics.draw_2P_TurnP1(self.buttons_excited,self.Main_Board,self.Current_Turn)
            Graphics.draw_2P_Turn_Main(self.Current_Turn.sprites_move_start) if self.step == "main" else Graphics.draw_2P_Turn_Branch(self.Current_Turn.sprite_active,self.Current_Turn.sprites_move_end)
        if self.state == "2P_TurnP2":
            Graphics.draw_2P_TurnP2(self.buttons_excited,self.Main_Board,self.Current_Turn)
            Graphics.draw_2P_Turn_Main(self.Current_Turn.sprites_move_start) if self.step == "main" else Graphics.draw_2P_Turn_Branch(self.Current_Turn.sprite_active,self.Current_Turn.sprites_move_end)
        
        if self.state == "1P_PreStart":
            Graphics.draw_1P_PreStart(self.buttons_excited)
        if self.state == "1P_GameStart":
            Graphics.draw_1P_GameStart(self.buttons_excited,self.Main_Board)
        if self.state == "1P_GameStart_Inputs":
            Graphics.draw_1P_GameStart_Inputs(self.buttons_excited,self.Main_Board)
        if self.state == "1P_TurnHuman":
            Graphics.draw_1P_TurnHuman(self.buttons_excited,self.Main_Board,self.Current_Turn)
            Graphics.draw_1P_Turn_Main(self.Current_Turn.sprites_move_start) if self.step == "main" else Graphics.draw_1P_Turn_Branch(self.Current_Turn.sprite_active,self.Current_Turn.sprites_move_end)
        if self.state == "1P_TurnAI":
            Graphics.draw_1P_TurnAI(self.buttons_excited,self.Main_Board,self.Current_Turn)
            if self.game_settings["AI Lines"] == True:
                Graphics.DrawMoveLines(self.Main_Board.moveData)
        if self.state == "1P_RollInputs":
            Graphics.draw_1P_RollInputs(self.buttons_excited,self.Main_Board,self.inputFor,self.currentRollInputs)
        
        if self.state == "0P_PreStart":
            Graphics.draw_0P_PreStart(self.buttons_excited,self.Main_Board)
        if self.state == "0P_Turn":
            Graphics.draw_0P_Turn(self.buttons_excited,self.Main_Board,self.Current_Turn)
            if self.game_settings["AI Lines"] == True:
                Graphics.DrawMoveLines(self.Main_Board.moveData)

        if self.state == "GameOver":
            Graphics.draw_GameOver(self.Game_Winner,self.buttons_excited,Crit_Version,self.TurnNumber)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):

        if self.state == "Splash":
            self.buttons_excited[0] = True if 375 < x < 825 and 262 < y < 338 else False
            self.buttons_excited[1] = True if 475 < x < 725 and 112 < y < 188 else False
            self.buttons_excited[2] = True if 225 < x < 475 and 112 < y < 188 else False
            self.buttons_excited[3] = True if 725 < x < 975 and 112 < y < 188 else False
            self.buttons_excited[4] = True if 1085 < x < 1165 and 685 < y < 765 else False
            self.buttons_excited[5] = True if 35 < x < 105 and 685 < y < 765 else False

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

        if self.state in {"2P_PreStart","2P_GameStart","2P_PreTurnP1","2P_PreTurnP2","2P_TurnP1","2P_TurnP2","1P_PreStart","1P_GameStart","1P_TurnHuman","1P_TurnAI","0P_Turn"}:
            self.buttons_excited[0] = True if 1025 < x < 1175 and 362 < y < 438 else False
            self.buttons_excited[1] = True if 20 < x < 80 and 720 < y < 780 else False
            self.buttons_excited[2] = True if 20 < x < 80 and 650 < y < 710 else False

        if self.state == "1P_GameStart_Inputs":
            self.buttons_excited[0] = True if 1025 < x < 1175 and 425 < y < 575 else False
            self.buttons_excited[1] = True if 1025 < x < 1175 and 225 < y < 375 else False
            self.buttons_excited[2] = True if 20 < x < 80 and 720 < y < 780 else False
            self.buttons_excited[3] = True if 20 < x < 80 and 650 < y < 710 else False

        if self.state == "1P_RollInputs":
            self.buttons_excited[0] = True if 1035 < x < 1085 and 525 < y < 575 else False
            self.buttons_excited[1] = True if 1115 < x < 1165 and 525 < y < 575 else False
            self.buttons_excited[2] = True if 1035 < x < 1085 and 465 < y < 515 else False
            self.buttons_excited[3] = True if 1115 < x < 1165 and 465 < y < 515 else False
            self.buttons_excited[4] = True if 1035 < x < 1085 and 405 < y < 455 else False
            self.buttons_excited[5] = True if 1115 < x < 1165 and 405 < y < 455 else False
            self.buttons_excited[6] = True if 1035 < x < 1085 and 345 < y < 395 else False
            self.buttons_excited[7] = True if 1115 < x < 1165 and 345 < y < 395 else False
            self.buttons_excited[8] = True if 1035 < x < 1085 and 285 < y < 335 else False
            self.buttons_excited[9] = True if 1115 < x < 1165 and 285 < y < 335 else False
            self.buttons_excited[10] = True if 1035 < x < 1085 and 225 < y < 275 else False
            self.buttons_excited[11] = True if 1115 < x < 1165 and 225 < y < 275 else False
            self.buttons_excited[12] = True if 1025 < x < 1175 and 120 < y < 180 else False
            self.buttons_excited[13] = True if 20 < x < 80 and 720 < y < 780 else False
            self.buttons_excited[14] = True if 20 < x < 80 and 650 < y < 710 else False

        if self.state == "GameOver":
            self.buttons_excited[0] = True if 325 < x < 525 and 262 < y < 338 else False
            self.buttons_excited[1] = True if 575 < x < 775 and 262 < y < 338 else False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        
        if self.state == "Splash":
            if 375 < x < 825 and 262 < y < 338:
                if self.game_type == "2P":
                    self.state = "2P_PreStart"
                elif self.game_type == "1P":
                    self.state = "1P_PreStart"
                elif self.game_type == "0P":
                    self.Main_Board = Logic.Board()
                    self.Main_Board.setStartPositions()
                    self.state = "0P_PreStart"
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
            if 35 < x < 105 and 685 < y < 765:
                arcade.exit()

        elif self.state == "Settings":
            if 25 < x < 175 and 700 < y <775:
                self.state = self.last_state
                if self.Current_Turn != None:
                    self.Current_Turn.updateTurnSettings(self.game_settings)
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
                self.TurnNumber = 0

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
                startingPlayer = random.randint(1,2)
                self.Current_Turn = Logic.Turn(startingPlayer,"Human",self.game_settings,First=True)
                self.Current_Turn.updatePossibleMoves(self.Main_Board)
                self.Current_Turn.formSpriteList(self.Main_Board)
                
                self.state = "2P_TurnP1" if startingPlayer == 1 else "2P_TurnP2"
                arcade.play_sound(Graphics.dice_roll)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "2P_GameStart"
                arcade.play_sound(Graphics.button_click)
        elif self.state == "2P_PreTurnP1":
            #If "ROLL" Button Pressed:
            if 1025 < x < 1175 and 362 < y < 438:
                self.Current_Turn = Logic.Turn(1,"Human",self.game_settings)
                self.Current_Turn.updatePossibleMoves(self.Main_Board)
                self.Current_Turn.formSpriteList(self.Main_Board)
                self.state = "2P_TurnP1"
                arcade.play_sound(Graphics.dice_roll,3)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "2P_PreTurnP1"
                arcade.play_sound(Graphics.button_click)
        elif self.state == "2P_PreTurnP2":
            #If "ROLL" Button Pressed:
            if 1025 < x < 1175 and 362 < y < 438:
                self.Current_Turn = Logic.Turn(2,"Human",self.game_settings)
                self.Current_Turn.updatePossibleMoves(self.Main_Board)
                self.Current_Turn.formSpriteList(self.Main_Board)
                self.state = "2P_TurnP2"
                arcade.play_sound(Graphics.dice_roll,3)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "2P_PreTurnP2"
                arcade.play_sound(Graphics.button_click)
        elif self.state == "2P_TurnP1":
            if self.step == "main":
                #When an possible move sprite is clicked:
                clicked_sprite = arcade.get_sprites_at_point((x,y),self.Current_Turn.sprites_move_start)
                if clicked_sprite != []:
                    self.Current_Turn.sprite_active = clicked_sprite[0]
                    self.Current_Turn.sprites_move_end = Graphics.createMoveEndSprites(self.Current_Turn.sprite_active,self.Main_Board)
                    self.step = "branch"

            elif self.step == "branch":
                self.step = "main"
                #When a possible sub-move sprite is clicked:
                clicked_sprite = arcade.get_sprites_at_point((x,y),self.Current_Turn.sprites_move_end)
                if clicked_sprite != []:
                    arcade.play_sound(Graphics.checker_move,5)
                    self.Main_Board.updateWithMove((self.Current_Turn.sprite_active.move[0],clicked_sprite[0].pos),1)
                    if self.Main_Board.pip[0] == 0:
                        self.state = "GameOver"
                        self.Game_Winner = 1
                        return
                    roll = self.Current_Turn.fromMoveToRoll(self.Current_Turn.sprite_active.move[0],clicked_sprite[0].pos,self.Current_Turn.unused_dice,1)
                    self.Current_Turn.unused_dice.remove(roll)
                    if len(self.Current_Turn.unused_dice) > 0:
                        self.Current_Turn.updatePossibleMoves(self.Main_Board)
                        self.Current_Turn.formSpriteList(self.Main_Board)
                    else:
                        self.Current_Turn.sprites_move_start = arcade.SpriteList()

            if 1025 < x < 1175 and 362 < y < 438:
                arcade.play_sound(Graphics.button_click)
                self.state = "2P_PreTurnP2"

            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "2P_TurnP1"
                arcade.play_sound(Graphics.button_click)
        elif self.state == "2P_TurnP2":
            if self.step == "main":
                #When an possible move sprite is clicked:
                clicked_sprite = arcade.get_sprites_at_point((x,y),self.Current_Turn.sprites_move_start)
                if clicked_sprite != []:
                    self.Current_Turn.sprite_active = clicked_sprite[0]
                    self.Current_Turn.sprites_move_end = Graphics.createMoveEndSprites(self.Current_Turn.sprite_active,self.Main_Board)
                    self.step = "branch"

            elif self.step == "branch":
                self.step = "main"
                #When a possible sub-move sprite is clicked:
                clicked_sprite = arcade.get_sprites_at_point((x,y),self.Current_Turn.sprites_move_end)
                if clicked_sprite != []:
                    arcade.play_sound(Graphics.checker_move,5)
                    self.Main_Board.updateWithMove((self.Current_Turn.sprite_active.move[0],clicked_sprite[0].pos),2)
                    if self.Main_Board.pip[1] == 0:
                        self.state = "GameOver"
                        self.Game_Winner = 2
                        return
                    roll = self.Current_Turn.fromMoveToRoll(self.Current_Turn.sprite_active.move[0],clicked_sprite[0].pos,self.Current_Turn.unused_dice,0)
                    self.Current_Turn.unused_dice.remove(roll)
                    if len(self.Current_Turn.unused_dice) > 0:
                        self.Current_Turn.updatePossibleMoves(self.Main_Board)
                        self.Current_Turn.formSpriteList(self.Main_Board)
                    else:
                        self.Current_Turn.sprites_move_start = arcade.SpriteList()

            #When the "End" button is pressed:
            if 1025 < x < 1175 and 362 < y < 438:
                arcade.play_sound(Graphics.button_click)
                self.state = "2P_PreTurnP1"
            
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "2P_TurnP2"
                arcade.play_sound(Graphics.button_click)

        elif self.state == "1P_PreStart":
            if 1025 < x < 1175 and 362 < y < 438:

                self.Main_Board = Logic.Board()
                self.Main_Board.setStartPositions()
                self.state = "1P_GameStart" if self.game_settings["1P Inputs"] == "Generated" else "1P_GameStart_Inputs"
                self.TurnNumber = 0

                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "1P_PreStart"
                arcade.play_sound(Graphics.button_click)
        elif self.state == "1P_GameStart":
            if 1025 < x < 1175 and 362 < y < 438:
                startingPlayer = random.randint(1,2)

                #IF 1 - Human Player
                if startingPlayer == 1:
                    self.Current_Turn = Logic.Turn(1,"Human",self.game_settings,First=True)
                    self.Current_Turn.updatePossibleMoves(self.Main_Board)
                    self.Current_Turn.formSpriteList(self.Main_Board)

                #IF 2 - AI Player
                if startingPlayer == 2:
                    self.Current_Turn = Logic.Turn(startingPlayer,"AI",self.game_settings,First=True)
                    self.Current_Turn.updatePossibleMoves(self.Main_Board)

                    Moves = AI.Main(self.Main_Board,self.Current_Turn,self.game_settings["AI Player"])
                    self.aiMoves = Moves

                    self.Main_Board.updateWithMoves(Moves,2)
                
                self.state = "1P_TurnHuman" if startingPlayer == 1 else "1P_TurnAI"
                arcade.play_sound(Graphics.dice_roll)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "1P_GameStart"
                arcade.play_sound(Graphics.button_click)
        elif self.state == "1P_GameStart_Inputs":
            if 1025 < x < 1175 and 425 < y < 575:
                self.state = "1P_RollInputs"
                self.inputFor = "AI"
                arcade.play_sound(Graphics.button_click)
            if 1025 < x < 1175 and 225 < y < 375:
                self.state = "1P_RollInputs"
                self.inputFor = "Human"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "1P_GameStart_Inputs"
                arcade.play_sound(Graphics.button_click)
        elif self.state == "1P_TurnHuman":
            if self.step == "main":
                #When an possible move sprite is clicked:
                clicked_sprite = arcade.get_sprites_at_point((x,y),self.Current_Turn.sprites_move_start)
                if clicked_sprite != []:
                    self.Current_Turn.sprite_active = clicked_sprite[0]
                    self.Current_Turn.sprites_move_end = Graphics.createMoveEndSprites(self.Current_Turn.sprite_active,self.Main_Board)
                    self.step = "branch"

            elif self.step == "branch":
                self.step = "main"
                #When a possible sub-move sprite is clicked:
                clicked_sprite = arcade.get_sprites_at_point((x,y),self.Current_Turn.sprites_move_end)
                if clicked_sprite != []:
                    arcade.play_sound(Graphics.checker_move,5)
                    self.Main_Board.updateWithMove((self.Current_Turn.sprite_active.move[0],clicked_sprite[0].pos),1)
                    if self.Main_Board.pip[0] == 0:
                        self.state = "GameOver"
                        self.Game_Winner = 1
                        return
                    roll = self.Current_Turn.fromMoveToRoll(self.Current_Turn.sprite_active.move[0],clicked_sprite[0].pos,self.Current_Turn.unused_dice,1)
                    self.Current_Turn.unused_dice.remove(roll)
                    if len(self.Current_Turn.unused_dice) > 0:
                        self.Current_Turn.updatePossibleMoves(self.Main_Board)
                        self.Current_Turn.formSpriteList(self.Main_Board)
                    else:
                        self.Current_Turn.sprites_move_start = arcade.SpriteList()

            if 1025 < x < 1175 and 362 < y < 438:

                if self.game_settings["1P Inputs"] == "Generated":
                    self.state = "1P_TurnAI"
                    self.Current_Turn = Logic.Turn(2,"AI",self.game_settings)
                    self.Current_Turn.updatePossibleMoves(self.Main_Board)
                    Moves = AI.Main(self.Main_Board,self.Current_Turn,self.game_settings["AI Player"])
                    self.aiMoves = Moves
                    self.Main_Board.updateWithMoves(Moves,2)
                    if self.Main_Board.pip[1] == 0:
                        self.state = "GameOver"
                        self.Game_Winner = 2
                        return

                else:
                    self.state = "1P_RollInputs"
                    self.inputFor = "AI"

                arcade.play_sound(Graphics.button_click)

            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "1P_TurnHuman"
                arcade.play_sound(Graphics.button_click)
        elif self.state == "1P_TurnAI":
            if 1025 < x < 1175 and 362 < y < 438:

                if self.game_settings["1P Inputs"] == "Generated":
                    self.state = "1P_TurnHuman"
                    self.Current_Turn = Logic.Turn(1,"Human",self.game_settings)
                    self.Current_Turn.updatePossibleMoves(self.Main_Board)
                    self.Current_Turn.formSpriteList(self.Main_Board)

                else:
                    self.state = "1P_RollInputs"
                    self.inputFor = "Human"

                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "1P_TurnAI"
                arcade.play_sound(Graphics.button_click)
        elif self.state == "1P_RollInputs":
            if 1035 < x < 1085 and 525 < y < 575:
                self.currentRollInputs[0] = 1
                arcade.play_sound(Graphics.button_click)
            if 1115 < x < 1165 and 525 < y < 575:
                self.currentRollInputs[1] = 1
                arcade.play_sound(Graphics.button_click)
            if 1035 < x < 1085 and 465 < y < 515:
                self.currentRollInputs[0] = 2
                arcade.play_sound(Graphics.button_click)
            if 1115 < x < 1165 and 465 < y < 515:
                self.currentRollInputs[1] = 2
                arcade.play_sound(Graphics.button_click)
            if 1035 < x < 1085 and 405 < y < 455:
                self.currentRollInputs[0] = 3
                arcade.play_sound(Graphics.button_click)
            if 1115 < x < 1165 and 405 < y < 455:
                self.currentRollInputs[1] = 3
                arcade.play_sound(Graphics.button_click)
            if 1035 < x < 1085 and 345 < y < 395:
                self.currentRollInputs[0] = 4
                arcade.play_sound(Graphics.button_click)
            if 1115 < x < 1165 and 345 < y < 395:
                self.currentRollInputs[1] = 4
                arcade.play_sound(Graphics.button_click)
            if 1035 < x < 1085 and 285 < y < 335:
                self.currentRollInputs[0] = 5
                arcade.play_sound(Graphics.button_click)
            if 1115 < x < 1165 and 285 < y < 335:
                self.currentRollInputs[1] = 5
                arcade.play_sound(Graphics.button_click)
            if 1035 < x < 1085 and 225 < y < 275:
                self.currentRollInputs[0] = 6
                arcade.play_sound(Graphics.button_click)
            if 1115 < x < 1165 and 225 < y < 275:
                self.currentRollInputs[1] = 6
                arcade.play_sound(Graphics.button_click)
            if 1025 < x < 1175 and 120 < y < 180:
                
                if self.inputFor == "Human":
                    self.state = "1P_TurnHuman"
                    self.Current_Turn = Logic.Turn(1,"Human",self.game_settings,roll=self.currentRollInputs)
                    self.Current_Turn.updatePossibleMoves(self.Main_Board)
                    self.Current_Turn.formSpriteList(self.Main_Board)

                if self.inputFor == "AI":
                    self.state = "1P_TurnAI"
                    self.Current_Turn = Logic.Turn(2,"AI",self.game_settings,roll=self.currentRollInputs)
                    self.Current_Turn.updatePossibleMoves(self.Main_Board)
                    Moves = AI.Main(self.Main_Board,self.Current_Turn)
                    self.aiMoves = Moves
                    self.Main_Board.updateWithMoves(Moves,2)
                    if self.Main_Board.pip[1] == 0:
                        self.state = "GameOver"
                        self.Game_Winner = 2
                        return

                arcade.play_sound(Graphics.button_click)

            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "1P_RollInputs"
                arcade.play_sound(Graphics.button_click)

        elif self.state == "0P_PreStart":
            if 1025 < x < 1175 and 362 < y < 438:
                startingPlayer = random.randint(1,2)
                self.TurnNumber = 0
                
                self.Current_Turn = Logic.Turn(startingPlayer,"AI",self.game_settings,First=True)
                self.Current_Turn.updatePossibleMovesAI(self.Main_Board)

                Moves = AI.Main(self.Main_Board,self.Current_Turn,self.game_settings["AI Player"])
                self.aiMoves = Moves
                self.Main_Board.updateWithMoves(Moves,self.Current_Turn.player)

                self.state = "0P_Turn"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "0P_PreStart"
                arcade.play_sound(Graphics.button_click)
        elif self.state == "0P_Turn":
        
            if 1025 < x < 1175 and 362 < y < 438:
                nextPlayer = 1 if self.Current_Turn.player == 2 else 2
                self.Current_Turn = Logic.Turn(nextPlayer,"AI",self.game_settings)
                self.Current_Turn.updatePossibleMovesAI(self.Main_Board)

                Moves = AI.Main(self.Main_Board,self.Current_Turn,self.game_settings["AI Player"])
                self.aiMoves = Moves
                self.Main_Board.updateWithMoves(Moves,self.Current_Turn.player)
                self.TurnNumber = self.TurnNumber + 1

                if self.Main_Board.pip[0 if self.Current_Turn.player == 1 else 1] == 0:
                    self.state = "GameOver"
                    self.Game_Winner = 1 if self.Current_Turn.player == 1 else 2
                    return

                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 720 < y < 780:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 20 < x < 80 and 650 < y < 710:
                self.state = "Settings"
                self.last_state = "0P_Turn"
                arcade.play_sound(Graphics.button_click)

        elif self.state == "GameOver":
            if 325 < x < 525 and 262 < y < 338:
                self.state = "Splash"
                arcade.play_sound(Graphics.button_click)
            if 575 < x < 775 and 262 < y < 338:
                arcade.exit()

#Initial Run Setup:
def main():
    game = Game_Window()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()


