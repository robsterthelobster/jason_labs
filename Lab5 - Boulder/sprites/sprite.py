#Robin Chen
#yuncc@uci.edu
#ICS 61
#Discussion 36781

#increased "gravity"
#increased <<< shift left on cat
#added fish to chase
#if cat catches fish >>> heart count plus 1

import pygame, sys

class SimpleSprite(pygame.sprite.Sprite):
  def __init__(self, imagePath, dimension, positions):
    imageSurface = pygame.image.load(imagePath)
    imageSurface.set_colorkey( (0, 0, 0) )
    self.surfaces = []
    for pos in positions:
      rect = pygame.Rect(pos[0], pos[1], dimension[0], dimension[1])
      self.surfaces.append(imageSurface.subsurface(rect))
    self.index = 0
    self.image = self.surfaces[self.index]

  def update(self):
    self.index = self.index + 1
    if self.index == (len(self.surfaces) - 1):
      self.index = 0
    self.image = self.surfaces[self.index]

cat = SimpleSprite('./images/char9.png', (105, 60),
                   [ [0, 70], 
                     [130, 70], 
                     [260, 70], 
                     [390, 70], 
                     [0, 203], 
                     [130, 203]])
fish = SimpleSprite('./images/char1.png', (50, 50),
                    [ [0, 280],
                      [125, 280],
                      [250, 280]])
block = SimpleSprite('./images/blocks1.png', (32, 32), [[206, 36]])

heart = SimpleSprite('./images/heart.png', (20,20), [[0,0]])

pygame.init()
mainClock = pygame.time.Clock()
pygame.key.set_repeat(30, 30)

_display = pygame.display.set_mode( (640, 480) )
pygame.display.set_caption('Cat Sprite')

fishX = 400
catY = 420
catRight = 1
catSpeed = 10# initialize catSpeed here

counter = 3

myfont = pygame.font.SysFont("Comic Sans MS", 15)
label = myfont.render(str(counter), 1, (0, 0, 0))

while True:

  _display.fill( (50, 150, 150) )
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        catY = catY - 50
      elif event.key == pygame.K_RIGHT:
        catRight = catRight + catSpeed
      
  catRight -= 5
  catX = 200 + catRight
  _display.blit(cat.image, (catX, catY))
  if catY < 420: catY = catY + 5

  if(catX + cat.image.get_width() > fishX and catX + cat.image.get_width() < fishX + fish.image.get_width()):
    counter += 1
    fishX = 400
    
  label = myfont.render(str(counter), 1, (0, 0, 0))

  _display.blit(fish.image, (fishX, 420))
  fishX += 10
  if(fishX > _display.get_width()):
    fishX = 400;
  _display.blit(heart.image, (50, 0))
  _display.blit(block.image, (350, 448))
  _display.blit(label, (80, 1))
  
  cat.update()
  fish.update()
  
  pygame.display.flip()
  mainClock.tick(15)
  
