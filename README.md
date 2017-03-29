# PresntAPI
---
# Installation

## :arrow_up: How to Setup On OSX/Linux

**Step 1:** git clone this repo: `git clone git@github.com:awolins/PresntAPI.git`

**Step 2:** cd to the cloned repo: `cd PresntAPI`

**Step 3:** Create a virtual environment: `python3 -m venv .penv`

**Step 4:** Activate virtual environment: `source .penv/bin/activate`

**Step 5:** Install dependencies: `pip install -r requirements.txt`


## :arrow_forward: How to Run App

**Step 1:** make migrations: `./manage.py makemigrations`

**Step 2:** migrate your migrations: `./manage.py migrate`

**Step 3:** run app: `./manage.py runserver`

## Remember:
**Whenever You Make Changes to Models (models.py):** make migrations and run migrations: `./manage.py makemigrations && ./manage.py migrate`
