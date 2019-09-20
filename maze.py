from tkinter import *
import tkinter.messagebox
from map import Map
from robot import Robot
from threading import Thread
import time
import PIL
from PIL import Image, ImageTk

map = Map("sweet3.txt")
robot = Robot(fakeRun=True, fakeMap = map)
UPDATE_RATE = 1000

class Maze(tkinter.Frame):
        def __init__(self, parent):
                super(Maze, self).__init__()
        
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

                self.button_random = Button(parent, text = 'Load Map', pady = 3)
                self.button_random.pack(side = RIGHT)
                self.button_random.bind("<Button-1>", self.actual_loading)

                self.button_random = Button(parent, text = 'Time Limited Algorithm', pady = 3)
                self.button_random.pack(side = RIGHT)
                self.button_random.bind("<Button-1>", self.timealgo)

                self.button_random = Button(parent, text = 'Steps per second', pady = 3)
                self.button_random.pack(side = RIGHT)
                self.button_random.bind("<Button-1>", self.robotspeed)

                self.button_random = Button(parent, text = 'Explore the arena', pady = 3)
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
                        self.realexplore2(event,wow)
                        
                work = Button(root, text ="submit", width=10, height=1,command = do_it)
                work.place(x=40, y=85)



        def actual_loading(self,event):
                root.title('Select the text file')
                heading = Label(root, text = "enter the text file").place(x=30,y=40)
                floatme = StringVar(value="")
                floatentry = Entry(root, textvariable = floatme, width=25)
                floatentry.place(x=10,y =60)
                def do_it():
                        answer = str(floatme.get())
                        map = Map(answer)
                        try:
                                map = Map()
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
                                                self.draw_cell(i,j,cellsize, color = 'white')
                                        elif map.getTile(pos) == 1:
                                                self.draw_cell(i,j,cellsize, color = 'black')
                        

                except:
                        pass

                
        def draw_cell(self, i, j, cellsize, color = ''):
                j = 19 - j
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
                        for j in reversed (range(0,20)):
                                self.draw_cell(i, j, cellsize)
                                
        def create_robot(self, event, i = robot.pos[0], j = robot.pos[1], cellsize = 25, color = 'purple'):
                j = 19 - j
                x1 = self.margin + i * cellsize
                y1 = self.margin + j * cellsize
                x2 = x1 + cellsize
                y2 = y1 + cellsize
                index = self.canvas.create_oval(x1, y1, x2, y2, fill = color)

                if robot.orientation ==0:
                        bottom1 = self.canvas.create_rectangle(x1,y1, x2, y2-50, fill = 'bisque2')
                        self.canvas.create_text(x1, y1-10, anchor=W, font=("Purisa", 8), text="Head")
                        top1 = self.canvas.create_rectangle(x1,y1 +25, x2, y2+25, fill ='green')
                        left1 = self.canvas.create_rectangle(x1,y1, x2-50, y2, fill ='indigo')
                        right1 = self.canvas.create_rectangle(x1 + 25,y1, x2 + 25, y2, fill ='deep pink') #the orientation is tilted

                elif robot.orientation ==1:
                        top1 = self.canvas.create_rectangle(x1,y1, x2-50, y2, fill ='green') #left1
                        bottom1 = self.canvas.create_rectangle(x1 + 25,y1, x2 + 25, y2, fill = 'bisque2') #right1
                        self.canvas.create_text(x1, y1, anchor=W, font=("Purisa", 8), text="Head")
                        right1 = self.canvas.create_rectangle(x1,y1 +25, x2, y2+25, fill ='deep pink')#top1
                        left1 = self.canvas.create_rectangle(x1,y1, x2, y2-50, fill ='indigo') #bottom1
                                             
                elif robot.orientation ==2:
                        top1 = self.canvas.create_rectangle(x1,y1, x2, y2-50, fill ='green') #bottom1
                        bottom1 = self.canvas.create_rectangle(x1,y1 +25, x2, y2+25, fill = 'bisque2') #top1
                        self.canvas.create_text(x1, y1+25, anchor=W, font=("Purisa", 8), text="Head")
                        right1 = self.canvas.create_rectangle(x1,y1, x2-50, y2, fill ='deep pink') #left1
                        left1 = self.canvas.create_rectangle(x1 + 25,y1, x2 + 25, y2, fill ='indigo') #right1
                elif robot.orientation ==3:
                        top1 = self.canvas.create_rectangle(x1 + 25,y1, x2 + 25, y2, fill ='green') #right1
                        bottom1 = self.canvas.create_rectangle(x1,y1, x2-50, y2, fill = 'bisque2') #left1
                        self.canvas.create_text(x1, y1, anchor=W, font=("Purisa", 8), text="Head")
                        right1 = self.canvas.create_rectangle(x1,y1, x2, y2-50, fill ='deep pink') #bottom1
                        left1 = self.canvas.create_rectangle(x1,y1 +25, x2, y2+25, fill ='indigo')#top1
                        
                        

        def update_robotpos(self,event):
                self.create_robot(event, i = robot.pos[0], j = robot.pos[1], cellsize = 25, color = 'purple')

                
        def update_map(self,event):
                self.loadmap()
                self.update_robotpos(event)



                
        def coverage_limited_expl(self,event):
                root.title('Popup Question!')
                heading = Label(root, text = "Enter the coverage %").place(x=30,y=10)
                floatme = DoubleVar()
                floatentry = Entry(root, textvariable = floatme, width=25)
                floatentry.place(x=10,y =35)
                def do_it():
                        answer = str(floatme.get())
                        wow = float(answer)
                        self.realexplore1(event,wow)

                work = Button(root, text ="submit", width=10, height=1,command = do_it)
                work.place(x=40, y=60)

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
                        self.realexplore(event)
                        
                work = Button(root, text ="submit", width=10, height=1,command = do_it)
                work.place(x=40, y=85)
                
        def mapGUI(self,robot):
                self.update_map(self)

        def realexplore1(self, event, wow):
                self.updater()
                
                t1 = Thread(target=robot.explore, args=(None, wow))
                
                t1.start()

        def realexplore2(self, event, wow):
                self.updater()
                
                t1 = Thread(target=robot.explore, args=(wow,))
                
                t1.start()
                
        def realexplore(self, event):
                self.updater()
                
                t1 = Thread(target=robot.explore, args=(None,))
                
                t1.start()

        def fastest_expl(self,event):
                self.updater()
                t1 = Thread(target=robot.findpath, args=(None,))
                t1.start()
                
        def updater(self):
                self.mapGUI(self)
                self.after(UPDATE_RATE, self.updater)

if __name__ == '__main__':
        root = Tk()
        maze = Maze(root)
        myCanvas = Canvas(root)
        myCanvas.pack()
        maze.draw_maze(20)
        root.mainloop()
