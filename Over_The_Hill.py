# OVER THE HILL - Created by Brenden Monteleone & Will Torres
# This game is a product of the 1982 game Donkey Kong by Nintendo. While not
# exactly the same, Over the Hill shares basic concepts and gameplay. Some
# functions used are borrowed from Professor Hiller's Starfish Collector game
# (ex. testKeyPressed, testSpriteOverlap).
#
# Please mind the messy(ish) code, but more importantly have fun playing!
###################
#Important info for development

# When creating enemies, update the size, add movement, add a hitbox, & draw
# When creating ladders, update the size, add functionality, add range, & draw
# When creating platforms, update the size, & draw

####################
import random
import pygame
from pygame.locals import *
####################
# Initialization
pygame.display.init()

window=pygame.display.set_mode([720,480])

pygame.display.set_caption("Over The Hill")

fpsClock = pygame.time.Clock()

keysPressed=[]

pygame.mixer.init()

####################
# Important Classes

class Sprite:
    # Create attributes for ALL sprites
    def __init__(self,x,y,imageFile):
        self.x = x
        self.y = y
        self.image = pygame.image.load(imageFile)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rectangle = self.image.get_rect(topleft=(x,y))
        self.visible = True

    # Change the sprite's visibility
    def changeVisibility(self):
        if self.visible == True:
            self.visible = False
        elif self.visible == False:
            self.visible = True

    # Draw Sprites onto screen
    def drawSprite(self):
        if self.visible==True:
            window.blit(self.image,self.rectangle)

# Class for all moveable sprites (Mainly used for inheritance purposes)
class Moveable:
    # Create Attributes for moveable sprites
    def __init__(self):
        self.moving = False
        self.onGround = True
        self.jAnimation = 0
        self.isJumping = False
        self.climbing = False

    # Move a sprite (must be followed by the appropriate update function)
    def moveSprite(self,newX,newY):
        self.x += newX
        self.y += newY

# Player Class
class Player(Sprite,Moveable):
    def __init__(self,x,y,imageFile):
        Sprite.__init__(self,x,y,imageFile)
        Moveable.__init__(self)
        # Atttributes needed for collision
        self.left_side = self.x 
        self.right_side = self.x + self.width 
        self.top_side = self.y 
        self.bottom_side = self.y + self.height + 3
        # Walking & Jumping
        self.walkCount = 0
        self.jumpCount = 5
        self.overlap = False  # Used to test if sprite is interacting with enemy
        self.attacking = False
        self.hasPeck = False  # Determines if the player has the peck ability

        # Determining Directional movement
        self.right = False
        self.left = False

    # Update Player Attributes
    def updatePlayer(self):
        self.x = CHICK.x
        self.y = CHICK.y
        x = self.x
        y = self.y

        self.rectangle = self.image.get_rect(topleft=(x,y))
        self.left_side = self.x 
        self.right_side = self.x + self.width 
        self.top_side = self.y 
        self.bottom_side = self.y + self.height + 3
        
# Platform class
class Platform(Sprite,Moveable):
    def __init__(self,x,y,imageFile):
        Sprite.__init__(self,x,y,imageFile)
        # Atttributes needed for collision
        self.left_side = self.x
        self.right_side = self.x + self.width
        self.top_side = self.y
        self.bottom_side = self.y + self.height

    # Update Platform Attributes (If needed)
    def updatePlatform(self):
        self.x = self.x
        self.y = self.y
        x = self.x
        y = self.y

        self.rectangle = self.image.get_rect(topleft=(x,y))
        self.left_side = self.x
        self.right_side = self.x + self.width
        self.top_side = self.y
        self.bottom_side = self.y + self.height

    # Increase the size of the platforms
    def increasePlatform(self,x,y):
        self.image = pygame.transform.scale(self.image,(x,y))
        # 50x15 is a good size
        # Update attributes accordingly
        self.updatePlatform
        self.width = x
        self.height = y

