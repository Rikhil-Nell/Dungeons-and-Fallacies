from agents import yapper_agent, kevin_and_karen_agent, cynic_agent, nietzsche_agent

PLAYER_STARTING_HEALTH = 10

MOBS_DATA = [
    {
        "name": "Yapper",
        "agent": yapper_agent,
        "health": 5,
        "special": "interrupt",
        "personality": "A non-stop talker who constantly interrupts and distracts with irrelevant chatter."
    },
    {
        "name": "Karen & Kevin",
        "agent": kevin_and_karen_agent,
        "health": 8,
        "special": "affirm",
        "personality": "A self-affirming duo who constantly agree with each other, reinforcing their own points regardless of validity."
    },
    {
        "name": "Cynic",
        "agent": cynic_agent,
        "health": 10,
        "special": "life_steal",
        "special_state": {"consecutive_wins": 0},
        "personality": "A pessimistic and draining individual who thrives on despair and negativity, seeking to undermine the player's resolve."
    },
    {
        "name": "Nietzsche (Boss)",
        "agent": nietzsche_agent,
        "health": 15,
        "special": "kill_or_get_killed",
        "special_state": {"turns_left": 0, "active": False},
        "personality": "A nihilistic philosopher focused on power, struggle, and the will to overcome. Arguments are a battlefield."
    }
]