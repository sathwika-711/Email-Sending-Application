
document.getElementById('send-mail').addEventListener('click', (event) => {
    // Prevent the default form submission
    event.preventDefault();
    sendData();
})

function sendData() {
    // confirm("send this message?")
    // fetching values from Html fields
    from_email = document.getElementById("from").value
	to_email = document.getElementById("to").value;
	subject = document.getElementById("subject").value;
	body = document.getElementById("body").value;
    // simple form check
    if (to_email == '' || subject == '' || body == ''){
        alert("Fill the required fields..")
        return
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if(!to_email.trim().match(emailRegex)){
        alert("Please provide valid email")
        return
    }
    // displaying the fetched values
    console.log(from_email)
	console.log(to_email);
	console.log(subject);
	console.log(body);

	var myHeaders = new Headers(); //creating a header object
	myHeaders.append("Content-Type", "application/json"); //specifying type of header

    // creating json data
	var raw = JSON.stringify({
		"to": to_email,
		"subject": subject,
		"body": body,
	});

    console.log(raw)


	var requestOptions = {
		method: "POST",
		headers: myHeaders,
		body: raw,
		redirect: "follow", //automatically goes to new page if redirected (if return value is any url)
	};
    // call to backend
	fetch("http://192.168.100.8:5000/mailwithbody", requestOptions) 
		.then((response) => response.text())   //handle the server reply
		.then((result) => {
            console.log(result)
            alert(result)
            document.getElementById('myForm').reset();
        }) // if our app.py receives the request then it stroes the return value from that endpoint in result and prints its on console
		.catch((error) => {
            console.log("error", error)
            alert("Error in Sending...!!" + error.message)
            document.getElementById('myForm').reset();
        }); //used to handle errors that may occur during http request

}   

