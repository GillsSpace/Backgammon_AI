import arcade, random
import arcade.gui
import Main_Files.Graphics_v3 as Graphics
import Main_Files.Logic_v3 as Logic

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
            self.window.MainBoard.setStartPositions()
            simView = MainSimView(self.backgroundColor)
            self.window.show_view(simView)
        @OnePlayer_button.event("on_click")
        def on_click_OnePlayer(event):
            print("Settings:", event)
        @TwoPlayer_button.event("on_click")
        def on_click_TwoPlayer(event):
            print("Changing view to 2 Player Start")
            self.window.MainBoard.setStartPositions()
            startView = Start_2P_View(self.backgroundColor)
            self.window.show_view(startView)
        @Settings_button.event("on_click")
        def on_click_Settings(event):
            print("Changing view to Settings")
            self.window.lastPage = self
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
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
class SettingsView(arcade.View):

    def __init__(self,backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIGrid

        Back_button = arcade.gui.UIFlatButton(15,745,75,40,"Back")
        Quit_button = arcade.gui.UIFlatButton(15,695,75,40,"Quit")

        AIAgent1_label = arcade.gui.UILabel()

        self.manager.add(Back_button)
        self.manager.add(Quit_button)


        @Back_button.event("on_click")
        def on_click_Back(event):
            print("Changing view to Last Known Page")
            self.window.show_view(self.window.lastPage)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            print("Application Quit")
            arcade.close_window()


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()


#Sim Views:
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
        @New_button.event("on_click")
        def on_click_New(event):
            self.window.MainBoard.setStartPositions()
        @Setting_button.event("on_click")
        def on_click_Settings(event):
            print("Changing view to Settings")
            self.window.lastPage = self
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)

        @EditBoard_button.event("on_click")
        def on_click_Edit(event):
            print("Changing view to EditBoardView")
            EditView = EditBoardView(self.backgroundColor)
            self.window.show_view(EditView)


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        self.manager.draw()

        Graphics.drawBoard()
        Graphics.drawPieces(self.window.MainBoard.positions,self.window.MainBoard.pip)
