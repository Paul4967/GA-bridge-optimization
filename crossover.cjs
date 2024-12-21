
//basenodes: define nodes seperately [base1,0,0],[base2,4,0],...
//-> if node id inside of connection starts with b, then leave it.



const baseNodes = {
    nodes: [
        [0.0,0,0],
        [2.0,2,0],
        [4.0,4,0],
        [6.0,6,0],
        /*
        ["b1",0,0],
        ["b2",2,0],
        ["b3",4,0],
        ["b4",6,0],
        */
    ]
};

const bridge1 = {
    nodes: [
        [1.2, 1, 2],
        [2.1, 2, 1],
        [5.2, 5, 2]
    ],
    connections: [
        [0.0, 1.2],
        [1.2, 2.1],
        [2.1, 2.0],
        [2.1, 4.0],
        [1.2, 5.2],
        [5.2, 4.0],
        [5.2, 6.0],
    ]
};

const bridge2 = {
    nodes: [
        [1.1, 1, 1],
        [3.1, 3, 1],
        [5.1, 5, 1]
    ],
    connections: [
        [0.0, 1.1],
        [2.0, 1.1],
        [2.0, 3.1],
        [4.0, 3.1],
        [4.0, 5.1],
        [6.0, 5.1],
        [1.1, 3.1],
        [3.1, 5.1],
    ]
};



// Merge nodes from both bridges
const allNodes = [...bridge1.nodes, ...bridge2.nodes];


// Function to randomly select 50% of the nodes
function selectRandomNodes(nodes) {

    const childNodes = [];
    const seen = [];

    // Create a copy of the array and shuffle it
    const shuffledNodes = nodes.slice();
    for (let i = shuffledNodes.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledNodes[i], shuffledNodes[j]] = [shuffledNodes[j], shuffledNodes[i]]; // Swap elements
    }

    // Select the first 50% of the shuffled array
    var a = 0
    for (let i = 0; i < Math.floor(nodes.length / 2) + a; i++) {
        
        // Check if the object has already been added
        if (seen.some(s => JSON.stringify(s) === JSON.stringify(shuffledNodes[i]))) {
            console.log('node already existing');
            a++;
        } else {
            console.log('node is new');
            childNodes.push(shuffledNodes[i]);
        }

    seen.push(shuffledNodes[i]);
        
    }

    console.log("shuffledNodes:", shuffledNodes); ///DEBUG
    console.log("seen:", seen);

    return childNodes;
}



// Select 50% of the nodes
const childNodes = selectRandomNodes(allNodes);

// Output the result
console.log('Child nodes:', childNodes);











///
/// List all Connections in new Array
///

var childConnections = [];
const allConnections = [...bridge1.connections, ...bridge2.connections];

//1 select connections with nodeIDs that are still available
//2 reconnect broken ones to closest node (not the one it is alreade connected to with the other end)
//2 chech if double (can be possible)
// crossings -> macht kein sinn da punkt zu erstellen, wenn punkte auf grid sein müssen. -> crossings löschen?

const validIds = childNodes.map(node => node[0]);

// Filter the main array
const filteredArray = allConnections.filter(([id1, id2]) => 
  validIds.includes(id1) || validIds.includes(id2)
);

console.log("Available Connections: ", filteredArray);

//
//FIX CONNECTIONS
//FIX CONNECTIONS

const baseNodeIds = baseNodes.nodes.map(node => node[0]);

childConnections = [...filteredArray]; // This creates a shallow copy of the array