# Enemy Class
class Enemy(Sprite,Moveable):
    def __init__(self,x,y,imageFile):
        Sprite.__init__(self,x,y,imageFile)
        Moveable.__init__(self)
        self.left_side = self.x - 20
        self.right_side = self.x + self.width - 20
        self.top_side = self.y - 20
        self.bottom_side = self.y + self.height - 20
        self.initialPosition = x
        self.limit = False
        self.direction = ""
        self.pecked = False

    def drawEnemy(self):
        if self.visible == True:
            window.blit(self.image,self.rectangle)

    def updateEnemy(self):
        self.x = self.x
        self.y = self.y
        x = self.x
        y = self.y
        self.rectangle = self.image.get_rect(topleft=(x,y))
        self.left_side = self.x + 17
        self.right_side = self.x + self.width - 12
        self.top_side = self.y + 17
        self.bottom_side = self.y + self.height 

    # Creates movement patterns for enemy sprites
    def setEnemyMovement(self,Range,moveSpeed,Fix_OffScreen_As_String):
        # Fixed Movement
        if Fix_OffScreen_As_String == "Fix":
            # Moves right
            if self.x <= (self.initialPosition + Range) and not self.limit:
                self.moveSprite(moveSpeed,0)
                self.updateEnemy()
                if self.x >= (self.initialPosition + Range):
                    self.direction = "Right"
                    self.limit = True
            # Moves left
            elif self.x >= self.initialPosition and self.limit:
                self.moveSprite(-moveSpeed,0)
                self.updateEnemy()
                if self.x <= self.initialPosition:
                    self.limit = False
                    self.direction = "Left"
            # Update image shown based on direction
            if self.direction == "Left":
                self.image = pygame.transform.flip(self.image,1,0)
                self.direction = ""
            elif self.direction == "Right":
                self.image = pygame.transform.flip(self.image,1,0)
                self.direction = ""
            else:
                pass
        # Offscreen & respawn movement
        elif Fix_OffScreen_As_String == "OffScreen":
            if self.x < -30:
                self.changeVisibility() # False
            elif self.x > 730:
                self.changeVisibility() # False
            else:
                self.moveSprite(moveSpeed,0)
                self.updateEnemy()
            if self.visible == False and self.x >= 730 and not self.pecked:
                self.x = -29
                self.updateEnemy()
                self.drawSprite()
                self.changeVisibility() #True
            elif self.visible == False and self.x <= -30 and not self.pecked:
                self.x = 729
                self.updateEnemy()
                self.drawSprite()
                self.changeVisibility() #True

    #Movement for boss ONLY
    def bossMovement(self):
        if self.x <= (self.initialPosition + 3) and not self.limit:
            self.moveSprite(.1,0)
            self.updateEnemy()
            
            if self.x >= (self.initialPosition + 3):
                self.direction = "Right"
                self.limit = True
            # Moves left
        elif self.x >= self.initialPosition and self.limit:
            self.moveSprite(-.1,0)
            self.updateEnemy()
            if self.x <= self.initialPosition:
                self.limit = False
                self.direction = "Left"

    #Movement for boss snake ONLY
    def bossSpawnedEnemy(self):
        if self.x > 730:
            self.changeVisibility() # False
        else:
            self.moveSprite(3.0,0)
            self.updateEnemy()
        if self.visible == False and self.x >= 730:
            self.x = 132
            self.updateEnemy()
            self.drawSprite()
            self.changeVisibility() #True

    # Changes enemy size and updates everything
    def changeSize(self,x,y):
        self.image = pygame.transform.scale(self.image,(x,y))
        self.x = self.x
        self.y = self.y
        x = self.x
        y = self.y

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rectangle = self.image.get_rect(topleft=(x,y))
        self.left_side = self.x - 10
        self.right_side = self.x + self.width - 10
        self.top_side = self.y - 10
        self.bottom_side = self.y + self.height - 10

####################
# Initialize all the Sprites that will be used
####################
# Player Info
CHICK = Player(0,437,"bird/R1.png")
CHICKL = Player(CHICK.x,CHICK.y,"bird/L1.png")
Peck = Sprite(0,0,"bird/R1.png") # Will be pecking ability sprite
# Player Animation Lists
walkRight = [pygame.image.load("bird/R1.png"),
             pygame.image.load("bird/R2.png"),
             pygame.image.load("bird/R3.png"),
             pygame.image.load("bird/R4.png"),
             pygame.image.load("bird/R5.png"),
             pygame.image.load("bird/R6.png"),
             pygame.image.load("bird/R7.png"),
             pygame.image.load("bird/R8.png")]

