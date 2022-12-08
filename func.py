from tkinter import Frame, Canvas
from turtle import TurtleScreen, RawTurtle
from PIL import Image, ImageTk
from playsound import playsound
import random


class Pong_screen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.sound_on = True
        self.y_cor = None
        self.x_cor = None
        self.lives = 3
        self.player_cord = 0
        self.canvas = Canvas(self)
        self.canvas.config(width=799, height=695)
        self.screen = TurtleScreen(self.canvas)
        self.canvas.grid()
        self.screen.bgcolor("#f4fce3")
        self.player_turtle = None
        self.ball_turtle = None
        self.guideline_turtle = None
        self.lives_turtle = None
        self.score_turtle = None
        self.score = 0
        self.ball_x = 3
        self.ball_y = 3
        self.broken = 0
        self.draw_guidelines()
        self.create_player()
        self.bind_mouse(master)
        self.draw_lives()
        self.draw_score()
        self.walls = []
        self.draw_breakout()
        self.create_ball()

    def draw_breakout(self):
        for turtles in range(150):
            self.walls.append(RawTurtle(self.screen, shape="square"))
        x_loc = -350
        y_loc = 250
        for char in self.walls:
            char.shapesize(stretch_wid=2, stretch_len=0.7)
            char.penup()
            char.speed("fastest")
            char.setheading(90)
            if x_loc != 350:
                x_loc += 50
            if self.walls.index(char) % 15 == 0:
                x_loc = -350
                y_loc -= 20
            char.goto(x_loc, y_loc)

    def check_breakout(self):
        for char in self.walls:
            if self.ball_turtle.distance(char) < 20:
                char.hideturtle()
                char.goto(0, 900)
                self.bounce_y()
                self.score += 20
                self.play_sound("brake")
                self.score_turtle.clear()
                self.draw_score()
                self.broken += 1
                if self.broken == 150:
                    self.ball_turtle = None
                    self.show_breakout()
                    self.create_ball()

    def hide_breakout(self):
        for char in self.walls:
            char.hideturtle()

    def show_breakout(self):
        x_loc = -350
        y_loc = 250
        for char in self.walls:
            char.hideturtle()
            if x_loc != 350:
                x_loc += 50
            if self.walls.index(char) % 15 == 0:
                x_loc = -350
                y_loc -= 20
            char.goto(x_loc, y_loc)
            char.showturtle()

    def draw_score(self):
        if self.score_turtle is None:
            self.score_turtle = RawTurtle(self.screen, shape="turtle")
            self.score_turtle.hideturtle()
            self.score_turtle.pensize(width=200)
            self.score_turtle.color("black")
            self.score_turtle.speed("fastest")
            self.score_turtle.penup()
        self.score_turtle.goto(310, 290)
        self.score_turtle.write(self.score, font=("Arial", 20, "normal"))

    def draw_lives(self):
        if self.lives_turtle is None:
            self.lives_turtle = RawTurtle(self.screen, shape="turtle")
            self.lives_turtle.hideturtle()
            self.lives_turtle.pensize(width=20)
            self.lives_turtle.color("black")
            self.lives_turtle.speed("fastest")
            self.lives_turtle.penup()
        if self.lives == 3:
            self.lives_turtle.goto(-350, 310)
            self.lives_turtle.dot(20, "black")
            self.lives_turtle.goto(-330, 310)
            self.lives_turtle.dot(20, "black")
            self.lives_turtle.goto(-310, 310)
            self.lives_turtle.dot(20, "black")
        elif self.lives == 2:
            self.lives_turtle.goto(-350, 310)
            self.lives_turtle.dot(20, "black")
            self.lives_turtle.goto(-330, 310)
            self.lives_turtle.dot(20, "black")
        elif self.lives == 1:
            self.lives_turtle.goto(-350, 310)
            self.lives_turtle.dot(20, "black")

    def play_sound(self, state):
        if self.sound_on:
            if state == "start":
                playsound("data/start_beep.mp3")
            elif state == "wall":
                playsound("data/wall_beep.mp3")
            elif state == "player":
                playsound("data/player_beep.mp3")
            elif state == "brake":
                playsound("data/brake2.mp3")

    def create_ball(self):
        self.ball_turtle = RawTurtle(self.screen, shape="circle")
        self.ball_turtle.speed("fastest")
        self.ball_turtle.penup()
        self.ball_turtle.goto(x=self.player_cord, y=-300)
        self.play_sound("start")

    def final_screen(self):
        self.guideline_turtle.goto(0, 50)
        self.ball_turtle.hideturtle()
        self.guideline_turtle.write(f"Breakout\n\nYour score: {self.score}", font=("Arial", 20, "normal"))
        self.hide_breakout()
        self.ball_turtle = None
        self.after(5000)
        self.guideline_turtle.clear()
        self.score_turtle.clear()
        self.lives_turtle.clear()
        self.draw_guidelines()
        self.lives = 3
        self.score = 0
        self.draw_lives()
        self.draw_score()
        self.show_breakout()
        self.create_ball()

    def move(self):
        self.x_cor = self.ball_turtle.xcor() + self.ball_x
        self.y_cor = self.ball_turtle.ycor() + self.ball_y
        self.ball_turtle.goto(self.x_cor, self.y_cor)

    def check_reflect(self):
        if self.x_cor <= -377:
            self.bounce_x()
            self.play_sound("wall")

        elif self.x_cor >= 377:
            self.bounce_x()
            self.play_sound("wall")

        elif self.y_cor >= 327:
            self.bounce_y()
            self.play_sound("wall")

        elif self.ball_turtle.distance(self.player_turtle) <= 50 and self.y_cor < -320:
            self.play_sound("player")
            self.bounce_y()

        elif self.y_cor < -400:
            self.ball_turtle.goto(x=self.player_cord, y=-300)
            self.bounce_y()
            self.play_sound("start")
            self.lives_turtle.clear()
            if self.lives != 0:
                self.lives -= 1
            else:
                self.final_screen()
            self.draw_lives()

    def bounce_x(self):
        self.ball_x *= -1

    def bounce_y(self):
        self.ball_y *= -1

    def create_player(self):
        self.player_turtle = RawTurtle(self.screen, shape="square")
        self.player_turtle.shapesize(stretch_wid=5, stretch_len=0.7)
        self.player_turtle.penup()
        self.player_turtle.speed("fastest")
        self.player_turtle.goto(x=0, y=-670 / 2)
        self.player_turtle.setheading(90)

    def draw_guidelines(self):
        self.guideline_turtle = RawTurtle(self.screen, shape="turtle")
        self.guideline_turtle.hideturtle()
        self.guideline_turtle.pensize(width=20)
        self.guideline_turtle.color("black")
        self.guideline_turtle.speed("fastest")
        self.guideline_turtle.penup()
        self.guideline_turtle.goto(x=795 / 2, y=-695 / 2)
        self.guideline_turtle.pendown()
        self.guideline_turtle.goto(x=795 / 2, y=695 / 2)
        self.guideline_turtle.goto(x=-795 / 2, y=695 / 2)
        self.guideline_turtle.goto(x=-795 / 2, y=-695 / 2)
        self.guideline_turtle.penup()

    def motion(self, event):
        if 750 > round(event.x) > 50:
            self.player_cord = -(799 / 2 - round(event.x))

    def move_player(self):
        self.player_turtle.goto(x=self.player_cord, y=-335)

    def bind_mouse(self, gui):
        return gui.bind("<Motion>", self.motion)

    def game(self):
        self.check_breakout()
        self.move()
        self.move_player()
        self.check_reflect()


def ico(gui):
    icon = Image.open('data/1978075.png')
    photo = ImageTk.PhotoImage(icon)
    return gui.wm_iconphoto(False, photo)
