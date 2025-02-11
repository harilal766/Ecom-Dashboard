const socket = new WebSocket("ws://127.0.0.1:8000/ws/websocket/");

/*
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const currentTime = data.time;  // The time from the server
    // Optionally, display the time in an element
    document.getElementById('timeDisplay').innerText = currentTime;
};

socket.onopen = () => {
    console.log("WebSocket connected!");
};

socket.onclose = (event) => {
    console.log("WebSocket closed:", event);
};

socket.onerror = (error) => {
    console.error("WebSocket error:", error);
};
*/
