from ApiManager import ApiManager
from typing import Optional
from fileHandling import *
from datetime import datetime

from fastapi import FastAPI

def checkDateFormat(date: str) -> bool:
    try:
        datetime.strptime(date, "%m/%d/%Y %H:%M:%S")
        return True
    except ValueError:
        return False

app = FastAPI()

@app.post("/add_survey/")
def addSurveyApi(name: str, start_date: str, end_date: str, description: Optional[str] = None):
    if checkDateFormat(start_date) and checkDateFormat(end_date):
        createSurvey(name, datetime.strptime(start_date, f"%m/%d/%Y %H:%M:%S"), datetime.strptime(end_date, f"%m/%d/%Y %H:%M:%S"), description)
        return {"Ok"}
    else:
        return {"Error. DateTime format is %m/%d/%Y %H:%M:%S"}

@app.post("/delete_survey/")
def deleteSurveyApi(id: int):
    if deleteSurvey(id):
        return {"Ok"}
    else:
        return {"Invalid id"}