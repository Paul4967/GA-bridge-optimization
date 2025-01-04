import random
import ga_modules
import copy
import json
import initialization
import itertools


        


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
all_nodes = bridge_nodes + base_nodes

'''


def filter_connections(id1, id2, all_connections):
    removed = False
    filtered_connections = []
    for connection in all_connections:
        if not removed and connection[0] == id1 and connection[1] == id2:
            removed = True
            continue  # Skip this connection
        filtered_connections.append(connection)

    return filtered_connections

#remove connection
def remove_connection(bridge_connections):
    del bridge_connections[random.randint(0, len(bridge_connections) - 1)]
    print("connection deleted")
    return bridge_connections

# ADD CONNECTION

def create_connection(all_nodes, all_connections, bridge_connections):
    #randomly select node (can be basenode too)
    random.shuffle(all_nodes)

    connection_found = False
    i = 0
    while not connection_found and i < len(all_nodes):    # iterate through all nodes
        id1, _, _ = all_nodes[i]

        j = 0
        while not connection_found and j < len(all_nodes):
            if j == i:  # if id1 is id2
                j += 1
                continue

            id2, _, _ = all_nodes[j]
            if ga_modules.connection_is_possible(id1, id2, all_connections, all_nodes, False):
                connection_found = True
                break               

            j += 1

        i += 1

    if connection_found:
        new_connection = [id1, id2]
        bridge_connections.append(new_connection)
        print("new connection at: ", id1, id2)
        return bridge_connections
    else:
        print("NO CONNECTION POSSIBLE")
        return False




### NODE MUTATION ### ----------------------------------------------- 



def delete_node(bridge_nodes, all_nodes, bridge_connections):
    node_to_delete = random.choice(bridge_nodes)
    bridge_nodes.remove(node_to_delete)
    all_nodes.remove(node_to_delete)

    # delete all beams connected with deleted node
    updated_bridge_connections = [connection for connection in bridge_connections if node_to_delete[0] not in connection]
    return updated_bridge_connections, bridge_nodes, all_nodes



def mutate_node(bridge_nodes, bridge_connections, base_nodes, all_nodes, base_connections, build_area, grid_size, max_node_offset_multiplier):
    
    # max_node_offset_multiplier = 1
    # build_area = 6, 4 # x, y
    # grid_size = 1

    max_shift_distance = max_node_offset_multiplier

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

    
    # left_nodes = [node for node in all_nodes if node not in old]

    is_possible = False
    for dx, dy in directions:
        temp_bridge_connections = copy.deepcopy(bridge_connections)

        # get all connections of this node ALL CONNECTIONS TO THIS NODE NEED TO BE ADAPTED!!!
        affected_connections = [
            [id1, id2] for (id1, id2) in bridge_connections 
            if id1 == old_id or id2 == old_id
        ]
        print(old_id)
        print("BR C:", bridge_connections)
        print("AF C:", affected_connections)

        # all_connection except affected connections
        remaining_bridge_connections = [connection for connection in bridge_connections if connection not in affected_connections]



        new_x = x + dx * node_offset_multiplier
        new_y = y + dy * node_offset_multiplier
        if new_x > build_area[0] or new_y > build_area[1] or new_x < 0 or new_y < 0:  # inside domain?
            print("not working for:", new_x, new_y)
            continue

        new_id = new_x + new_y / (10 ** len(str(int(new_y))))  
        # Replace the node with old_id by new_id
        new_nodes = copy.deepcopy(all_nodes)
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
        print("OLD NODES: ", all_nodes)
        print("NEW NODES: ", new_nodes)
        new_connections = base_connections + remaining_bridge_connections + affected_connections # all connections
        temp_bridge_connections = remaining_bridge_connections + affected_connections
        print("NEW CCC: ", new_connections)

        # not executet if affected_connections is empty, but why is it?!
        for connection in affected_connections:
            id1, id2 = connection

            new_connections = filter_connections(id1, id2, new_connections)

            print("DEBUG", id1, id2) # correct
            print("DEBUG 2: ", new_nodes)
            if ga_modules.connection_is_possible(id1, id2, new_connections, new_nodes, False): # is also true if connections overlay
                print("POSSIBLE")
                bridge_connections = temp_bridge_connections
                is_possible = True
            else:
                is_possible = False
                print(f'NOT POSSIBLE FOR: old: {old_id}, new: {new_id}')
                # return False # dont return false! -> try for other dx / dy
                break
        if is_possible: # this can be deletet and directly incorporated into script
            # Convert to sets of tuples
            all_nodes_set = set(map(tuple, all_nodes))
            base_nodes_set = set(map(tuple, base_nodes))

            # Subtract the sets
            result_set = all_nodes_set - base_nodes_set
            bridge_nodes = list(map(list, result_set))

            all_nodes = base_nodes + bridge_nodes
            return new_connections, all_nodes, bridge_connections, bridge_nodes
    return False
                             



def create_node(build_area, all_nodes, all_connections, base_connections, bridge_connections, base_nodes, bridge_nodes):
    # 1 place node at random possible point
    # draw 2 connections from this node (at least 3 are possible)
    # allow cutting
    # temp_all_nodes = copy.deepcopy(all_nodes)
    
    existing_coords = {(node[1], node[2]) for node in all_nodes}
    possible_coords = [
        (x, y)
        for x, y in itertools.product(range(build_area[0] + 1), range(build_area[1] + 1))
    ]

    available_coords = [coord for coord in possible_coords if coord not in existing_coords]
    random.shuffle(available_coords)

    node = []
    node_found = False
    for coord in available_coords:
        node_x = coord[0]
        node_y = coord[1]

        if initialization.node_is_existing(node_x, node_y, bridge_nodes) or initialization.node_intersecting_connection(node_x, node_y, all_connections, all_nodes): 
            continue

        node = [
            node_x + node_y / (10 ** len(str(int(node_y)))), # id, x, y
            node_x, 
            node_y
        ]
        bridge_nodes.append(node)
        all_nodes.append(node)
        node_found = True
        break
    if node_found is False:
        return False

    # CREATE CONNECTIONS
    for _ in range(2):  
        id1 = node[0]
        random.shuffle(all_nodes)
        for next_node in all_nodes:
            id2 = next_node[0]
            if ga_modules.connection_is_possible(id1, id2, all_connections, all_nodes, False) is False or id1 is id2:
                continue
            else:
                new_connection = [id1, id2]
                bridge_connections.append(new_connection)
                all_connections.append(new_connection)
                break
    return bridge_connections, bridge_nodes
    





### NEW ID CANT BE A EXISTING ID!!!

### SOME KIND OF ERROR; WHERE CORD CANT BE RETRIEVED

# Errors: -> old id not overwritten
# connection with same id -> e.g. 4.0, 4.0


############ NODES ALSO NEED TO BE ABLE TO BE DELETED OR CREATED!!!






### MUTATION HANDLER ### ------------------------------------

def mutate(mutate_node_probability, mutate_connection_probability, max_node_offset_multiplier, grid_size, build_area, 
           bridge_nodes, base_nodes, bridge_connections, base_connections, max_mutation_amplifier, min_mutation_amplifier, all_connections, all_nodes):
    # amplifier: how many times can a node be deleted for example
    # all_connections = base_connections + bridge_connections
    # all_nodes = base_nodes + bridge_nodes

    mutation_amplifier = random.randint(min_mutation_amplifier, max_mutation_amplifier)

    delete_c = False
    create_c = False
    move_node = False
    del_n = False
    create_n = False

    for _ in range(mutation_amplifier):

        
        if random.random() < mutate_connection_probability:
            delete_c = True
            # delete connection
            bridge_connections = remove_connection(bridge_connections)
            all_connections = base_connections + bridge_connections
        
        '''
        if random.random() < mutate_connection_probability:
            # create connection
            updated_bridge_connections = create_connection(all_nodes, all_connections, bridge_connections)
            if updated_bridge_connections is not False:
                print("CONNECTION POSSIBLE")
                bridge_connections = updated_bridge_connections
                all_connections = base_connections + bridge_connections
                create_c = True
        '''
        
        # node mutation
        if random.random() < mutate_node_probability:
            del_n = True
            # delete node (and associated connections)
            bridge_connections, bridge_nodes, all_nodes = delete_node(bridge_nodes, all_nodes, bridge_connections)
            all_connections = base_connections + bridge_connections

        
        
        if random.random() < mutate_node_probability:
            # create random node
            result = create_node(build_area, all_nodes, all_connections, base_connections, bridge_connections, base_nodes, bridge_nodes)
            if result is not False:
                bridge_connections, bridge_nodes = result
                all_connections = base_connections + bridge_connections
                all_nodes = base_nodes + bridge_nodes
                create_n = True
        
        
        if random.random() < mutate_node_probability:
            # mutate node
            result = mutate_node(bridge_nodes, bridge_connections, base_nodes, all_nodes, base_connections, build_area, grid_size, max_node_offset_multiplier)
            if result is not False:  # Proceed only if the function does not return False
                all_connections, all_nodes, bridge_connections, bridge_nodes = result
                print("MUTATED NODE")
                move_node = True
        
    print(f'C del: {delete_c}|| C created: {create_c}|| N del: {del_n}|| N created: {create_n}|| N moved: {move_node}')
    return bridge_connections, bridge_nodes


            














'''
all_connections = mutate


### EXPORT ### --------------------------------------------------------

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


### MUTATION IS RUNNING (have i implemented creating new beams?)
'''