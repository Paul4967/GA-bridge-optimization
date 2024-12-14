const WebSocket = require('ws');




// Create WebSocket server
const wss = new WebSocket.Server({ port: 8080 });

console.log('WebSocket server running on ws://localhost:8080');

wss.on('connection', (ws) => {
    console.log('Client connected');
    
    setInterval(myMethod, 1000);

function myMethod( )
{
    const { childNodes, childConnections } = require('./scriptController.js');
    delete require.cache[require.resolve('./scriptController.js')];         //DELETE CACHE
    // Send data to client
    ws.send(JSON.stringify({ childNodes, childConnections }));

}

    
    ws.on('message', (message) => {
        console.log('Received:', message);
        // Optionally, process messages from the client here
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});
