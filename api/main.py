
from io import BytesIO
from PyPDF2 import PdfReader



import sbi
import nbo

from fastapi import FastAPI, UploadFile, File, HTTPException
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/upload")
async def read(name:str, bank: str, file: UploadFile = File(...) ):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    pdf_data = await file.read()


    # for checking pdf belongs to user or not 
    pdf_stream = BytesIO(pdf_data)
    pdf = PdfReader(pdf_stream)
    page1 = pdf.pages[0]
    text = page1.extract_text()[:200].lower()

    if name.lower() not in text: 
        raise HTTPException(status_code=400, detail=f"Pdf file does not belongs to {name}.")


    try:
        if bank.lower() == 'nbo' or bank.lower() == 'national bank of oman': 
            return nbo.nbo_cal(pdf_data)

        elif bank.lower() == 'sbi' or bank.lower() == 'state bank of india':
            return sbi.sbi_cal(pdf_data)
        
        else:
            return {'msg': f'can\'t handle {bank}\'s statement at the moment.'}
    except:
        return {'error msg': "Error Occured while proccesing pdf file"}

# ------------------------------------------------------

