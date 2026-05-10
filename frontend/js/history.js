let historyData = [];

const table = document.getElementById("historyTable");
const filter = document.getElementById("monthFilter");

let barChart, unitLineChart, lineChart, pieChart;


// ================= FETCH DATA =================
async function fetchHistory() {
    try {
        let acctId = localStorage.getItem("acct_id");

        if (!acctId) {
            acctId = "1001";
        }

        const response = await fetch(`http://127.0.0.1:8000/user/history/${acctId}`);

        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }

        const data = await response.json();

        if (!data || data.length === 0) {
            table.innerHTML = `<tr><td colspan="3">No history found</td></tr>`;
            return;
        }

        historyData = data;

        loadHistory(parseInt(filter.value));

    } catch (error) {
        console.error("Error:", error);
        table.innerHTML = `<tr><td colspan="3">Error loading data</td></tr>`;
    }
}


// ================= LOAD TABLE =================
function loadHistory(months) {

    table.innerHTML = "";

    let filteredData = historyData.slice(-months);

    if (filteredData.length === 0) {
        table.innerHTML = `<tr><td colspan="3">No data available</td></tr>`;
        return;
    }

    filteredData.forEach(item => {
        table.innerHTML += `
        <tr>
            <td>${item.month}-${item.year}</td>
            <td>${item.units}</td>
            <td>₹${item.bill}</td>
        </tr>
        `;
    });

    updateCharts(filteredData);
}


// ================= CHARTS =================
function updateCharts(data) {

    const months = data.map(d => `${d.month}-${d.year}`);
    const units = data.map(d => d.units);
    const bills = data.map(d => d.bill);

    // -------------------Destroy old charts (VI)--------------
    if (barChart) barChart.destroy();
    if (unitLineChart) unitLineChart.destroy();
    if (lineChart) lineChart.destroy();
    if (pieChart) pieChart.destroy();

    // ===== BAR CHART (Units) =====
    barChart = new Chart(document.getElementById("barChart"), {
        type: 'bar',
        data: {
            labels: months,
            datasets: [{
                label: "Units Consumption",
                data: units,
                backgroundColor: "#4e73df"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // ===== UNITS LINE CHART =====
    const unitCtx = document.getElementById("unitLineChart").getContext("2d");

    unitLineChart = new Chart(unitCtx, {
     type: 'line',
     data: {
        labels: months,
        datasets: [{
            label: "Units Consumption",
            data: units,
            borderColor: "#007bff",
            backgroundColor: "rgba(0,123,255,0.2)",
            fill: true,
            tension: 0.4,
            pointRadius: 5
        }]
     },
     options: {
        responsive: true,
        maintainAspectRatio: false
     }
    });

    // ===== BILL LINE CHART =====
    lineChart = new Chart(document.getElementById("lineChart"), {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: "Bill Amount (₹)",
                data: bills,
                borderColor: "green",
                backgroundColor: "rgba(0,128,0,0.1)",
                fill: true,
                tension: 0.4,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // ===== PIE CHART =====
    pieChart = new Chart(document.getElementById("pieChart"), {
        type: 'pie',
        data: {
            labels: months,
            datasets: [{
                label: "Units Distribution",
                data: units
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true
        }
    });
}


// ================= FILTER =================
filter.addEventListener("change", function () {
    loadHistory(parseInt(this.value));
});


// ================= START =================
fetchHistory();