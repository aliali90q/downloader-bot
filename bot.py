import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = '8673459656:AAGgr5lgxFQXN8d92kN-6zmVM3IX0Wncm7Y'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً إبراهيم! أرسل لي رابط فيديو وسأحمله لك فوراً 📥")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" in url:
        msg = await update.message.reply_text("⏳ جاري التحميل... انتظر قليلاً")
        
        # إعدادات التحميل
        ydl_opts = {'outtmpl': 'video.mp4', 'quiet': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # إرسال الفيديو للمستخدم
            await update.message.reply_video(video=open('video.mp4', 'rb'))
            await msg.delete()
            os.remove('video.mp4') # حذف الملف من الحاسبة بعد الإرسال
        except Exception as e:
            await update.message.reply_text(f"حدث خطأ أثناء التحميل: {e}")
    else:
        await update.message.reply_text("يرجى إرسال رابط صحيح.")

if __name__ == "__main__":
    print("البوت يعمل الآن... جربه!")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()