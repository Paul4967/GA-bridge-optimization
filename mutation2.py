import random


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


def connection_is_possible(x1, y1, x2, y2):
    for connection in all_connections:
        id1_, id2_ = connection
        [x1_, y1_] = getCoords(id1_)
        [x2_, y2_] = getCoords(id2_)

        if 1 == 1: # avoid checking same connections
            print("con1: ", id1, id2, "con2: ", id1_, id2_)
            slope1 = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf') # slope of new theoretical connection
            slope2 = (y2_ - y1_) / (x2_ - x1_) if x2_ != x1_ else float('inf')

            #check if b is equal
            b1 = (slope1 * x1) - y1
            b2 = (slope2 * x1_) - y1_
            if slope1 == slope2 and b1 == b2 and slope1 != float('inf') and max(x1, x2) > min(x1_, x2_) and max(x1_, x2_) > min(x1, x2): # 1 has to be left and 2 has to be right
                print ("x-overlap")
                return False
            # logic for infinite slope
            elif slope1 == float('inf') and x1 == x1_:
                if max(y1, y2) > min(y1_, y2_) and max(y1_, y2_) > min(y1, y2):
                    print("y-overlap")
                    return False
            else:
                #test for crossing
                [p1, q1] = [id1, id2]
                [p2, q2] = [id1_, id2_] 
                if calcRotation(p1, q1, p2) + calcRotation(p1, q1, q2) == 0 and calcRotation(p2, q2, p1) + calcRotation(p2, q2, q1) == 0:
                    print (id1, id2, "is crossing with ", id1_, id2_)
                    return False
                
        else:
            print("same connection for:", id1, id2, id1_, id2_)
            return False
    
    print("WORKING")
    return True



        



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
        #[2.1, 2.0],
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



mutate_connection_probability = 1 # in range 0 to 1

if random.random() < mutate_connection_probability:  # random.random() generates a float in [0, 1)
    print("mutating")

    # add or remove random connection

    if random.randint(0,1) == 0:
        #remove connection
        del bridge_connections[random.randint(0, len(bridge_connections) - 1)]
        print("connection deleted")
    else:
        # ADD CONNECTION
        #randomly select node (can be basenode too)
        random.shuffle(available_nodes)

        connection_found = False
        i = 0
        while not connection_found and i < len(available_nodes):    # iterate through all nodes
            [id1, x1, y1] = available_nodes[i]

            j = 0
            while not connection_found and j < len(available_nodes):
                if j == i:  # id1 != id2
                    j += 1
                    continue
                    
                
                [id2, x2, y2] = available_nodes[j]
                
                if any(set([id1, id2]) != set(connection) for connection in bridge_connections): # check if connection exists

                    # check posibility, by comparing to all other connections
                    if connection_is_possible(x1, y1, x2, y2):
                        connection_found = True
                

                j += 1

            i += 1
        
        if connection_found:
            print("new connection at: ", id1, id2)