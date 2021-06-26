import logging
from AItools import OCR, CreateImage, SpeechRecognition, CreateAudio, ChatBott
import constants as keys
from telegram.ext import *
from telegram import * 
import os


# img = ImageClassification('Inception')
# img.read_process_image('abc.jpg')
# print(img.predict())



# ocr = OCR()
# out = ocr.text_from_image('bcd.jpg')
# print(out)


# crimg = CreateImage()
# crimg.draw('black', 1200, 1200, out)

# sr = SpeechRecognition()
# print(sr.text_from_audio('abc.wav'))

# au = CreateAudio()
# au.text_to_audio('that contain at least half as many vowels as consonants.')



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


_CHOOSING, _IMAGE, _AUDIO, _CHAT = range(4)
_IMAGETOTEXT, _AUDIOTOTEXT, _TEXTTOIMAGE, _TEXTTOAUDIO = range(4, 8)

keyboard1 = [
    ['IMAGE', 'AUDIO'],
    ["CHAT"]
]
keyboard2 = [
    ['IMAGE TO TEXT', 'TEXT TO IMAGE'],
    ['BACK']
]
keyboard3 = [
    ['AUDIO TO TEXT', 'TEXT TO AUDIO'],
    ['BACK']
]
keyboard4 = [
    ["CANCEL"]
]

markup1 = ReplyKeyboardMarkup(keyboard1, resize_keyboard=True, one_time_keyboard=True)
markup2 = ReplyKeyboardMarkup(keyboard2, resize_keyboard=True, one_time_keyboard=True)
markup3 = ReplyKeyboardMarkup(keyboard3, resize_keyboard=True, one_time_keyboard=True)
markup4 = ReplyKeyboardMarkup(keyboard4, resize_keyboard=True, one_time_keyboard=True)

ocr = OCR()
crimg = CreateImage()
sr = SpeechRecognition()
au = CreateAudio()
ch = ChatBott()


def start(update, context) -> int:
    update.message.reply_text(
        "Hello I am AI-Bot\nI can change Image and Audio to Text and vice versal and also you can chat with me",
        reply_markup=markup1,
    )
    return _CHOOSING

def image(update, context) -> int:
    update.message.reply_text(
        "choose either image to text or text to image or back to return to main",
        reply_markup=markup2,
    )

    return _IMAGE

def audio(update, context) -> int:
    update.message.reply_text(
        "choose either audio to text or text to audio or back to return to main",
        reply_markup=markup3,
    )

    return _AUDIO

def chat(update, context):
    global chat
    chat = ch.createbot()
    update.message.reply_text(
        "your chat is started say hello or something to start or back to return to main", 
        reply_markup=markup4
    )

    return _CHAT

def image_to_text(update, context):
    update.message.reply_text(
        "now send me an image file or cancel to go back", 
        reply_markup=markup4,
        )

    return _IMAGETOTEXT

def uploadimage(update, context):
    try:
        has_photo = len(update.message.photo) if update.message.photo else False
        bot = context.bot
        file_ = [
            [fil["file_size"], fil["file_id"], fil["file_unique_id"]]
            for fil in update.message.photo
        ]
        file_.sort()
        file_name = 'trash/temp.png'
        download_file = bot.getFile(file_[-1][1])
        download_file.download(custom_path=file_name)
        update.message.reply_text("succesfully uploaded!")
        text = ocr.text_from_image(file_name)
        update.message.reply_text(
            "text extracted from the image:\n"+text, 
            reply_markup=markup2
            )

        return _IMAGE
    except:
        update.message.reply_text(
            "there was an error please send me the photo again",
            reply_markup=markup4
            )

        return _IMAGETOTEXT

def text_to_image(update, context):
    update.message.reply_text(
        "now send me an text that you want to write it on a picture or cancel to go back", 
        reply_markup=markup4,
        )

    return _TEXTTOIMAGE

def textonimage(update, context):
    text = update.message.text
    chat_id = update.message.chat_id
    try:
        # saves the image with name temp.png in the current directory
        crimg.draw('black', 1200, 1200, text=text)
        update.message.reply_text('here you go')
        context.bot.send_photo(
            chat_id=chat_id, photo=open('trash/temp.png', 'rb'), 
            reply_markup=markup2
            )
        
        return _IMAGE

    except:
        update.message.reply_text(
            'an error has occured please send me the text again',
            )

        return _TEXTTOIMAGE

