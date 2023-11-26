import math
import pygame
import random
import sys

pygame.init()

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ball parameters
BALL_SPEED = 100
BALL_HEIGHT = 30
BALL_WIDTH = 30

# Score needed to win
SCORE_LIMIT = 5

# Paddle parameters
PADDLE_SPEED = (0, 5)
PADDLE_OFFSET = 20
PADDLE_WIDTH = 30
PADDLE_HEIGHT = 150

# Set up window
display = pygame.display.set_mode((800, 600))
window = display.get_rect()

# Title of the window
pygame.display.set_caption("Pong")

# set up time (fps)
fps = pygame.time.Clock()

# Fonts
FONT = pygame.font.Font('freesansbold.ttf', 48)
FONT_GAMEOVER = pygame.font.Font('freesansbold.ttf', 96)


class Paddle:
    """
    A class used to represent the paddle (player-controlled element)
    in the game

    Atrributes
    ----------
    width : int
        Width of the paddle (in the x axis)
    height : int
        Height of the paddle (in the y axis)
    rect: Rect(float, float, float, float)
        Pygame object describing the object as an Rectagle
    color: (int, int, int)
        Color of the paddle given in (r,g,b) format

    Methods
    -------
    move_up((int,int))
        Moves the paddle up
    move_down((int,int))
        Moves the paddle down
    """
    def __init__(self, x, y, width, height, color):
        """
        Constructor for the paddle object

        Parameters
        ----------
            x : int
                X coordinate of the top left most corner of the paddle,
                where paddle is placed
            y : int
                Y coordinate of the top left most corner of the paddle,
                where paddle is placed
            width : int
                Width of the paddle (in the x axis) in pixels
            height : int
                Height of the paddle (in the y axis) in pixels
            color: (int, int, int)
                Color of the paddle in (r,g,b) format [max values of 0-255]
        """
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = color

    def move_up(self, paddle_speed):
        """
        Moves the paddle up

        Parameters
        ----------
            paddle_speed : (int,int)
                Vector of the movement [x,y] in px, should be always positive

        Returns
        -------
        None
        """
        self.rect = self.rect.move(paddle_speed[0], -paddle_speed[1])

    def move_down(self, paddle_speed):
        """
        Moves the paddle down

        Parameters
        ----------
            paddle_speed : (int,int)
                Vector of the movement [x,y] in px, should be always positive

        Returns
        -------
        None
        """
        self.rect = self.rect.move(paddle_speed[0], paddle_speed[1])


