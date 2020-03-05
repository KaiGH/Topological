from tkinter import ttk, filedialog, Label, Frame, W, Entry, E, Canvas, NW
from PIL import Image as PILImage,ImageTk
import tkinter as tk
import yaml
import copy

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.mapPath = ""
        self.tmapPath = ""

        container = tk.Frame(self)
        container.grid(row=0,column=0, sticky="nsew")

        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)

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
        YAML=Label(self, width= 50, text ="Insert YAML File Path")
        Map =Label(self, width= 50, text = "Insert Map File Path")
        #positioning of text label
        YAML.grid(row=3, column=0)
        Map.grid(row=3, column=2)  
        #declaring button
        YAMLButton = ttk.Button(self, text= "Open YAML File", command =self.YAML)
        MapButton = ttk.Button(self, text= "Open Map File",  command =self.Map)
        nextbutton = ttk.Button(self, text= "Generate", command= lambda: controller.show_frame("Edit"))
        #postioning button
        YAMLButton.grid(row=3, column=1)
        MapButton.grid(row=3, column=3)
        nextbutton.grid(row= 3, column= 4)

      
     #selecting map file
     def Map(self):
        self.filename = filedialog.askopenfilename(title = "Select A File",filetypes =[('PGM Files', '*.pgm')])
        if(self.yamlfilename == ""):
           self.yamlfilename = "/Insert Map File Path"
        self.mainGUI.mapPath = self.filename
        MapP=Label(self, width= 50, text =self.mainGUI.mapPath.split("/")[-1])
        MapP.grid(row=3, column=2)
        
    #selecting node file
     def YAML(self):
        self.yamlfilename = filedialog.askopenfilename(title = "Select A File", filetypes =[('TMAP Files', '*.tmap')])
        if(self.yamlfilename == ""):
            self.yamlfilename = "/Insert YAML File Path"
        self.mainGUI.tmapPath = self.yamlfilename
        YAMLp=Label(self, width= 50, text = self.mainGUI.tmapPath.split("/")[-1])
        YAMLp.grid(row=3, column=0)

     def onShow(self):
         return

class EditingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.mainGUI = controller
        self.header = Frame(self)
        self.header.grid(row=0, column = 1)
        self.buttons = Frame(self)
        self.buttons.grid(row = 1, column=0, sticky = W)
        FilePagebutton = ttk.Button(self.header, text ="select different files", command= lambda:controller.show_frame("Start"))
        FilePagebutton.grid()


        X=Label(self.buttons, text ="Insert X Coordinate")
        self.XEntry=Entry(self.buttons, width= 50, text ="Insert X Coordinate")
        X.grid(row=1, column=0, sticky = W)
        self.XEntry.grid(row=1, column=1, sticky = W)

        Y=Label(self.buttons, text ="Insert Y Coordinate")
        self.YEntry=Entry(self.buttons, width= 50, text ="Insert Y Coordinate")
        Y.grid(row=2, column=0, sticky = W)
        self.YEntry.grid(row=2, column=1, sticky = W)

        nodeName=Label(self.buttons, text ="Insert Node Name")
        self.nodeNameEntry=Entry(self.buttons, width= 50, text ="Insert Node Name ")
        nodeName.grid(row=3, column=0, sticky = W)
        self.nodeNameEntry.grid(row=3, column=1, sticky = W)

        AddNode = ttk.Button(self.buttons, text= "Add New Node", command = self.addNode)
        AddNode.grid(row=4, column=1, sticky = W)
        DeleteNode = ttk.Button(self.buttons, text= "Delete A Node", command = self.nodeDelete)
        DeleteNode.grid(row=4, column=1)
        EditNode = ttk.Button(self.buttons, text= "Edit A Node" , command = self.nodeEdit)
        EditNode.grid(row=4, column=1, sticky = E)

        nodeName1=Label(self.buttons, text ="Insert Starting Node Name")
        self.nodeName1Entry=Entry(self.buttons, width= 50, text ="Insert Starting Node Name ")
        nodeName1.grid(row=5, column=0, sticky = W)
        self.nodeName1Entry.grid(row=5, column=1, sticky = W)

        nodeName2=Label(self.buttons, text ="Insert Destination Node Name")
        self.nodeName2Entry=Entry(self.buttons, width= 50, text ="Insert Destination Node Name ")
        nodeName2.grid(row=6, column=0, sticky = W)
        self.nodeName2Entry.grid(row=6, column=1, sticky = W)

        AddPath = ttk.Button(self.buttons, text= "Add Path" , command = self.pathAdd)
        AddPath.grid(row=7, column=1, sticky = W, padx=40)

        DeletePath = ttk.Button(self.buttons, text= "Delete Path" , command = self.pathDelete)
        DeletePath.grid(row=7, column=1, sticky = E, padx=40)
        save = ttk.Button(self.buttons, text= "Save", command = self.mapSave)
        save.grid(row=8, column=1)



        #Opening the Yaml File to Print out the Contents
    def readYaml(self, filename):
        with open(filename) as fileReader:
            node_coords = yaml.load(fileReader, Loader=yaml.FullLoader)
            return (node_coords)      

    def nodeDelete(self):
        #nodeList = self.readYaml(self.mainGUI.tmapPath)
        nodeName = self.nodeNameEntry.get()
        print(self.nodeNameEntry.get())
        #Searches from the First to the Last Node
        for index in range(len(self.nodeList)):      
        #If the Node Matches with the Inputted Node
          if self.nodeList[index]["meta"]["node"] == nodeName:
              #Deletes Node
              del(self.nodeList[index])
              #stream = open(self.mainGUI.tmapPath, 'w')   
              #yaml.dump(self.nodeList, stream) 
              #stream.close()
              self.canvas.destroy()
              self.loadImage()

    def addNode(self):
        #Get User Input
        newX = self.XEntry.get()
        newY = self.YEntry.get()

        #Gets File, Takes a Node to be Used as a Template for our New Node
        #nodeList = self.readYaml(self.mainGUI.tmapPath)
        newNode = copy.deepcopy(self.nodeList[0])
        #Calls next number in sequence of nodes to define this new one
        newNumber = self.nodeNumber(self.mainGUI.tmapPath)
    
        #More attributes can be changed but I've started with node definition, name, x and y
        newNode["meta"]["node"] = "WayPoint"+str(newNumber)
        newNode["node"]["name"] = "WayPoint"+str(newNumber)
        newNode["node"]["pose"]["position"]["x"] = newX
        newNode["node"]["pose"]["position"]["y"] = newY
    
        #Appends new node to rest of the file then dumps into file
        self.nodeList.append(newNode)
        #stream = open(self.mainGUI.tmapPath, 'w')   
        #yaml.dump(self.nodeList, stream) 
        #stream.close()
        self.canvas.destroy()
        self.loadImage()

    def nodeEdit(self):
        #nodeList = self.readYaml(self.mainGUI.tmapPath)
        nodeName = self.nodeNameEntry.get()
        newX = self.XEntry.get()
        newY = self.YEntry.get()
    
        #Searches from the First to the Last Node
        for index in range(len(self.nodeList)):     
        #If the Node Matches with the Inputted Node
          if self.nodeList[index]["meta"]["node"] == nodeName:
              #Changing Variables to Match User Input
              self.nodeList[index]["node"]["pose"]["position"]["x"] = newX
              self.nodeList[index]["node"]["pose"]["position"]["y"] = newY    
              #Opens "write" Stream 
              #stream = open(self.mainGUI.tmapPath, 'w')
              ##Dumps New Yaml Data into File
              #yaml.dump(self.nodeList, stream) 
              #stream.close()
              self.canvas.destroy()
              self.loadImage()
              
    def nodeNumber(self, filename):
        #searches all "WayPoint" data and takes the numbers from the ends of those strings
        numbers = [int(node["meta"]["node"][8:]) for node in self.nodeList]
        #puts numbers in order
        numbers.sort()
        #returns the next number in sequence
        return numbers[-1] + 1

    def nodeCoords(self, filename):
        #returns all nodes that exist in file
        return [[node["node"]["pose"]["position"]["x"],node["node"]["pose"]["position"]["y"], node["meta"]["node"]]for node in self.nodeList]

    def pathNums(self,filename):
        #nodeList = self.readYaml(filename)
        paths = []
        for i in range(len(self.nodeList)):     
            for j in range(len(self.nodeList[i]["node"]["edges"])):
                path = self.nodeList[i]["node"]["edges"][j]["edge_id"]
                paths.append([[path[:path.index("_")]], [path[path.index("_")+1:]]])
        return paths

    def pathAdd(self):
        #nodeList = self.readYaml(self.mainGUI.tmapPath)
        nodeName1 = self.nodeName1Entry.get()
        nodeName2 = self.nodeName2Entry.get()
        newPath = copy.deepcopy(self.nodeList[1]["node"]["edges"][0])
        newPath["edge_id"] = nodeName1 + "_" + nodeName2
        newPath["node"] = nodeName1

        for index in range(len(self.nodeList)):
            if nodeName1 == self.nodeList[index]["meta"]["node"]:
                self.nodeList[index]["node"]["edges"].append(newPath)
                #stream = open(self.mainGUI.tmapPath, 'w')   
                #yaml.dump(self.nodeList, stream) 
                #stream.close()
                self.canvas.destroy()
                self.loadImage()

    def pathDelete(self):
        #nodeList = self.readYaml(self.mainGUI.tmapPath)
        nodeName1 = self.nodeName1Entry.get()
        nodeName2 = self.nodeName2Entry.get()
        searchPath = nodeName1 + "_" + nodeName2      
        for i in range(len(self.nodeList)):     
            for j in range(len(self.nodeList[i]["node"]["edges"])):
                if self.nodeList[i]["node"]["edges"][j]["edge_id"] == searchPath:
                    del(self.nodeList[i]["node"]["edges"][j])
                    #stream = open(self.mainGUI.tmapPath, 'w')   
                    #yaml.dump(self.nodeList, stream) 
                    #stream.close()
                    self.canvas.destroy()
                    self.loadImage()
    def mapSave(self):
        stream = open(self.mainGUI.tmapPath, 'w')   
        yaml.dump(self.nodeList, stream) 
        stream.close()

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
            #print(F"Plotting point {point[2][8:]}")
            self.draw_point(point[0], point[1], 0.05, point[2][8:])

    def loadImage(self):
        im = PILImage.open(self.mainGUI.mapPath)
        self.SCALE = 3
        self.ORIGIN = (-31.45, -12.45)
        self.width, self.height = im.size
        self.canvas = Canvas(self, width=self.width/self.SCALE, height = self.height/self.SCALE)
        self.canvas.grid(row = 1, column=1,sticky = E, padx=40)  
        image2=im.resize((int(self.width/self.SCALE),int(self.height/self.SCALE)),PILImage.ANTIALIAS)
        picture=ImageTk.PhotoImage(image2)
        label = Label(image=picture)
        label.image = picture # keep a reference!
        label.grid(row = 1, column=1, sticky = E, padx=40)
        label.grid_forget()
        self.canvas.create_image(0,0, anchor=NW, image=picture) 
        self.drawingWayPoints()

    def draw_line(self, a, b, scale):
        newAX, newAY =  (((float(a[0])-float(self.ORIGIN[0]))/scale)/self.SCALE), (self.height/self.SCALE)- (((float(a[1])-float(self.ORIGIN[1]))/scale)/self.SCALE)
        newBX, newBY =  (((float(b[0])-float(self.ORIGIN[0]))/scale)/self.SCALE), (self.height/self.SCALE)- (((float(b[1])-float(self.ORIGIN[1]))/scale)/self.SCALE)
        self.canvas.create_line(newAX, newAY, newBX, newBY)

    def draw_point(self, x, y, scale, label):
        x = float(x)
        y = float(y)
        newX, newY =  (((x-self.ORIGIN[0])/scale)/self.SCALE), (self.height/self.SCALE)- (((y-self.ORIGIN[1])/scale)/self.SCALE)
        radius = 7.5
        self.canvas.create_oval(newX - radius, newY - radius, newX + radius, newY + radius, fill = 'blue')
        self.canvas.create_text(newX, newY, text = label, font=("Courier", 6), fill='white')



    def onShow(self):
        self.nodeList = self.readYaml(self.mainGUI.tmapPath)
        self.loadImage()



#sets instance of GUI
app = GUI()
#main loops GUI instance
app.mainloop()
