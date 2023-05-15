#Imports
import arcade
import copy

#Load images & sounds:
gear_icon = arcade.load_texture("Images\gear_icon.png")
exit_icon = arcade.load_texture("Images\exit_icon.png")
quit_icon = arcade.load_texture("Images\quit_icon.png")
button_click = arcade.Sound("Sounds/sound3.mp3")
checker_move = arcade.Sound("Sounds/sound.mp3")
dice_roll = arcade.Sound("Sounds/soundDice.mp3")

#Data:
Master_Location_Dict = {1:(247,755),2:(307,755),3:(367,755),4:(427,755),5:(487,755),6:(547,755),7:(655,755),8:(715,755),9:(775,755),10:(835,755),11:(895,755),12:(955,755),13:(955,47),14:(895,47),15:(835,47),16:(775,47),17:(715,47),18:(655,47),19:(547,47),20:(487,47),21:(427,47),22:(367,47),23:(307,47),24:(247,47)}

#Theme:
button_default = arcade.color.ALMOND
button_excited = arcade.color.AERO_BLUE
button_used = arcade.color.CHARCOAL
checkerColor1 = arcade.color.SIENNA
checkerColor2 = arcade.color.SKY_BLUE
darkTextColor = arcade.color.BLACK
lightTextColor = arcade.color.AERO_BLUE
lightTextColor2 = arcade.color.ALMOND
Background = arcade.color.DARK_SCARLET
board_color = arcade.color.ALMOND
board_border = arcade.color.BLACK_BEAN
Point1 = arcade.color.OTTER_BROWN
Point2 = arcade.color.ROSY_BROWN
black = arcade.color.BLACK


#Helper Functions:
def drawButton(text, centerx, centery, width=150, height=75, excited=False, fontSize=30, defaultColor=board_color, border=12):
    color = defaultColor if excited == False else button_excited
    arcade.draw_rectangle_filled(centerx,centery,width,height,color)
    arcade.draw_rectangle_outline(centerx,centery,width,height,board_border,border)
    arcade.draw_text(text,(centerx - (.5*width)),(centery - 15),black,fontSize,width,"center","arial",bold=True)
def drawButtonIcon(icon, centerx, centery, width=75, height=75, excited=False, defaultColor=board_color, border=12):
    color = defaultColor if excited == False else button_excited
    arcade.draw_rectangle_filled(centerx,centery,width,height,color)
    arcade.draw_rectangle_outline(centerx,centery,width,height,board_border,border)
    arcade.draw_texture_rectangle(centerx,centery,width-25,height-25,icon)
def drawButtonSmall(text,centerx,centery,width,height,excited=False, fontSize=15, defaultColor=board_color):
    color = defaultColor if excited == False else button_excited
    arcade.draw_rectangle_filled(centerx,centery,width,height,color)
    arcade.draw_rectangle_outline(centerx,centery,width,height,board_border,6)
    arcade.draw_text(text,(centerx - (.5*width)),(centery - 5),black,fontSize,width,"center","arial",bold=True)
def drawButtonMultiLine1(text1, text2, centerx, centery, width=150, height=75, excited=False, fontSize=30, defaultColor=board_color):
    color = defaultColor if excited == False else button_excited
    arcade.draw_rectangle_filled(centerx,centery,width,height,color)
    arcade.draw_rectangle_outline(centerx,centery,width,height,board_border,12)
    arcade.draw_text(text1,(centerx - (.5*width)),(centery + 25),black,fontSize,width,"center","arial",bold=True,anchor_y="center")
    arcade.draw_text(text2,(centerx - (.5*width)),(centery - 25),black,fontSize,width,"center","arial",bold=True,anchor_y="center")
def drawSignature(version):
    arcade.draw_text("Backgammon by Wills Erda",1000,25,black,10)
    arcade.draw_text(f"v{version} @2022 ",1000,10,black,10)
    
