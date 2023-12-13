# !pip install tabula-py
import pandas as pd
import numpy as np
import re
import tabula

from io import BytesIO

def sbi_cal(pdf):
    # dfs = tabula.read_pdf(pdf, pages='all')
    try:
        pdf_stream = BytesIO(pdf)
        
        dfs = tabula.read_pdf(pdf_stream)

        df = pd.concat([ dfs[page] for page in range(len(dfs))], axis=0)
        df = df.dropna(subset=['Txn Date', 'Balance'])

        s = pd.Series(list(range(df.shape[0])))
        # print(s)
        df = df.set_index([s])

        for row_no in df.index:
            df["Txn Date"][row_no] = re.findall(r'\b([A-Za-z]+)', df['Txn Date'][row_no])[0]
            df['Debit'][row_no] = float(str(df["Debit"][row_no]).replace(',', ''))
            df['Credit'][row_no] = float(str(df["Credit"][row_no]).replace(',', ''))
            df['Balance'][row_no] = float(str(df["Balance"][row_no]).replace(',', ''))

        total = {}

        for month in list(set(df['Txn Date'])):
            # print(month)
            debit_sum = df[df['Txn Date'] == month]['Debit'].sum()
            credit_sum = df[df['Txn Date'] == month]['Credit'].sum()
            saving = credit_sum - debit_sum
            balance_sum = df[df['Txn Date'] == month]['Balance'].sum()

            # print("Debite sum",df[df['Txn Date'] == month]['Debit'].sum())
            # print("Credit sum", df[df['Txn Date'] == month]['Credit'].sum())
            # print("Balance sum",df[df['Txn Date'] == month]['Balance'].sum())

            total[month] = {'Debit sum': debit_sum,
                            'Credit sum' : credit_sum,
                            'Saving' : saving,
                            'balance' : balance_sum
                            }

        return total 
    
    except:
        return {"msg" : "Error Occured while proccesing file"}

        
