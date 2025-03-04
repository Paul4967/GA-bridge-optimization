import ga_modules
import math
import truss_calculator
import copy


# weight = euclidean distance of each connection
# max_load = maximal force exerted on a connection

def calc_all_failure_forces(all_connections, forces, all_nodes, grid_size, material_yield_strenght, material_elastic_modulus, width):
    
    APPLIED_FORCE = 1000 #1kN

    CA = width ** 2 #cross-sectional area
    I = (width * (width ** 3)) / 12 #Moment of inertia
    K = 1.0 #Effective lenght factor (1.0 for pinned pinned)

    failure_forces = []
    
    for connection, force in zip(all_connections, forces.values()):

        if force > 0:
            # calc yield_force
            yield_force = material_yield_strenght * CA
            failure_forces.append(yield_force)

        elif force < 0:
            id1, id2 = connection
            x1, y1 = ga_modules.get_coords(id1, all_nodes)
            x2, y2 = ga_modules.get_coords(id2, all_nodes)
            # calculate distance
            lenght = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2)) * grid_size

            buckling_force = (math.pi**2 * material_elastic_modulus * I) / ((K * lenght)**2)
            failure_forces.append(buckling_force)

        else:
            failure_forces.append(0)

    failing_applied_forces = []
    for member_force, failure_force in zip(forces.values(), failure_forces):
        if member_force != 0:
            failing_applied_forces.append(failure_force / (member_force / APPLIED_FORCE))
        else:
            failing_applied_forces.append(float("inf"))


    return failing_applied_forces # max force that can be applied before one of the members is failing



def calc_truss_failure_force(all_connections, forces, all_nodes, grid_size, material_yield_strenght, material_elastic_modulus, width):
    
    APPLIED_FORCE = 1000 #1kN

    # material_yield_strenght = 0.06e9 #GPa
    # material_elastic_modulus = 3.6e9 #GPa

    # for squared beam:
    # width = 10e-3
    CA = width ** 2 #cross-sectional area
    I = (width * (width ** 3)) / 12 #Moment of inertia
    K = 1.0 #Effective lenght factor (1.0 for pinned pinned)

    failure_forces = []
    
    for connection, force in zip(all_connections, forces.values()):

        if force > 0:
            # calc yield_force
            yield_force = material_yield_strenght * CA
            failure_forces.append(yield_force)

        elif force < 0:
            id1, id2 = connection
            x1, y1 = ga_modules.get_coords(id1, all_nodes)
            x2, y2 = ga_modules.get_coords(id2, all_nodes)
            # calculate distance
            lenght = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2)) * grid_size

            buckling_force = (math.pi**2 * material_elastic_modulus * I) / ((K * lenght)**2)
            failure_forces.append(buckling_force)

        else:
            failure_forces.append(0)

    failing_applied_forces = []
    for member_force, failure_force in zip(forces.values(), failure_forces):
        if member_force != 0:
            failing_applied_forces.append(abs(failure_force / (member_force / APPLIED_FORCE)))
        else:
            failing_applied_forces.append(float("inf"))
    
    min_failure_force = min(failing_applied_forces)

    return failing_applied_forces, min_failure_force # max force that can be applied before one of the members is failing



def calc_fitness(all_connections, all_nodes, grid_size, material_yield_strenght, material_elastic_modulus, materials, loads, supports, width): #+ DISPLACEMENT_THRESHOLD AND max_force_ratio??


    # Create a dictionary to track the connections for each node
    connection_count = {node[0]: 0 for node in all_nodes}
    # Iterate through each connection and update the connection count
    for connection in all_connections:
        id1, id2 = connection
        if id1 in connection_count:
            connection_count[id1] += 1
        if id2 in connection_count:
            connection_count[id2] += 1

    
    # Check if any node is connected less than 2 times
    for _, count in connection_count.items():
        if count < 2:
            print("ERROR 404")
            return 0, 0, 0 #return fitness of 0

    # CHECK IF STABLE
    if ((len(all_nodes) * 2) - len(all_connections)) > 3:
        print("ERROR 303")
        return 0, 0, 0 #return fitness of 0
    

    ### ANALYZE TRUSS ### ---------------------------------------------------------------------------------------
    # convert input data
    converted_members, converted_nodes = analyze_truss(all_connections, all_nodes)

    # Analyze
    try:
        print(converted_members)
        displacements, forces, stress_strain = truss_calculator.analyze_truss(converted_nodes, converted_members, materials, loads, supports)
    except Exception as e:
        print(":DEBUG:", materials, "\nLOADS", loads, "\nSUPPORTS", supports)
        print(f"Error during truss analysis: {e}")
        print("ERROR 202")
        return 0, 0, 0


    # check for nodal displacement
    displacement_threshold = 1e+1 #10
    for _, displacement in displacements.items():
        if abs(displacement) > displacement_threshold:
            print("ERROR 101")
            return 0, 0, 0

    
    truss_failure_forces, truss_failure_force = calc_truss_failure_force(all_connections, forces, all_nodes, grid_size, material_yield_strenght, material_elastic_modulus, width)


    ### WEIGHT ### -----------------------------------------------------------
    weight = 0 # weight == total distance
    for connection in all_connections:
        id1, id2 = connection

        x1, y1 = ga_modules.get_coords(id1, all_nodes)
        x2, y2 = ga_modules.get_coords(id2, all_nodes)

        # calculate distance
        distance = math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))
        weight += distance


    all_failure_forces = calc_all_failure_forces(all_connections, forces, all_nodes, grid_size, material_yield_strenght, material_elastic_modulus, width)

    # pass to algorithm.py
    return weight, truss_failure_force, all_failure_forces



def analyze_truss(all_connections, all_nodes):
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


    return converted_members, converted_nodes
