# Crossover
import random

base_nodes = {
    "nodes": [
        [0.0, 0, 0],
        [2.0, 2, 0],
        [4.0, 4, 0],
        [6.0, 6, 0],
        # ["b1", 0, 0],
        # ["b2", 2, 0],
        # ["b3", 4, 0],
        # ["b4", 6, 0],
    ]
}

bridge1 = {
    "nodes": [
        [1.1, 1, 1],
        [3.1, 3, 1],
        [5.1, 5, 1]
    ],
    "connections": [
        [0.0, 1.2],
        [1.2, 2.1],
        [2.1, 2.0],
        [2.1, 4.0],
        [1.2, 5.2],
        [5.2, 4.0],
        [5.2, 6.0],
    ]
}

bridge2 = {
    "nodes": [
        [1.1, 1, 1],
        [3.1, 3, 1],
        [5.1, 5, 1]
    ],
    "connections": [
        [0.0, 1.1],
        [2.0, 1.1],
        [2.0, 3.1],
        [4.0, 3.1],
        [4.0, 5.1],
        [6.0, 5.1],
        [1.1, 3.1],
        [3.1, 5.1],
    ]
}


# merge nodes of parent 1 and 2
all_nodes = bridge1["nodes"] + bridge2["nodes"]


def select_random_nodes(nodes):
    child_nodes = []
    seen = []

    # create copy and shuffle
    shuffled_nodes = nodes[:]
    random.shuffle(shuffled_nodes)


    # select first 50% of shuffled array
    a = 0
    i = 0
    average_node_num = len(nodes) // 2
    while i < average_node_num + a:
        
        # check if object is seen & append if not
        if shuffled_nodes[i] in seen:
            a+=1
        
        else:
            child_nodes.append(shuffled_nodes[i])
        
        seen.append(shuffled_nodes[i])
        i+=1
     
    print("all nodes: ", all_nodes)
    print("shullfed Nodes:", shuffled_nodes)
    print("seen", seen)
    print("child nodes:     ", child_nodes)

    return child_nodes

# call the above function
child_nodes = select_random_nodes(all_nodes)

print(child_nodes)