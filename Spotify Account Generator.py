__author__ = "Henry Richard J"
__license__ = "MIT License"
__maintainer__ = "Henry Richard"

import exrex
import requests
import PySimpleGUI as sg
from faker import Faker
from threading import Thread
from datetime import datetime

now = datetime.now()
date_time = now.strftime("Spotify Accounts Generated At [%m_%d_%Y %H_%M_%S]")

to_verify = []


def user_password_gen():
    fake = Faker()
    name = fake.name()
    user_name = exrex.getone("[a-z]{7}\d{2}")
    password = exrex.getone("[A-Z][a-z]{7}\d{2}")
    return user_name, password, name


def generateSpotifyAccount(start, stop, email_domain):
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
            "Accept-Encoding": "gzip,deflate,br",
        }

        result = requests.post(url, headers=headers, data=post_data).json()
        if result["status"] == 1:
            window["EMAIL_PASS_COMBO"].print(f"{emails}:{passwords}")
            open(f"Accounts/{date_time}.txt", "a").write(f"{emails}:{passwords}\n")
        else:
            print(result["status"])


sg.theme("LightGreen3")
Layout = [
    [
        sg.Image(filename="Icons/spotify (1).png", size=(50, 50)),
        sg.Text("Spotify Account Generator", font=("", 25)),
    ],
    [sg.Text("Developed by Henry Richard J", font=("", 15))],
    [
        sg.Text("Email Domain"),
        sg.InputText(key="--DOMAIN-NAME", size=(35, 1), do_not_clear=True),
    ],
    [
        sg.Multiline(
            "EMAIL:PASSWORD here", size=(45, 25), disabled=True, key="EMAIL_PASS_COMBO"
        ),
    ],
    [sg.Text("Number of Accounts to generate:")],
    [
        sg.Slider(
            range=(1, 100),
            default_value=5,
            size=(15, 20),
            font=("", 10),
            key="Number_OF_Accounts",
            tooltip="Use The Slider To Choose Number Of Accounts To Be Generated",
            orientation="horizontal",
        )
    ],
    [
        sg.Button(
            "Generate Accounts", size=(20, 2), font=("", 15), key="Generate_Accounts"
        ),
    ],
]
window = sg.Window("Spotify Account Generator", Layout, element_justification="center")

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Generate_Accounts":
        to_verify.clear()
        no_of_accounts = int(values["Number_OF_Accounts"])
        domain_name = values["--DOMAIN-NAME"]
        window["EMAIL_PASS_COMBO"].update("")

        for n in range(0, no_of_accounts, int(no_of_accounts / 2)):
            stop = (
                n + int(no_of_accounts / 2)
                if n + int(no_of_accounts / 2) <= no_of_accounts
                else no_of_accounts
            )
            if domain_name != "":
                Thread(
                    target=generateSpotifyAccount,
                    args=(n, stop, domain_name),
                    daemon=True,
                ).start()
            else:
                sg.popup("Please Enter A Valid Domain Name")
                break

window.close()
