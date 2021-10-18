import requests
import pandas as pd
import os

def getTable(link, nth):
    """
    Returns specified nth table from website

    """
    try:
        headers = {'User-Agent': 
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        pageTree = requests.get(link, headers=headers)
        df = pd.read_html(pageTree.text)
        df = df[nth]
        list_of_files = os.listdir('static/')
        try:
            latest_file = max(list_of_files, key=os.path.getctime)
        except:
            latest_file = 'New.xlsx'
        x = latest_file.split('.')
        file = x+"1.xlsx"
        df.to_excel('static/'+file)
        return file
    except:
        return "Error.xlsx"
