import Code.Main_Files.AI as AI
import Code.Main_Files.Graphics as Graphics
import Code.Main_Files.Logic as Logic
import arcade
import arcade.gui
import random


# Main Views:
class MainMenuView(arcade.View):

    def __init__(self, background_color):
        super().__init__()
        self.backgroundColor = background_color

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        title_text = arcade.gui.UILabel(text="Backgammon", font_size=75, text_color=(255, 255, 255))
        self.v_box.add(title_text.with_space_around(bottom=20))
        subtitle_text = arcade.gui.UILabel(text="by Wills Erda", font_size=30, text_color=(255, 255, 255))
        self.v_box.add(subtitle_text.with_space_around(bottom=40))

        sim_button = arcade.gui.UIFlatButton(text="Simulation", width=300)
        one_player_button = arcade.gui.UIFlatButton(text="One Player", width=300)
        two_player_button = arcade.gui.UIFlatButton(text="Two Player", width=300)
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=300)
        quit_button = arcade.gui.UIFlatButton(text="Quit", width=300)

        self.v_box.add(sim_button.with_space_around(bottom=20))
        self.v_box.add(one_player_button.with_space_around(bottom=20))
        self.v_box.add(two_player_button.with_space_around(bottom=20))
        self.v_box.add(settings_button.with_space_around(bottom=20))
        self.v_box.add(quit_button.with_space_around(bottom=20))

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center", align_y=0, child=self.v_box))

        @sim_button.event("on_click")
        def on_click_Sim(event):
            self.window.MainBoard.setStartPositions()
            self.window.settings["Agent1"] = "TS 1" if self.window.settings["Agent1"] == "Human" else \
            self.window.settings["Agent1"]
            self.window.settings["Agent2"] = "TS 1" if self.window.settings["Agent2"] == "Human" else \
            self.window.settings["Agent2"]
            simView = MainSimView(self.backgroundColor)
            self.window.show_view(simView)

        @one_player_button.event("on_click")
        def on_click_OnePlayer(event):
            pass

        @two_player_button.event("on_click")
        def on_click_TwoPlayer(event):
            self.window.MainBoard.setStartPositions()
            startView = Start_2P_View(self.backgroundColor)
            self.window.show_view(startView)

        @settings_button.event("on_click")
        def on_click_Settings(event):
            self.window.lastPage = self
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)

        @quit_button.event("on_click")
        def on_click_Quit(event):
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

    def __init__(self, backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Settings_label = arcade.gui.UILabel(100, 625, 1100, 150, "Settings", font_size=30, align="center", bold=True)
        Help_label = arcade.gui.UILabel(100, 0, 1100, 20, "*Agent 1 is used for single player games*", font_size=10, align="center", bold=True)

        Back_button = arcade.gui.UIFlatButton(15, 745, 75, 40, "Back")
        Quit_button = arcade.gui.UIFlatButton(15, 695, 75, 40, "Quit")

        AIAgent1_label = arcade.gui.UILabel(165, 635, 100, 50, "Agent 1:", font_size=15, text_color=Graphics.black,
                                            bold=True)
        AIAgent2_label = arcade.gui.UILabel(165, 560, 100, 50, "Agent 2:", font_size=15, text_color=Graphics.black,
                                            bold=True)

        AIAgent1_Option1_button = arcade.gui.UIFlatButton(265, 655, 100, 40, "Human")
        AIAgent1_Option2_button = arcade.gui.UIFlatButton(380, 655, 100, 40, "Random")
        AIAgent1_Option3_button = arcade.gui.UIFlatButton(495, 655, 100, 40, "PBP")
        AIAgent1_Option4_button = arcade.gui.UIFlatButton(610, 655, 100, 40, "TS 1")
        AIAgent1_Option5_button = arcade.gui.UIFlatButton(725, 655, 100, 40, "TS 2")
        AIAgent1_Option6_button = arcade.gui.UIFlatButton(840, 655, 100, 40, "Network:")

        AIAgent2_Option2_button = arcade.gui.UIFlatButton(380, 580, 100, 40, "Random")
        AIAgent2_Option3_button = arcade.gui.UIFlatButton(495, 580, 100, 40, "PBP")
        AIAgent2_Option1_button = arcade.gui.UIFlatButton(265, 580, 100, 40, "Human")
        AIAgent2_Option4_button = arcade.gui.UIFlatButton(610, 580, 100, 40, "TS 1")
        AIAgent2_Option5_button = arcade.gui.UIFlatButton(725, 580, 100, 40, "TS 2")
        AIAgent2_Option6_button = arcade.gui.UIFlatButton(840, 580, 100, 40, "Network:")

        NetworkID1 = arcade.gui.UIInputText(955, 645, 150, 40, self.window.settings["Network1 ID"])
        NetworkID2 = arcade.gui.UIInputText(955, 570, 150, 40, self.window.settings["Network2 ID"])

        self.manager.add(Back_button)
        self.manager.add(Quit_button)

        self.manager.add(Settings_label)
        self.manager.add(Help_label)
        self.manager.add(AIAgent1_label)
        self.manager.add(AIAgent2_label)

        self.manager.add(AIAgent1_Option1_button)
        self.manager.add(AIAgent1_Option2_button)
        self.manager.add(AIAgent1_Option3_button)
        self.manager.add(AIAgent1_Option4_button)
        self.manager.add(AIAgent1_Option5_button)
        self.manager.add(AIAgent1_Option6_button)

        self.manager.add(AIAgent2_Option1_button)
        self.manager.add(AIAgent2_Option2_button)
        self.manager.add(AIAgent2_Option3_button)
        self.manager.add(AIAgent2_Option4_button)
        self.manager.add(AIAgent2_Option5_button)
        self.manager.add(AIAgent2_Option6_button)

        self.manager.add(NetworkID1)
        self.manager.add(NetworkID2)

        @Back_button.event("on_click")
        def on_click_Back(event):
            self.window.settings["Network1 ID"] = NetworkID1.text
            self.window.settings["Network2 ID"] = NetworkID2.text
            self.window.show_view(self.window.lastPage)
            print(f" Current Settings: {self.window.settings}")  # DEBUG

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            arcade.close_window()

        @AIAgent1_Option1_button.event("on_click")
        def on_click_Option1(event):
            self.window.settings["Agent1"] = "Human"

        @AIAgent1_Option2_button.event("on_click")
        def on_click_Option2(event):
            self.window.settings["Agent1"] = "Random"

        @AIAgent1_Option3_button.event("on_click")
        def on_click_Option3(event):
            self.window.settings["Agent1"] = "PBP"

        @AIAgent1_Option4_button.event("on_click")
        def on_click_Option4(event):
            self.window.settings["Agent1"] = "TS 1"

        @AIAgent1_Option5_button.event("on_click")
        def on_click_Option5(event):
            self.window.settings["Agent1"] = "TS 2"

        @AIAgent1_Option6_button.event("on_click")
        def on_click_Option6(event):
            self.window.settings["Agent1"] = "Network"

        @AIAgent2_Option1_button.event("on_click")
        def on_click_Option1(event):
            self.window.settings["Agent2"] = "Human"

        @AIAgent2_Option2_button.event("on_click")
        def on_click_Option2(event):
            self.window.settings["Agent2"] = "Random"

        @AIAgent2_Option3_button.event("on_click")
        def on_click_Option3(event):
            self.window.settings["Agent2"] = "PBP"

        @AIAgent2_Option4_button.event("on_click")
        def on_click_Option4(event):
            self.window.settings["Agent2"] = "TS 1"

        @AIAgent2_Option5_button.event("on_click")
        def on_click_Option5(event):
            self.window.settings["Agent2"] = "TS 2"

        @AIAgent2_Option6_button.event("on_click")
        def on_click_Option6(event):
            self.window.settings["Agent2"] = "Network"

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        Graphics.DrawSettings(self.window.settings)

        self.manager.draw()


# Sim Views:
class MainSimView(arcade.View):
    def __init__(self, backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Back_button = arcade.gui.UIFlatButton(15, 745, 75, 40, "Exit")
        Quit_button = arcade.gui.UIFlatButton(15, 695, 75, 40, "Quit")
        New_button = arcade.gui.UIFlatButton(15, 15, 75, 60, "New Game")
        Setting_button = arcade.gui.UIFlatButton(1010, 15, 175, 40, "Settings")

        RunGame_button = arcade.gui.UIFlatButton(1010, 745, 175, 40, "Run Game")
        RunRandomTurn_button = arcade.gui.UIFlatButton(1010, 695, 175, 40, "Run Turn")
        RunSetTurn_button = arcade.gui.UIFlatButton(1010, 645, 175, 40, "Run Set Turn")
        EditBoard_button = arcade.gui.UIFlatButton(1010, 595, 175, 40, "Edit board")

        nextPlayer_label = arcade.gui.UILabel(1010, 545, 175, 40, "Next Player", align="center", font_size=16)
        self.nextPlayerDark_button = arcade.gui.UITextureButton(1055, 515, 40, 40, Graphics.darkPiece_icon,
                                                                Graphics.darkPiece_icon2, Graphics.darkPiece_icon3)
        self.nextPlayerLight_button = arcade.gui.UITextureButton(1105, 515, 40, 40, Graphics.lightPiece_icon,
                                                                 Graphics.lightPiece_icon2, Graphics.lightPiece_icon3)

        setRoll_label = arcade.gui.UILabel(1010, 300, 175, 40, "Next Set Roll", align="center", font_size=16)
        setRoll_input = arcade.gui.UIInputText(1085, 260, 175, 40, "6,6", font_size=16)

        self.manager.add(Back_button)
        self.manager.add(Quit_button)
        self.manager.add(New_button)
        self.manager.add(Setting_button)

        self.manager.add(RunGame_button)
        self.manager.add(RunRandomTurn_button)
        self.manager.add(RunSetTurn_button)
        self.manager.add(EditBoard_button)

        self.manager.add(nextPlayer_label)
        self.manager.add(self.nextPlayerDark_button)
        self.manager.add(self.nextPlayerLight_button)

        self.manager.add(setRoll_label)
        self.manager.add(setRoll_input)

        @Back_button.event("on_click")
        def on_click_Back(event):
            mainView = MainMenuView(self.backgroundColor)
            self.window.show_view(mainView)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            arcade.close_window()

        @New_button.event("on_click")
        def on_click_New(event):
            self.window.MainBoard.setStartPositions()
            self.window.firstTurn = True

        @Setting_button.event("on_click")
        def on_click_Settings(event):
            self.window.lastPage = self
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)

        @RunGame_button.event("on_click")
        def on_click_run(event):
            self.window.nextPlayer = self.window.nextPlayer if self.window.nextPlayer != 0 else random.randint(1, 2)
            game_over = False
            while not game_over:
                if self.window.nextPlayer == 1:
                    if self.window.settings["Agent1"] == "Human":
                        pass
                    else:
                        self.window.MainTurn = Logic.Turn(self.window.nextPlayer, self.window.settings["Agent1"],
                                                          First=(self.window.nextPlayer == 0))
                        self.window.MainTurn.updatePossibleMovesStandardFormat(self.window.MainBoard)
                        Moves = AI.Main(self.window.MainBoard, self.window.MainTurn, self.window.settings["Agent1"],
                                        self.window.settings["Network1 ID"])
                        self.window.MainBoard.makeMoves(Moves, 1, True)
                        if self.window.MainBoard.pip[0] == 0:
                            messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                                "Game Over: \nPlayer 1 Wins! Please Select 'New Game' to start a new game."),
                                                                 callback=None, buttons=["Ok"])
                            self.manager.add(messageBox)
                            game_over = True
                        self.window.nextPlayer = 2
                else:
                    if self.window.settings["Agent2"] == "Human":
                        pass
                    else:
                        self.window.MainTurn = Logic.Turn(self.window.nextPlayer, self.window.settings["Agent2"],
                                                          First=(self.window.nextPlayer == 0))
                        self.window.MainTurn.updatePossibleMovesStandardFormat(self.window.MainBoard)
                        Moves = AI.Main(self.window.MainBoard, self.window.MainTurn, self.window.settings["Agent2"],
                                        self.window.settings["Network2 ID"])
                        self.window.MainBoard.makeMoves(Moves, 2, True)
                        if self.window.MainBoard.pip[1] == 0:
                            messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                                "Game Over: \nPlayer 2 Wins! Please Select 'New Game' to start a new game."),
                                                                 callback=None, buttons=["Ok"])
                            self.manager.add(messageBox)
                            game_over = True
                        self.window.nextPlayer = 1

        @RunRandomTurn_button.event("on_click")
        def on_click_run(event):
            player = self.window.nextPlayer if self.window.nextPlayer != 0 else random.randint(1, 2)
            if player == 1:
                if self.window.settings["Agent1"] == "Human":
                    pass
                else:
                    self.window.MainTurn = Logic.Turn(player, self.window.settings["Agent1"],
                                                      First=(self.window.nextPlayer == 0))
                    self.window.MainTurn.updatePossibleMovesStandardFormat(self.window.MainBoard)
                    Moves = AI.Main(self.window.MainBoard, self.window.MainTurn, self.window.settings["Agent1"],
                                    self.window.settings["Network1 ID"])
                    self.window.MainBoard.makeMoves(Moves, 1, True)
                    if self.window.MainBoard.pip[0] == 0:
                        messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                            "Game Over: \nPlayer 1 Wins! Please Select 'New Game' to start a new game."), callback=None,
                                                             buttons=["Ok"])
                        self.manager.add(messageBox)
                    self.window.nextPlayer = 2
            else:
                if self.window.settings["Agent2"] == "Human":
                    pass
                else:
                    self.window.MainTurn = Logic.Turn(player, self.window.settings["Agent2"],
                                                      First=(self.window.nextPlayer == 0))
                    self.window.MainTurn.updatePossibleMovesStandardFormat(self.window.MainBoard)
                    Moves = AI.Main(self.window.MainBoard, self.window.MainTurn, self.window.settings["Agent2"],
                                    self.window.settings["Network2 ID"])
                    self.window.MainBoard.makeMoves(Moves, 2, True)
                    if self.window.MainBoard.pip[1] == 0:
                        messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                            "Game Over: \nPlayer 2 Wins! Please Select 'New Game' to start a new game."), callback=None,
                                                             buttons=["Ok"])
                        self.manager.add(messageBox)
                    self.window.nextPlayer = 1

            self.window.firstTurn = False

        @RunSetTurn_button.event("on_click")
        def on_click_run(event):

            set_roll_string = setRoll_input.text.rsplit(sep=",")
            set_roll = [int(num) for num in set_roll_string]

            if not Logic.isLegalRoll(set_roll):
                messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                    "Inputted roll not legal. \nPlease input valid roll in form num1,num2 \ne.g. 4,5"), callback=None,
                                                     buttons=["Ok"])
                self.manager.add(messageBox)
                return

            if set_roll[0] == set_roll[1] and self.window.firstTurn:
                messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                    "Inputted roll not legal. No Doubles allowed for first move. \nPlease input valid roll in form num1,num2 \ne.g. 4,5"),
                                                     callback=None, buttons=["Ok"])
                self.manager.add(messageBox)
                return

            player = self.window.nextPlayer if self.window.nextPlayer != 0 else random.randint(1, 2)
            if player == 1:
                if self.window.settings["Agent1"] == "Human":
                    pass
                else:
                    self.window.MainTurn = Logic.Turn(player, self.window.settings["Agent1"],
                                                      First=self.window.firstTurn, roll=set_roll)
                    self.window.MainTurn.updatePossibleMovesStandardFormat(self.window.MainBoard)
                    Moves = AI.Main(self.window.MainBoard, self.window.MainTurn, self.window.settings["Agent1"],
                                    self.window.settings["Network1 ID"])
                    self.window.MainBoard.makeMoves(Moves, 1, True)
                    if self.window.MainBoard.pip[0] == 0:
                        messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                            "Game Over: \nPlayer 1 Wins! Please Select 'New Game' to start a new game."), callback=None,
                                                             buttons=["Ok"])
                        self.manager.add(messageBox)
                    self.window.nextPlayer = 2
            else:
                if self.window.settings["Agent2"] == "Human":
                    pass
                else:
                    self.window.MainTurn = Logic.Turn(player, self.window.settings["Agent2"],
                                                      First=self.window.firstTurn, roll=set_roll)
                    self.window.MainTurn.updatePossibleMovesStandardFormat(self.window.MainBoard)
                    Moves = AI.Main(self.window.MainBoard, self.window.MainTurn, self.window.settings["Agent2"],
                                    self.window.settings["Network2 ID"])
                    self.window.MainBoard.makeMoves(Moves, 2, True)
                    if self.window.MainBoard.pip[1] == 0:
                        messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                            "Game Over: \nPlayer 2 Wins! Please Select 'New Game' to start a new game."), callback=None,
                                                             buttons=["Ok"])
                        self.manager.add(messageBox)
                    self.window.nextPlayer = 1

            self.window.firstTurn = False

        @EditBoard_button.event("on_click")
        def on_click_Edit(event):
            EditView = EditBoardView(self.backgroundColor)
            self.window.show_view(EditView)

        @self.nextPlayerDark_button.event("on_click")
        def on_click_Dark(event):
            self.window.nextPlayer = 1 if self.window.nextPlayer != 1 else 0

        @self.nextPlayerLight_button.event("on_click")
        def on_click_Light(event):
            self.window.nextPlayer = 2 if self.window.nextPlayer != 2 else 0

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()

        if self.window.nextPlayer == 1:
            self.nextPlayerDark_button.texture = Graphics.darkPiece_icon3
            self.nextPlayerLight_button.texture = Graphics.lightPiece_icon
        elif self.window.nextPlayer == 2:
            self.nextPlayerLight_button.texture = Graphics.lightPiece_icon3
            self.nextPlayerDark_button.texture = Graphics.darkPiece_icon
        else:
            self.nextPlayerDark_button.texture = Graphics.darkPiece_icon
            self.nextPlayerLight_button.texture = Graphics.lightPiece_icon

        Graphics.drawBoard()
        Graphics.drawPieces(self.window.MainBoard.positions, self.window.MainBoard.pip)

        Graphics.DrawSimMain()

        if self.window.MainBoard.MoveLineData != None:
            Graphics.DrawMoveLines(self.window.MainBoard.MoveLineData)
        if self.window.MainTurn != None:
            Graphics.drawDice(self.window.MainTurn.roll[0], self.window.MainTurn.roll[1],
                              self.window.MainTurn.unused_dice)

        self.manager.draw()


