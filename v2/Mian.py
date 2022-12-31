import arcade
import Graphics
import Logic
import random

#Convention: Player1 = 1, dark ,first list item // Player2 = 0, light, second list item

class Game_Window(arcade.Window):
    def __init__(self) -> None:
        super().__init__(1200,800,"Backgammon")
        arcade.set_background_color(arcade.color.DARK_SCARLET)
        self.state = "Splash"
        self.step = 0

        self.button_slot_1_excited = False
        self.button_slot_2_excited = False

        self.game_over = False
        self.Main_Board = None
        self.currentTurn = None

    def on_draw(self):
        arcade.start_render()

        if self.state == "Splash":
            Graphics.draw_splash(self.button_slot_1_excited)
            
        if self.state == "Pre-Start":
            Graphics.draw_pre_start(self.button_slot_1_excited)
        
        if self.state == "Game-Start":
            Graphics.draw_game_start(self.button_slot_1_excited,self.Main_Board)

        if self.state == "Turn-P1":
            Graphics.draw_turn(1,self.button_slot_1_excited,self.Main_Board,self.currentTurn)

        if self.state == "Turn-P2":
            Graphics.draw_turn(0,self.button_slot_1_excited,self.Main_Board,self.currentTurn)

        if self.state == "Turn-Start-P1":
            Graphics.draw_turn_start(1,self.button_slot_1_excited,self.button_slot_2_excited,self.Main_Board)

        if self.state == "Turn-Start-P2":
            Graphics.draw_turn_start(0,self.button_slot_1_excited,self.button_slot_2_excited,self.Main_Board)

    def setup(self):
        pass

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):

        if self.state == "Splash":
            self.button_slot_1_excited = True if 525 < x < 675 and 262 < y < 338 else False

        if self.state in {"Pre-Start","Game-Start","Turn-P1","Turn-p2"}:
            self.button_slot_1_excited = True if 1025 < x < 1175 and 362 < y < 438 else False
            
        if self.state in {"Turn-Start-P1","Turn-Start-P2"}:
            self.button_slot_1_excited = True if 1025 < x < 1175 and 313 < y < 388 else False
            self.button_slot_2_excited = True if 1025 < x < 1175 and 413 < y < 488 else False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):

        if self.state == "Splash":
            if 525 < x < 675 and 262 < y < 338:
                self.state = "Pre-Start"

        elif self.state == "Pre-Start":
            if 1025 < x < 1175 and 362 < y < 438:

                #Setup Function for each time a game is started:
                self.Main_Board = Logic.Board()
                self.Main_Board.setStartPositions()

                self.state = "Game-Start"

        elif self.state == "Game-Start":
            if 1025 < x < 1175 and 362 < y < 438:
                
                #When Initial Roll Button Pressed:
                startingPlayer = random.randint(0,1)
                self.currentTurn = Logic.Turn(startingPlayer,self.Main_Board,First=True)
                self.state = "Turn-P1" if startingPlayer == 1 else "Turn-P2"

        elif self.state == "Turn-P1":

            #When the "End" button is pressed:
            if 1025 < x < 1175 and 362 < y < 438:
                self.state = "Turn-Start-P2"

        elif self.state == "Turn-P2":

            #When the "End" button is pressed:
            if 1025 < x < 1175 and 362 < y < 438:
                self.state = "Turn-Start-P1"

        elif self.state == "Turn-Start-P1":

            #If "ROLL" Button Pressed:
            if 1025 < x < 1175 and 313 < y < 388:
                self.currentTurn = Logic.Turn(1,self.Main_Board)
                self.state = "Turn-P1"

            #If "DOUBLE" Button Pressed:
            if 1025 < x < 1175 and 413 < y < 488:
                pass


        elif self.state == "Turn-Start-P2":

            #If "ROLL" Button Pressed:
            if 1025 < x < 1175 and 313 < y < 388:
                self.currentTurn = Logic.Turn(0,self.Main_Board)
                self.state = "Turn-P2"

            #If "DOUBLE" Button Pressed:
            if 1025 < x < 1175 and 413 < y < 488:
                pass


def main():
    game = Game_Window()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()