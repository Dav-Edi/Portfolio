from aiogram import Dispatcher
from aiogram.types import Message

from lexicon.lexicon_ru import LEXICON_RU

async def send_answer(message: Message):
    await message.answer(LEXICON_RU['other_answer'])

async def register_other_handlers(dp: Dispatcher):
    await dp.register_message_handler(send_answer)