import mutation
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
        #[4.0, 3.1],
        [4.0, 5.1],
        [6.0, 5.1],
        [1.1, 3.1],
        [3.1, 5.1]
    ]
}













mutate_node_probability = 1
mutate_connection_probability = 1
max_node_offset_multiplier = 1
grid_size = 1
build_area = 6, 3
bridge_nodes = bridge["nodes"]
base_nodes = base["nodes"]
bridge_connections = bridge["connections"]
base_connections = base["connections"]
max_mutation_amplifier = 1
min_mutation_amplifier = 1
all_connections = bridge_connections + base_connections
all_nodes = bridge_nodes + base_nodes


for _ in range(100):
    bridge_connections_copy = copy.deepcopy(bridge_connections)
    bridge_nodes_copy = copy.deepcopy(bridge_nodes)
    all_connections_copy = copy.deepcopy(all_connections)
    all_nodes_copy = copy.deepcopy(all_nodes)

    bridge_connections_, bridge_nodes_ = mutation.mutate(
        mutate_node_probability, mutate_connection_probability, max_node_offset_multiplier, grid_size, build_area,
        bridge_nodes_copy, base_nodes, bridge_connections_copy, base_connections, max_mutation_amplifier, min_mutation_amplifier, all_connections_copy, all_nodes_copy
    )




all_connections = [[0.0, 2.0], [2.0, 4.0], [4.0, 6.0], [5.2, 4.0], [2.2, 0.1], [0.1, 0.0], [6.0, 5.2], [5.2, 2.2], [2.2, 4.0]]
all_nodes = [[0.0, 0, 0], [2.0, 2, 0], [4.0, 4, 0], [6.0, 6, 0], [0.1, 0, 1], [5.2, 5, 2], [2.2, 2, 2]]

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