#Drawing The Board:
def drawBoard():
    arcade.draw_rectangle_outline(601,401,774,774,board_border,12)
    arcade.draw_rectangle_filled(601,401,768,768,board_color)
    arcade.draw_rectangle_outline(601,401,24,774,board_border,12)
    def drawTriangles(x,y,o): #OffsetX, OffsetY, Orientation(1 or -1)
        color1 = Point1 if o == 1 else Point2
        color2 = Point2 if o == 1 else Point1
        arcade.draw_triangle_filled((601-x),(401-y),(601-x)+30,(401-y)+(300*o),(601-x)+60,(401-y),color1)
        arcade.draw_triangle_filled((601-x)+60,(401-y),(601-x)+90,(401-y)+(300*o),(601-x)+120,(401-y),color2)
        arcade.draw_triangle_filled((601-x)+120,(401-y),(601-x)+150,(401-y)+(300*o),(601-x)+180,(401-y),color1)
        arcade.draw_triangle_filled((601-x)+180,(401-y),(601-x)+210,(401-y)+(300*o),(601-x)+240,(401-y),color2)
        arcade.draw_triangle_filled((601-x)+240,(401-y),(601-x)+270,(401-y)+(300*o),(601-x)+300,(401-y),color1)
        arcade.draw_triangle_filled((601-x)+300,(401-y),(601-x)+330,(401-y)+(300*o),(601-x)+360,(401-y),color2)
    drawTriangles(384,384,1)
    drawTriangles(384,-384,-1)
    drawTriangles(-24,384,1)
    drawTriangles(-24,-384,-1)
    arcade.draw_rectangle_outline(150,201,64,304,board_border,8)
    arcade.draw_rectangle_outline(150,601,64,304,board_border,8)
    arcade.draw_rectangle_filled(150,201,60,300,board_color)
    arcade.draw_rectangle_filled(150,601,60,300,board_color)
def diceSub(baseX,baseY,num,color,override=False,altColor=black):
        p1 = [baseX+13,baseY+13]
        p2 = [baseX+13,baseY+25]
        p3 = [baseX+13,baseY+38]
        p4 = [baseX+25,baseY+25]
        p5 = [baseX+38,baseY+13]
        p6 = [baseX+38,baseY+25]
        p7 = [baseX+38,baseY+38]
        arcade.draw_rectangle_filled(baseX+25,baseY+25,50,50,color if override == False else altColor)
        arcade.draw_rectangle_outline(baseX+25,baseY+25,50,50,black,2)
        if num == 1:
            arcade.draw_points([p4],black,7)
        if num == 2:
            arcade.draw_points([p3,p5],black,7)
        if num == 3:
            arcade.draw_points([p1,p4,p7],black,7)
        if num == 4:
            arcade.draw_points([p1,p3,p5,p7],black,7)
        if num == 5:
            arcade.draw_points([p1,p3,p4,p5,p7],black,7)
        if num == 6:
            arcade.draw_points([p1,p2,p3,p5,p6,p7],black,7)
def drawDice(num1,num2,availableRolls):
    tempList = copy.deepcopy(availableRolls)
    U1 = U2 = U3 = U4 = True
    if num1 in tempList:
        U1 = False
        tempList.remove(num1)
    if num2 in tempList:
        U2 = False
        tempList.remove(num2)
    if num1 in tempList:
        U3 = False
        tempList.remove(num1)
    if num2 in tempList:
        U4 = False
        tempList.remove(num2)
    diceSub(1040,455,num1, board_color if U1 == False else arcade.color.CHARCOAL)
    diceSub(1110,455,num2, board_color if U2 == False else arcade.color.CHARCOAL)
    if num1 == num2:
        diceSub(1040,515,num1, board_color if U3 == False else arcade.color.CHARCOAL)
        diceSub(1110,515,num2, board_color if U4 == False else arcade.color.CHARCOAL)

#Drawing the Pieces and the Pip:
def drawPIP(pip):
    arcade.draw_rectangle_filled(150,25,60,30,board_border)
    arcade.draw_rectangle_filled(150,775,60,30,board_border)
    arcade.draw_rectangle_outline(150,25,60,30,black,2)
    arcade.draw_rectangle_outline(150,775,60,30,black,2)
    arcade.draw_text(pip[0],75,15,board_color,20,150,"center","arial")
    arcade.draw_text(pip[1],75,765,board_color,20,150,"center","arial")
