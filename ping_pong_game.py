import turtle
import time
import pygame
import threading

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load sound effects (Make sure these .wav files are in your project folder)
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
player_a_name = tl.textinput("Player A", "Enter Player A's Name:") or "Player A"
player_b_name = tl.textinput("Player B", "Enter Player B's Name:") or "Player B"

# Score variables
score_a = 0
score_b = 0
game_running = True
game_paused = False

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
ball.speed(0)
ball.shape("circle")
ball.penup()
ball.goto(0, 0)
ball.dx = 1.5
ball.dy = 1.5

# Pen for score
pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"{player_a_name}: {score_a}  {player_b_name}: {score_b}", align="center", font=("Courier", 22, "normal"))

# Winner display
winner_pen = turtle.Turtle()
winner_pen.hideturtle()
winner_pen.penup()
winner_pen.color("darkred")

# Paddle move functions
def paddle_a_up():
    y = paddle_a.ycor()
    if y < 250:
        paddle_a.sety(y + 20)

def paddle_a_down():
    y = paddle_a.ycor()
    if y > -240:
        paddle_a.sety(y - 20)

def paddle_b_up():
    y = paddle_b.ycor()
    if y < 250:
        paddle_b.sety(y + 20)

def paddle_b_down():
    y = paddle_b.ycor()
    if y > -240:
        paddle_b.sety(y - 20)

def toggle_pause():
    global game_paused
    game_paused = not game_paused

def reset_game():
    global score_a, score_b, ball, game_running, game_paused
    score_a = 0
    score_b = 0
    ball.goto(0, 0)
    ball.dx = 1.5
    ball.dy = 1.5
    game_running = True
    game_paused = False
    pen.clear()
    pen.write(f"{player_a_name}: {score_a}  {player_b_name}: {score_b}", align="center", font=("Courier", 22, "normal"))
    winner_pen.clear()

# Keyboard bindings
tl.listen()
tl.onkeypress(paddle_a_up, "w")
tl.onkeypress(paddle_a_down, "s")
tl.onkeypress(paddle_b_up, "i")
tl.onkeypress(paddle_b_down, "k")
tl.onkeypress(toggle_pause, "p")
tl.onkeypress(reset_game, "r")

# Main game loop in a separate thread
def game_loop():
    global score_a, score_b, game_running, game_paused

    while True:
        if not game_running or game_paused:
            time.sleep(0.05)
            continue

        tl.update()

        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Boundary collisions
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
            wall_hit_sound.play()

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1
            wall_hit_sound.play()

        # Right paddle miss
        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            score_sound.play()
            pen.clear()
            pen.write(f"{player_a_name}: {score_a}  {player_b_name}: {score_b}", align="center", font=("Courier", 22, "normal"))

        # Left paddle miss
        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            score_sound.play()
            pen.clear()
            pen.write(f"{player_a_name}: {score_a}  {player_b_name}: {score_b}", align="center", font=("Courier", 22, "normal"))

        # Paddle collisions
        if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50):
            ball.setx(340)
            ball.dx *= -1
            paddle_hit_sound.play()

        if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50):
            ball.setx(-340)
            ball.dx *= -1
            paddle_hit_sound.play()

        # Speed increase
        if score_a + score_b > 5:
            ball.dx = max(min(ball.dx * 1.001, 4), -4)
            ball.dy = max(min(ball.dy * 1.001, 4), -4)

        # Win condition
        if score_a >= 10:
            winner_pen.goto(0, 0)
            winner_pen.write(f"{player_a_name} Wins!", align="center", font=("Courier", 30, "bold"))
            game_running = False
        elif score_b >= 10:
            winner_pen.goto(0, 0)
            winner_pen.write(f"{player_b_name} Wins!", align="center", font=("Courier", 30, "bold"))
            game_running = False

        time.sleep(0.01)

# Start the game loop in a thread
threading.Thread(target=game_loop).start()

tl.mainloop()
