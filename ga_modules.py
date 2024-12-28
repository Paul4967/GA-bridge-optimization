# all_nodes: nodes from base and bridge
# all_connections: connections from base and bridge



def getCoords(id, all_nodes):
    for node in all_nodes:
        if node[0] == id:
            return node[1], node[2]
    raise ValueError(f"ID {id} not found in available nodes.")


def calcRotation(point1, point2, point3, all_nodes):
    
    # nodes can be from child, or basenodes
    point1_ = next((node[1:] for node in all_nodes if node[0] == point1), None)
    point2_ = next((node[1:] for node in all_nodes if node[0] == point2), None)
    point3_ = next((node[1:] for node in all_nodes if node[0] == point3), None)

    rotation = (point2_[1] - point1_[1]) * (point3_[0] - point2_[0]) - (point3_[1] - point2_[1]) * (point2_[0] - point1_[0])
    # rotation > 0 = right, = 0 -> straight 
    rotation = (point2_[1] - point1_[1]) * (point3_[0] - point2_[0]) - (point3_[1] - point2_[1]) * (point2_[0] - point1_[0])
    # rotation > 0 = right, = 0 -> straight 

    direction = 1 if rotation > 0 else (-1 if rotation < 0 else 5) # to prevent linear on 1 line parallel connecting beams from being deleted in if statement below
    return direction




def connection_is_possible(id1, id2, all_connections, all_nodes, allow_splitting):
    x1, y1 = getCoords(id1, all_nodes)
    x2, y2 = getCoords(id2, all_nodes)

    for connection in all_connections:
        id1_, id2_ = connection
        if min(id1, id2) == min(id1_, id2_) and max(id1, id2) == max(id1_, id2_):
            continue
        [x1_, y1_] = getCoords(id1_, all_nodes)
        [x2_, y2_] = getCoords(id2_, all_nodes)

        
        print("con1: ", id1, id2, "con2: ", id1_, id2_)
        slope1 = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf') # slope of new theoretical connection
        slope2 = (y2_ - y1_) / (x2_ - x1_) if x2_ != x1_ else float('inf')

        # check for overlay
        # check if b is equal
        b1 = (slope1 * x1) - y1
        b2 = (slope2 * x1_) - y1_
        if slope1 == slope2 and b1 == b2 and slope1 != float('inf') and max(x1, x2) > min(x1_, x2_) and max(x1_, x2_) > min(x1, x2): # 1 has to be left and 2 has to be right
            print ("x-overlap")
            return False
        # logic for infinite slope
        elif slope1 == float('inf') and slope2 == float('inf') and x1 == x1_:
            if max(y1, y2) > min(y1_, y2_) and max(y1_, y2_) > min(y1, y2):
                print("y-overlap")
                return False
        else:
            # test for crossing
            [p1, q1] = [id1, id2]
            [p2, q2] = [id1_, id2_] 
            if calcRotation(p1, q1, p2, all_nodes) + calcRotation(p1, q1, q2, all_nodes) == 0 and calcRotation(p2, q2, p1, all_nodes) + calcRotation(p2, q2, q1, all_nodes) == 0:
                print (id1, id2, "is crossing with ", id1_, id2_)
                return False
            
            
    for node in all_nodes:
        _, x3, y3 = node

        # Check if the node lies within the bounds of the connection
        in_bound_of_connection = (
            (x1 == x2 and min(y1, y2) < y3 < max(y1, y2) and x3 == x1) or  # Vertical connection
            (y1 == y2 and min(x1, x2) < x3 < max(x1, x2) and y3 == y1) or  # Horizontal connection
            (min(x1, x2) < x3 < max(x1, x2) and min(y1, y2) < y3 < max(y1, y2))  # Diagonal connection
        )

        if abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) == 0 and in_bound_of_connection:  # calculate triangle area
            print(f'connection {x1, y1}, {x2, y2} is crossing with point: {node}')

            if allow_splitting:
                split_c1 = [
                x1 + y1 / (10 ** len(str(int(y1)))),  
                x3 + y3 / (10 ** len(str(int(y3)))) 
                ]
                split_c2 = [
                x2 + y2 / (10 ** len(str(int(y2)))),  
                x3 + y3 / (10 ** len(str(int(y3)))) 
                ]
                print(split_c1, split_c2)
                return split_c1, split_c2
            return False
                    
    print("WORKING")
    return True