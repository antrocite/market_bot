
from selenium import webdriver
import PySimpleGUI as gui

from pathlib import Path
from time import sleep, localtime
from re import search
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException
from statistics import mean

path = Path(__file__).parent.absolute()
path = str(path)

driver_path = path + '/chromedriver'

PATH_TABLE = """/html/body/center/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody"""               
PATH_PRICE = """.//table/tbody/tr/td[1]/div/table/tbody/tr/td[2]"""
PATH_BUY = """.//td[5]/form/div/a"""
PATH_BUY_CONFIRM = """.//td[5]/form/div/input[2]"""
PATH_AMOUNT = """.//td[1]/table/tbody/tr/td[2]/b[2]"""
PATH_BUY_AMOUNT = """.//td[5]/form/div/input[1]"""
PATH_RETURN = """/html/body/center/table/tbody/tr/td/table/tbody/tr/td/a[1]"""

BUY_RATIO = 0.93

elements = {
    "abrasive" :{"name" : "Abrasive",
                 "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=abrasive&sbn=1&sau=0",
                 "buy_price" : 940,
                 "sell_price" : 1089
    },
    "snake_poison" :{"name" : "Viper venom",
                     "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=snake_poison&sbn=1&sau=0",
                     "buy_price" : 120,
                     "sell_price" : 149
    },
    "tiger_tusk" :{"name" : "Tiger`s claw",
                   "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=tiger_tusk&sbn=1&sau=0",
                   "buy_price" : 880,
                   "sell_price" : 979
    },
    "ice_crystal" :{"name" : "Ice crystal",
                    "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=ice_crystal&sbn=1&sau=0",
                    "buy_price" : 1640,
                    "sell_price" : 1739
    },
    "moon_stone" :{"name" : "Moonstone",
                   "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=moon_stone&sbn=1&sau=0",
                   "buy_price" : 2440,
                   "sell_price" : 2539
    },
    "fire_crystal" :{"name" : "Fire crystal",
                     "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=fire_crystal&sbn=1&sau=0",
                     "buy_price" : 1340,
                     "sell_price" : 1479
    },
    "meteorit" :{"name" : "Meteorite shard",
                 "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=meteorit&sbn=1&sau=0",
                 "buy_price" : 2560,
                 "sell_price" : 2729
    },
    "witch_flower" :{"name" : "Witch bloom",
                     "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=witch_flower&sbn=1&sau=0",
                     "buy_price" : 120,
                     "sell_price" : 139
    },
    "wind_flower" :{"name" : "Windflower",
                    "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=wind_flower&sbn=1&sau=0",
                    "buy_price" : 2700,
                    "sell_price" : 2859
    },
    "fern_flower" :{"name" : "Fern flower",
                    "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=fern_flower&sbn=1&sau=0",
                    "buy_price" : 120,
                    "sell_price" : 139
    },
    "badgrib" :{"name" : "Toadstool",
                "link" : "https://www.lordswm.com/auction.php?cat=elements&sort=4&type=0&art_type=badgrib&sbn=1&sau=0",
                "buy_price" : 170,
                "sell_price" : 212
    }
}

class GUI():
    def __init__(self):
        self.form = gui.Window('Стартуем!')

        self.layout = [
            [gui.Text('Введите имя пользователя и по роль')],
            [gui.Text('Имя пользователя', size=(18, 1)), gui.InputText(key = 'username')],
            [gui.Text('По роль', size=(18, 1)), gui.Input(key='password', password_char = '*')],
            [gui.Checkbox('Запомнить меня', key = 'IsRemember')],
            [gui.Text('Или :')],
            [gui.Checkbox('Использовать сохранные данные', key = 'UseSaved')],
            [gui.Submit(), gui.Button('Все, кончай!')],
        ]

        self.button, self.values = self.form.Layout(self.layout).Read()

        if self.button is 'Все, кончай!' or self.button is 'None':
                exit()

    def obtain_values(self):
        if(self.values['UseSaved'] is True):
            login_path = path + '/login.txt'
            try:
                with open(login_path) as login_file:
                    temp = login_file.read().splitlines()
                    self.values['username'] = temp[0]
                    self.values['password'] = temp[1]
            except:
                gui.popup('Что-то не то с сохраненными данными\nВведите данные мануально')
                self.button, self.values = self.form.Read()

            if self.button is 'Cancel' or self.button is 'None':
                exit()
        elif(self.values['IsRemember'] is True):
            save_login(self.values)

        return(self.values)

    def close(self):
        self.form.close() 

def save_login(values):
    login_path = path + "/login.txt"
    with open(login_path, 'w') as login_file:
        for value in values.values():
            login_file.write('{}\n'.format(value))

