// Wait for the DOM to be fully loaded
window.onload = function () {
    // Get the button element
    var sendButton = document.getElementById("send-command");

    // Add click event listener to the button
    sendButton.addEventListener("click", async function () {
        // Get the user input
        const userInput = document.getElementById("user-input").value;

        // Send the command to the server
        let response = await fetch("/command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ command: userInput }),
        });

        // Process the response
        let data = await response.json();
        const outputDiv = document.getElementById("game-output");
        outputDiv.innerHTML = "";
        data.messages.forEach((message) => {
            outputDiv.innerHTML += message + "<br>";
        });

        // Clear the input field
        document.getElementById("user-input").value = "";
    });
};