walkLeft = [pygame.image.load("bird/L1.png"),
            pygame.image.load("bird/L2.png"),
            pygame.image.load("bird/L3.png"),
            pygame.image.load("bird/L4.png"),
            pygame.image.load("bird/L5.png"),
            pygame.image.load("bird/L6.png"),
            pygame.image.load("bird/L7.png"),
            pygame.image.load("bird/L8.png")] 

jumping = [pygame.image.load("bird/J1.png"),
           pygame.image.load("bird/J2.png"),
           pygame.image.load("bird/J3.png"),
           pygame.image.load("bird/J4.png"),
           pygame.image.load("bird/J5.png")]

jumpingL = [pygame.image.load("bird/JL1.png"),
            pygame.image.load("bird/JL2.png"),
            pygame.image.load("bird/JL3.png"),
            pygame.image.load("bird/JL4.png"),
            pygame.image.load("bird/JL5.png")]

attack = [pygame.image.load("bird/P1.png"),
          pygame.image.load("bird/P2.png")]

attackL = [pygame.image.load("bird/PL1.png"),
           pygame.image.load("bird/PL2.png")]

attackCount = 0
# Keep track of the player's direction (for stationary sprite)
direction = "Right"

####################
# Enemy Info
Boss = Enemy(107,22,"level/hiller.png")
Snk1 = Enemy(150,442,"level/snek.png") # Bottom
Snk2 = Enemy(240,366,"level/snek.png") # 2nd
Snk3 = Enemy(480,366,"level/snek.png") # 2nd
Snk4 = Enemy(350,293,"level/snek.png") # 3rd
Snk5 = Enemy(200,217,"level/snek.png") # 4th
Snk6 = Enemy(132,66,"level/snek.png")  # Top
Snk7 = Enemy(30,141,"level/snek.png")  # 5th

# Change Enemy size, direction & Update
Boss.changeSize(75,75)
Snk1.changeSize(25,30)
Snk2.changeSize(25,30)
Snk3.changeSize(25,30)
Snk4.changeSize(25,30)
Snk5.changeSize(25,30)
Snk6.changeSize(25,30)
Snk7.changeSize(25,30)

Snk2.image = pygame.transform.flip(Snk2.image,1,0) #Flips snake vertically
Snk5.image = pygame.transform.flip(Snk5.image,1,0)

####################
# Game Sprites
MenuBackground = [pygame.image.load("menu/menuback1.png"),
                  pygame.image.load("menu/menuback2.png"),
                  pygame.image.load("menu/menuback3.png"),
                  pygame.image.load("menu/menuback4.png"),
                  pygame.image.load("menu/menuback5.png"),
                  pygame.image.load("menu/menuback6.png"),
                  pygame.image.load("menu/menuback7.png"),
                  pygame.image.load("menu/menuback8.png")]
# Change image sizes
for i in range(0,8):
    MenuBackground[i] = pygame.transform.scale(MenuBackground[i],(720,480))
Levels = Platform(0,0,"level/level.jpeg")
Menu = Platform(155,-70,"menu/title.png")
text1 = pygame.image.load("menu/Menu1.png")
text1 = pygame.transform.scale(text1,(250,25))
text2 = pygame.image.load("menu/startText.png")
text2 = pygame.transform.scale(text2,(250,25))
Instructions = pygame.image.load("menu/instructions.png")
Floor = Platform(-35,469,"level/platform3.png")
Door1 = Sprite(25,62,"level/Door1.png") # Top Door
DoorClose = pygame.image.load("level/Door2.png")
Door2 = Platform(25,437,"level/Door1.png")
Door2.visible = False
DoorBackground = Platform(25,62,"level/background.jpeg")
Lives = pygame.image.load("level/Lives.png")
Lives = pygame.transform.scale(Lives,(50,12))
LifeNum = [pygame.image.load("level/2.png"),
           pygame.image.load("level/1.png"),
           pygame.image.load("level/0.png")]
LifeNum[0] = pygame.transform.scale(LifeNum[0],(13,13))
LifeNum[1] = pygame.transform.scale(LifeNum[1],(13,13))
LifeNum [2] = pygame.transform.scale(LifeNum[2],(13,13))
PeckAbility = Platform(352,110,"level/peckUpgrade.png")
PeckAbility.increasePlatform(20,20)
PeckAbility.updatePlatform()

