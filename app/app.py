from flask import Flask, render_template, request
import os
import logging
from datetime import datetime
import pandas as pd
import preorder as Prunner

app = Flask(__name__)

# Constants
DAILY_ROUTINES_ACTION = 'daily'
CLOSE_PREORDER_ACTION = '1'
OPEN_PREORDER_ACTION = '2'
FIND_MISSING_ACTION = '3'

# Logging setup
def setup_logger():
    if not os.path.exists('log'):
        os.makedirs('log')

    now = datetime.now()
    log_file = f'log/{now.strftime("%Y-%m-%d_%H-%M-%S")}.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Preorder actions
def execute_action(action):
    pbot = Prunner.Preorder()
    if action == CLOSE_PREORDER_ACTION:
        print("Running close pre-order")
        pbot.PreOrderClose()
    elif action == OPEN_PREORDER_ACTION:
        print("Running open pre-order")
        pbot.PreOrderOpen()
    elif action == FIND_MISSING_ACTION:
        print("Running find missing pre-order")
        pbot.FindMissingPreOrderOpen()

def execute_daily_routines():
    print("Running daily routines")
    logging.info("Executing all daily routines")
    pbot = Prunner.Preorder()
    pbot.PreOrderClose()
    logging.info('All pre-order closed successfully')
    pbot = Prunner.Preorder()
    pbot.PreOrderOpen()
    logging.info('All pre-order opened successfully')
    logging.info('All daily routines completed successfully')

# Flask route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        choice = request.form["choice"]
        if choice == '1':
            action = request.form.get("pre_order_action")
            if action:
                if action == DAILY_ROUTINES_ACTION:
                    execute_daily_routines()
                else:
                    execute_action(action)
                return "Task completed. <a href='/'>Back</a>"
            else:
                return "Invalid action. Please try again."

        elif choice == '2':
            print("Running Google Merchant Compliance Update...")
            os.system("python google_merchant_compliance.py")
            return "Task completed. <a href='/'>Back</a>"
        else:
            return "Invalid choice. Please try again."

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
