__author__ = "Henry Richard J"
__license__ = "MIT License"
__maintainer__ = "Henry Richard"
from concurrent.futures import ThreadPoolExecutor
from msedge.selenium_tools import Edge, EdgeOptions
import exrex
import cfscrape
import requests
import PySimpleGUI as sg
from faker import Faker
from threading import Thread
from datetime import datetime

now = datetime.now()
date_time = now.strftime("Spotify Accounts Generated At [%m_%d_%Y %H_%M_%S]")



email_domain = "@henry-mail.ml"# Custom domain for emailfake.com using freenom

to_verify = []



def run1():
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(verify_account, account) for account in to_verify]
        executor.shutdown(wait=True)

def user_password_gen():
    fake = Faker()
    name = fake.name()
    user_name = exrex.getone("[a-z]{7}\d{2}")
    password = exrex.getone("[A-Z][a-z]{7}\d{2}")
    return user_name, password, name


def generateSpotifyAccount(start, stop):

     for i in range(start, stop):
         email = user_password_gen()[0]
         emails = email + email_domain
         passwords = user_password_gen()[1]
         DM_Name = user_password_gen()[2]

         url = "https://spclient.wg.spotify.com/signup/public/v1/account"
         post_data = f"gender=male&password={passwords}&password_repeat={passwords}&birth_month=8&birth_year=2000&creation_point=client_mobile&email={emails}&birth_day=1&displayname={DM_Name}&key=bff58e9698f40080ec4f9ad97a2f21e0&platform=iOS-ARM&creation_flow=mobile_email&iagree=1"
         headers = {

            "Host": "spclient.wg.spotify.com",
            "Content-Type": "application /x-www-form-urlencoded",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": "Spotify/8.5.7iOS/13.5.1(iPhone12, 8)",
            "Accept-Language": "fr, en;q = 0.01",
            "Content-Length": "283",
            "Accept-Encoding": "gzip,deflate,br"

        }

         result = requests.post(url, headers=headers, data=post_data).json()
         if result['status'] == 1:
           window['EMAIL_PASS_COMBO'].print(f"{emails}:{passwords}")
           window["Verification_Email"].print(f"https://emailfake.com/henry-mail.ml/{email}")
           to_verify.append(f"https://emailfake.com/henry-mail.ml/{email}")
           open(f"{date_time}.txt","a").write(f"{emails}:{passwords}\n")
         else:
             print(result['status'])

def verify_account(url):
 runner = cfscrape.create_scraper()
 options = EdgeOptions()
 options.use_chromium = True
 options.add_argument("disable-gpu")
 options.add_argument('headless')
 options.add_argument('ignore-certificate-errors')
 driver = Edge(options = options,executable_path=r"WebDriver\msedgedriver.exe")
 driver.get(url)

 link = driver.find_element_by_xpath(r"//a[@style='text-decoration: none; color: #1ed760']").get_attribute('href')
 driver.close()

 result = runner.get(url=link).text
 if "all set" in result:
     window["Verified_Email"].print(f"[*] Verification Completed")
 else:
     window["Verified_Email"].print(f"[*] {result}")





sg.theme("LightGreen3")
Layout = [[sg.Image(filename="Icons/spotify (1).png", size=(50, 50)),sg.Text("Spotify Account Generator",font=("",25))],
          [sg.Text("Developed by Henry Richard J",font=("",15))],
          [sg.Multiline("EMAIL:PASSWORD here",size=(45,25),disabled=True,key="EMAIL_PASS_COMBO"),
           sg.Multiline("Verification Email Link Here",size=(45,25),disabled=True,key="Verification_Email"),
           sg.Multiline("Verification Details here",size=(45,25),disabled=True,key="Verified_Email")],
          [sg.Text("Number of Accounts to generate:")],
          [sg.Slider(range=(1,100),default_value=5,size=(15,20),font=("",10),key="Number_OF_Accounts",tooltip="Use The Slider To Choose Number Of Accounts To Be Generated",orientation="horizontal")],
          [sg.Button("Generate Accounts",size=(20,2),font=("",15),key="Generate_Accounts"),sg.Button("Verify Accounts",size=(20,2),font=("",15),key="Verify_Accounts")]]
window = sg.Window('Spotify Account Generator' , Layout,element_justification='center')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Generate_Accounts":
        to_verify.clear()
        no_of_bins = int(values["Number_OF_Accounts"])
        window['EMAIL_PASS_COMBO'].update("")
        window["Verification_Email"].update("")

        for n in range(0, no_of_bins, int(no_of_bins/2)):
            stop = n + int(no_of_bins/2) if n + int(no_of_bins/2) <= no_of_bins else no_of_bins
            Thread(target=generateSpotifyAccount, args=(n, stop),daemon=True).start()
    if event == "Verify_Accounts":
        window["Verified_Email"].update("")
        Thread(target=run1).start()


window.close()