class EditBoardView(arcade.View):
    def __init__(self, backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.tool = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Done_button = arcade.gui.UIFlatButton(15, 745, 75, 40, "Done")
        Quit_button = arcade.gui.UIFlatButton(15, 695, 75, 40, "Quit")

        light_button = arcade.gui.UITextureButton(1010, 510, 75, 75, Graphics.lightPiece_icon,
                                                  Graphics.lightPiece_icon2, Graphics.lightPiece_icon3)
        dark_button = arcade.gui.UITextureButton(1010, 420, 75, 75, Graphics.darkPiece_icon, Graphics.darkPiece_icon2,
                                                 Graphics.darkPiece_icon3)
        delete_button = arcade.gui.UITextureButton(1010, 330, 75, 75, Graphics.delete_icon, Graphics.delete_icon2,
                                                   Graphics.delete_icon3)
        restart_button = arcade.gui.UITextureButton(1010, 240, 75, 75, Graphics.restart_icon, Graphics.restart_icon2,
                                                    Graphics.restart_icon3, )

        Edit_button = arcade.gui.UIFlatButton(1010, 15, 175, 40, "Edit as String")

        light_label = arcade.gui.UITextArea(1100, 525, 90, 45, "Add Light", font_size=15)
        dark_label = arcade.gui.UITextArea(1100, 435, 90, 45, "Add    Dark", font_size=15)
        delete_label = arcade.gui.UITextArea(1100, 345, 90, 45, "Delete Piece", font_size=15)
        restart_label = arcade.gui.UITextArea(1100, 255, 90, 45, "Delete All", font_size=15)

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
            if Logic.isLegalBoard(self.window.MainBoard.positions):
                simView = MainSimView(self.backgroundColor)
                self.window.MainBoard.MoveLineData = None
                self.window.show_view(simView)
            else:
                messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                    "Error: \nThis in not a legal Backgammon board. Please Provide a legal board."), callback=None,
                                                     buttons=["Ok"])
                self.manager.add(messageBox)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            arcade.close_window()

        @light_button.event("on_click")
        def on_click_light(event):
            self.tool = "Light"
            light_button.texture = Graphics.lightPiece_icon3
            dark_button.texture = Graphics.darkPiece_icon
            delete_button.texture = Graphics.delete_icon

        @dark_button.event("on_click")
        def on_click_dark(event):
            self.tool = "Dark"
            light_button.texture = Graphics.lightPiece_icon
            dark_button.texture = Graphics.darkPiece_icon3
            delete_button.texture = Graphics.delete_icon

        @delete_button.event("on_click")
        def on_click_delete(event):
            self.tool = "Delete"
            light_button.texture = Graphics.lightPiece_icon
            dark_button.texture = Graphics.darkPiece_icon
            delete_button.texture = Graphics.delete_icon3

        @restart_button.event("on_click")
        def on_click_light(event):
            self.window.MainBoard.positions = [0] * 28

        @Edit_button.event("on_click")
        def on_click_Edit(event):
            editView = EditAsString_View(self.backgroundColor)
            self.window.show_view(editView)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        position = None
        if (216 < x < 276) and (484 < y < 766):
            position = 0
        if (276 < x < 336) and (484 < y < 766):
            position = 1
        if (336 < x < 396) and (484 < y < 766):
            position = 2
        if (396 < x < 456) and (484 < y < 766):
            position = 3
        if (456 < x < 516) and (484 < y < 766):
            position = 4
        if (516 < x < 576) and (484 < y < 766):
            position = 5
        if (216 < x < 276) and (44 < y < 316):
            position = 23
        if (276 < x < 336) and (44 < y < 316):
            position = 22
        if (336 < x < 396) and (44 < y < 316):
            position = 21
        if (396 < x < 456) and (44 < y < 316):
            position = 20
        if (456 < x < 516) and (44 < y < 316):
            position = 19
        if (516 < x < 576) and (44 < y < 316):
            position = 18
        if (624 < x < 684) and (484 < y < 766):
            position = 6
        if (684 < x < 744) and (484 < y < 766):
            position = 7
        if (744 < x < 804) and (484 < y < 766):
            position = 8
        if (804 < x < 864) and (484 < y < 766):
            position = 9
        if (864 < x < 924) and (484 < y < 766):
            position = 10
        if (924 < x < 984) and (484 < y < 766):
            position = 11
        if (624 < x < 684) and (44 < y < 316):
            position = 17
        if (684 < x < 744) and (44 < y < 316):
            position = 16
        if (744 < x < 804) and (44 < y < 316):
            position = 15
        if (804 < x < 864) and (44 < y < 316):
            position = 14
        if (864 < x < 924) and (44 < y < 316):
            position = 13
        if (924 < x < 984) and (44 < y < 316):
            position = 12
        if (120 < x < 180) and (450 < y < 750):
            position = 27
        if (120 < x < 180) and (50 < y < 350):
            position = 26
        if (505 < x < 555) and (350 < y < 450):
            position = 24
        if (645 < x < 695) and (350 < y < 450):
            position = 25

        if position == 24:
            if self.tool == "Light":
                if self.window.MainBoard.positions[position] > 0:
                    self.window.MainBoard.positions[position] += -1
            elif self.tool == "Dark":
                self.window.MainBoard.positions[position] += 1
            elif self.tool == "Delete":
                self.window.MainBoard.positions[position] = 0
        elif position == 25:
            if self.tool == "Light":
                self.window.MainBoard.positions[position] += 1
            elif self.tool == "Dark":
                if self.window.MainBoard.positions[position] > 0:
                    self.window.MainBoard.positions[position] += -1
            elif self.tool == "Delete":
                self.window.MainBoard.positions[position] = 0
        elif position == 27:
            if self.tool == "Light":
                self.window.MainBoard.positions[position] += 1
            elif self.tool == "Dark":
                if self.window.MainBoard.positions[position] > 0:
                    self.window.MainBoard.positions[position] += -1
            elif self.tool == "Delete":
                self.window.MainBoard.positions[position] = 0
        elif position == 26:
            if self.tool == "Light":
                if self.window.MainBoard.positions[position] > 0:
                    self.window.MainBoard.positions[position] += -1
            elif self.tool == "Dark":
                self.window.MainBoard.positions[position] += 1
            elif self.tool == "Delete":
                self.window.MainBoard.positions[position] = 0
        elif position != None:
            if self.tool == "Light":
                self.window.MainBoard.positions[position] += 1
            elif self.tool == "Dark":
                self.window.MainBoard.positions[position] += -1
            elif self.tool == "Delete":
                self.window.MainBoard.positions[position] = 0

    def on_draw(self):
        self.clear()

        Graphics.drawBoard()
        Graphics.drawPieces(self.window.MainBoard.positions, self.window.MainBoard.pip)
        Graphics.DrawBarBoxes()
        self.manager.draw()


