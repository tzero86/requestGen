# requestGen ._.

> **Current In Progress feature:** GUI Version

Data gen utility for da test team. Inspired by Mati's JS script to make the plans for the save req easier to use.
This is half-baked python approach with some easy to maintain dictionaries for the plan data, the plan data can even be initially generated with Mati's script and update the dictionary with that.

## User Interface

A simple UI made with Tkinter, should make the user of this even easier. Still requires setting up the cfg.json file before using.

![](https://i.imgur.com/Eek8g3R.png)

The plans for 2021 and 2022 for both APTC and QHP can be stored in the script and consumed on-demand by the parameters passed to the function.


## Usage

1. Rename the environment config file from `cfg_sample.json` to `cfg.json` and complete the values in that same file.
2. Change the Plans array and populate with the plan values you need for testing, add those into the appropriate type and year.
3. If you don't want to generate the HHID automatically, just set the `"sendSaveReq": true,`  to `"sendSaveReq": false,`.
4. Select the parameters to create your custom request.
5. Click Generate button and it will generate the request for you to copy and also send it to the API to get an ID back! (Might not always be convenient, will add a switch to turn it off later.)
6. Enjoy!


For example running the function with the following values:

```python
# Parameters: year, zip, members, months, usage, type
generate_save_req(2021, 98178, 2, 1.5, ["Low", "Medium"], "QHP")
```

Will produce the following JSON code ready to be used in postman:

```JSON
{
    "coverageYear": 2021,
    "zipCode": 98178,
    "noOfMembers": 2,
    "coverageMonths": 1.5,
    "medicalUse": "low",
    "prescriptionsUse": "medium",
    "plans": [
        {
            "id": "QHP218CA54786",
            "netPremium": 40.69
        },
        {
            "id": "QHP218CA54786",
            "netPremium": 40.69
        },
        {
            "id": "QHP218CA54786",
            "netPremium": 530.46
        },
        {
            "id": "QHP218CA54786",
            "netPremium": 530.46
        }
    ]
}

```

The script also communicates directly with end endpoint and returns the ID generated for the request crafted.

```
[API POST Request -> SavehouseholdId Endpoint]: Sending request to the endpoint...
[API Response -> HouseholdId Generated]: {"householdId":"1dbc6b36-XXX-XXXX-95ba-12e6efff6a4b"}
```


## Nice to have features

- Add support for Anonymous or registered user
- Fully configure commandline arguments support to generate batches of data
- Export the generated req in JSON


@tzero86


