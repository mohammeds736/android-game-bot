import os
import logging
import sys

# إصلاح مشكلة imghdr في Python 3.13
try:
    import imghdr
except ImportError:
    # إنشاء بديل بسيط لـ imghdr
    import struct
    
    def imghdr_what(file):
        with open(file, 'rb') as f:
            header = f.read(12)
        if header.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'png'
        elif header.startswith(b'\xff\xd8\xff'):
            return 'jpeg'
        elif header.startswith(b'GIF87a') or header.startswith(b'GIF89a'):
            return 'gif'
        elif header.startswith(b'BM'):
            return 'bmp'
        return None
    
    # إضافة الوظيفة إلى sys.modules
    class ImghdrModule:
        what = staticmethod(imghdr_what)
    
    sys.modules['imghdr'] = ImghdrModule()
    import imghdr

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask
import threading

# إعدادات التطبيق
app = Flask(__name__)
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'default_token')
PORT = int(os.environ.get('PORT', 10000))

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# صفحة ويب أساسية
@app.route('/')
def home():
    return "🎮 بوت تحكم لعبة أندرويد يعمل بنجاح! استخدم Telegram للتحكم."

# أوامر البوت
def start(update: Update, context: CallbackContext):
    keyboard = [['⚔ هجوم', '🛡 دفاع'], ['🏃 حركة', '🎯 جمع']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('🎮 بوت التحكم في اللعبة جاهز!', reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    
    if text == '⚔ هجوم':
        update.message.reply_text("✅ تم الهجوم!")
    elif text == '🛡 دفاع':
        update.message.reply_text("✅ تم الدفاع!")
    elif text == '🏃 حركة':
        update.message.reply_text("✅ تمت الحركة!")
    elif text == '🎯 جمع':
        update.message.reply_text("✅ تم الجمع!")

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

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
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        
        logger.info("✅ البوت يعمل...")
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        logger.error(f"❌ فشل تشغيل البوت: {e}")

if __name__ == "__main__":
    main()