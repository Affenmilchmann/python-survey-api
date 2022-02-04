from ApiManager import ApiManager
from typing import Optional
from fileHandling import *
from datetime import datetime

from fastapi import FastAPI, HTTPException

def checkDateFormat(date: str) -> bool:
    if date == None:
        return True
    try:
        datetime.strptime(date, "%m/%d/%Y %H:%M:%S")
        return True
    except ValueError:
        return False

app = FastAPI()

@app.post("/survey/add/")
def addSurveyApi(name: str, start_date: str, end_date: str, description: Optional[str] = None):
    if checkDateFormat(start_date) and checkDateFormat(end_date):
        createSurvey(name, datetime.strptime(start_date, f"%m/%d/%Y %H:%M:%S"), datetime.strptime(end_date, f"%m/%d/%Y %H:%M:%S"), description)
        return {"Ok"}
    else:
        raise HTTPException(
            status_code=400,
            detail=[{"msg": "DateTime format is %m/%d/%Y %H:%M:%S"}]
        )

@app.delete("/survey/delete/")
def deleteSurveyApi(survey_id: int):
    if deleteSurvey(survey_id):
        return {"Ok"}
    else:
        raise HTTPException(
            status_code=400,
            detail=[{"msg": "Invalid survey_id"}]
        )

@app.put("/survey/edit/")
def editSurveyApi(survey_id: int, name: Optional[str] = None, description: Optional[str] = None, end_date: Optional[str] = None):
    if checkDateFormat(end_date):
        if editSurvey(survey_id, name, description, datetime.strptime(end_date, f"%m/%d/%Y %H:%M:%S")):
            return {"Ok"}
        else:
            raise HTTPException(
            status_code=400,
            detail=[{"msg": "record with given 'survey_id' does not exists or 'name', 'description' and 'end_date' were missing"}]
        )
    else:
        raise HTTPException(
            status_code=400,
            detail=[{"msg": "DateTime format is %m/%d/%Y %H:%M:%S"}]
        )

@app.post("/survey/question/add/")
def addQuestionApi(survey_id: int, text: str, question_type: str, 
                    single_correct_answer: Optional[str] = None, 
                    multiple_correct_answers: Optional[List[str]] = None,
                    other_answers: Optional[List[str]] = None):
    missing_args = False
    if question_type == QuestionState.single_choice.name:
        if not single_correct_answer or not other_answers:
            print(other_answers)
            missing_args = True
    elif question_type == QuestionState.multiple_choice.name:
        if not multiple_correct_answers or not other_answers:
            missing_args = True
    elif question_type != QuestionState.text.name:
        raise HTTPException(
            status_code=400,
            detail=[{"msg": "Wrong quiestion type. Types are 'text', 'single_choice' or 'multiple_choice'"}]
        )

    if missing_args:
        raise HTTPException(
            status_code=400,
            detail=[{"msg": "Missing args for non text question"}]
        )
    
    if addQuestion(
            survey_id, text, question_type, 
            single_correct_answer, 
            multiple_correct_answers, 
            other_answers
            ):
        return {"Ok"}
    else:
        raise HTTPException(
            status_code=400,
            detail=[{"msg": "survey with such id does not exists or needed args for QuestionState were missing"}]
        )