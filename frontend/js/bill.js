// ================= PIE CHART =================

let pieChart;

function updatePieChart(paid, remaining){

    const ctx = document.getElementById("paymentChart");

    // destroy old chart if exists
    if(pieChart){
        pieChart.destroy();
    }

    pieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Paid', 'Remaining'],
            datasets: [{
                data: [paid, remaining],
                backgroundColor: ['green', 'red']
            }]
        },
        options:{
            responsive: true,
            maintainAspectRatio: false
        }
    });
}


// ================= FETCH BILL DATA =================

async function loadBill(){

    try{

        const acct_id = localStorage.getItem("acct_id");

        if(!acct_id){
            alert("User not logged in");
            return;
        }

        const response = await fetch(`http://127.0.0.1:8000/user/bill/${acct_id}`);

        if(!response.ok){
            throw new Error("Failed to fetch bill data");
        }

        const data = await response.json();

        // ================= UPDATE UI =================

        document.getElementById("billMonth").innerText =
        `${data.month} ${data.year}`;

        document.getElementById("billUnits").innerText =
        data.units + " kWh";

        document.getElementById("billTotal").innerText =
        "₹ " + data.current_bill;

        document.getElementById("paidAmount").innerText =
         Math.round(data.paid);

        document.getElementById("remainingAmount").innerText =
        Math.round(data.remaining);

        // ================= UPDATE CHART =================

        updatePieChart(data.paid, data.remaining);

    }catch(error){

        console.error("Error:", error);
        alert("Error loading bill data");

    }

}


// ================= RUN ON PAGE LOAD =================

document.addEventListener("DOMContentLoaded", function(){
    loadBill();
});