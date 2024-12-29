window.onload = function() {
    var canvas = document.getElementById('courtCanvas');
    var ctx = canvas.getContext('2d');

    var isDrawing = false;  // Track if the user is drawing a line
    var isDragging = false;  // Track if the user is dragging a player
    var selectedPlayer = null;  // Track the currently selected player
    var isErasing = false;  // Track if the user is erasing lines

    var startX, startY;  // Coordinates for drawing

    // Array to store all the drawn lines
    var lines = [];

    // Checkbox for toggling between dragging and drawing mode
    var drawModeCheckbox = document.getElementById('drawMode');
    var eraseModeCheckbox = document.getElementById('eraseMode');  // New checkbox for erase mode

    // Load the basketball court image
    var courtImage = new Image();
    courtImage.src = '/static/court.jpg';

    courtImage.onload = function() {
        ctx.drawImage(courtImage, 0, 0, canvas.width, canvas.height);  // Draw the court
        drawPlayers();  // Once the court is drawn, draw the players
    };

    // Player positions
    var players = [
        { x: 210, y: 80, color: 'blue' },
        { x: 180, y: 220, color: 'red' },
        { x: 300, y: 200, color: 'green' },
        { x: 80, y: 300, color: 'yellow' },
        { x: 250, y: 330, color: 'purple' }
    ];

    // Draw players function
    function drawPlayers() {
        players.forEach(function(player) {
            ctx.beginPath();
            ctx.arc(player.x, player.y, 15, 0, Math.PI * 2);  // Draw each player as a circle
            ctx.fillStyle = player.color;
            ctx.fill();
            ctx.closePath();
        });
    }

    // Function to draw a line between two points
    function drawLine(startX, startY, endX, endY) {
        ctx.beginPath();
        ctx.moveTo(startX, startY);  // Move to start position
        ctx.lineTo(endX, endY);  // Draw a line to the end position
        ctx.strokeStyle = 'black';  // Set line color
        ctx.lineWidth = 2;  // Set line width
        ctx.stroke();  // Draw the line
        ctx.closePath();  // Close the path
    }

    // Function to redraw all stored lines
    function drawAllLines() {
        lines.forEach(function(line) {
            drawLine(line.startX, line.startY, line.endX, line.endY);
        });
    }

    // Function to check if a click is near a line
    function isNearLine(x, y, line) {
        var distance = pointToLineDistance(x, y, line.startX, line.startY, line.endX, line.endY);
        return distance < 5;  // Set a tolerance of 5 pixels
    }

    // Helper function to calculate the distance from a point to a line segment
    function pointToLineDistance(px, py, x1, y1, x2, y2) {
        var A = px - x1;
        var B = py - y1;
        var C = x2 - x1;
        var D = y2 - y1;

        var dot = A * C + B * D;
        var len_sq = C * C + D * D;
        var param = (len_sq !== 0) ? dot / len_sq : -1;

        var xx, yy;

        if (param < 0) {
            xx = x1;
            yy = y1;
        } else if (param > 1) {
            xx = x2;
            yy = y2;
        } else {
            xx = x1 + param * C;
            yy = y1 + param * D;
        }

        var dx = px - xx;
        var dy = py - yy;
        return Math.sqrt(dx * dx + dy * dy);
    }

    // Event handler for mouse down (start dragging, drawing, or erasing)
    canvas.onmousedown = function(e) {
        var mouseX = e.offsetX;
        var mouseY = e.offsetY;

        if (eraseModeCheckbox.checked) {
            // In erase mode
            isErasing = true;
            for (var i = 0; i < lines.length; i++) {
                if (isNearLine(mouseX, mouseY, lines[i])) {
                    lines.splice(i, 1);  // Remove the line if it's near the click
                    break;
                }
            }
            redrawCanvas();  // Redraw after erasing
        } else if (drawModeCheckbox.checked) {
            // In drawing mode
            isDrawing = true;
            startX = mouseX;
            startY = mouseY;
        } else {
            // In dragging mode
            selectedPlayer = players.find(function(player) {
                return Math.sqrt((player.x - mouseX) ** 2 + (player.y - mouseY) ** 2) < 15;
            });

            if (selectedPlayer) {
                isDragging = true;  // Start dragging if a player is clicked
            }
        }
    };

    // Event handler for mouse move (dragging or previewing the line)
    canvas.onmousemove = function(e) {
        var mouseX = e.offsetX;
        var mouseY = e.offsetY;

        if (isDragging && selectedPlayer) {
            // Update player position
            selectedPlayer.x = mouseX;
            selectedPlayer.y = mouseY;

            // Redraw the canvas
            redrawCanvas();
        }

        if (isDrawing) {
            // Optionally show a preview of the line being drawn
            redrawCanvas();
            drawLine(startX, startY, mouseX, mouseY);  // Preview the line being drawn
        }
    };

    // Event handler for mouse up (finish dragging or drawing)
    canvas.onmouseup = function(e) {
        var mouseX = e.offsetX;
        var mouseY = e.offsetY;

        if (isDragging) {
            isDragging = false;
            selectedPlayer = null;  // Reset the selected player
        }

        if (isDrawing) {
            // Store the drawn line in the lines array
            lines.push({ startX: startX, startY: startY, endX: mouseX, endY: mouseY });
            drawLine(startX, startY, mouseX, mouseY);  // Finalize the line being drawn
            isDrawing = false;
        }
    };

    // Redraw the entire canvas (court, players, lines)
    function redrawCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);  // Clear the canvas
        ctx.drawImage(courtImage, 0, 0, canvas.width, canvas.height);  // Redraw the court
        drawAllLines();  // Redraw all stored lines
        drawPlayers();  // Redraw the players
    }
};