def audio_to_text(update, context):
    update.message.reply_text(
        "now send me an audio file wav format preferred or cancel to go back", 
        reply_markup=markup4
        )

    return  _AUDIOTOTEXT

def uploadaudio(update, context):
    try:
        download_file = update.message.audio.get_file()
        file_name = update.message.audio.file_name
        new_filename = 'trash/temp.'+file_name.split('.')[-1]
        # print(dir(update.message.audio))
        download_file.download(custom_path=new_filename)
        update.message.reply_text("succesfully uploaded!")

        text = sr.text_from_audio(new_filename)
        update.message.reply_text(
            "text extracted from the audio file\n"+text, 
            reply_markup=markup3
            )

        return _AUDIO

    except:
        update.message.reply_text(
            "there was an error please send me the audio file again", 
            reply_markup=markup4
            )

        return _AUDIOTOTEXT

def text_to_audio(update, context):
    update.message.reply_text(
        "now send me an text that you want to convert it to audio or cancel to go back", 
        reply_markup=markup4)

    return _TEXTTOAUDIO

def textonaudio(update, context):
    text = update.message.text 
    chat_id = update.message.chat_id
    try:
        # saves the audio file named 'temp.ext' in current directory
        au.text_to_audio(text)
        update.message.reply_text("here you go", reply_markup=markup3)
        context.bot.send_audio(
            chat_id=chat_id, audio=open('trash/temp.mp3', 'rb'),
            reply_markup=markup3)
            
        return _AUDIO

    except:
        update.message.reply_text(
            "an error has occured please send me the text again", 
            reply_markup=markup3)

        return _TEXTTOAUDIO

def chatting(update, context):
    global chat
    text = update.message.text
    res = chat.get_response(text)
    update.message.reply_text(
        str(res), reply_markup=markup4
    )

    return _CHAT

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(keys.API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            _CHOOSING : [
                MessageHandler(
                    Filters.regex(
                        "^(IMAGE)$",
                    ),
                    image,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(AUDIO)$",
                    ),
                    audio,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(CHAT)$",
                    ),
                    chat,
                ),
            ],
            _IMAGE : [
                MessageHandler(
                    Filters.regex(
                        "^(IMAGE TO TEXT)$",
                    ),
                    image_to_text,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(TEXT TO IMAGE)$",
                    ),
                    text_to_image,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(BACK)$",
                    ),
                    start,
                ),
            ],
            _IMAGETOTEXT : [
                MessageHandler(
                    Filters.photo | Filters.document.category("image"), uploadimage
                ),
                MessageHandler(
                    Filters.regex(
                        "^(CANCEL)$",
                    ),
                    image,
                ),
            ],
            _TEXTTOIMAGE : [
                MessageHandler(
                    Filters.regex(
                        "^(CANCEL)$",
                    ),
                    image,
                ),
                MessageHandler(
                    Filters.text, 
                    textonimage,
                ),
            ],
            _AUDIO: [
                MessageHandler(
                    Filters.regex(
                        "^(AUDIO TO TEXT)$",
                    ),
                    audio_to_text,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(TEXT TO AUDIO)$",
                    ),
                    text_to_audio,
                ),
                MessageHandler(
                    Filters.regex(
                        "^(BACK)$",
                    ),
                    start,
                ),
            ],
            _AUDIOTOTEXT : [
                MessageHandler(
                    Filters.audio | Filters.document.category("audio"), uploadaudio
                ),
                MessageHandler(
                    Filters.regex(
                        "^(CANCEL)$",
                    ),
                    audio,
                ),
            ],
            _TEXTTOAUDIO : [
                MessageHandler(
                    Filters.regex(
                        "^(CANCEL)$",
                    ),
                    audio,
                ),
                MessageHandler(
                    Filters.text, 
                    textonaudio,
                ),
            ],
            _CHAT : [
                MessageHandler(
                    Filters.regex(
                        "^(CANCEL)$",
                    ),
                    start,
                ),
                MessageHandler(
                    Filters.text, 
                    chatting,
                ),
            ],
        },

        fallbacks=[
            MessageHandler(Filters.text, start),
        ],
    )

    # dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()





if __name__ == '__main__':
    main()
