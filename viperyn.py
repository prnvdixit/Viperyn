import pygame
import time
import random

pygame.init()

"""setting up the color scheme for the game """

white = (255,255,255)
red = (255,0,0)
black = (0, 0, 0)
green = (0, 255, 0)

"""setting up the screen size"""
desktopWidth, desktopHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
display_width = 72 * int(desktopWidth/100)
display_height = 95 * int(desktopHeight/100)

"""setting the game-name and display window"""

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Viperyn')

"""loading the necessary images"""

head = pygame.image.load('body_head.png')
body = pygame.image.load('body_mid.png')
apple = pygame.image.load('apple.png')
specialApple = pygame.image.load('specialApple.png')
tail = pygame.image.load('body_tail.png')
back = pygame.image.load("background_dust.png")
death = pygame.image.load("death.png")
death_new = pygame.transform.scale(death,(display_width,display_height))

"""# For FPS, we are going to need clock """
clock = pygame.time.Clock()

def fillBackground() :

    """ The function used to blit the whole background using the background image"""

    for i in xrange(display_width/10 + 1) :
        for j in xrange(display_height/10 + 1) :
            gameDisplay.blit(back, (10 * i, 10 * j))

def showScore(score) :

    """ The function used to print the score on the top-left corner of screen"""

    font = pygame.font.SysFont("comicsansms", 20, True, True)
    screen_text = font.render("Score : " + str(score), True, black)
    gameDisplay.blit(screen_text, [0, 0])


def snake(block_size, snakeBody) :

    """
    Based on the direction in which the snake is moving, this function rotates the
    images corresponding to body, head and tail of snake by appropriate angle and
    then blit them on the game-display.
    """

    if direction == "East" :
        head_new = pygame.transform.rotate(head, 90)
        tail_new = pygame.transform.rotate(tail, 90)

    if direction == "West" :
        head_new = pygame.transform.rotate(head, 270)
        tail_new = pygame.transform.rotate(tail, 270)

    if direction == "North" :
        head_new = pygame.transform.rotate(head, 0)
        tail_new = pygame.transform.rotate(tail, 0)

    if direction == "South" :
        head_new = pygame.transform.rotate(head, 180)
        tail_new = pygame.transform.rotate(tail, 180)


    gameDisplay.blit(tail_new, (snakeBody[0][0], snakeBody[0][1]))
    gameDisplay.blit(head_new, (snakeBody[-1][0], snakeBody[-1][1]))

    for XY in snakeBody[1:-1] :
       #pygame.draw.rect(gameDisplay, green, [XY[0], XY[1], block_size, block_size])
        gameDisplay.blit(body,(XY[0], XY[1]))

def message_to_screen(msg, color, vert_displacement=0, size=25, text_font="None", bold="False", italic="False") :

    """
    Function to print a message (msg) on the game-display of colour (color), at a vertical
    distance (vert_displacement) from the x-axis (mid of the game-display) of letter-size (size) using
    the font (text_font) and boolean bold(T/F) and italic(T/F). Note that the text is always centered
    int the horizontal direction.
    """

    font = pygame.font.SysFont(text_font, size, bold, italic)
    screen_text = font.render(msg, True, color)
    text_position = screen_text.get_rect()
    text_position.center = (display_width/2, display_height/2 + vert_displacement)
    gameDisplay.blit(screen_text, text_position)

