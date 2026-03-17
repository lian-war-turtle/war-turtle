import turtle
import random
import winsound
import threading

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("War Turtle")

player = turtle.Turtle()
player.color("white")
player.shape("turtle")
player.speed(0)
player.hideturtle()

score = 0
lives = 3
game_started = False
game_over = False
bullet_active = False
boss_active = False
boss_health = 10
boss_kills = 0
game_mode = "normal"

score_display = turtle.Turtle()
score_display.color("white")
score_display.hideturtle()
score_display.penup()
score_display.goto(-280, 260)

lives_display = turtle.Turtle()
lives_display.color("red")
lives_display.hideturtle()
lives_display.penup()
lives_display.goto(180, 260)

boss_display = turtle.Turtle()
boss_display.color("orange")
boss_display.hideturtle()
boss_display.penup()
boss_display.goto(-30, 260)

title_screen = turtle.Turtle()
title_screen.color("yellow")
title_screen.hideturtle()
title_screen.penup()

def draw_title():
    title_screen.clear()
    title_screen.goto(0, 130)
    title_screen.color("yellow")
    title_screen.write("WAR TURTLE", align="center", font=("Arial", 48, "bold"))
    title_screen.goto(0, 70)
    title_screen.color("white")
    title_screen.write("Arrow keys to move  |  WASD to shoot", align="center", font=("Arial", 14, "normal"))
    title_screen.goto(0, 20)
    title_screen.color("lime green")
    title_screen.write("Press E for EASY", align="center", font=("Arial", 22, "bold"))
    title_screen.goto(0, -10)
    title_screen.color("white")
    title_screen.write("5 lives  |  slow enemies  |  mouse shooting", align="center", font=("Arial", 13, "normal"))
    title_screen.goto(0, -50)
    title_screen.color("orange")
    title_screen.write("Press N for NORMAL", align="center", font=("Arial", 22, "bold"))
    title_screen.goto(0, -80)
    title_screen.color("white")
    title_screen.write("3 lives  |  normal enemies  |  WASD shooting", align="center", font=("Arial", 13, "normal"))
    title_screen.goto(0, -120)
    title_screen.color("red")
    title_screen.write("Press H for HARD", align="center", font=("Arial", 22, "bold"))
    title_screen.goto(0, -150)
    title_screen.color("white")
    title_screen.write("1 life  |  fast enemies  |  boss at 25 kills!!", align="center", font=("Arial", 13, "normal"))

draw_title()

def play_sound(freq, duration):
    threading.Thread(target=lambda: winsound.Beep(freq, duration), daemon=True).start()

def safe_spawn():
    while True:
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        if abs(x - player.xcor()) > 80 or abs(y - player.ycor()) > 80:
            return x, y

enemies = []
for i in range(3):
    e = turtle.Turtle()
    e.color("red")
    e.shape("circle")
    e.speed(0)
    e.hideturtle()
    x, y = safe_spawn()
    e.goto(x, y)
    enemies.append(e)

boss = turtle.Turtle()
boss.color("orange")
boss.shape("circle")
boss.speed(0)
boss.hideturtle()
boss.penup()
boss.turtlesize(3)

bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("circle")
bullet.speed(0)
bullet.hideturtle()
bullet.penup()

overlay = turtle.Turtle()
overlay.hideturtle()
overlay.penup()

def update_displays():
    score_display.clear()
    score_display.write("Score: " + str(score), font=("Arial", 16, "normal"))
    lives_display.clear()
    lives_display.write("Lives: " + str(lives), font=("Arial", 16, "normal"))
    if boss_active:
        boss_display.clear()
        boss_display.write("BOSS HP: " + str(boss_health), font=("Arial", 16, "bold"))

def add_enemy():
    e = turtle.Turtle()
    e.color("red")
    e.shape("circle")
    e.speed(0)
    x, y = safe_spawn()
    e.goto(x, y)
    enemies.append(e)

def spawn_boss():
    global boss_active, boss_health
    boss_health = 10 + (boss_kills * 5)
    boss_active = True
    x, y = safe_spawn()
    boss.goto(x, y)
    boss.showturtle()
    boss_display.clear()
    boss_display.write("BOSS HP: " + str(boss_health), font=("Arial", 16, "bold"))
    play_sound(300, 400)

def show_game_over():
    play_sound(150, 800)
    overlay.goto(0, 40)
    overlay.color("red")
    overlay.write("GAME OVER!", align="center", font=("Arial", 36, "bold"))
    overlay.goto(0, -10)
    overlay.color("white")
    overlay.write("Score: " + str(score), align="center", font=("Arial", 24, "normal"))
    overlay.goto(0, -50)
    overlay.write("Press R to restart!", align="center", font=("Arial", 18, "normal"))
    overlay.goto(0, -85)
    overlay.color("yellow")
    overlay.write("Press T for Title Screen!", align="center", font=("Arial", 18, "normal"))

def go_to_title():
    global score, game_over, bullet_active, lives, boss_active, boss_health, boss_kills, game_started
    if not game_over:
        return
    score = 0
    boss_kills = 0
    lives = 3
    game_over = False
    game_started = False
    bullet_active = False
    boss_active = False
    boss_health = 10
    overlay.clear()
    boss_display.clear()
    score_display.clear()
    lives_display.clear()
    boss.hideturtle()
    player.hideturtle()
    player.goto(0, 0)
    bullet.hideturtle()
    while len(enemies) > 3:
        e = enemies.pop()
        e.hideturtle()
    for e in enemies:
        e.hideturtle()
        x, y = safe_spawn()
        e.goto(x, y)
    draw_title()

