#Imports
import arcade
import copy

#Themes:
def theme1():
    global Excited_Button
    global Background
    global board_color
    global board_border
    global Piece1
    global Piece2
    global Accent1
    global Accent2
    global black
    Excited_Button = arcade.color.AERO_BLUE
    Background = arcade.color.DARK_SCARLET
    board_color = arcade.color.ALMOND
    board_border = arcade.color.BLACK_BEAN
    Piece1 = arcade.color.SIENNA
    Piece2 = arcade.color.SKY_BLUE
    Accent1 = arcade.color.OTTER_BROWN
    Accent2 = arcade.color.ROSY_BROWN
    black = arcade.color.BLACK
theme1()

#Data
Master_Location_Dict = {1:(247,755),2:(307,755),3:(367,755),4:(427,755),5:(487,755),6:(547,755),7:(655,755),8:(715,755),9:(775,755),10:(835,755),11:(895,755),12:(955,755),13:(955,47),14:(895,47),15:(835,47),16:(775,47),17:(715,47),18:(655,47),19:(547,47),20:(487,47),21:(427,47),22:(367,47),23:(307,47),24:(247,47)}


#Sounds
basicMove = arcade.Sound()

#Helper Functions
def draw_button(text, centerx, centery, width=150, height=75, excited=False, fontSize=30, defaultColor=board_color):
    color = defaultColor if excited == False else Excited_Button
    arcade.draw_rectangle_filled(centerx,centery,width,height,color)
    arcade.draw_rectangle_outline(centerx,centery,width,height,board_border,12)
    arcade.draw_text(text,(centerx - (.5*width)),(centery - 15),arcade.color.BLACK,fontSize,width,"center","arial",bold=True)

#Drawing the board
def drawSignature():
    arcade.draw_text("Backgammon by Wills Erda",1000,25,black,10)
    arcade.draw_text("v0.3 @2022 ",1000,10,black,10)
def drawBoard(): 
    arcade.draw_rectangle_outline(601,401,774,774,board_border,12)
    arcade.draw_rectangle_filled(601,401,768,768,board_color)
    arcade.draw_rectangle_outline(601,401,24,774,board_border,12)

    def drawTriangles(x,y,o): #OffsetX, OffsetY, Orientation(1 or -1)
        color1 = Accent1 if o == 1 else Accent2
        color2 = Accent2 if o == 1 else Accent1
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
def drawSideboard():
    arcade.draw_rectangle_outline(150,201,64,304,board_border,8)
    arcade.draw_rectangle_outline(150,601,64,304,board_border,8)
    arcade.draw_rectangle_filled(150,201,60,300,board_color)
    arcade.draw_rectangle_filled(150,601,60,300,board_color)
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

    def diceSub(baseX,baseY,num,color):
        p1 = [baseX+13,baseY+13]
        p2 = [baseX+13,baseY+25]
        p3 = [baseX+13,baseY+38]
        p4 = [baseX+25,baseY+25]
        p5 = [baseX+38,baseY+13]
        p6 = [baseX+38,baseY+25]
        p7 = [baseX+38,baseY+38]
        arcade.draw_rectangle_filled(baseX+25,baseY+25,50,50,color)
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
    diceSub(1040,455,num1, board_color if U1 == False else arcade.color.CHARCOAL)
    diceSub(1110,455,num2, board_color if U2 == False else arcade.color.CHARCOAL)
    if num1 == num2:
        diceSub(1040,515,num1, board_color if U3 == False else arcade.color.CHARCOAL)
        diceSub(1110,515,num2, board_color if U4 == False else arcade.color.CHARCOAL)
def drawPIP(pip):
    arcade.draw_rectangle_filled(150,25,60,30,board_border)
    arcade.draw_rectangle_filled(150,775,60,30,board_border)
    arcade.draw_rectangle_outline(150,25,60,30,black,2)
    arcade.draw_rectangle_outline(150,775,60,30,black,2)
    arcade.draw_text(pip[0],75,15,board_color,20,150,"center","arial")
    arcade.draw_text(pip[1],75,765,board_color,20,150,"center","arial")

