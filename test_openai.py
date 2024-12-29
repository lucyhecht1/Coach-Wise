import openai  # Import the OpenAI package
import textwrap as tw
import openai_secrets  # Assuming openai_secrets holds your API key
import traceback

# Set your OpenAI API key
openai.api_key = openai_secrets.SECRET_KEY

def print_result_wrapped(result):
    """Helper function to neatly print the output."""
    if result:  # Only wrap the result if it exists
        wrapped_result = tw.wrap(result)
        print("\n".join(wrapped_result))
    else:
        print("No result to display.")

def generate_basketball_play(players, defense):
    """Generates a basketball play based on the players and defense."""
    try:
        prompt = f"""
        Create a basketball play for the following players: {players}.
        They are playing against a {defense} defense. Provide a clear strategy.
        Generate a detailed play explanation. When referring to the players, simply refer to them by their first names.
        Provide your answer in the following format. Do not deviate from this format:

        1. **Name the play**: Give the play a name that the point guard could call out. It should be catchy and short. Not more than 2 words.
        2. **General setup**: Briefly describe how the players should position themselves on the court. Each player should be on a new line.
        3. **Main objective**: Explain what the play is designed to achieve.
        4. **Detailed play breakdown**: Step-by-step, describe each part of the play. Each step should be on a new line.
        4. **Summarize the play**: Step-by-step, describe each part of the play. Each step should be on a new line.

        Example:
        1. Play name: Quick Swing
        2. General setup:
            - Player 1: Top of the key
            - Player 2: Right wing
            - Player 3: Left corner
            - Player 4: Low post
            - Player 5: High post
        3. Main objective: Create an open 3-point shot for Player 3 in the corner.
        4. Play breakdown:
            - Step 1: Player 1 dribbles to the right wing.
            - Step 2: Player 5 sets a screen for Player 3.
            - Step 3: Player 3 moves to the corner for an open shot.
        5. Summary:
            - Player 1:
            - Player 2:
            - Player 3:
            - Player 4:
            - Player 5:
        """

        # Log the prompt for debugging
        print("OpenAI Prompt:", prompt)

        # Use the correct API method for chat completions
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512
        )

        # Log the full response for debugging
        print("OpenAI API Response:", response)

        # Extract the generated play from the response
        generated_play = response['choices'][0]['message']['content'].strip()
        return generated_play

    except Exception as e:
        print(f"OpenAI API call failed: {e}")
        traceback.print_exc()
        return None