def login(driver, login_data):
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
    driver.get(dict_ele['link']) 
    lot_table = driver.find_element_by_xpath(PATH_TABLE)
    lots_ele = lot_table.find_elements_by_class_name("wb")

    if len(lots_ele) > 0:
        lot_ele = lots_ele[0]
    else:
        return
           
    price_ele = lot_ele.find_element_by_xpath(PATH_PRICE)
    price = int(price_ele.text.replace(',', ''))

    if dict_ele['sell_price'] < 300:
        BUY_RATIO = 0.8
    elif dict_ele['sell_price'] < 1200:
        BUY_RATIO = 0.9
    elif dict_ele['sell_price'] < 2000:
        BUY_RATIO = 0.94
    else:
        BUY_RATIO = 0.96
    
    if(price <= (dict_ele['sell_price'] * BUY_RATIO)):
        buy(driver, lot_ele, dict_ele['name'], price)
        return

def buy(driver, lot_ele, name, price):
    amount_ele = lot_ele.find_element_by_xpath(PATH_AMOUNT)
    amount = amount_ele.text
    amount = search('\d+|$', amount).group()

    print('Trying to buy', str(amount), 'piece(s) of', name, 'for', price)
    lot_ele.find_element_by_xpath(PATH_BUY).click()
    if amount is not '1':
        lot_ele.find_element_by_xpath(PATH_BUY_AMOUNT).send_keys(amount)
    lot_ele.find_element_by_xpath(PATH_BUY_CONFIRM).click()

    text_ele = driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td/table/tbody/tr/td/center")
    print(text_ele.text)

def sell(driver, dict_ele, amount):
    selling_price = get_selling_price(driver, dict_ele)

    driver.get("https://www.lordswm.com/auction_new_lot.php")

    select_ele = driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td/table/tbody/tr/td/form/select[1]")
    options = select_ele.find_elements_by_tag_name('option')
    for option in options:
        text = option.text.split(' ')
        if len(text) == 3:
            name = text[0] + ' ' + text[1]
        else:
            name = text[0]

        if dict_ele['name'] == name:
            option.click()
            break

    driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td/table/tbody/tr/td/form/input[1]").send_keys(Keys.BACK_SPACE, amount)
    driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td/table/tbody/tr/td/form/input[2]").send_keys(Keys.BACK_SPACE, selling_price)

    select_ele = driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td/table/tbody/tr/td/form/select[3]")
    options = select_ele.find_elements_by_tag_name('option')
    options[2].click()

    driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td/table/tbody/tr/td/form/input[4]").click()
    driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td/table/tbody/tr/td/form/table[2]/tbody/tr/td[1]/input").click()
    sleep(2)
    
    alert = driver.switch_to.alert
    alert.accept()

    print('selling', amount, 'piece(s) of', dict_ele['name'], 'for', selling_price)

def get_selling_price(driver, dict_ele):
    prices = []
    driver.get(dict_ele['link'])

    i = 0
    k = 3
    while i < 4:
        xpath = "/html/body/center/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr[" + str(k) + "]"
        try:
            lot_ele = driver.find_element_by_xpath(xpath)
        except:
            return dict_ele['sell_price']

        price_ele = lot_ele.find_element_by_xpath(PATH_PRICE)
        price = int(price_ele.text.replace(',', ''))

        prices.append(price)

        i += 1
        k += 1

    mean_price = mean(prices) - dict_ele['sell_price'] * 0.01
    
    if mean_price < dict_ele['sell_price']:
        final_price = dict_ele['sell_price']    
    else:
        final_price = mean_price
    print('mean price is', mean_price, 'sell price', dict_ele['sell_price'])
    return int(final_price)

def check_inv(driver, available_places):
    driver.get("https://www.lordswm.com/pl_info.php?id=6648316")

    stocks = driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td/table[2]/tbody/tr[2]/td[1]").text.split('\n')
    i = 0
    while i < len(stocks):
        stocks[i] = stocks[i].strip()
        i += 1

    for stock in stocks:
        if available_places > 0:
            stock_info = stock.split(':')
            if len(stock_info) != 1:
                stock_info[0].strip()
                stock_info[1] = int(stock_info[1].strip())
                for key in elements.keys():  
                    if elements[key]['name'] == stock_info[0] and stock_info[1] >= 5:
                        if stock_info[1] > 10:
                            stock_info[1] = 10
                        sell(driver, elements[key], stock_info[1])
                        available_places -= 1
                        break
        else:
            break
                
def check_lots(driver):
    driver.get("https://www.lordswm.com/auction.php?cat=my&sort=0")

    lot_table = driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody")
    lots = lot_table.find_elements_by_class_name("wb")
    return(3 - len(lots))

def main():
    i = 0

    win = GUI()
    login_data = win.obtain_values()
    win.close()

    #chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path = driver_path)
    login(driver, login_data)

    while True:
        try:
            if i % 40 == 0:
                available_places = check_lots(driver)
                if(available_places) != 0:
                    check_inv(driver, available_places)
                i = 0

            for key in elements.keys():
                inspect(driver, elements[key])

            i += 1  
        except NoAlertPresentException:
            print('NO ALERT ERROR OCCURED')
            driver.quit()
            driver = webdriver.Chrome(executable_path = driver_path)
            login(driver, login_data)
            continue
        except:
            print('ERROR OCCURED')
            driver.quit()
            sleep(300)
            driver = webdriver.Chrome(executable_path = driver_path)
            login(driver, login_data)
            continue
    

if __name__ == "__main__":
    main()
 

    