#Draw Pieces & Pip
def drawPieces(LocationList,Sideboard_Pieces_List,Out_Pieces_List,pip):
    drawPIP(pip)
    for listNum in range(len(LocationList,)):
        listNum = listNum + 1
        list = LocationList[listNum - 1]
        if len(list) != 0: #Set Necessary Variables For Drawn Points
            color = Piece1 if list[0] == 1 else Piece2
            location = listNum
            orientation = 1 if location > 12 else -1
            centerx = Master_Location_Dict[location][0]
            centery = Master_Location_Dict[location][1] 
        if len(list) < 7 and len(list) != 0: #Draw Points with 6 or less Pieces
            for i in range(len(list)):
                offset = ((i)*60*orientation)
                arcade.draw_circle_filled(centerx,centery+offset,30,color)
                arcade.draw_circle_outline(centerx,centery+offset,30,arcade.color.BLACK,2)
        if len(list) > 6: #Draw  Points with 7 or more Pieces
            for i in range(len(list)):
                height = 360/len(list)
                offset = ((i)*height*orientation)
                adjustment = (30-height)*orientation
                arcade.draw_ellipse_filled(centerx,centery+offset+adjustment,60,height,color)
                arcade.draw_ellipse_outline(centerx,centery+offset+adjustment,60,height,arcade.color.BLACK,2)
    for pc in range(Sideboard_Pieces_List[0]):
        arcade.draw_rectangle_filled(150,341-(20*(pc)),60,20,Piece1)
        arcade.draw_line(120,331-(20*pc),180,331-(20*pc),arcade.color.BLACK,2)
    for pc in range(Sideboard_Pieces_List[1]):
        arcade.draw_rectangle_filled(150,461+(20*(pc)),60,20,Piece2)
        arcade.draw_line(120,471+(20*pc),180,471+(20*pc),arcade.color.BLACK,2)
    if len(Out_Pieces_List) != 0:
        totalDist = 70 * len(Out_Pieces_List)
        startDist = totalDist/2
        for pc in range(len(Out_Pieces_List)):
            color = Piece1 if Out_Pieces_List[pc] == 1 else Piece2
            arcade.draw_circle_filled(601,401-startDist+35+(60*pc),30,color)
            arcade.draw_circle_outline(601,401-startDist+35+(60*pc),30,arcade.color.BLACK,2)

#Sprite Management
def createMoveStartSprites(possibleMoves,Board,player):
    board_location_list = Board.locationList
    board_hit_list = Board.hitPieceList
    sprites = arcade.SpriteList()

    for move in possibleMoves:
        startPoint = move[0]

        if startPoint == "hit":
            totalDist = 70 * len(board_hit_list)
            startDist = totalDist/2
            for pc in range(len(board_hit_list)):
                doDraw = True if board_hit_list[pc] == player else False
                if doDraw == True:
                    tempSprite = arcade.Sprite("C:/Users/wills/OneDrive/Desktop/WFE/Code/(W) Backgammon/Images/Move.png",0.07)
                    tempSprite.center_x = 601
                    tempSprite.center_y = 401-startDist+35+(60*pc)
                    tempSprite.move = move
        
        else:
            o = 1 if startPoint > 12 else -1
            pointLength = len(board_location_list[startPoint-1]) - 1
            tempSprite = arcade.Sprite("C:/Users/wills/OneDrive/Desktop/WFE/Code/(W) Backgammon/Images/Move.png",0.07)
            tempSprite.center_x = Master_Location_Dict[startPoint][0]
            tempSprite.center_y = Master_Location_Dict[startPoint][1] + (60*pointLength*o)
            tempSprite.move = move
        
        sprites.append(tempSprite)
    
    return sprites