Lose = Platform(0,0,"lose/Lose1.png")
Lose2 = Platform(0,0,"lose/Lose2.png")
Lose3 = Platform(0,0,"lose/Lose3.png")
Lose4 = Platform(0,0,"lose/Lose4.png")
Lose5 = Platform(0,0,"lose/Lose5.png")
Lose.increasePlatform(720,480)
Lose2.increasePlatform(720,480)
Lose3.increasePlatform(720,480)
Lose4.increasePlatform(720,480)
Lose5.increasePlatform(720,480)

Win = Platform(0,0,"win/win1.png")
Win2 = Platform(0,0,"win/win2.png")
Win3 = Platform(0,0,"win/win3.png")
Win4 = Platform(0,0,"win/win4.png")
Win5 = Platform(0,0,"win/win5.png")
Win6 = Platform(0,0,"win/win6.png")
Win7 = Platform(0,0,"win/win7.png")
Win8 = Platform(0,0,"win/win8.png")
Win9 = Platform(0,0,"win/win9.png")
Win.increasePlatform(720,480)
Win2.increasePlatform(720,480)
Win3.increasePlatform(720,480)
Win4.increasePlatform(720,480)
Win5.increasePlatform(720,480)
Win6.increasePlatform(720,480)
Win7.increasePlatform(720,480)
Win8.increasePlatform(720,480)
Win9.increasePlatform(720,480)
# Platform Sprites
LP1 = Platform(-35,394,"level/platform3.png")
LP2 = Platform(-35,319,"level/platform3.png")
LP3 = Platform(-35,244,"level/platform3.png")
LP4 = Platform(-35,169,"level/platform3.png")
LP5 = Platform(-35,94,"level/platform3.png")
Lad1 = Platform(650,397,"level/ladder.png")
Lad2 = Platform(400,322,"level/ladder.png")
Lad3 = Platform(680,247,"level/ladder.png")
Lad4 = Platform(50,172, "level/ladder.png")
Lad5 = Platform(600,97,"level/ladder.png")
# Increase Platform Sizes
Levels.increasePlatform(720,480)
Floor.increasePlatform(800,15)
DoorBackground.increasePlatform(32,32)
LP1.increasePlatform(800,15)
LP2.increasePlatform(800,15)
LP3.increasePlatform(800,15)
LP4.increasePlatform(800,15)
LP5.increasePlatform(800,15)
Lad1.increasePlatform(30,71)
Lad2.increasePlatform(30,71)
Lad3.increasePlatform(30,71)
Lad4.increasePlatform(30,71)
Lad5.increasePlatform(30,71)
# Update Platforms from size increase

Floor.updatePlatform()
LP1.updatePlatform()
LP2.updatePlatform()
LP3.updatePlatform()
LP4.updatePlatform()
LP5.updatePlatform()
Lad1.updatePlatform()
Lad2.updatePlatform()
Lad3.updatePlatform()
Lad4.updatePlatform()
Lad5.updatePlatform()

####################
# Important Functions
####################

# Draws all enemies & Sets movement
def spawnEnemies():
    Snk6.drawSprite()
    Boss.drawSprite()
    Snk1.drawSprite()
    Snk2.drawSprite()
    Snk3.drawSprite()
    Snk4.drawSprite()
    Snk5.drawSprite()
    Snk7.drawSprite()
    
    Boss.bossMovement()
    Snk1.setEnemyMovement(350,1.5,"Fix")
    Snk2.setEnemyMovement(0,-2.5,"OffScreen")
    Snk3.setEnemyMovement(0,1.5,"OffScreen")
    Snk4.setEnemyMovement(250,1.5,"Fix")
    Snk5.setEnemyMovement(0,-2.5,"OffScreen")
    Snk7.setEnemyMovement(0,3.5,"OffScreen")

