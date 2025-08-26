const btn = document.getElementById("run")
const list = document.getElementById("list")

async function postClientData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/clients', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            // body: JSON.stringify()
        });

        // Check if the response is OK (status 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Parse the JSON response
        const data = await response.json();
        console.log('Response from server:', data)

        // Handle the response data as needed
        return data;
    } catch (error) {
        console.error('Error making request:', error.message);
    }
}

// Call the function to send the request
btn.addEventListener("click", async () => {
    const data = await postClientData();
    // Clear old list
    list.innerHTML = "";

    // Check if clients exist in response
    if (data.clients) {
        data.clients.forEach(client => {
            const h3 = document.createElement("h3");
            h3.textContent = JSON.stringify(client); // or client.name
            list.appendChild(h3);
        });
    }
});
