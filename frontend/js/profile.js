window.onload = async function(){

const acct_id = localStorage.getItem("acct_id");

if(!acct_id){
    window.location.href="index.html";
    return;
}

try{

const res = await fetch(`http://127.0.0.1:8000/user/dashboard/${acct_id}`);
const data = await res.json();

console.log(data);

function setValue(id,value){
    const el = document.getElementById(id);
    if(el){
        el.innerText = value || "-";
    }
}

setValue("user_name",data.name);
setValue("consumer_id",data.acct_id);
setValue("conn_status",data.connection_status);

setValue("name",data.name);
setValue("cid",data.acct_id);
setValue("meter",data.meter_number);
setValue("tariff",data.tariff);

setValue("mobile",data.mobile);
setValue("address",data.address);
setValue("status",data.connection_status);

}
catch(err){
console.error("Error loading profile:",err);
}

}