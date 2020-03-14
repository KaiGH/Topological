from tkinter import ttk, filedialog, Label, Frame, W, Entry, E, Canvas, NW
from PIL import Image as PILImage,ImageTk
import tkinter as tk
import yaml
import copy

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #variable for file path
        self.yamlPath = ""
        self.mapPath = ""
        self.tmapPath = ""

        #intial frame all elements are stored in
        container = tk.Frame(self)
        container.grid(row=0,column=0, sticky="nsew")

        #array of frames
        self.frames = {}
        #intialises start page
        self.frames["Start"] = StartPage(container, self)
        #intialises edit page
        self.frames["Edit"] = EditingPage(container, self)
        #builds start page
        self.frames["Start"].grid(row=0,column=0, sticky="nsew")
        #builds edit page
        self.frames["Edit"].grid(row=0,column=0, sticky="nsew")

        #calls show frame method to bring start page to front
        self.show_frame("Start")

        #brings page to front
    def show_frame(self, page):
        #shows page
        frame = self.frames[page]
        #bring frame to top
        frame.tkraise()
        #sets variables
        frame.onShow()

        #start page class
class StartPage(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.mainGUI = controller
        #inserted text label for each file selection
        YAML =Label(self, width= 20, text = "Insert YAML File Path")
        TMAP=Label(self, width= 20, text ="Insert TMAP File Path")
        Map =Label(self, width= 20, text = "Insert Map File Path")
        #positioning of labels
        YAML.grid(row=3, column=0)
        TMAP.grid(row=3, column=2)
        Map.grid(row=3, column=4)  
        #declaring buttons for opening files
        YAMLButton = ttk.Button(self, text= "Open YAML File", command =self.YAML)
        TMAPButton = ttk.Button(self, text= "Open TMAP File", command =self.TMAP)
        MapButton = ttk.Button(self, text= "Open Map File",  command =self.Map)
        nextbutton = ttk.Button(self, text= "Generate", command= lambda: controller.show_frame("Edit"))
        #postioning of buttons
        YAMLButton.grid(row=3, column=1)
        TMAPButton.grid(row=3, column=3)
        MapButton.grid(row=3, column=5)
        nextbutton.grid(row= 3, column= 6)

     #selecting YAML file
     def YAML(self):
         #sets file type
        self.yamlfilename = filedialog.askopenfilename(title = "Select File",filetypes =[('YAML Files', '*.yaml')])

        #if user clicks on open file and then does not select path this will display
        if(self.yamlfilename == ""):
            self.yamlfilename = "/Insert Map File Path"
        #sets variable for yaml path for use in file
        self.mainGUI.yamlPath = self.yamlfilename
        #displays chosen file path
        YAMLP=Label(self, width= 20, text =self.mainGUI.yamlPath.split("/")[-1])
        YAMLP.grid(row=3, column=0) 

     #selecting map file
     def Map(self):
         #sets file type
        self.mapfilename = filedialog.askopenfilename(title = "Select File", filetypes =[('PGM Files', '*.pgm')])

        #if user clicks on open file and then does not select path this will display
        if(self.mapfilename == ""):
           self.mapfilename = "/Insert Map File Path"

        #sets variable for map path for use in file
        self.mainGUI.mapPath = self.mapfilename
        #displays chosen file path
        MapP=Label(self, width= 20, text =self.mainGUI.mapPath.split("/")[-1])
        MapP.grid(row=3, column=4)
        
    #selecting tmap file
     def TMAP(self):
         #sets file type
        self.tmapfilename = filedialog.askopenfilename(title = "Select A File", filetypes =[('TMAP Files', '*.tmap'),('YAML Files', '*.yaml')])
        #if user clicks on open file and then does not select path this will display
        if(self.tmapfilename == ""):
            self.tmapfilename = "/Insert TMAP File Path"
        #sets variable for map path for use in file
        self.mainGUI.tmapPath = self.tmapfilename
        #displays chosen file path
        TMAPp=Label(self, width= 20, text = self.mainGUI.tmapPath.split("/")[-1])
        TMAPp.grid(row=3, column=2)

     def onShow(self):
         return

#editing page class
class EditingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        #for page showing
        self.mainGUI = controller
        #default of image scale
        self.SCALE = 3
        #header above image container
        self.header = Frame(self)
        self.header.grid(row=0, column = 1)
        #change file button
        FilePagebutton = ttk.Button(self.header, width= 20, text ="select different files", command= lambda:controller.show_frame("Start"))
        FilePagebutton.grid()
        #footer below image container
        self.footer = Frame(self)
        self.footer.grid(row=3, column = 1)
        #button container left of image
        self.buttonContainer = Frame(self)
        self.buttonContainer.grid(row = 1, column=0)
        #container for node buttons
        self.nodeButtons = Frame(self.buttonContainer)
        self.nodeButtons.grid(row = 1, column=0)
        #blank line
        Blank1=Label(self.buttonContainer, width= 20,text ="Insert Parameters:")
        Blank1.grid(row=2, column=0)
        #container for entry boxes of node edting
        self.nodeButtonsEntry = Frame(self.buttonContainer)
        self.nodeButtonsEntry.grid(row = 3, column=0)
        #blank line
        Blank2=Label(self.buttonContainer, width= 20,text ="")
        Blank2.grid(row=5, column=0)
        #container for paths buttons
        self.pathButtons = Frame(self.buttonContainer)
        self.pathButtons.grid(row = 6, column=0)
        #container for path entry
        self.pathButtonsEntry = Frame(self.buttonContainer)
        self.pathButtonsEntry.grid(row = 8, column=0)
        #container for scale entry
        self.scaleContainer = Frame(self.buttonContainer)
        self.scaleContainer.grid(row = 12, column=0)
        #blank line
        Blank4=Label(self.buttonContainer, width= 20,text ="")
        Blank4.grid(row=9, column=0)
        #Save button
        Save = ttk.Button(self.buttonContainer, width= 20, text= "Save", command = self.mapSave)
        Save.grid(row=10, column=0)
        #blank line
        Blank5=Label(self.buttonContainer, width= 20,text ="")
        Blank5.grid(row=11, column=0)
        #scale lable, entry and button
        scaleLabel=Label(self.scaleContainer, width= 20,text ="Scale")
        self.scaleEntry=Entry(self.scaleContainer, width= 30, text ="Scale")
        scaleLabel.grid(row=0, column=0)
        self.scaleEntry.grid(row=0, column=1)
        Scale=ttk.Button(self.buttonContainer, width= 20,text ="Scale", command = self.scale)
        Scale.grid(row=13, column=0)
        #add node button
        AddNode = ttk.Button(self.nodeButtons, width= 20, text= "Add New Node", command = self.addNode)
        AddNode.grid(row=1, column=1)
        #delete node button
        DeleteNode = ttk.Button(self.nodeButtons, width= 20, text= "Delete A Node", command = self.nodeDelete)
        DeleteNode.grid(row=1, column=2)
        #edit node button
        EditNode = ttk.Button(self.nodeButtons, width= 20, text= "Edit A Node" , command = self.nodeEdit)
        EditNode.grid(row=1, column=3)
        #node name entry
        nodeName=Label(self.nodeButtonsEntry, width= 30,text ="Insert Node Name")
        self.nodeNameEntry=Entry(self.nodeButtonsEntry, width= 30, text ="Insert Node Name ")
        nodeName.grid(row=2, column=1)
        self.nodeNameEntry.grid(row=2, column=2)
        #x entry
        X=Label(self.nodeButtonsEntry, width= 30,text ="Insert X Coordinate")
        self.XEntry=Entry(self.nodeButtonsEntry, width= 30, text ="Insert X Coordinate")
        X.grid(row=3, column=1,)
        self.XEntry.grid(row=3, column=2)
        #y entry
        Y=Label(self.nodeButtonsEntry, width= 30,text ="Insert Y Coordinate")
        self.YEntry=Entry(self.nodeButtonsEntry, width= 30, text ="Insert Y Coordinate")
        Y.grid(row=4, column=1)
        self.YEntry.grid(row=4, column=2)
        #add path button
        AddPath = ttk.Button(self.pathButtons, width= 20, text= "Add Path" , command = self.pathAdd)
        AddPath.grid(row=1, column=1)
        #delete path button
        DeletePath = ttk.Button(self.pathButtons, width= 20, text= "Delete Path" , command = self.pathDelete)
        DeletePath.grid(row=1, column=2)
        #blank line
        Blank3=Label(self.buttonContainer, width= 20,text ="Insert Parameters:")
        Blank3.grid(row=7, column=0)
        #path start entry
        pathStart=Label(self.pathButtonsEntry, width= 30,text ="Insert Starting Node Name")
        self.pathStartEntry=Entry(self.pathButtonsEntry, width= 30, text ="Insert Starting Node Name ")
        pathStart.grid(row=2, column=1)
        self.pathStartEntry.grid(row=2, column=2)
        #path end entry
        pathEnd=Label(self.pathButtonsEntry, width= 30,text ="Insert Destination Node Name")
        self.pathEndEntry=Entry(self.pathButtonsEntry, width= 30, text ="Insert Destination Node Name ")
        pathEnd.grid(row=3, column=1)
        self.pathEndEntry.grid(row=3, column=2)

        #add node click button
        addNodeClick = ttk.Button(self.buttonContainer, width= 20, text= "Add Node", command = self.addNodeClick)
        addNodeClick.grid(row=14, column=0)
        #delete node click button
        deleteNodeClick = ttk.Button(self.buttonContainer, width= 20, text= "Delete Node", command = self.deleteNodeClick)
        deleteNodeClick.grid(row=15, column=0)
        #add path click button
        addPathClick = ttk.Button(self.buttonContainer, width= 20, text= "Add Path", command = self.addPathClick)
        addPathClick.grid(row=17, column=0)
        #delete path click button
        deletePathClick = ttk.Button(self.buttonContainer, width= 20, text= "Delete Path", command = self.deletePathClick)
        deletePathClick.grid(row=18, column=0)

        #Opening the Yaml File to Print out the Contents
    def readYaml(self, filename):
        #opens file
        with open(filename) as fileReader:
            #reads file into array
            node_coords = yaml.load(fileReader, Loader=yaml.FullLoader)
            #returns file
            return (node_coords)  

    def addNodeClick(self):
        #sets command type for getxy function
        self.type=1
        #binds next mouse click to event variable and sends to getxy function
        self.canvas.bind('<Button-1>', self.getxy)

    def deleteNodeClick(self):
        #sets commands type for getxy
        self.type=2
        #binds next mouse click to event variable and sends to getxy function
        self.canvas.bind('<Button-1>', self.getxy)

    def addPathClick(self):
        #sets commands type for getxy
        self.type=3
        #binds next mouse click to event variable and sends to getxy function
        self.canvas.bind('<Button-1>', self.getxy)

    def deletePathClick(self):
        #sets commands type for getxy
        self.type=4
        #binds next mouse click to event variable and sends to getxy function
        self.canvas.bind('<Button-1>', self.getxy)

    def getxy(self, event):  
        #scales x,y into map scale
        x, y = ((event.x*self.SCALE)*0.05) + self.ORIGIN[0], (self.height*0.05) - (((event.y*self.SCALE)*0.05) - self.ORIGIN[1])
        #based on type varible executes corrosponding command
        if self.type == 1:
            self.addNodeClickPlace(x, y)
        if self.type == 2:
            self.deleteNodeClickRemove(x, y)
        if self.type == 3:
            #sets first x and y variable
            self.pathx1, self.pathy1 = x,y 
            #executes a second method to get a second x and y for paths
            self.canvas.bind('<Button-1>', self.getxy2)
        if self.type == 4:
            #sets first x and y variable
            self.pathx1, self.pathy1 = x,y 
            #executes a second method to get a second x and y for paths
            self.canvas.bind('<Button-1>', self.getxy2)

    def getxy2(self, event):   
        #scales x,y into map scale
        x, y = ((event.x*self.SCALE)*0.05) + self.ORIGIN[0], (self.height*0.05) - (((event.y*self.SCALE)*0.05) - self.ORIGIN[1])
        if self.type == 3:
            #sets second x and y variable
            self.pathx2, self.pathy2 = x,y 
            #sends both xy varibles to method
            self.addPathClickPlace(self.pathx1,self.pathy1,self.pathx2,self.pathy2)

        if self.type == 4:
            #sets second x and y variable
            self.pathx2, self.pathy2 = x,y 
            #sends both xy varibles to method
            self.deletePathClickRemove(self.pathx1,self.pathy1,self.pathx2,self.pathy2)
        
    def addNodeClickPlace(self, x, y):
        #Get User Input
        newX = x
        newY = y

        #Gets File, Takes a Node to be Used as a Template for our New Node
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
        self.canvas.destroy()
        self.loadImage()
        
    def deleteNodeClickRemove(self, x ,y):
        #creates upper and lower bounds for x, y coords
        xUpper = x+1
        xLower = x-1
        yUpper = y+1
        yLower = y-1
        #searches array for coords inside of bounds
        for i in range(len(self.nodeList)): 
            if float(self.nodeList[i]["node"]["pose"]["position"]["y"])<yUpper and float(self.nodeList[i]["node"]["pose"]["position"]["y"]) > yLower and float(self.nodeList[i]["node"]["pose"]["position"]["x"])<xUpper and float(self.nodeList[i]["node"]["pose"]["position"]["x"]) > xLower:
                #deletes node
                del(self.nodeList[i])
                break
        #reloads image canvas
        self.canvas.destroy()
        self.loadImage()

    def addPathClickPlace(self, x1,y1,x2,y2):
        #creates upper and lower bounds for x, y coords
        x1Upper = x1+1
        x1Lower = x1-1
        y1Upper = y1+1
        y1Lower = y1-1
        #creates upper and lower bounds for x, y coords
        x2Upper = x2+1
        x2Lower = x2-1
        y2Upper = y2+1
        y2Lower = y2-1

        #searches array for coords inside of bounds
        for i in range(len(self.nodeList)): 
            if float(self.nodeList[i]["node"]["pose"]["position"]["y"])<y1Upper and float(self.nodeList[i]["node"]["pose"]["position"]["y"]) > y1Lower and float(self.nodeList[i]["node"]["pose"]["position"]["x"])<x1Upper and float(self.nodeList[i]["node"]["pose"]["position"]["x"]) > x1Lower:
                startNode = self.nodeList[i]["node"]["name"]
        #searches array for coords inside of bounds
        for i in range(len(self.nodeList)): 
            if float(self.nodeList[i]["node"]["pose"]["position"]["y"])<y2Upper and float(self.nodeList[i]["node"]["pose"]["position"]["y"]) > y2Lower and float(self.nodeList[i]["node"]["pose"]["position"]["x"])<x2Upper and float(self.nodeList[i]["node"]["pose"]["position"]["x"]) > x2Lower:
                endNode = self.nodeList[i]["node"]["name"]
        #creates copy of path section
        newPath = copy.deepcopy(self.nodeList[1]["node"]["edges"][0])
        #inserts name of start node
        newPath["node"] = startNode
        #adds path name to it 
        newPath["edge_id"] = startNode + "_" + endNode

        #finds start path node info and appends new path
        for index in range(len(self.nodeList)):
            if startNode == self.nodeList[index]["meta"]["node"]:
                self.nodeList[index]["node"]["edges"].append(newPath)
                break
        #destroys and reloads canvas
        self.canvas.destroy()
        self.loadImage()

    def deletePathClickRemove(self, x1,y1,x2,y2):
        #creates upper and lower bounds for x, y coords
        x1Upper = x1+1
        x1Lower = x1-1
        y1Upper = y1+1
        y1Lower = y1-1
        #creates upper and lower bounds for x, y coords
        x2Upper = x2+1
        x2Lower = x2-1
        y2Upper = y2+1
        y2Lower = y2-1
        #searches array for coords inside of bounds
        for i in range(len(self.nodeList)): 
            if float(self.nodeList[i]["node"]["pose"]["position"]["y"])<y1Upper and float(self.nodeList[i]["node"]["pose"]["position"]["y"]) > y1Lower and float(self.nodeList[i]["node"]["pose"]["position"]["x"])<x1Upper and float(self.nodeList[i]["node"]["pose"]["position"]["x"]) > x1Lower:
                startNode = self.nodeList[i]["node"]["name"]
        #searches array for coords inside of bounds
        for i in range(len(self.nodeList)): 
            if float(self.nodeList[i]["node"]["pose"]["position"]["y"])<y2Upper and float(self.nodeList[i]["node"]["pose"]["position"]["y"]) > y2Lower and float(self.nodeList[i]["node"]["pose"]["position"]["x"])<x2Upper and float(self.nodeList[i]["node"]["pose"]["position"]["x"]) > x2Lower:
                endNode = self.nodeList[i]["node"]["name"]
        #creates both combinations of each path
        searchPath = startNode + "_" + endNode  
        searchPath2 = endNode + "_" + startNode  

        #searches for path combinations
        for i in range(len(self.nodeList)):     
            for j in range(len(self.nodeList[i]["node"]["edges"])):
                if self.nodeList[i]["node"]["edges"][j]["edge_id"] == searchPath:
                    #deletes path if found
                    del(self.nodeList[i]["node"]["edges"][j])
                    break
        for i in range(len(self.nodeList)):     
            for j in range(len(self.nodeList[i]["node"]["edges"])):
                if self.nodeList[i]["node"]["edges"][j]["edge_id"] == searchPath2:
                    #deletes path if found
                    del(self.nodeList[i]["node"]["edges"][j])
                    break
        #destroys canvas then reloads
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
        #destroys canvas then reloads
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
              #destroys canvas then reloads
              self.canvas.destroy()
              self.loadImage()  

    def nodeDelete(self):
        #nodeList = self.readYaml(self.mainGUI.tmapPath)
        nodeName = self.nodeNameEntry.get()
        #Searches from the First to the Last Node
        for index in range(len(self.nodeList)):      
        #If the Node Matches with the Inputted Node
          if self.nodeList[index]["meta"]["node"] == nodeName:
              #Deletes Node
              del(self.nodeList[index])
              break
        #destroys canvas then reloads
        self.canvas.destroy()
        self.loadImage()

    def pathAdd(self):
        pathStart = self.pathStartEntry.get()
        pathEnd = self.pathEndEntry.get()
        newPath = copy.deepcopy(self.nodeList[1]["node"]["edges"][0])
        newPath["edge_id"] = pathStart + "_" + pathEnd
        newPath["node"] = pathStart

        for index in range(len(self.nodeList)):
            if pathEnd == self.nodeList[index]["meta"]["node"]:
                self.nodeList[index]["node"]["edges"].append(newPath)
                #stream = open(self.mainGUI.tmapPath, 'w')   
                #yaml.dump(self.nodeList, stream) 
                #stream.close()
                self.canvas.destroy()
                self.loadImage()

    def pathDelete(self):
        #nodeList = self.readYaml(self.mainGUI.tmapPath)
        pathStart = self.pathStartEntry.get()
        pathEnd = self.pathEndEntry.get()
        searchPath = pathStart + "_" + pathEnd 
        searchPath2 = pathEnd + "_" + pathStart
        for i in range(len(self.nodeList)):     
            for j in range(len(self.nodeList[i]["node"]["edges"])):
                if self.nodeList[i]["node"]["edges"][j]["edge_id"] == searchPath:
                    del(self.nodeList[i]["node"]["edges"][j])
                    break
        for i in range(len(self.nodeList)):     
            for j in range(len(self.nodeList[i]["node"]["edges"])):
                if self.nodeList[i]["node"]["edges"][j]["edge_id"] == searchPath2:
                    del(self.nodeList[i]["node"]["edges"][j])
                    break
        self.canvas.destroy()
        self.loadImage()



    def mapSave(self):
        stream = open(self.mainGUI.tmapPath, 'w')   
        yaml.dump(self.nodeList, stream) 
        stream.close()

    def scale(self):
        #sets scale to user entry
        self.SCALE = float(self.scaleEntry.get())
        if self.SCALE == None:
            self.SCALE = 3
        #destroys canvas then reloads
        self.canvas.destroy()
        self.loadImage()
              
    def nodeNumber(self, filename):
        #searches all "WayPoint" data and takes the numbers from the ends of those strings
        numbers = [int(node["meta"]["node"][8:]) for node in self.nodeList]
        #puts numbers in order
        numbers.sort()
        #returns the next number in sequence
        return numbers[-1] + 1

    def nodeCoords(self):
        #returns all nodes that exist in file
        return [[node["node"]["pose"]["position"]["x"],node["node"]["pose"]["position"]["y"], node["meta"]["node"]]for node in self.nodeList]

    def pathNums(self):
        #creates path array
        paths = []
        #searches for paths breaks them in two for each side of path
        for i in range(len(self.nodeList)):     
            for j in range(len(self.nodeList[i]["node"]["edges"])):
                path = self.nodeList[i]["node"]["edges"][j]["edge_id"]
                paths.append([[path[:path.index("_")]], [path[path.index("_")+1:]]])
        #returns paths
        return paths



    def drawingWayPoints(self):
        #gets all nodes
        points = self.nodeCoords()
        #gets all paths
        paths = self.pathNums()

        for path in paths: 
            #nodes that connect
            pointA = path[0][0]
            pointB = path[1][0]
            #variables for node x, y 
            pointACoords = None
            pointBCoords = None

            #assigns coords to path names
            for point in points:
                if point[2] == pointA:
                    pointACoords = [point[0], point[1]]
                if point[2] == pointB:
                    pointBCoords = [point[0], point[1]]
            #if both sides of path has coords then create path
            if(pointACoords != None and pointBCoords != None):
                self.draw_line(pointACoords, pointBCoords)


        for point in points:
            #if point exists
            if(point[0] != "" or point[1] != ""):
                #send coords and waypoint name to draw point
                self.draw_point(float(point[0]), float(point[1]), point[2][8:])


    def loadImage(self):
        #creates canvas, size of height and width with scale factor
        self.canvas = Canvas(self, width=self.width/self.SCALE, height = self.height/self.SCALE)
        #places canvas on grid
        self.canvas.grid(row = 1, column=1)  
        #resize images to scale factor
        image2=self.im.resize((int(self.width/self.SCALE),int(self.height/self.SCALE)),PILImage.ANTIALIAS)
        #makes image a tk object
        picture=ImageTk.PhotoImage(image2)
        #image reference so it can be called
        label = Label(image=picture)
        label.image = picture # keep a reference!
        label.grid(row = 1, column=1)
        label.grid_forget()
        #puts image in canvas
        self.canvas.create_image(0,0, anchor=NW, image=picture) 
        #calls the drawing of points
        self.drawingWayPoints()

    def draw_line(self, a, b):
        #scales coords to map
        newAX, newAY =  (((float(a[0])-float(self.ORIGIN[0]))/self.scale)/self.SCALE), (self.height/self.SCALE)- (((float(a[1])-float(self.ORIGIN[1]))/self.scale)/self.SCALE)
        newBX, newBY =  (((float(b[0])-float(self.ORIGIN[0]))/self.scale)/self.SCALE), (self.height/self.SCALE)- (((float(b[1])-float(self.ORIGIN[1]))/self.scale)/self.SCALE)
        #creates lines between scaled coords
        self.canvas.create_line(newAX, newAY, newBX, newBY)

    def draw_point(self, x, y, label):
        #scales coords to map
        newX, newY =  (((x - self.ORIGIN[0])/self.scale)/self.SCALE), (self.height/self.SCALE)- (((y - self.ORIGIN[1])/self.scale)/self.SCALE)
        #sets radius of point circle
        radius = 7.5
        #creates circle
        self.canvas.create_oval(newX - radius, newY - radius, newX + radius, newY + radius, fill = 'blue')
        #labels nodes
        self.canvas.create_text(newX, newY, text = label, font=("Courier", 6), fill='white')

    def onShow(self):
        #initialises variables
        #node file
        self.nodeList = self.readYaml(self.mainGUI.tmapPath)
        #yaml file
        self.yamlFile = self.readYaml(self.mainGUI.yamlPath)
        #resolution from yaml file
        self.scale = float(self.yamlFile["resolution"])
        #origin from yaml file
        self.ORIGIN = (self.yamlFile["origin"][0], self.yamlFile["origin"][1])
        #image opened from user selected path
        self.im = PILImage.open(self.mainGUI.mapPath)
        #width and size of image
        self.width, self.height = self.im.size
        #load imagee
        self.loadImage()
        #path variables
        self.pathx1=0
        self.pathy1=0
        self.pathx2=0
        self.pathy2=0



#sets instance of GUI
app = GUI()
#main loops GUI instance
app.mainloop()
