from tkinter import ttk
from tkinter import filedialog
from PIL import Image as PILImage,ImageTk
import tkinter as tk
from tkinter import *
import yaml

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.mapPath = ""
        self.tmapPath = ""

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["Start"] = StartPage(container, self)
        self.frames["Edit"] = EditingPage(container, self)
        self.frames["Start"].grid(row=0,column=0, sticky="nsew")
        self.frames["Edit"].grid(row=0,column=0, sticky="nsew")

        self.show_frame("Start")

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        frame.onShow()

class StartPage(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.mainGUI = controller
        
        #inserted text label
        YAML=Label(self, width= 50, text ="insert YAML file path")
        Map =Label(self, width= 50, text = "insert Map file path")
        #positioning of text label
        YAML.grid(row=3, column=1)
        Map.grid(row=3, column=3)  
        #declaring button
        YAMLButton = ttk.Button(self, text= "Open YAML File", command =self.YAML)
        MapButton = ttk.Button(self, text= "Open Map File",  command =self.Map)
        nextbutton = ttk.Button(self, text= "Generate", command= lambda: controller.show_frame("Edit"))
        #postioning button
        YAMLButton.grid(row=3, column=2)
        MapButton.grid(row=3, column=4)
        nextbutton.grid(row= 3, column= 8 )
       
     def Map(self):
        self.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
        (("Map file","*.PGM"),("all files","*.*")))
        self.mainGUI.mapPath = self.filename
        MapP=Label(self, text =self.mainGUI.mapPath)
        MapP.grid(row=3, column=3)
        

     def YAML(self):
        self.yamlfilename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =
        (("TMAP","*.tmap"),("Yaml file","*.Yaml"),("all files","*.*")))
        self.mainGUI.tmapPath = self.yamlfilename
        YAMLp=Label(self, width= 50, text = self.mainGUI.tmapPath)
        YAMLp.grid(row=3, column=1)

     def onShow(self):
         return

