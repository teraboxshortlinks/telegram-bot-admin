import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# লগিং চালু করুন (সমস্যা সমাধানের জন্য)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- অনুগ্রহ করে এই অংশগুলো পরিবর্তন করুন ---
# BotFather থেকে পাওয়া আপনার টেলিগ্রাম বটের টোকেনটি এখানে বসান
BOT_TOKEN = "YOUR_BOT_TOKEN" 
# আপনার মিনি অ্যাপের (ওয়েবসাইট) URL
WEB_APP_URL = "https://fb-erning-bot.vercel.app/" 
# ------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start কমান্ডের উত্তর দেয়। এটি রেফারেল কোডসহ বা কোড ছাড়া কাজ করে।
    """
    user = update.effective_user
    final_url = WEB_APP_URL
    
    # context.args থেকে রেফারেল কোডটি (payload) গ্রহণ করুন
    if context.args:
        referral_code = context.args[0]
        # URL-এর শেষে রেফারেল কোডটি ?ref= پارامیটার হিসেবে যোগ করুন
        final_url += f"?ref={referral_code}"
        logger.info(f"User {user.id} started with referral code: {referral_code}. Final URL: {final_url}")
    else:
        logger.info(f"User {user.id} started without a referral code. Final URL: {final_url}")

    # একটি বাটন তৈরি করুন যা আপনার মিনি অ্যাপটি খুলবে
    keyboard = [
        [InlineKeyboardButton("🚀 Open App & Start Earning!", web_app=WebAppInfo(url=final_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ব্যবহারকারীকে স্বাগত বার্তা এবং বাটনটি পাঠান
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! 👋"
        "\n\nWelcome to Daily Earn Money Pro. Click the button below to open the app and start earning!",
        reply_markup=reply_markup,
    )

def main() -> None:
    """বটটি চালু করে।"""
    # Application তৈরি করুন এবং আপনার বটের টোকেন দিন
    application = Application.builder().token(BOT_TOKEN).build()

    # /start কমান্ডের জন্য একটি হ্যান্ডলার যোগ করুন
    application.add_handler(CommandHandler("start", start))

    # বটটি চালু করুন এবং নতুন বার্তা গ্রহণ করার জন্য প্রস্তুত থাকুন
    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
```

---