def refine_play(generated_play, player_name):
    """Refines the play if a specific player is having an off night."""
    prompt_for_refinement = f"""
    Given the following offensive play:

    {generated_play}

    The player, {player_name}, is having an off night and should not be taking shots.
    Instead, modify the play so that {player_name} sets picks and focuses on passing.
    Ensure the play still maximizes the strengths of other players.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are advising a basketball coach."},
                {"role": "user", "content": prompt_for_refinement}
            ],
            max_tokens=512
        )

        refined_play = response['choices'][0]['message']['content'].strip()
        return refined_play
    except Exception as e:
        print(f"Failed to refine the play: {e}")
        traceback.print_exc()
        return None
    
def generate_inbound_play(players, defense):
    """Generates an inbounds basketball play based on the players and a 2-3 defense."""
    try:
        prompt = f"""
        You are always inbouning the ball from under the basket.
        Create an inbounds basketball play for the following players: {players}.
        They are playing against a {defense} defense. The play should focus on getting the ball in safely and setting up an immediate scoring opportunity.
        Feel free to utilize off-ball screens so weak-side players can get open.
        Always say that the inbounder should come in bounds after they pass in the first pass.
        Provide a clear and structured explanation. Use the following format:

        1. Name the play: Give the play a catchy and short name. It should describe the formation that the player's start in.
        2. Inbounds setup: Describe the positioning of each player relative to the inbounder. Each player should be on a new line.
        3. Objective: Explain what the inbounds play aims to achieve (e.g., layup, quick shot, safe pass, isolation).
        4. Play breakdown: Provide a step-by-step breakdown of the play, highlighting where each player moves on the court.
        5. Summary: Summarize the play with the expected outcome and any contingency plans if the initial option is denied.

        Example:
        1. Inbounds play name - it should describe the set up (ex. stack, box, 4-across):
        2. General setup:
            - Player 1: Inbounding under the basket
            - Player 2: bottom of the stack,
            - Player 3: second in the stack,
            - Player 4: third in the stack,
            - Player 5: fourth in the stack,
        3. Main objective: Set a screen for player 3 to get an easy layup.
        4. Play breakdown:
            - Step 1: Player 2 sets a screen for Player 3.
            - Step 2: Player 3 gets open.
            - Step 3: Player 1 passes in the ball.
            - etc. etc.
        5. Summary:
            - Player 1:
            - Player 2:
            - Player 3:
            - Player 4:
            - Player 5:
        """

        print("OpenAI Inbounds Play Prompt:", prompt)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512
        )

        print("OpenAI API Inbounds Play Response:", response)

        # Extract the generated play from the response
        inbound_play = response['choices'][0]['message']['content'].strip()

        # Post-process the response to ensure new lines after each numbered section
        formatted_play = (
            inbound_play.replace("1.", "\n1.")
                        .replace("2.", "\n2.")
                        .replace("3.", "\n3.")
                        .replace("4.", "\n4.")
                        .replace("5.", "\n5.")
        )

        return formatted_play

    except Exception as e:
        print(f"Failed to generate inbounds play: {e}")
        traceback.print_exc()
        return None

def new_imbound(players, defense):
    """Redo the imbounds play so that I can compare my options"""
    prompt_for_refinement = f"""
            You are always inbouning the ball from inder the basket.
        Create an inbounds basketball play for the following players: {players}.
        They are playing against a {defense} defense. The play should focus on getting the ball in safely and setting up an immediate scoring opportunity.
        Feel free to utilize off-ball screens so weak-side players can get open.
        Always say that the inbounder should come in bounds after they pass in the first pass.
        Provide a clear and structured explanation. Use the following format:

        1. Name the play: Give the play a catchy and short name.
        2. Inbounds setup: Describe the positioning of each player relative to the inbounder. Each player should be on a new line.
        3. Objective: Explain what the inbounds play aims to achieve (e.g., quick shot, safe pass, isolation).
        4. Play breakdown: Provide a step-by-step breakdown of the play, highlighting key movements and actions.
        5. Summary: Summarize the play with the expected outcome and any contingency plans if the initial option is denied.

        Example:
        1. Inbounds play name - it should describe the set up (ex. stack, box, 4 across):
        2. General setup:
            - Player 1: Inbounding under the basket
            - Player 2: xx
            - Player 3: xx
            - Player 4: xx
            - Player 5: xx
        3. Main objective: Create an open 3-point shot for Player 3 in the corner.
        4. Play breakdown:
            - Step 1: Player 1 dribbles to the right wing.
            - Step 2: Player 5 sets a screen for Player 3.
            - Step 3: Player 3 moves to the corner for an open shot.
        5. Summary:
            - Player 1:
            - Player 2:
            - Player 3:
            - Player 4:
            - Player 5:
        """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are advising a basketball coach."},
                {"role": "user", "content": prompt_for_refinement}
            ],
            max_tokens=512
        )

        refined_play = response['choices'][0]['message']['content'].strip()
        return refined_play
    except Exception as e:
        print(f"Failed to refine the play: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test example
    players = "Ava Cohen, Liv Solomon, Nava Bousbib, Gaby Kalish, Liyora Marmar"
    defense = "3-2 Zone"

    # Generate play
    generated_play = generate_basketball_play(players, defense)
    print("Generated Play:")
    print_result_wrapped(generated_play)

    # Refine play based on a player's off night
    if generated_play:
        refined_play = refine_play(generated_play, "Liv Solomon")
        print("\nRefined Play:")
        print_result_wrapped(refined_play)

    # Generate inbound play
    inbound_play = generate_inbound_play(players, defense)
    print("\nInbounds Play:")
    print_result_wrapped(inbound_play)