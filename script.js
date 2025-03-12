async function fetchSign() {
    try {
        let response = await fetch("/get_sign");
        let data = await response.text();
        document.getElementById("sign_output").innerText = data;
    } catch (error) {
        console.error("Error fetching sign language translation:", error);
    }
}

setInterval(fetchSign, 1000);
