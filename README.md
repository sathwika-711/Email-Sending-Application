
# Email Sending Application

This project is a web application that allows users to send emails with HTML content and attachments. It uses Flask for the backend and HTML/CSS/JavaScript for the frontend. Users can enter email details, attach files, and send emails via an SMTP server.

## Features

- **Send HTML Emails**: Allows sending formatted HTML emails.
- **Attachments**: Supports attachments with size restrictions.
- **File Uploads**: Handles file uploads for attachments.
- **Responsive Design**: The application is designed to be responsive on different screen sizes.

## Technologies Used

- **Flask**: A Python web framework for handling server-side logic.
- **SMTP**: For sending emails.
- **HTML/CSS**: For structuring and styling the web pages.
- **JavaScript**: For handling client-side logic and form validations.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- pip (Python package manager)
- An SMTP server for sending emails (e.g., Gmail, SendGrid)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/email-sending-application.git
   cd email-sending-application
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**

   Create a `.env` file in the root directory and add the following variables:

   ```
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   SMTP_USERNAME=your_username
   SMTP_PASSWORD=your_password
   ```

6. **Run the Flask Application**

   ```bash
   python app.py
   ```

   The application will start running on `http://127.0.0.1:5000`.

   The application will also be accessible on your local network if you start it with `python app.py --host 0.0.0.0`.

## Usage

1. **Open the Application**

   Navigate to `http://127.0.0.1:5000` in your web browser.

2. **Fill Out the Form**

   - **From**: Enter your email address.
   - **To**: Enter the recipient's email address.
   - **Subject**: Enter the subject of the email.
   - **Body**: Enter the content of the email in HTML format.
   - **Attachments**: Choose a file to attach (PDFs up to 30MB, photos up to 1MB).

3. **Send the Email**

   Click the "Send" button to send the email. If there are any errors or missing fields, an alert box will notify you.

## Frontend

The frontend consists of an HTML form styled with CSS. The form includes input fields for email details and a file upload option. JavaScript is used to handle form validation and file processing.

### HTML Structure

- **Form**: Contains fields for the email sender, recipient, subject, body, and attachments.
- **Button**: A button to submit the form.

### CSS Styling

- **Container**: Styles the main content area.
- **Navbar**: Provides navigation options (if implemented).
- **Form Elements**: Styles input fields, buttons, and error messages.

### JavaScript

- **File Handling**: Uses `FileReader` to process and validate file uploads.
- **Form Validation**: Ensures all required fields are filled out before allowing form submission.

## Backend

The backend is implemented using Flask and handles:

- **Form Submission**: Receives form data and processes it.
- **Email Sending**: Uses `smtplib` and `MIMEMultipart` to send emails with HTML content and attachments.
- **Error Handling**: Handles and logs any errors during email sending.

### Flask Routes

- **`/`**: The main page with the email form.
- **`/sendmail`**: Endpoint to handle form submission and send the email.

## Troubleshooting

- **SMTP Errors**: Ensure SMTP server credentials and configuration are correct.
- **File Upload Issues**: Check file size and format restrictions.
- **Environment Variables**: Verify that all required environment variables are set correctly.

<!-- ## Contributing

If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request. -->

<!-- ## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. -->

## Contact

For any questions or issues, please contact [your-email@example.com](mailto:your-email@example.com).
