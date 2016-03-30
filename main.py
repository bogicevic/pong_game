# Go to http://www.codeskulptor.org/ to play Pong
# Implementation of classic arcade game Pong
# Use http://www.codeskulptor.org/#user41_4nHJv4iPhG_0.py for convenience

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400

BALL_RADIUS = 20
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [random.randrange(120, 240) / 60,  -  (random.randrange(60, 180) / 60)]

PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_pos = [[HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
paddle2_pos = [[WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if right == True:
        ball_vel = [random.randrange(120, 240) / 60, -  (random.randrange(60, 180) / 60)]
    else:
        ball_vel = [ - (random.randrange(120, 240) / 60), -  (random.randrange(60, 180) / 60)]
    return ball_vel



# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    ball_init(random.randrange(0, 2))
    score1 = 0
    score2 = 0

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel, WIDTH, HEIGHT
 
    # update paddle's vertical position, keep paddle on the screen
    
    if paddle1_pos[0][1] > 0:
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel
    else:
        paddle1_pos[0][1] = 0
        paddle1_pos[1][1] = PAD_HEIGHT
    
    if paddle1_pos[1][1] <= HEIGHT:
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel
    else:
        paddle1_pos[0][1] = HEIGHT - PAD_HEIGHT
        paddle1_pos[1][1] = HEIGHT
    
    if paddle2_pos[0][1] > 0:  
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
    else:
        paddle2_pos[0][1] = 0
        paddle2_pos[1][1] = PAD_HEIGHT
    if paddle2_pos[1][1] < HEIGHT:  
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
    else:
        paddle2_pos[0][1] = HEIGHT - PAD_HEIGHT
        paddle2_pos[1][1] = HEIGHT
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line(paddle1_pos[0], paddle1_pos[1], PAD_WIDTH, "White")
    c.draw_line(paddle2_pos[0], paddle2_pos[1], PAD_WIDTH, "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # collide and reflect off of top wall of canvas
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # collide and reflect off of bottom wall of canvas
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # When the ball touches a gutter, but not the paddle,
    # opposite player scores. Respawn the ball in the center  
    # of the table headed towards the opposite gutter.
    # Adds 10% velocity to ball after each reflection.
    if (ball_pos[1] >= paddle1_pos[0][1]) and (ball_pos[1] <= paddle1_pos[1][1]) and (ball_pos[0] <= PAD_WIDTH + BALL_RADIUS):
        ball_vel[0] = - ball_vel[0] * 1.1
        ball_vel[1] = ball_vel[1] * 1.1        
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH - 1:
        ball_init(True)
        score2 += 1
    if (ball_pos[1] >= paddle2_pos[0][1]) and (ball_pos[1] <= paddle2_pos[1][1]) and (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS):
        ball_vel[0] = - ball_vel[0] * 1.1
        ball_vel[1] = ball_vel[1] * 1.1
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH + 1:
        ball_init(False)
        score1 += 1
            
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    c.draw_text(str(score1), (230, 70), 42, "White")
    c.draw_text(str(score2), (346, 70), 42, "White")


def keydown(key):
    global paddle1_vel, paddle2_vel
    step = 2
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += step
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= step
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += step
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= step
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)


# start frame
init()
frame.start()

