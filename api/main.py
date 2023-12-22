import sbi
import nbo
from io import BytesIO
from PyPDF2 import PdfReader
from fastapi import FastAPI, UploadFile, File, Form,HTTPException
from pydantic import BaseModel
import re
import pdfplumber

app = FastAPI()

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}


@app.post("/upload")
async def read(  name:str =  Form(...) , bank: str=Form(...), file: UploadFile = File(...) ):
    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    pdf_data = await file.read()


    # # for checking pdf belongs to user or not 
    # pdf_stream = BytesIO(pdf_data)
    # pdf = PdfReader(pdf_stream)
    # page1 = pdf.pages[0]
    # text = page1.extract_text()[:len(name)].lower()

    # if text != name.lower(): 
    #     raise HTTPException(status_code=400, detail=f"Pdf file does not belongs to {name}.")

    pdf_stream = BytesIO(pdf_data)
    pdf = pdfplumber.open(pdf_stream)
    page1 = pdf.pages[0]

    try:
        if bank.lower() == 'nbo' or bank.lower() == 'national bank of oman': 
            text = page1.extract_text()[:100].lower().split('\n')[0].split("'")[0]
            print("Extracted text : ",text)
            if text == name.lower():
                return nbo.nbo_cal(pdf_data)
            else:
                return {"msg": f"Pdf file does not belongs to {name}."}

        elif bank.lower() == 'sbi' or bank.lower() == 'state bank of india':
            text = page1.extract_text()[:100].lower().split('\n')[0].split(":")[1]
            print("Extracted text : ",text)
            if text == name.lower():
                return sbi.sbi_cal(pdf_data)

            else:
                return {"msg": f"Pdf file does not belongs to {name}."}
            
        
        else:
            return {'msg': f'can\'t handle {bank}\'s statement at the moment.'}
   
    except Exception as e:
        return {'error msg': "Error Occured while proccesing pdf file",'error':e}

# ------------------------------------------------------
