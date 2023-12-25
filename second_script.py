import csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Read the data from the temporary file
with open('temp_output.txt', 'r') as file:
  lines = file.readlines()

# Process the data
processed_data = []
current_symbol = None
current_data = []

for line in lines:
  if line.strip():  # Check if line is not empty
    parts = line.strip().split(': ')
    if len(parts) == 2:
      # New symbol entry
      if current_symbol:
        # Add previous symbol's data to processed_data
        processed_data.append([current_symbol] + current_data)
        current_data = []
      current_symbol, data = parts
      current_data.extend(
          data.split(' '))  # Adjust this split according to your data's format
    else:
      # Continuation of data for the current symbol
      current_data.extend(line.strip().split(' '))  # Adjust this split as well

# Add the last symbol's data
if current_symbol:
  processed_data.append([current_symbol] + current_data)

# Write the processed data to a CSV file
with open('outputOrganized.csv', 'w', newline='') as csvfile:
  csvwriter = csv.writer(csvfile)
  for row in processed_data:
    csvwriter.writerow(row)

# Initialize GoogleAuth and authorize
gauth = GoogleAuth()
gauth.LoadCredentialsFile("credentials.json")
if gauth.credentials is None:
  # Authenticate if they're not there
  gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
  # Refresh them if expired
  gauth.Refresh()
else:
  # Initialize the saved creds
  gauth.Authorize()
gauth.SaveCredentialsFile("credentials.json")

drive = GoogleDrive(gauth)

# Create a file and upload to drive
file = drive.CreateFile({'title': 'outputOrganized.csv'})
file.SetContentFile('outputOrganized.csv')
file.Upload()
