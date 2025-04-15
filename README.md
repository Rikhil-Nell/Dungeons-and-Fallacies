# Dungeons & Fallacies

A text-based RPG where logic is your weapon and fallacies are your foes. Developed for a hackathon.

## Overview

Dungeons & Fallacies flips the script on traditional RPG combat. Instead of swords and spells, players navigate encounters armed with well-reasoned arguments. Face off against unique mobs, each embodying a specific personality or flawed reasoning style. Your goal is to dismantle their arguments and expose their fallacies before your own resolve (health) runs out. The game utilizes AI agents powered by `pydantic-ai` and large language models (specifically Cerebras Llama 3.3 70B via API in this implementation) to drive mob responses and judge the debates.

## Core Gameplay

* **Argumentation Combat:** Engage in turn-based debates. Mobs present arguments or challenges based on their personality.
* **Counter Arguments:** The player's primary action is to formulate and present counter-arguments.
* **Null vs. Alternative Hypothesis:** Each round's exchange is framed as the player's "Alternative Hypothesis" challenging the mob's stance or last point (the "Null Hypothesis").
* **AI Judge:** A neutral AI agent evaluates the effectiveness of the player's counter within the context of the debate, deciding the winner of the exchange based on logic and relevance.
* **Health System:** Winning an argument damages the opponent's resolve (health), while losing an exchange depletes the player's health. The first to reach zero loses.

## Mobs & Mechanics

Players will encounter the following adversaries:

1.  **Yapper:**
    * *Personality:* Non-stop talker who interrupts constantly.
    * *Mechanic (Interrupting Babble):* Delays the player's action phase with irrelevant chatter.
2.  **Karen & Kevin:**
    * *Personality:* Self-affirming duo who always agree with each other.
    * *Mechanic (Self-Affirmation):* Heal 1 heart each turn by agreeing with each other.
3.  **Cynic:**
    * *Personality:* Pessimistic and draining, thrives on despair.
    * *Mechanic (Life Steal):* If the Cynic wins 2 argument rounds consecutively, they drain 1 heart from the player and heal themselves.
4.  **Nietzsche (Boss):**
    * *Personality:* Nihilistic philosopher focused on power and struggle.
    * *Mechanic (Kill or Get Killed):* A high-risk, timed ability where Nietzsche either gains health or suffers significant health loss based on whether they win or lose the argument exchange during the active period.

## Technology Stack

* **Language:** Python 3.x
* **Core Logic:** Standard Python libraries
* **AI Agents:** `pydantic-ai` library
* **LLM Backend:** Cerebras Llama 3.3 70B (via OpenAI-compatible API)
* **User Interface:** Terminal-based (`print`/`input`)
* **Package Management:** `uv`
* **API Client:** `openai` library (for interacting with Cerebras endpoint)

## Project Structure

The project is organized into several files for clarity:

```.
├── main.py             # Main entry point to run the game
├── game_logic.py       # Contains the core game loop and turn logic
├── agents.py           # AI agent setup, model definitions, Pydantic schemas
├── config.py           # Game configuration (player health, mob data)
├── utils.py            # Utility functions (clear screen, display status)
├── prompts/            # Directory containing .txt files for agent system prompts
│   ├── judge_agent_prompt.txt
│   ├── yapper_agent_prompt.txt
│   ├── ... (other mob prompts)
├── requirements.txt    # Python package dependencies (or pyproject.toml)
└── README.md           # This file
```

## Setup and Running (Using uv)

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```
2.  **Install `uv`:**
    If you don't have `uv` installed, you can install it using one of the following methods (see [official uv installation guide](https://github.com/astral-sh/uv#installation) for more options):

    * **macOS / Linux:**
        ```bash
        curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
        ```
    * **Windows (via pip):**
        ```bash
        pip install uv
        ```
    * *(Or use `pipx install uv`)*

3.  **Create Virtual Environment & Install Dependencies:**
    Ensure you have your dependency file ready (e.g., `requirements.txt` or `pyproject.toml`). Then run:
    ```bash
    # Create and activate a virtual environment (recommended)
    uv venv

    # Source the environment (syntax varies by shell)
    # Linux/macOS (bash/zsh):
    source .venv/bin/activate
    # Windows (cmd):
    # .venv\Scripts\activate.bat
    # Windows (PowerShell):
    # .venv\Scripts\Activate.ps1

    # Sync dependencies from requirements.txt (or pyproject.toml)
    uv sync
    ```
    This command creates the environment (if needed) and installs the exact locked dependencies, similar to `pip install -r requirements.txt` but generally faster.

4.  **API Keys:**
    This project requires API access to the Cerebras LLM endpoint. Set up your API key and base URL. It's recommended to use environment variables (e.g., via a `.env` file and the `python-dotenv` library) rather than hardcoding keys. Update `agents.py` or a `settings.py` file accordingly to load these credentials. (You might need to add `python-dotenv` to your `requirements.txt` if using `.env` files).

5.  **Prompt Files:**
    Ensure the `.txt` files defining the system prompts for each agent exist within the `prompts/` directory.

6.  **Run the Game:**
    With your virtual environment activated, run:
    ```bash
    python main.py
    ```

## Future Ideas

* **Visible Input Timer:** Implement a visual countdown timer for player input using libraries like `prompt_toolkit` or Textual, or by migrating to a web UI.
* **Enhanced UI:** Utilize a TUI framework like Textual for a richer terminal experience, or develop a full web-based UI using JavaScript.
* **More Mobs/Content:** Add more fallacies, arguments, and perhaps items or player skills.
* **Refined Judging:** Further improve the AI Judge's prompts and evaluation criteria.
* **Difficulty Levels:** Implement varying mob health or argument strength.

## Hackathon Context

This project was developed during the Cerebras Llama 4 hackathon.
