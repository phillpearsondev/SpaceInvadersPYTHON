#Space Invaders
#Python 3.8

#import modules
import os
import random
import turtle
import math
import winsound

#register the shapes
turtle.register_shape("invader.gif")
turtle.register_shape("ship.gif")
turtle.register_shape("bullet.gif")

#setup the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("stars.gif")

#draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#set the score to 0
score = 0

#draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("green")
score_pen.penup()
score_pen.setposition(-290, 270)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

#choose a number of enemies
number_of_enemies = 5
#create an empty list of enemies
enemies = []

#add enemies to the list
for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    #reset enemy position
    x = random.randint(-200, 200)
    y = random.randint(100, 200)
    enemy.setposition(x, y)

enemyspeed = 2

#create players bullet
bullet = turtle.Turtle()
bullet.color("white")
bullet.speed(0)
bullet.shape("bullet.gif")
bullet.penup()
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 20

#define bullet state
#read - ready to fire
#fire - bullet is fireing
bulletstate = "ready"

#create player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("ship.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

#move the player
playerspeed = 15

def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = - 280
    player.setx(x)
    
def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x) 
    
def fire_bullet():
    #declare bulletstate as global
    global bulletstate
    if bulletstate == "ready":
        #play fireing sound
        winsound.PlaySound("laser.wav", winsound.SND_ASYNC|winsound.SND_NOSTOP)
        bulletstate = "fire"
        #move bullet to above player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()
    
def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2)+math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15:
        return True
    else:
        return False
    
#create keyboard binding
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

#main game loop
while True:
    
   #move the bullet
   if bulletstate == "fire":
      y = bullet.ycor()
      y += bulletspeed
      bullet.sety(y)
    
   #check if bullet reached top of screen
   if bullet.ycor() > 275:
      bullet.hideturtle()
      bulletstate = "ready" 
    
   for enemy in enemies:
        #move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)
    
        #move the enemy back and down
        if enemy.xcor() > 280:
           #move all enemies down
           for e in enemies:
               y = e.ycor()
               y -= 40
               e.sety(y)
           #change enemy direction
           enemyspeed *= -1
        
        if enemy.xcor() < -280:
            #move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            #change enemy direction
            enemyspeed *= -1
           
        #check for bullet collision with the enemy
        if isCollision(bullet, enemy):
           #reset bullet
           bullet.hideturtle()
           bulletstate = "ready"
           bullet.setposition(0, -400)
        
           #reset the enemy
           x = random.randint(-200, 200)
           y = random.randint(100, 200)
           enemy.setposition(x, y)
           #play collision sound
           winsound.PlaySound("explosion.wav", winsound.SND_ASYNC|winsound.SND_NOSTOP)
           #update the score
           score += 100
           scorestring = "Score: %s" %score
           score_pen.clear()
           score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

        if isCollision(player, enemy):
           player.hideturtle()
           enemy.hideturtle()
           print ("GAME OVER")
           break