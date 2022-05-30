import urllib, urllib.request
from datetime import datetime


def get_data(province_id):  # Отримання тестових даних із WEB-сторінки
    url = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2020&type=Mean'.format(province_id)

    # Відкриття WEB-сторінки можна зробити наступним чином:
    webpage = urllib.request.urlopen(url)
    text = webpage.read()

    # Отримати поточну дату і час
    now = datetime.now()
    # Згенерувати строку з поточою датою і часом та необхідним форматуванням можна за допомогою методу strftime
    date_and_time_time = now.strftime("%d.%m.%Y_%H^%M^%S")

    # Створити новий файл за допомоги функції open
    out = open('/home/maryna/Desktop/lab1/' + 'NOAA_ID' + str(province_id) + '-' + date_and_time_time + '.csv', 'wb')
    # Після відкриття у змінній text міститься текст із WEB-сторінки, який тепер можна записати у файл
    out.write(text)
    out.close()

import sys
sys.path.append('/home/maryna/Desktop/lab1')
for id in range(1, 28):
    get_data(id)



import pandas as pd
import os.path

def make_header(filepath):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    dataframe = pd.read_csv(filepath, header=1, names=headers)
    dataframe.drop(dataframe.loc[dataframe['VHI'] == -1].index)
    return dataframe


def index_change(filepath, new, oblast):
    dataframe = make_header(filepath)
    dataframe['area'] = new
    dataframe.to_csv(f'/home/maryna/Desktop/lab1/NOAA_ID_{new}_({oblast}).csv', index=False)
    return dataframe

index_change('/home/maryna/Desktop/lab1/NOAA_ID2-29.05.2022_12^56^37.csv', 24, "Чернігівська") 


import pandas as pd
def data_analysis(filepath, year):
    data = pd.read_csv(filepath)
    df = data[(data['VHI'] != -1)]

    ext_drought = df[df['VHI'] <= 15]  # Дані у періоди екстримальної засухи
    max_val = ext_drought[ext_drought.Year.astype(str) == str(year)]['VHI'].max()
    print(f"{max_val} - максимальний VIH екстримальної засухи в {year} році")
    min_val = ext_drought[ext_drought.Year.astype(str) == str(year)]['VHI'].min()
    print(f"\t{min_val} - мінімальний VIH екстримальної засухи в {year} році")

    this_year = int(ext_drought[ext_drought['VHI'] == ext_drought['VHI'].min()]['Year'])
    print(f"\t\t{this_year} - рік, в якому був найектримальніший період засухи")

    drought = df[(15 < df['VHI']) & (df['VHI'] <= 35)]  # Дані у періоди помірної посухи
    min_val = drought[drought.Year.astype(str) == str(year)]['VHI'].min()
    print(f"\t{min_val} - мінімальний VIH помірної посухи в {year} році")
    max_val = drought[drought.Year.astype(str) == str(year)]['VHI'].max()
    print(f"{max_val} - максимальний VIH помірної посухи в {year} році")
    pass

data_analysis("/home/maryna/Desktop/lab1/NOAA_ID_15_(Полтавська).csv", 1991)