import logging

from datetime import datetime
from functools import wraps
from flask import Flask, request

from db import DB

notification_time = int(DB.get_notification_time(673162780))
cur_time = datetime.now().hour

time_left_possible1 = notification_time - cur_time
time_left_possible2 = time_left_possible1 % 24

print(max(time_left_possible1, time_left_possible2))