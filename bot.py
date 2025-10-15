import os
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# লগিং চালু করুন
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- অনুগ্রহ করে এই অংশগুলো পরিবর্তন করুন ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_FALLBACK_TOKEN")
WEB_APP_URL = "https://onlinetakaincome.vercel.app/"
# ------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    final_url = WEB_APP_URL
    
    if context.args:
        referral_code = context.args[0]
        final_url += f"?ref={referral_code}"
        logger.info(f"User {user.id} started with ref code: {referral_code}")

    keyboard = [[InlineKeyboardButton("🚀 Open App & Start Earning!", web_app=WebAppInfo(url=final_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! 👋 Welcome to Daily Earn Money Pro.",
        reply_markup=reply_markup,
    )

async def handle_update(update_data):
    """ gelen güncellemeyi işler """
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    update = Update.de_json(update_data, application.bot)
    await application.process_update(update)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update_data = json.loads(post_data.decode('utf-8'))
            
            import asyncio
            asyncio.run(handle_update(update_data))

            self.send_response(200)
            self.end_headers()
        except Exception as e:
            logger.error(f"Error handling POST request: {e}")
            self.send_response(500)
            self.end_headers()