def drawPieces(positions,pip):
    drawPIP(pip)
    for index in range(24):
        listNum = index + 1
        pointNum = positions[index]
        if pointNum != 0: #Set Necessary Variables For Drawn Points
            color = checkerColor1 if pointNum < 0 else checkerColor2
            location = listNum
            orientation = 1 if location > 12 else -1
            centerx = Master_Location_Dict[location][0]
            centery = Master_Location_Dict[location][1] 
        if abs(pointNum) < 7 and abs(pointNum) != 0: #Draw Points with 6 or less Pieces
            for i in range(abs(pointNum)):
                offset = ((i)*60*orientation)
                arcade.draw_circle_filled(centerx,centery+offset,30,color)
                arcade.draw_circle_outline(centerx,centery+offset,30,arcade.color.BLACK,2)
        if abs(pointNum) > 6: #Draw  Points with 7 or more Pieces
            offset = 360/abs(pointNum)
            for i in range(abs(pointNum)):
                off = offset * i * orientation
                arcade.draw_circle_filled(centerx,centery+off,30,color)
                arcade.draw_circle_outline(centerx,centery+off,30,arcade.color.BLACK,2)
    for pc in range(positions[26]):
        arcade.draw_rectangle_filled(150,341-(20*(pc)),60,20,checkerColor1)
        arcade.draw_line(120,331-(20*pc),180,331-(20*pc),arcade.color.BLACK,2)
    for pc in range(positions[27]):
        arcade.draw_rectangle_filled(150,461+(20*(pc)),60,20,checkerColor2)
        arcade.draw_line(120,471+(20*pc),180,471+(20*pc),arcade.color.BLACK,2)
    if positions[24] != 0 or positions[25] != 0:
        list1 = [1] * positions[24]
        list2 = [2] * positions[25]
        barList = list1 + list2
        totalDist = 70 * len(barList)
        startDist = totalDist/2
        for pc in range(len(barList)):
            color = checkerColor1 if barList[pc] == 1 else checkerColor2
            arcade.draw_circle_filled(601,401-startDist+35+(60*pc),30,color)
            arcade.draw_circle_outline(601,401-startDist+35+(60*pc),30,arcade.color.BLACK,2)

#Sprite Management:
def createMoveStartSprites(possibleMoves,Board,player): #UPDATE NEEDED
    board_location_list = Board.positions
    list1 = [1] * Board.positions[24]
    list2 = [2] * Board.positions[25]
    board_bar_list = list1 + list2
    sprites = arcade.SpriteList()

    for move in possibleMoves:
        startPoint = move[0]

        if startPoint == 1001:
            totalDist = 70 * len(board_bar_list)
            startDist = totalDist/2
            for pc in range(len(board_bar_list)):
                doDraw = True if board_bar_list[pc] == player else False
                if doDraw == True:
                    tempSprite = arcade.Sprite("Images/Move.png",0.07)
                    tempSprite.center_x = 601
                    tempSprite.center_y = 401-startDist+35+(60*pc)
                    tempSprite.move = move
        
        else:
            o = 1 if startPoint > 12 else -1
            pointLength = abs(board_location_list[startPoint-1])
            tempSprite = arcade.Sprite("Images/Move.png",0.07)
            tempSprite.center_x = Master_Location_Dict[startPoint][0]
            tempSprite.center_y = Master_Location_Dict[startPoint][1] + (60*(pointLength - 1)*o)
            tempSprite.move = move
        
        sprites.append(tempSprite)

    return sprites
def createMoveEndSprites(activeSprite,Board): #UPDATE NEEDED
    board_location_list = Board.positions
    sprites = arcade.SpriteList()

    for move in activeSprite.move[1]:

        if move == 2002:
            tempSprite = arcade.Sprite("Images/Submove.png",.07)
            tempSprite.center_x = 150
            tempSprite.center_y = 400
            tempSprite.pos = move

        else:
            o = 1 if move > 12 else -1
            pointLength = abs(board_location_list[move-1]) - 1
            if pointLength == -1:
                pointLength = 0
            tempSprite = arcade.Sprite("Images/Submove.png",.07)
            tempSprite.center_x = Master_Location_Dict[move][0]
            tempSprite.center_y = Master_Location_Dict[move][1] + (60*pointLength*o)
            tempSprite.pos = move

        sprites.append(tempSprite)

    return sprites