class EditAsString_View(arcade.View):

    def __init__(self, backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        stringList = [str(num) for num in self.window.MainBoard.positions]
        string = ", ".join(stringList)

        Done_button = arcade.gui.UIFlatButton(550, 300, 100, 50, "Done")
        text_input = arcade.gui.UIInputText(325, 375, 600, 50, string)

        self.manager.add(Done_button)
        self.manager.add(text_input)

        @Done_button.event("on_click")
        def on_click_Done(event):

            stringList = text_input.text.rsplit(sep=", ")

            try:
                numList = [int(num) for num in stringList]
            except:
                messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                    "Error: \nThis in not a legal Backgammon board string. Please Provide a legal board string."),
                                                     callback=None, buttons=["Ok"])
                self.manager.add(messageBox)

            if Logic.isLegalBoard(numList):
                self.window.MainBoard.positions = numList
                editView = EditBoardView(self.backgroundColor)
                self.window.show_view(editView)
            else:
                messageBox = arcade.gui.UIMessageBox(width=300, height=150, message_text=(
                    "Error: \nThis in not a legal Backgammon board string. Please Provide a legal board string."),
                                                     callback=None, buttons=["Ok"])
                self.manager.add(messageBox)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_rectangle_filled(600, 400, 600, 50, Graphics.board_color)
        arcade.draw_rectangle_outline(600, 400, 600, 50, Graphics.board_color, 6)

        self.manager.draw()


