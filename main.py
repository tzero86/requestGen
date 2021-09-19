import json
import requests
from tkinter import *
from functools import partial

# we create the window
root = Tk()
root.title('reqGen')
root.call('wm', 'iconphoto', root._w, PhotoImage(file='reqGen_icon.png'))

# Program title and instruction label
welcome_text = StringVar()
welcome_text.set(""
                 "Select the desired options to generate a saveHousehold Request ready to be copied into Postman. You can also specify in the ENV.json file if you want to automatically send the request to get your household ID back.")
title = Message(root, textvariable=welcome_text, width=1200).pack(side=TOP, padx=5, pady=15)

# the different frames (like divs)
frame = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root, width=50, height=5)
frame4 = Frame(root, width=50, height=5)
frame.pack()
frame2.pack()
frame3.pack()
frame4.pack()

# footer text
footer_text = StringVar()
footer_text.set(".:: .._ _.. ::.")
title = Message(root, textvariable=footer_text, width=1200).pack(side=TOP, padx=5, pady=15)


# Year selector
years = ['2021', '2022']
def_year = StringVar(frame)
def_year.set(years[0])
plan_year = OptionMenu(frame, def_year, *years)
year_selection_label = Label(frame, text="Plan Year:").pack(side=LEFT, padx=5, pady=15)
plan_year.pack(side=LEFT, padx=5, pady=15)

# Plan Types
plan_types = ["APTC", "QHP", "QDP"]
def_plan_type = StringVar(frame)
def_plan_type.set("APTC")
plan_type_selection_label = Label(frame, text="Plan Type:").pack(side=LEFT, padx=5, pady=15)
plan_type = OptionMenu(frame, def_plan_type, *plan_types).pack(side=LEFT, padx=5, pady=15)


# Usange indicator
indicators = ["Low", "Medium", "High", "Very High"]
def_usage_med = StringVar(frame)
def_usage_med.set("Medium")
usage_med_label = Label(frame, text="Medical Usage:").pack(side=LEFT, padx=5, pady=15)
usage_medical = OptionMenu(frame, def_usage_med, *indicators).pack(side=LEFT, padx=5, pady=15)

# Prescription Usange indicator
def_presc_usage = StringVar(frame)
def_presc_usage.set("Medium")
presc_usage_med_label = Label(frame, text="Prescription Usage:").pack(side=LEFT, padx=5, pady=15)
usage_presc = OptionMenu(frame, def_presc_usage, *indicators).pack(side=LEFT, padx=5, pady=15)

# Zip code, num of members, coverage months
def_zip = StringVar()
def_zip.set("98178")
zip_code = Label(frame2, text="ZipCode:").pack(side=LEFT, padx=15, pady=15)
zip_code_input_area = Entry(frame2,textvariable=def_zip, width=10).pack(side=LEFT, padx=15, pady=15)

# members
def_members = StringVar()
def_members.set("1")
num_members = Label(frame2, text="Members:").pack(side=LEFT, padx=15, pady=15)
num_members_input_area = Entry(frame2, textvariable=def_members, width=10).pack(side=LEFT, padx=15, pady=15)

# coverage months left
def_months = StringVar()
def_months.set("6.5")
coverage_months = Label(frame2, text="Coverage Months:").pack(side=LEFT, padx=15, pady=15)
coverage_months_input_area = Entry(frame2, textvariable=def_months, width=10).pack(side=LEFT, padx=15, pady=15)

# generated request text area and label
req_gen_label = Label(frame3, text="Request Generated:").pack(side=LEFT, padx=15, pady=15)
req_gen_input_area = Text(frame3, bg='#57CC99', fg='#112031', width=70, height=10, relief=FLAT)
req_gen_input_area.pack(side=LEFT, padx=15, pady=15)

# generated API response text area and label
api_resp_label = Label(frame4, text="Response Generated:").pack(side=LEFT, padx=10, pady=15)
api_resp_input_area = Text(frame4, bg='#80ED99', fg='#112031', width=70, height=10, relief=FLAT)
api_resp_input_area.pack(side=LEFT, padx=15, pady=15)


# Load ENV settings from the file
file = open('ENV.json', )
env_cfg = json.load(file)

