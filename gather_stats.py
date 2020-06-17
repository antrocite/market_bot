
from selenium import webdriver
from pathlib import Path
from time import sleep, localtime
from re import search
from statistics import mean
import xlwt
import xlrd
from xlutils.copy import copy
from selenium.webdriver.common.keys import Keys

login_data = {
    'username' : '---',
    'password' : '---'
}

path = Path(__file__).parent.absolute()
path = str(path)

driver_path = path + '/chromedriver'

STATS_FILE_PATH = path + '/price_stats_new.xlsx'

PATH_TABLE = """/html/body/center/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody"""               
PATH_PRICE = """.//table/tbody/tr/td[1]/div/table/tbody/tr/td[2]"""
PATH_BUY = """.//td[5]/form/div/a"""
PATH_BUY_CONFIRM = """.//td[5]/form/div/input[2]"""
PATH_AMOUNT = """.//td[1]/table/tbody/tr/td[2]/b[2]"""
PATH_BUY_AMOUNT = """.//td[5]/form/div/input[1]"""
PATH_RETURN = """/html/body/center/table/tbody/tr/td/table/tbody/tr/td/a[1]"""

elements = {
    "Abrasive" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=abrasive&sbn=1&sau=0",
                 "buy_price" : "970",
                 "sell_price" : "1039"
    },
    "Viper venom" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=snake_poison&sbn=1&sau=0",
                     "buy_price" : "110",
                     "sell_price" : "139"
    },
    "Tiger`s claw" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=tiger_tusk&sbn=1&sau=0",
                     "buy_price" : "870",
                     "sell_price" : "959"
    },
    "Ice crystal" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=ice_crystal&sbn=1&sau=0",
                    "buy_price" : "1650",
                    "sell_price" : "1729"
    },
    "Moonstone" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=moon_stone&sbn=1&sau=0",
                  "buy_price" : "2470",
                  "sell_price" : "2549"
    },
    "Fire crystal" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=fire_crystal&sbn=1&sau=0",
                     "buy_price" : "1370",
                     "sell_price" : "1489"
    },
    "Meteorite shard" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=meteorit&sbn=1&sau=0",
                        "buy_price" : "2470",
                        "sell_price" : "2539"
    },
    "Witch bloom" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=witch_flower&sbn=1&sau=0",
                    "buy_price" : "110",
                    "sell_price" : "139"
    },
    "Windflower" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=wind_flower&sbn=1&sau=0",
                   "buy_price" : "2550",
                   "sell_price" : "2729"
    },
    "Fern flower" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=fern_flower&sbn=1&sau=0",
                    "buy_price" : "110",
                    "sell_price" : "139"
    },
    "Toadstool" :{"link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=badgrib&sbn=1&sau=0",
                  "buy_price" : "150",
                  "sell_price" : "199"
    }
}

def login(driver):
    print('Authentification')
    driver.get('https://www.lordswm.com')

    select = driver.find_element_by_name('login')
    select.send_keys(login_data['username'])

    id_box = driver.find_element_by_name('pass')
    id_box.send_keys(login_data['password'])

    driver.find_element_by_class_name('entergame').click()

    login_error = 'Неверное имя пользователя или пароль.'
    need_captcha_error = 'Введен неверный код с картинки'
    if login_error in driver.page_source:
        print(login_error)
        exit()
    elif need_captcha_error in driver.page_source:
        print(need_captcha_error + '(Много неудачных попыток). Войдите в игру и перезапустите бота.')
        exit()

def inspect(driver, dict_ele):
    prices = []

    driver.get(dict_ele['link']) 
    lot_table = driver.find_element_by_xpath(PATH_TABLE)
    lots_ele = lot_table.find_elements_by_class_name("wb")

    if len(lots_ele) <= 5:
        return

    for lot_ele in lots_ele[0:5]:          
        price_ele = lot_ele.find_element_by_xpath(PATH_PRICE)
        price = int(price_ele.text.replace(',', ''))
        prices.append(price)

    avg = mean(prices)
    return avg

def reload_stats(sheet):   
    old_wb = xlrd.open_workbook(STATS_FILE_PATH)
    old_sheet = old_wb.sheet_by_index(0)
    
    for row in range(old_sheet.nrows):
        for col in range(old_sheet.ncols):
            sheet.write(row, col, old_sheet.cell_value(row, col))

    return (old_sheet.nrows)

def write_stats(sheet, mean_prices, row): 
    loc_time = localtime()
    time = loc_time[3:5]
    time = str(time)

    sheet.write(row, 0, time)

    print(mean_prices)
    i = 0
    while i < 11:
        sheet.write(row, i+1, mean_prices[i])
        i += 1

def main():
    wb = xlwt.Workbook()  
    sheet = wb.add_sheet('Sheet 1') 
    row = reload_stats(sheet)

    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path = driver_path)

    login(driver)

    prices = []
    for key in elements.keys():
        prices_of_ele = []
        prices.append(prices_of_ele)
    mean_prices = []
    i = 0 
    while True:
        j = 0
        for key in elements.keys():
            price = inspect(driver, elements[key])
            prices[j].append(price)
            j += 1

        if i == 11:
            for k in range(11):
                mean_prices.append(mean(prices[k]))

            write_stats(sheet, mean_prices, row)
            wb.save(STATS_FILE_PATH)
            row += 1

            mean_prices = []
            for k in range(11):
                prices[k] = []
                k += 1
            i = 0

        i += 1
        sleep(293)

    wb.close()

   
if __name__ == "__main__":
    main()