# Ladder Functionality Algorithm    
def ladderFunction(Ladder,X_Pos_of_Gnd):
    # Check Sprite Overlap (When at base of ladder)
    if testSpriteOverlap(CHICK,Ladder) and (Ladder.left_side - 4) <= CHICK.left_side and CHICK.right_side <= (Ladder.right_side + 4):
        # Allow player to move up, disabling left/right movement
        if testKeyPressed(K_UP):
            CHICK.climbing = True
            CHICK.onGround = False
            CHICK.moveSprite(0,-5)
            CHICK.updatePlayer()
            CHICKL.updatePlayer()
        else:
            pass
    # Player is on ground if not on ladder
    if not testSpriteOverlap(CHICK,Ladder):
        CHICK.onGround = True
        CHICK.climbing = False
    #  Check if player is at the top of a ladder
    if CHICK.bottom_side == Ladder.top_side and (Ladder.left_side - 4) <= CHICK.left_side and CHICK.right_side <= (Ladder.right_side + 4):
        CHICK.climbing = True
    if CHICK.climbing:
        # Allow player to move down a ladder
        if testKeyPressed(K_DOWN):
            CHICK.onGround = False
            CHICK.moveSprite(0,5)
            CHICK.updatePlayer()
            CHICKL.updatePlayer()
            # Stops player once ground of platform is reached
            if CHICK.y == X_Pos_of_Gnd:
                CHICK.climbing = False
                CHICK.onGround = True
        else:
            pass

# Contains information for all ladders
def level_1_ladders():
    # Ladder Functionality - make sure chick is between ladders
    if 645<=CHICK.x<=655:
        ladderFunction(Lad1,437)
    elif 397<=CHICK.x<=403:
        ladderFunction(Lad2,362)
    elif 677<=CHICK.x<=683:
        ladderFunction(Lad3,287)
    elif 45<=CHICK.x<=56:
        ladderFunction(Lad4,212)
    elif 595<=CHICK.x<=605:
        ladderFunction(Lad5,137)

