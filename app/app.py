from flask import Flask, render_template, request
import os
import logging
from datetime import datetime
import preorder_runner

app = Flask(__name__)

def setup_logger():
    if not os.path.exists('log'):
        os.makedirs('log')

    now = datetime.now()
    log_file = f'log/{now.strftime("%Y-%m-%d_%H-%M-%S")}.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        choice = request.form["choice"]
        if choice == '1':
            preorder_runner.main()
        elif choice == '2':
            print("Running Google Merchant Compliance Update...")
            os.system("python google_merchant_compliance.py")
        else:
            return "Invalid choice. Please try again."

        return "Task completed. <a href='/'>Back</a>"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
