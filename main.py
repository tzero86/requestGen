import json
import argparse


# we can parse console positional arguments to generate data in bulk.

# parser = argparse.ArgumentParser(description='SaveHousehold Request Generator. e.g: python main.py 2021 2 5 "low" "High" "QHP"')
# parser.add_argument('year', metavar='Y', type=int, nargs='+',
#                     help='The year you want to create your plan for.')
# parser.add_argument('zip', metavar='Z', type=int, nargs='+',
#                     help='The zip code you want to use.')
# parser.add_argument('members', metavar='N', type=int, nargs='+',
#                     help='The number of members for the household.')
# parser.add_argument('months', metavar='M', type=int, nargs='+',
#                     help='The number of coverage months.')
# parser.add_argument('medUsage', metavar='Q', type=str, nargs='+',
#                     help='The medicalUse indicator: Low, Medium, High, Very High')
# parser.add_argument('prescUsage', metavar='E', type=str, nargs='+',
#                     help='The prescriptionUse indicator: Low, Medium, High, Very High')
# parser.add_argument('type', metavar='T', type=str, nargs='+',
#                     help='The plan Type: QHP, APTC')
#
# args = parser.parse_args()


# the main dictionary for the plans, this is the data to be replaced with the actual plans.
# for both APTC and QHP and for 2021 AND 2022.
plans = {

    "2021": {
        "QHP": [
            {"id": "QHP218CA54786", "netPremium": 40.69},
            {"id": "QHP218CA54786", "netPremium": 40.69},
            {"id": "QHP218CA54786", "netPremium": 530.46},
            {"id": "QHP218CA54786", "netPremium": 530.46},
        ],
        "APTC": [
            {"id": "APTC21CA54786", "netPremium": 40.69},
            {"id": "APTC21CA54786", "netPremium": 530.46},
            {"id": "APTC21CA54786", "netPremium": 40.69},
            {"id": "APTC21CA54786", "netPremium": 530.46}
        ],
    },
    "2022": {
        "QHP": [
            {"id": "QHP228CA54786", "netPremium": 40.69},
            {"id": "QHP228CA54786", "netPremium": 530.46},
            {"id": "QHP228CA54786", "netPremium": 40.69},
            {"id": "QHP228CA54786", "netPremium": 530.46}
        ],
        "APTC": [
            {"id": "APTC22CA54786", "netPremium": 40.69},
            {"id": "APTC22CA54786", "netPremium": 530.46},
            {"id": "APTC22CA54786", "netPremium": 40.69},
            {"id": "APTC22CA54786", "netPremium": 530.46}
        ],
    }
}

# the main function, gets the parameters and spits out a JSON to be used in postman
def generateSaveReq(year, zip , members, months, usage, type):
    # We create our object with the request fields we need
    request_cfg = {
        "coverageYear": year,
        "zipCode": zip,
        "noOfMembers": members,
        "coverageMonths": months,
        "medicalUse": usage[0],
        "prescriptionsUse": usage[1],
        "plans": [
        ]
    }
    # if program type is QHP or APTC we proceed.
    if type == "QHP" or type == "APTC":
        # for each plan stored for the YEAR and Plan Type, we append that plan to the plans array in request_cfg
        for plan in plans[str(year)][str(type)]:
            request_cfg["plans"].append(plan)
    # we parse the dictionary into a JSON object and print it out, we can direct the same to a file on the disk.
    req_final = json.dumps(request_cfg, indent= 4, sort_keys= False)
    print(req_final)


# Examples to generate some saveHousehold request.
generateSaveReq(2021, 98178, 2, 1.5, ["low", "medium"], "QHP")
generateSaveReq(2021, 98203, 9, 7.3, ["High", "Low"], "APTC")
generateSaveReq(2022, 92251, 7, 10.5, ["low", "Very High"], "QHP")
generateSaveReq(2022, 98001, 5, 6.5, ["Very High", "Low"], "APTC")


