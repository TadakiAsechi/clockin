# coding: utf-8

from dataclasses import dataclass, field
import enum


@dataclass
class Email:
    # server
    smtp_server: str
    port: int
    username: str
    password: str
    # message
    to: str = ""
    cc: list = field(default_factory=list)
    subject: str = ""
    body: str = ""


class APP(enum.Enum):
    MAIN = 0
    OFF = 1
    CHECK = 2


class Message(enum.Enum):
    IN = 1
    OUT = 2
    OFF = 3


class MailResult(enum.Enum):
    SUCCESS = (0, "送信に成功しました。")
    CONNECTIONERROR = (1, "コネクションに失敗しました。")
    EXCEPTION = (2, f"エラーが発生しました。")
