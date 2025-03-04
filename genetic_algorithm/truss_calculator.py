import numpy as np
import time
start_time = time.perf_counter()

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Member:
    def __init__(self, id, node1, node2, material_id):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.material_id = material_id

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

def assemble_stiffness_matrix(nodes, members, materials):
    num_dof = 2 * len(nodes)
    K_global = np.zeros((num_dof, num_dof))

    for member in members:
        n1 = nodes[member.node1 - 1]
        n2 = nodes[member.node2 - 1]
        material = materials[member.material_id - 1]
        
        L = np.sqrt((n2.x - n1.x)**2 + (n2.y - n1.y)**2)
        c = (n2.x - n1.x) / L
        s = (n2.y - n1.y) / L

        k_local = (material.E * material.A / L) * np.array([
            [ c*c,  c*s, -c*c, -c*s],
            [ c*s,  s*s, -c*s, -s*s],
            [-c*c, -c*s,  c*c,  c*s],
            [-c*s, -s*s,  c*s,  s*s]
        ])

        indices = [2*(member.node1-1), 2*(member.node1-1)+1, 2*(member.node2-1), 2*(member.node2-1)+1]

        for i in range(4):
            for j in range(4):
                K_global[indices[i], indices[j]] += k_local[i, j]

    return K_global

def apply_supports(K_global, supports):
    for support in supports:
        node_id = support.node_id - 1
        if support.x_support:
            K_global[2*node_id, :] = 0
            K_global[:, 2*node_id] = 0
            K_global[2*node_id, 2*node_id] = 1
        if support.y_support:
            K_global[2*node_id+1, :] = 0
            K_global[:, 2*node_id+1] = 0
            K_global[2*node_id+1, 2*node_id+1] = 1
    return K_global

def assemble_load_vector(nodes, loads):
    F = np.zeros(2 * len(nodes))
    for load in loads:
        node_id = load.node_id - 1
        F[2*node_id] = load.fx
        F[2*node_id + 1] = load.fy
    return F

def solve_displacements(K, F):
    try: 
        displacements = np.linalg.solve(K, F)
        return displacements
    except np.linalg.LinAlgError:
        print("Error: Singular matrix - truss not solvable.")
        return None  # or any other indicator like 'truss_not_solvable'

def calculate_internal_forces(members, materials, displacements, nodes):
    internal_forces = {}
    for member in members:
        material = materials[member.material_id - 1]
        n1 = nodes[member.node1 - 1]
        n2 = nodes[member.node2 - 1]

        u1 = displacements[2*(member.node1-1):2*(member.node1-1)+2]
        u2 = displacements[2*(member.node2-1):2*(member.node2-1)+2]

        L = np.sqrt((n2.x - n1.x)**2 + (n2.y - n1.y)**2)
        c = (n2.x - n1.x) / L
        s = (n2.y - n1.y) / L

        delta = np.dot([-c, -s, c, s], np.hstack([u1, u2]))
        N = material.E * material.A * delta / L
        internal_forces[member.id] = N
    return internal_forces


def compute_stress_strain(members, materials, internal_forces):
    stress_strain = {}
    for member in members:
        material = materials[member.material_id - 1]
        force = internal_forces[member.id]
        stress = force / material.A
        strain = stress / material.E
        stress_strain[member.id] = {"stress": stress, "strain": strain}
    return stress_strain

def format_nodal_displacements(nodal_displacements):
    formatted_displacements = {}
    for i, displacement in enumerate(nodal_displacements):
        node_id = i // 2 + 1
        direction = 'x' if i % 2 == 0 else 'y'
        formatted_displacements[f'Node {node_id} {direction}'] = displacement
    return formatted_displacements

# Modify the main analysis workflow to include stress and strain calculations
def analyze_truss(nodes, members, materials, loads, supports):
    K_global = assemble_stiffness_matrix(nodes, members, materials)
    K_global = apply_supports(K_global, supports)
    F = assemble_load_vector(nodes, loads)
    displacements = solve_displacements(K_global, F)
    forces = calculate_internal_forces(members, materials, displacements, nodes)
    stress_strain = compute_stress_strain(members, materials, forces)
    formatted_displacements = format_nodal_displacements(displacements)
    return formatted_displacements, forces, stress_strain


end_time = time.perf_counter()

execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")