# Contains all information for player movement (L,R,Jump,Peck)       
def playerMovement():
    global direction, attackCount

    if CHICK.walkCount == 7:
        CHICK.walkCount = 0

    level_1_ladders()
    
    # Update directional attributes based on keys pressed
    if testKeyPressed(K_RIGHT) and CHICK.onGround: #Chick not on ladder
        CHICK.moving = True
        CHICK.right = True
        CHICK.left = False
        direction = "Right"
    elif testKeyPressed (K_LEFT) and CHICK.onGround:
        CHICK.moving = True
        CHICK.right = False
        CHICK.left = True
        direction = "Left"
    else:
        CHICK.moving = False
        CHICK.right = False
        CHICK.left = False
        CHICK.walkCount = 0
        # Draw Stationary Sprite
        if direction == "Right":
            CHICK.drawSprite()
        elif direction == "Left":
            CHICKL.drawSprite()

    if CHICK.moving == True:
        if CHICK.right:
            # Create an x bound (Right side)
            if CHICK.x < 688:
                CHICK.moveSprite(4,0)
                CHICKL.moveSprite(4,0)
                CHICK.updatePlayer()
                CHICKL.updatePlayer()
                CHICK.walkCount += 1
                if CHICK.isJumping == False:
                    window.blit(walkRight[CHICK.walkCount], (CHICK.x, CHICK.y))
            else:
                window.blit(walkRight[CHICK.walkCount], (CHICK.x, CHICK.y))
        elif CHICK.left:
            # Create an x bound (Left side)
            if CHICK.x > 0 and CHICK.y > 62:
                CHICK.moveSprite(-4,0)
                CHICKL.moveSprite(-4,0)
                CHICK.updatePlayer()
                CHICKL.updatePlayer()
                CHICK.walkCount += 1
                if CHICK.isJumping == False:
                    window.blit(walkLeft[CHICK.walkCount], (CHICK.x,CHICK.y))
            # Create a wall on the top platform only
            elif CHICK.x > 172 and CHICK.y <= 62:
                CHICK.moveSprite(-4,0)
                CHICKL.moveSprite(-4,0)
                CHICK.updatePlayer()
                CHICKL.updatePlayer()
                CHICK.walkCount += 1
                if CHICK.isJumping == False:
                    window.blit(walkLeft[CHICK.walkCount], (CHICK.x,CHICK.y))
            else:
                window.blit(walkLeft[CHICK.walkCount], (CHICK.x,CHICK.y))
            
            
    # Check if player is jumping
    if (CHICK.isJumping == False) and CHICK.onGround:
        if testKeyPressed(K_SPACE):
            CHICK.isJumping = True
    elif CHICK.isJumping == True and CHICK.onGround:
        CHICK.visible = False
        CHICKL.visible = False
        if CHICK.jumpCount >= -5:
            CHICK.jAnimation += 1
            if CHICK.jAnimation == 5:
                CHICK.jAnimation = 0
            if CHICK.jumpCount > 0:
                CHICK.y -= (CHICK.jumpCount**2) * 0.5
                CHICK.jumpCount -= 1
                CHICK.updatePlayer()
                CHICKL.updatePlayer()
                if direction == "Right":
                    window.blit(jumping[CHICK.jAnimation], (CHICK.x,CHICK.y))
                elif direction == "Left":
                    window.blit(jumpingL[CHICK.jAnimation], (CHICK.x,CHICK.y))
            elif CHICK.jumpCount <= 0:
                CHICK.y += (CHICK.jumpCount**2) * 0.5
                CHICK.jumpCount -= 1
                CHICK.updatePlayer()
                CHICKL.updatePlayer()
                if direction == "Right":
                    window.blit(jumping[CHICK.jAnimation], (CHICK.x,CHICK.y))
                elif direction == "Left":
                    window.blit(jumpingL[CHICK.jAnimation], (CHICK.x,CHICK.y))
        else:
            # Reset variables when jumping is complete
            CHICK.isJumping = False
            CHICK.onGround = True
            CHICK.jumpCount = 5
            CHICK.visible  = True
            CHICKL.visible = True
            
    # Pecking
    if (testKeyPressed(303) or testKeyPressed(304)) and CHICK.onGround and not CHICK.moving and CHICK.hasPeck:
        CHICK.attacking = True  #Enable Attacking
        CHICK.onGround = False  #Prevents moving
        CHICK.visible = False
        CHICKL.visible = False
        attackCount = 0
        
    if CHICK.attacking == True:
        if direction == "Right":
            if attackCount < 1:
                window.blit(attack[0],(CHICK.x,CHICK.y))
                attackCount += .4
            elif attackCount < 2:
                window.blit(attack[1],(CHICK.x,CHICK.y))
                attackCount += .4
            elif attackCount < 3:
                window.blit(attack[0],(CHICK.x,CHICK.y))
                attackCount += .4
            else:
                attackCount += .4
        elif direction == "Left":
            if attackCount < 1:
                window.blit(attackL[0],(CHICK.x,CHICK.y))
                attackCount += .4
            elif attackCount < 2:
                window.blit(attackL[1],(CHICK.x,CHICK.y))
                attackCount += .4
            elif attackCount < 3:
                window.blit(attackL[0],(CHICK.x,CHICK.y))
                attackCount += .4
            else:
                attackCount += .4
            
        if attackCount > 3:
            CHICK.visible = True
            CHICKL.visible = True
            attackCount = 0
            CHICK.attacking = False
            CHICK.onGround = True
            
def testSpriteOverlap(sprite1,sprite2):
    noOverlap = (sprite1.right_side <= sprite2.left_side) or (sprite2.right_side <= sprite1.left_side) or (sprite1.bottom_side <= sprite2.top_side) or (sprite2.bottom_side <= sprite1.top_side)
    return (not noOverlap)

def testKeyPressed(key):
    return key in keysPressed

# Draw Level onto board
def drawAllSprites():
    Levels.drawSprite()
    PeckAbility.drawSprite()
    Door2.drawSprite()
    if Door2.visible == False:
        window.blit(DoorClose,(Door2.x,Door2.y))
    Floor.drawSprite()
    Door1.drawSprite()
    if Door1.visible == False:
        window.blit(DoorClose,(Door1.x,Door1.y))
    LP1.drawSprite()
    LP2.drawSprite()
    LP3.drawSprite()
    LP4.drawSprite()
    LP5.drawSprite()
    Lad1.drawSprite()
    Lad2.drawSprite()
    Lad3.drawSprite()
    Lad4.drawSprite()
    Lad5.drawSprite()

