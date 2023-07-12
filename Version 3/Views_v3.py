import arcade
import arcade.gui

class MainMenuView(arcade.View):

    def __init__(self,backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

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

        @Sim_button.event("on_click")
        def on_click_Sim(event):
            print("Settings:", event)
        @OnePlayer_button.event("on_click")
        def on_click_OnePlayer(event):
            print("Settings:", event)
        @TwoPlayer_button.event("on_click")
        def on_click_TwoPlayer(event):
            print("Settings:", event)
        @Settings_button.event("on_click")
        def on_click_Settings(event):
            print("Changing view to Settings")
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)
        @Quit_button.event("on_click")
        def on_click_Quit(event):
            print("Application Quit")
            arcade.close_window()


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable

    def on_draw(self):
        self.clear()
        self.manager.draw()

class SettingsView(arcade.View):

    def __init__(self,backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Back_button = arcade.gui.UIFlatButton(25,725,100,50,"Back")

        self.manager.add(Back_button)


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable

    def on_draw(self):
        self.clear()
        self.manager.draw()