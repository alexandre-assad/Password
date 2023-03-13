import random
import math
import pygame


#Initialization
pygame.init()

#Création écran
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load('background.jpg')

#Titre et Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('iconspace.png')
pygame.display.set_icon(icon)

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
testX = 10
testY = 10

def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

over_font = pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text,(200,250))
#Player
playerImg = pygame.image.load('SpritePlayer.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x,y):
    screen.blit(playerImg, (x, y))
    
#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,730))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)
    
def enemy(x,y, i):
    screen.blit(enemyImg[i], (x, y))
    
#Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.4
bullet_state = "ready"


def fire_bullet(x,y):
    global bullet_state, bulletX
    bulletX = x
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))
    
#Colision
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((bulletX-enemyX)**2+(bulletY-enemyY)**2)
    if distance < 27:
        return True
    else:
        return False
def isCollisionPlayer(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((bulletX-enemyX)**2+(bulletY-enemyY)**2)
    if distance < 47:
        return True
    else:
        return False
collisionJ = False
#Game Loop
running = True
while running:
    
    screen.fill((35,35,35))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #Keyboard
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -0.1
        if event.key == pygame.K_RIGHT:
            playerX_change = 0.1
        if bullet_state == "ready":
            if event.key == pygame.K_DOWN:
                fire_bullet(playerX,bulletY)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0
            
    playerX += playerX_change
    
    #Border
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX=736
        
     
     #Enemy
    for i in range(num_of_enemies):
        if isCollisionPlayer(enemyX[i],enemyY[i],playerX,playerY):
            collisionJ = True
        if collisionJ:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] *=-1
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] *=-1
            enemyY[i] += enemyY_change[i]
        if bullet_state == "fire":
            collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
            if collision:
                bulletY= 480
                bullet_state = "ready"
                for y in range (num_of_enemies):
                    if enemyX_change[y] > 0:
                        enemyX_change[y] += 0.02
                    else:
                        enemyX_change[y] -= 0.02
                enemyX[i] = random.randint(0,730)
                enemyY[i] = random.randint(50,150)
                score_value += 100
        enemy(enemyX[i], enemyY[i], i)
        
        
    #Mouvement balles
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    
        
    player(playerX, playerY)
    show_score(testX,testY)
    pygame.display.update()