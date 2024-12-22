# Crossover
import random
import math

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
average_node_num = len(all_nodes) // 2
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

            distance = math.sqrt(((x-mx)**2) + ((y-my)**2))

            if distance < min_distance and (x != mx or y != my):
                min_distance = distance
                closest_node = child_available_nodes[i]
                print(distance)
                print("closest node:   ", closest_node)
                [x_, y_] = [x, y]

        # convert coords to: [id1, id2] (can be deleted here)
        result = [
        x_ + y_ / (10 ** len(str(int(y_)))),  
        mx + my / (10 ** len(str(int(my)))) 
        ]
        print("fixed connection: ", result)


        # overwrite old connection (by first searching its place in ch_connections)
        for i in range(len(child_connections)):
            [id1_, id2_] = child_connections[i]
            if id1_ == id1 and id2_ == id2:
                child_connections[i] = [
                x_ + y_ / (10 ** len(str(int(y_)))),  
                mx + my / (10 ** len(str(int(my)))) 
                ]
                break

    ### testet ob die connection (aus id1, id2) bereits in child_connections existiert.
    ### -> es müssen aber alle connections geprüft werden
    ### ---> quatsch! er sucht nur die stelle mit der alten connection um die zu replacen


    ### INRGENDWAS ZUM PRÜFEN, OB FIXED CONNECTION BEREITS EXISTIERT
    ### WAS WENN BEIDE NODES VON EINER CONNECTION FEHLEN?
    
print(child_connections)
    








# crossings: or calculate every possible connection and crossing?
# -> so you know if 2 cross?



