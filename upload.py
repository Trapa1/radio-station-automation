import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# Load Google credentials path from environment variable
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_PATH")

if not GOOGLE_CREDENTIALS_FILE:
    raise ValueError("Google credentials path is missing. Set the environment variable GOOGLE_CREDENTIALS_PATH.")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def authenticate_youtube():
    """Authenticate YouTube API and return service."""
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=8080)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_to_youtube(file_path, title, description, tags):
    """Upload a video to YouTube."""
    youtube = authenticate_youtube()
    media = MediaFileUpload(file_path, mimetype="video/mp4", resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description, "tags": tags},
            "status": {"privacyStatus": "public"},
        },
        media_body=media
    )

    response = request.execute()
    print(f"✅ Video uploaded successfully: https://www.youtube.com/watch?v={response['id']}") 
    # here is the link to a video I made for tetsing purpose only use the studio link

