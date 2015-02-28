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
			#print("Stopped")
			self.mVel = math3d.VectorN(2)
			
class boulder(physicsObject):
	def __init__(self, pos, vel):
		super().__init__(pos,vel)
		self.img = pygame.image.load("images/boulder_simple.bmp")
		#self.img = pygame.image.load("images/boulder.bmp").convert_alpha()
		
	def update(self, dt):
		super().update(dt)
	
	def render(self, surf, dt):
		pass
	
	def accel(self, a, dt):
		super().accel(a, dt)
		
	def friction(self, f, dt):
		super().friction(f,dt)
		
class player(physicsObject):
	def __init__(self,pos,vel):
		super().__init__(pos, vel)
		self.velMax = 800
		self.velInc = 8000
		#self.img = pygame.image.load("images/boulder_simple.bmp").convert_alpha()
		self.img = pygame.image.load("images/indiana_jones.bmp").convert_alpha()
		self.imgRect = self.img.get_rect()
		self.imgs = []
		for i in range(12):
			self.imgs.append(pygame.transform.chop(self.img, (0,0,self.imgRect[2]/(i+1),self.imgRect[3])))
		
	def update(self, eList, dt):
		#print(self.mVel)
		if not self.mVel.isZero():
			self.friction(self.velInc*.8, dt)
		super().update(dt)
		
		for e in eList:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 1:
					pass
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_UP] or keys[pygame.K_w]):
			self.accel((0, -self.velInc), dt)
		if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
			self.accel((0, self.velInc), dt)
		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
			self.accel((self.velInc,0), dt)
		if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
			self.accel((-self.velInc,0), dt)
					
	def render(self, surf, dt):
		surf.blit(self.img, self.mPos.iTuple())
		#surf.blit(self.imgs[1], self.mPos.iTuple())
		
	def accel(self, a, dt):
		super().accel(a, dt)
		
		if self.mVel.dot(self.mVel) > pow(self.velMax,2):
			self.mVel = self.mVel.normalized_copy()*self.velMax
		
	def friction(self, f, dt):
		super().friction(f, dt)
		
class laser(object):
	def __init__(self, pos):
		self.mPos = math3d.VectorN(pos)
		self.angle = 180
		
	def update(self, dt):
		pass
	
	def render(self, surf, dt):
		pass
		
#====================Game==================

pygame.display.init()

size = width, height = 1280,720
clock = pygame.time.Clock()
done = False

screen = pygame.display.set_mode(size)

P = player((width/2,height/2),(0,0))

while not done:
	eList = pygame.event.get()
	#Update
	dt = clock.tick()/1000
	P.update(eList,dt)
	
	for e in eList:
		if e.type == pygame.QUIT:
			done = True
	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		done = True
		
	#Draw
	bgColor = 0, 0, 0
	screen.fill(bgColor)
	P.render(screen, dt)
		
	pygame.display.flip()
	
pygame.display.quit()