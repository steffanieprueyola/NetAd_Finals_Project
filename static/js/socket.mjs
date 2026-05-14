import { io } from "https://cdn.socket.io/4.5.4/socket.io.esm.min.js";

const socket = io();

// listen for logs from backend
socket.on("new_log", (data) => {

    const logs = document.getElementById("logs");

    const logEntry = document.createElement("div");
    logEntry.classList.add("log-entry", data.type);

    logEntry.innerHTML = `
        <div>${data.message}</div>
        <div class="log-time">${data.time}</div>
    `;

    logs.prepend(logEntry);
});
