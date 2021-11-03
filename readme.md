from urllib import request
from bs4 import BeautifulSoup
from re import search

def check_profile_command():
    while(True):
        page = request.urlopen("https://docs.saltproject.io/en/latest/ref/states/all/salt.states.file.html")
        page_content = page.read()
        page.close()
        soup = BeautifulSoup(page_content, "html.parser")
        command = search("{.}", soup.body.div.text)
        if(command[1] == 0):
            print("Found command to stop")
            sleep(10*60)
        else:
            print("Allowed to start")
            break

check_profile_command()