#Drawing Move Line:
def GenerateMoveLineDataFast(Move,Board): #UPDATE NEEDED
    startPoint = Move[0]
    endPoint = Move[1]

    if startPoint == 1001:
        startX = 601
        startY = 401
    else:
        orientationStart = 1 if startPoint > 12 else -1
        numberOnStartPoint = abs(Board.positions[startPoint-1])
        startX = Master_Location_Dict[startPoint][0]
        if numberOnStartPoint < 7:
            startY = Master_Location_Dict[startPoint][1] + (60*numberOnStartPoint*orientationStart)
        else:
            offset = 360/numberOnStartPoint
            startY = Master_Location_Dict[startPoint][1] + (offset*numberOnStartPoint*orientationStart)

    if endPoint == 2002:
        endX = 150
        endY = 401
    else:
        orientationEnd = 1 if endPoint > 12 else -1
        numberOnEndPoint = abs(Board.positions[endPoint-1])
        endX = Master_Location_Dict[endPoint][0]
        if numberOnEndPoint < 7:
            endY = Master_Location_Dict[endPoint][1]  + (60*(numberOnEndPoint - 1)*orientationEnd)
        else:
            offset = 360/numberOnEndPoint
            endY = Master_Location_Dict[endPoint][1]  + (offset*(numberOnEndPoint - 1)*orientationEnd)
        
    return (startX,startY,endX,endY)

def DrawMoveLines(Moves):
    if Moves == []:
        return
    elif type(Moves[1]) == int:
        arcade.draw_circle_outline(Moves[0],Moves[1],30,black,2)
        arcade.draw_line(Moves[0],Moves[1],Moves[2],Moves[3],black,2)
    else:
        for move in Moves:
            arcade.draw_circle_outline(move[0],move[1],30,black,2)
            arcade.draw_line(move[0],move[1],move[2],move[3],black,2)


### GAME STATES ###

#General: ---
def draw_Splash(buttons_excited,Game_Type,version):
    arcade.draw_text("BACKGAMMON",300,500,darkTextColor,60,600,"center")
    arcade.draw_text("By Wills Erda",300,440,lightTextColor,40,600,"center")
    drawSignature(version)
    drawButton("START",600,300,400,excited=buttons_excited[0])
    drawButton("SIM",600,150,200,excited=buttons_excited[1],defaultColor=(button_used if Game_Type == "0P" else button_default))
    drawButton("1 PLAYER",350,150,250,excited=buttons_excited[2],defaultColor=(button_used if Game_Type == "1P" else button_default))
    drawButton("2 PLAYER",850,150,250,excited=buttons_excited[3],defaultColor=(button_used if Game_Type == "2P" else button_default))
    drawButtonIcon(gear_icon,1125,725,excited=buttons_excited[4])
    drawButtonIcon(quit_icon,75,725,excited=buttons_excited[5])
    # Button 1: 375 < x < 825 and 262 < y < 338 
    # Button 2: 475 < x < 725 and 112 < y < 188
    # Button 3: 225 < x < 475 and 112 < y < 188
    # Button 4: 725 < x < 975 and 112 < y < 188
    # Button 5: 1085 < x < 1165 and 685 < y < 765
    # Button 6: 35 < x < 105 and 685 < y < 765

