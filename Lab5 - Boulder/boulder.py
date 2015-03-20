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
			
	def getCenteredImgPos(self, img, imgRect):
		tmp = math3d.VectorN((self.mPos[0]-imgRect[2], self.mPos[1]-imgRect[3])).iTuple()
		return tmp

class objectManager(object):
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.screenWidth = pygame.display.Info().current_w
		self.screenHeight = pygame.display.Info().current_h
		self.boulderList = []
		self.playerImage = self.loadSprites("images/indiana_jones.bmp",(29, 34), 12, (65,136,164))
		self.player = player(self.getRandPos(29,34).iTuple(),(0,0),self.playerImage)
		self.boulderImage = self.loadSprites("images/boulder.bmp", (64,64),100,(64,64,64))

		for i in range(10):
			tmpV = self.getRandPos(64, 64)
			tmpS = random.uniform(.5,2)
			if self.boulderList:
				overlap = True
				while overlap:
					for b in self.boulderList:
						newV = b.mPos-tmpV
						if newV.dot(newV) > pow(b.radius+(32*tmpS), 2):
							overlap = False
						else:
							overlap = True
							tmpV = self.getRandPos(64, 64)
							break
				
			vX = random.randint(-250,250)
			vY = random.randint(-250,250)
			self.boulderList.append(boulder(tmpV.iTuple(),(vX,vY),self.boulderImage,tmpS))
			
		rad = 20
		self.laser = laser(self.getRandPos(20,20).iTuple(), self.screenWidth, 
							rad, self.boulderList, self.player)
		
	def update(self, eList, dt):
		self.laser.update(dt)
		self.player.update(eList, dt)
	
		if self.boulderList:
			for b in self.boulderList:
				b.update(dt)
				
			#For bouncing with other boulders, look in the link in the assignment pdf
			if len(self.boulderList) >= 2:
				for i in range(len(self.boulderList)):
					for j in range(i+1, len(self.boulderList)):
						B1 = self.boulderList[i]
						B2 = self.boulderList[j]
						n = B2.mPos-B1.mPos
						un = n.normalized_copy()
						
						if n.dot(n) <= pow(B1.radius+B2.radius,2):
							V1 = B1.mVel
							V2 = B2.mVel
							nV = V2-V1
							unV = nV.normalized_copy()
							utV = math3d.VectorN((-unV[1],unV[0]))
							dotV = unV.dot(utV)							#?
							
							nV1 = unV.dot(V1)
							tV1 = utV.dot(V1)
							nV2 = unV.dot(V2)
							tV2 = utV.dot(V2)
							
							new_nV1 = (nV1*(B1.radius - B2.radius)+2*B2.radius*nV2)/(B1.radius+B2.radius)
							new_nV2 = (nV2*(B2.radius - B1.radius)+2*B1.radius*nV1)/(B1.radius+B2.radius)
							
							new_nV1 *= unV
							new_tV1 = tV1*utV
							new_nV2 *= unV
							new_tV2 = tV1*utV
							
							new_V1 = new_nV1 + new_tV1
							new_V2 = new_nV2 + new_tV2
							
							B1.mVel = new_V1
							B2.mVel = new_V2
			#===============End of boulder collision===============
				
	def render(self, dt):
		if self.boulderList:
			for b in self.boulderList:
				b.render(self.screen, dt)
		
		self.laser.render(self.screen, dt)
		
		self.player.render(self.screen, dt)
		
	def loadSprites(self, imagePath, dimension, numImages, colorkey):
		imageSurface = pygame.image.load(imagePath).convert()
		imageSurface.set_colorkey(colorkey)
		surfaces = []
		for i in range(numImages):
			rect = pygame.Rect(i*dimension[0], 0, dimension[0], dimension[1])
			surfaces.append(imageSurface.subsurface(rect))
		return surfaces
	
	def getRandPos(self, w, h):
		x = random.randint(w,self.screenWidth-w)
		y = random.randint(h,self.screenHeight-h)
		return math3d.VectorN((x,y))
		
class boulder(physicsObject):
	def __init__(self, pos, vel, images, scale):
		super().__init__(pos,vel)
		self.img = images
		self.scaleMultiplier = scale
		self.radius = 64/2 * self.scaleMultiplier
		self.rotation = 0
		self.rotIncr = 50
		self.indexIncr = 100
		self.indexFloat = 0
		self.imgIndex = 0
		self.imgRect = self.img[self.imgIndex].get_rect()
		
	def update(self, dt):
		super().update(dt)
		self.rotation += self.rotIncr * dt
		self.indexFloat += (self.indexIncr*dt)
		if self.indexFloat >= 100:
			self.indexFloat = 0
		self.imgIndex = round(self.indexFloat)
		if self.imgIndex >= len(self.img):
			self.imgIndex = 0
		self.imgRect = self.img[self.imgIndex].get_rect()
		
		#Bounce when hit screen edges
		if self.mPos[0] < round(self.radius):
			self.mPos[0] = round(self.radius)
			self.mVel[0] *= -1
		elif self.mPos[0] > pygame.display.Info().current_w - round(self.radius):
			self.mPos[0] = pygame.display.Info().current_w - round(self.radius)
			self.mVel[0] *= -1
		elif self.mPos[1] < round(self.radius):
			self.mPos[1] = round(self.radius)
			self.mVel[1] *= -1
		elif self.mPos[1] > pygame.display.Info().current_h - round(self.radius):
			self.mPos[1] =  pygame.display.Info().current_h - round(self.radius)
			self.mVel[1] *= -1

	def render(self, surf, dt):
		tmpV = math3d.VectorN((self.imgRect[2],self.imgRect[3]))
		tmpV *= self.scaleMultiplier
		scaleImg = pygame.transform.scale(self.img[self.imgIndex], tmpV.iTuple())
		rotImg = pygame.transform.rotate(scaleImg, self.rotation)
		rotRect = rotImg.get_rect()
		screen.blit(rotImg, self.mPos-math3d.VectorN((rotRect[2]/2,rotRect[3]/2)))
	
	def accel(self, a, dt):
		super().accel(a, dt)
		
	def friction(self, f, dt):
		super().friction(f,dt)
		
