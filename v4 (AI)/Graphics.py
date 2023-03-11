#Imports
import arcade

#Themes
def Theme1():
    global checkerColor1
    global darkTextColor 
    global lightTextColor
    checkerColor1 = arcade.color.AERO_BLUE
    darkTextColor = arcade.color.BLACK
    lightTextColor = arcade.color.AERO_BLUE

#

#Pages:

def drawSplashPage(Excited_Button_list,Current_Game_Type):
    arcade.draw_text("BACKGAMMON",300,500,darkTextColor,60,600,"center")
    arcade.draw_text("By Wills Erda",300,440,lightTextColor,40,600,"center")