class Ball:
    """
    A class used to represent the ball

    Attributes
    ----------
        width : int
            Width of the ball (in the x axis) in pixels
        height : int
            Height of the ball (in the y axis) in pixels
        rect: Rect(float, float, float, float)
            Pygame object describing the object as an Rectagle
        color: (int, int, int)
            Color of the paddle given in (r,g,b) format
        speed: [int, int]
            Vector of the movement [x,y] in pixels

    Methods
    -------
        move()
            Moves the ball along the vector (speed attribute)
        randomize_speed()
            Randomises the speed vector
        bounce_wall()
            Rotates the speed vector by 90 deg, to bounce of the wall
        bounce_paddle(paddle)
            Modifies the speed vector, so the ball bounces of the paddle
    """
    def __init__(self, x, y, width, height, color):
        """
        Parameters
        ----------
            x : int
                X coordinate of the top left most corner of the ball,
                where ball is placed
            y : int
                Y coordinate of the top left most corner of the ball,
                where paddle is placed
            width : int
                Width of the ball (in the x axis) in pixels
            height : int
                Height of the ball (in the y axis) in pixels
            color: (int, int, int)
                Color of the paddle in (r,g,b) format [max values of 0-255]
        """
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = color
        self.speed = [0, 0]

    def move(self):
        """
        Moves the ball along the vector (speed attribute)

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.rect = self.rect.move(self.speed)

    def randomize_speed(self):
        """
        Randomises the speed vector of the ball

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        x_speed = random.randint(math.floor(math.sqrt(BALL_SPEED)/2),
                                 math.floor(math.sqrt(BALL_SPEED)))
        y_speed = math.sqrt(BALL_SPEED - math.pow(x_speed, 2))

        sidex = random.randint(0, 1)
        if (sidex == 0):
            x_speed = -x_speed
        sidey = random.randint(0, 1)
        if (sidey == 0):
            y_speed = -y_speed
        self.speed = [x_speed, y_speed]

    def bounce_wall(self):
        """
        Rotates the speed vector by 90 deg, so the ball bounces of the wall

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.speed[1] = - self.speed[1]

    def bounce_paddle(self, paddle):
        """
        Modifies the speed vector, so the ball bounces away from the paddle

        Parameters
        ----------
        paddle : int, int, (float,float,float,float), (int, int, int)
            The paddle object that it colides with

        Returns
        -------
        None
        """

        if -40 < paddle.rect.centery - self.rect.centery < 40:
            self.speed[0] = - self.speed[0]

        if paddle.rect.centery - self.rect.centery <= -40:
            x_speed = random.randint(math.floor(math.sqrt(BALL_SPEED)/2),
                                     math.floor(math.sqrt(BALL_SPEED)))
            y_speed = math.sqrt(BALL_SPEED - math.pow(x_speed, 2))

            if (paddle.rect.left < window.centerx):
                self.speed = [x_speed, y_speed]
            else:
                self.speed = [-x_speed, y_speed]

        if paddle.rect.centery - self.rect.centery >= 40:
            x_speed = random.randint(math.floor(math.sqrt(BALL_SPEED)/2),
                                     math.floor(math.sqrt(BALL_SPEED)))
            y_speed = math.sqrt(BALL_SPEED - math.pow(x_speed, 2))

            if (paddle.rect.left < window.centerx):
                self.speed = [x_speed, -y_speed]
            else:
                self.speed = [-x_speed, -y_speed]


class Score:
    """
    This class is used to represent the score of a player

    Attributes
    ----------
    value : int
        Value of the score counter
    message : object
        The pygame render of the score textbox
    textbox: Rect(float,float,float,float)
        Pygame representation of the textbox as rectagle object
    id : int
        The number of the player that this score belongs to

    Methods
    -------
        update()
            Ups the score by one and checks for gameover
    """
    def __init__(self, player_id):
        """
        Constructor for the score object

        Parameters
        ----------
        player_id : int
            The number of the player that this score belongs to

        Returns
        -------
        None
        """
        self.value = 0
        self.message = FONT.render(str(self.value), True, WHITE)
        self.textbox = self.message.get_rect()
        self.id = player_id

    def update(self):
        """
        Ups the score by one and checks for gameover

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.value += 1
        self.message = FONT.render(str(self.value), True, WHITE)

        if self.value == SCORE_LIMIT:
            game_over(self.id)


def initialize_game(paddle1, paddle2, ball, score1, score2):
    """
    Puts every element on their starting position, and delays the start

    Parameters
    ----------
    paddle1: Paddle
        Object representing paddle of left side player
    paddle2: Paddle
        Object representing paddle of right side player
    ball: Ball
        Object representing the ball
    score1: Score
        Object representing the score of the left side player
    score2: Score
        Object representing the score of the right side player

    Returns
    -------
    None
    """
    paddle1.rect.midleft = window.midleft
    paddle1.rect.centerx += PADDLE_OFFSET

    paddle2.rect.midright = window.midright
    paddle2.rect.centerx -= PADDLE_OFFSET

    ball.rect.center = window.center
    ball.randomize_speed()

    display.fill(BLACK)
    draw([paddle1, paddle2, ball])

    display.blit(score1.message, score1.textbox)
    display.blit(score2.message, score2.textbox)

    pygame.display.flip()

    pygame.time.delay(2000)


