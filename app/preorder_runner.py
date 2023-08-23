import os
import logging
import pandas as pd
import preorder as Prunner

def create_exclude_excel_file(exclude_file_path):
    if os.path.exists(exclude_file_path):
        print(f"{exclude_file_path} already exists. Please update your exclude keywords.")
    else:
        df = pd.DataFrame(columns=["Keywords or Product Name"])
        df.to_excel(exclude_file_path, index=False)
        print("Exclude keyword file created successfully!")

def daily_routines():
    print("Daily routine: Close pre-order, open pre-order")
    close_preorder()
    print("Pre-order closed successfully")
    open_preorder()
    print("Pre-order opened successfully")

def close_preorder():
    pbot = Prunner.Preorder()
    pbot.PreOrderClose()

def open_preorder():
    pbot = Prunner.Preorder()
    pbot.PreOrderOpen()

def close_preorder_by_keywords():
    pbot = Prunner.Preorder()
    pbot.PreOrderCloseKeywords()

def find_missing():
    pbot = Prunner.Preorder()
    pbot.FindMissingPreOrderOpen()

def description_force_update():
    pbot = Prunner.Preorder()
    pbot.PreOrderDescriptionForceUpdate()

def main():
    print("===================")
    print("Welcome to Shopline Pre Order Automation Tool")
    print("===================")
    print("Initializing...")
    exclude_file_path = "search/exclude.xls"
    create_exclude_excel_file(exclude_file_path)

    while True:
        print("===================")
        print("Select an option:")
        print("daily: Run all daily routines")
        print("1: Close all Pre-order")
        print("2: Open all Pre-order")
        print("3: Close Pre-order by keyword")
        print("4: Find Missing Pre-order by keyword")
        print("5: Pre-order Description Force Update")
        print("quit: Quit")

        choice = input("Enter your choice: ")
        if choice.lower() == 'daily':
            logging.info("Executing all daily routines")
            daily_routines()
            logging.info('All daily routines completed successfully')
        elif choice == '1':
            logging.info("Executing close all Pre-order")
            close_preorder()
            logging.info('All pre-order closed successfully')
        elif choice == '2':
            logging.info("Executing open all Pre-order")
            open_preorder()
            logging.info('All pre-order opened successfully')
        elif choice == '3':
            logging.info("Executing close pre-order by keyword")
            close_preorder_by_keywords()
            logging.info("Pre-order closed by keyword successfully")
        elif choice == '4':
            logging.info("Executing find Missing Pre-order by keyword")
            find_missing()
            logging.info("Find missing pre-order by keyword successfully")
        elif choice == '5':
            logging.info("Executing pre-order Description force update")
            description_force_update()
            logging.info("Pre-order Description force updated successfully")
        elif choice.lower() == 'quit':
            print("Thank you for using Shopline Automation Tool. Goodbye!")
            logging.info('Script completed successfully')
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()