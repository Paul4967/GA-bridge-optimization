

# weight = euclidean distance of each connection
# max_load = maximal force exerted on a connection -> is lenght important?
# is_connected = check if node is connected to (at least to or 3?) nodes. -> rewards in percentage of all beams (5 of 10 connected = 50%)

# IMPORT NODES AND CONNECTIONS -> NO! --> IMPORT FITNESS FUNCTION INTO CONTROLLER, AND PASS CONNECTIONS TO IT!

import ga_modules
import math
import truss_calculator
import copy


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

# all_connections = bridge["connections"] + base["connections"]
# all_nodes = bridge["nodes"] + base["nodes"]



def calc_fitness(all_connections, all_nodes):
    ### ANALYZE TRUSS ### ---------------------------------------------------------------------------------------

    ### convert node format ### -----------------------------------------

    all_nodes_ = copy.deepcopy(all_nodes)
    for index, node in enumerate(all_nodes_):
        node.insert(0, index + 1)
    print("NODES: ", all_nodes_)

    class Node:
        def __init__(self, id, x, y):
            self.id = id
            self.x = x
            self.y = y

        def __repr__(self):
            return f"Node({self.id}, {self.x}, {self.y})"
        
    # Transformation function
    def transform_nodes(data):
        new_nodes = []
        for index, (i, id, x, y) in enumerate(data, start=1):
            new_nodes.append(Node(index, x, y))
        return new_nodes

    # Convert to the new format
    converted_nodes = transform_nodes(all_nodes_)

    # Print the results
    for node in converted_nodes:
        print(node)


    ### convert connection format ### -----------------------------------------

    
    id_to_index = {node[1]: node[0] for node in all_nodes_}
    print("ID to Index Mapping:", id_to_index)
    all_connections_ = [
        [id_to_index[node_id] for node_id in connection] for connection in all_connections
    ]
    print("ALL C:", all_connections_)


    # Define the Member class
    class Member:
        def __init__(self, id, node1, node2, material_id):
            self.id = id
            self.node1 = node1
            self.node2 = node2
            self.material_id = material_id

        def __repr__(self):
            return f"Member({self.id}, {self.node1}, {self.node2}, {self.material_id})"

    # Transform connections into members
    def create_members(connections):
        members = []
        for index, (node1, node2) in enumerate(connections, start=1):
            members.append(Member(index, node1, node2, 1))
        return members

    # Convert to the desired format
    converted_members = create_members(all_connections_)

    # Print the results
    for member in converted_members:
        print(member)



    ### other inputs ###

    class Material:
        def __init__(self, id, E, A):
            self.id = id
            self.E = E  # Young's modulus
            self.A = A  # Cross-sectional area

    class Load:
        def __init__(self, node_id, fx, fy):
            self.node_id = node_id
            self.fx = fx
            self.fy = fy

    class Support:
        def __init__(self, node_id, x_support, y_support):
            self.node_id = node_id
            self.x_support = x_support
            self.y_support = y_support

    materials = [Material(1, 210E9, 0.0005625)]  # Using steel with E = 210 GPa and A = 0.01 m^2
    loads = [Load(5, 0, -1000), Load(6, 0, -1000)] # Applying a downward force of 980 N (100kg weight) at node 6
    supports = [Support(4, True, True), Support(7, False, True)] # Fixing both x and y displacements at node 4 and only y displacement at node 7.



    ### ANALYZE ###
    print(converted_members)
    displacements, forces, stress_strain = truss_calculator.analyze_truss(converted_nodes, converted_members, materials, loads, supports)

    print("Nodal Displacements:")
    for node, displacement in displacements.items():
        print(f"{node}: {displacement:.6e}")

    print("\nInternal Forces, Stress, and Strain:")
    for member_id, values in stress_strain.items():
        print(f"Member {member_id}: Force = {forces[member_id]:.6e} N, Stress = {values['stress']:.6e} Pa, Strain = {values['strain']:.6e}")






    ### FORCE VARIANCE ### ---------------------------------------------------

    # 1 Average Force
    avg_force = sum(abs(force) for force in forces.values()) / len(forces)
    print(f"avg Force: {avg_force:.6e} N")

    force_variance = sum((abs(force) - avg_force) ** 2 for force in forces.values()) / len(forces)
    print(f"Force Variance: {force_variance:.6e} N^2")
    # 2 Variance


    ### MAX FORCE ### --------------------------------------------------------
    max_absolute_force = max(abs(force) for force in forces.values())
    print(f"max abs Force: {max_absolute_force:.6e} N")


    ### WEIGHT ### -----------------------------------------------------------
    print(all_nodes)
    weight = 0 # weight == total distance
    for connection in all_connections:
        id1, id2 = connection

        x1, y1 = ga_modules.get_coords(id1, all_nodes)
        x2, y2 = ga_modules.get_coords(id2, all_nodes)

        # calculate distance
        distance = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))
        weight += distance

    print(f'Weight: {weight}')
        

    ### NOT CONNECTED PENALTY ### --------------------------------------------            ### UNFINISHED
    num_of_unconnected_nodes = 0
    for node in all_nodes: 
        if sum(node[0] in connection for connection in all_connections) < 2:
            num_of_unconnected_nodes += 1





    ### OVERALL FITNESS EQUATION ### -----------------------------------------
    # weights
    w1 = 1
    w2 = 1
    w3 = 1

    fitness = w1 * (1 /(1 + weight)) + (w2 * (1 / (1 + max_absolute_force)))  * (1 / (1 + force_variance))

    return fitness, weight, max_absolute_force


# print("RETUNR: ", calc_fitness(bridge["connections"] + base["connections"], bridge["nodes"] + base["nodes"]))
print("RETUNR 2: ", calc_fitness([[2.2, 2.0], [0.1, 0.0], [3.2, 6.0], [0.1, 2.2], [3.2, 2.2], [0.0, 2.2], [4.0, 3.2], [3.1, 3.2], [3.1, 2.0], [0.0, 2.0], [2.0, 4.0], [4.0, 6.0]], [[3.2, 3, 2], [2.2, 2, 2], [0.1, 0, 1], [3.1, 3, 1], [0.0, 0, 0], [2.0, 2, 0], [4.0, 4, 0], [6.0, 6, 0]]))
# all_connections = bridge["connections"] + base["connections"]
# all_nodes = bridge["nodes"] + base["nodes"]

###########################
###########################
###########################
###########################
###########################
###########################
###########################


def is_determinate(all_nodes, all_connections):
    # maybe schon durch truss analysis aussortiert
    ...


### not connected node penalty
### divide all penalties by amount of nodes or beams, to avoid bridges with less nodes / beams to score higher

# first calculate if stable, or unstalbe with m+r - 2j > 0 -> or just use truss force calc? -> test cases!