import pygame
import math3d
import random
import math

class obj_Physics(object):
	def __init__(self, pos, vel):
		self.mPos = math3d.VectorN(pos)
		self.mVel = math3d.VectorN(vel)
		
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
	def __init__(self, pos, vel):
		super().__init__(pos,vel)
		self.img = pygame.image.load("images/coconut.png").convert()
		self.gravity = math3d.VectorN((0,.01))
		self.rotation = 0
	
	def update(self, dt):
		super().update(dt)
		self.rotation += 5
		self.mVel += self.gravity
	
	def render(self, dt):
		tmp = pygame.transform.rotate(self.img, self.rotation)
		screen.blit(tmp, self.mPos.iTuple())
			
class cannon(obj_Physics):

	def __init__(self,pos,vel):
		super().__init__(pos,vel)
		self.img = pygame.image.load("images/cannon.png")
		self.barrelImg = pygame.image.load("images/barrell.png")
		self.barrelRect = self.barrelImg.get_rect()
		self.angle = 0
		self.friction = math3d.VectorN((.1,0))
		self.accelSpd = .01	
		self.projectiles = []
		self.shootCD = .5
	
	def update(self, dt):
		super().update(dt)
		self.applyFriction()
		
		for ball in self.projectiles:
			if ball.mPos[0] > width or ball.mPos[1] > height:
				self.projectiles.remove(ball)
		
		eList = pygame.event.get()
		for e in eList:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 1:
					self.shoot()
			elif e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					self.shoot()
		
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.mPos[0] < width:
			self.accel(self.accelSpd,dt)
			
		if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.mPos[0] > 0:
			self.accel(-self.accelSpd,dt)
	
	def render(self,dt):
		tmp = self.rotate()
		screen.blit(tmp, self.mPos.iTuple())
		screen.blit(self.img, self.mPos.iTuple())
		
	def applyFriction(self):
		if self.mVel[0] > 0:
			self.mVel -= self.friction
			if self.mVel[0] < 0:
				self.mVel[0] = 0
		elif self.mVel[0] < 0:
			self.mVel += self.friction
			if self.mVel[0] > 0:
				self.mVel[0] = 0
		
	def shoot(self):
		tmpM = math3d.VectorN(self.getMousePos())
		velV = tmpM - self.mPos
		velV = velV.normalized_copy() * random.uniform(50,350)/100
		print(velV.iTuple())
		self.projectiles.append(cannonBall(self.mPos.iTuple(), velV.iTuple()))

	def getMousePos(self):
		return pygame.mouse.get_pos()             #Returns in a tuple
		
	def getAngle(self):
		mouseV = math3d.VectorN(self.getMousePos())
		newV = mouseV - self.mPos
		angle = math.atan2(newV.mData[0], newV.mData[1])
		angle = angle * (180/math.pi)
		angle = (angle+270) % 360
		if angle > 45 and angle <= 180:
			angle = 45
		elif angle > 180:
			angle = 0
		return angle
		
	def rotate(self):
		rotImg = pygame.transform.rotate(self.barrelImg, self.getAngle())
		return rotImg

#====================Game==================

pygame.display.init()

size = width, height = 800,600
clock = pygame.time.Clock()
done = False

screen = pygame.display.set_mode(size)

C = cannon((400,300),(0,0))

while not done:
	#Update
	dt = clock.tick(60) #This is in milliseconds
	C.update(dt)
	for ball in C.projectiles:
		ball.update(dt)
	
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
	C.render(dt)
	for ball in C.projectiles:
		ball.render(dt)
		
	pygame.display.flip()
	
pygame.display.quit()
	