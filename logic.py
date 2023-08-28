# coding: utf-8

import ssl
import os
import random
from datetime import datetime
import time

import tkinter.ttk as ttk
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib
import openai

from conf import Email, Message

def send_email(sbj, msg):
    """引数の内容でメールを上司に送る

    :param sbj:
    :param msg:
    :return result:
    """

    # メールサーバーの情報をセット
    host = os.environ["CLOCKIN_SERVER"]
    username = os.environ["CLOCKIN_USERNAME"]
    password = os.environ["CLOCKIN_PASSWORD"]

    # メールオブジェクトをインスタンス化
    email = Email(
        smtp_server=host,
        port=465,
        username=username,
        password=password)

    # メッセージを詰める
    email.to = os.environ["CLOCKIN_BOSSMAIL"]

    cc_list = [item.strip() for item in os.environ["CLOCKIN_CC"].split(",")]
    email.cc.extend(cc_list)

    email.subject = sbj
    email.body = msg

    # SSLコンテクストの作成
    context = ssl.create_default_context()

    # メッセージの作成
    message = MIMEMultipart()
    message["From"] = email.username
    message["To"] = email.to
    message["CC"] = ", ".join(cc_list)
    message["Subject"] = email.subject
    message.attach(MIMEText(email.body, "plain"))

    # サーバーのセットアップと送信
    try:
        server = smtplib.SMTP_SSL(email.smtp_server, email.port, context=context, timeout=10)
        server.ehlo()
        server.login(email.username, email.password)
        send_list = email.cc
        send_list.append(email.to)
        server.sendmail(email.username, send_list, message.as_string())
    except (OSError, ConnectionRefusedError) as e:
        print("Connection failed: ", e)
        result = "コネクションに失敗しました。"
    except Exception as e:
        print(type(e), e)
        result = f"エラーが発生しました:{type(e)}"
    else:
        result = "送信に成功しました。"
    finally:
        server.quit()

    return result


def get_message(msg_type):
    match msg_type:
        case Message.IN:
            sbj = "出勤報告_${me}"
            msg = "${boss}部長\n\nお疲れ様です。${me}です。\n\n本日${time}に出社いたしましたのでご報告いたします。" \
                  "\n\n以上、ご確認のほどよろしくお願いいたします。\n\n${me}"
        case Message.OUT:
            sbj = "退勤報告_${me}"
            msg = "${boss}部長\n\nお疲れ様です。${me}です。\n\n本日${time}に退勤いたしますのでご報告いたします。" \
                  "\n\n以上、ご確認のほどよろしくお願いいたします。\n\n${me}"
        case Message.OFF:
            sbj = "有給申請_${me}"
            msg = "${boss}部長\n\nお疲れ様です。${me}です。\n\n以下の日程で有給休暇を取得させていただきたく思います。\n\n${term} \n" \
                  "\n先方にも確認済みで、前後での業務の引き継ぎやフォローなどはしっかり行おうと思います。\n\n以上、ご査証のほどよろしくお願いいたします。\n\n${me}"
        case _:
            raise ValueError("引数はEnum型Messageから選んでください。")

    return sbj, msg


def get_quartered_time():
    now = datetime.now()
    hour = now.hour
    min = now.minute
    min_quarter = min//15
    time = f"{hour}:{min_quarter*15}"

    return time


def generate_message():
    openai.api_key = os.environ["CLOCKIN_OPENAI_API_KEY"]
    now = datetime.now()
    hour = now.hour

    rand = random.randint(1, 3)

    match rand:
        case 1:
            prompt = f"Now time is {hour}. I'm at office. greet me in nice way."
        case 2:
            prompt = f"Give me a insightful quote."
        case 3:
            prompt = f"Give me a fun fact."
        case _:
            prompt = f"Just echo this: 'Unexpected number was chosen.'"

    # メッセージがランダム性を高くするため、temperatureを高めに設定する。
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=1.5,
        messages=[
            {"role": "user", "content": prompt }
        ]
    )

    message = res['choices'][0]['message']['content']

    return message

