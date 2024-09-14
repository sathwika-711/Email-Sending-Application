document.getElementById("send-mail").addEventListener("click", (event) => {
    // Prevent the default form submission
    event.preventDefault();
    sendData();
});

document.getElementById("close-button").addEventListener("click", (event) => {
    // console.log(event);
    closeCustomAlert();
});

document.getElementById("file-button").addEventListener("click", (event) => {
    validateFileSize(event);
});


let file_content = null
let file_name = null
let file_type = null


function sendData() {
    // confirm("send this message?")
    // fetching values from Html fields
    sender_name = document.getElementById("from_name").value;
    bulk_emails = document.getElementById("to").value;
    receiver_names = document.getElementById("to_name").value;
    subject = document.getElementById("subject").value;
    body = document.getElementById("body").value;

    // simple form check
    if (bulk_emails == "" || subject == "" || body == "") {
        showCustomAlert("Fill the required fields..");
        return;
    }

    //storing bulk emails in an array and validating emails
    let bulk = bulk_emails.split(",").map(email => email.trim());    ; //Split the comma-separated values into arrays
    console.log(bulk)
    bulk.forEach(function(to_email) {
        console.log(to_email)
    // validating email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!to_email.trim().match(emailRegex)) {
        showCustomAlert("Please provide valid email");
        return;
    }
      });
    
    // storing receiver names in an array
    let to_name = receiver_names.split(",").map(name => name.trim());
    ;
    console.log(to_name)

    // Create an array of objects to store in JSON
    let dataArray = [];
    for (let i = 0; i < bulk.length; i++) {
        dataArray.push({
            "email": bulk[i],
            "receiver_name": to_name[i] || ""  // Use an empty string if name is not provided
        });
    }

    // displaying the fetched values
    console.log(sender_name);
    console.log(bulk_emails);
    console.log(to_name);
    console.log(subject);
    console.log(body);

    var myHeaders = new Headers(); //creating a header object
    myHeaders.append("Content-Type", "application/json"); //specifying type of header
    // myHeaders.append("Content-Type", "*/*"); //specifying type of header

    // creating json data
    var raw = JSON.stringify({
        "sender_name": sender_name,
        to: dataArray,
        "subject": subject,
        "body": body,
        attachments: {
            "file_type" : file_type,
            "file_name": file_name,
            "file_content": file_content
        }
    });

    console.log(raw);

    var requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow", //automatically goes to new page if redirected (if return value is any url)
    };

    //call to backend
    // Fetch message from Flask and show in the alert box
    fetch("http://localhost:5000/bulkmails", requestOptions) // Fetches the message from Flask route
        .then((response) => response.json()) // Parse JSON response
        .then((data) => {
            // Show custom alert with the returned message
            // document.getElementById('loading').style.display = 'block';
            showCustomAlert(data['message']);
            document.getElementById("myForm").reset();
            console.log("Message sent successfully " + data);

        })
        .catch((error) => {
            showCustomAlert("Error in Sending...!! \n" + error.message);
            console.error("Error fetching message:", error);
            document.getElementById("myForm").reset();
        });


    //call to backend
    fetch("http://192.168.100.8:5000/sent_emails", requestOptions)
     	.then((response) => response.json())   //handle the server reply
     	.then((result) => console.log(result)) // if our app.py receives the request then it stroes the return value from that endpoint in result and prints its on console
     	.catch((error) => console.log("error", error)); //used to handle errors that may occur during http request
}

function showCustomAlert(message) {
    document.getElementById("alert-message").innerText = message;
    document.getElementById("custom-alert").style.display = "flex";
}

// Close the custom alert box
function closeCustomAlert() {
    document.getElementById("custom-alert").style.display = "none";
}

// Handle changes in file type selection
function handleFileTypeChange() {
    const fileInput = document.getElementById("file-input");
    const format = document.getElementById("format").value;
    const button = document.getElementById("file-button");

    if (format === "attach") {
        fileInput.style.display = "block"; // Show file input for attaching files
        button.style.display = "block";
        fileInput.accept = ".pdf,.docx"; // Restrict to PDF and Word documents
    } else if (format === "photo") {
        fileInput.style.display = "block"; // Show file input for photos
        button.style.display = "block";
        fileInput.accept = "image/*"; // Restrict to images
    } else {
        fileInput.style.display = "none"; // Hide file input if no selection
        button.style.display = "none"; // Hide file input if no selection
    }
}

// Validate file size before sending
function validateFileSize(event) {
    const fileInput = document.getElementById("file-input");
    const fileError = document.getElementById("file-error");
    const format = document.getElementById("format").value;

    // If no file is selected, allow the submission to proceed
    if (!fileInput.files.length) {
        return;
    }

    // Check file size
    const file = fileInput.files[0]; //fetching selected file
    file_name = file.name; //fetching name of the file
    console.log("165 : " + file.type + " " + file.size + " " + file.name);

    // max size validation
    if (format == "photo" && file.size > 1 * 1024 * 1024) {
        // 1MB limit for photos
        console.log(file.size);
        fileError.style.display = "block";
        fileError.textContent = "Photo must be less than 1MB.";
        event.preventDefault();
        return false;
    }

    if (format == "attach" && file.size > 30 * 1024 * 1024) {
        // 30MB limit for PDFs
        fileError.style.display = "block";
        fileError.textContent = "PDF must be less than 30MB.";
        event.preventDefault();
        return false;
    }
    readFile(file);
    fileError.style.display = "none"; // Hide the error message if the file is valid
}

// Function to read the uploaded file
function readFile(file) {
    const reader = new FileReader();

    // When the file is successfully read, log its contents
    reader.onload = function (e) {
        // Log the file content or perform any other action with the file
        console.log("195 file_type : " + file.type);
        file_type = file.type;
        file_content = e.target.result; //returns the result of the file reading operation (readastext or dataurl or arraybuffer)
        console.log("\n\n\n\n\n file_content : " + file_content);
        file_content = file_content.substring(file_content.indexOf(",") + 1);
        // console.log("e : " + e.target.result) 
        // console.log("reader.result: " + reader.result);   
        console.log("file_content: " + file_content);

    };

    reader.readAsDataURL(file); // data: URL representing the file's data as a base64 encoded string.

}   

    //  fetch("http://192.168.100.8:5000/showsent_mails", requestOptions)
    //  	.then((response) => response.text())   //handle the server reply
    //  	.then((result) => console.log(result)) // if our app.py receives the request then it stroes the return value from that endpoint in result and prints its on console
    //  	.catch((error) => console.log("error", error)); //used to handle errors that may occur during http request


// var emails = {{ emails | tojson }};
//         console.log(emails);