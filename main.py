import os, requests, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")
BALL_KEY = os.environ.get("BALLDONTLIE_KEY")

app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot SavNbaProno en ligne !"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏀 Bienvenue sur SavNbaProno !\n\nTape /over pour les pronos OVER.\nTape /matchs pour les matchs.")

async def matchs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    headers = {"Authorization": BALL_KEY}
    try:
        r = requests.get("https://api.balldontlie.io/nba/v1/games?dates[]=2026-11-13&per_page=25", headers=headers, timeout=10)
        data = r.json().get("data", [])
        if not data:
            await update.message.reply_text("Pas de matchs aujourd'hui.")
            return
        txt = "🏀 MATCHS DU JOUR :\n\n"
        for g in data:
            txt += f"{g['home_team']['abbreviation']} vs {g['visitor_team']['abbreviation']} - {g['status']}\n"
        await update.message.reply_text(txt)
    except:
        await update.message.reply_text("Erreur API, reessaie.")

async def over(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 PRONO OVER DU JOUR :\n\nAnalyse en cours...\nUtilise /matchs pour voir les matchs.")

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("matchs", matchs))
    app.add_handler(CommandHandler("over", over))
    print("Bot lance...")
    app.run_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
