import pygame
import math3d
import random
import math

class obj_Physics(object):
	def __init__(self, x, y, vX, vY):
		self.mPos = math3d.VectorN((x, y))
		self.mVel = math3d.VectorN((vX, vY))
		
	def printPos(self):
		print(self.mPos)
		
	def printVel(self):
		print(self.mVel)
		
	def printAll(self):
		self.printPos()
		self.printVel()
		
	def accel(self, a, dt):
		self.mVel += math3d.VectorN((a*dt,0))
		
	def update(self, dt):
		self.mPos += self.mVel * dt

class cannonBall(obj_Physics):
	def __init__(self, x, y, vX, vY):
		super().__init__(x, y, vX, vY)
		self.img = pygame.image.load("images/coconut.png").convert()
		
	def render(self, dt):
		screen.blit(self.img, self.mPos.iTuple())

	def destroy(self):
		print("Destroy!")
		pass
		
	def update(self, dt):
		super().update(dt)
		d = 50
		if self.mPos[0] < -d or self.mPos[0] > (width+d) or self.mPos[1] < -d or self.mPos[1] > (height+d):
			self.destroy()
			
class cannon(obj_Physics):

	projectiles = []

	def __init__(self, x, y, vX, vY):
		super().__init__(x, y, vX, vY)
		self.img = pygame.image.load("images/cannon.png")
		self.friction = math3d.VectorN((.1,0))
		self.accelSpd = .01
	
	def update(self, dt):
		super().update(dt)
		self.applyFriction()
		
		eList = pygame.event.get()
		for e in eList:
			if e.type == pygame.mouse.get_pressed():
				shoot()
		
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT] and self.mPos[0] < width:
			self.accel(self.accelSpd,dt)
			
		if keys[pygame.K_LEFT] and self.mPos[0] > 0:
			self.accel(-self.accelSpd,dt)

		if keys[pygame.K_SPACE]:
			pass
			#shoot()
			
	def applyFriction(self):
		if self.mVel[0] > 0:
			self.mVel -= self.friction
			if self.mVel[0] < 0:
				self.mVel[0] = 0
		elif self.mVel[0] < 0:
			self.mVel += self.friction
			if self.mVel[0] > 0:
				self.mVel[0] = 0
	
	def render(self,dt):
		screen.blit(self.img, self.mPos.iTuple())
		
	#def shoot(self):
	#	tmpV = self.mPos + 
	#	projectiles.append(cannonBall(
		
class barrel(cannon):
	def __init__(self, x, y, Vx, Vy):
		super().__init__(x,y,Vx,Vy)
		self.offset = math3d.VectorN((0,0))
		self.img = pygame.image.load("images/barrell.png")
		self.angle = 0

	def update(self,dt):
		super().update(dt)
		pygame.transform.rotate(self.img,self.getAngle())
	
	def render(self,dt):
		print(self.getAngle())
		screen.blit(self.img, self.mPos.iTuple())

	def getMousePos(self):
		return pygame.mouse.get_pos()             #Returns in a tuple
		
	def getAngle(self):
		mouseV = math3d.VectorN(self.getMousePos())
		newV = mouseV - self.mPos
		angle = math.atan2(newV.mData[0], newV.mData[1])
		angle = angle * (180/math.pi)
		#if angle > 45:
		#	angle = 45
		#elif angle < 0:
		#	angle = 0
		return angle

#====================Game==================

pygame.display.init()

size = width, height = 800,600
clock = pygame.time.Clock()
done = False

screen = pygame.display.set_mode(size)

objects = []
objects.append(barrel(400,300,0,0))
objects.append(cannon(400,300,0,0))

while not done:
	#Update
	dt = clock.tick(60) #This is in milliseconds
	for obj in objects:
		obj.update(dt)
	
	#Inputs
	eList = pygame.event.get()
	for e in eList:
		if e.type == pygame.QUIT:
			done = True
		
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		done = True
		
	#Draw
	bgColor = 0, 0, 0
	screen.fill(bgColor)
	for obj in objects:
		obj.render(dt)
		
	pygame.display.flip()
	
pygame.display.quit()
	