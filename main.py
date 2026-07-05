import os
import requests
from dotenv import load_dotenv

#Enter API keys from footballdata.org in footballtoken and from newsapi.org in newskey
load_dotenv()
FOOTBALL_TOKEN = os.getenv("Footballdataapikey")
NEWS_KEY = os.getenv("Newsapikey")

def get_live_scores():
    print("\n⏳ Fetching live/recent matches...")
    url = "https://api.football-data.org/v4/matches"
    headers = { "X-Auth-Token": FOOTBALL_TOKEN }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = data.get("matches", [])
            if not matches:
                print("No matches scheduled for today.")
                return
                
            for match in matches[:10]:
                home_team = match["homeTeam"]["name"]
                away_team = match["awayTeam"]["name"]
                status = match["status"]
                home_score = match["score"]["fullTime"].get("home", 0)
                away_score = match["score"]["fullTime"].get("away", 0)
                
                if status == "LIVE" or status == "IN_PLAY":
                    print(f"🔴 LIVE: {home_team} {home_score} - {away_score} {away_team}")
                elif status == "FINISHED":
                    print(f"✅ FT: {home_team} {home_score} - {away_score} {away_team}")
                else:
                    print(f"📅 Upcoming: {home_team} vs {away_team} (Status: {status})")
        else:
            print("Failed to fetch live scores. Check your API key or limits.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_football_news(query):
    print(f"\n⏳ Fetching latest news for '{query}'...")
    # Clean up the search by combining the query with football tags to reduce unrelated noise
    search_query = f"{query} AND (football OR soccer OR transfer)"
    url = f"https://newsapi.org/v2/everything?q={search_query}&language=en&sortBy=publishedAt&apiKey={NEWS_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            if not articles:
                print("No relevant articles found for your search.")
                return
                
            for index, article in enumerate(articles[:5], 1):
                title = article["title"]
                source = article["source"]["name"]
                print(f"{index}. 📰 {title} (via {source})")
        else:
            print("Failed to fetch news. Check your API key.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- CONTINUOUS PROGRAM LOOP ---
while True:
    print("\n=============================================")
    print("⚽ Welcome to the Live Football Aggregator! ⚽")
    print("=============================================")
    print("1. View Real-Time Scores & Fixtures")
    print("2. General Football News & Rumors")
    print("3. Search News for a Club, Player, or Nation")
    print("4. ❌ Stop and Exit Aggregator")
    print("=============================================")
    
    choice = input("\nChoose an option (1-4): ")

    if choice == "1":
        get_live_scores()
    elif choice == "2":
        get_football_news("football transfer rumor")
    elif choice == "3":
        search_term = input("Enter team, player, or nation (e.g., Real Madrid / Ronaldo / Brazil): ")
        get_football_news(search_term)
    elif choice == "4":
        print("\nThank you for using the Football Aggregator! Goodbye! 👋⚽")
        break  # This breaks the loop and stops the program completely
    else:
        print("\n❌ Invalid option! Please type a number between 1 and 4.")