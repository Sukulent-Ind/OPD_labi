import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv
import random
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove


load_dotenv()
TOKEN = getenv("BOT_TOKEN")

storage = MemoryStorage()
bot_router = Router()


quiz_questions = {

        "Какой город является столицей Франции?": "Париж",
        "На каком континенте находится река Амазонка?": "Южная Америка",
        "Какой океан самый большой на планете?": "Тихий",
        "В какой стране находится пирамида Хеопса?": "Египет",
        "Какой самый высокий водопад в мире?": "Анхель",


        "Какой химический элемент имеет символ O?": "Кислород",
        "Какой закон описывает относительность движения в механике?": "Закон инерции",
        "Кто разработал периодическую таблицу элементов?": "Менделеев",
        "Как правильно называется в астрономии 'Красная планета'?": "Марс",


        "В каком году началась Вторая мировая война?": "1939",
        "Кто был первым президентом США?": "Джордж Вашингтон",
        "Как называется древнегреческий город, известный своим театром и философами?": "Афины",
        "Кто открыл Америку для европейцев?": "Колумб",


        "Какое животное является национальным символом Австралии?": "Кенгуру",
        "Что означает аббревиатура 'WWW'?": "Всемирная паутина",
        "Какой элемент на таблице Менделеева имеет атомный номер 1?": "Водород",

}


class Game(StatesGroup):
    game_is_on = State()


# Функция для отправки вопроса
async def send_quiz_question(message: Message, state: FSMContext):
    question, answer = random.choice(list(quiz_questions.items()))
    await message.answer(question)
    await state.set_state(Game.game_is_on)
    return answer  # Возвращаем правильный ответ для дальнейшей проверки


@bot_router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer(
        "Привет! Если хочешь начать викторину, то напиши /quiz, если захочешь отменить викторину - напиши /cancel",
        reply_markup=ReplyKeyboardRemove(),
    )


@bot_router.message(Command("cancel"))
@bot_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@bot_router.message(Command("quiz"))
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Отлично! Первый вопрос",
        reply_markup=ReplyKeyboardRemove(),
    )
    await asyncio.sleep(1)

    correct_answer = await send_quiz_question(message, state)
    await state.update_data(correct_answer=correct_answer)
    await state.update_data(cnt=1)


@bot_router.message(Game.game_is_on)
async def game_is_going(message: Message, state: FSMContext):
    data = await state.get_data()

    if message.text.lower() == data.get("correct_answer").lower():
        await state.update_data(cnt=data.get("cnt") + 1)

        if data.get("cnt") == 5:
            await state.clear()
            await message.answer("Поздравляю! Вы ответили на все вопросы")
            return

        await message.answer("Неплохо! Следующий вопрос")
        correct_answer = await send_quiz_question(message, state)
        await state.update_data(correct_answer=correct_answer)

    else:
        await message.answer("Хорошая попытка, но попробуй ещё раз")
        return



async def main():
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=storage)

    dp.include_router(bot_router)

    # Start event dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())