filteredArray.forEach(([id1, id2]) => {                                                         //HIER ANSETZEN
  const id1Exists = validIds.includes(id1);
  const id2Exists = validIds.includes(id2);

  // Check if either id1 or id2 is not in baseNodeIds
  const id1InBaseNodes = baseNodeIds.includes(id1);
  const id2InBaseNodes = baseNodeIds.includes(id2);

  if (id1Exists !== id2Exists && (!id1InBaseNodes && !id2InBaseNodes)) { //second ID not a basenode ID
    const missingId = id1Exists ? id2 : id1; // Determine the missing ID
    console.log(`Entry: [${id1}, ${id2}] - Missing ID: ${missingId}`);
    const existingId = id1Exists ? id1 : id2; // Get Existing ID
    console.log("EX ID", existingId);

    //Cord of existing ID:
    const [ex, ey] = getCoordOfExId(existingId, allNodes);
    console.log("EX ID COORD", ex, ey);
  

    //get cord of missing ID
    const missingNode = missingId
    const getCoord = getCoordOfNode(missingNode, allNodes)
    console.log("CORD OF MISSING NODE: ", getCoord);

    //calculate distance to all other available points / ids (+ base nodes)
    //childNodes + baseNodes
    const clearBaseNodes = baseNodes.nodes.map(([_, ...rest]) => rest);
    const clearChildNodes = childNodes.map(([_, ...rest]) => rest);
    console.log("base", clearBaseNodes);
    const ChildAvailableNodes = [...clearChildNodes, ...clearBaseNodes];
    console.log("AVAILABLE NODES:", ChildAvailableNodes);


    let minimalDistance = 999999;
    var [cx, cy] = [0, 0];
    var [cx_, cy_] = [0, 0];
    function closestNodeToMissingNode(){
        
        //iterate through childAvailableNodes
        //refresh closestNode if distance is smaller than before
        for (let i = 0; i < ChildAvailableNodes.length; i++){
            var [x, y] = getCoord;                  //M O V E  OUT OF FOR LOOP?
            var [x_, y_] = ChildAvailableNodes[i];
            console.log("XXXXXXXX: ", x, y, x_, y_); //debug
    
            const Distance = Math.sqrt(((x-x_)** 2) + ((y-y_) ** 2));
            if (minimalDistance > Distance && (x_ !== ex || y_ !== ey)){        //should Work (check if closest node != node where beam starts)
                minimalDistance = Distance;
                const closestNode = ChildAvailableNodes[i];
                console.log("CLOSEST N", closestNode);
                [cx, cy] = [x, y];
                [cx_, cy_] = [x_, y_];
            }
        }

        
    }
    closestNodeToMissingNode();
    console.log("MIN N N N ", minimalDistance);
    


    //--> bei connection jetzt xy einsetzen von closestNode -> ist ja schon ID
    // old: id1, id2
    // new: id1, x_ + y_        -> aber wenn eins z.B. 0,6 dann in "b3" übersetzen -> aber erst den filtered Array dann
    //const ExistingId = id1Exists ? id1 : id2;
    //const newConnection = ExistingId // ,  x_+y_
    // replace old id1, id2 oder kann ich einfach sagen id1 = x+y und id2 = x_+y_ --> reihenfolge ist ja egal
    // Creating decimal numbers
    const result = [ex + ey / Math.pow(10, ey.toString().length), cx_ + cy_ / Math.pow(10, cy_.toString().length)];

    console.log("NEW CONNECTION : : : : ", result); // Output: [5.11, 1.3]
    //[id1, id2] = [ex + ey / Math.pow(10, ey.toString().length), cx_ + cy_ / Math.pow(10, cy_.toString().length)];
    console.log(" F F F", filteredArray);


    //NEW NODE CANNOT BE ITSELF
    for (let i = 0; i < childConnections.length; i++) {
        const [id1_, id2_] = childConnections[i];
        if (id1_ === id1 && id2_ === id2) {
            // Overwrite both values with x and y
            childConnections[i] = [ex + ey / Math.pow(10, ey.toString().length), cx_ + cy_ / Math.pow(10, cy_.toString().length)];
            break; // Exit loop once the update is made
        }
    }
    

  }
});


//loop through all nodes and check for each if it intersects with another.
//if it does: move 1st point of node to each other point (start with closest point) and test for intersections each time.
//if no point found, do it for other side of beam
//if still intersecting, remove beam

//OR: determine all free and possible connections first and store them.             --> this is also expensive!!!
// -> then check if beam that needs to be moved has one point in common with a available connection
// if yes: move it.     if no, delete it
// -> doing this, reduces a lot of computation work. NO!^^

//PUT ALL THIS LOGIC INTO EXISTING LOOP





console.log("FINAL CONNECTIONS: : :", childConnections);
//further steps: Delete Duplicates (id1 and id2 can be switched)
// -> deal with crossings




function getCoordOfNode(missingNode, allNodes) {
    for (let node of allNodes) {
        if (node[0] === missingNode) { //check if place 0 has id of missing node (i think)
            return node.slice(1); // Return [x, y]
        }
    }
    console.log("E R R O R");
    throw new Error("Node Coord missing");
}


function getCoordOfExId(existingId, allNodes) {
    for (let node of allNodes) {
        if (node[0] === existingId) { //check if place 0 has id of missing node (i think)
            return node.slice(1); // Return [x, y]
        }
    }
    console.log("E R R O R");
    throw new Error("Node Coord missing");
}



//PASS TO CONTROLLER
const message = "Hello from script1!\n\n-->";
module.exports = { message, childNodes, childConnections};


