# DEME-MOCKUP
ETI : Implementation of our mocked part for HORSE project

## Setup and Run Guide for DEME-MOCKUP Application
This guide provides detailed instructions on how to set up and run the DEME mockup application on an Ubuntu

## Prerequisites
Before starting, ensure that you have the following software installed on your System:

```
1. Docker
2. Git
```

## Step 1: Clone the Repository
### Navigate to the directory where you want to clone the repository
```cd <your path desctinationfolder>```

### Clone your repository
```git clone https://github.com/HORSE-EU-Project/DEME.git```

### Navigate into the cloned repository

```cd DEME-MOCKUP```

## Step2: Run the python application that mocks DEME
The mocked application can run both standalone or in a docker container.
If you want to run the application standalone follow "Option 1", otherwise follow "Option 2" described in the following paragraphs.

### Option 1. Run the python application standalone
From a new shell run the command
```python3 deme_mockup.py```

### Option 2. Run the application in a docker container
#### create the image locally specifying the version, for instance 1
From a new shell run the command
```./build-deme-mockup.sh 1```

#### check the image has been created
```docker images```

#### start and run the mocks DEME container specifying the version of the image for instance 1
```./run-deme-mockup.sh 1```


#### check the container is running
```docker ps -a```

## Step3: Check the DEME mockup is running correctly and listening to port 8091
The application is correctly running and waiting for https rest commands showing:

```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8091 (Press CTRL+C to quit)
```

In a new shell apply the ```GET/is_ok``` API against the running DEME mockup, for instance by curl command:

```curl -X GET http://localhost:8091/is_ok```

then check the response received to be:

```{"message":"ok"}```

## Step4: Configure DEME mockup

DEME mockup must be configured via ```deme_mockup_configure POST```

On the basis of your network instances and network features you can instruct DEME mockup to reply to GET/detection rest.

For example, if you are monitoring NTP, DNS and PFCP counters on two nodes, let's call them Genoa and Athens, of the network and you want simulate an attack only on PFCP of Genoa you have to send this configuration POST to DEME-mockup (in the example via curl):

```
curl -X POST -H "Content-Type: application/json" -d '{
    "mockup_periocity": 10,
    "attacks_configuration": [
        {
            "instance": "Genoa",
            "attack_configuration": [
                {
                    "feature": "NTP",
                    "attack_simulation": false
                },
                {
                    "feature": "DNS",
                    "attack_simulation": false
                },
                {
                    "feature": "PFCP",
                    "attack_simulation": true
                }
            ]
        },
        {
            "instance": "Athens",
            "attack_configuration": [
                {
                    "feature": "NTP",
                    "attack_simulation": false
                },
                {
                    "feature": "DNS",
                    "attack_simulation": false
                },
                {
                    "feature": "PFCP",
                    "attack_simulation": false
                }
            ]
        }
    ]
}' http://localhost:8091/deme_mockup_configure
```
By setting ```mockup_periocity``` to the value 10 the accuracy values ​​returned by GET/detection API will be different for the first 10 calls and then the accuracy ​​returned values will be repeated cyclically (the values returned to the 11th GET/detection call are equals to the values returned to the first call, the retuned values of the 12th GET/detection call are equals to the value returned by the second call and so on).\
The maximum value allowed for ```mockup_periocity``` is 20.


## Step5: Call GET/detection or POST/estimate APIs (port 8091)
### GET/detection
Depending on the DEME-mockup configuration DEME-mockup  will return the accuracy of an attach for each nodes

example: curl detection command:
```curl -X GET http://localhost:8091/detection```

### POST/estimate
DEME-mockup will check just the suyntax on the body of this POST

example: curl correct estimate command:
```
curl -X POST -H "Content-Type: application/json" -d '[
  {
    "timestamp": "1713303373",
    "instances": [
      {
        "instance": "Test_Instance",
        "features": [
          {
            "feature": "NTP",
            "value": 141
          },
          {
            "feature": "DNS",
            "value": 125
          },
          {
            "feature": "PFCP",
            "value": 138
          }
        ]
      }
    ]
  }
]' http://localhost:8091/estimate
```
that will return 
```
{"value" : "done"}
```

example: curl incorrect estimate command (date incorrect field name instead of the coorect timestamp field):
```
curl -X POST -H "Content-Type: application/json" -d '[
  {
    "date": "1713303373",
    "instances": [
      {
        "instance": "Test_Instance",
        "features": [
          {
            "feature": "NTP",
            "value": 141
          },
          {
            "feature": "DNS",
            "value": 125
          },
          {
            "feature": "PFCP",
            "value": 138
          }
        ]
      }
    ]
  }
]' http://localhost:8091/estimate
```
that will return an error specifying that ```timestamp``` field is missing 
```
{"detail":[{"type":"missing","loc":["body",0,"timestamp"],"msg":"Field required","input":{"date":"1713303373","instances":[{"instance":"Test_Instance","features":[{"feature":"NTP","value":141},{"feature":"DNS","value":125},{"feature":"PFCP","value":138}]}]}}]}
```