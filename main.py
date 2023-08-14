import os
import logging
from datetime import datetime
import preorder_runner

def setup_logger():
    if not os.path.exists('log'):
        os.makedirs('log')

    now = datetime.now()
    log_file = f'log/{now.strftime("%Y-%m-%d_%H-%M-%S")}.log'
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def main():
    print("Welcome to Shopline Automation Tool")
    print("===================")
    setup_logger()

    while True:
        print("===================")
        print("Select an option:")
        print("1: Pre Order Automation Tool")
        print("2: Google Category Compliance Update")
        print("quit: Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            preorder_runner.main()
        elif choice == '2':
            print("Running Google Merchant Compliance Update...")
            os.system("python google_merchant_compliance.py")  # Run the script directly
        elif choice.lower() == 'quit':
            print("Thank you for using Shopline Automation Tool, bye!")
            logging.info('Script completed successfully')
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()