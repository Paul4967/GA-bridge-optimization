
//script Controller
//send Parents data to crossover script here

//Hier auch Parameter einstellen (bzw. via Website interface)
// Z.B. Mutationsrate (0 to 1)
//save setting then in json -> so they dont get lost

const { message, childNodes, childConnections} = require('./crossover.cjs');
console.log(message); // Outputs: Hello from script1!
console.log("ChildNodes: ", childNodes);
console.log("ChildConnections: ", childConnections);

//test