def gameLoop(title) :

    while title :

        """
        This is the title window of the game which is run just once at the start of the game,
        to ensure this a bool value "title" is supplied as arguement every time "gameLoop" is
        called, which tells if we need to show the title window (if gameLoop is called for first time)
        or to not show the title window (if the user restarts the game by pressing the "c" after a gameOver)
        """

        fillBackground()

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q :
                    pygame.quit()
                    quit()

                if event.key == pygame.K_c :
                    title = False
                    break

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        message_to_screen("Time to feed the Viper", color=red, vert_displacement=-100, size=30, text_font="arial", bold="True")
        message_to_screen("REMEMBER :", color=red, vert_displacement=-60, size=23, text_font="arial")
        message_to_screen("Don't Run into Walls", color=black, vert_displacement=-20, size=17, text_font="timesnewroman")
        message_to_screen("Don't make my pet Viper, an autocannibalistic", color=black, vert_displacement=10, size=17, text_font="timesnewroman")
        message_to_screen("If you fail, press Q to Quit and C to try again", color=black, vert_displacement=40, size=17, text_font="timesnewroman")
        message_to_screen("Press C to start the game now !", color=black, vert_displacement=70, size=17, text_font="timesnewroman")

        pygame.display.update()
        clock.tick(15)



    """
    setting up the starting direction
    """
    global direction
    direction = "East"

    """
    The gameOver and gameExit loops needs to run only if corresponding boolean value are True
    """

    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    """
    We would have to assign a starting direction to snake's head, let that be East
    """
    lead_x_change = -10
    lead_y_change = 0

    snakeBody = []
    snakeLength = 3

    """
    Initialising the variables needed inside the gameLoop
    """
    block_size = 10
    n = 2
    apple_size = block_size * n
    #reduce = 1
    FPS = 20
    score = 0
    bonus = 0
    scoreChange = 160

    """
    Generating the coordinates of apple in a random manner
    """
    appleX = random.randint(2, display_width//apple_size-2) * apple_size
    appleY = random.randint(2, display_height//apple_size-2) * apple_size

    while not gameExit:

        while gameOver :
            #gameDisplay.fill(black)
            #fillBackground()

            """
            By NOT updating the display, or filling it with the background, it is ensured that if someone
            want to check out his score on dying or just see how beautifully he carried an animal massacre,
            he can do so right away, just to put the background out of focus, the screen would be striped.
            The game is restarted if 'C' is pressed and quitted if 'Q'/'CROSS' is pressed/clicked.
            """

            gameDisplay.blit(death_new, (0, 0))

            message_to_screen("Game Over", color=red, vert_displacement=-20, size=50, text_font="helvetica", bold="True")
            message_to_screen("Press C to continue playing and Q to quit", color=black, vert_displacement=35, size=25, text_font="timesnewroman", italic="True")
            pygame.display.update()

            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q :
                        gameExit = True
                        gameOver = False

                    if event.key == pygame.K_c :
                        gameLoop(False)
                if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False


        for event in pygame.event.get():
            """
            The part of code that controls where the snake would move, the pause functionality
            and provides quitting in middle of game. Mind you!, you can't lose by going opposite
            to the current direction.
            """

            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT or event.key == pygame.K_a :

                    if direction == "West" :
                        break

                    direction = "East"
                    lead_x_change = - block_size
                    lead_y_change = 0

                elif event.key == pygame.K_UP or event.key == pygame.K_w :

                    if direction == "South" :
                        break

                    direction = "North"
                    lead_y_change = - block_size
                    lead_x_change = 0

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s :

                    if direction == "North" :
                        break

                    direction = "South"
                    lead_y_change = + block_size
                    lead_x_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d :

                    if direction == "East" :
                        break

                    direction = "West"
                    lead_x_change = + block_size
                    lead_y_change = 0

                elif event.key == pygame.K_q :
                    gameExit = True

                elif event.key == pygame.K_p :
                    pauseState = True
                    message_to_screen("OOPS!!, viper is tired,let him take some rest", color=red, vert_displacement=-20, size=20, text_font="helvetica",bold="True")
                    message_to_screen("Press C to continue and Q to quit", color=red, vert_displacement=40, size=20, text_font="helvetica", bold="True")

                    while pauseState :
                        pygame.display.update()
                        clock.tick(FPS)

                        for event in pygame.event.get() :
                            if event.type == pygame.KEYDOWN :
                                if event.key == pygame.K_c :
                                    pauseState = False
                                    break

                                elif event.key == pygame.K_q :
                                    pauseState = False
                                    gameExit = True
                                    break


        lead_x = lead_x + lead_x_change
        lead_y = lead_y + lead_y_change

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0 :
            gameOver = True


        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeBody.append(snakeHead)

        if len(snakeBody) > snakeLength :
            del snakeBody[0]

        for pastP in snakeBody[:-1] :
            if lead_x == pastP[0] and lead_y == pastP[1] :
                gameOver = True

        #gameDisplay.fill(black)
        fillBackground()
        showScore(score)

        if bonus :
            message_to_screen("Bonus Apple, feed it to viper to get Bonus", color=red, vert_displacement=-display_height//2 + 50, size=20, text_font="helvetica")
            message_to_screen("Sooner you feed, more you would be rewarded", color=red, vert_displacement=-display_height//2 + 80, size=20, text_font="helvetica")

            if (lead_x >= specialAppleX and lead_x <= specialAppleX + apple_size) or (lead_x + block_size <= specialAppleX + apple_size and lead_x + block_size >= specialAppleX) :
                if (lead_y >= specialAppleY and lead_y <= specialAppleY + apple_size) or (lead_y + block_size <= specialAppleY + apple_size and lead_y + block_size >= specialAppleY) :
                    score += scoreChange
                    bonus = 0
                    scoreChange = 160

        if (lead_x >= appleX and lead_x <= appleX + apple_size) or (lead_x + block_size <= appleX + apple_size and lead_x + block_size >= appleX) :
            if (lead_y >= appleY and lead_y <= appleY + apple_size) or (lead_y + block_size <= appleY + apple_size and lead_y + block_size >= appleY) :
                score += 2

                appleX = random.randint(2, display_width//apple_size - 2) * apple_size
                appleY = random.randint(2, display_height//apple_size - 2) * apple_size

                if snakeLength % 8 == 0 :
                    specialAppleX, specialAppleY = appleX, appleY

                    while specialAppleX == appleX and specialAppleY == appleY :
                        specialAppleX = random.randint(2, display_width//apple_size - 2) * apple_size
                        specialAppleY = random.randint(2, display_height//apple_size - 2) * apple_size

                    bonus = 1

                #apple_size -= reduce
                #if apple_size <= block_size :
                #    reduce = 0
                snakeLength = snakeLength + 1
                FPS = FPS + 0.1

        #pygame.draw.rect(gameDisplay, red, [appleX, appleY, apple_size, apple_size])
        if bonus :
            gameDisplay.blit(specialApple, (specialAppleX, specialAppleY))

            if scoreChange <= 2 :
                scoreChange = 2

            else :
                scoreChange -= 1

        gameDisplay.blit(apple, (appleX, appleY))
        snake(block_size, snakeBody)

        pygame.display.update()

        clock.tick(FPS)

title = True
gameLoop(title)

pygame.quit()
quit()
