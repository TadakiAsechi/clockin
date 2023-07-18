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
