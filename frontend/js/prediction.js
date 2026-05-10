// ================= LOAD USER DATA FROM BACKEND =================
document.addEventListener("DOMContentLoaded", async function () {

    let acctId = localStorage.getItem("acct_id");

    if (!acctId) {
        alert("No Account ID found. Please login first.");
        return;
    }

    let usernameEl = document.getElementById("username");
    let acctEl = document.getElementById("acct_id");
    let statusEl = document.getElementById("status");

    try {
        let response = await fetch(`http://127.0.0.1:8000/user/dashboard/${acctId}`);

        if (!response.ok) {
            throw new Error("API not found or server error");
        }

        let data = await response.json();

        console.log("Profile Data:", data);

        if (usernameEl && acctEl && statusEl) {
            usernameEl.innerText = data.name || "N/A";
            acctEl.innerText = data.acct_id || "N/A";
            statusEl.innerText = data.status || "--";
        }

    } catch (error) {
        console.error("Error fetching profile:", error);

        if (usernameEl) usernameEl.innerText = "Not Loaded";
        if (acctEl) acctEl.innerText = "Not Loaded";
        if (statusEl) statusEl.innerText = "Error";
    }
});


// ================= SET STATUS BASED ON PREDICTION =================
function setStatus(avgConsumption){

    let statusText = "Normal Usage 🟡";
    let color = "orange";

    if(avgConsumption < 75){
        statusText = "Low Usage 🟢";
        color = "green";
    }
    else if(avgConsumption > 150){
        statusText = "High Usage 🔴";
        color = "red";
    }

    let statusEl = document.getElementById("status");

    if(statusEl){
        statusEl.innerText = statusText;
        statusEl.style.color = color;
    }
}


// ================= PREDICTION FUNCTION =================
async function predict(){

    let acctId = localStorage.getItem("acct_id");
    let months = document.getElementById("months").value;
    let table = document.querySelector("#resultTable tbody");

    table.innerHTML = "";

    try {
        let response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                acct_id: parseInt(acctId),
                months: parseInt(months)
            })
        });

        if (!response.ok) {
            throw new Error("Prediction API error");
        }

        let data = await response.json();

        console.log("Prediction Data:", data);

        let totalConsumption = 0;

        data.predictions.forEach((item, index) => {
            let consumption = item.predicted_units;
            let bill = consumption * 7;

            totalConsumption += consumption;

            let row = `
            <tr>
             <td>${item.month}</td>
             <td>${consumption} kWh</td>
             <td>₹${bill.toFixed(2)}</td>
            </tr>
         `;

            table.innerHTML += row;
        });

        let avgConsumption = totalConsumption / data.predictions.length;
        setStatus(avgConsumption);

    } catch(error) {
        console.error("Prediction Error:", error);
        alert("Failed to fetch prediction.");
    }
}