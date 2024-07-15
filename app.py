import os
from flask import Flask, request, jsonify, render_template
import openai
import requests
from dotenv import load_dotenv
from calendar_utils import add_event_to_calendar
from email_utils import send_email
from state_manager import StateManager

load_dotenv()  # Load environment variables from .env file

# Initialize Flask app
app = Flask(__name__)
state_manager = StateManager()


# Use environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
google_credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
weather_api_key = os.getenv("WEATHER_API_KEY")


# Session management
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


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():

    if 'news' in user_message.lower():
        topic = user_message.split()[-1]  # Assuming topic is the last word
        response = fetch_news(topic)
    elif 'remind me' in user_message.lower():
        event_details = parse_reminder(user_message)
        if event_details:
            response = add_event_to_calendar(event_details)
        else:
            response = "I couldn't understand the reminder details. Could you please specify again?"
    elif 'weather' in user_message.lower():
        city = user_message.split()[-1]  # Assuming city is the last word
        response = fetch_weather(city)
    elif 'joke' in user_message.lower():
        response = fetch_joke()
    elif 'quote' in user_message.lower():
        response = fetch_quote()
    else:
        response = det_gpt_response(user_message, user_id)

    return jsonify({'response': response})


def process_message(message, user_id):
    # Use Spacy for advanced NLP processing
    doc = nlp(message)
    intents = [ent_label_ for ent in doc.ents]

    # Manage state and context
    context = state_manager.get_context(user_id)
    context['intents'] = intents

    # Simple rule-based intent handling
    if 'EVENT' in intents:
        response = "I can help you schedule an event. When would you like to see it?"
    elif 'EMAIL' in intents:
        response = "I can send an email for you. What would you like the email to say?"
    else:
        # Fallback to OpenAI GPT-3 for general conversation
        response = openai.Completion.create(
            engine="davinci",
            prompt=message,
            max_tokens=150,
        ).choices[0].text.strip()

    state_manager.set_context(user_id, context)
    return response, context


if __name__ == '__main__':
    app.run(debug=True)


def fetch_news(topic):
    url = f'https://newsapi.org/v2/top-headlines?q={topic}&apiKey={news_api_key}'
    response = requests.get(url).json()
    articles = response['articles']
    news = [f"{article['title']} - {article['source']['name']}" for article in articles[:5]]
    return "\n".join(news)


def fetch_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'
    response = requests.get(url).json()
    if response.get('cod') != 200:
        return f"Could not retrieve weather data for {city}. Please check the city name."
    weather = response['weather'][0]['description']
    temp = response['main']['temp']
    return f"The current weather in {city} is {weather} with a temperature of {temp}°C"


def fetch_joke():
    url = f'http://api.icnublue.com/Jokes/random'
    response = requests.get(url).json()
    return f"{response['setup']} - {response['punchline']}"


def fetch_quote():
    url = f'http://api.icnublue.com/Quotes/random'
    response = requests.get(url).json()
    return f"{response['content']} - {response['author']}"


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













