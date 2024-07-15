# ChatBot
My virtual assistant powered by GPT.

This project implements a simple AI-based chatbot using OpenAI's GPT-3 for natural language processing and various APIs for fetching news, weather information, jokes, and quotes. The chatbot is integrated with Google Calendar API to set reminders.

## Features
- Natural Language Processing: Uses OpenAI's GPT-3 engine for conversational AI.
- News: Fetches top headlines based on user queries.
- Weather: Retrieves current weather conditions for specified cities.
- Jokes: Provides random jokes for entertainment.
- Quotes: Shares inspirational and motivational quotes.
- Calendar Integration: Allows users to set reminders using Google Calendar.

## Technologies Used

- Python
- Flask: Web framework for serving the chatbot interface.
- OpenAI API: For natural language processing.
- Google Calendar API: For calendar integration.
- News API: For fetching news headlines.
- OpenWeatherMap API: For retrieving weather data.
- Other libraries: Requests, dotenv (for environment variables).

## Setup Instructions

1. Clone the Repository:

   `git clone https://github.com/yourusername/chatbot-project.git`
   `cd chatbot-project`

2. Install Dependencies:

   `pip install -r requirements.txt`

3. Set Up Environment Variables:
   Create a .env file in the root directory with the following variables:

   OPENAI_API_KEY=your_openai_api_key
   NEWS_API_KEY=your_news_api_key
   WEATHER_API_KEY=your_weather_api_key
   GOOGLE_CREDENTIALS_PATH=path_to_your_google_credentials_file

4. Run the Application:

   `flask run`

    Access the chatbot interface at http://localhost:5000 in your web browser.

## Usage

- Type messages in the input box and click "Send" to interact with the chatbot.
- Commands like asking for news (news topic), setting reminders (remind me to do something at time), checking weather (weather city), jokes (tell me a joke), and quotes (give me a quote) are supported.

## Example Commands

- News: "Show me the latest news about technology."
- Weather: "What's the weather in New York?"
- Jokes: "Tell me a joke."
- Quotes: "Give me an inspirational quote."
- Set Reminder: "Remind me to call John at 5 PM tomorrow."

## Project Structure

 /chatbot
├── app.py
├── calendar_utils.py
├── email_utils.py
├── state_manager.py
├── .env
├── templates
│   └── index.html
├── static
│   ├── css
│   │   └── styles.css
│   └── js
│       └── scripts.js
├── requirements.txt
└── venv

## Contributing

Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- OpenAI for providing access to GPT-3.
- Google for the Calendar API.
- News API for news headlines.
- OpenWeatherMap for weather data.

