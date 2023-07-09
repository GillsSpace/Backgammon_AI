import arcade
import arcade.gui

from Main_v3 import BACKGROUND_COLOR

class MainMenuView(arcade.View):

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        Title_text = arcade.gui.UILabel(text="Backgammon",font_size=75,text_color=(255,255,255))
        self.v_box.add(Title_text.with_space_around(bottom=20))
        Subtitle_text = arcade.gui.UILabel(text="by Wills Erda",font_size=30,text_color=(255,255,255))
        self.v_box.add(Subtitle_text.with_space_around(bottom=40))
        

        Sim_button = arcade.gui.UIFlatButton(text="Simulation", width = 300)
        OnePlayer_button = arcade.gui.UIFlatButton(text="One Player", width = 300)
        TwoPlayer_button = arcade.gui.UIFlatButton(text="Two Player", width = 300)
        Settings_button = arcade.gui.UIFlatButton(text="Settings", width = 300)
        Quit_button = arcade.gui.UIFlatButton(text="Quit", width = 300)

        self.v_box.add(Sim_button.with_space_around(bottom=20))
        self.v_box.add(OnePlayer_button.with_space_around(bottom=20))
        self.v_box.add(TwoPlayer_button.with_space_around(bottom=20))
        self.v_box.add(Settings_button.with_space_around(bottom=20))
        self.v_box.add(Quit_button.with_space_around(bottom=20))

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center",align_y=0,child=self.v_box))


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(BACKGROUND_COLOR)

    def on_hide_view(self):
        self.manager.disable

    def on_draw(self):
        self.clear()
        self.manager.draw()


