import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    dates = get_friends(user_id, 'bday')
    sum = 0
    cou = 0
    for i in range(len(dates)):
        sum = sum + (2019 - int(dates[i]))
        cou += 1
    if cou == 0:
        return 'Не достаточно данных'
    else:
        return sum / cou