async function loadDashboard() {
    const acctId = localStorage.getItem("acct_id");

    if (!acctId) {
        alert("Please login first");
        window.location.href = "index.html";
        return;
    }

    try {
        const response = await fetch(`/user/dashboard/${acctId}`);
        const data = await response.json();

        console.log("Dashboard Data:", data);

        // Example fields — adjust based on your API response
        document.getElementById("name").innerText = data.name;
        document.getElementById("meter").innerText = data.meter_number;
        document.getElementById("units").innerText = data.current_units;
        document.getElementById("bill").innerText = data.current_bill;

    } catch (error) {
        console.error("Dashboard load error:", error);
    }
}

window.onload = loadDashboard;