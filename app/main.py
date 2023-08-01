import pandas as pd

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# from sqlalchemy.orm import Session

# import models
# from database import engine, get_db
import schemas


app = FastAPI(prefix='/chatbot')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


dataset = pd.read_excel("dataset.xlsx")
alphabet = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"

def convert_to_no(cell):
    cell = cell.lower()
    cell_no = [int(cell[1:])-2, alphabet.index(cell[0])]
    return cell_no

def convert_to_xl(cell_no):
    cell = alphabet[cell_no[1]].upper()+str(cell_no[0]+2)
    return cell

def convert_to_dict(response, cell_no):
    response = response.to_dict()
    response_tmp = response.copy()
    for key in response_tmp.keys():
        response[convert_to_xl([key, cell_no[1]+1])
                    ] = response.pop(key, None)
    return response

@app.get("/get_questions", )
def get_questions():
    cell="A2"
    cell_no = convert_to_no(cell)
    response = dataset.iloc[cell_no[0]:len(dataset.index), cell_no[1]+1].dropna()
    response = response.to_dict()
    response_tmp = response.copy()
    for key in response_tmp.keys():
        response[convert_to_xl([key, cell_no[1]])
                    ] = response.pop(key, None)
    return response

@app.post("/gen_response", status_code=status.HTTP_200_OK, response_model=schemas.QuestionResponse)
def gen_response(payLoad: schemas.CellPosition):
    cell_no = convert_to_no(payLoad.cell)
    if (cell_no[1]%2 == 0):
        response = {"question": dataset.iloc[cell_no[0], cell_no[1]+1]}
        next_index = dataset.index.where(dataset[list(dataset.columns)[cell_no[1]+1]].notna().dropna())
        next_index = list(i for i in (list(next_index)) if i>cell_no[0])[0]
        options = dataset.iloc[cell_no[0]:int(next_index), cell_no[1]+2].dropna()
        options = convert_to_dict(options, [cell_no[0], cell_no[1]+1])
        response["options"]=options
        return response

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Cell Position")
