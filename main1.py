from bs4 import BeautifulSoup # импортируем библиотеку BeautifulSoup
import requests # импортируем библиотеку requests
import unicodedata


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def parse():
    url = 'https://omgtu.ru/general_information/the-structure/the-department-of-university.php' # передаем необходимы URL адрес
    page = requests.get(url) # отправляем запрос методом Get на данный адрес и получаем ответ в переменную
    print(page.status_code) # смотрим ответ
    soup = BeautifulSoup(page.text, "html.parser") # передаем страницу в bs4

    block = soup.findAll('div', class_="main__content") # находим контейнер с нужным классом
    description = ''
    for data in block: # проходим циклом по содержимому контейнера
        if data.find('p'): # находим тег <p>
            description = data.text # записываем в переменную содержание тега


    lines = description.split('\n')
    res = []
    for el in lines:
        if el:
            res.append(remove_control_characters(el).strip("\xa0"))

    with open("kafedras.txt", "w", encoding="utf-8") as f:
        for el in res[1:]:
            if el:
                f.write(el + "\n")


parse()