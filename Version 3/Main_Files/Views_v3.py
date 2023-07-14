import arcade
import arcade.gui
import Main_Files.Graphics_v3 as Graphics

#Main Views:
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
            print("Changing view to Simulation")
            simView = MainSimView(self.backgroundColor)
            self.window.show_view(simView)
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

        Back_button = arcade.gui.UIFlatButton(15,745,75,40,"Back")

        self.manager.add(Back_button)


        @Back_button.event("on_click")
        def on_click_Back(event):
            print("Changing view to Last Known Page")
            self.window.show_view(self.window.lastPage)


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable

    def on_draw(self):
        self.clear()
        self.manager.draw()


#Sim Views
class MainSimView(arcade.View):
    def __init__(self,backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Back_button = arcade.gui.UIFlatButton(15,745,75,40,"Exit")
        Quit_button = arcade.gui.UIFlatButton(15,695,75,40,"Quit")
        New_button  = arcade.gui.UIFlatButton(15,15,75,60,"New Game")
        Setting_button = arcade.gui.UIFlatButton(1010,15,175,40,"Settings")

        RunGame_button = arcade.gui.UIFlatButton(1010,745,175,40,"Run Game")
        RunRandomTurn_button = arcade.gui.UIFlatButton(1010,695,175,40,"Run Turn")
        RunSetTurn_button = arcade.gui.UIFlatButton(1010,645,175,40,"Run Set Turn")
        EditBoard_button = arcade.gui.UIFlatButton(1010,595,175,40,"Edit Board")
        

        self.manager.add(Back_button)
        self.manager.add(Quit_button)
        self.manager.add(New_button)
        self.manager.add(Setting_button)

        self.manager.add(RunGame_button)
        self.manager.add(RunRandomTurn_button)
        self.manager.add(RunSetTurn_button)
        self.manager.add(EditBoard_button)

        @Back_button.event("on_click")
        def on_click_Back(event):
            print("Changing view to MainMenuView")
            mainView = MainMenuView(self.backgroundColor)
            self.window.show_view(mainView)
        @Quit_button.event("on_click")
        def on_click_Quit(event):
            print("Application Quit")
            arcade.close_window()
        @Setting_button.event("on_click")
        def on_click_Setting(event):
            print("Changing view to SettingsView")
            setView = SettingsView(self.backgroundColor)
            self.window.show_view(setView)

        @EditBoard_button.event("on_click")
        def on_click_Edit(event):
            print("Changing view to EditBoardView")
            EditView = EditBoardView(self.backgroundColor)
            self.window.show_view(EditView)


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable

    def on_draw(self):
        self.clear()

        self.manager.draw()

        Graphics.drawBoard()
        Graphics.drawPieces(self.window.MainBoard.positions,self.window.MainBoard.pip)
class EditBoardView(arcade.View):
    def __init__(self,backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Done_button = arcade.gui.UIFlatButton(15,745,75,40,"Done")
        Quit_button = arcade.gui.UIFlatButton(15,695,75,40,"Quit")

        RunGame_button = arcade.gui.UIFlatButton(1010,745,175,40,"Run Game")
        RunRandomTurn_button = arcade.gui.UIFlatButton(1010,695,175,40,"Run Turn")
        RunSetTurn_button = arcade.gui.UIFlatButton(1010,645,175,40,"Run Set Turn")
        EditBoard_button = arcade.gui.UIFlatButton(1010,595,175,40,"Edit Board")
        

        self.manager.add(Done_button)
        self.manager.add(Quit_button)

        self.manager.add(RunGame_button)
        self.manager.add(RunRandomTurn_button)
        self.manager.add(RunSetTurn_button)
        self.manager.add(EditBoard_button)

        @Done_button.event("on_click")
        def on_click_Sim(event):
            print("Changing view to Simulation")
            simView = MainSimView(self.backgroundColor)
            self.window.show_view(simView)
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

        Graphics.drawBoard()
        Graphics.drawPIP((100,100))

#1P Views:


#2P Views:
class Start_2P_View(arcade.View):

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
class P1_Turn_2P_View(arcade.View):

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
class P2_Turn_2P_View(arcade.View):

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
class P1_PreTurn_2P_View(arcade.View):

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
class P1_PreTurn_2P_View(arcade.View):

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
class GameOver_2P_View(arcade.View):

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







