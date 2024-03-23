import arcade
import arcade.gui

try:
    from Main_Files import Logic as Logic
    from Main_Files import Views as Views
except ModuleNotFoundError:
    from willse_backgammon.Main_Files import Logic as Logic
    from willse_backgammon.Main_Files import Views as Views

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = 13, 47, 69


class MainWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(BACKGROUND_COLOR)

        self.settings = {"Agent1": "Human", "Agent2": "Human", "Network1 ID": "V1.0-NV1-1.01",
                         "Network2 ID": "V1.0-NV1-1.01", "1P Inputs Rolls": False}
        self.lastPage = None
        self.MainBoard = Logic.Board()
        self.MainTurn = None
        self.nextPlayer = 0
        self.firstTurn = True

    def setup(self):
        main_menu_view = Views.MainMenuView(BACKGROUND_COLOR)
        self.lastPage = main_menu_view
        self.show_view(main_menu_view)

    def on_draw(self):
        pass

    def on_key_press(self, key, key_modifiers):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass


def main():
    main_window = MainWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Backgammon")
    main_window.setup()  # Currently Unused
    arcade.run()


if __name__ == "__main__":
    main()
