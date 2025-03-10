# radio-station-automation

#  Radio Station YouTube Uploader

This project **automates** the process of **uploading DJ videos** from **Dropbox to YouTube** when a **Google Form** is submitted. 

 Just fill out the form, and the video is uploaded! 

---

##  **How It Works **

1. ** A DJ submits a Google Form**  
   - The form contains: **Title, Description, Dropbox Video Link, Date of Show, Tags**.
   - The form responses go into a **Google Sheet**.

2. ** The script checks the Google Sheet**  
   - It looks for new form submissions.
   - It **matches the show date** with available **videos in Dropbox**.

3. ** The script downloads the correct video from Dropbox**  
   - The video file is pulled from the Dropbox folder.

5. ** The script uploads the video to YouTube**  
   - It uses the form details (title, description, tags, privacy settings).
   - The **YouTube link** is printed when the upload is successful.

---

##  **Setup Instructions (How to Get It Working)**

### **1️ Install Required Python Libraries**
Run this command in **Terminal** or **Command Prompt**:

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client gspread pandas dropbox python-dotenv 


2️ Set Up Your API Credentials
You need:  A Google API Client Secret JSON (for YouTube & Google Sheets).
 A Dropbox Access Token.

 How to Add API Credentials Securely Instead of saving API keys in the code, use environment variables.  DROPBOX_ACCESS_TOKEN=your_dropbox_access_token_here
GOOGLE_CREDENTIALS_PATH=path_to_your_google_client_secret.json
 

🔄 How to Run the Script
Once everything is set up, run:

python main.py

This will: Check the Google Form submissions
 Find the right video in Dropbox
 Download the video
 Upload it to YouTube

 Automating the Process (So It Runs on Its Own)
You can set up a scheduled task so you don’t have to run the script manually every time.

 Windows (Task Scheduler)
Open Task Scheduler.
Click Create Basic Task.
Choose Daily or Hourly.
Under Action, select Start a Program.

 What happens if a DJ submits two forms?
The script will upload both videos separately with their correct details.

 What if the video isn’t found in Dropbox?
The script won’t upload anything and will print: "No matching videos found."






