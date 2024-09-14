

console.log("sent_emails.js")

fetch("http://localhost:5000/getsentmails")
.then((response) => response.json())
.then((data) => {   //data contains the return value from the backend of getsentmails endpoint contains all the sent emails stored in database
    console.log(data);
    details(data);
})
.catch((error) => {
    console.log("error", error);
});


// Close the dialog box
function closeDialog() {
    document.getElementById('dialog').style.display = 'none';
}



function details(data)
{
    data.forEach(function(get_data) {
        // Create a new table row
        const row = document.createElement('tr');
        row.addEventListener('click', (event) => {

            // Set dialog content body, filename  (current target contains the details of table row)
            document.getElementById('dialog-body').innerHTML = event.currentTarget.children[4].textContent;  //body of the email
            let file_name_dialog = document.getElementById('dialog-file-name');  // storing id of file name
            file_name_dialog.textContent = event.currentTarget.children[6].textContent; // get and store file name from current target

            // if no attachments, display dialog box with body of email
            if (file_name_dialog.textContent == "") {
                document.getElementById('dialog-attachments').style.display = 'none';
            }
            // else display attachments in dialog box
            else {
            console.log(file_name_dialog.textContent);
            let embebedElement = document.getElementById('document-dialog');
            embebedElement.href = event.currentTarget.children[5].textContent;          // file-content: passing file conent to href 
            embebedElement.download = event.currentTarget.children[6].textContent;
            document.getElementById('dialog-attachments').style.display = 'block';   
           }   // file-name: passing file name to download (.download is an attribute of <a> tag)

            // Show the dialog
            document.getElementById('dialog').style.display = 'flex';
            console.log(event.currentTarget)
            console.log("clicked the row")
        })
    
        // Create and append cells to the row

        // create and append sender name
        const senderCell = document.createElement('td');
        senderCell.textContent = get_data.sender_name;
        row.appendChild(senderCell);
    
        // create and append receiver email
        const toCell = document.createElement('td');
        toCell.textContent = get_data.to_email;
        row.appendChild(toCell);

        // create and append receiver name
        const receiverCell = document.createElement('td');
        receiverCell.textContent = get_data.receiver_name;
        row.appendChild(receiverCell);
    
        // create and append subject
        const subjectCell = document.createElement('td');
        subjectCell.textContent = get_data.subject;
        row.appendChild(subjectCell);
        
        // create and append body
        const bodyCell = document.createElement('td');
        bodyCell.classList.add('hidden-td');
        bodyCell.textContent = get_data.body;
        row.appendChild(bodyCell);

        // create and append attachments of file_Content
        const fileDataCell = document.createElement('td');
        fileDataCell.classList.add('hidden-td');
        fileDataCell.textContent = "data:" + get_data.attachment.file_type + ";base64," + (get_data.attachment.file_content);
        console.log("textContent: " + fileDataCell.textContent)
        row.appendChild(fileDataCell);

        // create and append attachments of file_name
        const fileNameCell = document.createElement('td');
        fileNameCell.classList.add('hidden-td');
        fileNameCell.textContent = get_data.attachment.file_name;
        row.appendChild(fileNameCell);

        // create and append attachments of file_type
        let fileTypeCell = document.createElement('td');
        fileTypeCell.classList.add('hidden-td');
        fileTypeCell.textContent = get_data.attachment.file_type;
        row.appendChild(fileTypeCell);
    
        // Append the row to the table body
        document.querySelector('#emailTable tbody').appendChild(row);
    });
}

