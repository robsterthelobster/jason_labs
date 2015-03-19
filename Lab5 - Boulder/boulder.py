import math
import random
import pygame
import math3d

class physicsObject(object):
	def __init__(self, pos, vel):
		self.mPos = math3d.VectorN(pos)
		self.mVel = math3d.VectorN(vel)
		
	def update(self, dt):
		self.mPos += self.mVel*dt
	
	def accel(self, a, dt):
		aV = math3d.VectorN(a)
		self.mVel += aV*dt
		
	def friction(self, f, dt):
		old = self.mVel.copy()
		frict = -(self.mVel.normalized_copy()*f)
		self.mVel += frict*dt
		if self.mVel.dot(old) < 0:
			self.mVel = math3d.VectorN(2)
			
	def getCenteredImgPos(self, img):
		imgRect = img.get_rect()
		return math3d.VectorN((self.mPos[0]-imgRect[2], self.mPos[1]-imgRect[3])).iTuple()
		

class objectManager(object):
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.screenWidth = pygame.display.Info().current_w
		self.screenHeight = pygame.display.Info().current_h
		self.boulderList = []
		self.laser = laser(((random.randint(0,self.screenWidth)),random.randint(0,self.screenHeight)), self.screenWidth)
		#self.laser = laser((self.screenWidth*4/5,self.screenHeight/2), self.screenWidth)
		self.player = player((self.screenWidth/2,self.screenHeight/2),(0,0),
							 self.loadSprites("images/boulder_simple.bmp",
							 (348/12, 34), 12))
		
	def update(self, eList, dt):
		self.laser.update(dt)
		self.player.update(eList, dt)
	
		if self.boulderList:
			for b in self.boulderList:
				b.update(dt)
				
			#For bouncing with other boulders, look in the link in the assignment pdf
			#for i in range(len(boulderList))
				#for j in range(i+1, len(boulderList))
					#do something
	
				
	def render(self, dt):
		if self.boulderList:
			for b in self.boulderList:
				b.render(self.screen, dt)
		
		self.laser.render(self.screen, dt)
		
		self.player.render(self.screen, dt)
		
	def loadSprites(self, imagePath, dimension, numImages):
		imageSurface = pygame.image.load(imagePath)
		imageSurface.set_colorkey((0,0,0))
		surfaces = []
		for i in range(numImages):
			rect = pygame.Rect(i*dimension[0], 0, dimension[0], dimension[1])
			print(rect)
			surfaces.append(imageSurface.subsurface(rect))
		return surfaces
	
class boulder(physicsObject):
	def __init__(self, pos, vel):
		super().__init__(pos,vel)
		self.img = pygame.image.load("images/boulder_simple.bmp")
		#self.img = pygame.image.load("images/boulder.bmp").convert_alpha()
		self.imgRect = self.img.get_rect()
		self.rotation = 0
		self.rad = 30
		#self.rad = random.randInt(30,70)
		
	def update(self, dt):
		super().update(dt)
		
		#Bounce when hit screen edges
		

	def render(self, surf, dt):
		rotImg = pygame.transform.rotate(self.img, self.rotation)
		screen.blit(rotImg, self.getCenteredImgPos)
	
	def accel(self, a, dt):
		super().accel(a, dt)
		
	def friction(self, f, dt):
		super().friction(f,dt)
		
	def getCenteredImgPos(self, img):
		super().getCenteredImgPos(img)
		
