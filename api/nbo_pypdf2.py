from collections import defaultdict

from PyPDF2 import PdfReader
from io import BytesIO
import re

def nbo_cal(pdf_data: bytes) -> dict:

    try:
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

            
        # Initializing dictionaries to store credit sum, debit sum, and savings
        credit_sum = defaultdict(float)
        debit_sum = defaultdict(float)
        saving = defaultdict(float)

        # Calculating credit sum, debit sum, and savings for each month
        for row in rows:
            month = row['month']
            credit_sum[month] += row['credit']
            debit_sum[month] += row['debit']
            saving[month] += row['credit'] - row['debit']


        print( {
            "credit_sum": dict(credit_sum),
            "debit_sum": dict(debit_sum),
            "saving": dict(saving)
        })
        return {
            "credit_sum": dict(credit_sum),
            "debit_sum": dict(debit_sum),
            "saving": dict(saving)
        }

        

        # ------------------------------------------
        # old code-----------
        # credit_sum = {}
        # debit_sum = {}
        # saving = {}

        # for row in rows:
        #     month = row['month']
        #     credit = row['credit']
        #     debit = row['debit']


            
        #     credit_sum[month] = credit_sum.get(month, 0) + credit
        #     debit_sum[month] = debit_sum.get(month, 0) + debit


        # for x in credit_sum: 
        #     # print(credit_sum[x]-debit_sum[x])
        #     # calculating saving  credit - debit (for each month)
        #     saving[x] = credit_sum[x] - debit_sum[x]



        # return {"credit_sum": credit_sum, "debit_sum":debit_sum, "saving": saving}
    
    except: 
        return {"msg" : "Error Occured while proccesing file"}
