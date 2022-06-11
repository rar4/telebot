from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import cv2
import easyocr

bot = Bot(token='5476184332:AAE2b3f0lAnNrSI3k9pP5dN08T4Il2kKQ14')

dispacher = Dispatcher(bot)


@dispacher.message_handler(commands=['start'])
async def starter(message: types.Message):
    """

    start comand hendler
    """
    await message.reply(" Hello it is a scaner bot. \nYou can sand image there and recive text from it,"
                        " it scans only english and russian text."
                        "\n DISCLAMER"
                        "\n This bot can scan scan inexactly.")


@dispacher.message_handler(content_types=types.ContentType.PHOTO)
async def scan_message(message: types.Message):

    print('start')
    """
scans text from photos which you sends to this bot
    """
    chat_id = message.from_user.id

    imdict = await bot.get_file(message.photo[-1].file_id)
    down_file = await bot.download_file(imdict.file_path)

    new_file = "media/as.png"

    with open(new_file, 'wb') as file:
        file.write(down_file.getvalue())

    img = cv2.imread('media/as.png')

    string = ''

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (1024, 767))
    txt = easyocr.Reader(['en', 'ru'])

    text = txt.readtext(gray, detail=0)
    string += text[0]
    text.pop(0)
    for i in text:
        string += f' {i}'

    await dispacher.bot.send_message(chat_id=chat_id, text=string)


executor.start_polling(dispacher)
