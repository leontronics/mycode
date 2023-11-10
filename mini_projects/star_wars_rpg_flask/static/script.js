window.onload = function () {
    const sendButton = document.getElementById("send-command");
    const userInputField = document.getElementById("user-input");

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

    sendButton.addEventListener("click", sendCommand);

    userInputField.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendCommand();
        }
    });
    updateStatus();
};
