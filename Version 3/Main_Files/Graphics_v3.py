#Imports
import arcade
import copy
import arcade.gui

import os
import pathlib
PATH = pathlib.Path(__file__).parent.parent.parent
os.chdir(PATH)

#Load images & sounds:
gear_icon = arcade.load_texture("Version 3\Images\gear_icon.png")
exit_icon = arcade.load_texture("Version 3\Images\exit_icon.png")
quit_icon = arcade.load_texture("Version 3\Images\quit_icon.png")

delete_icon = arcade.load_texture("Version 3\Images\delete_icon.png")
darkPiece_icon = arcade.load_texture("Version 3\Images\darkPiece.png")
lightPiece_icon = arcade.load_texture("Version 3\Images\lightPiece.png")
restart_icon = arcade.load_texture("Version 3\Images\\restart_icon.png")

delete_icon2 = arcade.load_texture("Version 3\Images\delete_icon2.png")
darkPiece_icon2 = arcade.load_texture("Version 3\Images\darkPiece2.png")
lightPiece_icon2 = arcade.load_texture("Version 3\Images\lightPiece2.png")
restart_icon2 = arcade.load_texture("Version 3\Images\\restart_icon2.png")

delete_icon3 = arcade.load_texture("Version 3\Images\delete_icon3.png")
darkPiece_icon3 = arcade.load_texture("Version 3\Images\darkPiece3.png")
lightPiece_icon3 = arcade.load_texture("Version 3\Images\lightPiece3.png")
restart_icon3 = arcade.load_texture("Version 3\Images\\restart_icon3.png")


#Data:
Master_Location_Dict = {1:(247,755),2:(307,755),3:(367,755),4:(427,755),5:(487,755),6:(547,755),7:(655,755),8:(715,755),9:(775,755),10:(835,755),11:(895,755),12:(955,755),13:(955,47),14:(895,47),15:(835,47),16:(775,47),17:(715,47),18:(655,47),19:(547,47),20:(487,47),21:(427,47),22:(367,47),23:(307,47),24:(247,47)}

#Theme:
button_default = arcade.color.ALMOND
button_excited = arcade.color.AERO_BLUE
button_used = arcade.color.CHARCOAL
darkCheckerColor = arcade.color.SIENNA
lightCheckerColor = arcade.color.SKY_BLUE
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
def drawSignature(version):
    arcade.draw_text("Backgammon by Wills Erda",1000,25,black,10)
    arcade.draw_text(f"v{version} @2022 ",1000,10,black,10)
def drawButtonIcon(icon, centerx, centery, width=75, height=75, excited=False, defaultColor=board_color, border=12):
    color = defaultColor if excited == False else button_excited
    arcade.draw_rectangle_filled(centerx,centery,width,height,color)
    arcade.draw_rectangle_outline(centerx,centery,width,height,board_border,border)
    arcade.draw_texture_rectangle(centerx,centery,width-25,height-25,icon)

def drawTurnMain(sprites):
    sprites.draw()

