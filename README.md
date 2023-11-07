# Shopline Automation Tool

Author: Willon Lai

Version: 3.0

Last Update: 31/10/2023

- Functions
  1. Automotaion tool in handling pre-order settings
  2. Update Google Merchant Product Category

Prerequisite:

* pip
* python (ver 3.9 or above)
* git

Run this command before running the code for setup, install the required libraries and pull the latest version.

```
git pull
pip install -r requirements.txt   
```

Run the code in the app folder:

```
cd app
python main.py

```

Prepare for the Browser (recommend using Chrome)

* If you're using Google Chrome in Ubuntu on Windows Subsystem Linux.

Download and install Chrome (Linux):

```
sudo apt update && sudo apt -y upgrade && sudo apt -y autoremove
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt -y install ./google-chrome-stable_current_amd64.deb
```

Check that it's installed ok:

```
google-chrome --version
```

* Using Google Chrome in Mac or Windows

Just make sure you have installed Chrome broswer.

Pre-Order Data

- exclude.xls

A list of Chinese peoduct title which are not able to provide pre order service at the moment.

- namelist.xls

A list of keywords that are allow for pre order and a column of period indicator, keywords are usually are brand name or series name.

* period_template.xls

The template of the pre-order message in both Chinese and English.

Shopline API Reference

Products JSON

```
https://admin.shoplineapp.com/api/admin/v1/5f23e6c55680fc0012f13584/products?
```

You can add parameter:

`scope=search&type=product_sets` to access product sets.

`query=ts6` can be used as search and filter

`page=1` is used for the page number

`limit=1000` is used for the no. of items showing in the result

All right reserved, copyright @WillonLai :D
Email: prologic338@gmail.com
