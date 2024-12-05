# Urban Lab Project

The **Urban Lab Project** is designed to build a robust and scalable database system for managing student and contact interactions, events, and grants in urban development and sustainability research environments.

## Features

- **Student Management**: Track and manage student information, including their personal details, course enrollments, and interactions with events and contacts.
- **Contact Management**: Manage contacts such as professors, employers, and industry representatives.
- **Event Tracking**: Record details of various events such as seminars, workshops, and field trips.
- **Interaction Management**: Track interactions between students, contacts, and events with detailed notes.
- **Grant Tracking**: Manage information on recurring grants, including start and end dates, frequency, and purpose.

## Technologies Used

- **Frontend**: Vue.js, Bootstrap (for styling)
- **Backend**: Flask (Python), Flask-JWT-Extended (for authentication)
- **Database**: MySQL
- **Authentication**: JSON Web Tokens (JWT)

## Setup and Installation

### 1. Clone the repository
Clone the project to your local machine:
```bash
git clone https://github.com/your-username/urban-lab-project.git
2. Install Backend Dependencies
Navigate to the backend directory and install Python dependencies:

bash
Copy code
cd urbanlab_backend
pip install -r requirements.txt  # Install the Python dependencies
3. Set Up MySQL Database
Make sure you have MySQL installed and running on your machine.

Create a new database for the project:

sql
Copy code
CREATE DATABASE urbanlab_db;
Set up the tables using the SQL scripts provided in the repository, or manually create the necessary tables based on the schema.

4. Start the Backend
In the backend directory, run the Flask application:

bash
Copy code
python app.py  # This starts the Flask server
The backend will now be available at http://127.0.0.1:5000.

5. Install Frontend Dependencies
Navigate to the frontend directory and install the frontend dependencies:

bash
Copy code
cd urbanlab_frontend
npm install  # Install Node.js dependencies
6. Run the Frontend
In the frontend directory, run the Vue application:

bash
Copy code
npm run serve  # This starts the Vue.js development server
The frontend will be available at http://localhost:8080.

7. Access the Application
Open your browser and go to http://localhost:8080 for the frontend.
The backend will be running at http://127.0.0.1:5000.
8. Login and Admin Panel
Use the login page to authenticate as an admin or regular user.
Admin users can access the Register User page to add new users to the system.
API Endpoints
Authentication
POST /auth/login
Login with a username and password. Returns a JWT token upon successful login.

Request body: { "username": "your-username", "password": "your-password" }
Response: { "access_token": "your-jwt-token" }
POST /auth/register (Admin only)
Register a new user. Only accessible by admin users.

Request body: { "username": "new-username", "password": "new-password", "role": "user/admin" }
Students
GET /students
Fetch a list of all students.

POST /students
Add a new student.

PUT /students/{id}
Update student details.

DELETE /students/{id}
Delete a student.

Contacts
GET /contacts
Fetch a list of all contacts.

POST /contacts
Add a new contact.

PUT /contacts/{id}
Update contact details.

DELETE /contacts/{id}
Delete a contact.

Events
GET /events
Fetch a list of all events.

POST /events
Add a new event.

PUT /events/{id}
Update event details.

DELETE /events/{id}
Delete an event.

Interactions
GET /interactions
Fetch a list of all interactions between students, contacts, and events.

POST /interactions
Create a new interaction record.

Grants
GET /grants
Fetch a list of all grants.

POST /grants
Add a new grant.

PUT /grants/{id}
Update grant details.

DELETE /grants/{id}
Delete a grant.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature/your-feature).
Create a new Pull Request.
