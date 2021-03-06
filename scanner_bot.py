from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import cv2
import easyocr


with open('token', 'r') as t:
    text = t.read()
    if text == '':
        token = input('input token: ')
        with open('token', 'w') as tx:
            tx.write(token)

with open('token', 'r') as t:
    tokeen = t.read()

bot = Bot(token=tokeen)

dispacher = Dispatcher(bot)

class Bot:

    def __init__(self):
        self.token = tokeen

    @staticmethod
    @dispacher.message_handler(commands=['start'])
    async def starter(message: types.Message):
        """start comand hendler """
        await message.reply(" Hello it is a scaner bot. \nYou can sand image there and recive text from it,"
                            " it scans only english and russian text."
                            "\n DISCLAMER"
                            "\n This bot can scan incorectly.")


    @staticmethod
    @dispacher.message_handler(content_types=types.ContentType.PHOTO)
    async def scan_message(message: types.Message):

        print('start')
        """scans text from photos which you sends to this bot"""

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

        scanned_text = txt.readtext(gray, detail=0)
        string += scanned_text[0]
        scanned_text.pop(0)
        for i in scanned_text:
            string += f' {i}'

        await dispacher.bot.send_message(chat_id=chat_id, text=string)


executor.start_polling(dispacher)