def draw_Settings(buttons_excited,game_settings):
    drawButton("Back",100,737,excited=buttons_excited[0])
    arcade.draw_text("General Settings",300,725,darkTextColor,30,600,"center",)
    arcade.draw_text("AI Settings",300,525,darkTextColor,30,600,"center",)
    arcade.draw_text("Input Method For 1P Games:",250,675,lightTextColor2,15,350,"right",bold=True,italic=True)
    arcade.draw_text("Sim Games Move Delay(sec):",250,625,lightTextColor2,15,350,"right",bold=True,italic=True)
    arcade.draw_text("Draw Lines For AI Move:",250,475,lightTextColor2,15,350,"right",bold=True,italic=True)
    arcade.draw_text("Display AI Info:",250,425,lightTextColor2,15,350,"right",bold=True,italic=True)
    arcade.draw_text("AI Agent:",250,375,lightTextColor2,15,350,"right",bold=True,italic=True)
    drawButtonSmall("Generated",700,682,100,30,buttons_excited[1],10,defaultColor=(button_used if game_settings["1P Inputs"] == "Generated" else button_default))
    drawButtonSmall("Inputted",825,682,100,30,buttons_excited[2],10,defaultColor=(button_used if game_settings["1P Inputs"] == "Inputted" else button_default))
    drawButtonSmall("1",665,632,30,30,buttons_excited[3],10,defaultColor=(button_used if game_settings["Sim Delay"] == 1 else button_default))
    drawButtonSmall("3",705,632,30,30,buttons_excited[4],10,defaultColor=(button_used if game_settings["Sim Delay"] == 3 else button_default))
    drawButtonSmall("5",745,632,30,30,buttons_excited[5],10,defaultColor=(button_used if game_settings["Sim Delay"] == 5 else button_default))
    drawButtonSmall("7",785,632,30,30,buttons_excited[6],10,defaultColor=(button_used if game_settings["Sim Delay"] == 7 else button_default))
    drawButtonSmall("10",825,632,30,30,buttons_excited[7],10,defaultColor=(button_used if game_settings["Sim Delay"] == 10 else button_default))
    drawButtonSmall("15",865,632,30,30,buttons_excited[8],10,defaultColor=(button_used if game_settings["Sim Delay"] == 15 else button_default))
    drawButtonSmall("On",700,482,100,30,buttons_excited[9],10,defaultColor=(button_used if game_settings["AI Lines"] == True else button_default))
    drawButtonSmall("Off",825,482,100,30,buttons_excited[10],10,defaultColor=(button_used if game_settings["AI Lines"] == False else button_default))
    drawButtonSmall("On",700,432,100,30,buttons_excited[11],10,defaultColor=(button_used if game_settings["Display AI Info"] == True else button_default))
    drawButtonSmall("Off",825,432,100,30,buttons_excited[12],10,defaultColor=(button_used if game_settings["Display AI Info"] == False else button_default))
    drawButtonSmall("Random",700,382,100,30,buttons_excited[13],10,defaultColor=(button_used if game_settings["AI Player"] == "Random" else button_default))
    drawButtonSmall("PBP",825,382,100,30,buttons_excited[14],10,defaultColor=(button_used if game_settings["AI Player"] == "PBP" else button_default))
    drawButtonSmall("TS1",950,382,100,30,buttons_excited[15],10,defaultColor=(button_used if game_settings["AI Player"] == "Tree Search I" else button_default))
    drawButtonSmall("TBD1",1075,382,100,30,buttons_excited[16],10,defaultColor=(button_used if game_settings["AI Player"] == "TBD1" else button_default))
    drawButtonSmall("TBD2",700,332,100,30,buttons_excited[17],10,defaultColor=(button_used if game_settings["AI Player"] == "TBD2" else button_default))
    drawButtonSmall("TBD3",825,332,100,30,buttons_excited[18],10,defaultColor=(button_used if game_settings["AI Player"] == "TBD3" else button_default))
    drawButtonSmall("TBD4",950,332,100,30,buttons_excited[19],10,defaultColor=(button_used if game_settings["AI Player"] == "TBD4" else button_default))
    drawButtonSmall("TBD5",1075,332,100,30,buttons_excited[20],10,defaultColor=(button_used if game_settings["AI Player"] == "TBD5" else button_default))
    # Button 1: 25 < x < 175 and 700 < y <775
    # Button 2: 650 < x < 750 and 675 < y < 705
    # Button 3: 775 < x < 875 and 675 < y < 705
    # Button 4: 650 < x < 680 and 625 < y < 655
    # Button 5: 690 < x < 720 and 625 < y < 655
    # Button 6: 730 < x < 760 and 625 < y < 655
    # Button 7: 770 < x < 800 and 625 < y < 655
    # Button 8: 810 < x < 840 and 625 < y < 655
    # Button 9: 850 < x < 880 and 625 < y < 655
    # Button 10: 650 < x < 750 and 475 < y < 505
    # Button 11: 775 < x < 875 and 475 < y < 505
    # Button 12: 650 < x < 750 and 425 < y < 455
    # Button 13: 775 < x < 875 and 425 < y < 455
    # Button 14: 650 < x < 750 and 375 < y < 405
    # Button 15: 775 < x < 875 and 375 < y < 405
    # Button 16: 900 < x < 1000 and 375 < y < 405

#2 Player: ---
def draw_2P_PreStart(buttons_excited):
    drawBoard()
    drawButton("PLAY",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)
    #Button1: 1025 < x < 1175 and 362 < y < 438
    #Button2: 20 < x < 80 and 720 < y < 780
    #Button3: 20 < x < 80 and 650 < y < 710
    
def draw_2P_GameStart(buttons_excited,Board):
    drawBoard()
    drawPieces(Board.positions,Board.pip)
    drawButton("Roll",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)
    #Button1: 1025 < x < 1175 and 362 < y < 438
    #Button2: 20 < x < 80 and 720 < y < 780
    #Button3: 20 < x < 80 and 650 < y < 710

