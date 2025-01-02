
import ga_modules
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
        [1.1, 1, 1], [4.3, 4, 3], [5.1, 5, 1], [0.0, 0, 0], [2.0, 2, 0], [4.0, 4, 0], [6.0, 6, 0]
    ],
    "connections": [
        [[0.0, 2.0], [2.0, 4.0], [4.0, 6.0], [4.2, 1.1], [1.1, 6.0], [6.1, 6.0], [1.1, 2.0], [2.0, 4.0], [4.0, 1.1], [1.1, 6.0], [6.0, 6.0], [2.0, 4.0], [4.2, 4.1], [4.1, 6.0], [6.0, 6.0]]
    ]
}

all_connections = [[0.0, 2.0], [2.0, 4.0], [4.0, 6.0], [4.2, 1.1], [1.1, 6.0], [6.1, 6.0], [1.1, 2.0], [2.0, 4.0], [4.0, 1.1], [1.1, 6.0], [6.0, 6.0], [2.0, 4.0], [4.2, 4.1], [4.1, 6.0], [6.0, 6.0]]
all_nodes = [[0.0, 0, 0], [2.0, 2, 0], [4.0, 4, 0], [6.0, 6, 0], [2.2, 2, 2], [6.1, 6, 1], [4.2, 4, 2], [1.1, 1, 1], [4.1, 4, 1], [5.0, 5, 0]]

'''
for connection in all_connections:
    id1, id2 = connection

    if ga_modules.connection_is_possible(id1, id2, all_connections, all_nodes, False) == True: # is also true if connections are on top of each other. prevent this!
        print("POSSIBLE", id1, id2)
    else:
        print("NO!", id1, id2)
'''








