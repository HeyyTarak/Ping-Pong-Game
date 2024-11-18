import turtle
import time
import pygame

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load sound effects
paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
wall_hit_sound = pygame.mixer.Sound("wall_hit.wav")
score_sound = pygame.mixer.Sound("score_sound.wav")

# Set up the screen
tl = turtle.Screen()
tl.title("Ping Pong Game")
tl.bgcolor("grey")
tl.setup(width=800, height=600)
tl.tracer(0)

# Get player names
player_a_name = tl.textinput("Player A", "Enter Player A's Name:")
player_b_name = tl.textinput("Player B", "Enter Player B's Name:")

# Score variables
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.color("blue")
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.penup()
paddle_a.goto(-350, 0)
paddle_a.shapesize(stretch_wid=5, stretch_len=1)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.color("green")
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.penup()
paddle_b.goto(350, 0)
paddle_b.shapesize(stretch_wid=5, stretch_len=1)

# Ball
ball = turtle.Turtle()
ball.color("red")
ball.speed(2)
ball.shape("circle")
ball.penup()
ball.goto(0, 0)
ball.dx = 1.5
ball.dy = 1.5

# Pen (for scoring)
pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"{player_a_name}: {score_a}  {player_b_name}: {score_b}", align="center", font=("Courier", 22, "normal"))

# Functions to move paddles
def paddle_a_up():
    y = paddle_a.ycor()
    if y < 250:
        y += 20
        paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240:
        y -= 20
        paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    if y < 250:
        y += 20
        paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    if y > -240:
        y -= 20
        paddle_b.sety(y)

# Key bindings
tl.listen()
tl.onkeypress(paddle_a_up, "w")
tl.onkeypress(paddle_a_down, "s")
tl.onkeypress(paddle_b_up, "i")
tl.onkeypress(paddle_b_down, "k")

# Main game loop
while True:
    tl.update()

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Boundary hits
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        wall_hit_sound.play()  # Play wall hit sound

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        wall_hit_sound.play()  # Play wall hit sound

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_a += 1
        score_sound.play()  # Play score sound
        pen.clear()
        pen.write(f"{player_a_name}: {score_a}  {player_b_name}: {score_b}", align="center", font=("Courier", 22, "normal"))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_b += 1
        score_sound.play()  # Play score sound
        pen.clear()
        pen.write(f"{player_a_name}: {score_a}  {player_b_name}: {score_b}", align="center", font=("Courier", 22, "normal"))

    # Paddle hits
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 40 and ball.ycor() > paddle_b.ycor() - 40):
        ball.setx(340)
        ball.dx *= -1
        paddle_hit_sound.play()  # Play paddle hit sound

    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 40 and ball.ycor() > paddle_a.ycor() - 40):
        ball.setx(-340)
        ball.dx *= -1
        paddle_hit_sound.play()  # Play paddle hit sound

    # Gradually increase ball speed
    if score_a + score_b > 5:  # After 5 points combined, increase speed
        ball.dx *= 1.05
        ball.dy *= 1.05

    time.sleep(0.01)
