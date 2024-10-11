import asyncio
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import requests
from flask import Flask, request

from src.create_bot import bot
from src.database.models import OneWinRegistration, OneWinDeposit
from src.database.users import get_user_or_none
from src.handlers.user.kb import Keyboards
from src.handlers.user.messages import Messages
from config import Config


app = Flask(__name__)


async def send_registration_passed(user_id):
    await bot.send_message(
        chat_id=user_id,
        text=Messages.get_registration_passed(),
        reply_markup=Keyboards.get_check_deposit(user_id=user_id)
    )


async def send_dep(user_id):
    user  =get_user_or_none(user_id)
    await bot.send_message(
        chat_id=user_id,
        text=Messages.get_bot_activated(),
        reply_markup=Keyboards.get_play(lang=user.language_code)
    )

# def send_registration_success(user_id):
#     text = Messages.get_registration_passed()
#     markup = Keyboards.get_check_deposit(user_id=user_id).as_json()
#     requests.get(
#         f'https://api.telegram.org/bot{Config.BOT_TOKEN}/sendMessage?'
#         f'chat_id={user_id}&text={quote(text)}'
#         f'&reply_markup={quote(markup)}&parse_mode=HTML'
#     )
#
#
# def send_deposit_success(user_id):
#     text = Messages.get_bot_activated()
#     markup = Keyboards.get_play().as_json()
#     requests.get(
#         f'https://api.telegram.org/bot{Config.BOT_TOKEN}/sendMessage?'
#         f'chat_id={user_id}&text={quote(text)}'
#         f'&reply_markup={quote(markup)}&parse_mode=HTML'
#     )


def send_notification(text: str):
    for admin_id in Config.ADMIN_IDS:
        requests.get(
            f'https://api.telegram.org/bot{Config.POSTBACK_BOT_TOKEN}/'
            f'sendMessage?chat_id={admin_id}&text={text}'
        )


@app.route('/', methods=['GET'])
def index():
    return "I'm alive!"


@app.route("/registration", methods=['GET'])
def registration():
    one_win_id = request.args.get('user_id')
    sub1 = request.args.get('sub1')

    OneWinRegistration.get_or_create(one_win_id=one_win_id, sub1=sub1)
    user = get_user_or_none(sub1)
    if user:
        user.onewin_id = sub1
        user.save()

    text = f"Регистрация: {one_win_id} \nsub1:{sub1}"
    send_notification(text=text)

    return 'OK: 200'


@app.route('/fd', methods=['GET'])
def fd():
    one_win_id = request.args.get('user_id')
    amount = request.args.get('amount')
    sub1 = request.args.get('sub1')

    OneWinDeposit.get_or_create(sub1=sub1, one_win_id=one_win_id, amount=amount)
    # send_deposit_success(user_id=sub1)

    text = f'{one_win_id} : первый депозит : {amount}  \nsub1:{sub1}'
    send_notification(text=text)

    return 'OK: 200'



@app.route('/deposit')
def deposit():
    one_win_id = request.args.get('user_id')
    amount = request.args.get('amount')
    sub1 = request.args.get('sub1')

    OneWinDeposit.get_or_create(sub1=sub1, one_win_id=one_win_id, amount=amount)

    text = f'{one_win_id} : депозит : {amount} \nsub1:{sub1}'
    send_notification(text=text)

    return 'OK: 200'



def run_app():
    while True:
        try:
            app.run(host="0.0.0.0", port=Config.POSTBACK_PORT)
        except Exception as ex:
            print(ex)
