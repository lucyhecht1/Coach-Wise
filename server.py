from flask import Flask, request, jsonify, render_template, redirect, url_for
from test_openai import generate_basketball_play, refine_play, generate_inbound_play, new_imbound
import openai
import openai_secrets

app = Flask(__name__)

# for GPT
openai.api_key = openai_secrets.SECRET_KEY

# Basic data representation for basketball play
play_data = {
    "players": "",
    "defense": "",
    "generated_play": ""
}

sample_play_data = {
    "players": "",
    "defense": "",
    "generated_play": ""
}

# Initialize play data with sample data
play_data = sample_play_data


@app.route('/submit_players', methods=['POST'])
def submit_players():
    """API endpoint to submit player and defense info and generate both play types."""
    global play_data
    data = request.json
    players = data.get('players')
    defense = data.get('defense')

    print("Received players:", players)  # Debugging log
    print("Received defense:", defense)  # Debugging log

    # Generate the offensive play
    generated_play = generate_basketball_play(players, defense)
    if not generated_play:
        generated_play = "Error: Could not generate a basketball play."

    inbound_play = generate_inbound_play(players, defense)
    if not inbound_play:
        inbound_play = "Error: Could not generate an inbound play."

    # Update play data
    play_data.update({
        "players": players,
        "defense": defense,
        "generated_play": generated_play,
        "inbound_play": inbound_play
    })

    return jsonify(play_data)

@app.route('/generate-play', methods=['GET'])
def generate_play():
    """Render the generate-play page to display the generated play and court."""
    global play_data
    
    # Make sure to check if players and defense are available
    players = play_data.get("players")
    defense = play_data.get("defense")

    # You could regenerate the play here if necessary
    generated_play = play_data.get("generated_play")
    
    if not generated_play:
        generated_play = generate_basketball_play(players, defense)  # Generate if not already done
    
    return render_template('generate-play.html', data=play_data)


@app.route('/refine_play', methods=['GET', 'POST'])
def refine_play_route():
    """API endpoint to refine a generated play based on player performance."""
    global play_data
    data = request.get_json()   
    player_name = data.get("player_name")

    # Refine the play for the player having an off night
    refined_play = refine_play(play_data["generated_play"], player_name)

    # Update play data with the refined play
    play_data["generated_play"] = refined_play

    # Send back the whole array of data, so the client can redisplay it
    return jsonify(play_data)


@app.route('/inbound-play', methods=['GET', 'POST'])
def inbound_play():
    """Render the inbound-play page and generate the inbound play using AI."""
    global play_data

    if request.method == 'POST':
        # Use the player and defense info to generate the inbound play
        players = play_data.get("players")
        defense = play_data.get("defense")

        # Generate the inbound play using AI
        inbound_play = generate_inbound_play(players, defense)
        
        if not inbound_play:
            inbound_play = "Error: Could not generate an inbound play."

        # Update play data with the generated play
        play_data["inbound_play"] = inbound_play

        return jsonify({"inbound_play": inbound_play})

    # Render the inbound-play page with the current play data
    return render_template('inbound-play.html', data=play_data)

@app.route('/new_inbound_play', methods=['POST'])
def new_inbound_play():
    """API endpoint to generate a new inbound play using the new_imbound function."""
    global play_data

    players = play_data.get("players")
    defense = play_data.get("defense")

    # Generate a new inbound play using the new_imbound function
    new_inbound_play = new_imbound(players, defense)

    # Update play data with the newly generated inbound play
    play_data["inbound_play"] = new_inbound_play

    return jsonify(play_data)


@app.route('/home')
def home():
    """Render the home page with play data."""
    return render_template('home.html', data=play_data)


@app.route('/')
def welcome_page():
    """Render the welcome page to introduce the site."""
    return render_template('welcome.html')


if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