class EditBoardView(arcade.View):
    def __init__(self,backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.tool = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Done_button = arcade.gui.UIFlatButton(15,745,75,40,"Done")
        Quit_button = arcade.gui.UIFlatButton(15,695,75,40,"Quit")

        light_button = arcade.gui.UITextureButton(1010,510,75,75,Graphics.lightPiece_icon,Graphics.lightPiece_icon2,Graphics.lightPiece_icon3)
        dark_button = arcade.gui.UITextureButton(1010,420,75,75,Graphics.darkPiece_icon,Graphics.darkPiece_icon2,Graphics.darkPiece_icon3)
        delete_button = arcade.gui.UITextureButton(1010,330,75,75,Graphics.delete_icon,Graphics.delete_icon2,Graphics.delete_icon3)
        restart_button = arcade.gui.UITextureButton(1010,240,75,75,Graphics.restart_icon,Graphics.restart_icon2,Graphics.restart_icon3)

        Edit_button = arcade.gui.UIFlatButton(1010,15,175,40,"Edit as String")

        light_label = arcade.gui.UITextArea(1100,525,90,45,"Add Light",font_size=15)
        dark_label = arcade.gui.UITextArea(1100,435,90,45,"Add    Dark",font_size=15)
        delete_label = arcade.gui.UITextArea(1100,345,90,45,"Delete Piece",font_size=15)
        restart_label = arcade.gui.UITextArea(1100,255,90,45,"Delete All",font_size=15)
        

        self.manager.add(Done_button)
        self.manager.add(Quit_button)

        self.manager.add(light_button)
        self.manager.add(dark_button)
        self.manager.add(delete_button)
        self.manager.add(restart_button)

        self.manager.add(light_label)
        self.manager.add(dark_label)
        self.manager.add(delete_label)
        self.manager.add(restart_label)

        self.manager.add(Edit_button)

        @Done_button.event("on_click")
        def on_click_Done(event):
            print("Changing view to Simulation")
            simView = MainSimView(self.backgroundColor)
            self.window.show_view(simView)
        @Quit_button.event("on_click")
        def on_click_Quit(event):
            print("Application Quit")
            arcade.close_window()

        @light_button.event("on_click")
        def on_click_light(event):
            self.tool = "Light"
        @dark_button.event("on_click")
        def on_click_dark(event):
            self.tool = "Dark"
        @delete_button.event("on_click")
        def on_click_light(event):
            self.tool = "Delete"
        @restart_button.event("on_click")
        def on_click_light(event):
            self.window.MainBoard.positions = [0] * 28 

        @Edit_button.event("on_click")
        def on_click_Edit(event):
            print("Changing view to Edit as String View")
            editView = EditAsString_View(self.backgroundColor)
            self.window.show_view(editView)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        self.manager.draw()

        Graphics.drawBoard()
        Graphics.drawPieces(self.window.MainBoard.positions,self.window.MainBoard.pip)
class EditAsString_View(arcade.View):

    def __init__(self,backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        stringList = [str(num) for num in self.window.MainBoard.positions]
        string = ", ".join(stringList)

        Done_button = arcade.gui.UIFlatButton(550,300,100,50,"Done")
        text_input = arcade.gui.UIInputText(325,375,600,50,string)

        self.manager.add(Done_button)
        self.manager.add(text_input)

        @Done_button.event("on_click")
        def on_click_Done(event):
            print("Changing view to EditBoardView")

            stringList = text_input.text.rsplit(sep=", ")
            self.window.MainBoard.positions = [int(num) for num in stringList]

            editView = EditBoardView(self.backgroundColor)
            self.window.show_view(editView)


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(600,400,600,50,Graphics.board_color)
        arcade.draw_rectangle_outline(600,400,600,50,Graphics.board_color,6)

        self.manager.draw()
#1P Views:


#2P Views:
class Start_2P_View(arcade.View):
    def __init__(self,backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Back_button = arcade.gui.UIFlatButton(15,745,75,40,"Back")
        Quit_button = arcade.gui.UIFlatButton(15,695,75,40,"Quit")
        Roll_button = arcade.gui.UIFlatButton(400,375,125,50,"Roll")
        Settings_button = arcade.gui.UIFlatButton(700,375,125,50,"Settings")

        self.manager.add(Back_button)
        self.manager.add(Quit_button)
        self.manager.add(Roll_button)
        self.manager.add(Settings_button)

        @Back_button.event("on_click")
        def on_click_back(event):
            print("Changing view to Main Menu")
            mainmenuView = MainMenuView(self.backgroundColor)
            self.window.show_view(mainmenuView)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            print("Application Quit")
            arcade.close_window()

        @Roll_button.event("on_click")
        def on_click_roll(event):
            firstPlayer = random.randint(1,2)

            self.window.MainTurn = Logic.Turn(firstPlayer,"Human",First=True)
            self.window.MainTurn.updatePossibleMovesHumanFormat(self.window.MainBoard)
            self.window.MainTurn.formSpriteList(self.window.MainBoard)

            if firstPlayer == 1:
                player1view = P1_Turn_2P_View(self.backgroundColor)
                self.window.show_view(player1view)
            else:
                player2view = P2_Turn_2P_View(self.backgroundColor)
                self.window.show_view(player2view)


        @Settings_button.event("on_click")
        def on_click_Settings(event):
            print("Changing view to Settings")
            self.window.lastPage = self
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        Graphics.drawBoard()
        Graphics.drawPieces(self.window.MainBoard.positions,self.window.MainBoard.pip)
        self.manager.draw()
class P1_Turn_2P_View(arcade.View):

    def __init__(self,backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Exit_button = arcade.gui.UIFlatButton(15,745,75,40,"Exit")
        Quit_button = arcade.gui.UIFlatButton(15,695,75,40,"Quit")
        Settings_button = arcade.gui.UIFlatButton(1010,15,175,40,"Settings")

        self.manager.add(Exit_button)
        self.manager.add(Quit_button)
        self.manager.add(Settings_button)

        @Exit_button.event("on_click")
        def on_click_exit(event):
            print("Changing view to Main Menu")
            mainmenuView = MainMenuView(self.backgroundColor)
            self.window.show_view(mainmenuView)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            print("Application Quit")
            arcade.close_window()

        @Settings_button.event("on_click")
        def on_click_Settings(event):
            print("Changing view to Settings")
            self.window.lastPage = self
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        Graphics.drawBoard()
        Graphics.drawPieces(self.window.MainBoard.positions,self.window.MainBoard.pip)
        Graphics.drawDice(self.window.MainTurn.roll[0],self.window.MainTurn.roll[1],self.window.MainTurn.unused_dice)
        arcade.draw_rectangle_filled(601,401,12,762,Graphics.checkerColor1)
class P2_Turn_2P_View(arcade.View):

    def __init__(self,backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Exit_button = arcade.gui.UIFlatButton(15,745,75,40,"Exit")
        Quit_button = arcade.gui.UIFlatButton(15,695,75,40,"Quit")
        Settings_button = arcade.gui.UIFlatButton(1010,15,175,40,"Settings")

        self.manager.add(Exit_button)
        self.manager.add(Quit_button)
        self.manager.add(Settings_button)

        @Exit_button.event("on_click")
        def on_click_exit(event):
            print("Changing view to Main Menu")
            mainmenuView = MainMenuView(self.backgroundColor)
            self.window.show_view(mainmenuView)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            print("Application Quit")
            arcade.close_window()

        @Settings_button.event("on_click")
        def on_click_Settings(event):
            print("Changing view to Settings")
            self.window.lastPage = self
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)


    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        Graphics.drawBoard()
        Graphics.drawPieces(self.window.MainBoard.positions,self.window.MainBoard.pip)
        Graphics.drawDice(self.window.MainTurn.roll[0],self.window.MainTurn.roll[1],self.window.MainTurn.unused_dice)
        arcade.draw_rectangle_filled(601,401,12,762,Graphics.checkerColor2)
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
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
class P2_PreTurn_2P_View(arcade.View):

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
        self.manager.disable()

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
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()




