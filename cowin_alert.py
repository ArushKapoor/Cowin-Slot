import email
import smtplib

import requests
from datetime import datetime

from requests.sessions import session


def create_session_info(center, session):
    return {"name": center["name"],
            "date": session["date"],
            "capacity": session["available_capacity"],
            "capacity_dose1": session["available_capacity_dose1"],
            "age_limit": session["min_age_limit"],
            "state_name": center["state_name"]
            }


def get_sessions(data):
    for center in data["centers"]:
        for session in center["sessions"]:
            yield create_session_info(center, session)


def is_available(session):
    return session["capacity"] > 0 and session["capacity_dose1"] > 1


def is_eighteen_plus(session):
    return session["age_limit"] == 18


def get_for_seven_days(start_date):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    params = {"district_id": 108, "date": start_date.strftime("%d-%m-%Y")}
    # params = {"district_id": 108, "date": start_date}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()
    return [session for session in get_sessions(data) if is_eighteen_plus(session) and is_available(session)]


def create_output(session_info):
    return f"Date - {session_info['date']}, Location - {session_info['name']}, Total Capacity - ({session_info['capacity']}), Dose 1 - ({session_info['capacity_dose1']})"


true_content = ""


def cowin():
    content = "\n".join([create_output(session_info)
                         for session_info in get_for_seven_days(datetime.today())])

    global true_content
    if not content or true_content == content:
        print("No Availability")
    else:
        print(content)
        # global true_content
        true_content = content
        # email_msg = email.message.EmailMessage()
        # email_msg["Subject"] = "Vaccination Slot Open"
        # email_msg["From"] = username
        # email_msg["To"] = ""
        #
        # email_msg.set_content(content)

        # with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
        #     server.starttls()
        #     server.login(username, password)
        #     server.send_message(email_msg, username, "")
        url = "https://api.telegram.org/bot1839240494:AAHbMrnu8bzHjyrcuTECGWYc8ynJgpFRl90/sendMessage?chat_id=-523418255&text={}".format(
            content)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        requests.get(url, headers=headers)


# def get_district_id():
#     for state_id in range(1, 100):
#         url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(
#             state_id)
#         params = {"district_id": state_id, "date": "21-05-2021"}
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
#         resp = requests.get(url, params, headers=headers)
#         data = resp.json()
#         districts = data["districts"]
#         for district in districts:
#             if district["district_name"] == "Chandigarh":
#                 print(district["district_id"])
#                 print(district["district_name"])
#     return None


# get_district_id()
