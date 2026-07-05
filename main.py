
import requests
import tkinter as tk
from tkinter import messagebox, ttk


# Put the API keys for the code to work. The API Keys could be found from football-data.org and newsapi.org

FOOTBALL_TOKEN = "FootballdataAPIKey"
NEWS_KEY = "Newsapikey"

# --- DATA FETCHING FUNCTIONS ---

def fetch_live_scores():
    """Fetches matches and displays them in the text area."""
    output_box.delete("1.0", tk.END)  # Clear old text
    output_box.insert(tk.END, "⏳ Fetching live/recent matches...\n\n")
    root.update()
    
    url = "https://api.football-data.org/v4/matches"
    headers = { "X-Auth-Token": FOOTBALL_TOKEN }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            output_box.delete("1.0", tk.END)
            data = response.json()
            matches = data.get("matches", [])
            
            if not matches:
                output_box.insert(tk.END, "📅 No matches scheduled for today.")
                return
                
            for match in matches[:15]:
                home_team = match["homeTeam"]["name"]
                away_team = match["awayTeam"]["name"]
                status = match["status"]
                home_score = match["score"]["fullTime"].get("home", 0)
                away_score = match["score"]["fullTime"].get("away", 0)
                
                if status in ["LIVE", "IN_PLAY"]:
                    output_box.insert(tk.END, f"🔴 LIVE | {home_team} {home_score} - {away_score} {away_team}\n")
                elif status == "FINISHED":
                    output_box.insert(tk.END, f"✅ FT   | {home_team} {home_score} - {away_score} {away_team}\n")
                else:
                    output_box.insert(tk.END, f"📅 Scheduled | {home_team} vs {away_team} ({status})\n")
        else:
            output_box.insert(tk.END, f"❌ Failed to fetch live scores. HTTP Status: {response.status_code}")
    except Exception as e:
        output_box.insert(tk.END, f"⚠️ Connection error occurred: {e}")

def fetch_news(query):
    """Fetches football news based on a specific query keyword."""
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, f"⏳ Searching news database for '{query}'...\n\n")
    root.update()
    
    search_query = f"{query} AND (football OR soccer OR transfer)"
    url = f"https://newsapi.org/v2/everything?q={search_query}&language=en&sortBy=publishedAt&apiKey={NEWS_KEY}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            output_box.delete("1.0", tk.END)
            data = response.json()
            articles = data.get("articles", [])
            
            if not articles:
                output_box.insert(tk.END, "❌ No news articles found matching that term.")
                return
                
            for index, article in enumerate(articles[:8], 1):
                title = article["title"]
                source = article["source"]["name"]
                output_box.insert(tk.END, f"{index}. 📰 {title}\n   Source: {source}\n\n")
        else:
            output_box.insert(tk.END, f"❌ Failed to fetch news.\nStatus Code: {response.status_code}\nDetails: {response.text}")
    except Exception as e:
        output_box.insert(tk.END, f"⚠️ Connection error occurred: {e}")

def handle_search():
    """Triggers the custom search field execution."""
    search_term = search_entry.get().strip()
    if not search_term:
        messagebox.showwarning("Input Error", "Please type a player, team, or nation first!")
        return
    fetch_news(search_term)


# --- GUI WINDOW BUILDER ---

root = tk.Tk()
root.title("Football News Aggregator")
root.geometry("700x550")
root.configure(bg="#1e1e2e") # Modern dark-themed dashboard background

# 1. Dashboard Title Header
header_label = tk.Label(root, text="⚽ Football Fan Dashboard", font=("Arial", 18, "bold"), fg="#ffffff", bg="#1e1e2e")
header_label.pack(pady=15)

# 2. Top Button Bar for Primary Options
button_frame = tk.Frame(root, bg="#1e1e2e")
button_frame.pack(pady=5)

live_btn = tk.Button(button_frame, text="🔴 Live Scores & Fixtures", font=("Arial", 11, "bold"), bg="#ff5555", fg="white", padx=10, command=fetch_live_scores)
live_btn.pack(side=tk.LEFT, padx=10)

news_btn = tk.Button(button_frame, text="📰 Top Rumors & Transfers", font=("Arial", 11, "bold"), bg="#8be9fd", fg="black", padx=10, command=lambda: fetch_news("football transfer rumor"))
news_btn.pack(side=tk.LEFT, padx=10)

# 3. Custom Search Frame (For specific Player/Club/Nation queries)
search_frame = tk.Frame(root, bg="#1e1e2e")
search_frame.pack(pady=15)

search_label = tk.Label(search_frame, text="Search Team/Player/Nation:", font=("Arial", 10), fg="#ffffff", bg="#1e1e2e")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, font=("Arial", 11), width=25)
search_entry.pack(side=tk.LEFT, padx=5)

search_btn = tk.Button(search_frame, text="🔍 Search", font=("Arial", 10, "bold"), bg="#50fa7b", fg="black", command=handle_search)
search_btn.pack(side=tk.LEFT, padx=5)

# 4. Content Frame (Scrollable display where text loads)
content_frame = tk.Frame(root)
content_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Add a text scrolling widget for easy reading
output_box = tk.Text(content_frame, font=("Consolas", 11), wrap=tk.WORD, bg="#282a36", fg="#f8f8f2", bd=0, padx=10, pady=10)
scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=output_box.yview)
output_box.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Initial default message in the display window
output_box.insert(tk.END, "Welcome! Click one of the options above or run a search query to load real-time football data.")

# Run the GUI application
root.mainloop()