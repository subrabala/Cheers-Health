import pandas as pd
from typing import List

from fastapi import FastAPI, Depends, Response, status, HTTPException
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware


from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db
from app.config import settings

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get_response", status_code=status.HTTP_200_OK, response_model=List[schemas.AddressDetails])
def getAddresses(payLoad: schemas.GetAddress, db: Session = Depends(get_db)):

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

def gen_response(cell):
    cell_no = convert_to_no(cell)
    if (cell == "A1"):
        cell="A2"
        cell_no = convert_to_no(cell)
        response = dataset.iloc[cell_no[0]:len(dataset.index), cell_no[1]+1].dropna()
        response = response.to_dict()
        response_tmp = response.copy()
        for key in response_tmp.keys():
            response[convert_to_xl([key, cell_no[1]])
                     ] = response.pop(key, None)
        return response

    if (cell_no[1]%2 == 0):
        # response = dataset.iloc[cell_no[0], cell_no[1]+1]
        # response = {convert_to_xl([cell_no[0], cell_no[1]+1]): response}
        response = {"Question": dataset.iloc[cell_no[0], cell_no[1]+1]}
        next = dataset.index.where(dataset[list(dataset.columns)[cell_no[1]+1]].notna().dropna())
        next = list(i for i in (list(next)) if i>cell_no[0])[0]
        options = dataset.iloc[cell_no[0]:int(next), cell_no[1]+2].dropna()
        options = convert_to_dict(options, [cell_no[0], cell_no[1]+1])
        response["Options"]=options
        return response