
import arcade
import arcade.gui
import Views_v3 as Views

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = 13, 47, 69
GAME_SETTINGS = {"Type":"0P",
                 "AI Agent 1": "Random",
                 "AI Agent 2": "Random"}

class MainWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(BACKGROUND_COLOR)

        self.settings = {"Agent1":"Human","Agent2":"Human"}
        self.lastPage = "MainMenu"

    def setup(self):
        pass

    def on_draw(self):
        pass

    def on_key_press(self, key, key_modifiers):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass


def main():
    mainWindow = MainWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Backgammon")
    mainWindow.setup() #Currently Unused
    mainmenu_view = Views.MainMenuView(BACKGROUND_COLOR)
    mainWindow.show_view(mainmenu_view)
    arcade.run()


if __name__ == "__main__":
    main()