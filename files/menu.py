import pygame
from pygame.locals import *
import button
import random

pygame.init()

#dimensions for screen
screen_width = 1250
screen_height = 650


fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))

#Adds 'Pong' text
pygame.display.set_caption('Pong')

#define font
font = pygame.font.SysFont('Constantia', 30)
title = pygame.font.SysFont('Comic Sans', 100)

#images
one_img = pygame.image.load('one_p.png').convert_alpha()
two_img = pygame.image.load('two_p.png').convert_alpha()
resume_img = pygame.image.load('start_btn.png').convert_alpha()
home_img = pygame.image.load('home.png').convert_alpha()
how_img = pygame.image.load('how.png').convert_alpha()


#gamestate variables
game_start_one = False
game_start_two = False
game_paused = False
how_to = False

#define game variable
game_end = False
live_ball = False
margin = 50
player_score = 0
player2_score = 0
cpu_score = 0
fps = 60
winner = 0

result = ["Winner is Player 1", "Winner is Player 2"]
result2 = ["Winner is cpu", "Winner is Player 1"]

#define colors
bg = (50, 25, 50)
white = (255, 255, 255)

def draw_board():
    """
        Draws the board/screen where everything is displayed on

        Args:
            none

        Returns:
            none

   
        """

    screen.fill(bg)
    pygame.draw.line(screen, white, (0, margin), (screen_width, margin))


def draw_text(text, font, text_color, x, y):
    """
        Draws text based on text, font, color, and position given

        Args:
            text (str): Text to draw
            font (defined font): Font to draw text in
            text_color (tuple): Color to draw text in
            x (int): Represents the x-coordinate
            y (int): Represents the y-coordinate

        Returns:
            none

   
        """

    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


class Paddle():
    def __init__(self, x, y):
        """
        Initizalizes the Paddle class

        Args:
            x (int): Represents the x-coordinate
            y (int): Represents the y-coordinate

        Returns:
            none

   
        """
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 30, 150)
        self.speed = 5

    def move(self):
        """
        Moves paddle position

        Args:
            None

        Returns:
            none

   
        """
        key = pygame.key.get_pressed()

        #When key is pressed and the paddle is within screen paddle moves up or down
        if key[pygame.K_w] and player_paddle.rect.top > margin:
            player_paddle.rect.move_ip(0, -1 * self.speed)
        elif key[pygame.K_s] and player_paddle.rect.bottom < screen_height:
            player_paddle.rect.move_ip(0, self.speed)

        if key[pygame.K_UP] and player2_paddle.rect.top > margin:
            player2_paddle.rect.move_ip(0, -1 * self.speed)
        elif key[pygame.K_DOWN] and player2_paddle.rect.bottom < screen_height:
            player2_paddle.rect.move_ip(0, self.speed)

    def ai(self):
        """
        Follows the ball as the "ai" for cpu paddle

        Args:
            None

        Returns:
            none

   
        """
        #"ai" to move paddle automatically
        #move down
        
        if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed)     
        #move up
        if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed) 

    def draw(self):
        """
        Draws the actual paddle

        Args:
            None

        Returns:
            none

   
        """
        pygame.draw.rect(screen, white, self.rect)

