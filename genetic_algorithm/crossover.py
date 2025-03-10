# Crossover
import random
import math
import json
import ga_modules

def crossover(base_nodes, base_connections, bridge1_nodes, bridge2_nodes, bridge1_connections, bridge2_connections):

    all_nodes = bridge1_nodes + bridge2_nodes

    # remove basenodes
    base_ids = {node[0] for node in base_nodes}
    filtered_nodes = [node for node in all_nodes if node[0] not in base_ids]
    all_nodes = filtered_nodes
    # ----------------------------------------------

    child_nodes = []
    seen = []

    # create copy and shuffle
    shuffled_nodes = all_nodes[:]
    random.shuffle(shuffled_nodes)

    # select first 50% of shuffled list
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
        

    all_connections = bridge1_connections + bridge2_connections

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
    base_node_ids = [node[0] for node in base_nodes]

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
            child_available_nodes = child_nodes + base_nodes
            print("AVAILABLE NODES:", child_available_nodes)

            # find closest node
            closest_node = min(
                (node for node in child_available_nodes if node[1] != ex or node[2] != ey),
                key=lambda node: math.sqrt(((node[1] - mx) ** 2) + ((node[2] - my) ** 2))
            )
            print(f'{mx, my} closest node: {closest_node}')
            _, x, y = closest_node
                    
            # overwrite old connection
            for i, connection in enumerate(child_connections):
                [id1_, id2_] = connection
                if id1_ == id1 and id2_ == id2:
                    child_connections[i] = [ga_modules.generate_id(x, y), ga_modules.generate_id(ex, ey)]
                    print("fixed connection: ", child_connections[i])

                    break
        

    ### CHECK IF CONNECTION IS POSSIBLE ### ------------------------------
    all_available_connections = child_connections + base_connections
    all__nodes = child_nodes + base_nodes

    i = 0
    while i < len(child_connections):
        id1, id2 = child_connections[i]

        result = ga_modules.connection_is_possible(id1, id2, ga_modules.filter_connections(id1, id2, all_available_connections), all__nodes, True)
        if result is False:
            del child_connections[i]
            del all_available_connections[i]
        elif isinstance(result, tuple) and len(result) == 2:
            del child_connections[i]
            del all_available_connections[i]
            c1, c2 = result
            child_connections.append(c1)
            child_connections.append(c2)
            all_available_connections.append(c1)
            all_available_connections.append(c2)
            #--------------------------------------------------------

        else:
            i += 1


    seen = set()
    unique_connections = []

    for connection in child_connections:
        # Sort the connection to ensure order does not matter
        sorted_connection = tuple(sorted(connection))
        if sorted_connection not in seen:
            unique_connections.append(connection)
            seen.add(sorted_connection)
        
    child_connections = unique_connections

    return child_nodes, child_connections
