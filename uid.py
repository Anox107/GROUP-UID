from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle token submission and fetch Messenger groups
@app.route('/get_groups', methods=['POST'])
def get_groups():
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

        # Get user's Messenger groups (conversations)
        groups_url = f"https://graph.facebook.com/v12.0/{user_id}/conversations?access_token={access_token}"
        groups_response = requests.get(groups_url)
        
        if groups_response.status_code == 200:
            groups_data = groups_response.json().get('data', [])
            group_details = []
            
            # Loop through the groups and get each group's details (ID and name)
            for group in groups_data:
                group_id = group['id']
                group_name = group.get('name', 'Unnamed Group')  # Some groups may not have a name
                
                group_details.append({'id': group_id, 'name': group_name})
            
            # Render the user information and groups on the page
            return render_template(
                'groups.html',
                user_name=user_name,
                user_picture=user_picture,
                user_email=user_email,
                user_birthday=user_birthday,
                user_location=user_location,
                user_id=user_id,
                groups=group_details
            )
        else:
            return "Error fetching groups. Please check your Facebook access token."
    else:
        return "Error fetching user information. Please check your Facebook access token."


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
