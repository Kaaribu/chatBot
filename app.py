from flask import Flask, request, jsonify
import openai

app = Flask(__name__)
openai.api_key = 'sk-proj-JBYxJV5qMmEDmzeORALoT3BlbkFJ1dJk7EKoWxP11lg61rJX'
sessions = {}


def get_session(user_id):
    if user_id not in sessions:
        sessions[user_id] = {'history': ''}
    return sessions[user_id]


def det_gpt_response(user_message, user_id):
    session = get_session(user_id)
    conversation_history = session['history'] + f"\nUser: {user_message}\nAI:"
    response = openai.Completion.create(
        engine=openai.Engine('gpt-4'), prompt=conversation_history,
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
    response = det_gpt_response(user_message, user_id)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)













