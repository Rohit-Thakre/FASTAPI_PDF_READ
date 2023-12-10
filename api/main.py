from fastapi import FastAPI, UploadFile, File, HTTPException

# django ----
from PyPDF2 import PdfReader
from io import BytesIO
import re
# -----------

app = FastAPI()

def cal(pdf_data: bytes) -> dict:
    pdf_stream = BytesIO(pdf_data)

    # Use PdfReader to read the PDF data from the BytesIO object
    pdf = PdfReader(pdf_stream)
    page_size = len(pdf.pages)

    rows = []
    months = list()
    
    for no in range(page_size): 
    # for no in range(1): 
        page_obj = pdf.pages[no]    
        
        # start_from 120
        page_text = page_obj.extract_text()[120:]

        page_list = re.split(r'OMR\n', page_text)
        # last me ORM add karn hai, since ORM\n se splite kr rahe hai to vo remove kiya hai 

        for line in page_list:
            try : 
                line = line+'OMR'

                amt = re.findall(r'\-*\d{1,3}\.\d{1,}\sOMR', line)
                amount = amt[0]

                float_amount = float(amount.split(' ')[0])

                ac_bal = float(amt[1].split(' ')[0])   

                credite = 0
                debit = 0
                if amount[0] =="-":
                    # debited_sum += float_amount
                    debit += float_amount
                else: 
                    # credited_sum += float_amount
                    credite += float_amount

                posting_date = re.findall(r'\d{2}\s\w{3}\s\d{4}', line)[0]
                month = posting_date.split(' ')[1]
                
                if month not in months: 
                    months.append(month)

                rows.append({'month': month, 'credit': credite, 'debit': -debit, "ac_bal" : ac_bal})


            except:
                # print("error occured")
                pass
        
    credit_sum = {}
    debit_sum = {}
    saving = {}

    for row in rows:
        month = row['month']
        credit = row['credit']
        debit = row['debit']
        
        credit_sum[month] = credit_sum.get(month, 0) + credit
        debit_sum[month] = debit_sum.get(month, 0) + debit

    for x in credit_sum: 
        # print(credit_sum[x]-debit_sum[x])
        # calculating saving  credit - debit (for each month)
        saving[x] = credit_sum[x] - debit_sum[x]



    return {"credit_sum": credit_sum, "debit_sum":debit_sum, "saving": saving}
  
  

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/upload")
async def read(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file")

    pdf_data = await file.read()
    # total_dct = cal(pdf_data)
    
    return cal(pdf_data)


