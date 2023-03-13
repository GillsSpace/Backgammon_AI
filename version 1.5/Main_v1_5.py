#Imports:
import arcade
import Graphics_v1_5 as Graphics
import Logic_v1_5 as Logic
import AI_v1_5 as AI
import random
import time

#Convention: Player1 = 1, dark ,first list item // Player2 = 0, light, second list item, first AI player

#Game Loop:
class Game_Window(arcade.Window):
    def __init__(self) -> None:
        super().__init__(1200,800,"Backgammon")
        arcade.set_background_color(arcade.color.DARK_SCARLET)

        self.game_type = "0P"

        self.state = "Splash"
        self.step = "main"

        self.button_slot_1_excited = False
        self.button_slot_2_excited = False
        self.button_slot_3_excited = False
        self.button_slot_4_excited = False

        self.game_winner = None
        self.Main_Board = None
        self.currentTurn = None

    def on_draw(self):
        arcade.start_render()

        if self.state == "Splash":
            Graphics.draw_splash(self.button_slot_1_excited,self.button_slot_2_excited,self.button_slot_3_excited,self.button_slot_4_excited,self.game_type)
            
        if self.state == "Pre-Start":
            Graphics.draw_pre_start(self.button_slot_1_excited)
        
        if self.state == "Game-Start":
            Graphics.draw_game_start(self.button_slot_1_excited,self.Main_Board)

        if self.state == "Turn-P1":
            Graphics.draw_turn(1,self.button_slot_1_excited,self.Main_Board,self.currentTurn)
            if self.game_type in {"2P","1P"}:
                Graphics.draw_turn_main(self.currentTurn.sprites_move_start) if self.step == "main" else Graphics.draw_turn_branch(self.currentTurn.sprite_active,self.currentTurn.sprites_move_end)

        if self.state == "Turn-P2":
            Graphics.draw_turn(0,self.button_slot_1_excited,self.Main_Board,self.currentTurn)
            if self.game_type == "2P":
                Graphics.draw_turn_main(self.currentTurn.sprites_move_start) if self.step == "main" else Graphics.draw_turn_branch(self.currentTurn.sprite_active,self.currentTurn.sprites_move_end)

        if self.state == "Turn-Start-P1":
            Graphics.draw_turn_start(1,self.button_slot_1_excited,self.button_slot_2_excited,self.Main_Board)

        if self.state == "Turn-Start-P2":
            Graphics.draw_turn_start(0,self.button_slot_1_excited,self.button_slot_2_excited,self.Main_Board)

        if self.state == "GAME-END":
            Graphics.draw_Game_Over(self.game_winner,self.button_slot_1_excited)

    def setup(self):
        pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):

        if self.state in {"Splash"}:
            self.button_slot_1_excited = True if 375 < x < 825 and 262 < y < 338 else False
            self.button_slot_2_excited = True if 475 < x < 725 and 112 < y < 188 else False
            self.button_slot_3_excited = True if 225 < x < 475 and 112 < y < 188 else False
            self.button_slot_4_excited = True if 725 < x < 975 and 112 < y < 188 else False

        if self.state in {"GAME_END"}:
            self.button_slot_1_excited = True if 525 < x < 675 and 262 < y < 338 else False

        if self.state in {"Pre-Start","Game-Start","Turn-P1","Turn-p2"}:
            self.button_slot_1_excited = True if 1025 < x < 1175 and 362 < y < 438 else False
            
        if self.state in {"Turn-Start-P1","Turn-Start-P2"}:
            self.button_slot_1_excited = True if 1025 < x < 1175 and 313 < y < 388 else False
            self.button_slot_2_excited = True if 1025 < x < 1175 and 413 < y < 488 else False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):

        #General State Changes:
        if self.state == "Splash":
            if 375 < x < 825 and 262 < y < 338:
                self.state = "Pre-Start"
                print("State Now Pre-start") #DEBUG
                arcade.play_sound(Graphics.playSound,0.4)
            if 475 < x < 725 and 112 < y < 188:
                self.game_type = "0P"
                arcade.play_sound(Graphics.clickSound,3)
            if 225 < x < 475 and 112 < y < 188:
                self.game_type = "1P"
                arcade.play_sound(Graphics.clickSound,3)
            if 725 < x < 975 and 112 < y < 188:
                self.game_type = "2P"
                arcade.play_sound(Graphics.clickSound,3)

        elif self.state == "Pre-Start":
            if 1025 < x < 1175 and 362 < y < 438:

                #Setup Function for each time a game is started:
                self.Main_Board = Logic.Board()
                self.Main_Board.setStartPositions()

                self.state = "Game-Start"
                print("State Now Game-start") #DEBUG
                arcade.play_sound(Graphics.playSound,0.4)

        elif self.state == "Game-Start":
            if 1025 < x < 1175 and 362 < y < 438:
                
                #When Initial Roll Button Pressed:
                startingPlayer = random.randint(0,1)
                self.currentTurn = Logic.Turn(startingPlayer,First=True)
                self.currentTurn.updatePossibleMoves(self.Main_Board)
                if self.game_type == "2P" or (self.game_type == "1P" and startingPlayer == 1):
                    self.currentTurn.FormSpriteLists(self.Main_Board)
                self.state = "Turn-P1" if startingPlayer == 1 else "Turn-P2"
                if self.state == "Turn-P1" and self.game_type in {"0P"}:
                    turnMoves = AI.main(self.currentTurn,self.Main_Board)
                    if self.currentTurn.doublesTurn == True:
                        for i in range(4):
                            self.Main_Board.updateWithMove(turnMoves[i][0],turnMoves[i][1],1)
                            arcade.play_sound(Graphics.basicMoveSound,5)
                    else:
                        for i in range(2):
                            self.Main_Board.updateWithMove(turnMoves[i][0],turnMoves[i][1],1)
                            arcade.play_sound(Graphics.basicMoveSound,5)
                if self.state == "Turn-P2" and self.game_type in {"0P", "1P"}:
                    turnMoves = AI.main(self.currentTurn,self.Main_Board)
                    if self.currentTurn.doublesTurn == True:
                        for i in range(4):
                            self.Main_Board.updateWithMove(turnMoves[i][0],turnMoves[i][1],0)
                            arcade.play_sound(Graphics.basicMoveSound,5)
                    else:
                        for i in range(2):
                            self.Main_Board.updateWithMove(turnMoves[i][0],turnMoves[i][1],0)
                            arcade.play_sound(Graphics.basicMoveSound,5)

                arcade.play_sound(Graphics.diceSound,3)

        elif self.state == "Turn-P1":

            if self.game_type in {"2P","1P"}:

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
                        arcade.play_sound(Graphics.basicMoveSound,5)
                        self.Main_Board.updateWithMove(self.currentTurn.sprite_active.move[0],clicked_sprite[0].pos,1)
                        if self.Main_Board.calcPip()[0] == 0:
                            self.state = "GAME-END"
                            self.game_winner = 1
                            return
                        roll = self.currentTurn.fromMoveToRoll(self.currentTurn.sprite_active.move[0],clicked_sprite[0].pos,self.currentTurn.availableRolls,1)
                        self.currentTurn.availableRolls.remove(roll)
                        if len(self.currentTurn.availableRolls) > 0:
                            self.currentTurn.updatePossibleMoves(self.Main_Board)
                            self.currentTurn.FormSpriteLists(self.Main_Board)
                        else:
                            self.currentTurn.sprites_move_start = arcade.SpriteList()

            else:
                pass

            #When the "End" button is pressed:
            if 1025 < x < 1175 and 362 < y < 438:
                arcade.play_sound(Graphics.clickSound,3)
                if self.game_type in {"0P", "1P"}:
                    arcade.play_sound(Graphics.diceSound,3)
                    self.currentTurn = Logic.Turn(0,self.Main_Board)
                    self.currentTurn.updatePossibleMoves(self.Main_Board)

                    turnMoves = AI.main(self.currentTurn,self.Main_Board)
                    if self.currentTurn.doublesTurn == True:
                        for i in range(4):
                            self.Main_Board.updateWithMove(turnMoves[i][0],turnMoves[i][1],0)
                            arcade.play_sound(Graphics.basicMoveSound,5)
                    else:
                        for i in range(2):
                            self.Main_Board.updateWithMove(turnMoves[i][0],turnMoves[i][1],0)
                            arcade.play_sound(Graphics.basicMoveSound,5)

                    self.state = "Turn-P2"
                    print("State Now Turn-P2") #DEBUG

                else:
                    self.state = "Turn-Start-P2"

        elif self.state == "Turn-P2":

            if self.game_type == "2P":

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
                        arcade.play_sound(Graphics.basicMoveSound,5)
                        self.Main_Board.updateWithMove(self.currentTurn.sprite_active.move[0],clicked_sprite[0].pos,0)
                        if self.Main_Board.calcPip()[1] == 0:
                            self.state = "GAME-END"
                            self.game_winner = 0
                            return
                        roll = self.currentTurn.fromMoveToRoll(self.currentTurn.sprite_active.move[0],clicked_sprite[0].pos,self.currentTurn.availableRolls,0)
                        self.currentTurn.availableRolls.remove(roll)
                        if len(self.currentTurn.availableRolls) > 0:
                            self.currentTurn.updatePossibleMoves(self.Main_Board)
                            self.currentTurn.FormSpriteLists(self.Main_Board)
                        else:
                            self.currentTurn.sprites_move_start = arcade.SpriteList()

            else:
                pass

            #When the "End" button is pressed:
            if 1025 < x < 1175 and 362 < y < 438:
                arcade.play_sound(Graphics.clickSound,3)
                if self.game_type == "0P":
                    arcade.play_sound(Graphics.diceSound,3)
                    self.currentTurn = Logic.Turn(1,self.Main_Board)
                    self.currentTurn.updatePossibleMoves(self.Main_Board)

                    turnMoves = AI.main(self.currentTurn,self.Main_Board)
                    if self.currentTurn.doublesTurn == True:
                        for i in range(4):
                            self.Main_Board.updateWithMove(turnMoves[i][0],turnMoves[i][1],1)
                            arcade.play_sound(Graphics.basicMoveSound,5)
                    else:
                        for i in range(2):
                            self.Main_Board.updateWithMove(turnMoves[i][0],turnMoves[i][1],1)
                            arcade.play_sound(Graphics.basicMoveSound,5)

                    self.state = "Turn-P1"
                    print("State Now Turn-P1") #DEBUG

                else:
                    self.state = "Turn-Start-P1"

        elif self.state == "Turn-Start-P1":

            #If "ROLL" Button Pressed:
            if 1025 < x < 1175 and 313 < y < 388:
                self.currentTurn = Logic.Turn(1,self.Main_Board)
                self.currentTurn.updatePossibleMoves(self.Main_Board)
                self.currentTurn.FormSpriteLists(self.Main_Board)
                self.state = "Turn-P1"
                arcade.play_sound(Graphics.diceSound,3)

            #If "DOUBLE" Button Pressed:
            if 1025 < x < 1175 and 413 < y < 488:
                pass


        elif self.state == "Turn-Start-P2":

            #If "ROLL" Button Pressed:
            if 1025 < x < 1175 and 313 < y < 388:
                self.currentTurn = Logic.Turn(0,self.Main_Board)
                self.currentTurn.updatePossibleMoves(self.Main_Board)
                self.currentTurn.FormSpriteLists(self.Main_Board)
                self.state = "Turn-P2"
                arcade.play_sound(Graphics.diceSound,3)

            #If "DOUBLE" Button Pressed:
            if 1025 < x < 1175 and 413 < y < 488:
                pass

        elif self.state == "GAME-END":
            if 525 < x < 675 and 262 < y < 338:
                self.state = "Pre-Start"
                arcade.play_sound(Graphics.clickSound,3)

def main():
    game = Game_Window()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
