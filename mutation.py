
# shift random nodes randomly (set max distance)
# set max and min distance
# set step / snap (e.g. snap to 0.25 grid)
# set probability for each individual node to be shifted
# if connection is not possible afterwards, shift in other directions, till it works. otherwise dont shift. (then increase probability for other nodes?)

# create new, or delete connections
# 10 connections: each one has 5% probability to be deleted -> 10*5 = 50%
# 1. decide on deleting or not, then if yes (50% probability) delete 1 random connection
# checking if connection is possible is important.
# -> if connection exists or crosses other connection, try for next point, till tried to connect every point with each other point.

import random

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
    ],
    "connections": [
        [0.0, 2.0],
        [2.0, 4.0],
        [4.0, 6.0]
    ]
}

bridge = {
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


bridge_connections = bridge["connections"]
all_connections = bridge["connections"] + base_nodes["connections"]

base_nodes = base_nodes["nodes"]
bridge_nodes = bridge["nodes"]
available_nodes = bridge_nodes + base_nodes


def getCoords(id):
    for node in available_nodes:
        if node[0] == id:
            return node[1], node[2]
    raise ValueError(f"ID {id} not found in available nodes.")


def calcRotation(point1, point2, point3):
    
    all_available_nodes = available_nodes
    # nodes can be from child, or basenodes
    point1_ = next((node[1:] for node in all_available_nodes if node[0] == point1), None)
    point2_ = next((node[1:] for node in all_available_nodes if node[0] == point2), None)
    point3_ = next((node[1:] for node in all_available_nodes if node[0] == point3), None)

    rotation = (point2_[1] - point1_[1]) * (point3_[0] - point2_[0]) - (point3_[1] - point2_[1]) * (point2_[0] - point1_[0])
    # rotation > 0 = right, = 0 -> straight 


    if rotation > 0:
        direction = 1
    elif rotation < 0:
        direction = -1
    else:
        direction = 5 # to prevent linear on 1 line parallel connecting beams from being deleted in if statement below

    return direction


#////////////////////////////////////////////////////




# create / delete connection                                                # DELETE OR ADD MULTIPLE CONNECTIONS AT ONCE? -> faster evolution? (for loop for this)
mutate_connection_probability = 0.5 # in range 0 to 1
if random.random() < mutate_connection_probability:  # random.random() generates a float in [0, 1)
    print("mutating")

    # add or remove connection
    if random.randint(0,1) == 0:
        #remove connection
        del bridge_connections[random.randint(0, len(bridge_connections) - 1)]
        print("connection deleted")
    else:
        #add connection
        #randomly select node (can be basenode too)
        random.shuffle(available_nodes)
        [id1, x1, y1] = available_nodes[0]

        # check if connection is possilbe
        for i in range(len(available_nodes)):
            [id2, x2, y2] = available_nodes[i]
            # connect id1 to every other id and check for crossings, start with random id -> SHUFFLE available nodes!
            # possible if: 
            # new node is not itself 
            # connection does not already exist
            # not crossing
            print(id1, id2)
            if id1 != id2 and any(set([id1, id2]) != set(connection) for connection in bridge_connections): # check if connection exists
                # check for overlay         # what if slope is infinite? -> vertical
                # by: 1 check if both lines have the same slope
                #     2 create linear function and compare them (m * x + b) -> b bestimmen
                slope1 = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf') # slope of new theoretical connection
                for connection in all_connections:
                    id1_, id2_ = connection
                    [x1_, y1_] = getCoords(id1_)
                    [x2_, y2_] = getCoords(id2_)
                    slope2 = (y2_ - y1_) / (x2_ - x1_) if x2_ != x1_ else float('inf')
                    print("con1: ", id1, id2, "con2: ", id1_, id2_)

                    #check if b is equal
                    b1 = (slope1 * x1) - y1
                    b2 = (slope2 * x1_) - y1_
                    if slope1 == slope2 and b1 == b2 and slope1 != float('inf'):
                        print(" COLLINEAR EXISTING CONNECTION FOUND", b1, b2)
                        break

                    elif slope1 == float('inf'):

                        if x1 == x1_ and max(y1, y1_) < min(y2, y2_):
                            print('connections overlap')
                            break # will exit nearest enclosing loop
                    

                    #test for crossing
                    a = 0
                    i = 0
                    while i < len(bridge_connections):  
                        print("check crossing for: ", bridge_connections[i])

                        [p1, q1] = bridge_connections[i]

                        j = 0
                        while j < len(bridge_connections):  # Nested while loop
                            if i == j:  # Skip the same connection
                                j += 1
                                continue

                            [p2, q2] = bridge_connections[j]
                            # print("_points: ", p1, q1, p2, q2)

                            if p1 != p2 and q1 != q2:
            
                                crossing = False
                                if calcRotation(p1, q1, p2) + calcRotation(p1, q1, q2) == 0 and calcRotation(p2, q2, p1) + calcRotation(p2, q2, q1) == 0:
                                    crossing = True
                                    print(p1, q1, "is crossing with: ", bridge_connections[j])
                                    del bridge_connections[j]
                                    a -= 1
                                    continue  # Skip incrementing `j` since the list size has changed

                            j += 1  # Increment `j` if no deletion

                        i += 1  # Increment `i` after finishing checks for the current connection
            

                
                
            

# 0.0 6.0 ist ja auch nicht possible -> darf keinen anderen punkt schneiden

print("EX")
print(all_connections)
    


