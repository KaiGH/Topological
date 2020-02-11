import yaml

#Opening the yaml file to print out the contents
def readYaml():
    with open("test.yaml") as rf:
        node_coords = yaml.load(rf, Loader=yaml.FullLoader)

        print(node_coords)


#Editing existing data in the yaml file
def editYaml():
    with open("test.yaml") as ef:
        node_coords = yaml.load(ef, Loader=yaml.FullLoader)

        node = input("Enter node: \n")
        newX = int(input("Enter new x value: \n"))
        newY = int (input("enter new y value: \n"))

        for nodes in node_coords:
            if nodes["name"] == node:
                nodes["x"] = newX
                nodes["y"] = newY

    with open("test.yaml", "w") as wf:
        yaml.dump(node_coords, wf)


#Adding a new node to the yaml file
def writeYaml():
    with open("test.yaml") as rf:
        node_coords = yaml.load(rf, Loader=yaml.FullLoader)


    for nodes in node_coords:
        print(nodes["name"])

    node = nodes["name"].split('_')
    nodeNum = int(node[1])
    nodeNum = nodeNum + 1

    
    newX = input("Enter X coordinate for new node: \n")
    newY = input("Enter Y coordinate for new node: \n")

    # UNFINISHED CODE -------- Need to find way to input formatted data back into the yaml file
    #new_data_dict = {
    #    '- name: ':  'node_' + str(nodeNum),
    #}

    #node_coords.update(node_coords, new_data_dict)


    #with open("test.yaml", "w") as wf:
    #    yaml.dump(node_coords, wf)


#writeYaml()
readYaml()
editYaml()