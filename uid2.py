from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle token submission and fetch Messenger conversations
@app.route('/get_conversations', methods=['POST'])
def get_conversations():
    access_token = request.form['access_token']
    
    # Facebook Graph API URL to get the user's basic details (name, picture, etc.)
    url = f"https://graph.facebook.com/v12.0/me?fields=id,name,picture,email,birthday,location&access_token={access_token}"

    # Send request to fetch user's details
    user_response = requests.get(url)

    if user_response.status_code == 200:
        user_data = user_response.json()
        user_id = user_data['id']
        user_name = user_data['name']
        user_picture = user_data.get('picture', {}).get('data', {}).get('url', '')
        user_email = user_data.get('email', 'Not Available')
        user_birthday = user_data.get('birthday', 'Not Available')
        user_location = user_data.get('location', {}).get('name', 'Not Available')

        # Get user's Messenger conversations (threads)
        conversations_url = f"https://graph.facebook.com/v12.0/{user_id}/conversations?access_token={access_token}"
        conversations_response = requests.get(conversations_url)
        
        if conversations_response.status_code == 200:
            conversations_data = conversations_response.json().get('data', [])
            conversation_details = []
            
            # Loop through the conversations and get each conversation's details (ID, name, etc.)
            for conversation in conversations_data:
                conversation_id = conversation['id']
                conversation_name = conversation.get('name', 'Unnamed Conversation')  # Some conversations may not have a name
                
                # Filter out unwanted conversations (optional logic, e.g., exclude system chats)
                if 'system' not in conversation_name.lower():  # Example: Ignore system-related conversations
                    conversation_details.append({'id': conversation_id, 'name': conversation_name})
            
            # Render the user information and conversations on the page
            return render_template(
                'conversations.html',
                user_name=user_name,
                user_picture=user_picture,
                user_email=user_email,
                user_birthday=user_birthday,
                user_location=user_location,
                conversations=conversation_details
            )
        else:
            return "Error fetching conversations. Please check your Facebook access token."
    else:
        return "Error fetching user information. Please check your Facebook access token."


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
