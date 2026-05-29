from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import yt_dlp
import os

TOKEN = "8604112617:AAFzOdCVwFRBIgeNN7POscrRaN-HJKpTghU"

async def baixar_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("Baixando vídeo...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best[height<=480]'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            arquivo = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(arquivo, 'rb'))

        os.remove(arquivo)

    except Exception as e:
        await update.message.reply_text(f"Erro: {e}")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, baixar_video))

print("Bot online...")

app.run_polling()