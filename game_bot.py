import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, render_template_string

# إعدادات التطبيق
app = Flask(__name__)
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'default_token')
AUTHORIZED_USERS = [int(x) for x in os.environ.get('AUTHORIZED_USERS', '').split(',') if x]

# إعداد التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# صفحة ويب أساسية
@app.route('/')
def home():
    return render_template_string('''
        <h1>🎮 بوت تحكم لعبة أندرويد</h1>
        <p>البوت يعمل بنجاح على Heroku!</p>
        <p>استخدم Telegram للتحكم في اللعبة.</p>
    ''')

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if AUTHORIZED_USERS and user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("❌ غير مصرح لك باستخدام هذا البوت.")
        return
        
    keyboard = [
        ['⚔ هجوم', '🛡 دفاع'],
        ['🏃 حركة', '🎯 جمع'],
        ['📊 الحالة', '🔄 تحديث']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text('🎮 بوت التحكم في اللعبة جاهز! اختر أمراً:', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if AUTHORIZED_USERS and user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("❌ غير مصرح لك باستخدام هذا البوت.")
        return
        
    text = update.message.text
    
    if text == '⚔ هجوم':
        await update.message.reply_text("✅ تم الهجوم!")
        
    elif text == '🛡 دفاع':
        await update.message.reply_text("✅ تم الدفاع!")
        
    elif text == '🏃 حركة':
        await update.message.reply_text("✅ تمت الحركة!")
        
    elif text == '🎯 جمع':
        await update.message.reply_text("✅ تم الجمع!")
        
    elif text == '📊 الحالة':
        await update.message.reply_text("🟢 البوت يعمل بشكل طبيعي")
        
    elif text == '🔄 تحديث':
        await update.message.reply_text("🔄 تم التحديث!")

def main():
    # تشغيل Flask في الخلفية
    from threading import Thread
    port = int(os.environ.get('PORT', 5000))
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False))
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