const WebSocket = require('ws');

const server = new WebSocket.Server({ port: 8080 });

console.log('WebSocket server running on ws://localhost:8080');

server.on('connection', (socket) => {
    console.log('Client connected.');

    // Handle messages from the client
    socket.on('message', (message) => {
        console.log('Received from client:', message);
    });

    // Send a message to the client
    process.stdin.on('data', (data) => {
        const message = data.toString().trim();
        socket.send(message);
        console.log('Sent to client:', message);
    });

    // Handle client disconnect
    socket.on('close', () => {
        console.log('Client disconnected.');
    });
});
