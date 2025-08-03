import pygame
import random
import time


#creating highscorefile
highscore = 0
try:
    open("highscore.txt", "x")
except:
    with open("highscore.txt") as f:
        highscore = f.read()
        if not highscore:
            highscore = 0

#starting stuff
pygame.init()
screen = pygame.display.set_mode((640, 640))

#sprite
sprite = pygame.image.load('sprite.png').convert_alpha()
sprite = pygame.transform.scale(sprite,
                                (sprite.get_width() * 1,
                                sprite.get_height() *1))
#sprite position
x = screen.get_width() / 2
y = screen.get_height() / 2

#stuff
running = True
collision = False

#time stuff
clock = pygame.time.Clock()
delta_time = 0.1
interval = 5  
last_increment_time = time.time()

#text stuff
font = pygame.font.Font(None, size=30)
gameoverfont  = pygame.font.Font(None, size=60)

#player movement
moving_right = False
moving_left = False
moving_up = False
moving_down = False
score = 0

#enemies
enemyCount = 1
enemyPosList = [{"xpos": 0, "ypos": 0}]
enemyUpdatingSpeedList = [{"xpos": 0, "ypos": 0}]

#sounds
bonkSound = pygame.mixer.Sound('hurt.wav')
gameoverSound = pygame.mixer.Sound('GameOver.wav')
gameOverCounter = 0

while running:
    while not collision:
        #updating player position
        screen.fill("black")
        screen.blit(sprite, (x, y))

        #update enemy position
        counter = 0
        while counter < enemyCount:    
            if enemyPosList[counter]["xpos"] <= 33:
                enemyUpdatingSpeedList[counter]["xpos"] = random.randint(10,30)
                #bonkSound.play()
            if enemyPosList[counter]["xpos"] >= screen.get_width() - 33:
                enemyUpdatingSpeedList[counter]["xpos"] = random.randint(10,30) * -1 
                #bonkSound.play()
            if enemyPosList[counter]["ypos"] <= 33:
                enemyUpdatingSpeedList[counter]["ypos"] = random.randint(10,30) 
                #bonkSound.play()
            if enemyPosList[counter]["ypos"] >= screen.get_height() - 33:
                enemyUpdatingSpeedList[counter]["ypos"] = random.randint(10,30) * -1
                #bonkSound.play()

            enemyPosList[counter]["xpos"] += enemyUpdatingSpeedList[counter]["xpos"] * delta_time
            enemyPosList[counter]["ypos"] += enemyUpdatingSpeedList[counter]["ypos"] * delta_time
            
            #player hitbox
            hitbox = pygame.Rect(x, y, sprite.get_width(), sprite.get_height())

            red = pygame.draw.circle(screen, "red", (enemyPosList[counter]["xpos"],enemyPosList[counter]["ypos"]), 33)
            collision = hitbox.colliderect(red)
            #pygame.draw.rect(screen, (255 * collision, 255, 0), red)

            if(not collision):
                score += 1
            
            current_time = time.time()
            if current_time - last_increment_time >= interval:
                enemyCount += 1
                last_increment_time = current_time
                enemyPosList.append({"xpos": 0, "ypos": 0})
                enemyUpdatingSpeedList.append({"xpos": 0, "ypos": 0})

            counter += 1

        #user movement
        if moving_right:
            x += 40 * delta_time
            if x > (screen.get_width() - sprite.get_width()):
                x = 0
        if moving_left:
            x -= 40 * delta_time
            if x < 0:
                x = (screen.get_width() - sprite.get_width())
        if moving_up:
            y -= 40 * delta_time
            if y < 0:
                y = (screen.get_height() - sprite.get_height())
        if moving_down:
            y += 40 * delta_time      
            if y > (screen.get_height() - sprite.get_height()):
                y = 0

        #score text
        scoreText = font.render('Score: {}'.format(score), True, (255,255,255))
        screen.blit(scoreText, (120,10))
        highScoreText = font.render('High-Score: {}'.format(highscore), True, (255,255,255))
        screen.blit(highScoreText, (420,10))

        for event in pygame.event.get():
            #exiting the game
            if event.type == pygame.QUIT:
                running = False
            #key input / user controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                        moving_right = True
                if event.key == pygame.K_a:
                        moving_left = True  
                if event.key == pygame.K_w:
                        moving_up = True
                if event.key == pygame.K_s:
                        moving_down = True                                               
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                        moving_right = False
                if event.key == pygame.K_a:
                        moving_left = False     
                if event.key == pygame.K_w:
                        moving_up = False
                if event.key == pygame.K_s:
                        moving_down = False                                            
        #display update screen
        pygame.display.flip()

        delta_time = clock.tick(60)
        delta_time = max(0.001, min(0.1, delta_time))

    while gameOverCounter < 1:
        gameoverSound.play()
        gameOverCounter += 1

    gameOverText = gameoverfont.render('Game Over!', True, 'Yellow')
    screen.blit(gameOverText, (screen.get_width() / 3, screen.get_height() / 2))

    pygame.display.flip()

    delta_time = clock.tick(60)
    delta_time = max(0.001, min(0.1, delta_time))

    for event in pygame.event.get():
        #exiting the game
        if event.type == pygame.QUIT:
            running = False

if highscore or highscore == 0:
    if int(highscore) < score:
        with open("highscore.txt", "w") as f:
            f.write(str(score))

pygame.quit