# Draws the main menu of the game
menuCount = 0
def drawMainMenu():
    global menuCount
    if menuCount > 16:
        menuCount = 0
    if menuCount < 2:
        window.blit(MenuBackground[0],(0,0))
        menuCount += .4
    elif menuCount < 4:
        window.blit(MenuBackground[1],(0,0))
        menuCount += .4
    elif menuCount < 6:
        window.blit(MenuBackground[2],(0,0))
        menuCount += .4
    elif menuCount < 8:
        window.blit(MenuBackground[3],(0,0))
        menuCount += .4
    elif menuCount < 10:
        window.blit(MenuBackground[4],(0,0))
        menuCount += .4
    elif menuCount < 12:
        window.blit(MenuBackground[5],(0,0))
        menuCount += .4
    elif menuCount < 14:
        window.blit(MenuBackground[6],(0,0))
        menuCount += .4
    elif menuCount < 16:
        window.blit(MenuBackground[7],(0,0))
        menuCount += .4
    
    # Moves title for a cool effect
    if Menu.y != 0:
        Menu.moveSprite(0,1)
        Menu.updatePlatform()
    Menu.drawSprite()
    if Menu.y == 0 and canPressKey:
        window.blit(text1,(20,450))
        window.blit(text2,(360,450))

# Determines if enemy hits the player
def hit(Enemy_Sprite):
    if testSpriteOverlap(CHICK,Enemy_Sprite) and Enemy_Sprite.visible == True:
        if CHICK.overlap == False:
            CHICK.overlap = True

# Determines if player hits the Boss            
bossCount = 0
Bosshit = False
def hitBoss():
    global bossCount,Bosshit
    if testSpriteOverlap(CHICK,Boss) and Boss.visible == True and CHICK.attacking:
        Bosshit = True
    if Bosshit == True:
        bossCount+=1
        Bosshit = False
    if bossCount == 100: # Change for difficulty
        Boss.visible = False
        Bosshit = False #Restarts for future games
        bossCount = 0

# Determines if Player pecks an enemy
def pecked(Enemy_Sprite):
    global AttackList
    if testSpriteOverlap(CHICK,Enemy_Sprite) and CHICK.attacking:
        Enemy_Sprite.visible = False
        Enemy_Sprite.pecked = True
        AttackList += [Enemy_Sprite]

# Restarts variables for a new game
def Restart():
    global AttackList
    CHICK.onGround = False  #Stops player from moving
    CHICK.jumpCount = -10   #Force player out of jump
    CHICK.x = 0         # Restart Positions
    CHICK.y = 437
    CHICK.updatePlayer()    #Update player
    CHICKL.updatePlayer()
    CHICK.hasPeck = False
    PeckAbility.visible = True
    Door1.visible = True
    Door2.visible = False
    Snk6.x = 132
    Snk6.visible = True
    Snk6.updateEnemy()
    Boss.visible = True
    Bosshit = False
    bossCount = 0
    CHICK.overlap = False   #Restart overlap
    for enemy in AttackList:    #Reset enemies
        enemy.visible = True
        enemy.pecked = False
    AttackList = []
        
####################
# Level Building Functions

def mainMenu():
    drawMainMenu()

def Level1():
    global levelCount, direction

    if Boss.visible == False:
        Snk6.visible = False
        Door1.visible = False
        Door2.visible = True
        
    drawAllSprites()
    playerMovement()
    spawnEnemies()

    if CHICK.y <= 62.0 and Boss.visible == True:
        Snk6.bossSpawnedEnemy()
    
#####################
# Game Loop
gameRunning=True
# Set this to 1 to skip main menu
levelCount=0
timer = 0
lives = 3
LoseCount = 0
numCount = 0
AttackList = []
winCount = 0

