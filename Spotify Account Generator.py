__author__ = "Henry Richard J"
__license__ = "MIT License"
__maintainer__ = "Henry Richard"

import exrex
import requests
import PySimpleGUI as sg
from faker import Faker

email_domain = "@henry-mail.ml"# Custom domain for emailfake.com using freenom


def user_password_gen():
    fake = Faker()
    name = fake.name()
    user_name = exrex.getone("[a-z]{7}\d{2}")
    password = exrex.getone("[A-Z][a-z]{7}\d{2}")
    return user_name, password, name


def generateSpotifyAccount():
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
        print(f"Email: {emails} Password: {passwords} to verify Account go to https://emailfake.com/henry-mail.ml/{email}")
        window['EMAIL_PASS_COMBO'].print(f"{emails}:{passwords}")
        window["Verification_Email"].print(f"https://emailfake.com/henry-mail.ml/{email}")
    else:
        sg.popup("Error","Please Try again after some time or use VPN")


sg.theme("DarkGreen5")
Layout = [[sg.Text("Spotify Account Generator",font=("",25))],
          [sg.Text("Developed by Henry Richard J",font=("",15))],
          [sg.Multiline("EMAIL:PASSWORD here",size=(45,25),disabled=True,key="EMAIL_PASS_COMBO"),sg.Multiline("Verification Email Link Here",size=(45,25),disabled=True,key="Verification_Email")],
          [sg.Text("Number of Accounts to generate:")],
          [sg.Slider(range=(1,10),default_value=2,size=(15,20),font=("",10),key="Number_OF_Accounts",tooltip="Use The Slider To Choose Number Of Accounts To Be Generated",orientation="horizontal")],
          [sg.Button("Generate Accounts",size=(20,2),font=("",15),key="Generate_Accounts")]]
window = sg.Window('Spotify Account Generator' , Layout,element_justification='center')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Generate_Accounts":
        no_of_bins = int(values["Number_OF_Accounts"])
        window['EMAIL_PASS_COMBO'].update("")
        window["Verification_Email"].update("")
        for i in range(no_of_bins):
         generateSpotifyAccount()

window.close()