#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Elias Medina (@tzero86)
# Created Date: 09-18-2021
# version ='0.1'
# ---------------------------------------------------------------------------
""" Simple data generation tool for the testing team, this is to facilitate the creation of
household IDs for testing purposes"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import json
import os
import traceback
from tkinter import messagebox
import requests
from tkinter import *
from functools import partial
import sys

# ---------------------------------------------------------------------------
# Defaults  (TODO: Maybe it is best to move this to the config file.)
# ---------------------------------------------------------------------------

# Load ENV settings from the file (This feeds several parts of the script)
try:
    file = open('cfg.json', )
    env_cfg = json.load(file)
except Exception:
    error_message = str(traceback.format_exc())
    messagebox.showerror("Something broke while loading cfg.json ¯\_(ツ)_/¯", detail=error_message)

# Color Theme options
background_color = '#181b28'
font_color = '#a8b5c2'

# default program types
program_types = list(env_cfg["plans"]["2021"].keys())

# Default usage indicator values
indicators = list(env_cfg["usageIndicatorValues"])

# default supported years
years = list(env_cfg["plans"].keys())

# the main dictionary for the plans, this is the data to be replaced with the actual plans.
# for both APTC and QHP and for 2021 AND 2022 (we'll have to add QDP support).
# TODO: Need to replace this with useful data...
plans = env_cfg['plans']


# ---------------------------------------------------------------------------
# Here starts the UI drama.
# ---------------------------------------------------------------------------


# OS agnostic dir fix, just a helper function.
def get_dir(src):
    dir = sys.argv[0]
    dir = dir.split('/')
    dir.pop(-1)
    dir = '/'.join(dir)
    dir = dir + '/' + src
    return dir


# we create the window
root = Tk()
root.title('QA Mini Tool: reqGen for CDST SKU')
# root.call('wm', 'iconphoto', root._w, PhotoImage(file=get_dir('reqGen_icon.png')))
root.configure(bg=background_color, padx=10, pady=10)

# the different frames (like divs)
frame = Frame(root, bg=background_color)
frame2 = Frame(root, bg=background_color)
frame3 = Frame(root, width=50, height=5, bg=background_color)
frame4 = Frame(root, width=50, height=5, bg=background_color, pady=10)
frame5 = Frame(root, width=50, height=5, bg=background_color, pady=10)
frame5.pack()
frame.pack()
frame2.pack()
frame3.pack()
frame4.pack()

# Program title and instruction label
logo_text = StringVar()
logo_text.set("reqGen")
logo_control = Message(frame5, textvariable=logo_text, fg=font_color, bg=background_color, width=300)
logo_control.config(font=("Arial", 30))
logo_control.pack(side=LEFT, anchor=SW)
welcome_text = StringVar()
welcome_text.set(""
                 "Select the desired options to generate a saveHousehold Request ready to be copied into Postman. You "
                 "can also specify in the cfg.json file if you want to automatically send the request to the API and "
                 " get a household ID back. By default the requests are generated for anonymous users, select a specific user "
                 "from the list if you want to generate registerd user ids. Plans can be added into cfg.json for with "
                 "any key name. ")
title = Message(frame5, textvariable=welcome_text, fg=font_color, bg=background_color, width=800). \
    pack(side=LEFT, anchor=NW)

# footer text
footer_text = StringVar()
footer_text.set(".:: .._ _.. ::.")
footer_msg = Message(root, textvariable=footer_text, width=1200, fg=font_color, bg=background_color). \
    pack(side=TOP, padx=5, pady=15)

# Year selector
def_year = StringVar(frame)
def_year.set(years[0])
plan_year = OptionMenu(frame, def_year, *years)
plan_year.config(fg=font_color, bg=background_color)
year_selection_label = Label(frame, text="Plan Year:", fg=font_color, bg=background_color). \
    pack(side=LEFT, padx=5, pady=15)
plan_year.pack(side=LEFT, padx=5, pady=15)

# Plan Types
plan_types = program_types
def_plan_type = StringVar(frame)
def_plan_type.set("APTC")
plan_type_selection_label = Label(frame, text="Plan Type:", fg=font_color, bg=background_color). \
    pack(side=LEFT, padx=5, pady=15)
plan_type = OptionMenu(frame, def_plan_type, *plan_types)
plan_type.config(fg=font_color, bg=background_color)
plan_type.pack(side=LEFT, padx=5, pady=15)

# Medical Usage indicator
def_usage_med = StringVar(frame)
def_usage_med.set("Medium")
usage_med_label = Label(frame, text="Medical Usage:", fg=font_color, bg=background_color). \
    pack(side=LEFT, padx=5, pady=15)
usage_medical = OptionMenu(frame, def_usage_med, *indicators)
usage_medical.config(fg=font_color, bg=background_color)
usage_medical.pack(side=LEFT, padx=5, pady=15)

# Prescription Usage indicator
def_presc_usage = StringVar(frame)
def_presc_usage.set("Medium")
presc_usage_med_label = Label(frame, text="Prescription Usage:", fg=font_color, bg=background_color). \
    pack(side=LEFT, padx=5, pady=15)
usage_presc = OptionMenu(frame, def_presc_usage, *indicators)
usage_presc.config(fg=font_color, bg=background_color)
usage_presc.pack(side=LEFT, padx=5, pady=15)

# Username selection
username_selection = StringVar(frame2)
username_selection.set(env_cfg["users"][0])
username_selection_label = Label(frame2, text="Username:", fg=font_color, bg=background_color). \
    pack(side=LEFT, padx=5, pady=15)
username_dropdown = OptionMenu(frame2, username_selection, *env_cfg["users"])
username_dropdown.config(fg=font_color, bg=background_color)
username_dropdown.pack(side=LEFT, padx=5, pady=15)

# Zip code, num of members, coverage months
def_zip = StringVar()
def_zip.set("98178")
zip_code = Label(frame2, text="ZipCode:", fg=font_color, bg=background_color).pack(side=LEFT, padx=15, pady=15)
zip_code_input_area = Entry(frame2, textvariable=def_zip, width=10)
zip_code_input_area.config(fg=font_color, bg=background_color)
zip_code_input_area.pack(side=LEFT, padx=15, pady=15)

# members
def_members = StringVar()
def_members.set("1")
num_members = Label(frame2, text="Members:", fg=font_color, bg=background_color).pack(side=LEFT, padx=15, pady=15)
num_members_input_area = Entry(frame2, textvariable=def_members, width=10)
num_members_input_area.config(fg=font_color, bg=background_color)
num_members_input_area.pack(side=LEFT, padx=15, pady=15)

# coverage months left
def_months = StringVar()
def_months.set("6.5")
coverage_months = Label(frame2, text="Coverage Months:", fg=font_color, bg=background_color). \
    pack(side=LEFT, padx=15, pady=15)
coverage_months_input_area = Entry(frame2, textvariable=def_months, width=10)
coverage_months_input_area.config(fg=font_color, bg=background_color)
coverage_months_input_area.pack(side=LEFT, padx=15, pady=15)

# generated request text area and label and copy text button
def copy_clipboard(control):
    root.clipboard_clear()
    root.clipboard_append(control.get("1.0", END))


req_scrollbar = Scrollbar(frame3)
req_scrollbar.pack(side=RIGHT, fill=Y)
req_gen_label = Label(frame3, text="Request Generated:", fg=font_color, bg=background_color). \
    pack(side=LEFT, padx=15, pady=15)
req_gen_input_area = Text(frame3, bg='#57CC99', fg='#112031', width=70, height=10, relief=FLAT,
                          yscrollcommand=req_scrollbar.set)
req_gen_input_area.pack(side=LEFT, padx=15, pady=15)
req_scrollbar.config(command=req_gen_input_area.yview)

copy_req_to_clipboard = Button(frame3, text="Copy", command=partial(copy_clipboard, req_gen_input_area), bg="#57CC99", fg='#112031',
                          relief=FLAT).pack(side=LEFT, padx=15, pady=15)

# generated API response text area and label
resp_scrollbar = Scrollbar(frame4)
resp_scrollbar.pack(side=RIGHT, fill=Y)
api_resp_label = Label(frame4, text="Response Generated:", fg=font_color, bg=background_color). \
    pack(side=LEFT, padx=10, pady=15)
api_resp_input_area = Text(frame4, bg='#80ED99', fg='#112031', width=70, height=10, relief=FLAT)
api_resp_input_area.pack(side=LEFT, padx=15, pady=15)
resp_scrollbar.config(command=api_resp_input_area.yview)
copy_res_to_clipboard = Button(frame4, text="Copy", command=partial(copy_clipboard, api_resp_input_area), bg='#80ED99', fg='#112031',
                          relief=FLAT).pack(side=LEFT, padx=15, pady=15)


# ---------------------------------------------------------------------------
# Main "Logic" to generate the custom request
# ---------------------------------------------------------------------------


# the main function, gets the parameters and spits out a JSON to be used in postman
def generate_save_req(year, zip, members, months, usage, type, username):
    # We create our object with the request fields we need
    request_cfg = {
        "coverageMonths": float(months),
        "coverageYear": int(year),
        "zipCode": int(zip),
        "noOfMembers": int(members),
        "medicalUse": usage[0],
        "prescriptionUse": usage[1],
        "userName": username,
        "plans": [
        ]
    }
    # if program type is QHP or APTC we proceed.
    if type in program_types:
        # for each plan stored for the YEAR and Plan Type, we append that plan to the plans array in request_cfg
        for plan in plans[str(year)][str(type)]:
            request_cfg["plans"].append(plan)
    # if the user is still anonymous, we remove that field from the request.
    if username == 'Anonymous':
        del request_cfg["userName"]

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
    req = requests.post(url=env_cfg['endpoint'], data=save_household_req, headers=headers)
    print(f'[API Response -> HouseholdId Generated]: {req.text}')
    api_resp_input_area.delete(1.0, END)
    api_resp_input_area.insert(END, req.text)


# function to handle generate button click event
def ui_generate():
    generate_save_req(def_year.get(), def_zip.get(), def_members.get(), def_months.get(),
                      [def_usage_med.get(), def_presc_usage.get()], def_plan_type.get(), username_selection.get())


# Generate request button
gen_save_request = Button(frame, text="Generate", command=partial(ui_generate), bg="#57CC99", fg='#112031',
                          relief=FLAT).pack(side=LEFT, padx=15, pady=15)

# Required for Tkinter, all objects for the program must be above this line.
root.mainloop()

# Examples to generate some saveHousehold request.

# Parameters: year, zip, members, months, usage, type
# generate_save_req(2021, 98178, 2, 1.5, ["Low", "Medium"], "QHP")
# generateSaveReq(2021, 98203, 9, 7.3, ["High", "Low"], "APTC")
# generateSaveReq(2022, 92251, 7, 10.5, ["low", "Very High"], "QHP")
# generateSaveReq(2022, 98001, 5, 6.5, ["Very High", "Low"], "APTC")
