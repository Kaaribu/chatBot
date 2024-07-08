import os
from flask import Flask, request, jsonify
import openai
import requests
from dotenv import load_dotenv
from calendar_utils import add_event_to_calendar

load_dotenv()  # Load environment variables from .env file

# Use environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
google_credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")

app = Flask(__name__)
sessions = {}


def get_session(user_id):
    if user_id not in sessions:
        sessions[user_id] = {'history': ''}
    return sessions[user_id]


def det_gpt_response(user_message, user_id):
    session = get_session(user_id)
    conversation_history = session['history'] + f"\nUser: {user_message}\nAI:"
    response = openai.Completion.create(
        engine=openai.Engine('gpt-4'),
        prompt=conversation_history,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7, top_p=1, frequency_penalty=0.5,
    )
    session['history'] = conversation_history + response.choices[0].text.strip() + "\n"
    return response.choices[0].text.strip()


@app.route('/chat', methods=['POST'])
def chat():  # put application's code here
    user_message = request.json.get('message')
    user_id = request.json.get('user_id')

    if 'news' in user_message.lower():
        topic = user_message.split()[-1]  # Assuming topic is the last word
        response = fetch_news(topic)
    elif 'remind me' in user_message.lower():
        event_details = parse_reminder(user_message)
        if event_details:
            response = add_event_to_calendar(event_details)
        else:
            response = "I couldn't understand the reminder details. Could you please specify again?"

    else:
        response = det_gpt_response(user_message, user_id)

    return jsonify({'response': response})


def fetch_news(topic):
    url = f'https://newsapi.org/v2/top-headlines?q={topic}&apiKey={news_api_key}'
    response = requests.get(url).json()
    articles = response['articles']
    news = [f"{article['title']} - {article['source']['name']}" for article in articles[:5]]
    return "\n".join(news)

def parse_reminder(user_message):
    import re
    from datetime import datetime, timedelta

    match = re.search(r"remind me to (.+) at (\d+:\d+ (AM|PM))", user_message, re.IGNORECASE)
    if match:
        summary = match.group(1)
        time_str = match.group(2)
        time_obj = datetime.strptime(time_str, "%H:%M")
        now = datetime.now()
        reminder_time = datetime.combine(now.date(), time_obj.time())
        if reminder_time < now:
            reminder_time += timedelta(days=1)

        event_details = {
            'summary': summary,
            'start': reminder_time.isoformat(),
            'end': (reminder_time + timedelta(minutes=30)).isoformat()
        }
        return event_details
    return None


if __name__ == '__main__':
    app.run(debug=True)













