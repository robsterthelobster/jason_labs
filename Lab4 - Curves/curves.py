import math3d
import pygame
import random

class curvePoint(object):
	"""A curvePoint object. It will display it's own number and hold it's own position and tangent.
	   Each will update and render on there own."""
	def __init__(self, index, pos):
		self.index = index
		self.mPos = math3d.VectorN(pos)
		self.color = (0,255,0)
		self.textOffset = math3d.VectorN((0,-17))
		self.mRad = 8;
		self.isClicked = False
		self.destroy = False
		self.isTanClicked = False
		self.tangentOffset = math3d.VectorN((random.randint(-100,100),random.randint(-100,100)))
		self.tangentPos = self.mPos + self.tangentOffset
		self.tangentColor = (255,0,0)
		self.lineColor = (255,255,255)
		
	def update(self, eList):
		self.tangentOffset = self.tangentPos - self.mPos
		
		for e in eList:
			if e.type == pygame.MOUSEBUTTONDOWN:
				#Right click to drag, this checks if right mouse button is down.
				if e.button == 3:
					if(self.checkMouseOver(self.mPos)):
						self.isClicked = True
					elif(self.checkMouseOver(self.tangentPos)):
						self.isTanClicked = True
				#Middle Click to remove this point.
				if e.button == 2:
					if(self.checkMouseOver(self.mPos)):
						self.destroy = True
			#Checks if mouse button is up. Resets isclicked booleans
			elif e.type == pygame.MOUSEBUTTONUP:
				if e.button == 3:
					self.isClicked = False
					self.isTanClicked = False
			
	def render(self, surf, closed):
		#Display this curvePoint
		if closed:
			pygame.draw.circle(surf, self.color, self.mPos.iTuple(), self.mRad)
		else:
			pygame.draw.circle(surf, self.color, self.mPos.iTuple(), self.mRad, 2)
			
		#Display Tangent Circle
		pygame.draw.circle(surf, self.tangentColor, self.tangentPos.iTuple(), self.mRad, 2)
		pygame.draw.line(surf, self.lineColor, self.mPos, self.tangentPos)
		
		#Display number above this point
		font = pygame.font.SysFont('Arial', 20)
		text = font.render(str(self.index), 1, (0,255,255))
		textRect = text.get_rect()
		textV = math3d.VectorN((textRect[2], textRect[3]))/2
		textpos = self.mPos + self.textOffset - textV
		surf.blit(text,textpos.iTuple())
		
	def checkMouseOver(self, pos):
		"""Checks if this given pos was clicked on"""
		tmp = math3d.VectorN(pygame.mouse.get_pos())
		tmpV = tmp - pos
		lhs = pow(tmpV[0], 2) + pow(tmpV[1], 2)
		rhs = pow(self.mRad, 2)
		if lhs < rhs:
			return True
		else:
			return False
			
	def movePoint(self):
		"""Moves point to mouse position"""
		if self.isClicked:
			self.mPos = math3d.VectorN(pygame.mouse.get_pos())
			self.tangentPos = self.mPos + self.tangentOffset
			
		elif self.isTanClicked:
			self.tangentPos = math3d.VectorN(pygame.mouse.get_pos())
			
class curveManager(object):
	"""Create a curveManager that manages all curvePoints.  This object is able to add, remove, and modify points"""
	def __init__(self):
		self.count = 0
		self.cpList = []
		self.lineColor = (255,255,255)
		self.closed = False
		self.msg = "Left Click: Add C.P.  Middle Click: Remove C.P.  Right Drag: Move C.P./Tan  Space: Toggle Closed/Open"
		self.msgPos = math3d.VectorN((12, 570))
		self.tmpIndex = None
		self.res = 20
		
	def Add(self):
		"""Adds a curvePoint to cpList"""
		self.cpList.append(curvePoint(self.count,pygame.mouse.get_pos()))
		self.count += 1
		
	def Remove(self, cp):
		"""Removes a curvePoint"""
		self.cpList.remove(cp)
		
	def Modify(self, index):
		"""Modifies the curvePoint or its tangent position"""
		self.cpList[index].movePoint()
	
	def update(self, eList):
		if self.cpList:
			#Reversed list because when destroying or editing,
			#it will destroy or modify what is drawn on top (drawn last) first.
			for cp in reversed(self.cpList):
				cp.update(eList);
				if cp.destroy:
					self.Remove(cp)
					break									#Prevents destroying multiple points near the same position
					
				if cp.isClicked or cp.isTanClicked:
					self.tmpIndex = self.cpList.index(cp)	#This is the value that we check to make sure it modifies ONE position.
					break									#Prevents modifying multiple curve or tangent points near the same position
															
				elif not (cp.isClicked and cp.isTanClicked):
					self.tmpIndex = None
					
			if self.tmpIndex != None:		
				self.Modify(self.tmpIndex)
				
		for e in eList:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if e.button == 1:
					self.Add()
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					self.closed = not self.closed
	
	def render(self, surf):
		#Print Menu
		font = pygame.font.SysFont('Arial', 20)
		text = font.render(self.msg, 1, (255,255,255))
		surf.blit(text,self.msgPos.iTuple())
		
		#Lines
		if len(self.cpList) >= 2:
			i = 0
			for i in range(len(self.cpList) - 1):
				for u in range(0,self.res):
					tmpU1 = u/self.res
					cp1 = self.calcDrawPoints(tmpU1, self.cpList[i], self.cpList[i+1])
					tmpU2 = (u+1)/self.res
					cp2 = self.calcDrawPoints(tmpU2, self.cpList[i], self.cpList[i+1])
					pygame.draw.line(surf,self.lineColor,cp1,cp2)
				
			if self.closed and len(self.cpList) >= 2:
				for u in range(0, self.res):
					tmpU1 = u/self.res
					cp1 = self.calcDrawPoints(tmpU1, self.cpList[len(self.cpList)-1], self.cpList[0])
					tmpU2 = (u+1)/self.res
					cp2 = self.calcDrawPoints(tmpU2, self.cpList[len(self.cpList)-1], self.cpList[0])
					pygame.draw.line(surf,self.lineColor,cp1,cp2)
				#pygame.draw.line(surf, self.lineColor, self.cpList[len(self.cpList)-1].mPos, self.cpList[0].mPos)
				
		#Points
		if self.cpList:
			i = 0
			for i in range(len(self.cpList)-1):
				self.cpList[i].render(surf, True)
				
			self.cpList[len(self.cpList)-1].render(surf, self.closed)
				
	def calcDrawPoints(self, res, cp1, cp2):
		a = 2*pow(res,3) - 3*pow(res,2) + 1
		b = pow(res,3) - 2*pow(res,2)+res
		c = -2*pow(res,3) + 3*pow(res,2)
		d = pow(res,3) - pow(res,2)
		return a*cp1.mPos + b*(cp1.tangentPos - cp1.mPos)*10 + c*cp2.mPos + d*(cp2.tangentPos-cp2.mPos)*10
		
		
if __name__=="__main__":

	pygame.init()

	size = width, height = 800,600
	clock = pygame.time.Clock()
	done = False
	
	screen = pygame.display.set_mode(size)
	
	C = curveManager()
	
	while not done:
		eList = pygame.event.get()
		#Update
		dt = clock.tick()/1000
		C.update(eList)
		
		#Inputs
		for e in eList:
			if e.type == pygame.QUIT:
				done = True
				
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			done = True
			
		#Draw
		bgColor = 0, 0, 0
		screen.fill(bgColor)
		
		C.render(screen)
			
		pygame.display.flip()
		
	pygame.display.quit()