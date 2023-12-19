import requests
from googleapiclient.discovery import build
from google.cloud import language

SPREADSHEET_ID = '1tiEayQap3n2jWdD0SFER0whEa9DHNwSJWnfCpBcKHRA'
RANGE_NAME = 'Sheet1!A1:B26'
API_KEY = 'api-key'

def authenticate_sheets(api_key):
    return build('sheets', 'v4', developerKey=api_key).spreadsheets()

def analyze_sentiment(text):
    endpoint_url = "https://language.googleapis.com/v1/documents:analyzeSentiment?key=" + API_KEY

    document = {"content": text, "type": language.Document.Type.PLAIN_TEXT}
    request_data = {"document": document}

    response = requests.post(endpoint_url, json=request_data)
    response_json = response.json()

    sentiment = response_json.get("documentSentiment", {}).get("score", None)
    return sentiment


if __name__ == '__main__':

    sheets = authenticate_sheets(API_KEY)
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    sentiment_count = 0
    sentiment_sum = 0

    if not values:
        print('No data found.')
    else:
        print('User, Comment, Sentiment:')
        for row in values:
            sentiment_score = analyze_sentiment(row[1])
            print(f'{row[0]}, {row[1]}, {sentiment_score}')
            sentiment_sum = sentiment_sum + sentiment_score
            sentiment_count = sentiment_count + 1
        sentiment_average = sentiment_sum / sentiment_count
        print(f'Average: {sentiment_average}')