def start_game(mode):
    global game_started, game_mode, lives
    game_started = True
    game_mode = mode
    if mode == "easy":
        lives = 5
    elif mode == "normal":
        lives = 3
    else:
        lives = 1
    title_screen.clear()
    player.showturtle()
    for e in enemies:
        e.showturtle()
    update_displays()
    move_enemies()
    move_boss()
    move_bullet()
    play_sound(600, 200)

def start_easy():
    if not game_started:
        start_game("easy")

def start_normal():
    if not game_started:
        start_game("normal")

def start_hard():
    if not game_started:
        start_game("hard")

def restart():
    global score, game_over, bullet_active, lives, boss_active, boss_health, boss_kills
    if not game_over:
        return
    score = 0
    boss_kills = 0
    if game_mode == "easy":
        lives = 5
    elif game_mode == "normal":
        lives = 3
    else:
        lives = 1
    game_over = False
    bullet_active = False
    boss_active = False
    boss_health = 10
    overlay.clear()
    boss_display.clear()
    boss.hideturtle()
    player.goto(0, 0)
    bullet.hideturtle()
    while len(enemies) > 3:
        e = enemies.pop()
        e.hideturtle()
    for e in enemies:
        e.showturtle()
        x, y = safe_spawn()
        e.goto(x, y)
    update_displays()
    move_enemies()
    move_boss()
    move_bullet()
    play_sound(600, 200)

def move_enemies():
    global game_over, lives
    if not game_over and game_started:
        if game_mode == "easy":
            speed = 0.9
        elif game_mode == "normal":
            speed = 3.5
        else:
            speed = 1
        for e in enemies:
            e.setheading(e.towards(player))
            e.forward(speed)
            if e.distance(player) < 20:
                lives -= 1
                update_displays()
                play_sound(200, 200)
                x, y = safe_spawn()
                e.goto(x, y)
                player.goto(0, 0)
                if lives <= 0:
                    game_over = True
                    show_game_over()
                    return
    screen.ontimer(move_enemies, 50)

def move_boss():
    global game_over, lives
    if not game_over and game_started:
        if boss_active:
            boss.setheading(boss.towards(player))
            boss.forward(3)
            if boss.distance(player) < 30:
                lives -= 1
                update_displays()
                play_sound(200, 200)
                player.goto(0, 0)
                if lives <= 0:
                    game_over = True
                    show_game_over()
                    return
    screen.ontimer(move_boss, 50)

def do_shoot(heading):
    global bullet_active
    if not bullet_active and not game_over and game_started:
        bullet_active = True
        bullet.goto(player.xcor(), player.ycor())
        bullet.setheading(heading)
        bullet.showturtle()
        play_sound(500, 50)

def shoot_up():
    do_shoot(90)

def shoot_down():
    do_shoot(270)

def shoot_left():
    do_shoot(180)

def shoot_right():
    do_shoot(0)

def shoot_mouse(x, y):
    global bullet_active
    if game_mode == "easy" and not bullet_active and not game_over and game_started:
        bullet_active = True
        bullet.goto(player.xcor(), player.ycor())
        bullet.setheading(bullet.towards(x, y))
        bullet.showturtle()
        play_sound(500, 50)
        move_bullet()

def move_bullet():
    global bullet_active, score, boss_active, boss_health, boss_kills
    if bullet_active:
        bullet.forward(10)
        for e in enemies:
            if bullet.distance(e) < 20:
                bullet.hideturtle()
                bullet_active = False
                x, y = safe_spawn()
                e.goto(x, y)
                score += 1
                update_displays()
                play_sound(800, 100)
                if score % 5 == 0 and len(enemies) < 10:
                 add_enemy()
                boss_threshold = 25 if game_mode == "hard" else 50
                if score % boss_threshold == 0:
                    spawn_boss()
        if boss_active and bullet.distance(boss) < 30:
            bullet.hideturtle()
            bullet_active = False
            boss_health -= 1
            play_sound(1000, 150)
            if boss_health <= 0:
                boss_active = False
                boss_kills += 1
                boss.hideturtle()
                boss_display.clear()
                score += 10
                update_displays()
                play_sound(900, 400)
            else:
                update_displays()
        if abs(bullet.xcor()) > 300 or abs(bullet.ycor()) > 300:
            bullet.hideturtle()
            bullet_active = False
    screen.ontimer(move_bullet, 20)

def move_up():
    if not game_over and game_started:
        player.setheading(90)
        player.forward(20)

def move_down():
    if not game_over and game_started:
        player.setheading(270)
        player.forward(20)

def move_left():
    if not game_over and game_started:
        player.setheading(180)
        player.forward(20)

def move_right():
    if not game_over and game_started:
        player.setheading(0)
        player.forward(20)

screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(shoot_up, "w")
screen.onkey(shoot_down, "s")
screen.onkey(shoot_left, "a")
screen.onkey(shoot_right, "d")
screen.onkey(restart, "r")
screen.onkey(go_to_title, "t")
screen.onkey(start_easy, "e")
screen.onkey(start_normal, "n")
screen.onkey(start_hard, "h")
screen.onclick(shoot_mouse)
screen.listen()
screen.mainloop()