# the main dictionary for the plans, this is the data to be replaced with the actual plans.
# for both APTC and QHP and for 2021 AND 2022 (we'll have to add QDP support).
# TODO: Need to replace this with useful data...
plans = {

    "2021": {
        "QHP": [
            {"hiosId": "25210CA010001501", "netPremium": "336.21"},
            {"hiosId": "25210CA011001601", "netPremium": "426.48"},
            {"hiosId": "25210CA007001201", "netPremium": "350.00"},
            {"hiosId": "25210CA006001101", "netPremium": "299.00"},
            {"hiosId": "25210CA005001001", "netPremium": "248.00"},
            {"hiosId": "25210CA009001401", "netPremium": "272.00"},
            {"hiosId": "25210CA008001301", "netPremium": "221.00"},
            {"hiosId": "25210CA011001601", "netPremium": "426.48"},
            {"hiosId": "25210CA012001701", "netPremium": "516.75"},
            {"hiosId": "25210CA012001701", "netPremium": "516.75"}
        ],
        "APTC": [
            {"hiosId": "APTC21CA54786", "netPremium": 40.69},
            {"hiosId": "APTC21CA54786", "netPremium": 530.46},
            {"hiosId": "APTC21CA54786", "netPremium": 40.69},
            {"hiosId": "APTC21CA54786", "netPremium": 530.46}
        ],
    },
    "2022": {
        "QHP": [
            {"hiosId": "QHP228CA54786", "netPremium": 40.69},
            {"hiosId": "QHP228CA54786", "netPremium": 530.46},
            {"hiosId": "QHP228CA54786", "netPremium": 40.69},
            {"hiosId": "QHP228CA54786", "netPremium": 530.46}
        ],
        "APTC": [
            {"hiosId": "APTC22CA54786", "netPremium": 40.69},
            {"hiosId": "APTC22CA54786", "netPremium": 530.46},
            {"hiosId": "APTC22CA54786", "netPremium": 40.69},
            {"hiosId": "APTC22CA54786", "netPremium": 530.46}
        ],
    }
}


# the main function, gets the parameters and spits out a JSON to be used in postman
def generate_save_req(year, zip, members, months, usage, type):
    # We create our object with the request fields we need
    request_cfg = {
        "coverageMonths": float(months),
        "coverageYear": int(year),
        "zipCode": int(zip),
        "noOfMembers": int(members),
        "medicalUse": usage[0],
        "prescriptionUse": usage[1],
        "plans": [
        ]
    }
    # if program type is QHP or APTC we proceed.
    if type in ["QHP", "QDP", "APTC"]:
        # for each plan stored for the YEAR and Plan Type, we append that plan to the plans array in request_cfg
        for plan in plans[str(year)][str(type)]:
            request_cfg["plans"].append(plan)
    # we parse the dictionary into a JSON object and print it out, we can direct the same to a file on the disk.
    req_final = json.dumps(request_cfg, indent=4, sort_keys=False)
    print(req_final)
    if env_cfg["sendSaveReq"]:
        send_post_request(req_final)
    req_gen_input_area.delete(1.0, END)
    req_gen_input_area.insert(END, req_final)


def send_post_request(save_household_req):
    print(f'[API POST Request -> SavehouseholdId Endpoint]: Sending request to the endpoint...')
    headers = {
        "Content-Type": "application/json",
        "Authority": env_cfg['Authority'],
        "Host": env_cfg['Host'],
        "Accept": "/",
        "Accept-Encoding": "gzip, deflate, br"
    }
    req = requests.post(url=env_cfg['ENDPOINT'], data=save_household_req, headers=headers)
    print(f'[API Response -> HouseholdId Generated]: {req.text}')
    api_resp_input_area.delete(1.0, END)
    api_resp_input_area.insert(END, req.text)


# function to handle generate button click event
def ui_generate():
    generate_save_req(def_year.get(), def_zip.get(), def_members.get(), def_months.get(), [def_usage_med.get(), def_presc_usage.get()], def_plan_type.get())


# Generate request button
gen_save_request = Button(frame2, text="Generate", command=partial(ui_generate), bg="#57CC99", fg='#112031', relief=FLAT).pack(side=LEFT, padx=15, pady=15)

root.mainloop()

# Examples to generate some saveHousehold request.

# Parameters: year, zip, members, months, usage, type
# generate_save_req(2021, 98178, 2, 1.5, ["Low", "Medium"], "QHP")
# generateSaveReq(2021, 98203, 9, 7.3, ["High", "Low"], "APTC")
# generateSaveReq(2022, 92251, 7, 10.5, ["low", "Very High"], "QHP")
# generateSaveReq(2022, 98001, 5, 6.5, ["Very High", "Low"], "APTC")