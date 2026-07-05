import json

# Load our football data
with open("data.json", "r") as file:
    data = json.load(file)

print("⚽ Welcome to the Ultimate Football Aggregator! ⚽")
print("1. Live Scores\n2. News & Rumors\n3. Club Info")

choice = input("Choose an option (1-3): ")

if choice == "1":
    for match in data["live_scores"]:
        print(f"🔴 {match['home']} {match['score']} {match['away']} ({match['status']})")
elif choice == "2":
    for item in data["news"]:
        print(f"📰 [{item['type'].upper()}] {item['title']}")
elif choice == "3":
    club_name = input("Enter club name (e.g., Arsenal): ")
    if club_name in data["clubs"]:
        info = data["clubs"][club_name]
        print(f"🏟️ Stadium: {info['stadium']} | 👔 Manager: {info['manager']}")
    else:
        print("Club not found in our system yet!")