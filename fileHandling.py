from genericpath import isfile
from os import listdir, remove
from os.path import isfile, join, isdir
from pathlib import Path
from typing import List
from json import dump, load
from datetime import datetime
from enum import Enum

SURV_FOLDER = 'surveys'

if not isdir(SURV_FOLDER):
    Path(SURV_FOLDER).mkdir()
    print('Surveys folder was created')
else:
    print('Surveys folder was found')

def getSurveysList() -> List[str]:
    files_list = [f.replace('.json', '') for f in listdir(SURV_FOLDER) if isfile(join(SURV_FOLDER, f)) and f.endswith('.json')]
    
    return files_list

def getLastId() -> int:
    files_list = getSurveysList()
    max_id = -1
    for s in files_list:
        if s.isdigit():
            if int(s) > max_id:
                max_id = int(s)
    return max_id

def checkIfIdExists(id_: int) -> bool:
    files_list = getSurveysList()
    for f in files_list:
        if str(id_) == f:
            return True
    return False

def writeDictToJson(data: dict, path: str) -> None:
    with open(path, 'w') as f:
        dump(data, f)

def readJson(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            return load(f)
    except Exception as e:
        print(e)
        return {}

### SURVEY MANAGMENT

def createSurvey(name: str, start_date: datetime, end_date: datetime, description: str = "") -> None:
    data = {
        'name': name,
        'start_date': start_date.strftime("%m/%d/%Y %H:%M:%S"),
        'end_date': end_date.strftime("%m/%d/%Y %H:%M:%S"),
        'description': description,
        'questions': [],
        'responses': [],
    }

    writeDictToJson(data, join(SURV_FOLDER, str(getLastId() + 1) + '.json'))
 
def deleteSurvey(id_: int) -> bool:
    """Deletes survey by 'id'. Returns False if survey with id = 'id' does not exists"""
    files_list = getSurveysList()
    for f in files_list:
        if str(id_) == f:
            remove(join(SURV_FOLDER, str(id_) + '.json'))
            return True
    return False

def editSurvey(id_: int, 
                new_name: str = None, 
                new_description: str = None, 
                new_end_date: datetime = None) -> bool:
    """Edits survey by 'id'. Returns False if survey with id = 'id' does not exists or if both 'new_name', 'new_description' and 'new_end_date' were None or if error occured while reading file"""
    if not new_name and not new_description and not new_end_date:
        return False

    if not checkIfIdExists(id_):
        return False

    data = readJson(join(SURV_FOLDER, str(id_) + '.json'))
    if data == {}:
        return False

    if new_name:
        data['name'] = new_name
    if new_description:
        data['description'] = new_description
    if new_end_date:
        data['end_date'] = new_end_date.strftime("%m/%d/%Y %H:%M:%S")

    writeDictToJson(data, join(SURV_FOLDER, str(id_) + '.json'))

    return True
    
### QUESTIONS MANAGMENT
class QuestionState(Enum):
    text = 0
    single_choice = 1
    multiple_choice = 2

def addQuestion(id_: int, text: str, q_type: str,
                single_correct_answer: str = None,
                multiple_correct_answers: List[str] = None, 
                other_answers: List[str] = None) -> bool:
    """Returns False if survey with such id does not exists or needed args for QuestionState were missing. 
    
    QuestionStates are: text, single_choice, multiple_choice.
    
    'text' type requires no additional args

    'single_choice' type requires 'single_correct_answer' and 'other_answers'

    'multiple_choice' type requires 'multiple_correct_answers' and 'other_answers'"""
    if not checkIfIdExists(id_):
        return False

    data = readJson(join(SURV_FOLDER, str(id_) + '.json'))
    if data == {}:
        return False

    question_data = {
        'text': text, 
        'type': q_type,
    }

    if q_type == QuestionState.single_choice.name and single_correct_answer and other_answers:
        question_data['single_correct_answer'] = single_correct_answer
        question_data['other_answers'] = other_answers
    elif q_type == QuestionState.multiple_choice.name and multiple_correct_answers and other_answers:
        question_data['multiple_correct_answers'] = multiple_correct_answers
        question_data['other_answers'] = other_answers
    elif q_type != QuestionState.text.name:
        return False
        
    data['questions'].append(question_data)

    writeDictToJson(data, join(SURV_FOLDER, str(id_) + '.json'))

    return True

def deleteQuestion(survey_id: int, question_id: int) -> bool:
    if not checkIfIdExists(survey_id):
        return False

    data = readJson(join(SURV_FOLDER, str(survey_id) + '.json'))
    if data == {}:
        return False

    if question_id >= len(data['questions']):
        return False

    del data['questions'][question_id]

    writeDictToJson(data, join(SURV_FOLDER, str(survey_id) + '.json'))

    return True

def editQuestion(survey_id: int, question_id: int, q_type: QuestionState,
                new_text: str = None,
                new_single_correct_answer: str = None,
                new_multiple_correct_answers: List[str] = None, 
                new_other_answers: List[str] = None) -> bool:
    if not new_text and not new_single_correct_answer and not new_multiple_correct_answers and not new_other_answers:
        return False

    if not checkIfIdExists(survey_id):
        return False

    data = readJson(join(SURV_FOLDER, str(survey_id) + '.json'))
    if data == {}:
        return False

    if question_id >= len(data['questions']):
        return False

    if q_type.name != data['questions'][question_id]['type']:
        return False

    if q_type == QuestionState.single_choice and new_single_correct_answer:
        data['questions'][question_id]['single_correct_answer'] = new_single_correct_answer
    if q_type == QuestionState.multiple_choice and new_multiple_correct_answers:
        data['questions'][question_id]['multiple_correct_answers'] = new_multiple_correct_answers
    if (q_type == QuestionState.single_choice or q_type == QuestionState.multiple_choice) and new_other_answers:
        data['questions'][question_id]['other_answers'] = new_other_answers
    if new_text:
        data['questions'][question_id]['text'] = new_text

    writeDictToJson(data, join(SURV_FOLDER, str(survey_id) + '.json'))

    return True

#addQuestion(1, "why", QuestionState.multiple_choice, multiple_correct_answers=['bc', 'bc bc'], other_answers=['idk', 'what'])
#editQuestion(1, 1, QuestionState.multiple_choice, new_multiple_correct_answers=['BC'], new_other_answers=['IDK', 'what??'])