# 1P Views:


# 2P Views:
class Start_2P_View(arcade.View):

    def __init__(self, backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Back_button = arcade.gui.UIFlatButton(15, 745, 75, 40, "Back")
        Quit_button = arcade.gui.UIFlatButton(15, 695, 75, 40, "Quit")
        Roll_button = arcade.gui.UIFlatButton(400, 375, 125, 50, "Roll")
        Settings_button = arcade.gui.UIFlatButton(700, 375, 125, 50, "Settings")

        self.manager.add(Back_button)
        self.manager.add(Quit_button)
        self.manager.add(Roll_button)
        self.manager.add(Settings_button)

        @Back_button.event("on_click")
        def on_click_back(event):
            mainmenuView = MainMenuView(self.backgroundColor)
            self.window.show_view(mainmenuView)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            arcade.close_window()

        @Roll_button.event("on_click")
        def on_click_roll(event):
            firstPlayer = random.randint(1, 2)

            self.window.MainTurn = Logic.Turn(firstPlayer, "Human", First=True)
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
        Graphics.drawPieces(self.window.MainBoard.positions, self.window.MainBoard.pip)
        self.manager.draw()


class P1_Turn_2P_View(arcade.View):

    def __init__(self, backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.step = "Main"

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Exit_button = arcade.gui.UIFlatButton(15, 745, 75, 40, "Exit")
        Quit_button = arcade.gui.UIFlatButton(15, 695, 75, 40, "Quit")
        Settings_button = arcade.gui.UIFlatButton(1010, 15, 175, 40, "Settings")

        Done_button = arcade.gui.UIFlatButton(1010, 510, 175, 40, "Done")

        self.manager.add(Exit_button)
        self.manager.add(Quit_button)
        self.manager.add(Settings_button)
        self.manager.add(Done_button)

        @Exit_button.event("on_click")
        def on_click_exit(event):
            mainmenuView = MainMenuView(self.backgroundColor)
            self.window.show_view(mainmenuView)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            arcade.close_window()

        @Settings_button.event("on_click")
        def on_click_Settings(event):
            self.window.lastPage = self
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)

        @Done_button.event("on_click")
        def on_click_done(event):
            nextPlayerView = P2_PreTurn_2P_View(self.backgroundColor)
            self.window.show_view(nextPlayerView)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        Graphics.drawBoard()
        arcade.draw_rectangle_filled(601, 401, 12, 762, Graphics.darkCheckerColor)
        Graphics.drawPieces(self.window.MainBoard.positions, self.window.MainBoard.pip)
        Graphics.drawDice(self.window.MainTurn.roll[0], self.window.MainTurn.roll[1], self.window.MainTurn.unused_dice)
        Graphics.drawTurnMain(
            self.window.MainTurn.sprites_move_start) if self.step == "Main" else Graphics.drawTurnBranch(
            self.window.MainTurn.sprite_active, self.window.MainTurn.sprites_move_end)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.step == "Main":
            clicked_sprite = arcade.get_sprites_at_point((x, y), self.window.MainTurn.sprites_move_start)
            if clicked_sprite != []:
                self.window.MainTurn.sprite_active = clicked_sprite[0]
                self.window.MainTurn.sprites_move_end = Graphics.createMoveEndSprites(
                    self.window.MainTurn.sprite_active, self.window.MainBoard)
                self.step = "Branch"

        elif self.step == "Branch":
            self.step = "Main"
            # When a possible sub-move sprite is clicked:
            clicked_sprite = arcade.get_sprites_at_point((x, y), self.window.MainTurn.sprites_move_end)
            if clicked_sprite != []:
                self.window.MainBoard.makeMove((self.window.MainTurn.sprite_active.move[0], clicked_sprite[0].pos), 1)
                if self.window.MainBoard.pip[0] == 0:
                    pass
                    # TO DO: add game over logic here
                roll = Logic.fromMoveToDie(self.window.MainTurn.sprite_active.move[0], clicked_sprite[0].pos,
                                           self.window.MainTurn.unused_dice, 1)
                self.window.MainTurn.unused_dice.remove(roll)
                if len(self.window.MainTurn.unused_dice) > 0:
                    self.window.MainTurn.updatePossibleMovesHumanFormat(self.window.MainBoard)
                    self.window.MainTurn.formSpriteList(self.window.MainBoard)
                else:
                    self.window.MainTurn.sprites_move_start = arcade.SpriteList()


class P2_Turn_2P_View(arcade.View):

    def __init__(self, backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.step = "Main"

        Exit_button = arcade.gui.UIFlatButton(15, 745, 75, 40, "Exit")
        Quit_button = arcade.gui.UIFlatButton(15, 695, 75, 40, "Quit")
        Settings_button = arcade.gui.UIFlatButton(1010, 15, 175, 40, "Settings")

        Done_button = arcade.gui.UIFlatButton(1010, 510, 175, 40, "Done")

        self.manager.add(Exit_button)
        self.manager.add(Quit_button)
        self.manager.add(Settings_button)
        self.manager.add(Done_button)

        @Exit_button.event("on_click")
        def on_click_exit(event):
            mainmenuView = MainMenuView(self.backgroundColor)
            self.window.show_view(mainmenuView)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            arcade.close_window()

        @Settings_button.event("on_click")
        def on_click_Settings(event):
            self.window.lastPage = self
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)

        @Done_button.event("on_click")
        def on_click_done(event):
            nextPlayerView = P1_PreTurn_2P_View(self.backgroundColor)
            self.window.show_view(nextPlayerView)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        Graphics.drawBoard()
        arcade.draw_rectangle_filled(601, 401, 12, 762, Graphics.lightCheckerColor)
        Graphics.drawPieces(self.window.MainBoard.positions, self.window.MainBoard.pip)
        Graphics.drawDice(self.window.MainTurn.roll[0], self.window.MainTurn.roll[1], self.window.MainTurn.unused_dice)
        Graphics.drawTurnMain(
            self.window.MainTurn.sprites_move_start) if self.step == "Main" else Graphics.drawTurnBranch(
            self.window.MainTurn.sprite_active, self.window.MainTurn.sprites_move_end)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.step == "Main":
            clicked_sprite = arcade.get_sprites_at_point((x, y), self.window.MainTurn.sprites_move_start)
            if clicked_sprite != []:
                self.window.MainTurn.sprite_active = clicked_sprite[0]
                self.window.MainTurn.sprites_move_end = Graphics.createMoveEndSprites(
                    self.window.MainTurn.sprite_active, self.window.MainBoard)
                self.step = "Branch"

        elif self.step == "Branch":
            self.step = "Main"
            # When a possible sub-move sprite is clicked:
            clicked_sprite = arcade.get_sprites_at_point((x, y), self.window.MainTurn.sprites_move_end)
            if clicked_sprite != []:
                self.window.MainBoard.makeMove((self.window.MainTurn.sprite_active.move[0], clicked_sprite[0].pos), 2)
                if self.window.MainBoard.pip[0] == 0:
                    pass
                    # TO DO: add game over logic here
                roll = Logic.fromMoveToDie(self.window.MainTurn.sprite_active.move[0], clicked_sprite[0].pos,
                                           self.window.MainTurn.unused_dice, 2)
                self.window.MainTurn.unused_dice.remove(roll)
                if len(self.window.MainTurn.unused_dice) > 0:
                    self.window.MainTurn.updatePossibleMovesHumanFormat(self.window.MainBoard)
                    self.window.MainTurn.formSpriteList(self.window.MainBoard)
                else:
                    self.window.MainTurn.sprites_move_start = arcade.SpriteList()


class P1_PreTurn_2P_View(arcade.View):

    def __init__(self, backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Exit_button = arcade.gui.UIFlatButton(15, 745, 75, 40, "Exit")
        Quit_button = arcade.gui.UIFlatButton(15, 695, 75, 40, "Quit")
        Settings_button = arcade.gui.UIFlatButton(1010, 15, 175, 40, "Settings")

        Roll_button = arcade.gui.UIFlatButton(1010, 400, 175, 40, "Roll")

        self.manager.add(Exit_button)
        self.manager.add(Quit_button)
        self.manager.add(Settings_button)
        self.manager.add(Roll_button)

        @Exit_button.event("on_click")
        def on_click_exit(event):
            mainmenuView = MainMenuView(self.backgroundColor)
            self.window.show_view(mainmenuView)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            arcade.close_window()

        @Settings_button.event("on_click")
        def on_click_Settings(event):
            self.window.lastPage = self
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)

        @Roll_button.event("on_click")
        def on_click_roll(event):
            self.window.MainTurn = Logic.Turn(1, "Human", First=False)
            self.window.MainTurn.updatePossibleMovesHumanFormat(self.window.MainBoard)
            self.window.MainTurn.formSpriteList(self.window.MainBoard)

            nextPlayerView = P1_Turn_2P_View(self.backgroundColor)
            self.window.show_view(nextPlayerView)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        Graphics.drawBoard()
        arcade.draw_rectangle_filled(601, 401, 12, 762, Graphics.darkCheckerColor)
        Graphics.drawPieces(self.window.MainBoard.positions, self.window.MainBoard.pip)


class P2_PreTurn_2P_View(arcade.View):

    def __init__(self, backgroundColor):
        super().__init__()
        self.backgroundColor = backgroundColor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        Exit_button = arcade.gui.UIFlatButton(15, 745, 75, 40, "Exit")
        Quit_button = arcade.gui.UIFlatButton(15, 695, 75, 40, "Quit")
        Settings_button = arcade.gui.UIFlatButton(1010, 15, 175, 40, "Settings")

        Roll_button = arcade.gui.UIFlatButton(1010, 400, 175, 40, "Roll")

        self.manager.add(Exit_button)
        self.manager.add(Quit_button)
        self.manager.add(Settings_button)
        self.manager.add(Roll_button)

        @Exit_button.event("on_click")
        def on_click_exit(event):
            mainmenuView = MainMenuView(self.backgroundColor)
            self.window.show_view(mainmenuView)

        @Quit_button.event("on_click")
        def on_click_Quit(event):
            arcade.close_window()

        @Settings_button.event("on_click")
        def on_click_Settings(event):
            self.window.lastPage = self
            settingsView = SettingsView(self.backgroundColor)
            self.window.show_view(settingsView)

        @Roll_button.event("on_click")
        def on_click_roll(event):
            self.window.MainTurn = Logic.Turn(2, "Human", First=False)
            self.window.MainTurn.updatePossibleMovesHumanFormat(self.window.MainBoard)
            self.window.MainTurn.formSpriteList(self.window.MainBoard)

            nextPlayerView = P2_Turn_2P_View(self.backgroundColor)
            self.window.show_view(nextPlayerView)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        Graphics.drawBoard()
        arcade.draw_rectangle_filled(601, 401, 12, 762, Graphics.lightCheckerColor)
        Graphics.drawPieces(self.window.MainBoard.positions, self.window.MainBoard.pip)


class GameOver_2P_View(arcade.View):

    def __init__(self, background_color):
        super().__init__()
        self.backgroundColor = background_color

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        back_button = arcade.gui.UIFlatButton(25, 725, 100, 50, "Back")

        self.manager.add(back_button)

    def on_show_view(self):
        self.manager.enable()
        arcade.set_background_color(self.backgroundColor)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
