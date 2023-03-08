import preorder
import logging
import os
from datetime import datetime

def close_preorder():
    pbot = preorder.Preorder()
    pbot.PreOrderClose()

def open_preorder():
    pbot = preorder.Preorder()
    pbot.PreOrderOpen()

def close_preorder_by_keywords():
    pbot = preorder.Preorder()
    pbot.PreOrderCloseKeywords()

def find_missing():
    pbot = preorder.Preorder()
    pbot.FindMissingPreOrderOpen()

# Create the log folder if it doesn't exist
if not os.path.exists('log'):
    os.makedirs('log')

# Set up the logger
now = datetime.now()
log_file = f'log/{now.strftime("%Y-%m-%d_%H-%M-%S")}.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


print("Shopline Automation Tool")
while True:
    print("===================")
    print("Select an option:")
    print("1. Close all Pre-order")
    print("2. Open all Pre-order")
    print("3. Close Pre-order by keyword")
    print("4. Find Missing Pre-order by keyword")
    print("5. Quit")

    choice = input("Enter your choice (1-5): ")
    if choice == '1':
        logging.info("Execute close all Pre-order")
        close_preorder()
        logging.info('All pre-order closed successfully')
        print("Pre-order closed successfully")
    elif choice == '2':
        logging.info("Execute open all Pre-order")
        open_preorder()
        logging.info('All pre-order opened successfully')
        print("Pre-order opened successfully")
    elif choice == '3':
        logging.info("Execute close pre-order by keyword")
        close_preorder_by_keywords()
        logging.info("Pre-order closed by keyword successfully")
    elif choice == '4':
        logging.info("Execute find Missing Pre-order by keyword")
        find_missing()
        logging.info("Find missing pre-order by keyword successfully")
    elif choice == '5':
        print("Thank you for using Shopline Automation Tool, bye!")
        logging.info('Script completed successfully')
        break
    else:
        print("Invalid choice. Please try again.")