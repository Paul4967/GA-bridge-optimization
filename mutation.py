import random
import ga_modules
import copy
import json




        



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

bridge = {
    "nodes": [
        [1.1, 1, 1],
        [3.1, 3, 1],
        [5.1, 5, 1],
        # [2.1, 2, 1]
    ],
    "connections": [
        [0.0, 1.1],
        [2.0, 1.1],
        [2.0, 3.1],
        [4.0, 3.1],
        [4.0, 5.1],
        [6.0, 5.1],
        [1.1, 3.1],
        [3.1, 5.1]
    ]
}



bridge_connections = bridge["connections"]
all_connections = bridge["connections"] + base["connections"]

base_nodes = base["nodes"]
bridge_nodes = bridge["nodes"]
available_nodes = bridge_nodes + base_nodes



mutate_connection_probability = 1 # in range 0 to 1

if random.random() < mutate_connection_probability:  # random.random() generates a float in [0, 1)
    print("mutating")

    # add or remove random connection

    if random.randint(0,1) == 0:
        #remove connection
        del bridge_connections[random.randint(0, len(bridge_connections) - 1)]
        all_connections = bridge_connections + base["connections"]
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
                if ga_modules.connection_is_possible(id1, id2, all_connections, available_nodes, False):
                    connection_found = True
                    break               

                j += 1

            i += 1
        
        if connection_found:
            new_connection = [id1, id2]
            bridge_connections.append(new_connection)
            all_connections = bridge_connections + base["connections"]
            print("new connection at: ", id1, id2)
        else:
            print("NO CONNECTION POSSIBLE")



# 
# MUTATE POINTS (check for each connection that connects to mutated point if it is still possible. if not, move point in other direction / move other point) 
#


def delete_node():
    node_to_delete = random.choice(bridge_nodes)
    bridge_nodes.remove(node_to_delete)
    available_nodes.remove(node_to_delete)


def mutate_node(bridge_nodes, all_connections, base_nodes, available_nodes):
    mutate_node_probability = 1 # deal with this outside of function
    max_num_of_nodes_to_mutate = 2
    max_node_offset_multiplier = 1
    build_domain = 6, 4 # x, y

    grid_size = 1
    max_shift_distance = max_node_offset_multiplier * (1 / grid_size)

    old_id, x, y = random.choice(bridge_nodes)

    # MOVE NODE (edit coords)
    # in 1 of 8 directions multiplied by random step size
    directions = [
        (-1, 0),  # Left
        (1, 0),   # Right
        (0, 1),   # Up
        (0, -1),  # Down
        (-1, 1),  # Left + Up (Top-left diagonal)
        (-1, -1), # Left + Down (Bottom-left diagonal)
        (1, 1),   # Right + Up (Top-right diagonal)
        (1, -1)   # Right + Down (Bottom-right diagonal)
    ]
    
    random.shuffle(directions)
    node_offset_multiplier = random.randint(1, round(max_shift_distance)) # rounding beacause max shift distance is a float like this: 1.0

    
    # left_nodes = [node for node in available_nodes if node not in old]

    is_possible = False
    for dx, dy in directions:

        # get all connections of this node ALL CONNECTIONS TO THIS NODE NEED TO BE ADAPTED!!!
        affected_connections = [
            [id1, id2] for (id1, id2) in bridge_connections 
            if id1 == old_id or id2 == old_id
        ]
        print(old_id)
        print("BR C:", bridge_connections)
        print("AF C:", affected_connections)

        # all_connection except affected connections
        left_connections = [connection for connection in all_connections if connection not in affected_connections]



        new_x = x + dx * node_offset_multiplier
        new_y = y + dy * node_offset_multiplier
        if new_x > build_domain[0] or new_y > build_domain[1] or new_x < 0 or new_y < 0:  # inside domain?
            print("not working for:", new_x, new_y)
            continue

        new_id = new_x + new_y / (10 ** len(str(int(new_y))))  
        # Replace the node with old_id by new_id
        new_nodes = copy.deepcopy(available_nodes)
        for i, node in enumerate(new_nodes):
            if node[0] == old_id:
                new_nodes[i] = [new_id, new_x, new_y]  # Update node
                break

        
        # reroute affected connections
        print("AFFECTED C: ", affected_connections) # AFFECTED CONNECTIONS WIRD NICHT NEU BESTIMMT!
        for connection in affected_connections:
            if connection[0] == old_id:
                connection[0] = new_id
            else:
                connection[1] = new_id
        print(affected_connections)
        print("old id: ", old_id, "NEW ID:", new_id)
        print("OLD NODES: ", available_nodes)
        print("NEW NODES: ", new_nodes)
        new_connections = left_connections + affected_connections
        print("NEW CCC: ", new_connections)

        for connection in affected_connections:
            id1, id2 = connection
            print("DEBUG", id1, id2) # correct
            print("DEBUG 2: ", new_nodes)
            if ga_modules.connection_is_possible(id1, id2, new_connections, new_nodes, False): # is also true if connections overlay
                print("POSSIBLE")
                is_possible = True
            else:
                is_possible = False
                print(f'NOT POSSIBLE FOR: old: {old_id}, new: {new_id}')
                # return False # dont return false! -> try for other dx / dy
                break
        if is_possible: # this can be deletet and directly incorporated into script
            bridge_nodes = new_nodes
            available_nodes = base_nodes + bridge_nodes
            return new_connections, available_nodes
    return False
                             
    # return False

result = mutate_node(bridge_nodes, all_connections, base_nodes, available_nodes)

if result is not False:  # Proceed only if the function does not return False
    all_connections, available_nodes = result
   



### NEW ID CANT BE A EXISTING ID!!!

### SOME KIND OF ERROR; WHERE CORD CANT BE RETRIEVED

# Errors: -> old id not overwritten
# connection with same id -> e.g. 4.0, 4.0


############ NODES ALSO NEED TO BE ABLE TO BE DELETED OR CREATED!!!

'''-> create new node, and then draw between 2 and 4 connections to closest nodes -> at least connecting to the 1/2 closest is possible!'''
'''-> deleting nodes: reconnect connections to closest nodes (as in recombination) -> delete overlapping/ not possible connections'''



### EXPORT ### --------------------------------------------------------

data = {
    "all_connections": all_connections,
    "all_nodes": available_nodes
}

# Save the data to a json file
file_path = 'connections_and_nodes.json'
with open(file_path, 'w') as f:
    json.dump(data, f)

file_path

print("saved to file")


### MUTATION IS RUNNING (have i implemented creating new beams?)