async function sendOTP(){

const identifier = document.getElementById("identifier").value.trim();
const status = document.getElementById("otpStatus");

if(identifier === ""){
status.innerText = "Enter Mobile or Meter Number";
return;
}

const res = await fetch("http://127.0.0.1:8000/user/send-otp",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
identifier:identifier
})
});

const data = await res.json();

if(res.ok){

status.style.color = "green";
status.innerText = "OTP Sent Successfully";

document.getElementById("otpSection").style.display = "block";

document.getElementById("identifier").disabled = true;

}else{

status.style.color = "red";
status.innerText = data.detail || "User not found";

}

}



async function verifyOTP(){

const identifier = document.getElementById("identifier").value.trim();
const otp = document.getElementById("otp").value.trim();
const status = document.getElementById("otpStatus");

if(otp === ""){
status.innerText = "Enter OTP";
return;
}

const res = await fetch("http://127.0.0.1:8000/user/verify-otp",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
identifier:identifier,
otp:otp
})
});

const data = await res.json();

if(res.ok){

localStorage.setItem("acct_id",data.acct_id);

window.location.href = "profile.html";

}else{

status.style.color = "red";
status.innerText = data.detail || "Invalid OTP";

}

}


/* Navigation function for sidebar */
function navigate(page){
window.location.href = page;
}


/* Logout function */
function logout(){
localStorage.removeItem("acct_id");
window.location.href = "index.html";
}