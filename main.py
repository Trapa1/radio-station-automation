import pandas as pd
from get_dropbox_files import get_dropbox_files, extract_date_from_filename
from parse_google_doc import get_google_sheet
from upload import upload_to_youtube

def filter_files_by_date(form_data, dropbox_files):
    """
    Filter Dropbox files by matching date from Google Sheet form data
    """
    dropbox_files['Date'] = dropbox_files['Name'].apply(lambda x: extract_date_from_filename(x))

    # Merge Google Sheet data with Dropbox files based on 'Date of Show'
    form_data['Date of Show'] = form_data['Date of Show'].dt.strftime('%d-%m-%Y')  # Format Google Sheet date
    merged_data = pd.merge(form_data, dropbox_files, left_on='Date of Show', right_on='Date', how='inner')

    return merged_data

def main():
    # Retrieve form data from Google Sheets
    metadata = get_google_sheet()

    # Get Dropbox files
    folder_path = '/Youtube videos'  # Your Dropbox folder path
    dropbox_files = get_dropbox_files(folder_path)

    # Filter Dropbox files based on matching date
    merged_data = filter_files_by_date(metadata, dropbox_files)

    if not merged_data.empty:
        # Example: You can loop through the filtered data and upload to YouTube
        for index, row in merged_data.iterrows():
            video_path = f"test/input/{row['Name']}"  # Assuming videos are in the 'test/input' folder
            title = f"{row['Show Name']} on Brixton Radio: {row['Date of Show']}"
            description = f"{row['Description']} Recorded live @brixtonradio {row['Date of Show']}"
            tags = ['Brixton Radio', 'DJ Mix', 'Music']

            # Upload video to YouTube
            upload_to_youtube(video_path, title, description, tags)
    else:
        print("No matching videos found for today's date.")

if __name__ == "__main__":
    main()

# import os
# import pandas as pd
# from datetime import datetime, timedelta
# import dropbox
# from googleapiclient.discovery import build
# from google.auth.transport.requests import Request
# from google_auth_oauthlib.flow import InstalledAppFlow
# from get_dropbox_files import get_dropbox_files  # Import function for Dropbox

# # Function to convert start time to a proper time object
# def convert_start_time(start_time):
#     if isinstance(start_time, datetime):
#         start_time_str = start_time.strftime("%I:%M:%S %p")
#     else:
#         start_time_str = start_time
    
#     try:
#         return datetime.strptime(start_time_str, "%I:%M:%S %p").time()
#     except ValueError as e:
#         print(f"Error parsing time: {e}")
#         return None
# def extract_date_from_filename(file_name):
#     """
#     Extract date from Dropbox file name format: ShowName_dd-mm-yyyy.mp4
#     """
#     # Assuming the format is like 'ShowName_28-11-2024.mp4', extract '28-11-2024'
#     try:
#         # Split the file name by underscores and extract the date part, then remove '.mp4'
#         date_str = file_name.split('_')[-1].replace('.mp4', '')  # Example: Extract '28-11-2024'
#         # Convert the string into a datetime object
#         date_obj = datetime.strptime(date_str, "%d-%m-%Y")  # Expected date format: dd-mm-yyyy
#         return date_obj
#     except ValueError as e:
#         print(f"Error parsing date from filename '{file_name}': {e}")
#         return None

# # Function to retrieve data from Google Sheets
# def get_google_sheet():
#     link = "https://docs.google.com/spreadsheets/d/1xTZmYzrNLpuFIMBBwiRp5dBi4Q6zhMWmdcKJ5-IJSZ4/gviz/tq?tqx=out:csv&sheet=Form_Responses1"
#     df = pd.read_csv(link)

#     df.columns = df.columns.str.strip().str.replace('\n', ' ')
    
#     # Ensure 'Date of Show' is in datetime format
#     date_col = 'Date of Show'
#     time_col = 'Start Time'

#     try:
#         df[date_col] = pd.to_datetime(df[date_col])
#     except Exception as e:
#         print(f"Error converting '{date_col}' to datetime:", e)
#         return None

#     # Apply the function to convert 'Start Time' to time
#     df[time_col] = df[time_col].apply(convert_start_time)

#     # Combine 'Date of Show' and 'Start Time' into a single datetime column
#     df['Show datetime'] = pd.to_datetime(df[date_col].astype(str) + ' ' + df[time_col].astype(str))

#     # Create new columns '30m before' and '30m after'
#     df['30m before'] = df['Show datetime'] - timedelta(minutes=30)
#     df['30m after'] = df['Show datetime'] + timedelta(minutes=30)

#     print(df.head())  # Print the first few rows to check data
#     return df

# # Function to filter Dropbox files by matching date
# def filter_files_by_date(form_data, dropbox_files):
#     print("Dropbox files DataFrame:", dropbox_files)  # Print DataFrame to check if 'Name' column exists
#     dropbox_files['Date'] = dropbox_files['Name'].apply(lambda x: extract_date_from_filename(x))  # Assuming you have extract_date_from_filename implemented

#     form_data['Date of Show'] = form_data['Date of Show'].dt.strftime('%d-%m-%Y')
#     merged_data = pd.merge(form_data, dropbox_files, left_on='Date of Show', right_on='Date', how='inner')

#     return merged_data

# # Main function to control the workflow
# def main():
#     # Get Google Sheet data
#     metadata = get_google_sheet()
#     if metadata is None:
#         print("Error retrieving or processing Google Sheets data.")
#         return
    
#     # Get Dropbox files
#     folder_path = '/Youtube videos'  # Replace with your actual Dropbox folder path
#     dropbox_files = get_dropbox_files(folder_path)

#     # Filter Dropbox files by matching date
#     merged_data = filter_files_by_date(metadata, dropbox_files)




#     if not merged_data.empty:
#         for index, row in merged_data.iterrows():
#             video_path = f"test/input/{row['Name']}"  # Assuming videos are in the 'test/input' folder
#             title = f"{row['Show Name']} on Brixton Radio: {row['Date of Show']}"
#             description = f"{row['Description']} Recorded live @brixtonradio {row['Date of Show']}"
#             tags = ['Brixton Radio', 'DJ Mix', 'Music']
            
#             # Upload video to YouTube
#             upload_to_youtube(video_path, title, description, tags)
#     else:
#         print("No matching videos found for today's date.")

# if __name__ == "__main__":
#     main()
