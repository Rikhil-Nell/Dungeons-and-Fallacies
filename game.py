# game_logic.py
import time

# Import necessary components from other files
# Assuming ArgumentOutcome is defined in and imported from agents.py
from agents import judge_agent, ArgumentOutcome
from config import PLAYER_STARTING_HEALTH, MOBS_DATA
from utils import clear_screen, display_status
# Note: Individual mob agents are accessed via config.MOBS_DATA, no direct import needed here

def play_game():
    """Runs the main game loop for Dungeons and Fallacies."""
    player_health = PLAYER_STARTING_HEALTH

    print("Welcome to Dungeons and Fallacies!")
    print("Prepare to argue your way through!")
    input("Press Enter to start...")

    for mob_config in MOBS_DATA:
        clear_screen()
        mob_name = mob_config['name']
        print(f"\n*** Encounter: {mob_name} ***\n")

        # --- Encounter Setup ---
        mob_health = mob_config['health']
        mob_agent = mob_config['agent'] # Get the agent instance from config
        mob_special = mob_config.get('special')
        # Use .copy() for special_state to avoid altering the original MOBS_DATA dict
        mob_special_state = mob_config.get('special_state', {}).copy()
        mob_personality = mob_config.get('personality', 'A generic argumentative opponent.')
        encounter_history = []
        mob_last_statement = "" # Variable to hold the mob's most recent argument

        # --- Mob Delivers Opening Statement ---
        print(f"{mob_name} steps forward, preparing to argue...")
        opening_user_prompt = f"You are {mob_name}. Your personality is: {mob_personality}. State your core belief or pose a challenging opening question/argument to the player based on your personality."
        try:
            opening_response = mob_agent.run_sync(user_prompt=opening_user_prompt)
            mob_opening_statement = opening_response.data
            print(f"{mob_name}: {mob_opening_statement}")
            encounter_history.append(f"{mob_name} (Opening): {mob_opening_statement}")
            mob_last_statement = mob_opening_statement # Store this as the first thing player counters
        except Exception as e:
            print(f"An error occurred generating opening for {mob_name}: {e}")
            mob_opening_statement = "Let's just get this over with." # Fallback
            print(f"{mob_name}: {mob_opening_statement}")
            encounter_history.append(f"{mob_name} (Opening): {mob_opening_statement}")
            mob_last_statement = mob_opening_statement

        # --- Encounter Loop ---
        turn = 1
        player_argument = "" # Initialize

        while player_health > 0 and mob_health > 0:
            # Display status at the start of the round
            display_status(player_health, mob_name, mob_health)
            print(f"\n--- Round {turn} ---")

            # 1. PLAYER ACTS (Countering Mob's Last Statement)
            # Adjust user_prompt based on whether it's the first turn or not
            if turn == 1:
                user_prompt_text = f"Your counter to '{mob_last_statement}': "
            else:
                # Truncate mob_last_statement if too long for user_prompt display
                user_prompt_context = (mob_last_statement[:60] + '...') if len(mob_last_statement) > 60 else mob_last_statement
                user_prompt_text = f"Your counter to '{user_prompt_context}': "

            print(f"\n{mob_name}'s current stance to counter: \"{mob_last_statement}\"") # Remind player
            player_argument = input(user_prompt_text)

            if not player_argument:
                player_argument = "[Player offers no counter]" # Handle silence
                print("You offer no counter this round.")

            encounter_history.append(f"Player (R{turn}): {player_argument}")

            # --- Yapper Mechanic ---
            # If Yapper, interrupt before the Mob thinks/responds
            if mob_special == "interrupt":
                 print(f"\n{mob_name} interrupts before responding...")
                 try:
                     babble_response = mob_agent.run_sync(user_prompt="Say something brief, distracting, and irrelevant before giving your real response.")
                     print(f"{mob_name} (Interrupting): {babble_response.data}")
                 except Exception as e:
                     print(f"{mob_name} (Interrupting): Wait, what was I saying? Oh, right...")
                     # print(f"(Agent error: {e})") # Optional debug
                 time.sleep(2) # Simulate delay caused by interruption

            # 2. MOB ACTS (Countering Player's Last Statement)
            print(f"\n{mob_name} considers your counter...")
            time.sleep(1) # Thematic pause

            # Apply Mob pre-argument effects: K&K Heal, Nietzsche Check
            if mob_special == "affirm":
                print(f"{mob_name}: 'Right!' 'Couldn't agree more!' (They seem pleased)")
                heal_amount = 1
                # Optional: Cap health at initial value
                # current_max_health = mob_config['health']
                # mob_health = min(mob_health + heal_amount, current_max_health)
                mob_health += heal_amount # Apply heal
                print(f"{mob_name} heals {heal_amount} heart.")
                # Display updated status immediately after heal? Optional.
                # display_status(player_health, mob_name, mob_health)

            if mob_special == "kill_or_get_killed" and not mob_special_state.get('active', False):
                 # Example trigger: activate every 3 turns if not already active
                 if turn > 1 and turn % 3 == 1: # Activate on turn 4, 7, 10 etc.
                     print(f"\n{mob_name}'s eyes narrow: 'Only the strongest viewpoint survives this!'")
                     mob_special_state['active'] = True
                     mob_special_state['turns_left'] = 2 # Effect lasts 2 rounds
                     print("(Nietzsche's Kill or Get Killed ability activates for 2 rounds!)")


            # Mob generates its counter-argument
            mob_context = (
                f"You are {mob_name}. Your personality is: {mob_personality}.\n"
                f"Your opening statement was: '{mob_opening_statement}'\n"
                f"Conversation History (most recent first):\n{''.join(encounter_history[-6:])}\n"
                f"The Player just countered your last point ('{mob_last_statement}') with: '{player_argument}'\n"
                f"Generate your counter-argument to the Player's statement, staying true to your personality and reinforcing your stance."
            )

            mob_argument_text = "...struggles to respond." # Default fallback
            try:
                mob_response_obj = mob_agent.run_sync(user_prompt=mob_context)
                mob_argument_text = mob_response_obj.data
                print(f"{mob_name}: {mob_argument_text}")
                encounter_history.append(f"{mob_name} (R{turn}): {mob_argument_text}")
                mob_last_statement = mob_argument_text # Update mob's last statement for next round
            except Exception as e:
                print(f"An error occurred with the {mob_name} Agent: {e}")
                print(f"{mob_name}: {mob_argument_text}") # Print fallback
                encounter_history.append(f"{mob_name} (R{turn}): {mob_argument_text}")
                mob_last_statement = mob_argument_text # Update with fallback

            # 3. JUDGE EVALUATES & RESOLVES ROUND
            print("\nThe Judge weighs the arguments for Round {turn}...")
            time.sleep(1)

            # Define the Null Hypothesis (Mob's position) and Alternative (Player's counter) for the judge
            # Mob's previous point is implicitly the Null being defended/elaborated on
            # Player's argument is the Alternative challenging it
            # Mob's latest response is their defense/counter to the Alternative
            judge_context = (
                f"You are the impartial Judge. Player is fighting {mob_name}.\n"
                f"Mob's Opening Stance: '{mob_opening_statement}'\n"
                f"Conversation History (most recent first):\n{''.join(encounter_history[-7:])}\n"
                f"\n--- Round {turn} Exchange ---"
                # Identifying the core points exchanged this round:
                f"\nPlayer's Counter/Alternative Hypothesis: '{player_argument}'"
                f"\nMob's Response/Null Hypothesis Defense: '{mob_argument_text}'"
                f"\n(Context: These arguments followed the mob's previous point: '{encounter_history[-3]}')" # Show what player countered
                f"\n--- End Exchange ---"
                f"\nEvaluate this specific exchange. Did the Player's Alternative Hypothesis ('{player_argument}') effectively challenge or refute the point defended by the Mob's Response ('{mob_argument_text}')? "
                f"Consider logic, relevance, and strength within the context of the overall debate and personalities. "
                f"Who argued more effectively in this specific player-vs-mob exchange? "
                f"Assign 1 heart damage to the loser (whose hypothesis/argument was weaker this round). State who won ('player' or 'enemy') and provide brief reasoning based on the hypothesis evaluation."
             )

            round_winner = "neutral" # Default if judge fails or ties
            nietzsche_effect = 0 # Reset Nietzsche effect calculation for this round
            try:
                judge_response = judge_agent.run_sync(user_prompt=judge_context)
                outcome: ArgumentOutcome = judge_response.data

                print(f"Judge: {outcome.reasoning}")
                round_winner = outcome.winner # Store winner for effects

                # Apply Argument Damage based on Judge's decision
                if outcome.winner == 'player':
                    damage = outcome.damage_to_enemy # Should be 1 based on user_prompt
                    print(f"Player wins the exchange! {mob_name} loses {damage} heart.")
                    mob_health -= damage
                elif outcome.winner == 'enemy':
                    damage = outcome.damage_to_player # Should be 1 based on user_prompt
                    print(f"{mob_name} wins the exchange! Player loses {damage} heart.")
                    player_health -= damage
                else:
                     print("The exchange yields no clear winner; no damage from arguments.")

                # --- Resolve Special Effects Based on Judge Outcome ---

                # Nietzsche Power Dynamics Resolution (If active)
                if mob_special == "kill_or_get_killed" and mob_special_state.get('active', False):
                    print("(Kill or Get Killed is active!)")
                    if round_winner == 'enemy': # Nietzsche won the exchange
                        print(f"{mob_name} draws strength from winning the struggle!")
                        nietzsche_effect = 1 # Gain 1 heart
                    else: # Nietzsche lost or tied the exchange
                        print(f"{mob_name} falters from losing the struggle!")
                        nietzsche_effect = -2 # Lose 2 hearts

                    # Apply Nietzsche effect immediately
                    if nietzsche_effect != 0:
                        print(f"Nietzsche Effect: Gains {nietzsche_effect} heart(s).")
                        mob_health += nietzsche_effect
                        # Ensure health doesn't go below 1 from this effect? Optional rule.
                        # mob_health = max(1, mob_health)

                    # Manage duration
                    mob_special_state['turns_left'] -= 1
                    if mob_special_state['turns_left'] <= 0:
                        mob_special_state['active'] = False
                        print(f"(Nietzsche's Kill or Get Killed ability fades.)")
                    else:
                        print(f"(Kill or Get Killed active for {mob_special_state['turns_left']} more round(s).)")


                # Track Cynic's consecutive wins (based on round_winner)
                if mob_special == "life_steal":
                    if round_winner == 'enemy':
                        # Increment win streak
                        mob_special_state['consecutive_wins'] = mob_special_state.get('consecutive_wins', 0) + 1
                        print(f"({mob_name} has now won {mob_special_state['consecutive_wins']} round(s) in a row.)")
                        # Check for Life Steal trigger
                        if mob_special_state['consecutive_wins'] >= 2:
                             print(f"\n{mob_name}'s cynicism intensifies after winning {mob_special_state['consecutive_wins']} consecutive rounds!")
                             drain_amount = 1
                             print(f"{mob_name} drains {drain_amount} heart from you!")
                             player_health -= drain_amount
                             mob_health += drain_amount
                             print(f"You lose {drain_amount} heart, {mob_name} gains {drain_amount} heart.")
                             mob_special_state['consecutive_wins'] = 0 # Reset streak after triggering
                             print("(Cynic's win streak reset.)")
                    else: # Player won or tie (neutral)
                        # Reset win streak if it was > 0
                        if mob_special_state.get('consecutive_wins', 0) > 0:
                             print(f"({mob_name}'s win streak is broken.)")
                             mob_special_state['consecutive_wins'] = 0

            except Exception as e:
                print(f"An error occurred with the Judge Agent: {e}")
                print("The Judge is undecided on this round's outcome.")


            # 4. END ROUND CHECKS (After all damage and effects)
            if mob_health <= 0:
                 display_status(player_health, mob_name, mob_health) # Show final zero health
                 print(f"\nYou have successfully argued {mob_name} into silence!")
                 break # Exit encounter loop
            if player_health <= 0:
                 display_status(player_health, mob_name, mob_health) # Show final zero health
                 print("\nYour logical resolve has failed. You collapse under the weight of fallacies.")
                 break # Exit encounter loop

            # Prepare for next round
            input("\nPress Enter to continue to the next round...")
            clear_screen()
            turn += 1
            # --- End Encounter While Loop ---

        # --- Post-Encounter Logic ---
        # Check if loop exited due to player death
        if player_health <= 0:
            print("\n--- GAME OVER ---")
            # Optional: Show final score, history, etc.
            return # Exit play_game function

        # Otherwise, player won the encounter
        print(f"\nYou have defeated {mob_name}! Take a moment to gather your thoughts.")
        # Optional: player_health += 1 # Small heal between fights?
        input("Press Enter to proceed deeper into the dungeon...")
        # Loop continues to the next mob in MOBS_DATA

    # --- End Game ---
    # If the loop finishes and player health is > 0, the player wins the game
    if player_health > 0:
        clear_screen()
        print("\n*******************************************")
        print(" ✨ Congratulations! ✨ ")
        print("You have masterfully navigated the Dungeon of Fallacies!")
        print("Your logic and reason have prevailed!")
        print("*******************************************")

# Note: This file assumes it will be called by main.py,
# so it doesn't need the `if __name__ == "__main__":` block here.