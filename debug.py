import ga_modules

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
        [2.1, 2, 1] #
    ],
    "connections": [
        [0.0, 1.1],
        [2.0, 1.1],
        [2.0, 3.1],
        [4.0, 3.1],
        [4.0, 5.1],
        [6.0, 5.1],
        # [1.1, 3.1],
        [3.1, 5.1],
    ]
}

all_connections = base["connections"] + bridge["connections"]
all_nodes = base["nodes"] + bridge["nodes"]

if ga_modules.connection_is_possible(1.1, 0.0, all_connections, all_nodes):
    print("POSSIBLE")
else:
    print("NO!")


child_connections = [
    connection for connection in bridge["connections"]
    if ga_modules.connection_is_possible(connection[0], connection[1], all_connections, all_nodes)
]

print("Filtered child_connections:", child_connections)

# i know the problem. it also checks the existing connection!