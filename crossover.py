# Crossover
import random
import math
import json

base_nodes = {
    "nodes": [
        [0.0, 0, 0],
        [2.0, 2, 0],
        [4.0, 4, 0],
        [6.0, 6, 0],
        # ["b1", 0, 0],
        # ["b2", 2, 0],
        # ["b3", 4, 0],
        # ["b4", 6, 0],
    ]
}

bridge1 = {
    "nodes": [
        [1.2, 1, 2],
        [2.1, 2, 1],
        [5.2, 5, 2]
    ],
    "connections": [
        [0.0, 1.2],
        [1.2, 2.1],
        [2.1, 2.0],
        [2.1, 4.0],
        [1.2, 5.2],
        [5.2, 4.0],
        [5.2, 6.0],
    ]
}

bridge2 = {
    "nodes": [
        [1.1, 1, 1],
        [3.1, 3, 1],
        [5.1, 5, 1]
    ],
    "connections": [
        [0.0, 1.1],
        [2.0, 1.1],
        [2.0, 3.1],
        [4.0, 3.1],
        [4.0, 5.1],
        [6.0, 5.1],
        [1.1, 3.1],
        [3.1, 5.1],
    ]
}


#
# USE SETS FOR LOWER TIME COMPLEXITY?
#
# WHAT IF both parents have same connections???
#

# merge nodes of parent 1 and 2
all_nodes = bridge1["nodes"] + bridge2["nodes"]

child_nodes = []
seen = []

# create copy and shuffle
shuffled_nodes = all_nodes[:]
random.shuffle(shuffled_nodes)


# select first 50% of shuffled array
a = 0
i = 0
average_node_num = round(len(all_nodes) / 2)
while i < average_node_num + a:
        
    # check if object is seen & append if not
    if shuffled_nodes[i] in seen:
        a+=1
        
    else:
        child_nodes.append(shuffled_nodes[i])
        
    seen.append(shuffled_nodes[i])
    i+=1
     
print("all nodes: ", all_nodes)
print("shullfed Nodes:", shuffled_nodes)
print("seen", seen)
print("child nodes:     ", child_nodes)

print(child_nodes)




## Connections:

all_connections = bridge1["connections"] + bridge2["connections"]

# get IDs of childs nodes
valid_ids = [node[0] for node in child_nodes]
print("VALID_IDs: ", valid_ids)

# filter all connections, that connect to at least one kept point
available_connections = [
    [id1, id2] for (id1, id2) in all_connections 
    if id1 in valid_ids or id2 in valid_ids
]

print("ALL Connections: ", all_connections)
print("Available Connections:", available_connections)



# fix connections

base_node_ids = [node[0] for node in base_nodes["nodes"]]

child_connections = available_connections[:]

# Iterate over the filtered array and process each pair
for id1, id2 in available_connections:
    id1_exists = id1 in valid_ids
    id2_exists = id2 in valid_ids

    # Check if either id1 or id2 is in baseNodeIds (bool)
    id1_in_base_nodes = id1 in base_node_ids
    id2_in_base_nodes = id2 in base_node_ids

    # execute if 1 node is missing. 
    if (id1_exists != id2_exists) and (not id1_in_base_nodes and not id2_in_base_nodes):
        missing_id, existing_id = (id2, id1) if id1_exists else (id1, id2)
        print(f"Entry: [{id1}, {id2}] - Missing ID: {missing_id}")
        
        # get coord of existing node
        [ex, ey] = next((node[1:] for node in all_nodes if node[0] == existing_id), None)
        
        # get coord of missing node 
        [mx, my] = next((node[1:] for node in all_nodes if node[0] == missing_id), None)
        print(mx,my)

        # calculate distance to all other available points (nodes + base_nodes)
        clear_base_nodes = [node[1:] for node in base_nodes['nodes']]
        clear_child_nodes = [node[1:] for node in child_nodes]
        
        child_available_nodes = clear_child_nodes + clear_base_nodes
        print("AVAILABLE NODES:", child_available_nodes)


        # find closest node
        min_distance = float('inf')
        x_, y_ = 0, 0

        for i in range(len(child_available_nodes)):
            [x, y] = child_available_nodes[i]
            print(mx, my, x, y)

            # euclidiean distance formula
            distance = math.sqrt(((x-mx)**2) + ((y-my)**2))

            if distance < min_distance and (x != ex or y != ey):
                min_distance = distance
                closest_node = child_available_nodes[i]
                print(distance)
                print("closest node:   ", closest_node)
                [x_, y_] = [x, y]

        # convert coords to: [id1, id2] (can be deleted here)
        result = [
        x_ + y_ / (10 ** len(str(int(y_)))),  
        ex + ey / (10 ** len(str(int(ey)))) 
        ]
        print("fixed connection: ", result)
        print("A N: ", child_nodes)
        #^^ hier ist der fehler! manchmal wird existente node rplaced
        # FIXED!! (m mit e getauscht. m steht für missing. wow!)

        # overwrite old connection (by first searching its place in ch_connections)
        for i in range(len(child_connections)):
            [id1_, id2_] = child_connections[i]
            if id1_ == id1 and id2_ == id2:
                child_connections[i] = [
                x_ + y_ / (10 ** len(str(int(y_)))),  
                ex + ey / (10 ** len(str(int(ey)))) 
                ]
                print("fixed connection: ", child_connections[i])

                break
    
        


        

    ### testet ob die connection (aus id1, id2) bereits in child_connections existiert.
    ### -> es müssen aber alle connections geprüft werden
    ### ---> quatsch! er sucht nur die stelle mit der alten connection um die zu replacen


    ### INRGENDWAS ZUM PRÜFEN, OB FIXED CONNECTION BEREITS EXISTIERT
    ### -> ganz am Ende (nach crossings)
    ### WAS WENN BEIDE NODES VON EINER CONNECTION FEHLEN?
    
