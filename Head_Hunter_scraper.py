import requests
import pandas as pd
import datetime

'''
search_text is a word that we are looking for
page is an innicial page of the search
list is an empty list (it is needed for the list concatenation)
'''

# Scrapes all vacancies on tile pages for %search_text%
def search_vacancy_ids(search_text):
    page = 0
    list = []

    '''
    This part is needed to check the quantity of pages for current search_text
    hh_link is an IP request for current search_text
    data['pages'] is the quantity of pages for current search_text
    '''

    hh_link = 'https://api.hh.ru/vacancies?specialization=1&area=2&per_page=1&text={}&page={}'.format(search_text, page)
    r = requests.get(hh_link)
    data = r.json()

    # Get a list of all vacancies ID's for current search_text
    for i in range(data['pages']):
        link = 'https://api.hh.ru/vacancies?specialization=1&area=2&per_page=1&text={}&page={}'.format(search_text, page)
        r = requests.get(link)
        id = ((r.json())['items'])[0]['id']
        list = list + [id]
        # Showing the progress
        print("Progress is " +str(i) + "/" + str(data['pages']))
        page = page + 1
    # list is a list of all vacancies ID's for current search_text
    print('Here you go. The list of vacancies for  "' + str(search_text) + '":')
    print(list)
    save_Pandas_DataFrame_to_Excel(vacancies_to_scrape=list)

# Saves Pandas DataFrame to Excel file
def save_Pandas_DataFrame_to_Excel(vacancies_to_scrape):
    df_list = [scraping_preview_pages(i) for i in vacancies_to_scrape]
    df = pd.concat(df_list, ignore_index=True)
    time = str(datetime.datetime.now())[:19].replace(':', '-')
    df_name = 'Head Hanter_{}_{}.xlsx'.format(search_text, time)
    df.to_excel(df_name, index=False)

# Scrapes preview pages to the Pandas DataFrame
def scraping_preview_pages(job_id):
    print('Scraping the vacancy № ' + str(job_id))
    link = 'https://api.hh.ru/vacancies/{}'.format(job_id)
    r = requests.get(link)
    data = r.json()

    # Definition of a type of the salary (До вычета НДФЛ | на руки)
    try:
        salary_to = data['salary']['to']
        salary_from = data['salary']['from']
        salary_gross = data['salary']['gross']
        if data['salary']['gross'] == True:
            salary_gross = 'До вычета НДФЛ'
        elif data['salary']['gross'] == False:
            salary_gross = 'На руки'
        else:
            salary_gross = 'Не указана'
        salary_currency = data['salary']['currency']
    except:
        salary_to = salary_from = salary_gross = salary_currency = 'Не указано'

    # Address
    try:
        address = str(data['address']['street']) + ', ' + str(data['address']['building'])
    except:
        address = 'Не указан'

    # Metro stations
    try:
        metro = data['address']['metro']['station_name']
    except:
        metro = 'Не указано'

    # Contacts
    try:
        contacts = str(data['contacts']['name']) + ' ' + str(data['contacts']['email'])
    except:
        contacts = 'Не указаны'

    # Key skills - Data cleaning
    try:
        key_skills = str(data['key_skills']).replace("{'name': '", "").replace("[", "").replace("]", "").replace("'","").replace("{", "").replace("}", "")
    except:
        key_skills = ' '

    # Add all data in a Python dictionary
    dictionary = [{'Дата': data['created_at'][0:10],
                   'Город': data['area']['name'],
                   'Вакансия': data['name'],
                   'З/п от': salary_from,
                   'З/п до': salary_to,
                   'Налог': salary_gross,
                   'Валюта': salary_currency,
                   'Компания': data['employer']['name'],
                   'URL компании': data['employer']['alternate_url'],
                   'Адрес': address,
                   'Метро': metro,
                   'Опыт работы': data['experience']['name'],
                   'Занятость': data['employment']['name'],
                   'Контакты': contacts,
                   'URL вакансии': data['alternate_url'],
                   'Описание вакансии': data['description'],
                   'Ключевые навыки': key_skills,
                   'ID': data['id'],
                   'Запрос': search_text}]

    # Create DataFrame object from the dictionary
    df = pd.DataFrame(dictionary)
    df = df[['ID', 'Дата', 'Город', 'Запрос', 'Вакансия', 'З/п от', 'З/п до', 'Валюта', 'Налог', 'Компания', 'Адрес',
             'Метро', 'Опыт работы', 'Занятость', 'Ключевые навыки', 'Описание вакансии', 'Контакты', 'URL вакансии',
             'URL компании']]
    return df


# Search a single word
# search_text= 'QA engineer'
# search_vacancy_ids(search_text)

# Search a seleral words
search_list = ['automation', 'python', 'QA', 'tester', 'relocation']
for i in search_list:
    search_text = i
    search_vacancy_ids(i)
