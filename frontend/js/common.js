function navigate(page) {
    window.location.href = page;
}

function logout() {
    localStorage.removeItem("acct_id");
    window.location.href = "/index.html";
}