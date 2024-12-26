
# shift random nodes randomly (set max distance)
# set max and min distance
# set step / snap (e.g. snap to 0.25 grid)
# set probability for each individual node to be shifted
# if connection is not possible afterwards, shift in other directions, till it works. otherwise dont shift. (then increase probability for other nodes?)

# create new, or delete connections
# 10 connections: each one has 5% probability to be deleted -> 10*5 = 50%
# 1. decide on deleting or not, then if yes (50% probability) delete 1 random connection
# checking if connection is possible is important.
# -> if connection exists or crosses other connection, try for next point, till tried to connect every point with each other point.
