# 1 place random amount of nodes randomly in build domain (max node amount calculated by area of build domain)
# 2 draw random amount of connections between nodes -> check if possible

import random
import ga_modules
import json
import importlib
importlib.reload(ga_modules)

def node_is_existing(node_x, node_y, bridge_nodes):
    for node in bridge_nodes:
        if node[1] == node_x and node[2] == node_y:
            return True
    return False

def node_intersecting_connection(node_x, node_y, base_connections, base_nodes):
    for connection in base_connections:
        x1, y1 = ga_modules.get_coords(connection[0], base_nodes)
        x2, y2 = ga_modules.get_coords(connection[1], base_nodes)

        # Check if the node lies within the bounds of the connection
        in_bound_of_connection = (
            (x1 == x2 and min(y1, y2) <= node_y <= max(y1, y2) and node_x == x1) or  # Vertical connection
            (y1 == y2 and min(x1, x2) <= node_x <= max(x1, x2) and node_y == y1) or  # Horizontal connection 
            (min(x1, x2) <= node_x <= max(x1, x2) and min(y1, y2) <= node_y <= max(y1, y2))  # Diagonal connection
        )
        if abs(x1*(y2 - node_y) + x2*(node_y - y1) + node_x*(y1 - y2)) == 0 and in_bound_of_connection:  # calculate triangle area
            print(f'connection {x1, y1}, {x2, y2} is crossing with point: {node_x, node_y}')
            return True
    return False


'''
base = {
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

base_nodes = base["nodes"]
base_connections = base["connections"]



build_domain = 6, 2 # bottom and left are always at 0



max_node_percentage = 0.6    # basenodes are excluded
min_node_percentage = 0.25
'''

def initialize(base_nodes, base_connections, min_node_percentage, max_node_percentage, build_domain):
    build_domain_x = build_domain[0]
    build_domain_y = build_domain[1]


    node_num = round(random.uniform(min_node_percentage, max_node_percentage) * (build_domain_x * build_domain_y))

    bridge_nodes = []
    i = 0
    while i < node_num:
        # generate random nodes
        node_x = random.randint(0, round(build_domain_x)) # ERROR HERE?
        node_y = random.randint(0, round(build_domain_y))

        if node_is_existing(node_x, node_y, bridge_nodes) or node_intersecting_connection(node_x, node_y, base_connections, base_nodes): 
            continue # pick other random coords             #### or move node on x and then on y axis to next free spot

        node = [
            ga_modules.generate_id(node_x, node_y),
            node_x, 
            node_y
        ]
        bridge_nodes.append(node)
        i += 1




    ###### how can it still be basenode?: NODES:  [[1.2, 1, 2], [5.1, 5, 1], [2.0, 2, 0], [3.2, 3, 2], [0.1, 0, 1], [4.0, 4, 0], [6.1, 6, 1]]
    ###### -> because only checked if it lies on connection and not on point
    '''NODE PLACEMENT: shuffled list with all possible locations. select first few nodes'''





    ### make random connections ### ------------------------------------------------


    bridge_connections = []
    all_connections = base_connections + bridge_connections
    all_nodes = bridge_nodes + base_nodes
    # connect_to = bridge_nodes[:]
    for _ in range(2):
        for node in bridge_nodes:
            id1 = node[0]
            random.shuffle(all_nodes)
            for next_node in all_nodes:
                id2 = next_node[0]
                if ga_modules_old.connection_is_possible(id1, id2, all_connections, all_nodes, False) is False or id1 is id2:
                    continue
                else:
                    new_connection = [id1, id2]
                    bridge_connections.append(new_connection)
                    all_connections.append(new_connection)
                    break
    
    for _ in range(2):
        for node in base_nodes:
                id1 = node[0]
                random.shuffle(all_nodes)
                for next_node in all_nodes:
                    id2 = next_node[0]
                    if ga_modules_old.connection_is_possible(id1, id2, all_connections, all_nodes, False) is False or id1 is id2:
                        continue
                    else:
                        new_connection = [id1, id2]
                        bridge_connections.append(new_connection)
                        all_connections.append(new_connection)
                        break

    print("ALL CONNECTIONS: ", all_connections)
    print("CONNECTIONS: ", bridge_connections)
    print("NODES: ", bridge_nodes)
    return bridge_nodes, bridge_connections





### DEBUG ### --------------------------------------------------------
base_nodes = [[0.0, 0, 0], [20.0, 2, 0], [40.0, 4, 0], [60.0, 6, 0], [80.0, 8, 0], [100.0, 10, 0]]
base_connections = [[0.0, 20.0], [20.0, 40.0], [40.0, 60.0], [60.0, 80.0], [80.0, 100.0]]
# build_domain = 100, 30
build_domain = 10 / 0.1, 3 / 0.1
print(initialize(base_nodes, base_connections, 0.01, 0.01, build_domain))
print("RESULT")



### EXPORT ### --------------------------------------------------------
'''
data = {
    "all_connections": all_connections,
    "all_nodes": all_nodes
}

# Save the data to a json file
file_path = 'connections_and_nodes.json'
with open(file_path, 'w') as f:
    json.dump(data, f)

file_path

print("saved to file")



### Initialization finished

'''