class player(physicsObject):
	def __init__(self,pos, vel, images):
		super().__init__(pos, vel)
		self.velMax = 700
		self.velInc = 7000
		self.images = images
		#self.img = pygame.image.load("images/indiana_jones.bmp").convert_alpha()
		self.imgRect = self.img.get_rect()
		self.isMoving = False			#For mouse
		self.stillMoving = False		#For walking animation
		self.lastDirection = "down"
		self.currFrame = 1				#Keeps track of walking animation frame
		#for i in range(12):
		#	self.imgs.append(pygame.transform.chop(self.img, (0,0,self.imgRect[2]/(i+1),self.imgRect[3])))
		
		#Sprite sheet
		#screen.blit(frame*offset, 0,0,26,48) basically a rectangle of the image
		
		
	def update(self, eList, dt):
		#print(self.mVel)
		if not self.mVel.isZero():
			self.stillMoving = True
			self.friction(self.velInc*.8, dt)
		if self.mVel.isZero():
			self.stillMoving = False
		super().update(dt)
		
		for e in eList:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 1:
					self.isMoving = True
					
			if e.type == pygame.MOUSEBUTTONUP:
				if e.button == 1:
					self.isMoving = False
					
		if self.isMoving:
			self.mouseMove(dt)
					
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_UP] or keys[pygame.K_w]):
			self.accel((0, -self.velInc), dt)
			self.lastDirection = "up"
		if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
			self.accel((0, self.velInc), dt)
			self.lastDirection = "down"
		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
			self.accel((self.velInc,0), dt)
			self.lastDirection = "right"
		if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
			self.accel((-self.velInc,0), dt)
			self.lastDirection = "left"
			
		#For direction, use mouse pos angle to find last direction
					
	def render(self, surf, dt):
		#Add moving animation and account for facing direction
	
		currImg = self.images[self.currFrame]
		surf.blit(currImg, self.mPos.iTuple())
		
		
	def accel(self, a, dt):
		super().accel(a, dt)
		
		if self.mVel.dot(self.mVel) > pow(self.velMax,2):
			self.mVel = self.mVel.normalized_copy()*self.velMax
		
	def friction(self, f, dt):
		super().friction(f, dt)
		
	def mouseMove(self, dt):
		tmp = (math3d.VectorN(pygame.mouse.get_pos()) - self.mPos).normalized_copy()
		tmp = tmp*self.velInc
		self.accel(tmp.iTuple(), dt)
		
	def getLastDirection(self):
		pass
		
class laser(object):
	def __init__(self, pos, screenWidth):
		self.mPos = math3d.VectorN(pos)
		
		self.angleMax = 360
		self.angleMin = 0
		#self.angle = 180
		tmp = math3d.VectorN((pygame.display.Info().current_w/2,pygame.display.Info().current_h/2)) - self.mPos
		self.angle = math.atan2(-tmp[1], tmp[0])*180/math.pi + 180
		self.angleInc = 50
		
		self.laserLength = screenWidth*.6
		self.endPos = self.mPos-self.mPos.normalized_copy()*self.laserLength
		self.color = (255,255,255)
		self.mRad = 20
		self.beamColor = (255,0,0)
		
	def update(self, dt):
		print(self.angle)
		self.angle += self.angleInc*dt
		if self.angle >= self.angleMax or self.angle <= self.angleMin:
			self.angleInc *= -1
		x = math.cos(math.radians(self.angle))
		y = math.sin(math.radians(self.angle))
		tmp = math3d.VectorN((x,y))*self.laserLength
		self.endPos = tmp + self.mPos
		
		#Hitting object
		#Get perpendicular line with object and check if that line is less than radius of object
		#Best way is to check all objects
			
	def render(self, surf, dt):
		pygame.draw.line(surf, self.beamColor, self.mPos.iTuple(), self.endPos.iTuple())
		pygame.draw.circle(surf, self.color, self.mPos.iTuple(), self.mRad)
		
#====================Game==================

pygame.display.init()

size = width, height = 1280,720
clock = pygame.time.Clock()
done = False

screen = pygame.display.set_mode(size)

M = objectManager()

while not done:
	eList = pygame.event.get()
	#Update
	dt = clock.tick()/1000
	M.update(eList, dt)
	
	for e in eList:
		if e.type == pygame.QUIT:
			done = True
	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		done = True
		
	#Draw
	bgColor = 0, 0, 0
	screen.fill(bgColor)
	M.render(dt)
		
	pygame.display.flip()
	
pygame.display.quit()