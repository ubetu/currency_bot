import logging

from datetime import datetime
from functools import wraps
from flask import Flask

from db import DB



logging.basicConfig(level=logging.INFO, filename="/home/a0999441/domains/parcingcbscript.ru/public_html/py_log.log",
                    filemode="w", format="%(asctime)s %(levelname)s %(message)s")
                    
app = Flask(__name__)




def logging_wrapper(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result if result is not None else 'YES'
            
        except Exception as e:
            logging.error(e, exc_info=True)
            return 'NO'
            
    return inner
    
    

  
@app.route('/currencies_checking/<currencies>/<user_id>/<registrated>', methods=['GET'])
@logging_wrapper
def currencies_checking(currencies: str, user_id: str, registrated: str) -> str:
    if DB.check_correct_currencies(currencies):
        if registrated == 'True':
            DB.set_currencies(user_id, currencies)
        return 'YES'
        
    return 'NO'



@app.route('/rewriting_time/<notification_time>/<user_id>', methods=['POST'])
@logging_wrapper
def rewriting_time(notification_time: str, user_id: str) -> str:
    DB.set_notification_time(user_id, notification_time)
    return 'YES'



@app.route('/registration/<currencies>/<notification_time>/<user_id>', methods=['POST'])
@logging_wrapper
def registration(currencies: str, notification_time: str, user_id: str) -> str:
    DB.write_user_info(user_id, currencies, notification_time)
    return 'YES'



@app.route('/get_currencies_cost/<user_id>', methods=['GET'])
@logging_wrapper
def get_currencies_cost(user_id: str) -> str:
    return DB.get_currencies_cost(user_id)



@app.route('/get_notification_time/<user_id>', methods=['GET'])
@logging_wrapper
def get_notification_time(user_id: str) -> str:
    return DB.get_notification_time(user_id)



@app.route('/get_time_left/<user_id>', methods=['GET'])
@logging_wrapper
def get_time_left(user_id: str) -> str:
    notification_time = int(DB.get_notification_time(user_id))
    cur_time = datetime.now().hour
    
    time_left_possible1 = notification_time - cur_time
    time_left_possible2 = time_left_possible1 % 24

    return str(max(time_left_possible1, time_left_possible2))



if __name__ == "__main__":
    app.run()
