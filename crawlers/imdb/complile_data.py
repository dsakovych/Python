import pandas as pd
import os
from bs4 import BeautifulSoup
import numpy as np


def gather_data():
    reviews = os.listdir(os.getcwd() + '/reviews/')
    total_df = pd.DataFrame()
    for file in reviews:
        temp_df = pd.read_csv('reviews/' + file, delimiter='|', encoding='cp1251')
        temp_df['id'] = file.split('.')[0]
        total_df = total_df.append(temp_df)
    total_df.to_csv('results.csv', delimiter='|', encoding='cp1251')


if __name__ == "__main__":
    gather_data()