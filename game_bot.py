import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, render_template_string
import threading

# إعدادات التطبيق
app = Flask(__name__)
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'default_token')
PORT = int(os.environ.get('PORT', 5000))

# إعداد التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# صفحة ويب أساسية
@app.route('/')
def home():
    return "🎮 بوت تحكم لعبة أندرويد يعمل بنجاح! استخدم Telegram للتحكم."

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):        
    keyboard = [['⚔ هجوم', '🛡 دفاع'], ['🏃 حركة', '🎯 جمع']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('🎮 بوت التحكم في اللعبة جاهز!', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == '⚔ هجوم':
        await update.message.reply_text("✅ تم الهجوم!")
    elif text == '🛡 دفاع':
        await update.message.reply_text("✅ تم الدفاع!")
    elif text == '🏃 حركة':
        await update.message.reply_text("✅ تمت الحركة!")
    elif text == '🎯 جمع':
        await update.message.reply_text("✅ تم الجمع!")

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False)

def main():
    # تشغيل Flask في الخلفية
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # تشغيل بوت Telegram
    if BOT_TOKEN == "default_token":
        logger.error("❌ لم يتم تعيين توكن البوت")
        return
        
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("✅ البوت يعمل...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"❌ فشل تشغيل البوت: {e}")

if __name__ == "__main__":
    main()
