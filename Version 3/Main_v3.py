import arcade
import arcade.gui
import Main_Files.Views_v3 as Views
import Main_Files.Logic_v3 as Logic

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = 13, 47, 69

class MainWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(BACKGROUND_COLOR)

        self.settings = {"Agent1":"Human","Agent2":"Human","Network1 ID":None,"Network2 ID":None,"1P Inputs Rolls":False}
        self.lastPage = None
        self.MainBoard = Logic.Board()
        self.MainTurn = None
        self.nextPlayer = 0

    def setup(self):
        mainmenu_view = Views.MainMenuView(BACKGROUND_COLOR)
        self.lastPage = mainmenu_view
        self.show_view(mainmenu_view)

    def on_draw(self):
        pass

    def on_key_press(self, key, key_modifiers):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass


def main():
    mainWindow = MainWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Backgammon")
    mainWindow.setup() #Currently Unused
    arcade.run()


if __name__ == "__main__":
    main()