import requests
import time

import config


def zapr(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = timeout / 2
    while True:
        error = params
        if not error:
            # ok, got response
            b = requests.get(url)
            return b
            break

        # error happened, pause between requests
        time.sleep(delay)

        # calculate next delay
        delay = min(delay * backoff_factor, timeout)
        delay = delay + (delay * 0.1)
    # PUT YOUR CODE HERE


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = config.VK_CONFIG['domain']
    access_token = config.VK_CONFIG['access_token']
    v = config.VK_CONFIG['version']
    fields = 'bdate'
    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = zapr(query)
    years = []
    coun = response.json()['response']['count']
    for i in range(coun):
        try:
            years.append(response.json()['response']['items'][i]['bdate'])
        except:
            continue
    for i in range(len(years)):
        years[i] = years[i][-4:]
    otvet = []
    for i in range(len(years)):
        if years[i][1] != '.' and years[i][2] != '.':
            otvet.append(years[i])
    return otvet