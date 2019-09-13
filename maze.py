from tkinter import *
import tkinter.messagebox
from map import Map
from robot import Robot
from threading import Thread
import time

x = input("your password to initialise it")
map = Map(x)
robot = Robot(fakeRun=True, fakeMap = map)

class Maze:
        def __init__(self, parent):
                self.margin = 30
                self.pixel_width = 500
                self.canvas = Canvas(parent, width = self.pixel_width + 2 * self.margin,
                                                                         height = self.pixel_width + 2 * self.margin)
                self.canvas.pack(side = TOP)

                self.button_solve = Button(parent, text = 'Coverage Limited Algorithm', pady = 3)
                self.button_solve.pack(side = RIGHT)
                self.button_solve.bind("<Button-1>", self.coverage_limited_expl)

                self.button_solve = Button(parent, text = 'Fastest Path', pady = 3)
                self.button_solve.pack(side = RIGHT)
                self.button_solve.bind("<Button-1>", self.fastest_expl)

                self.button_solve = Button(parent, text = 'Create robot', pady = 3)
                self.button_solve.pack(side = RIGHT)
                self.button_solve.bind("<Button-1>", self.create_robot)
                
                self.button_solve = Button(parent, text = 'Exploration Algorithm', pady = 3)
                self.button_solve.pack(side = RIGHT)
                self.button_solve.bind("<Button-1>", self.robot_movement)

                self.button_random = Button(parent, text = 'Load Map', pady = 3)
                self.button_random.pack(side = RIGHT)
                self.button_random.bind("<Button-1>", self.actual_loading)

                self.button_random = Button(parent, text = 'Time Limited Algorithm', pady = 3)
                self.button_random.pack(side = RIGHT)
                self.button_random.bind("<Button-1>", self.timealgo)

                self.button_random = Button(parent, text = 'Steps per second', pady = 3)
                self.button_random.pack(side = RIGHT)
                self.button_random.bind("<Button-1>", self.robotspeed)

                self.button_random = Button(parent, text = 'Real explore', pady = 3)
                self.button_random.pack(side = RIGHT)
                self.button_random.bind("<Button-1>", self.realexplore)


                self.m = {}
                self.rev_m = {}

        def timealgo(self,event):
                root.title('Say a time')
                heading = Label(root, text = "Enter the time limit in minutes and seconds").place(x=30,y=40)
                floatme = IntVar()
                floatentry = Entry(root, textvariable = floatme, width=25)
                floatentry.place(x=10,y =60)
                def do_it():
                        answer = str(floatme.get())
                        wow = int(answer)
                        robot.explore(timer = wow, exploreLimit = None)
                        self.update_map(self)
                work = Button(root, text ="submit", width=10, height=1,command = do_it)
                work.place(x=40, y=85)

        def robotspeed(self,event):
                root.title('Set the robot speed')
                heading = Label(root, text = "Enter the robot speed").place(x=30,y=40)
                floatme = IntVar()
                floatentry = Entry(root, textvariable = floatme, width=25)
                floatentry.place(x=10,y =60)
                def do_it():
                        answer = str(floatme.get())
                        wow = int(answer)
                        robot.coordinator.stepsPerSec = wow
                        robot.explore()
                        self.update_map(self)
                work = Button(root, text ="submit", width=10, height=1,command = do_it)
                work.place(x=40, y=85)

        def actual_loading(self,event):
                root.title('Select the text file')
                heading = Label(root, text = "enter the text file").place(x=30,y=40)
                floatme = StringVar()
                floatentry = Entry(root, textvariable = floatme, width=25)
                floatentry.place(x=10,y =60)
                def do_it():
                        answer = str(floatme.get())
                        map = Map(answer)
                        try:
                                map= Map()
                                ncell=20
                                self.canvas.focus_set()
                                cellsize = self.pixel_width/ncell
                                self.maze = [[0] * ncell for x in range(ncell)]
                                for i in range(15):
                                        for j in range(0,20):
                                                pos=[i,j]
                                        #None=unexplored, 0=explored, no obstacle, 1= obstacle, has obstacle
                                                if pos ==[0,1]:
                                                        self.draw_cell(i,j,cellsize, color = 'red')
                                                elif pos ==[0,0]:
                                                        self.draw_cell(i,j,cellsize, color = 'red')
                                                elif pos ==[0,2]:
                                                        self.draw_cell(i,j,cellsize, color = 'red')
                                                elif pos ==[1,0]:
                                                        self.draw_cell(i,j,cellsize, color = 'red')
                                                elif pos ==[1,1]:
                                                        self.draw_cell(i,j,cellsize, color = 'red')
                                                elif pos ==[1,2]:
                                                        self.draw_cell(i,j,cellsize, color = 'red')
                                                elif pos ==[2,0]:
                                                        self.draw_cell(i,j,cellsize, color = 'red')
                                                elif pos ==[2,1]:
                                                        self.draw_cell(i,j,cellsize, color = 'red')
                                                elif pos ==[2,2]:
                                                        self.draw_cell(i,j,cellsize, color = 'red')
                                                elif pos ==[14,19]:
                                                        self.draw_cell(i,j,cellsize, color = 'yellow')
                                                elif pos ==[14,18]:
                                                        self.draw_cell(i,j,cellsize, color = 'yellow')
                                                elif pos ==[14,17]:
                                                        self.draw_cell(i,j,cellsize, color = 'yellow')
                                                elif pos ==[13,19]:
                                                        self.draw_cell(i,j,cellsize, color = 'yellow')
                                                elif pos ==[13,18]:
                                                        self.draw_cell(i,j,cellsize, color = 'yellow')
                                                elif pos ==[13,17]:
                                                        self.draw_cell(i,j,cellsize, color = 'yellow')
                                                elif pos ==[12,19]:
                                                        self.draw_cell(i,j,cellsize, color = 'yellow')
                                                elif pos ==[12,18]:
                                                        self.draw_cell(i,j,cellsize, color = 'yellow')
                                                elif pos ==[12,17]:
                                                        self.draw_cell(i,j,cellsize, color = 'yellow')
                                                elif map.getTile(pos) == None:
                                                        self.draw_cell(i,j,cellsize, color = 'purple')
                                                elif map.getTile(pos) == 0:
                                                        self.draw_cell(i,j,cellsize, color = 'blue')
                                                elif map.getTile(pos) == 1:
                                                        self.draw_cell(i,j,cellsize, color = 'black')
                

                        except:
                                pass
                work = Button(root, text ="submit", width=10, height=1,command = do_it)
                work.place(x=40, y=85)

                
                
        def loadmap(self):
                
                try:
                        map = robot.map
                        ncell=20
                        self.canvas.focus_set()
                        cellsize = self.pixel_width/ncell
                        self.maze = [[0] * ncell for x in range(ncell)]
                        for i in range(15):
                                for j in range(0,20):
                                        pos=[i,j]
                                        #None=unexplored, 0=explored, no obstacle, 1= obstacle, has obstacle
                                        if pos ==[0,1]:
                                                self.draw_cell(i,j,cellsize, color = 'red')
                                        elif pos ==[0,0]:
                                                self.draw_cell(i,j,cellsize, color = 'red')
                                        elif pos ==[0,2]:
                                                self.draw_cell(i,j,cellsize, color = 'red')
                                        elif pos ==[1,0]:
                                                self.draw_cell(i,j,cellsize, color = 'red')
                                        elif pos ==[1,1]:
                                                self.draw_cell(i,j,cellsize, color = 'red')
                                        elif pos ==[1,2]:
                                                self.draw_cell(i,j,cellsize, color = 'red')
                                        elif pos ==[2,0]:
                                                self.draw_cell(i,j,cellsize, color = 'red')
                                        elif pos ==[2,1]:
                                                self.draw_cell(i,j,cellsize, color = 'red')
                                        elif pos ==[2,2]:
                                                self.draw_cell(i,j,cellsize, color = 'red')
                                        elif pos ==[14,19]:
                                                self.draw_cell(i,j,cellsize, color = 'yellow')
                                        elif pos ==[14,18]:
                                                self.draw_cell(i,j,cellsize, color = 'yellow')
                                        elif pos ==[14,17]:
                                                self.draw_cell(i,j,cellsize, color = 'yellow')
                                        elif pos ==[13,19]:
                                                self.draw_cell(i,j,cellsize, color = 'yellow')
                                        elif pos ==[13,18]:
                                                self.draw_cell(i,j,cellsize, color = 'yellow')
                                        elif pos ==[13,17]:
                                                self.draw_cell(i,j,cellsize, color = 'yellow')
                                        elif pos ==[12,19]:
                                                self.draw_cell(i,j,cellsize, color = 'yellow')
                                        elif pos ==[12,18]:
                                                self.draw_cell(i,j,cellsize, color = 'yellow')
                                        elif pos ==[12,17]:
                                                self.draw_cell(i,j,cellsize, color = 'yellow')
                                        elif map.getTile(pos) == None:
                                                self.draw_cell(i,j,cellsize, color = 'purple')
                                        elif map.getTile(pos) == 0:
                                                self.draw_cell(i,j,cellsize, color = 'blue')
                                        elif map.getTile(pos) == 1:
                                                self.draw_cell(i,j,cellsize, color = 'black')
                        

                except:
                        pass

                
        def draw_cell(self, i, j, cellsize, color = ''):
                x1 = self.margin + i * cellsize
                y1 = self.margin + j * cellsize
                x2 = x1 + cellsize
                y2 = y1 + cellsize
                index = self.canvas.create_rectangle(x1, y1, x2, y2, fill = color)
                self.m[index] = (i, j)
                self.rev_m[(i, j)] = index

                                        
        def draw_maze(self, ncell):
                cellsize = self.pixel_width/ncell
                self.maze = [[0] * ncell for x in range(ncell)]
                for i in range(15):
                        for j in range(0,20):
                                self.draw_cell(i, j, cellsize)
                                
        def create_robot(self, event, i = robot.pos[0], j = robot.pos[1], cellsize = 25, color = 'purple'):
                x1 = self.margin + i * cellsize
                y1 = self.margin + j * cellsize
                x2 = x1 + cellsize
                y2 = y1 + cellsize
                index = self.canvas.create_oval(x1, y1, x2, y2, fill = color)

                if robot.orientation ==0:
                        bottom1 = self.canvas.create_rectangle(x1,y1, x2, y2-50, fill = 'black')
                        top1 = self.canvas.create_rectangle(x1,y1 +25, x2, y2+25, fill ='green')
                        left1 = self.canvas.create_rectangle(x1,y1, x2-50, y2, fill ='indigo')
                        right1 = self.canvas.create_rectangle(x1 + 25,y1, x2 + 25, y2, fill ='deep pink')

                elif robot.orientation ==1:
                        top1 = self.canvas.create_rectangle(x1,y1, x2-50, y2, fill ='green') #left1
                        bottom1 = self.canvas.create_rectangle(x1 + 25,y1, x2 + 25, y2, fill = 'black') #right1
                        right1 = self.canvas.create_rectangle(x1,y1 +25, x2, y2+25, fill ='deep pink')#top1
                        left1 = self.canvas.create_rectangle(x1,y1, x2, y2-50, fill ='indigo') #bottom1
                                             
                elif robot.orientation ==2:
                        top1 = self.canvas.create_rectangle(x1,y1, x2, y2-50, fill ='green') #bottom1
                        bottom1 = self.canvas.create_rectangle(x1,y1 +25, x2, y2+25, fill = 'black') #top1
                        right1 = self.canvas.create_rectangle(x1,y1, x2-50, y2, fill ='deep pink') #left1
                        left1 = self.canvas.create_rectangle(x1 + 25,y1, x2 + 25, y2, fill ='indigo') #right1
                elif robot.orientation ==3:
                        top1 = self.canvas.create_rectangle(x1 + 25,y1, x2 + 25, y2, fill ='green') #right1
                        bottom1 = self.canvas.create_rectangle(x1,y1, x2-50, y2, fill = 'black') #left1
                        right1 = self.canvas.create_rectangle(x1,y1, x2, y2-50, fill ='deep pink') #bottom1
                        left1 = self.canvas.create_rectangle(x1,y1 +25, x2, y2+25, fill ='indigo')#top1
                        
                        
                
        def robot_movement(self, event):
                robot.explore()
                self.update_map(event)


        def update_robotpos(self,event):
                self.create_robot(event, i = robot.pos[0], j = robot.pos[1], cellsize = 25, color = 'purple')

                
        def update_map(self,event):
                next_map = []
                next_map = robot.updatemap()
                self.loadmap()
                self.update_robotpos(event)


        def fastest_expl(self,event):
                robot.findpath()
                
        def coverage_limited_expl(self,event):
                root.title('Popup Question!')
                heading = Label(root, text = "Enter the coverage %").place(x=30,y=10)
                floatme = DoubleVar()
                floatentry = Entry(root, textvariable = floatme, width=25)
                floatentry.place(x=10,y =35)
                def do_it():
                        answer = str(floatme.get())
                        wow = float(answer)
                        robot.explore(timer=None, exploreLimit = wow)
                        self.update_map(self)
                work = Button(root, text ="submit", width=10, height=1,command = do_it)
                work.place(x=40, y=60)
                
        def mapGUI(self,robot):
                time.sleep(1)
                self.update_map(self)
                
        def realexplore(self, event):
                
                t1 = Thread(target = self.robot_movement(event), args = (None))
                t2 = Thread(target = self.mapGUI(self), args = (robot, event))

                t1.start()
                t2.start()

                t1.join()
                t2.join()

if __name__ == '__main__':
        root = Tk()
        maze = Maze(root)
        myCanvas = Canvas(root)
        myCanvas.pack()
        maze.draw_maze(20)
        root.mainloop()







   
  
           
