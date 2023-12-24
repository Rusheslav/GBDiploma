import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup

URL = 'https://www.pealim.com/ru/search/?q='
HEB = 'פםןוטארקףךלחיעכגדשץתצמנהבסז'


def translate(msg):
    html = get_html(URL + msg)
    buttons = ReplyKeyboardRemove()
    if msg[0] in HEB:
        url = get_new_url_heb(html)
    else:
        url = get_new_url_rus(html)
    if 'https' not in url:  # if 'url' doesn't contain a link, then we want the user to choose a verb by hitting a button
        result, buttons = url[0], url[1]
        return result, buttons
    new_html = get_html(url)
    result = get_data(new_html)
    return result, buttons


def get_html(url):
    r = requests.get(url)
    return r.text


def get_new_url_heb(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        url = soup.find('a', class_='btn btn-primary').get('href')
        return 'https://www.pealim.com'+url
    except:
        text = 'Кажется, вы допустили ошибку в написании. Попробуйте ещё раз'
        buttons = ReplyKeyboardRemove()
        return text, buttons 


def get_new_url_rus(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        translations = soup.find('table', class_='table table-hover dict-table-t').find_all('tr')
        if str(translations).count('<tr') == 2: # two "tr's" mean that there is only one possible translation for the chosen verb 
            url = soup.find('table', class_='table table-hover dict-table-t').find('a').get('href')
            return 'https://www.pealim.com'+url
        return get_reply(translations)
    except:
        text = 'Кажется, вы допустили ошибку в написании. Попробуйте ещё раз'
        buttons = ReplyKeyboardRemove()
        return text, buttons


def get_reply(rows):
    verbs_heb = []
    verbs_transcription = []
    verbs_rus = []
    for i in range(1, len(rows)):
        verbs_heb.append(rows[i].find('span', class_='menukad').text)
        verbs_transcription.append(rows[i].find('span', class_='dict-transcription').text)
        verbs_rus.append(rows[i].find(class_='dict-meaning').text)
    text_before = "Какой глагол разобрать?"
    verb_options = tabulate([
        [f'{verbs_heb[i]}\n({verbs_transcription[i]})\n{verbs_rus[i]}\n***\n'] for i in range(len(verbs_heb))
    ])
    text_after = "Нажмите нужную кнопку под строкой ввода"
    reply = f'{text_before}\n{verb_options}\n{text_after}'
    buttons = get_buttons(verbs_heb)
    return reply, buttons


def get_buttons(verbs):
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(verbs)):
        buttons = buttons.add(verbs[i])
    return buttons


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    root = soup.find('span', class_='menukad').text
    translation = soup.find('div', class_='lead').text
    binyan = soup.find('b').text

    binyanim = {
        'пааль': 'פָּעַל',
        'пиэль': 'פִּיעֵל',
        'hифъиль': 'הִפְעִיל',
        'hитпаэль': 'הִתְפַּעֵל',
        'нифъаль': 'נִפְעַל',
        'пуаль': 'פֻּעַל',
        'hуфъаль': 'הֻפְעַל'
    }

    binyan_heb = binyanim[binyan.lower()] if binyan.lower() in binyanim.keys() else ''
    
    line = soup.find('table', class_='table table-condensed conjugation-table').find_all('tr')
    forms = {
        "Настоящее время": -1,
        "Прошедшее время": -1,
        "Будущее время": -1,
        "Инфинитив": -1
    }

    for i in range(len(line)):
        for form in forms.keys():
            if form in line[i].text:
                forms[form] = i

    if forms["Настоящее время"] == -1:
        present_hu = "Не употребляется"
        present_hu_transcribed = ""
        present_hi = "Не употребляется"
        present_hi_transcribed = ""
        present_hem = "Не употребляется"
        present_hem_transcribed = ""
        present_hen = "Не употребляется"
        present_hen_transcribed = ""
    else:
        present = line[forms["Настоящее время"]].find_all('span', class_='menukad')
        present_transcribed = line[forms["Настоящее время"]].find_all('div', class_='transcription')
        present_hu = present[0].text
        present_hu_transcribed = present_transcribed[0].text
        present_hi = present[1].text
        present_hi_transcribed = present_transcribed[1].text
        present_hem = present[2].text
        present_hem_transcribed = present_transcribed[2].text
        present_hen = present[3].text
        present_hen_transcribed = present_transcribed[3].text
    
    if forms["Прошедшее время"] == -1:
        past_ani = "Не употребляется"
        past_ani_transcribed = ""
        past_anakhnu = "Не употребляется"
        past_anakhnu_transcribed = ""
        past_ata = "Не употребляется"
        past_ata_transcribed = ""
        past_at = "Не употребляется"
        past_at_transcribed = ""
        past_atem = "Не употребляется"
        past_atem_transcribed = ""
        past_aten = "Не употребляется"
        past_aten_transcribed = ""
        past_hu = "Не употребляется"
        past_hu_transcribed = ""
        past_hi = "Не употребляется"
        past_hi_transcribed = ""
        past_hem_hen = "Не употребляется"
        past_hem_hen_transcribed = ""
    else:
        past_ani = line[forms["Прошедшее время"]].find_all('span', class_='menukad')[0].text
        past_ani_transcribed = line[forms["Прошедшее время"]].find_all('div', class_='transcription')[0].text
        past_anakhnu = line[forms["Прошедшее время"]].find_all('span', class_='menukad')[1].text
        past_anakhnu_transcribed = line[forms["Прошедшее время"]].find_all('div', class_='transcription')[1].text
        past_ata = line[forms["Прошедшее время"] + 1].find_all('span', class_='menukad')[0].text
        past_ata_transcribed = line[forms["Прошедшее время"] + 1].find_all('div', class_='transcription')[0].text
        past_at = line[forms["Прошедшее время"] + 1].find_all('span', class_='menukad')[1].text
        past_at_transcribed = line[forms["Прошедшее время"] + 1].find_all('div', class_='transcription')[1].text
        past_atem = line[forms["Прошедшее время"] + 1].find_all('span', class_='menukad')[2].text
        past_atem_transcribed = line[forms["Прошедшее время"] + 1].find_all('div', class_='transcription')[2].text
        past_aten = line[forms["Прошедшее время"] + 1].find_all('span', class_='menukad')[4].text
        past_aten_transcribed = line[forms["Прошедшее время"] + 1].find_all('div', class_='transcription')[3].text
        past_hu = line[forms["Прошедшее время"] + 2].find_all('span', class_='menukad')[0].text
        past_hu_transcribed = line[forms["Прошедшее время"] + 2].find_all('div', class_='transcription')[0].text
        past_hi = line[forms["Прошедшее время"] + 2].find_all('span', class_='menukad')[1].text
        past_hi_transcribed = line[forms["Прошедшее время"] + 2].find_all('div', class_='transcription')[1].text
        past_hem_hen = line[forms["Прошедшее время"] + 2].find_all('span', class_='menukad')[2].text
        past_hem_hen_transcribed = line[forms["Прошедшее время"] + 2].find_all('div', class_='transcription')[2].text
    
    if forms["Будущее время"] == -1:
        future_ani = "Не употребляется"
        future_ani_transcribed = ""
        future_anakhnu = "Не употребляется"
        future_anakhnu_transcribed = ""
        future_ata = "Не употребляется"
        future_ata_transcribed = ""
        future_at = "Не употребляется"
        future_at_transcribed = ""
        future_atem = "Не употребляется"
        future_atem_transcribed = ""
        future_aten = "Не употребляется"
        future_aten_transcribed = ""
        future_hu = "Не употребляется"
        future_hu_transcribed = ""
        future_hi = "Не употребляется"
        future_hi_transcribed = ""
        future_hem_hen = "Не употребляется"
        future_hem_hen_transcribed = ""

    else:
        future_ani = line[forms["Будущее время"]].find_all('span', class_='menukad')[0].text
        future_ani_transcribed = line[forms["Будущее время"]].find_all('div', class_='transcription')[0].text
        future_anakhnu = line[forms["Будущее время"]].find_all('span', class_='menukad')[1].text
        future_anakhnu_transcribed = line[forms["Будущее время"]].find_all('div', class_='transcription')[1].text
        future_ata = line[forms["Будущее время"] + 1].find_all('span', class_='menukad')[0].text
        future_ata_transcribed = line[forms["Будущее время"] + 1].find_all('div', class_='transcription')[0].text
        future_at = line[forms["Будущее время"] + 1].find_all('span', class_='menukad')[1].text
        future_at_transcribed = line[forms["Будущее время"] + 1].find_all('div', class_='transcription')[1].text
        future_atem = line[forms["Будущее время"] + 1].find_all('span', class_='menukad')[2].text
        future_atem_transcribed = line[forms["Будущее время"] + 1].find_all('div', class_='transcription')[2].text
        future_aten = line[forms["Будущее время"] + 1].find_all('span', class_='menukad')[2].text
        future_aten_transcribed = line[forms["Будущее время"] + 1].find_all('div', class_='transcription')[2].text
        future_hu = line[forms["Будущее время"] + 2].find_all('span', class_='menukad')[0].text
        future_hu_transcribed = line[forms["Будущее время"] + 2].find_all('div', class_='transcription')[0].text
        future_hi = line[forms["Будущее время"] + 2].find_all('span', class_='menukad')[1].text
        future_hi_transcribed = line[forms["Будущее время"] + 2].find_all('div', class_='transcription')[1].text
        future_hem_hen = line[forms["Будущее время"] + 2].find_all('span', class_='menukad')[2].text
        future_hem_hen_transcribed = line[forms["Будущее время"] + 2].find_all('div', class_='transcription')[2].text
    
    if forms["Инфинитив"] == -1:
        infinitive = "Не употребляется"
        infinitive_transcribed = ""
    else:
        infinitive = line[forms["Инфинитив"]].find_all('span', class_='menukad')[0].text
        infinitive_transcribed = line[forms["Инфинитив"]].find_all('div', class_='transcription')[0].text

    return tabulate([
        [f'Инфинитив      ({infinitive_transcribed})      {infinitive}'],
        [f'Биньян             ({binyan})          {binyan_heb}'],
        [f'Корень             {root}'],
        [f'Перевод           {translation}'],
        [],
        ['НАСТОЯЩЕЕ ВРЕМЯ'],
        [f'м.р., ед.ч.      ({present_hu_transcribed})      {present_hu}'],
        [f'ж.р., ед.ч.      ({present_hi_transcribed})      {present_hi}'],
        [f'м.р., мн.ч.      ({present_hem_transcribed})      {present_hem}'],
        [f'ж.р., мн.ч.      ({present_hen_transcribed})      {present_hen}'],

        [],
        ['ПРОШЕДШЕЕ ВРЕМЯ'],
        [f'я                      ({past_ani_transcribed})      {past_ani}'],
        [f'ты (м)             ({past_ata_transcribed})      {past_ata}'],
        [f'ты (ж)             ({past_at_transcribed})      {past_at}'],
        [f'он                    ({past_hu_transcribed})      {past_hu}'],
        [f'она                  ({past_hi_transcribed})      {past_hi}'],
        [f'мы                   ({past_anakhnu_transcribed})      {past_anakhnu}'],
        [f'вы (м)             ({past_atem_transcribed})      {past_atem}'],
        [f'вы (ж)             ({past_aten_transcribed})      {past_aten}'],
        [f'они                  ({past_hem_hen_transcribed})      {past_hem_hen}'],

        [],
        ['БУДУЩЕЕ ВРЕМЯ'],
        [f'я                       ({future_ani_transcribed})      {future_ani}'],
        [f'ты (м)              ({future_ata_transcribed})      {future_ata}'],
        [f'ты (ж)              ({future_at_transcribed})      {future_at}'],
        [f'он                     ({future_hu_transcribed})      {future_hu}'],
        [f'она                   ({future_hi_transcribed})      {future_hi}'],
        [f'мы                    ({future_anakhnu_transcribed})      {future_anakhnu}'],
        [f'вы (м)              ({future_atem_transcribed})      {future_atem}'],
        [f'вы (ж)              ({future_aten_transcribed})      {future_aten}'],
        [f'они                   ({future_hem_hen_transcribed})      {future_hem_hen}']
    ],
        tablefmt='simple')
