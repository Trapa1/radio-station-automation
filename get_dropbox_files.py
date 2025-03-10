import dropbox
import re

# Read Dropbox access token from file
with open("dropbox_access_token.txt", "r") as f:
    DROPBOX_ACCESS_TOKEN = f.read().strip()

dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def extract_date_from_filename(filename):
    """Extract date from filenames formatted as DD-MM-YYYY."""
    match = re.search(r'(\d{2}-\d{2}-\d{4})', filename)
    return match.group(1) if match else None

def get_dropbox_files(folder_path):
    """List all files in a Dropbox folder."""
    try:
        response = dbx.files_list_folder(folder_path)
        files = [{"Name": entry.name, "Path": entry.path_lower} for entry in response.entries]
        return pd.DataFrame(files)
    except Exception as e:
        print(f" Error fetching Dropbox files: {e}")
        return pd.DataFrame()