class EditingPage(tk.Frame):
    def adding(self):
        with open(YamlPath) as rf:
            node_coords = yaml.load(rf, Loader=yaml.FullLoader)
        for nodes in node_coords:
                print(nodes["name"])
                node = nodes["name"].split('_')
                nodeNum = int(node[1])
                nodeNum = nodeNum + 1    
                
    def Editing(self):
        with open (YamlPath) as ef:
            node_coords = yaml.load(ef, Loader=yaml.FullLoader)
            node = Nodename.get
            NewX = X.get
            NewY = Y.get
        for nodes in node_coords:
            if nodes["name"] == node:
                nodes["x"] = NewX
                nodes["y"] = NewY
        with open("test.yaml", "w") as wf:
            yaml.dump(node_coords, wf)

    #Opening the Yaml File to Print out the Contents
    def readYaml(self, filename):
        with open(filename) as fileReader:
            node_coords = yaml.load(fileReader, Loader=yaml.FullLoader)
            return (node_coords)

    def nodeCoords(self, filename):
       #Recieves file data from read function
        data = self.readYaml(filename)
        #returns all nodes that exist in file
        return [[node["node"]["pose"]["position"]["x"],node["node"]["pose"]["position"]["y"], node["meta"]["node"]]for node in data]

    def pathNums(self,filename):
        nodeList = self.readYaml(filename)
        paths = []
        for i in range(len(nodeList)):     
            for j in range(len(nodeList[i]["node"]["edges"])):
                path = nodeList[i]["node"]["edges"][j]["edge_id"]
                paths.append([[path[:path.index("_")]], [path[path.index("_")+1:]]])
        return paths


    def drawingWayPoints(self):
        points = self.nodeCoords(self.mainGUI.tmapPath)
        paths = self.pathNums(self.mainGUI.tmapPath)

        for path in paths: 
            pointA = path[0][0]
            pointB = path[1][0]
    
            pointACoords = None
            pointBCoords = None
            for point in points:
                if point[2] == pointA:
                    pointACoords = [point[0], point[1]]
                if point[2] == pointB:
                    pointBCoords = [point[0], point[1]]
            if(pointACoords != None and pointBCoords != None):
                self.draw_line(pointACoords, pointBCoords, 0.05)
        for point in points:
            print(F"Plotting point {point[2][8:]}")
            self.draw_point(point[0], point[1], 0.05, point[2][8:])

    def loadImage(self):
        
        im = PILImage.open(self.mainGUI.mapPath)
        self.SCALE = 3
        self.ORIGIN = (-31.45, -12.45)
        self.width, self.height = im.size
        self.canvas = Canvas(self, width=self.width/self.SCALE, height = self.height/self.SCALE)
        self.canvas.pack()      
        image2=im.resize((int(self.width/self.SCALE),int(self.height/self.SCALE)),PILImage.ANTIALIAS)
        riseholme2=ImageTk.PhotoImage(image2)
        label = Label(image=riseholme2)
        label.image = riseholme2 # keep a reference!
        label.pack()
        label.pack_forget()
        self.canvas.create_image(0,0, anchor=NW, image=riseholme2) 
        self.drawingWayPoints()

    def draw_line(self, a, b, scale):
        newAX, newAY =  (((a[0]-self.ORIGIN[0])/scale)/self.SCALE), (self.height/self.SCALE)- (((a[1]-self.ORIGIN[1])/scale)/self.SCALE)
        newBX, newBY =  (((b[0]-self.ORIGIN[0])/scale)/self.SCALE), (self.height/self.SCALE)- (((b[1]-self.ORIGIN[1])/scale)/self.SCALE)
        self.canvas.create_line(newAX, newAY, newBX, newBY)

    def draw_point(self, x, y, scale, label):
        newX, newY =  (((x-self.ORIGIN[0])/scale)/self.SCALE), (self.height/self.SCALE)- (((y-self.ORIGIN[1])/scale)/self.SCALE)
        radius = 7.5
        self.canvas.create_oval(newX - radius, newY - radius, newX + radius, newY + radius, fill = 'blue')
        self.canvas.create_text(newX, newY, text = label, font=("Courier", 6), fill='white')



    def onShow(self):
        self.loadImage()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.mainGUI = controller
        FilePagebutton = ttk.Button(self, text ="select different files", command= lambda:controller.show_frame("Start"))
        FilePagebutton.pack()

        X=Label(self, width= 50, text ="Insert X Corodinate")
        XEntry=Entry(self, width= 50, text ="Insert X Corodinate")
        X.pack()
        XEntry.pack()

        Y=Label(self, width= 50, text ="Insert Y Corodinate")
        YEntry=Entry(self, width= 50, text ="Insert Y Coordinate")
        Y.pack()
        YEntry.pack()

        nodeName=Label(self, width= 50, text ="Insert Node Name")
        nodeNameEntry=Entry(self, width= 50, text ="Insert Node Name ")
        nodeName.pack()
        nodeNameEntry.pack()

        nodeName1=Label(self, width= 50, text ="Insert Starting Node Name")
        nodeName1Entry=Entry(self, width= 50, text ="Insert Starting Node Name ")
        nodeName1.pack()
        nodeName1Entry.pack()

        nodeName2=Label(self, width= 50, text ="Insert Destination Node Name")
        nodeName2Entry=Entry(self, width= 50, text ="Insert Destination Node Name ")
        nodeName2.pack()
        nodeName2Entry.pack()

        Add = ttk.Button(self, text= "Add New Node", command = self.adding)
        Add.pack()
        Delete = ttk.Button(self, text= "Delete A Node")
        Delete.pack()
        Edit = ttk.Button(self, text= "Edit A Node" , command = self.Editing )
        Edit.pack()
        save = ttk.Button(self, text= "Save")
        save.pack()
        

        #nodename.grid(row = 2, column =1)
        #X.grid(row = 2, column =2)
        #Y.grid(row = 2, column =3)
        #Add.grid(row = 3, column =3)
        #warning = Label(self, width= 50, text = "Going back to file selecting page will lose all work not saved")

#sets instance of GUI
app = GUI()
#main loops GUI instance
app.mainloop()
