import yaml
import copy
from PIL import Image as PILImage,ImageTk
from tkinter import *

 
#Opening the Yaml File to Print out the Contents
def readYaml(filename):
    with open(filename) as fileReader:
        node_coords = yaml.load(fileReader, Loader=yaml.FullLoader)
        return (node_coords)

#Name all Nodes
def nodeNames(filename):
   #Recieves file data from read function
    data = readYaml(filename)
    #returns all nodes that exist in file
    return [node["meta"]["node"] for node in data]

def nodeCoords(filename):
   #Recieves file data from read function
    data = readYaml(filename)
    #returns all nodes that exist in file
    return [[node["node"]["pose"]["position"]["x"],node["node"]["pose"]["position"]["y"], node["meta"]["node"]]for node in data]

#Generates all Numbers Attached to Waypoints, Finds the Next Unused Number
def nodeNumber(filename):
    data = readYaml(filename)
    #searches all "WayPoint" data and takes the numbers from the ends of those strings
    numbers = [int(node["meta"]["node"][8:]) for node in data]
    #puts numbers in order
    numbers.sort()
    #returns the next number in sequence
    return numbers[-1] + 1

#Editing Existing Node Data in the Yaml File
def editNode(filename):
    nodeList = readYaml(filename)
    print("Choose a node to edit")
    print(nodeNames(filename))
    nodeName = input("Enter node: \n")
    newX = int(input("Enter new x value: \n"))
    newY = int (input("enter new y value: \n"))
    
    #Searches from the First to the Last Node
    for index in range(len(nodeList)):     
    #If the Node Matches with the Inputted Node
      if nodeList[index]["meta"]["node"] == nodeName:
          #Changing Variables to Match User Input
          nodeList[index]["node"]["pose"]["position"]["x"] = newX
          nodeList[index]["node"]["pose"]["position"]["y"] = newY
          print(nodeList[index]["node"]["pose"]["position"])
          
          #Opens "write" Stream 
          stream = open('riseholme.tmap', 'w')
          #Dumps New Yaml Data into File
          yaml.dump(nodeList, stream)   
          break
#Deleting Nodes
def deleteNode(filename):
    nodeList = readYaml(filename)
    print("Choose a node to delete")
    nodeName = input("Enter node: \n")
    #Searches from the First to the Last Node
    for index in range(len(nodeList)):      
    #If the Node Matches with the Inputted Node
      if nodeList[index]["meta"]["node"] == nodeName:
          #Deletes Node
          del(nodeList[index])
          stream = open('riseholme.tmap', 'w')   
          yaml.dump(nodeList, stream)   


#Adding Path Data in the Yaml File
def addPath(filename):
    nodeList = readYaml(filename)
    nodeName1 = input("Enter start WayPoint: \n")
    nodeName2 = input("Enter end WayPoint: \n")
    newPath = copy.deepcopy(nodeList[1]["node"]["edges"][0])
    newPath["edge_id"] = nodeName1 + "_" + nodeName2
    newPath["node"] = nodeName1

    for index in range(len(nodeList)):
        if nodeName1 == nodeList[index]["meta"]["node"]:
            nodeList[index]["node"]["edges"].append(newPath)
            stream = open('riseholme.tmap', 'w')   
            yaml.dump(nodeList, stream)   
            #how to access a specific path print(nodeList[1]["node"]["edges"][0]["edge_id"])

#Deleting Existing Node
def deletePath(filename):
     nodeList = readYaml(filename)
     print("Select nodes to remove path")
     nodeName1 = input("Enter start node of path: \n")
     nodeName2 = input("Enter end node of path: \n")
     searchPath = nodeName1 + "_" + nodeName2      
     for i in range(len(nodeList)):     
        for j in range(len(nodeList[i]["node"]["edges"])):
            if nodeList[i]["node"]["edges"][j]["edge_id"] == searchPath:
                print(i, j, "\n", nodeList[i]["node"]["edges"][j])
                del(nodeList[i]["node"]["edges"][j])
                stream = open('riseholme.tmap', 'w')   
                yaml.dump(nodeList, stream)  


def pathNums(filename):
    nodeList = readYaml(filename)
    paths = []
    for i in range(len(nodeList)):     
        for j in range(len(nodeList[i]["node"]["edges"])):
            path = nodeList[i]["node"]["edges"][j]["edge_id"]
            paths.append([[path[:path.index("_")]], [path[path.index("_")+1:]]])
    return paths

