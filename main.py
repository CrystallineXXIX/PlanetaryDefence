import pygame
import sys
from math import *
import random

pygame.init()
screen = pygame.display.set_mode((1200,800))
bg = pygame.image.load('Assets/bg.jpeg').convert()
blist = []
enemies = []
started = False
lives = 10
angle = 90
tip = ()
remaining = 5
score = 0
points = 0

with open('Highscore.txt','r') as f:
	high = highscore =  int(f.read())

class Ball():
	def __init__(self,pos,speed,angle,color = False):
		angle = radians(angle) 
		self.x = pos[0]
		self.y = pos[1]
		self.xvel = speed * cos(angle)
		self.yvel = -speed * sin(angle)
		self.img = pygame.image.load('assets/bullet.png').convert()
		self.bullet = None
		self.heading = angle
		self.color = color
		self.rect = self.img.get_rect(center = pos)
		
class Enemy():
	def __init__(self,health,speed):
		self.x = random.choice(list(range(20,800,20)))
		self.y = 0
		self.health = health
		self.currenthealth = health
		self.speed = speed
		self.rect = None
	def randomize(self):
		self.x = random.choice(list(range(20,800,20)))
		self.y = 0
		self.health,self.speed = random.randint(3,5),random.randint(1,5)
		self.currenthealth = self.health
	def move(self):
		global lives,blist,score,points,remaining,high
		hp = (self.currenthealth/self.health)*100
		if hp >= 90:
			color = 'green' 
		elif hp >= 50:
			color = 'orange'
		elif hp >= 30:
			color = 'yellow'
		else:
			color = 'red'
		self.y += self.speed
		self.rect = pygame.Rect(self.x-20,self.y-20,40,40)
		for bullet in blist:
			if self.rect.collidepoint((bullet.x,bullet.y)):
				self.currenthealth -= 1
				blist.remove(bullet)
			if self.currenthealth <= 0:
				self.randomize()
				score += 1
				if score > high:
					high = score
				points += 1
				if points > 49:
					points = 0 
					if remaining < 5:
						remaining +=1
			if self.y >= 800:
				lives -= 1
				self.randomize()
		pygame.draw.rect(screen,color,self.rect)
		
def shoot(balls,ang):

	global started,tip
	
	#label = pygame.font.SysFont('Monospace',32).render('•',1,'#ffffff')
	angle = ang + random.randint(-10,10)
	#ang = radians(degrees(- atan((750-pygame.mouse.get_pos()[1])/(pygame.mouse.get_pos()[0]+1))))
	if started:
		balls.append(Ball(tip,20,angle))
		started = False
	
	for ball in balls:
		
		ball.x += ball.xvel
		ball.y += ball.yvel
		#ball.heading = degrees(-atan(ball.yvel/ball.xvel)) - 90
		
		if ball.color: ball.rect = pygame.Rect(ball.x-5,ball.y-5,10,10)
		else:
			img = pygame.transform.rotozoom(ball.img,degrees(ball.heading) - 90,0.25)
			imgrect = img.get_rect(center = (ball.x,ball.y))
		color = 'blue' if ball.color else 'red'
		if color == 'blue':
			pygame.draw.rect(screen,color,ball.rect)
		else:
			screen.blit(img,imgrect)
		
		if ball.color and ball.y < 200:
			balls.remove(ball)
		if ball.y < 0 or ball.x > 800:
			balls.remove(ball)
	return balls
def hyperclear():
	for i in range(20,800,20):
		for j in range(5):
			blist.append(Ball((i,800-(15*j)),40,90,True))

def line(O = 0):
	global tip 
	
	""" x1,y1 = 600,800
	x2,y2 = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1] 
	m = (y2-y1)/(x2-x1+0.01) 
	O = -degrees(atan(m)) """
	if O > 0:
		x =  400 + 125 * cos(radians(O))
		y =  800 - 125* sin(radians(O))
	else:
		O = O + 180
		x =  400 + 125 * cos(radians(O))
		y =  800 - 125* sin(radians(O))

	pygame.draw.line(screen,'#FFFFFF',(400,800),(x,y),10)
	pygame.draw.rect(screen,'#FFFFFF',(x-5,y-5,10,10))
	tip = (x,y)#print(O,(x2,y2))
	return O

def ui():
	pygame.draw.line(screen,'white',(810,0),(810,800),10)
	font = pygame.font.SysFont('Monospace',22)
	label = font.render('Health',1,'black','white')
	lrect = label.get_rect(topleft = (860,750))
	screen.blit(label,lrect)
	label = font.render('Hyperclear(<S>)',1,'black','white')
	lrect = label.get_rect(topleft = (980,750))
	screen.blit(label,lrect)
	font = pygame.font.SysFont('Monospace',32)
	label = font.render(f'Score: {score}',1,'white')
	lrect = label.get_rect(topleft = (860,50))
	screen.blit(label,lrect)
	label = font.render(f'Highcore: {high}',1,'white')
	lrect = label.get_rect(topleft = (860,100))
	screen.blit(label,lrect)
	pygame.draw.rect(screen,'red',(870,int(700-((lives/10)*500)),60,int((lives/10)*500)))
	pygame.draw.rect(screen,'blue',(1050,int(700-((remaining/5)*500)),60,int((remaining/5)*500)))


for _ in range(5):
	enemies.append(Enemy(random.randint(3,5),random.randint(1,3)))

c = 0
while lives > 0:
	pygame.time.Clock().tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			started = True
		if event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and remaining > 0:
					remaining -= 1
					hyperclear()

	screen.fill('#000000')
	screen.blit(bg,(0,120))
	if (pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]) and angle < 175:
		angle += 5
	if (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]) and angle > 5:
		angle -= 5

	line(angle)
	c += 1
	if c > 1:
		c = 0
		started = True
	blist = shoot(blist,angle)
	for i in enemies:
		i.move()

	pygame.draw.circle(screen,'#FFFFFF',(400,800),75)
	ui()
	
	pygame.display.update()

if score > highscore:
	with open('Highscore.txt','w') as f:
		f.write(str(score))