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
        outputDiv.innerHTML = "";
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
        userInputField.value = "";
        updateStatus();

        if (data.game_over) {
            userInputField.disabled = true;
            sendButton.disabled = true;
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
};
