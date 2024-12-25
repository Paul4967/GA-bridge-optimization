const WebSocket = require('ws');
const fs = require('fs')




// Create WebSocket server
const wss = new WebSocket.Server({ port: 8080 });

console.log('WebSocket server running on ws://localhost:8080');

wss.on('connection', (ws) => {
    console.log('Client connected');
    
    setInterval(myMethod, 1000);

function myMethod( )
{
    // GET DATA
    //const { childNodes, childConnections } = require('./scriptController.js');
    //delete require.cache[require.resolve('./scriptController.js')];         //DELETE CACHE
    fs.readFile('temp.json', 'utf8', (err, jsonString) => {
        if (err) {
            console.error('Error reading file:', err);
            return;
        }
        try {
            const data = JSON.parse(jsonString); // Parse JSON
            const childNodes = data.child_nodes;
            const childConnections = data.child_connections;
    
            // Send data to client
            ws.send(JSON.stringify({ childNodes, childConnections }));
        } catch (err) {
            console.error('Error parsing JSON:', err);
        }
    });
    

}

    
    ws.on('message', (message) => {
        console.log('Received:', message);
        // Optionally, process messages from the client here
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});