def draw_2P_PreTurnP1(buttons_excited,Board):
    drawBoard()
    color = checkerColor1
    arcade.draw_rectangle_filled(601,401,12,762,color)
    drawPieces(Board.positions,Board.pip)
    drawButton("Roll",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)

def draw_2P_PreTurnP2(buttons_excited,Board):
    drawBoard()
    color = checkerColor2
    arcade.draw_rectangle_filled(601,401,12,762,color)
    drawPieces(Board.positions,Board.pip)
    drawButton("Roll",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)

def draw_2P_TurnP1(buttons_excited,Board,Turn):
    drawBoard()
    color = checkerColor1
    arcade.draw_rectangle_filled(601,401,12,762,color)
    drawPieces(Board.positions,Board.pip)
    drawDice(Turn.roll[0],Turn.roll[1],Turn.unused_dice)
    drawButton("End",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)

def draw_2P_TurnP2(buttons_excited,Board,Turn):
    drawBoard()
    color = checkerColor2
    arcade.draw_rectangle_filled(601,401,12,762,color)
    drawPieces(Board.positions,Board.pip)
    drawDice(Turn.roll[0],Turn.roll[1],Turn.unused_dice)
    drawButton("End",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)

def draw_2P_Turn_Main(sprites):
    sprites.draw()

def draw_2P_Turn_Branch(main_sprite,sprites):
    main_sprite.draw()
    sprites.draw()

#1 Player: ---
def draw_1P_PreStart(buttons_excited):
    drawBoard()
    drawButton("PLAY",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)
    #Button1: 1025 < x < 1175 and 362 < y < 438
    #Button2: 20 < x < 80 and 720 < y < 780
    #Button3: 20 < x < 80 and 650 < y < 710

def draw_1P_GameStart(buttons_excited,Board):
    drawBoard()
    drawPieces(Board.positions,Board.pip)
    drawButton("Roll",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)
    #Button1: 1025 < x < 1175 and 362 < y < 438
    #Button2: 20 < x < 80 and 720 < y < 780
    #Button3: 20 < x < 80 and 650 < y < 710

def draw_1P_GameStart_Inputs(buttons_excited,Board):
    drawBoard()
    drawPieces(Board.positions,Board.pip)
    drawButtonMultiLine1("AI", "First",1100,500,150,150,buttons_excited[0])
    drawButtonMultiLine1("Human", "First",1100,300,150,150,buttons_excited[1])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[2],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[3],border=6)
    #Button1: 1025 < x < 1175 and 425 < y < 575
    #Button1: 1025 < x < 1175 and 225 < y < 375
    #Button2: 20 < x < 80 and 720 < y < 780
    #Button3: 20 < x < 80 and 650 < y < 710

def draw_1P_TurnHuman(buttons_excited,Board,Turn):
    drawBoard()
    color = checkerColor1
    arcade.draw_rectangle_filled(601,401,12,762,color)
    drawPieces(Board.positions,Board.pip)
    drawDice(Turn.roll[0],Turn.roll[1],Turn.unused_dice)
    drawButton("End",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)

def draw_1P_Turn_Main(sprites):
    sprites.draw()

def draw_1P_Turn_Branch(main_sprite,sprites):
    main_sprite.draw()
    sprites.draw()

def draw_1P_TurnAI(buttons_excited,Board,Turn):
    drawBoard()
    color = checkerColor2
    arcade.draw_rectangle_filled(601,401,12,762,color)
    drawPieces(Board.positions,Board.pip)
    drawDice(Turn.roll[0],Turn.roll[1],Turn.unused_dice)
    drawButton("Roll",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)