def drawTurnBranch(main_sprite,sub_sprites):
    main_sprite.draw()
    sub_sprites.draw()


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
    diceSub(1040,445,num1, board_color if U1 == False else arcade.color.CHARCOAL)
    diceSub(1110,445,num2, board_color if U2 == False else arcade.color.CHARCOAL)
    if num1 == num2:
        diceSub(1040,385,num1, board_color if U3 == False else arcade.color.CHARCOAL)
        diceSub(1110,385,num2, board_color if U4 == False else arcade.color.CHARCOAL)

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
            color = darkCheckerColor if pointNum < 0 else lightCheckerColor
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
        arcade.draw_rectangle_filled(150,341-(20*(pc)),60,20,darkCheckerColor)
        arcade.draw_line(120,331-(20*pc),180,331-(20*pc),arcade.color.BLACK,2)
    for pc in range(positions[27]):
        arcade.draw_rectangle_filled(150,461+(20*(pc)),60,20,lightCheckerColor)
        arcade.draw_line(120,471+(20*pc),180,471+(20*pc),arcade.color.BLACK,2)
    if positions[24] != 0 or positions[25] != 0:
        list1 = [1] * positions[24]
        list2 = [2] * positions[25]
        barList = list1 + list2
        totalDist = 70 * len(barList)
        startDist = totalDist/2
        for pc in range(len(barList)):
            color = darkCheckerColor if barList[pc] == 1 else lightCheckerColor
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
def GenerateMoveLineDataFast(Move,Board):
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
def DrawMoveLines(MoveData):
    if MoveData == []:
        return
    elif type(MoveData[1]) == int or type(MoveData[1]) == float:
        arcade.draw_circle_outline(MoveData[0],MoveData[1],30,black,2)
        arcade.draw_line(MoveData[0],MoveData[1],MoveData[2],MoveData[3],black,2)
    else:
        for move in MoveData:
            arcade.draw_circle_outline(move[0],move[1],30,black,2)
            arcade.draw_line(move[0],move[1],move[2],move[3],black,2)

#Help Drawing Views:
def DrawSettings(settings):

    arcade.draw_rectangle_filled(650,675,1000,60,board_color)
    arcade.draw_rectangle_filled(650,600,1000,60,board_color)

    if settings["Agent1"] == "Human":
        arcade.draw_rectangle_filled(315,675,120,60,button_used)
    elif settings["Agent1"] == "Random":
        arcade.draw_rectangle_filled(430,675,120,60,button_used)
    elif settings["Agent1"] == "PBP":
        arcade.draw_rectangle_filled(545,675,120,60,button_used)
    elif settings["Agent1"] == "TS 1":
        arcade.draw_rectangle_filled(660,675,120,60,button_used)
    elif settings["Agent1"] == "TS 2":
        arcade.draw_rectangle_filled(775,675,120,60,button_used)
    elif settings["Agent1"] == "Network":
        arcade.draw_rectangle_filled(990,675,320,60,button_used)

    if settings["Agent2"] == "Human":
        arcade.draw_rectangle_filled(315,600,120,60,button_used)
    elif settings["Agent2"] == "Random":
        arcade.draw_rectangle_filled(430,600,120,60,button_used)
    elif settings["Agent2"] == "PBP":
        arcade.draw_rectangle_filled(545,600,120,60,button_used)
    elif settings["Agent2"] == "TS 1":
        arcade.draw_rectangle_filled(660,600,120,60,button_used)
    elif settings["Agent2"] == "TS 2":
        arcade.draw_rectangle_filled(775,600,120,60,button_used)
    elif settings["Agent2"] == "Network":
        arcade.draw_rectangle_filled(990,600,320,60,button_used)

    arcade.draw_rectangle_filled(1040,675,200,40,arcade.color.WHITE)
    arcade.draw_rectangle_filled(1040,600,200,40,arcade.color.WHITE)
def DrawBarBoxes():
    arcade.draw_rectangle_filled(530,401,50,100,darkCheckerColor)
    arcade.draw_rectangle_filled(670,401,50,100,lightCheckerColor)
    arcade.draw_rectangle_outline(530,401,50,100,black,2)
    arcade.draw_rectangle_outline(670,401,50,100,black,2)
    arcade.draw_text("B",505,416,arcade.color.WHITE,20,50,"center",bold=True,multiline=True)
    arcade.draw_text("A",505,391,arcade.color.WHITE,20,50,"center",bold=True,multiline=True)
    arcade.draw_text("R",505,366,arcade.color.WHITE,20,50,"center",bold=True,multiline=True)
    arcade.draw_text("B",645,416,arcade.color.WHITE,20,50,"center",bold=True,multiline=True)
    arcade.draw_text("A",645,391,arcade.color.WHITE,20,50,"center",bold=True,multiline=True)
    arcade.draw_text("R",645,366,arcade.color.WHITE,20,50,"center",bold=True,multiline=True)
def DrawSimMain():
    arcade.draw_rectangle_filled(1098,285,175,40,board_color)