# Ensures that the user can only press 'start' once
canPressKey = True
while gameRunning==True:

    #First we need statements regarding our user input
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            gameRunning = False
        if event.type == pygame.KEYDOWN:
            keysPressed.append(event.key)
        if event.type == pygame.KEYUP:
            keysPressed.remove(event.key)
   
    #then we update our game data
    if levelCount==0:
        winCount = 0
        mainMenu()
        lives = 3
        LoseCount = 0
        numCount = 0
        
        if testKeyPressed(105):
            canPressKey = False
            window.blit(Instructions,(0,0))
        else:
            canPressKey = True
            
        if testKeyPressed(K_SPACE) and canPressKey==True:
            # Algorithm for starting game after music stops found at
            # https://nerdparadise.com/programming/pygame/part3
            # Basically, it creates a new event that executes once the
            # music has stopped playing, so we check for that event
            SONG_END = pygame.USEREVENT + 1
            # Play start theme
            pygame.mixer.music.set_endevent(SONG_END)
            pygame.mixer.music.load('audio/Start.mp3')
            pygame.mixer.music.play(0)
            canPressKey=False
            while timer != 1:
                for event in pygame.event.get():
                    if event.type == SONG_END:
                        timer = 1
                        levelCount+=1
                        lives = 3
                        CHICK.onGround = True   #Restart Player
            timer = 0
            keysPressed = []
            
    elif levelCount==1:
        if timer == 0:
            pygame.mixer.music.load('audio/Level1.mp3')
            pygame.mixer.music.play(-1)
            timer += 1
            
        Level1()
        window.blit(Lives,(640,0))
        window.blit(LifeNum[numCount],(690,0))
        
        # Check for Sprite attack
        pecked(Snk1)
        pecked(Snk2)
        pecked(Snk3)
        pecked(Snk4)
        pecked(Snk5)
        pecked(Snk6)
        pecked(Snk7)
        hitBoss()
        # Test Enemy Overlap

        hit(Snk1)
        hit(Snk2)
        hit(Snk3)
        hit(Snk4)
        hit(Snk5)
        hit(Snk6)
        hit(Snk7)

        #Peck Ability Gain Condition
        if testSpriteOverlap(CHICK,PeckAbility):
            CHICK.hasPeck = True
            PeckAbility.visible = False

        #Enemy Hits Player Condition   
        if CHICK.overlap == True:
            Restart()
            lives -= 1              # Take away a life
            numCount += 1
            if numCount == 3:
                numCount = 2
            CHICK.onGround = True   #Allow player to move
            
        # Used for building platforms
        if testKeyPressed(120):
            print(CHICK.x)
        elif testKeyPressed(121):
            print(CHICK.y)
          
    # Lose Condition       
    if lives == 0:
        CHICK.onGround = False
        Menu.y = -70        #Restart Menu
        if timer == 1:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("audio/lose.mp3")
            pygame.mixer.music.play()
            timer += 1
        if LoseCount < 1:
            Lose.drawSprite()
            LoseCount += .1
        elif LoseCount < 2:
            Lose2.drawSprite()
            LoseCount += .1
        elif LoseCount < 3:
            Lose3.drawSprite()
            LoseCount += .1
        elif LoseCount < 10:
            Lose4.drawSprite()
            LoseCount += .1
        elif LoseCount > 10.5:
            Lose5.drawSprite()
            levelCount = 0
        elif LoseCount > 10:
            Lose5.drawSprite()
            LoseCount += .1
            
    # Win Condition
    if testSpriteOverlap(CHICK,Door2):
        if testKeyPressed(K_UP) and Door2.visible:
            CHICK.onGround = False
            Menuy = -70
            pygame.mixer.music.stop()
            levelCount = 100
            
    if levelCount==100:
        if timer == 1:
            pygame.mixer.music.stop()
            timer += 1
        if winCount > 14:
            pygame.mixer.music.stop()
            levelCount = 0
            Restart()
            Menu.y = -70
        if winCount < 1:
            Win.drawSprite()
            winCount += .1
        elif winCount < 2:
            Win2.drawSprite()
            winCount += .1
        elif winCount < 3:
            Win3.drawSprite()
            winCount += .1
        elif winCount < 4:
            Win4.drawSprite()
            winCount += .1
        elif winCount < 5:
            Win5.drawSprite()
            winCount += .1
        elif winCount < 6:
            Win6.drawSprite()
            winCount += .1
        elif winCount < 7:
            Win7.drawSprite()
            winCount += .1
        elif winCount < 10:
            Win8.drawSprite()
            winCount += .1
        elif winCount < 14:
            Win9.drawSprite()
            winCount += .1
            if winCount == 12.199999999999973:
                Win9.drawSprite()
                pygame.mixer.music.load("win/win.mp3")
                pygame.mixer.music.play()
          
    # we translate our data into images
    pygame.display.update()
    # pause program for enough time
    fpsClock.tick(30)
    
pygame.quit()
