from tkinter import ttk, filedialog, Label, Frame, W, Entry, E, Canvas, NW
from PIL import Image as PILImage,ImageTk
import tkinter as tk
import yaml
import copy

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
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
        frame = self.frames[page]
        frame.tkraise()
        frame.onShow()

        #start page class
class StartPage(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.mainGUI = controller
        #inserted text label
        YAML =Label(self, width= 20, text = "Insert YAML File Path")
        TMAP=Label(self, width= 20, text ="Insert TMAP File Path")
        Map =Label(self, width= 20, text = "Insert Map File Path")
        #positioning of text label
        YAML.grid(row=3, column=0)
        TMAP.grid(row=3, column=2)
        Map.grid(row=3, column=4)  
        #declaring button
        YAMLButton = ttk.Button(self, text= "Open YAML File", command =self.YAML)
        TMAPButton = ttk.Button(self, text= "Open TMAP File", command =self.TMAP)
        MapButton = ttk.Button(self, text= "Open Map File",  command =self.Map)

        nextbutton = ttk.Button(self, text= "Generate", command= lambda: controller.show_frame("Edit"))
        #postioning button
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
        self.tmapfilename = filedialog.askopenfilename(title = "Select A File", filetypes =[('TMAP Files', '*.tmap')])
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
        self.mainGUI = controller

        self.header = Frame(self)
        self.header.grid(row=0, column = 1)

        self.footer = Frame(self)
        self.footer.grid(row=3, column = 1)

        self.buttonContainer = Frame(self)
        self.buttonContainer.grid(row = 1, column=0)

        self.nodeButtons = Frame(self.buttonContainer)
        self.nodeButtons.grid(row = 1, column=0)

        Blank1=Label(self.buttonContainer, width= 20,text ="Insert Parameters:")
        Blank1.grid(row=2, column=0)

        self.nodeButtonsEntry = Frame(self.buttonContainer)
        self.nodeButtonsEntry.grid(row = 3, column=0)

        self.pathButtons = Frame(self.buttonContainer)
        self.pathButtons.grid(row = 6, column=0)

        Blank2=Label(self.buttonContainer, width= 20,text ="")
        Blank2.grid(row=5, column=0)

        self.pathButtonsEntry = Frame(self.buttonContainer)
        self.pathButtonsEntry.grid(row = 8, column=0)
        
        FilePagebutton = ttk.Button(self.header, width= 20, text ="select different files", command= lambda:controller.show_frame("Start"))
        FilePagebutton.grid()
        Save = ttk.Button(self.footer, width= 20, text= "Save", command = self.mapSave)
        Save.grid(row=1, column=1)

        AddNode = ttk.Button(self.nodeButtons, width= 20, text= "Add New Node", command = self.addNode)
        AddNode.grid(row=1, column=1)

        DeleteNode = ttk.Button(self.nodeButtons, width= 20, text= "Delete A Node", command = self.nodeDelete)
        DeleteNode.grid(row=1, column=2)

        EditNode = ttk.Button(self.nodeButtons, width= 20, text= "Edit A Node" , command = self.nodeEdit)
        EditNode.grid(row=1, column=3)

        nodeName=Label(self.nodeButtonsEntry, width= 30,text ="Insert Node Name")
        self.nodeNameEntry=Entry(self.nodeButtonsEntry, width= 30, text ="Insert Node Name ")
        nodeName.grid(row=2, column=1)
        self.nodeNameEntry.grid(row=2, column=2)

        X=Label(self.nodeButtonsEntry, width= 30,text ="Insert X Coordinate")
        self.XEntry=Entry(self.nodeButtonsEntry, width= 30, text ="Insert X Coordinate")
        X.grid(row=3, column=1,)
        self.XEntry.grid(row=3, column=2)

        Y=Label(self.nodeButtonsEntry, width= 30,text ="Insert Y Coordinate")
        self.YEntry=Entry(self.nodeButtonsEntry, width= 30, text ="Insert Y Coordinate")
        Y.grid(row=4, column=1)
        self.YEntry.grid(row=4, column=2)

        AddPath = ttk.Button(self.pathButtons, width= 20, text= "Add Path" , command = self.pathAdd)
        AddPath.grid(row=1, column=1)

        DeletePath = ttk.Button(self.pathButtons, width= 20, text= "Delete Path" , command = self.pathDelete)
        DeletePath.grid(row=1, column=2)

        Blank3=Label(self.buttonContainer, width= 20,text ="Insert Parameters:")
        Blank3.grid(row=7, column=0)

        nodeName1=Label(self.pathButtonsEntry, width= 30,text ="Insert Starting Node Name")
        self.nodeName1Entry=Entry(self.pathButtonsEntry, width= 30, text ="Insert Starting Node Name ")
        nodeName1.grid(row=2, column=1)
        self.nodeName1Entry.grid(row=2, column=2)

        nodeName2=Label(self.pathButtonsEntry, width= 30,text ="Insert Destination Node Name")
        self.nodeName2Entry=Entry(self.pathButtonsEntry, width= 30, text ="Insert Destination Node Name ")
        nodeName2.grid(row=3, column=1)
        self.nodeName2Entry.grid(row=3, column=2)



        #Opening the Yaml File to Print out the Contents
    def readYaml(self, filename):
        with open(filename) as fileReader:
            node_coords = yaml.load(fileReader, Loader=yaml.FullLoader)
            return (node_coords)      

    def nodeDelete(self):
        #nodeList = self.readYaml(self.mainGUI.tmapPath)
        nodeName = self.nodeNameEntry.get()
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

    def nodeCoords(self):
        #returns all nodes that exist in file
        return [[node["node"]["pose"]["position"]["x"],node["node"]["pose"]["position"]["y"], node["meta"]["node"]]for node in self.nodeList]

    def pathNums(self):
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
        points = self.nodeCoords()
        paths = self.pathNums()

        for path in paths: 
            #nodes that connect
            pointA = path[0][0]
            pointB = path[1][0]
            #variables for node x, y 
            pointACoords = None
            pointBCoords = None

            for point in points:
                if point[2] == pointA:
                    pointACoords = [point[0], point[1]]
                if point[2] == pointB:
                    pointBCoords = [point[0], point[1]]
            if(pointACoords != None and pointBCoords != None):
                self.draw_line(pointACoords, pointBCoords, self.yamlFile["resolution"])
        for point in points:
            #print(F"Plotting point {point[2][8:]}")
            if(point[0] != "" or point[1] != ""):
                self.draw_point(float(point[0]), float(point[1]), point[2][8:], float(self.yamlFile["resolution"]))
#sticky = E, padx=40

    def loadImage(self):
        im = PILImage.open(self.mainGUI.mapPath)
        self.SCALE = 3
        self.ORIGIN = (self.yamlFile["origin"][0], self.yamlFile["origin"][1])
        self.width, self.height = im.size
        self.canvas = Canvas(self, width=self.width/self.SCALE, height = self.height/self.SCALE)
        self.canvas.grid(row = 1, column=1)  
        image2=im.resize((int(self.width/self.SCALE),int(self.height/self.SCALE)),PILImage.ANTIALIAS)
        picture=ImageTk.PhotoImage(image2)
        label = Label(image=picture)
        label.image = picture # keep a reference!
        label.grid(row = 1, column=1)
        label.grid_forget()
        self.canvas.create_image(0,0, anchor=NW, image=picture) 
        self.drawingWayPoints()

    def draw_line(self, a, b, scale):
        newAX, newAY =  (((float(a[0])-float(self.ORIGIN[0]))/scale)/self.SCALE), (self.height/self.SCALE)- (((float(a[1])-float(self.ORIGIN[1]))/scale)/self.SCALE)
        newBX, newBY =  (((float(b[0])-float(self.ORIGIN[0]))/scale)/self.SCALE), (self.height/self.SCALE)- (((float(b[1])-float(self.ORIGIN[1]))/scale)/self.SCALE)
        self.canvas.create_line(newAX, newAY, newBX, newBY)

    def draw_point(self, x, y, label, scale):

        newX, newY =  (((x-self.ORIGIN[0])/scale)/self.SCALE), (self.height/self.SCALE)- (((y-self.ORIGIN[1])/scale)/self.SCALE)
        radius = 7.5
        self.canvas.create_oval(newX - radius, newY - radius, newX + radius, newY + radius, fill = 'blue')
        self.canvas.create_text(newX, newY, text = label, font=("Courier", 6), fill='white')



    def onShow(self):
        self.nodeList = self.readYaml(self.mainGUI.tmapPath)
        self.yamlFile = self.readYaml(self.mainGUI.yamlPath)
        self.loadImage()



#sets instance of GUI
app = GUI()
#main loops GUI instance
app.mainloop()
