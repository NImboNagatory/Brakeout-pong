from func import Pong_screen, ico
from tkinter import Tk

gui = Tk()

gui.title("BrakeOut_Pong")

gui.resizable(False, False)

gui.geometry("801x698")

ico(gui)

screen = Pong_screen(gui)

screen.grid()

LOOP_ACTIVE = True
while LOOP_ACTIVE:
    screen.game()
    gui.update()
