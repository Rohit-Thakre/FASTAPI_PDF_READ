from collections import defaultdict
from io import BytesIO
import re
import pdfplumber

def nbo_cal(pdf_data: bytes) -> dict:

    pdf_stream = BytesIO(pdf_data)
    pdf = pdfplumber.open(pdf_stream)
    page_size = len(pdf.pages)
        
    rows = []
    
        
    for no in range(page_size): 
    # for no in range(1): 
        page_obj = pdf.pages[no]    
            
        # start_from 120
        page_text = page_obj.extract_text()[120:]

        page_list = page_text.split('\n')

        for line in page_list:
              
            try:

                amt = re.findall(r'\-*\d{1,3}\.\d{1,}\sOMR', line)
                amount = amt[0]

                float_amount = float(amount.split(' ')[0])

                ac_bal = float(amt[1].split(' ')[0])   

                credite = 0
                debit = 0
                if amount[0] =="-":
                    debit += float_amount
                else: 
                    credite += float_amount

                posting_date = re.findall(r'\d{2}\s\w{3}\s\d{4}', line)[0]

                month = posting_date.split(' ')[1]
            
            
                rows.append({'month': month, 'credit': credite, 'debit': -debit, "ac_bal" : ac_bal})

            except:
                print('line has no related data')
                print(line)


    monthly_sum_credit = defaultdict(float)
    monthly_sum_debit = defaultdict(float)
    monthly_sum_ac_bal = defaultdict(float)

    # Calculate sum for each month
    for dct in rows:
        month = dct['month']
        monthly_sum_credit[month] += dct['credit']
        monthly_sum_debit[month] += dct['debit']
        monthly_sum_ac_bal[month] += dct['ac_bal']



    return_dct = {}
    for month in monthly_sum_credit: 
        return_dct[month] = {
                            'Credit sum': monthly_sum_credit[month],
                             'Debit sum': monthly_sum_debit[month],
                             'Saving': monthly_sum_credit[month] - monthly_sum_debit[month]
                             }
    return return_dct

            
