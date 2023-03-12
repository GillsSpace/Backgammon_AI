#Imports
import arcade

#Load images & sounds:
gear_icon = arcade.load_texture("Images\gear_icon.png")
button_click = arcade.Sound("Sounds/sound3.mp3")


#Theme:
button_default = arcade.color.ALMOND
button_excited = arcade.color.AERO_BLUE
button_used = arcade.color.CHARCOAL
checkerColor1 = arcade.color.AERO_BLUE
darkTextColor = arcade.color.BLACK
lightTextColor = arcade.color.AERO_BLUE
lightTextColor2 = arcade.color.ALMOND
Background = arcade.color.DARK_SCARLET
board_color = arcade.color.ALMOND
board_border = arcade.color.BLACK_BEAN

Accent1 = arcade.color.OTTER_BROWN
Accent2 = arcade.color.ROSY_BROWN
black = arcade.color.BLACK


#Helper Functions:
def draw_button(text, centerx, centery, width=150, height=75, excited=False, fontSize=30, defaultColor=board_color):
    color = defaultColor if excited == False else button_excited
    arcade.draw_rectangle_filled(centerx,centery,width,height,color)
    arcade.draw_rectangle_outline(centerx,centery,width,height,board_border,12)
    arcade.draw_text(text,(centerx - (.5*width)),(centery - 15),arcade.color.BLACK,fontSize,width,"center","arial",bold=True)
def draw_button_icon(icon, centerx, centery, width=75, height=75, excited=False, defaultColor=board_color):
    color = defaultColor if excited == False else button_excited
    arcade.draw_rectangle_filled(centerx,centery,width,height,color)
    arcade.draw_rectangle_outline(centerx,centery,width,height,board_border,12)
    arcade.draw_texture_rectangle(centerx,centery,width-25,height-25,icon)
def draw_button_small(text,centerx,centery,width,height,excited=False, fontSize=15, defaultColor=board_color):
    color = defaultColor if excited == False else button_excited
    arcade.draw_rectangle_filled(centerx,centery,width,height,color)
    arcade.draw_rectangle_outline(centerx,centery,width,height,board_border,6)
    arcade.draw_text(text,(centerx - (.5*width)),(centery - 5),arcade.color.BLACK,fontSize,width,"center","arial",bold=True)
def drawSignature(version):
    arcade.draw_text("Backgammon by Wills Erda",1000,25,black,10)
    arcade.draw_text(f"v{version} @2022 ",1000,10,black,10)
    


#Pages:

#Splash Page:
def drawSplashPage(buttons_excited,Game_Type,version):
    arcade.draw_text("BACKGAMMON",300,500,darkTextColor,60,600,"center")
    arcade.draw_text("By Wills Erda",300,440,lightTextColor,40,600,"center")
    drawSignature(version)
    draw_button("START",600,300,400,excited=buttons_excited[0])
    draw_button("SIM",600,150,200,excited=buttons_excited[1],defaultColor=(button_used if Game_Type == "0P" else button_default))
    draw_button("1 PLAYER",350,150,250,excited=buttons_excited[2],defaultColor=(button_used if Game_Type == "1P" else button_default))
    draw_button("2 PLAYER",850,150,250,excited=buttons_excited[3],defaultColor=(button_used if Game_Type == "2P" else button_default))
    draw_button_icon(gear_icon,1125,725,excited=buttons_excited[4])
    # Button 1: 375 < x < 825 and 262 < y < 338 
    # Button 2: 475 < x < 725 and 112 < y < 188
    # Button 3: 225 < x < 475 and 112 < y < 188
    # Button 4: 725 < x < 975 and 112 < y < 188
    # Button 5: 1085 < x < 1165 and 685 < y < 765

def drawSettingsPage(buttons_excited,game_settings):
    draw_button("Back",100,737,excited=buttons_excited[0])
    arcade.draw_text("General Settings",300,725,darkTextColor,30,600,"center",)
    arcade.draw_text("AI Settings",300,525,darkTextColor,30,600,"center",)
    arcade.draw_text("Input Method For 1P Games:",250,675,lightTextColor2,15,350,"right",bold=True,italic=True)
    arcade.draw_text("Sim Games Move Delay(sec):",250,625,lightTextColor2,15,350,"right",bold=True,italic=True)
    arcade.draw_text("Draw Lines For AI Move:",250,475,lightTextColor2,15,350,"right",bold=True,italic=True)
    arcade.draw_text("Display AI Info:",250,425,lightTextColor2,15,350,"right",bold=True,italic=True)
    arcade.draw_text("AI Agent:",250,375,lightTextColor2,15,350,"right",bold=True,italic=True)
    draw_button_small("Generated",700,682,100,30,buttons_excited[1],10,defaultColor=(button_used if game_settings["1P Inputs"] == "Generated" else button_default))
    draw_button_small("Inputted",825,682,100,30,buttons_excited[2],10,defaultColor=(button_used if game_settings["1P Inputs"] == "Inputted" else button_default))
    draw_button_small("1",665,632,30,30,buttons_excited[3],10,defaultColor=(button_used if game_settings["Sim Delay"] == 1 else button_default))
    draw_button_small("3",705,632,30,30,buttons_excited[4],10,defaultColor=(button_used if game_settings["Sim Delay"] == 3 else button_default))
    draw_button_small("5",745,632,30,30,buttons_excited[5],10,defaultColor=(button_used if game_settings["Sim Delay"] == 5 else button_default))
    draw_button_small("7",785,632,30,30,buttons_excited[6],10,defaultColor=(button_used if game_settings["Sim Delay"] == 7 else button_default))
    draw_button_small("10",825,632,30,30,buttons_excited[7],10,defaultColor=(button_used if game_settings["Sim Delay"] == 10 else button_default))
    draw_button_small("15",865,632,30,30,buttons_excited[8],10,defaultColor=(button_used if game_settings["Sim Delay"] == 15 else button_default))
    draw_button_small("On",700,482,100,30,buttons_excited[9],10,defaultColor=(button_used if game_settings["AI Lines"] == True else button_default))
    draw_button_small("Off",825,482,100,30,buttons_excited[10],10,defaultColor=(button_used if game_settings["AI Lines"] == False else button_default))
    draw_button_small("On",700,432,100,30,buttons_excited[11],10,defaultColor=(button_used if game_settings["Display AI Info"] == True else button_default))
    draw_button_small("Off",825,432,100,30,buttons_excited[12],10,defaultColor=(button_used if game_settings["Display AI Info"] == False else button_default))
    draw_button_small("Random",700,382,100,30,buttons_excited[13],10,defaultColor=(button_used if game_settings["AI Player"] == "Random" else button_default))
    draw_button_small("Tree",825,382,100,30,buttons_excited[14],10,defaultColor=(button_used if game_settings["AI Player"] == "Tree" else button_default))
    draw_button_small("DRL",950,382,100,30,buttons_excited[15],10,defaultColor=(button_used if game_settings["AI Player"] == "DRL" else button_default))
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


    
