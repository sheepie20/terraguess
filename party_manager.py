import random
import os
import json

async def create_party(host_username: str):
    party_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    if not os.path.exists(f"parties/"):
        os.mkdir("parties/")
    
    if os.path.exists(f"parties/{party_id}.json"):
        return await create_party()
    
    party_data = {
        "code": party_id,
        "status": "waiting",
        "host": host_username,
        "players": [host_username],
        "rounds": {
            "1": {
                "places": {},
                "location": [],
                "distances": {},
                "guesses": {}
            },
            "2": {
                "places": {},
                "location": [],
                "distances": {},
                "guesses": {}
            },
            "3": {
                "places": {},
                "location": [],
                "distances": {},
                "guesses": {}
            },
            "4": {
                "places": {},
                "location": [],
                "distances": {},
                "guesses": {}
            },
            "5": {
                "places": {},
                "location": [],
                "distances": {},
                "guesses": {}
            }
        },
        "current_round": 0,
        "time_created": str(os.path.getctime(f"parties/{party_id}.json"))
    }

    with open(f"parties/{party_id}.json", "w") as f:
        json.dump(party_data, f)

    return party_id

async def join_party(party_id: str, username: str):
    if not os.path.exists(f"parties/{party_id}.json"):
        return False, "Party does not exist."
    
    with open(f"parties/{party_id}.json", "r") as f:
        party_data = json.load(f)
    
    if username in party_data["players"]:
        return False, "Username already taken in this party."
    
    party_data["players"].append(username)

    with open(f"parties/{party_id}.json", "w") as f:
        json.dump(party_data, f)

    return True, "Joined party successfully."

async def kick_player(party_id: str, username: str):
    if not os.path.exists(f"parties/{party_id}.json"):
        return False, "Party does not exist."
    
    with open(f"parties/{party_id}.json", "r") as f:
        party_data = json.load(f)
    
    if username not in party_data["players"]:
        return False, "Player not found in this party."
    
    party_data["players"].remove(username)

    with open(f"parties/{party_id}.json", "w") as f:
        json.dump(party_data, f)

    return True, "Player kicked successfully."

async def start_game(party_id: str):
    if not os.path.exists(f"parties/{party_id}.json"):
        return False, "Party does not exist."
    
    with open(f"parties/{party_id}.json", "r") as f:
        party_data = json.load(f)
    
    if party_data["status"] != "waiting":
        return False, "Game already started or finished."
    
    party_data["status"] = "active"
    party_data["current_round"] = 1

    with open(f"parties/{party_id}.json", "w") as f:
        json.dump(party_data, f)

    return True, "Game started successfully."

async def update_round_data(party_id: str, round_number: int = None, places: dict = None, locations: dict = None, distances: dict = None):
    if not os.path.exists(f"parties/{party_id}.json"):
        return False, "Party does not exist."
    
    with open(f"parties/{party_id}.json", "r") as f:
        party_data = json.load(f)
    
    if round_number != party_data["current_round"]:
        return False, "Invalid round number."

    if places is not None:
        party_data["rounds"]["places"][str(round_number)] = places
    if locations is not None:
        party_data["rounds"]["locations"][str(round_number)] = locations
    if distances is not None:
        party_data["rounds"]["distances"][str(round_number)] = distances

    with open(f"parties/{party_id}.json", "w") as f:
        json.dump(party_data, f)

    return True, "Round data updated successfully."

async def end_game(party_id: str):
    if not os.path.exists(f"parties/{party_id}.json"):
        return False, "Party does not exist."
    
    with open(f"parties/{party_id}.json", "r") as f:
        party_data = json.load(f)
    
    if party_data["status"] != "active":
        return False, "Game is not active."
    
    party_data["status"] = "finished"

    with open(f"parties/{party_id}.json", "w") as f:
        json.dump(party_data, f)

    return True, "Game ended successfully."

async def get_party_data(party_id: str):
    if not os.path.exists(f"parties/{party_id}.json"):
        return None, "Party does not exist."
    
    with open(f"parties/{party_id}.json", "r") as f:
        party_data = json.load(f)
    
    return party_data, "Party data retrieved successfully."

async def delete_party(party_id: str):
    if not os.path.exists(f"parties/{party_id}.json"):
        return False, "Party does not exist."
    
    os.remove(f"parties/{party_id}.json")
    return True, "Party deleted successfully."

async def list_parties():
    if not os.path.exists("parties/"):
        return []
    
    parties = [f.split(".json")[0] for f in os.listdir("parties/") if f.endswith(".json")]
    return parties