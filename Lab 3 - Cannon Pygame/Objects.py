import pygame
import math3d
import Game

class obj_Physics(object):
	def __init__(self, x, y, vX, vY):
		self.mPos = math3d.VectorN((x, y))
		self.mVel = math3d.VectorN((vX, vY))
		
	def update(self, dt):
		self.mPos += self.mVel * dt

class cannonBall(obj_Physics):
	def __init__(self, x, y, vX, vY):
		obj_Physics.__init__(self, x, y, vX, vY)
		self.img = pygame.image.load("images/coconut.png").convert()
		self.rect = self.img.get_rect()
		
	def render(self, dt):
		Game.getScreen().blit(self.img, self.mPos.iTuple())

	def destroy(self):
		pass
		
class cannon(obj_Physics):
	def __init__(self, x, y, vX, vY):
		obj_Physics.__init__(self, x, y, vX, vY)
		self.img = pygame.image.load("images/cannon.png")
		self.rect = self.img.get_rect()
	
	def render(self):
		pass
		
class barrel(object):
	def __init__(self):
		self.img = pygame.image.load("images/barrell.png")
		self.offset = math3d.VectorN((0,0))
		#self.angle = 

	def update(self,dt):
		pass
	
	def render(self,dt):
		pass
		
	def getMousePos(self):
		return pygame.mouse.get_pos()
		
	def getAngle(self):
		pass