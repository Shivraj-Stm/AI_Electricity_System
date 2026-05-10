// ================= GREETING =================
window.onload = async function () {

    const greetingText = document.getElementById("greetingText")

    let hour = new Date().getHours()
    let greeting = ""

    if (hour < 12) greeting = "Good Morning"
    else if (hour < 18) greeting = "Good Afternoon"
    else greeting = "Good Evening"

    let acct_id = localStorage.getItem("acct_id")
    let username = "User"

    if (acct_id) {
        try {
            const res = await fetch(`http://127.0.0.1:8000/user/dashboard/${acct_id}`)
            const data = await res.json()

            username = data.name || "User"
            localStorage.setItem("username", username)

        } catch (error) {
            username = localStorage.getItem("username") || "User"
        }
    }

    let firstName = username.trim().split(" ")[0]
    greetingText.innerText = `${greeting}, ${firstName}`

    setupInputUI()
}



function setupInputUI(){

    const input = document.getElementById("userInput")
    const micBtn = document.getElementById("micBtn")
    const sendBtn = document.getElementById("sendBtn")

    //  Toggle mic & send button
    input.addEventListener("input", () => {

        if(input.value.trim() === ""){
            micBtn.style.display = "flex"
            sendBtn.style.display = "none"
        }else{
            micBtn.style.display = "none"
            sendBtn.style.display = "flex"
        }

    })

    //  Enter key
    input.addEventListener("keypress", function(e){
        if(e.key === "Enter"){
            sendMessage()
        }
    })

    //  FIX: ADD HERE (inside function)
    sendBtn.addEventListener("click", sendMessage)
}
// ================= SEND MESSAGE =================
async function sendMessage(){

    const input = document.getElementById("userInput")
    const chatBox = document.getElementById("chatMessages")

    let message = input.value.trim()
    if(message === "") return

    // ------------------- REMOVE GREETING (ONLY ONCE)------------------
    let greeting = document.querySelector(".greeting")
    if (greeting && greeting.style.display !== "none") {
        greeting.classList.add("hide-greeting")

        setTimeout(() => {
            greeting.style.display = "none"
        }, 400)
    }

    // ------------------- Show user message-------------
    let userMsg = document.createElement("div")
    userMsg.className = "user-message"
    userMsg.innerText = message
    chatBox.appendChild(userMsg)

    input.value = ""
    input.dispatchEvent(new Event("input"))

    // ---------------- Get username-------------
    let username = localStorage.getItem("username") || "User"

    try {
        // -------- CALL BACKEND-----------------
        let res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                username: username,
                acct_id: localStorage.getItem("acct_id")
            })
        })

        let data = await res.json()

        //  Show AI response
        let aiMsg = document.createElement("div")
        aiMsg.className = "ai-message"
        aiMsg.innerText = data.reply || data.response || "No response"
        chatBox.appendChild(aiMsg)

        chatBox.scrollTop = chatBox.scrollHeight

    } catch (error) {
        console.log("Error:", error)

        let errorMsg = document.createElement("div")
        errorMsg.className = "ai-message"
        errorMsg.innerText = "Something went wrong. Please try again."
        chatBox.appendChild(errorMsg)

        chatBox.scrollTop = chatBox.scrollHeight
    }
}

// ================= VOICE INPUT =================
function startVoice(){

    const input = document.getElementById("userInput")

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)()

    recognition.lang = "en-IN"
    recognition.start()

    recognition.onresult = function(event){

        let text = event.results[0][0].transcript

        input.value = text

        // trigger UI update
        input.dispatchEvent(new Event("input"))
    }

    recognition.onerror = function(){
        alert("Voice not supported or permission denied")
    }
}