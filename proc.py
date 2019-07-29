#!/usr/bin/python3

import cgi, sys

"""
Скрипт обработки запроса на согласование
Фактически он нужен для записи данных о согласовании в базу данных
Это делается в функции (которая здесь не реализована)
"""
def addSignDate( id, login ):
    """ добавляет информацию о согласовании страницы по ее имени """
    return None

# В скрипт передаются параметры 
form = cgi.FieldStorage()
signee = form["signee"].value # логин согласующего
id = form["id"].value         # имя страницы, которую необходимо согласовать

addSignDate(id, signee)       # фиксируем факт согласования


# отрисовываем HTML с автоматическим редиректом (если уменьшить задержку - будет совсем незаметно)
resHtml = """
<html>
<head>
<meta http-equiv="refresh" content="5;url=http://wiki.alfastrah.ru/display/DIT/{0}">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Согласование отработано</title>
</head>
<body>
<p>Запрос на согласование страницы <b>{0}</b> пользователем <b>{1}</b> обработан.
<br>Сейчас Вы будете перенаправлены обратно на страницу...</p>
<a href="http://wiki.alfastrah.ru/display/DIT/{0}">перейти вручную</a>
</body>
</html>
""".format(id, signee)

sys.stdout.buffer.write(b'Content-Type: text/html;charset=utf-8\n\n')
sys.stdout.buffer.write(resHtml.encode("utf-8"))
