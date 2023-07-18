# coding: utf-8

import ssl
import os
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

import smtplib

from conf import Email, Message


def greet():
    time = datetime.now()
    print(f"now, it's {time} o'clock!")
    msg = "Morning!"
    
    return msg


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
    email.cc.append(os.environ["CLOCKIN_USERNAME"])

    email.subject = sbj
    email.body = msg

    # SSLコンテクストの作成
    context = ssl.create_default_context()

    # メッセージの作成
    message = MIMEMultipart()
    message["From"] = email.username
    message["To"] = email.to
    message["CC"] = ",".join(email.cc)
    message["Subject"] = email.subject
    message.attach(MIMEText(email.body, "plain"))

    # サーバーのセットアップと送信
    try:
        server = smtplib.SMTP_SSL(email.smtp_server, email.port, context=context, timeout=10)
        server.ehlo()
        server.login(email.username, email.password)
        server.sendmail(email.username, email.to, message.as_string())
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
            msg = "出勤しましたよ！"
        case Message.OUT:
            sbj = "退勤報告_${me}"
            msg = "退勤しましたよ！"
        case Message.OFF:
            sbj = "有給申請_${me}"
            msg = "${boss}部長\n\nお疲れ様です。${me}です。\n\n以下の日程で有給休暇を取得させていただきたく思います。\n\n${term} \n" \
                  "\n先方にも確認済みで、前後での業務の引き継ぎやフォローなどはしっかり行おうと思います。\n\n以上、ご査証のほどよろしくお願いいたします。\n\n${me}"
        case _:
            raise ValueError("引数はEnum型Messageから選んでください。")

    return sbj, msg
