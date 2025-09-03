const btn = document.getElementById("run");
const tableBody = document.getElementById("clientBody");

async function fetchClients() {
    try {
        const response = await fetch('/clients', {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();
        console.log('Response from server:', data);

        // Clear previous rows
        tableBody.innerHTML = "";

        // Loop clients and add rows
        data.clients.forEach(client => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${client.id}</td>
                <td>${client.first_name}</td>
                <td>${client.middle_name}</td>
                <td>${client.last_name}</td>
                <td>${client.nickname}</td>
                <td>${client.age}</td>
                <td>${client.birthdate}</td>
                <td>${client.deathdate}</td>
                <td>${client.address}</td>
                <td>${client.religion}</td>
                <td>${client.coffin}</td>
                <td>${client.accessories}</td>
                <td>${client.mor_plan}</td>
                <td>${client.mor_plan_amount}</td>
                <td>${client.gov_ass}</td>
                <td>${client.amount}</td>
            `;
            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error('Error fetching clients:', error.message);
    }
}

btn.addEventListener("click", fetchClients);
