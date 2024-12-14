

const {childNodes, childConnections} = require('./scriptController.js');
console.log(childNodes, childConnections);






const baseNodes = [
    [0.0, 0, 0],
    [2.0, 4, 0],
    [4.0, 8, 0],
    [6.0, 12, 0]
];

const canvas = document.getElementById('bridgeCanvas');
const ctx = canvas.getContext('2d');

// Combine baseNodes and childNodes for easier visualization
const allNodes = [...baseNodes, ...childNodes];

// Helper function to find node by ID
function findNodeById(id) {
    return allNodes.find(node => node[0] === id);
}

// Draw connections
function drawConnections() {
    ctx.strokeStyle = 'gray';
    ctx.lineWidth = 2;

    childConnections.forEach(([id1, id2]) => {
        const node1 = findNodeById(id1);
        const node2 = findNodeById(id2);

        if (node1 && node2) {
            const [_, x1, y1] = node1;
            const [__, x2, y2] = node2;

            ctx.beginPath();
            ctx.moveTo(x1 * 40, canvas.height - y1 * 40);
            ctx.lineTo(x2 * 40, canvas.height - y2 * 40);
            ctx.stroke();
        }
    });
}

// Draw nodes
function drawNodes() {
    allNodes.forEach(([id, x, y]) => {
        const screenX = x * 40;
        const screenY = canvas.height - y * 40;
        ctx.beginPath();
        ctx.arc(screenX, screenY, 5, 0, Math.PI * 2);
        ctx.fillStyle = baseNodes.some(node => node[0] === id) ? 'blue' : 'red';
        ctx.fill();

        // Draw node ID for clarity
        ctx.fillStyle = 'black';
        ctx.font = '12px Arial';
        ctx.fillText(id, screenX + 5, screenY - 5);
    });
}

// Main drawing function
function drawBridge() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawConnections();
    drawNodes();
}

drawBridge();
