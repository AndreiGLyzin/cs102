from bottle import route, run, template, request, redirect
from hackkk import get_news
from sql import News, session

@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)

run(host='localhost', port=8080)
