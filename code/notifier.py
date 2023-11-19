"""
File: notifier.py
Author: Vyshnavi Adusumelli, Tejaswini Panati, Harshavardhan Bandaru
Date: October 01, 2023
Description: File contains Telegram bot message handlers and their associated functions.

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
from jproperties import Properties

configs = Properties()

class TelegramNotifier:
    def __init__(self, token: str, parse_mode: str = None, chat_id: str = None):
        self._token = token
        self._parse_mode = parse_mode
        if chat_id is None:
            self._get_chat_id()
        else:
            self._chat_id = chat_id

    def _get_chat_id(self):
        try:
            data = {"offset": 0}
            response = requests.get(
                f"https://api.telegram.org/bot{self._token}/getUpdates",
                data=data,
                timeout=10,
            )
            if response.status_code == 200:
                self._chat_id = response.json()["result"][-1]["message"]["chat"]["id"]
        except Exception as e:
            self._chat_id = None
            print("Couldn't get chat_id!\n\t", e)

    def send(self, msg: str):
        if self._chat_id is None:
            self._get_chat_id()
            print("chat_id is none, nothing sent!")
            return
        data = {"chat_id": self._chat_id, "text": msg}
        if self._parse_mode:
            data["parse_mode"] = self._parse_mode
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{self._token}/sendMessage",
                data=data,
                timeout=10,
            )
            if response.status_code != 200 or response.json()["ok"] is not True:
                print(
                    f"Failed to send notification:\n\tstatus_code={response.status_code}\n\tjson:\n\t{response.json()}"
                )
        except Exception as e:
            print(f"Failed to send notification:\n\texception:\n\t{e}")