class player(physicsObject):
	def __init__(self,pos, vel, images):
		super().__init__(pos, vel)
		self.velMax = 700
		self.velInc = 7000
		self.images = images
		self.rightImgs = [0,1,2]
		self.upImgs    = [3,4,5]
		self.leftImgs  = [6,7,8]
		self.downImgs  = [9,10,11]
		self.imgRect = self.images[0].get_rect()
		self.isMoving = False			#For mouse
		self.stillMoving = False		#For walking animation
		self.lastDirection = "down"
		self.frameFloat = 0
		self.currFrame = 1				#Keeps track of walking animation frame
		self.currImg = self.images[self.downImgs[self.currFrame]]
		
	def update(self, eList, dt):
		if not self.mVel.isZero():
			self.stillMoving = True
			self.friction(self.velInc*.8, dt)
		if self.mVel.isZero():
			self.stillMoving = False
		super().update(dt)
		self.lastDirection = self.getLastDirection()
		
		for e in eList:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 1:
					self.isMoving = True
					
			if e.type == pygame.MOUSEBUTTONUP:
				if e.button == 1:
					self.isMoving = False
					
		if self.isMoving:
			self.mouseMove(dt)
			#print(self.getLastDirection())
					
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
					
	def render(self, surf, dt):
		if self.stillMoving:
			self.frameFloat += 10*dt
			if self.frameFloat >= 2:
				self.frameFloat = 0

		if not self.stillMoving:
			self.currFrame == 1
			
		self.currFrame = round(self.frameFloat)
		#print(self.currFrame)
		if self.lastDirection == "up":
			self.currImg = self.images[self.upImgs[self.currFrame]]
		elif self.lastDirection == "down":
			self.currImg = self.images[self.downImgs[self.currFrame]]
		elif self.lastDirection == "right":
			self.currImg = self.images[self.rightImgs[self.currFrame]]
		elif self.lastDirection == "left":
			self.currImg = self.images[self.leftImgs[self.currFrame]]
		if self.currFrame >= 2:
			self.currFrame = 0
		surf.blit(self.currImg, self.mPos.iTuple())
		
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
		tmp = "down"
		mousePos = math3d.VectorN(pygame.mouse.get_pos())
		tmpV = (mousePos - self.mPos).iTuple()
		angle = math.atan2(-tmpV[1], tmpV[0])*180/math.pi
		if angle >= -45 and angle <= 45:
			tmp = "right"
		elif angle > 45 and angle <= 135:
			tmp = "up"
		elif angle > 135 and angle <= 180 or angle >= -180 and angle <= -135:
			tmp = "left"
		elif angle < -45 and angle > -135:
			tmp = "down"
		return tmp
		
class laser(object):
	def __init__(self, pos, screenWidth, rad, boulderList, player):
		self.mPos = math3d.VectorN(pos)
		self.objectList = boulderList[:]
		self.objectList.append(player)
		self.angleMax = 360
		self.angleMin = 0
		#self.angle = 180
		tmp = math3d.VectorN((pygame.display.Info().current_w/2,pygame.display.Info().current_h/2)) - self.mPos
		self.angle = math.atan2(-tmp[1], tmp[0])*180/math.pi + 180
		self.angleInc = 50
		
		self.laserLength = screenWidth*.6
		self.endPos = self.mPos-self.mPos.normalized_copy()*self.laserLength
		self.color = (255,255,255)
		self.mRad = rad
		self.beamColor = (255,0,0)
		
	def update(self, dt):
		#print(self.angle)
		self.angle += self.angleInc*dt
		#if self.angle >= self.angleMax or self.angle <= self.angleMin:
		#	self.angleInc *= -1
		x = math.cos(math.radians(self.angle))
		y = math.sin(math.radians(self.angle))
		tmp = math3d.VectorN((x,y))*self.laserLength
		self.endPos = tmp + self.mPos
		
		#Hitting object
		#Get perpendicular line with object and check if that line is less than radius of object
		#Best way is to check all objects
		for obj in self.objectList:
			pass
		
			
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