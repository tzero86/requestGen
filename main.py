import json
import argparse


# we can parse console positional arguments to generate data in bulk.

# parser = argparse.ArgumentParser(description='SaveHousehold Request Generator. e.g: python main.py 2021 2 5 "low" "High" "QHP"')
# parser.add_argument('year', metavar='Y', type=int, nargs='+',
#                     help='The year you want to create your plan for.')
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




def generateSaveReq(year, members, months, usage, type):
    request_cfg = {
        "coverageYear": year,
        "numberOfMembers": members,
        "coverageMonths": months,
        "medicalUse": usage[0],
        "prescriptionsUse": usage[1],
        "plans": [
        ]
    }
    if type == "QHP" or type == "APTC":
        for plan in plans[str(year)][str(type)]:
            request_cfg["plans"].append(plan)
    req_final = json.dumps(request_cfg, indent= 4, sort_keys= False)
    print(req_final)


generateSaveReq(2021, 2, 1.5, ["low", "medium"], "QHP")



