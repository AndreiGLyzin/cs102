import requests
import config
import telebot
import datetime
from bs4 import BeautifulSoup


bot = telebot.TeleBot('1019738386:AAG5G6de4PTjFkyrOGRw9eLLW0XhCVBy6GY')
telebot.apihelper.proxy = {'https': 'https://141.125.82.106:80'}


def get_page(group, week):
    if week == '0' or week is None:
        week = ''
    else:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page

def chet_nechet():
    a = datetime.date.today().isocalendar()
    return (a[1] + 1) % 2 + 1

def parse_schedule(web_page, day_number):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": f"{day_number}day"})
    if schedule_table == None:
        return None, None, None

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list




@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    try:
        try:
            day, group, chet = message.text.split()
        except ValueError:
            day, group = message.text.split()
            chet = 0
        day = day[1:]
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for i in range(len(days)):
            if days[i] == day:
                day = i + 1
                break
        web_page = get_page(group, chet)
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day)
        resp = ''
        if times_lst != None:
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        else:
            resp = 'Нет пар'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except ValueError:
        r = ''
        return
    except TypeError:
        r = ''
        return


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    try:
        _, group = message.text.split()
    except ValueError:
        bot.send_message(message.chat.id, 'Неверное сообщение')
        return
    hour_now = datetime.datetime.now().hour
    minut_now = datetime.datetime.now().minute
    day = datetime.date.today().isoweekday()
    today_day = day
    chet = chet_nechet()
    web_page = get_page(group, chet)
    resp = ''
    while resp == '':
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day)
        if times_lst == None:
            day += 1
            if day == 8:
                day = 1
                chet = chet % 2 + 1
                web_page = get_page(group, chet)
            if day == today_day:
                bot.send_message(message.chat.id, 'Группа не существует')
                return
            continue
        if len(times_lst) > 0:
            for i in range(len(times_lst)):
                time = times_lst[i]
                hour = ''
                mint = ''
                hour += time[0]
                hour += time[1]
                mint += time[3]
                mint += time[4]
                if hour_now <= int(hour):
                    if minut_now <= int(mint):
                        resp += '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
                        bot.send_message(message.chat.id, resp, parse_mode='HTML')
                        return
                if today_day != day:
                    resp += '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    return
        day += 1
        if day == 8:
            day = 1
            chet = chet % 2 + 1
            web_page = get_page(group, chet)
        if day == today_day:
            bot.send_message(message.chat.id, 'Группа не существует')
            return



@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    try:
        now = datetime.datetime.now()
        tom = datetime.date.today().weekday() + 2
        _, group = message.text.split()
        chet = chet_nechet()
        if tom == 8:
            tom = 1
            if chet == 1:
                chet += 1
            else:
                chet -= 1
        _, group = message.text.split()
        web_page = get_page(group, chet)
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, tom)
        resp = ''
        if times_lst != None:
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        else:
            resp = 'Завтра нет пар, либо неверно набрана группа'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except ValueError:
        r = ''
        return
    except TypeError:
        r = ''
        return

@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    try:
        try:
            day, group, chet = message.text.split()
        except ValueError:
            try:
                day, group = message.text.split()
                chet = 0
            except ValueError:
                resp = 'Нет названия группы'
                bot.send_message(message.chat.id, resp, parse_mode='HTML')
                return
        days = [1, 2, 3, 4, 5, 6]
        naz = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        web_page = get_page(group, chet)
        resp = ''
        for i in range(6):
            resp = ''
            times_lst, locations_lst, lessons_lst = \
                parse_schedule(web_page, days[i])
            if times_lst != None:
                resp += '<b>{}</b>\n\n'.format(naz[i])
                for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                    resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
                bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except ValueError:
        r = ''
        return
    except TypeError:
        r = ''
        return


if __name__ == '__main__':
    bot.polling(none_stop=True)