class Ball():
    def __init__(self, x, y):
        """
        Initizalizes the Ball class (same as reset)

        Args:
            x (int): Represents the x-coordinate
            y (int): Represents the y-coordinate

        Returns:
            none

   
        """
        self.reset(x, y)

    def move(self):
        """
        Moves the ball around the screen and changes direction based on collisions

        Args:
            none
        Returns:
            none

   
        """

        #collision detect
        #collision with top margin
        if self.rect.top < margin:
            self.speed_y *= -1
        #collision with bottom margin
        if self.rect.bottom > screen_height:
            self.speed_y *= -1
        
        #collision check with paddles
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(player2_paddle) or self.rect.colliderect(cpu_paddle):
            self.speed_x *= -1
            self.collide_count += 1
            if self.collide_count % 5 == 0 and self.speed_x < 0:
                self.speed_x *= -1
                self.speed_x += 2
                self.speed_x *= -1
            elif self.collide_count % 5 == 0 and self.speed_x > 0:
                self.speed_x += 2
            
            if self.collide_count % 5 == 0 and self.speed_y < 0:
                self.speed_y *= -1
                self.speed_y += 2
                self.speed_y *= -1
            elif self.collide_count % 5 == 0 and self.speed_y > 0:
                self.speed_y += 2
                

        #out of bounds check
        if self.rect.left < 0:
            self.winner = -1
        if self.rect.right > screen_width:
            self.winner = 0
        
        #update ball pos
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.winner

    def draw(self):
        """
        Draws ball onto screen

        Args:
            none

        Returns:
            none

   
        """
        pygame.draw.circle(screen, white, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

    def reset(self, x, y):
        """
        Initizalizes the Button class (used to reset)

        Args:
            x (int): Represents the x-coordinate
            y (int): Represents the y-coordinate

        Returns:
            none

   
        """
        self.x = x
        self.y = y
        self.ball_rad = 10
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4 * random.choice((1,-1))
        self.speed_y = 4 * random.choice((1,-1))
        # 0 = Player 1 or Cpu winner and -1 means Player 2 or Player 1 winner (based on mode)
        self.winner = 1
        self.collide_count = 0


#create paddles
player_paddle = Paddle(20, screen_height // 2)
player2_paddle = Paddle(screen_width - 50, screen_height // 2)
cpu_paddle = Paddle(20, screen_height // 2)

#create pong ball
pong = Ball(screen_width // 2, screen_height // 2)

#buttons
one_button = button.Button(screen_width // 2, (screen_height // 2) - 50, one_img, 1)
two_button = button.Button(screen_width // 2, (screen_height // 2) + 50, two_img, 1)
how_button = button.Button(screen_width // 2, (screen_height // 2) + 150, how_img, 0.75)
resume = button.Button((screen_width // 2) + 100, screen_height // 2, resume_img, 0.25)
home = button.Button((screen_width // 2) - 100, screen_height // 2, home_img, 0.25)
home2 = button.Button(screen_width // 2, 500, home_img, 0.25)

#keeps game running while True (game loop)
run = True
while run:

    fpsClock.tick(fps)

    draw_board()

    #sees if game in paused screen
    if game_paused == True:
        screen.fill(bg)
        draw_text("Game Paused", font, white, screen_width - 715, 200)

        #resume button clicked
        if resume.draw(screen) == True:
            game_paused = False
        
        #home button clicked
        if home.draw(screen) == True:
            game_start_one = False
            game_start_two = False
            game_paused = False
            pong.reset(screen_width // 2, screen_height // 2)

    #sees if in starting menu screen
    if game_start_one == False and game_start_two == False and how_to == False:
        screen.fill(bg)
        draw_text("PONG", title, white, 485, 50)

        #if one_player button clicked
        if one_button.draw(screen) == True:
            game_start_one = True
        
        #if two_player button clicked
        elif two_button.draw(screen) == True:
            game_start_two = True
        
        #if how_to button clicked
        elif how_button.draw(screen) == True:
            how_to = True
    
    #How to button clicked
    elif how_to == True:
        draw_text("Space to start rally", font, white,  500,(screen_height // 2) - 50)
        draw_text("wasd or arrow keys to move", font, white, 500, screen_height // 2)
        draw_text("First to 5 points win", font, white, 500, (screen_height // 2) + 50)

        #If home button clicked
        if home2.draw(screen) == True:
            game_start_one = False
            game_start_two = False
            how_to = False

   #if one_player button clicked
    elif game_start_one == True and game_paused == False:

        #displays scores
        draw_text("Cpu: " + str(cpu_score), font, white, 20, 15)
        draw_text("P1: " + str(player_score), font, white, screen_width - 100, 15)
        draw_text(str(pong.collide_count), font, white, screen_width // 2, 15)

        #draws paddles
        if game_end == False:
            cpu_paddle.draw()
            player2_paddle.draw()

        if live_ball == True:
            #move ball
            winner = pong.move()

            if winner == 1:
                #move paddles
                cpu_paddle.ai()
                player2_paddle.move()
            
                #draw ball
                pong.draw()
            

            #sets scores based on result
            else:
                live_ball = False
                if winner == 0:
                    cpu_score += 1
                elif winner == -1:
                    player_score += 1
                
                if player_score == 5 or cpu_score == 5:
                    game_end = True

        #Sees if 5 points have been reached to display result of match
        if game_end == True:
            draw_text(result2[winner], font, white, screen_width - 710, screen_height // 2)

    #player_two button clicked
    elif game_start_two == True and game_paused == False:
        draw_text("P1: " + str(player_score), font, white, 20, 15)
        draw_text("P2: " + str(player2_score), font, white, screen_width - 100, 15)
        draw_text(str(pong.collide_count), font, white, screen_width // 2, 15)

        cpu_paddle = Paddle(20, screen_height // 2)


        #draw paddles
        if game_end == False:
            player_paddle.draw()
            player2_paddle.draw()


        if live_ball == True:
            #move ball
            winner = pong.move()

            if winner == 1:
                #move paddles
                player_paddle.move()
                player2_paddle.move()
            
                #draw ball
                pong.draw()
            
            else:
                live_ball = False
                if winner == 0:
                    player_score += 1
                elif winner == -1:
                    player2_score += 1
                
                if player_score == 5 or player2_score == 5:
                    game_end = True
        if game_end == True:
            draw_text(result[winner], font, white, screen_width - 710, screen_height // 2)

    
    #Eventhandler that checks what events have occured
    for event in pygame.event.get():

        #Checks if top corner exit button clicked
        if event.type == pygame.QUIT:
            run = False

        #When in player one or two mode and ball is not moving
        if event.type == pygame.KEYDOWN and live_ball == False and game_end == False and (game_start_one == True or game_start_two == True):

            #Space to spawn ball
            if event.key == pygame.K_SPACE:
                live_ball = True
                pong.reset(screen_width // 2, screen_height // 2)
            
            #Escape key to pull up pause menu
            elif event.key == pygame.K_ESCAPE:
               game_paused = True
        
        #Once game has ended
        elif event.type == pygame.KEYDOWN and game_end == True:

            #Resets game if space clicked
            if event.key == pygame.K_SPACE:
                live_ball = True
                game_end = False
                player_score = 0
                player2_score = 0
                winner = 0
                pong.reset(screen_width // 2, screen_height // 2)
        
        #Pull up pause menu
        elif event.type == pygame.KEYDOWN and (game_start_one == True or game_start_two == True):
            if event.key == pygame.K_ESCAPE:
                game_paused = True

    pygame.display.update()

pygame.quit()