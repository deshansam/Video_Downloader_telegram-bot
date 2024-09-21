from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_dl
import os

BOT_TOKEN = '7744572885:AAFrQBgz4CLmgXHJvvFr-Fh6YtZHiA9scH4'  # Your actual token

def start(update, context):
    update.message.reply_text("Send me a YouTube link, and I'll download the video for you.")

def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'noplaylist': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

def handle_message(update, context):
    message = update.message.text
    if 'youtube.com' in message or 'youtu.be' in message:
        update.message.reply_text("Downloading the video, please wait...")
        video_file = download_youtube_video(message)
        update.message.reply_text("Download complete. Sending the video...")
        context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_file, 'rb'))
        os.remove(video_file)  # Clean up
    else:
        update.message.reply_text("Please send a valid YouTube link.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
