# Crossover
import random
import math
import json
import ga_modules 

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
        child_available_nodes = child_nodes + base_nodes["nodes"] # rename base_nodes for clarity to base:nodes_connections or just base
        print("AVAILABLE NODES:", child_available_nodes)

        # find closest node
        closest_node = min(child_available_nodes, key=lambda node: math.sqrt(((node[1]-mx)**2) + ((node[2]-my)**2)))
        print(f'{mx, my} closest node: {closest_node}')
        _, x, y = closest_node
                
        # convert coords to: [id1, id2] (can be deleted here)
        
        # overwrite old connection (by first searching its place in ch_connections)
        for i, connection in enumerate(child_connections):
            [id1_, id2_] = connection
            if id1_ == id1 and id2_ == id2:
                child_connections[i] = [
                x + y / (10 ** len(str(int(y)))),  
                ex + ey / (10 ** len(str(int(ey)))) 
                ]
                print("fixed connection: ", child_connections[i])

                break
    










### CHECK IF CONNECTION IS POSSIBLE:


i = 0
all_available_connections = child_connections + base_nodes["connections"]
all__nodes = child_nodes + base_nodes["nodes"]
i = 0
while i < len(child_connections):
    id1, id2 = child_connections[i]
    result = ga_modules.connection_is_possible(id1, id2, all_available_connections, all__nodes, True)
    if result is False:
        del child_connections[i]
        del all_available_connections[i]
    elif isinstance(result, tuple) and len(result) == 2:
        del child_connections[i]
        del all_available_connections[i]
        c1, c2 = result
        child_connections.append(c1)
        child_connections.append(c2)
        # all_available_connections.append(result)
        print("APPENDING", c1, c2)
        print("CHILD CONN: ", child_connections)
    else:
        i += 1

            
        
### AUCH SCHAUEN OB ES CROSSING MIT FAHRBAHN GIBT (FALLS BUILDING DOMAIN AUCH NEGATIV IST!)
print(child_connections, "ch")
print(all_available_connections)


#### ELIMINATE SAME CONNECTIONS!!! (duplicates)
# nimmt er glaube durch crossigns schon raus
# -> doch noch nicht
seen = set()
unique_connections = []

for connection in child_connections:
    # Sort the connection to ensure order does not matter
    sorted_connection = tuple(sorted(connection))
    if sorted_connection not in seen:
        unique_connections.append(connection)
        seen.add(sorted_connection)
    
child_connections = unique_connections


#### delete collinear overlapping lines!






## save to json
data = {
    "child_connections": child_connections,
    "child_nodes": child_nodes
}

file_name = "temp.json"
with open(file_name, 'w') as json_file:
    json.dump(data, json_file)




# new script to check if connection is possible -> import -> the same logic will be used by mutation.py
# this script accounts for crossings only.