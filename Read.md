2. Setup Instructions
Clone the repository:

git clone https://github.com/your-username/file-sharing-system.git
cd file-sharing-system
Create and activate a virtual environment:


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:


pip install -r requirements.txt
Set up environment variables:


bash
uvicorn app.main:app --reload




API Endpoints
1. User Management
Endpoint	Method	Description	Role
/auth/signup	POST	Register a new user	Public
/auth/login	POST	Login and get access token	Public
/auth/verify-email/{email}	POST	Verify a user's email	Publi


3. File Management
Endpoint	Method	Description	Role
/file/upload	POST	Upload a file	Operator
/file/allfiles	GET	Fetch all uploaded files	Admin
/file/download-file/{file_id}	GET	Generate secure download link	Client
/download-fle/{encrypted_url}	GET	Download the file from the secure link	Client
Postman Collection
You can import the Postman Collection to test all API endpoints easily.

