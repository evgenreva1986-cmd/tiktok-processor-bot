import telebot
import yt_dlp
import asyncio
import os
from telebot import types
from telebot import apihelper
from shazamio import Shazam
from dotenv import load_dotenv

apihelper.CONNECT_TIMEOUT = 90
apihelper.READ_TIMEOUT = 90

load_dotenv()
TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(TOKEN)
shazam = Shazam()

async def find_song_info(filename):
    try:
        output = await shazam.recognize(filename)
        track = output.get("track")
        if track:
            main_info = f"name and author: <code>{track.get('share', {}).get('subject')}</code>\n<a href='{track.get('url')}'>More info</a>"
            if main_info:
                print(main_info)
                return main_info
            else: 
                return "Not found track info"
        else:
            return "<b><i>Not found track info</i></b>(\nmaybe video sound not even a music or it is very specific remix"
    except Exception as e:
        print(e)
        return "sorry, there is a problem with connection to shazam, please try again"
def download_mp4(url, f_id):
    filename = str(f_id) + ".mp4"
    ydl_opts = {
        "format": "best",
        "outtmpl": filename
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return filename

def download_mp3(url, file_id):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{file_id}.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        'ffmpeg_location': '.',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return f"{file_id}.mp3"

def clean():
    files = os.listdir(".")
    for file in files:
        if file.endswith(("mp4","mp3")):
            os.remove(file)
            print(f"file {file} deleted")
@bot.message_handler(commands=['start'])
def welcome(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Download video")
    btn2 = types.KeyboardButton("Info")
    kb.add(btn1)
    kb.add(btn2)
    bot.send_message(message.chat.id, "choose option:", reply_markup=kb) 

@bot.message_handler(func=lambda message: "tiktok.com" in message.text.lower())
def link_hand(message):
    url = message.text
    bot_message = bot.send_message(message.chat.id, "Converting link to mp4...", 
        reply_to_message_id=message.message_id)
    filename = f"{message.chat.id}_{message.message_id}"
    try:
        file_vid = download_mp4(message.text, filename)
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=bot_message.message_id,
                              text="failure to convert mp4, maybe link is <i>unsuported type</i>, or link is slide show",
                              parse_mode="HTML")
        print(e)
        return 0

    kb = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Get audio", callback_data="audio")
    button2 = types.InlineKeyboardButton(text="find music info (title, author)", callback_data="track_info")
    kb.add(button1)
    kb.add(button2)

    bot.edit_message_text(chat_id=message.chat.id, 
                          message_id=bot_message.message_id, 
                          text="Uploading video...")
    
    with open (file_vid, "rb") as video:
        bot.send_video(message.chat.id, 
                       video, caption=url, 
                       supports_streaming=True,
                       reply_markup=kb)
    script_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_path, file_vid)
    os.remove(file_path)

@bot.callback_query_handler(func = lambda call: True)
def call_handl(call):
    file_name = f"{call.message.chat.id}_{call.message.message_id}"
    url = call.message.caption

    if call.data == "audio":
        bot.answer_callback_query(call.id, text="converting mp3...")
        bot_message = bot.send_message(call.message.chat.id,"converting mp4 to mp3 file...")

        file_aud = download_mp3(url, file_name)
        bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=bot_message.message_id,
                                text="uploading audio...")
        
        with open(file_aud, "rb") as audio:
            bot.send_audio(call.message.chat.id, audio)
 
        script_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_path, file_aud)
        os.remove(file_path)

    elif call.data == "track_info":
        bot_message = bot.send_message(call.message.chat.id, "connecting to shazam data base...")

        file_aud = download_mp3(url, file_name)
        script_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_path, file_aud)
        
        mes_text = asyncio.run(find_song_info(file_path))
        bot.edit_message_text(chat_id=call.message.chat.id,
                               message_id=bot_message.message_id, 
                               text=mes_text,
                               parse_mode="HTML")
        
        bot.send_message(chat_id=call.message.chat.id, 
                        reply_to_message_id=bot_message.message_id,
                        text="information about music can be <i>not fully acurate</i>",
                        parse_mode="HTML")
        os.remove(file_path)

@bot.message_handler(func=lambda message: True)
def data_option(message):
    if message.text == "Download video":
        bot.send_message(message.chat.id, "Send link video:")
    elif message.text == "Info":
        bot.send_message(message.chat.id, f"bot for extracting video/audio from a Tiktok link, also can guess the song in a link\n" \
        "This is a synchronous bot, so please <b><i>wait until it responds</i></b> to your request before asking another one",
        parse_mode="HTML")
    else: 
        bot.send_message(chat_id=message.chat.id,
                        reply_to_message_id=message.message_id,
                        text="This message doesnt look like command, please enter <b>tiktok link or commands</b>",
                        parse_mode="HTMl")
clean()
bot.infinity_polling()