def draw(objects):
    """
    Uses Pygame.draw to draw a list of objects on the screen

    Parameters
    ----------
    objects : [Objects]
        All objects to be drawn must have .rect atrribute and .color attribute

    Returns
    -------
    None
    """

    for object in objects:
        pygame.draw.rect(display, object.color, object.rect)


def handle_movement(paddle1, paddle2):
    """
    Handles getting input from the user and moves the paddles

    Parameters
    ----------
    paddle1: Paddle
        Object representing paddle of the left side player
    paddle2: Paddle
        Object representing paddle of the right side player

    Returns
    -------
    None
    """
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        paddle1.move_up(PADDLE_SPEED)
        if (paddle1.rect.top < window.top):
            paddle1.rect.top = window.top

    if keys[pygame.K_s]:
        paddle1.move_down(PADDLE_SPEED)
        if (paddle1.rect.bottom > window.bottom):
            paddle1.rect.bottom = window.bottom

    if keys[pygame.K_UP]:
        paddle2.move_up(PADDLE_SPEED)
        if (paddle2.rect.top < window.top):
            paddle2.rect.top = window.top

    if keys[pygame.K_DOWN]:
        paddle2.move_down(PADDLE_SPEED)
        if (paddle2.rect.bottom > window.bottom):
            paddle2.rect.bottom = window.bottom


def game_over(id):
    """
    Displays the game over message on the screen and ends the game

    Parameters
    ----------
    id : int
        Number of the player who won the game (1 or 2)

    Returns
    -------
    None
    """
    game_over_message = FONT_GAMEOVER.render("Player " + str(id) +
                                             " won", True, WHITE)
    game_over_textbox = game_over_message.get_rect()

    game_over_textbox.center = window.center
    game_over_textbox.centery = window.centery - 50

    game_over_message2 = FONT_GAMEOVER.render("(space to exit)", True, WHITE)
    game_over_textbox2 = game_over_message2.get_rect()

    game_over_textbox2.center = window.center
    game_over_textbox2.centery = window.centery + 50

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
             or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                sys.exit()

        display.fill(BLACK)
        display.blit(game_over_message, game_over_textbox)
        display.blit(game_over_message2, game_over_textbox2)
        pygame.display.flip()


def main():
    """
    Main function of the game, creates all the elements
    and handles physics and collisions

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # Create paddles and the ball
    paddle1 = Paddle(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
    paddle2 = Paddle(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT, WHITE)
    ball = Ball(0, 0, BALL_WIDTH, BALL_HEIGHT, WHITE)

    # Setup score boxes
    score1 = Score(1)
    score2 = Score(2)

    # Position score boxes
    score1.textbox.centerx = window.centerx/2
    score1.textbox.centery = window.top + 32

    score2.textbox.centerx = window.right * 3/4
    score2.textbox.centery = window.top + 32

    initialize_game(paddle1, paddle2, ball, score1, score2)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        handle_movement(paddle1, paddle2)

        ball.move()

        # collision detection
        if (ball.rect.colliderect(paddle2)):
            ball.bounce_paddle(paddle2)

        if (ball.rect.colliderect(paddle1)):
            ball.bounce_paddle(paddle1)

        if ball.rect.top < window.top or ball.rect.bottom > window.bottom:
            ball.bounce_wall()

        # Couting the points if the ball goes behind the paddles
        # 2 is added to allow the ball to full go out
        # of the screen
        if ball.rect.left > window.right + 2:
            score1.update()
            initialize_game(paddle1, paddle2, ball, score1, score2)

        if ball.rect.right < window.left - 2:
            score2.update()
            initialize_game(paddle1, paddle2, ball, score1, score2)

        # Display all the elements
        display.fill(BLACK)
        display.blit(score1.message, score1.textbox)
        display.blit(score2.message, score2.textbox)
        draw([paddle1, paddle2, ball])

        pygame.display.flip()

        fps.tick(60)


if __name__ == "__main__":
    main()
