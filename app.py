from flask import Flask, request, jsonify
import os
import logging

import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = 'C:/Users/Batin/Downloads/abingusfile.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate using the service account
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Create a service object
service = build('sheets', 'v4', credentials=credentials)

# Google Sheets ID and range
SPREADSHEET_ID = '15DLTDRqGt6Z9wN0x2UXmE9S28cpWp5Q-2Vvyo8-006o'
RANGE_NAME = 'Sheet1!C2'  # Row 1, Column 1



app = Flask(__name__)
if not app.debug:  # Only configure logging when not in debug mode
    logging.basicConfig(level=logging.INFO)  # Adjust level to INFO, DEBUG, etc.
    app.logger.setLevel(logging.INFO)
    
@app.route('/webhook/<endpoint>', methods=['POST'])
def dynamic_webhook(endpoint):
    print("Starting Now")
    print("Headers:", request.headers)  # Print request headers
    print("Raw Data:", request.data)    # Print raw payload
    
    # Safely attempt to parse JSON
    try:
        data = request.get_json()
        if data is None:
            raise ValueError("No JSON in request")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        # Respond with "I love you" on JSON parse failure
        return jsonify({"response": "I love you"}), 200
    app.logger.info(f"Received data for {endpoint}: {data}")
    print(f"Received data for {endpoint}: {data}")
    tempWorkflow = getWorkflow(data.get("message"))
    if tempWorkflow:
        return jsonify({"Response": tempWorkflow}), 200
    return jsonify({"Response": "Failed"}), 200

def getWorkflow(companyName):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    value = result.get('values', [])
    print("Here is the value:" + value[0][0])
    print("This is companyName:" + companyName)
    if value[0][0] == companyName:
        newRange = 'Sheet1!F2'
        newResult = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=newRange).execute()
        newValue = newResult.get('values', [])
        print("Here is the newValue:" + newValue[0][0])
        return newValue[0][0]
    return None

if __name__ == '__main__':
    print("About to start")
    # Use the PORT environment variable if available, default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
