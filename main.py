import json
import requests

# Load ENV settings from the file

file = open('ENV.json',)
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
        "coverageMonths": months,
        "coverageYear": year,
        "zipCode": zip,
        "noOfMembers": members,
        "medicalUse": usage[0],
        "prescriptionUse": usage[1],
        "plans": [
        ]
    }
    # if program type is QHP or APTC we proceed.
    if type == "QHP" or type == "APTC":
        # for each plan stored for the YEAR and Plan Type, we append that plan to the plans array in request_cfg
        for plan in plans[str(year)][str(type)]:
            request_cfg["plans"].append(plan)
    # we parse the dictionary into a JSON object and print it out, we can direct the same to a file on the disk.
    req_final = json.dumps(request_cfg, indent=4, sort_keys=False)
    print(req_final)
    send_post_request(req_final)


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


# Examples to generate some saveHousehold request.

# Parameters: year, zip, members, months, usage, type
generate_save_req(2021, 98178, 2, 1.5, ["Low", "Medium"], "QHP")
# generateSaveReq(2021, 98203, 9, 7.3, ["High", "Low"], "APTC")
# generateSaveReq(2022, 92251, 7, 10.5, ["low", "Very High"], "QHP")
# generateSaveReq(2022, 98001, 5, 6.5, ["Very High", "Low"], "APTC")
