# requestGen ._.

> **Current In Progress feature:** Connect to the API endpoint directly generate the HHID based on the request generated



Data gen utility for da test team. Inspered by Mati's JS script to make the plans for the save req easier to use.
This is half-baked python approach with some easy to maintain dictionaries for the plan data, the plan data can even be initially generated with Mati's script and update the dictionary with that.

The plans for 2021 and 2022 for both APTC and QHP can be stored in the script and consumed on-demand by the parameters pased to the function.

For example running the function with the following values:

```python
generateSaveReq(2021, 98178, 2, 1.5, ["low", "medium"], "QHP")
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


## Nice to have features

- Add support for Anonymous or registered user
- Fully configure commandline arguments support to generate batches of data
- Export the generated req in JSON



