# -*- coding: utf-8 -*-
from tkinter import *
from random import randint
from math import sqrt
 
block_size = (25,25) #taille d'un bloc en pixel
map_size = (25,25) #taille de la carte en bloc l*h
grille = 0 # 0 pour ne pas l'afficher, 1 pour l'afficher
append = 3 # croissance de serpent à chaque fois qu'il mange
lene = 4 # longueur de départ

def dist_euclid(point1, point2):
	return sqrt((point1[0]-point2[0])**2 + (point1[1] - point2[1])**2)

class Block :
 
	def __init__(self,x,y,can,state="void"):
		self.x = x
		self.y = y
		self.can = can
		self.state = state
		self.draw()
 
	def draw(self):
		self.display = self.can.create_rectangle(self.x*block_size[0], self.y*block_size[1],\
			(self.x+1)*block_size[0], (self.y+1)*block_size[1], fill=("black" if self.state == "void" else  ("red" if self.state == "food" else "white")),width=grille)
		self.update()
 
	def update(self):
		self.can.itemconfigure(self.display,fill=("black" if self.state == "void" else ("red" if self.state == "food" else "white")))
		

class Snake :
 
	def __init__(self,can,appende=1,lene=2):
		self.appende = appende
		self.x = round(map_size[0]/2)
		self.y = round(map_size[1]/2)
		self.can = can
		self.tail = [(self.x,self.y)]
		self.map = []
		self.coords = []
		self.food = (randint(0,map_size[0]-1),randint(0,map_size[1]-1))
		self.direction = "right"
		self.len = lene
		self.game = False
		self.draw()
		self.update()
		self.finish = True
		self.dist = {"wallHG" : [],
					 "wallH" : [],
					 "wallHD":[],
					 "wallD":[],
					 "wallBD":[],
					 "wallB":[],
					 "wallBG":[],
					 "wallG":[],
					 "tailHG" : [],
					 "tailH" : [],
					 "tailHD":[],
					 "tailD":[],
					 "tailBD":[],
					 "tailB":[],
					 "tailBG":[],
					 "tailG":[],
					 "foodHG" :[],
					 "foodH" : [],
					 "foodHD":[],
					 "foodD":[],
					 "foodBD":[],
					 "foodB":[],
					 "foodBG":[],
					 "foodG":[]}
 
	def draw(self):
		for x in range(map_size[0]):
			for y in range(map_size[1]):
				self.map.append(Block(x,y,can))
				self.coords.append((x,y))
				 
	def update(self):
		for block in self.map:
			if (block.x,block.y) in self.tail :
				block.state = "snake"
			elif (block.x,block.y) == self.food :
				block.state = "food"
			else :
				block.state = "void"
			block.update()
		if self.direction == "right" :
			self.move(1,0)
		if self.direction == "left" :
			self.move(-1,0)
		if self.direction == "up" :
			self.move(0,-1)
		if self.direction == "down" :
			self.move(0,1)
		if self.tail[-1][0] == self.food[0] and self.tail[-1][1] == self.food[1] :
			while self.food in self.tail :
				self.food = (randint(0,map_size[0]-1),randint(0,map_size[1]-1))
			self.len += self.appende
		if self.tail[-1] in self.tail[0:-1] or not self.tail[-1] in self.coords :
			self.game = False
			print(f"Your score is {self.len}")
			print("Game over")
			self.finish = False
		self.x = self.tail[-1][0]
		self.y = self.tail[-1][1]
 
	def move(self,x,y):
		self.tail.append((self.tail[-1][0]+x,self.tail[-1][1]+y))
		while len(self.tail) > self.len :
			del self.tail[0]

	def entree_ai(self) :
		self.dist["tailG"] = self.dist["tailD"] = self.dist["foodG"] = self.dist["foodD"] = False
		self.dist["tailH"] = self.dist["tailB"] = self.dist["foodH"] = self.dist["foodB"] = False
		for x in range(map_size[0]+2) :
			if not (x-1,self.y) in self.coords :
				if x-1 < 0 :
					self.dist["wallG"] = dist_euclid((self.x,self.y),(x-1,self.y))
					continue
				elif x-1 >= map_size[0] :
					self.dist["wallD"] = dist_euclid((self.x,self.y),(x-1,self.y))
					continue
			if (x-1, self.y) in self.tail :
				if x-1 < self.x :
					if dist_euclid((self.x,self.y),(x-1,self.y)) < self.dist["tailG"] or self.dist["tailG"] == False :
						self.dist["tailG"] = dist_euclid((self.x,self.y),(x-1,self.y))
						continue
				elif x-1 > self.x :
					if dist_euclid((self.x,self.y),(x-1,self.y)) < self.dist["tailD"] or self.dist["tailD"] == False :
						self.dist["tailD"] = dist_euclid((self.x,self.y),(x-1,self.y))
						continue
			if (x-1,self.y) == self.food :
				if x-1 < self.x :
					self.dist["foodG"] = dist_euclid((self.x,self.y),(x-1,self.y))
					continue
				elif x-1 > self.x :
					self.dist["foodD"] = dist_euclid((self.x,self.y),(x-1,self.y))
########################################################################################################
		for y in range(map_size[1]+2) :
			if not (self.x,y-1) in self.coords :
				if y-1 < 0 :
					self.dist["wallH"] = dist_euclid((self.x,self.y),(self.x,y-1))
					continue
				elif y-1 >= map_size[1] :
					self.dist["wallB"] = dist_euclid((self.x,self.y),(self.x,y-1))
					continue
			if (self.x,y-1) in self.tail :
				if y-1 < self.y :
					if dist_euclid((self.x,self.y),(self.x,y-1)) < self.dist["tailH"] or self.dist["tailH"] == False :
						self.dist["tailH"] = dist_euclid((self.x,self.y),(self.x,y-1))
						continue
				elif y-1 > self.y :
					if dist_euclid((self.x,self.y),(self.x,y-1)) < self.dist["tailB"] or self.dist["tailB"] == False :
						self.dist["tailB"] = dist_euclid((self.x,self.y),(self.x,y-1))
						continue
			if (self.x,y-1) == self.food :
				if y-1 < self.y :
					self.dist["foodH"] = dist_euclid((self.x,self.y),(self.x,y-1))
					continue
				elif x-1 > self.x :
					self.dist["foodB"] = dist_euclid((self.x,self.y),(self.x,y-1))

		print(f"""   {self.dist["wallH"]}
{self.dist["wallG"]} | {self.dist["wallD"]}
   {self.dist["wallB"]} """)


fen = Tk()
 
can = Canvas(fen,height=map_size[1]*block_size[0], width=map_size[0]*block_size[1])
can.pack()
snake = Snake(can,appende=append,lene=lene)
 
def Update():
	global snake,can
	if not snake.finish :
		quit()
	if snake.game :
		snake.update()
		snake.entree_ai()
	can.after(100,Update)
 
def Up(event) :
	global snake
	if snake.direction != "down":
		snake.direction = "up"
def Down(event) :
	global snake
	if snake.direction != "up":
		snake.direction = "down"
def Right(event) :
	global snake
	if snake.direction != "left":
		snake.direction = "right"
def Left(event) :
	global snake
	if snake.direction != "right":
		snake.direction = "left"
def Start(event):
	global snake
	if not snake.game :
		snake.game = True
	else :
		snake.game = False
 
fen.bind("<Up>",Up)
fen.bind("<Down>",Down)
fen.bind("<Left>",Left)
fen.bind("<Right>",Right)
fen.bind("<space>",Start)
 
Update()
 
fen.mainloop()