def createMoveEndSprites(activeSprite,Board,player):
    board_location_list = Board.locationList
    sprites = arcade.SpriteList()

    for move in activeSprite.move[1]:

        if move == "safe":
            tempSprite = arcade.Sprite("C:/Users/wills/OneDrive/Desktop/WFE/Code/(W) Backgammon/Images/Submove.png",.07)
            tempSprite.center_x = 150
            tempSprite.center_y = 400
            tempSprite.pos = move

        else:
            o = 1 if move > 12 else -1
            pointLength = len(board_location_list[move-1]) - 1
            if pointLength == -1:
                pointLength = 0
            tempSprite = arcade.Sprite("C:/Users/wills/OneDrive/Desktop/WFE/Code/(W) Backgammon/Images/Submove.png",.07)
            tempSprite.center_x = Master_Location_Dict[move][0]
            tempSprite.center_y = Master_Location_Dict[move][1] + (60*pointLength*o)
            tempSprite.pos = move

        sprites.append(tempSprite)

    return sprites

### GAME STATES ###

#Splash Screen
def draw_splash(is_excited_1,is_excited_2,is_excited_3,is_excited_4,type):
    arcade.draw_text("BACKGAMMON",300,500,arcade.color.BLACK,60,600,"center")
    arcade.draw_text("By Wills Erda",300,440,arcade.color.AERO_BLUE,40,600,"center")
    draw_button("START",600,300,400,excited=is_excited_1)
    draw_button("SIM",600,150,200,excited=is_excited_2,defaultColor=(arcade.color.CHARCOAL if type == "0P" else board_color))
    draw_button("1 PLAYER",350,150,250,excited=is_excited_3,defaultColor=(arcade.color.CHARCOAL if type == "1P" else board_color))
    draw_button("2 PLAYER",850,150,250,excited=is_excited_4,defaultColor=(arcade.color.CHARCOAL if type == "2P" else board_color))

#Pre-Start
def draw_pre_start(is_excited):
    drawBoard()
    drawSideboard()
    draw_button("PLAY",1100,400,150,75,is_excited)

#Game-Start
def draw_game_start(is_excited,Board):
    drawBoard()
    drawSideboard()
    drawPieces(Board.locationList,Board.sideboardList,Board.hitPieceList,Board.calcPip())
    draw_button("ROLL",1100,400,150,75,is_excited)

#Turn-Start
def draw_turn_start(player,is_excited_roll,is_excited_double,Board):
    drawBoard()
    color = Piece1 if player == 1 else Piece2
    arcade.draw_rectangle_filled(601,401,12,762,color)
    drawSideboard()
    drawPieces(Board.locationList,Board.sideboardList,Board.hitPieceList,Board.calcPip())
    draw_button("ROLL",1100,351,150,75,is_excited_roll)
    draw_button("DOUBLE",1100,451,150,75,is_excited_double,20)

#Turns
def draw_turn(player,is_excited,Board,Turn):
    drawBoard()
    color = Piece1 if player == 1 else Piece2
    arcade.draw_rectangle_filled(601,401,12,762,color)
    drawSideboard()
    drawPieces(Board.locationList,Board.sideboardList,Board.hitPieceList,Board.calcPip())
    drawDice(Turn.roll[0],Turn.roll[1],Turn.availableRolls)
    draw_button("END",1100,400,150,75,is_excited)
def draw_turn_main(sprites):
    sprites.draw()
def draw_turn_branch(main_sprite,sprites):
    main_sprite.draw()
    sprites.draw()

def draw_Game_Over(player,is_excited):
    color = Piece1 if player == 1 else Piece2
    arcade.draw_rectangle_filled(600,400,1200,800,color)
    arcade.draw_text("GAME OVER",300,500,arcade.color.BLACK,60,600,"center")
    arcade.draw_text("By Wills Erda",300,440,arcade.color.AERO_BLUE,40,600,"center")
    draw_button("New",600,300,200,excited=is_excited)