def printPaths(filename):
    nodeList = readYaml(filename)
    for i in range(len(nodeList)):     
       print("For node", nodeList[i]["meta"]["node"], "these paths exist:")
       for j in range(len(nodeList[i]["node"]["edges"])):
           print(nodeList[i]["node"]["edges"][j]["edge_id"])

#Adding a New Node to The Yaml File
def addNode(filename):
    #Get User Input
    print("to make new node, enter x and y")
    newX = int(input("enter new x value: \n"))
    newY = int (input("enter new y value: \n"))

    #Gets File, Takes a Node to be Used as a Template for our New Node
    nodeList = readYaml(filename)
    newNode = copy.deepcopy(nodeList[0])
    #Calls next number in sequence of nodes to define this new one
    newNumber = nodeNumber(filename)
    
    #More attributes can be changed but I've started with node definition, name, x and y
    newNode["meta"]["node"] = "WayPoint"+str(newNumber)
    newNode["node"]["name"] = "WayPoint"+str(newNumber)
    newNode["node"]["pose"]["position"]["x"] = newX
    newNode["node"]["pose"]["position"]["y"] = newY
    #For testing the new node and the old one are different in the way you want
    print("\nNew Node:\n")
    print(newNode)   
    print("\nNode 1 for Comparison:\n")
    print(nodeList[0]) 
    
    #Appends new node to rest of the file then dumps into file
    nodeList.append(newNode)
    stream = open('riseholme.tmap', 'w')   
    yaml.dump(nodeList, stream)   

def showMap(filename, imagename, ORIGIN, SCALE):
    points = nodeCoords(filename)
    im = PILImage.open(imagename)
    width, height = im.size
    root = Tk()      
    canvas = Canvas(root, width=width/SCALE, height = height/SCALE)
    canvas.pack()      
    image2=im.resize((int(width/SCALE),int(height/SCALE)),PILImage.ANTIALIAS)
    riseholme2=ImageTk.PhotoImage(image2)
    canvas.create_image(0,0, anchor=NW, image=riseholme2) 

    paths = pathNums(filename)

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
                draw_line(pointACoords, pointBCoords, 0.05, ORIGIN, SCALE, width, height, canvas)

    for point in points:
        draw_point(point[0], point[1], 0.05, point[2][8:], ORIGIN, SCALE, width, height, canvas)

    mainloop()  

def draw_point(x, y, scale, label, ORIGIN, SCALE, width, height, canvas):
    newX, newY =  (((x-ORIGIN[0])/scale)/SCALE), (height/SCALE)- (((y-ORIGIN[1])/scale)/SCALE)
    radius = 7.5
    canvas.create_oval(newX - radius, newY - radius, newX + radius, newY + radius, fill = 'blue')
    canvas.create_text(newX, newY, text = label, font=("Courier", 6), fill='white')

def draw_line(a, b, scale, ORIGIN, SCALE, width, height, canvas):
    newAX, newAY =  (((a[0]-ORIGIN[0])/scale)/SCALE), (height/SCALE)- (((a[1]-ORIGIN[1])/scale)/SCALE)
    newBX, newBY =  (((b[0]-ORIGIN[0])/scale)/SCALE), (height/SCALE)- (((b[1]-ORIGIN[1])/scale)/SCALE)
    canvas.create_line(newAX, newAY, newBX, newBY)
  

def switch():
        SCALE = 2
        ORIGIN = (-31.45, -12.45)
        i=0
        while i != 9:
            i = int(input())
            if i == 1:
                addNode("riseholme.tmap")  
            if i == 2:
                editNode("riseholme.tmap")  
            if i == 3:
                deleteNode("riseholme.tmap")
            if i == 4:
                print(nodeNames("riseholme.tmap")) 
            if i == 5:
                addPath("riseholme.tmap")  
            if i == 6:
                deletePath("riseholme.tmap")
            if i == 7:
                printPaths("riseholme.tmap")
            if i == 8:
                showMap('riseholme.tmap', 'riseholme.pgm', ORIGIN, SCALE)

print("Enter the number corrosponding to the function you wish to execute:")
print("1.Add Node\n2.Edit Node\n3.Delete Node\n4.Print Nodes\n5.Add Path\n6.Delete Path\n7.Print Paths\n8.Show Map")
switch()

#Uncomment the function you wish to call
#All methods take file name to make file switching easy

#readYaml("riseholme.tmap")
#addNode("riseholme.tmap")
#addPath("riseholme.tmap")
#nodeNames("riseholme.tmap")
#editYaml("riseholme.tmap")
#deletePath("riseholme.tmap")
#print(nodeNumber("riseholme.tmap"))
#deleteNode("riseholme.tmap")
