window.onload = function () {
    const sendButton = document.getElementById("send-command");
    const userInputField = document.getElementById("user-input");

    const socket = io.connect(
        location.protocol +
            "//" +
            window.location.hostname +
            ":" +
            location.port
    );

    socket.on("game_message", function (data) {
        const outputDiv = document.getElementById("game-output");
        outputDiv.innerHTML += "<pre>" + data.message + "</pre>";
    });

    async function updateStatus() {
        let response = await fetch("/status");
        let data = await response.json();
        document.getElementById("game-status").innerHTML =
            "<pre>" + data.status + "</pre>";
    }

    async function sendCommand() {
        const userInput = userInputField.value;

        let response = await fetch("/command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ command: userInput }),
        });

        let data = await response.json();
        const outputDiv = document.getElementById("game-output");
        outputDiv.innerHTML = "";
        data.messages.forEach((message) => {
            outputDiv.innerHTML += "<pre>" + message + "</pre>";
        });

        userInputField.value = "";
        updateStatus();

        if (data.game_over) {
            userInputField.disabled = true;
            sendButton.disabled = true;
        }
    }

    async function updateMessages() {
        let response = await fetch("/messages");
        let data = await response.json();
        if (data.messages.length > 0) {
            const outputDiv = document.getElementById("game-output");
            data.messages.forEach((message) => {
                outputDiv.innerHTML += "<pre>" + message + "</pre>";
            });
        }
    }

    sendButton.addEventListener("click", sendCommand);

    userInputField.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendCommand();
        }
    });

    updateStatus();
    setInterval(updateMessages, 1000);
};
