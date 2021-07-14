# Monitoring of (vaccine) booking sites of a certain university...

You can get reservation availability information througe slack notification!

## SETUP

* Set your environment variable in .env file
```
TARGET_URL=*****
SLACK_WEBHOOK_URL=*****
```

## Run

* Build
```
docker build . -t get-vaccine
```

* Run 
```
docker run --env-file .env --rm -v $(pwd):/work -w /work get-vaccine sh -c "python main.py"
```
