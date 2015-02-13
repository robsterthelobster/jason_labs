import pygame
import math3d
import random
import math

class obj_Physics(object):
	"""A object that has basic attributes and definitions for this game such as:
	   -self.mPos: VectorN object holding object's position
	   -self.mVel: VectorN object holding object's velocity
	   -def accel: This object's acceleration
	   -def update: This object's basic update method of movement"""
	def __init__(self, pos, vel):
		self.mPos = math3d.VectorN(pos)
		self.mVel = math3d.VectorN(vel)
		
	def accel(self, a, dt):
		self.mVel += math3d.VectorN((a*dt,0))
		
	def update(self, dt):
		self.mPos += self.mVel * dt
		
	def friction(self, dt, k):
		"""In this lab, friction is only used for cannon"""
		oldVel = self.mVel.copy()
		af = -k*self.mVel.normalized_copy()
		self.mVel += af*dt
		if (oldVel[0] > 0 and self.mVel[0] < 0) or (oldVel[0] < 0 and self.mVel[0] > 0):
			self.mVel = math3d.VectorN(2)

	#For testing
	def printPos(self):
		print(self.mPos)
		
	def printVel(self):
		print(self.mVel)
		
	def printAll(self):
		self.printPos()
		self.printVel()

class cannonBall(obj_Physics):
	"""A cannonball object, which automatically rotates itself and has its own gravity.
	   Will destroy itself when out of screen."""
	def __init__(self, pos, vel):
		super().__init__(pos,vel)
		self.img = pygame.image.load("images/coconut.png").convert_alpha()
		self.imgRect = self.img.get_rect()
		self.gravity = math3d.VectorN((0,.2))
		self.rotation = 0
	
	def update(self, dt):
		super().update(dt)
		self.rotation += random.randint(0,2)
		self.mVel += self.gravity
	
	def render(self, dt):
		tmp = pygame.transform.rotate(self.img, self.rotation)
		screen.blit(tmp, (self.mPos[0]-self.imgRect[2], self.mPos[1]-self.imgRect[3]))	
class cannon(obj_Physics):
	"""Creates a cannon object.  The barrel will rotate between 0-45 degree angles.
	   The cannon can move left and right restricted to screen width.
	   The cannon can also shoot cannonballs."""

	def __init__(self,pos,vel):
		super().__init__(pos,vel)
		#Cannon Base
		self.img = pygame.image.load("images/cannon.png").convert_alpha()
		self.imgRect = self.img.get_rect()
		self.width = self.imgRect[0]
		#Cannon Barrel
		self.barrelOffset = math3d.VectorN((75,12))
		self.barrelImg = pygame.image.load("images/barrell.png").convert_alpha()
		self.barrelRect = self.barrelImg.get_rect()
		self.angle = 0
		#Other
		self.accelSpd = width
		self.projectiles = []
	
	def update(self, dt):
		#Handles movement
		super().update(dt)
		if not self.mVel.isZero():
			self.friction(dt,width/3)
		#Handles cannonball objects, specially destroying them out of screen
		for ball in self.projectiles:
			if ball.mPos[0] > width or ball.mPos[1] < 0 or ball.mPos[1] > height:
				self.projectiles.remove(ball)
		#Handles Inputs for cannon
		eList = pygame.event.get()
		for e in eList:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 1:
					self.shoot()
			elif e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					self.shoot()
			elif e.type == pygame.QUIT:
				return True
		
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
			self.accel(self.accelSpd,dt)
			
		if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
			self.accel(-self.accelSpd,dt)
		
		#Restrict movements to screen
		if self.mPos[0] <= 0:
			self.mPos[0] = 1
			self.mVel[0] = 0
		if self.mPos[0] >= width-self.barrelRect[2]:
			self.mPos[0] = width-self.barrelRect[2]-1
			self.mVel[0] = 0
		
		return False
	def render(self,dt):
		"""Rotates barrelImg first, then draws barrel and finally draws cannon base"""
		tmp = self.rotate()
		tmpRect = tmp.get_rect()
		tmpVector = self.barrelOffset - math3d.VectorN((tmpRect[2],tmpRect[3]))/2
		screen.blit(tmp, (self.mPos + tmpVector).iTuple())
		screen.blit(self.img, self.mPos.iTuple())
		
	def shoot(self):
		"""Creates a cannonball object at cannon tip with a random velocity
		in that angle"""
		#Position
		angle = math.radians(self.getAngle())
		cY = math.sin(angle) * self.barrelRect[2]/2
		cX = math.cos(angle) * self.barrelRect[2]/2
		offset = math3d.VectorN((cX,-cY)) + self.barrelOffset
		finalPos = self.mPos + offset
		#velocity
		velV = finalPos - self.mPos
		velV = velV.normalized_copy() * random.uniform(350,700)
		#velV = math3d.VectorN((random.uniform(50,350),-random.uniform(50,350)))
		self.projectiles.append(cannonBall((finalPos[0],finalPos[1]), velV.iTuple()))

	def getMousePos(self):
		return pygame.mouse.get_pos()             #Returns in a tuple
		
	def getAngle(self):
		"""Returns angle using mouse position and self.mPos"""
		mouseV = math3d.VectorN(self.getMousePos())
		newV = mouseV - self.mPos
		angle = math.atan2(-newV.mData[1], newV.mData[0])
		angle = angle * (180/math.pi)
		if angle > 45:
			angle = 45
		elif angle < 0:
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

C = cannon((width/2,height*.7),(0,0))

while not done:
	#Update
	dt = clock.tick()/1000
	done = C.update(dt)
		
	for ball in C.projectiles:
		ball.update(dt)
		
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
	