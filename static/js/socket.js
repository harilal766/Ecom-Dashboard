const socket = new WebSocket("ws://127.0.0.1:8000/ws/websocket/");


socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const time = data.time;

    document.getElementById('timeDisplay').innerText = time;
};