print("//////////////////////")
print("CHILD CONNECTIONS: ", child_connections) # fixed
print("CHILD NODES: ", child_nodes)
# print("CHILD AVAIL NODES: ", child_available_nodes)

print(available_connections)

# SOMETIMES IS CHILD AVAILABLE NODES NOT DEFINED?
# ---> das ist, wenn alle nodes von den connections noch vorhanden sind (wenn zufällig parent generiert wird)
# ----> weil child_availalble_nodes ja erst def. wird, wenn eine id nicht existiert

# irgendwie manchmal trotzdem falsche ID replaced





def calcRotation(point1, point2, point3):
    
    all_available_nodes = base_nodes["nodes"] + child_nodes
    # 1 get coordinates of p1, p2, ...
    # -> split at decimal point
    # nodes can be from child, or basenodes
    point1_ = next((node[1:] for node in all_available_nodes if node[0] == point1), None)
    point2_ = next((node[1:] for node in all_available_nodes if node[0] == point2), None)
    point3_ = next((node[1:] for node in all_available_nodes if node[0] == point3), None)

    print("POINTS", point1, point2, point3, "CORDS: ", point1_, point2_, point3_)
    print("A L L N O D E S:  ", all_available_nodes)
    # first_val = point1[0]
    # 2 do calculation
    # calculate slope (y2-y1 / x2-x1)
    ### zähler = 0 -> vertikal, nenner = 0 -> horizontal
    # sigma = (point2_[1] - point1_[1]) / (point2_[0] - point1_[0])
    # tau = (point3_[1] - point2_[1]) / (point3_[0] - point2_[0])

    rotation = (point2_[1] - point1_[1]) * (point3_[0] - point2_[0]) - (point3_[1] - point2_[1]) * (point2_[0] - point1_[0])
    # rotation > 0 = right, = 0 -> straight 


    if rotation > 0:
        direction = 1
    elif rotation < 0:
        direction = -1
    else:
        direction = 5 # to prevent linear on 1 line parallel connecting beams from being deleted in if statement below

    return direction





    # crossings
    # for i in range(len(child_connections)):
 #           [id1_, id2_] = child_connections[i]

# child_connections_2 = child_connections[:]
a = 0
i = 0
while i < len(child_connections):  # Use a while loop for better control
    print("check crossing for: ", child_connections[i])

    [p1, q1] = child_connections[i]

    j = 0
    while j < len(child_connections):  # Nested while loop
        if i == j:  # Skip the same connection
            j += 1
            continue

        [p2, q2] = child_connections[j]
        # print("_points: ", p1, q1, p2, q2)

        if p1 != p2 and q1 != q2:
            print("C C")
            print("ROT:", calcRotation(p1, q1, p2) + calcRotation(p1, q1, q2), calcRotation(p1, q1, p2), calcRotation(p1, q1, q2))
            crossing = False
            if calcRotation(p1, q1, p2) + calcRotation(p1, q1, q2) == 0 and calcRotation(p2, q2, p1) + calcRotation(p2, q2, q1) == 0:
                crossing = True
                print(p1, q1, "is crossing with: ", child_connections[j])
                del child_connections[j]
                a -= 1
                continue  # Skip incrementing `j` since the list size has changed

        j += 1  # Increment `j` if no deletion

    i += 1  # Increment `i` after finishing checks for the current connection
            
        

        


#### ELIMINATE SAME CONNECTIONS!!! (duplicates)
# nimmt er glaube durch crossigns schon raus
# -> doch noch nicht







## save to json
data = {
    "child_connections": child_connections,
    "child_nodes": child_nodes
}

file_name = "temp.json"
with open(file_name, 'w') as json_file:
    json.dump(data, json_file)


# same connections (or inverts need to be removed) -> accounted for in fixing connections example: 2.1 3.1 is going to 2.1 1.1 bc 3.1 is gone.
# -> no rerouting! just delete duplicates
# note: p1 and p2 can be switched!



### Rerouting
### -> cant cross
### -> cant be existing connection