def draw_1P_RollInputs(buttons_excited,Board,player,selectedRolls):
    drawBoard()
    color = checkerColor1 if player == "Human" else checkerColor2
    arcade.draw_rectangle_filled(601,401,12,762,color)
    drawPieces(Board.positions,Board.pip)

    arcade.draw_text("Select Rolls",1000,600,black,20,200,"center",bold=True,italic=True)

    diceSub(1035,525,1,button_used if selectedRolls[0] == 1 else button_default,override=buttons_excited[0],altColor=button_excited)
    diceSub(1115,525,1,button_used if selectedRolls[1] == 1 else button_default,override=buttons_excited[1],altColor=button_excited)
    diceSub(1035,465,2,button_used if selectedRolls[0] == 2 else button_default,override=buttons_excited[2],altColor=button_excited)
    diceSub(1115,465,2,button_used if selectedRolls[1] == 2 else button_default,override=buttons_excited[3],altColor=button_excited)
    diceSub(1035,405,3,button_used if selectedRolls[0] == 3 else button_default,override=buttons_excited[4],altColor=button_excited)
    diceSub(1115,405,3,button_used if selectedRolls[1] == 3 else button_default,override=buttons_excited[5],altColor=button_excited)
    diceSub(1035,345,4,button_used if selectedRolls[0] == 4 else button_default,override=buttons_excited[6],altColor=button_excited)
    diceSub(1115,345,4,button_used if selectedRolls[1] == 4 else button_default,override=buttons_excited[7],altColor=button_excited)
    diceSub(1035,285,5,button_used if selectedRolls[0] == 5 else button_default,override=buttons_excited[8],altColor=button_excited)
    diceSub(1115,285,5,button_used if selectedRolls[1] == 5 else button_default,override=buttons_excited[9],altColor=button_excited)
    diceSub(1035,225,6,button_used if selectedRolls[0] == 6 else button_default,override=buttons_excited[10],altColor=button_excited)
    diceSub(1115,225,6,button_used if selectedRolls[1] == 6 else button_default,override=buttons_excited[11],altColor=button_excited)

    drawButton("Confirm",1100,150,150,60,excited=buttons_excited[12],fontSize=20,border=8)

    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[13],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[14],border=6)

    #Button 1: 1035 < x < 1085 and 525 < y < 575
    #Button 2: 1115 < x < 1165 and 525 < y < 575
    #Button 3: 1035 < x < 1085 and 465 < y < 515
    #Button 4: 1115 < x < 1165 and 465 < y < 515
    #Button 5: 1035 < x < 1085 and 405 < y < 455
    #Button 6: 1115 < x < 1165 and 405 < y < 455
    #Button 7: 1035 < x < 1085 and 345 < y < 395
    #Button 8: 1115 < x < 1165 and 345 < y < 395
    #Button 9: 1035 < x < 1085 and 285 < y < 335
    #Button 10: 1115 < x < 1165 and 285 < y < 335
    #Button 11: 1035 < x < 1085 and 225 < y < 275
    #Button 12: 1115 < x < 1165 and 225 < y < 275
    #Button 13: 1025 < x < 1175 and 120 < y < 180
    #Button 14: 20 < x < 80 and 720 < y < 780
    #Button 15: 20 < x < 80 and 650 < y < 710

#Simulation: ---
def draw_0P_PreStart(buttons_excited,Board):
    drawBoard()
    drawPieces(Board.positions,Board.pip)
    drawButton("Play",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[1],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[2],border=6)
    #Button1: 1025 < x < 1175 and 362 < y < 438
    #Button2: 20 < x < 80 and 720 < y < 780
    #Button3: 20 < x < 80 and 650 < y < 710
def draw_0P_Turn(buttons_excited,Board,Turn):
    drawBoard()
    color = checkerColor1 if Turn.player == 1 else checkerColor2
    arcade.draw_rectangle_filled(601,401,12,762,color)
    drawPieces(Board.positions,Board.pip)
    drawDice(Turn.roll[0],Turn.roll[1],Turn.unused_dice)
    drawButton("Next",1100,400,150,75,buttons_excited[0])
    drawButtonIcon(exit_icon,50,750,60,60,excited=buttons_excited[2],border=6)
    drawButtonIcon(gear_icon,50,680,60,60,excited=buttons_excited[3],border=6)
    #Button1: 1025 < x < 1175 and 262 < y < 338
    #Button3: 20 < x < 80 and 720 < y < 780
    #Button4: 20 < x < 80 and 650 < y < 710


#Game Over: --- 
def draw_GameOver(player,buttons_excited,version,TurnNumber):
    color = checkerColor1 if player == 1 else checkerColor2
    arcade.draw_rectangle_filled(600,400,1200,800,color)
    arcade.draw_text("GAME OVER",300,500,arcade.color.BLACK,60,600,"center")
    arcade.draw_text(TurnNumber,10,10,black,)
    drawButton("New",425,300,200,excited=buttons_excited)
    drawButton("Quit",775,300,200,excited=buttons_excited)
    drawSignature(version)
    #Button 1: 325 < x < 525 and 262 < y < 338
    #Button 2: 575 < x < 775 and 262 < y < 338