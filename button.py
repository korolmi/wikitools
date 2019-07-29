#!/usr/bin/python3

import cgi, sys

"""
Скрипт инициации согласования.
Получает следующие параметры (через GET запрос)
"""
form = cgi.FieldStorage()
signee = form["signee"].value # логин согласующего (кто должен согласовать)
actual = form["actual"].value # логин текущего пользователя (в жизни получается автоматом)
id = form["id"].value # имя страницы, которую необходимо согласовать (в жизни получается автоматом)

# в этом модуле есть функция логина в Confluence
from login import *

# утилитные функции - черновая реализация
def getUserName ( token, user ):
    """ переводим по адресной книге Confluence логин пользователя в полное имя """

    if signee=="boss":
        return "Большой Босс"
    
    if server.confluence2.hasUser(token, user):
        userName = server.confluence2.getUser(token, user)["fullname"]
    else:
        userName = "(unknown user)"

    return userName
    
def getSignDate ( id, signee ):
    """ получает из базы данных информацию о дате согласования страницы согласующим """
    
    if signee=="boss":
        return "Jan 01, 2019"
    return ""

def wikiLogin():
    """ login в confluence - лучше использовать техническую учетку, плохо, что виден пароль... """

    if sys.version_info.major<3:
        server = xmlrpclib.ServerProxy('http://172.16.108.41/rpc/xmlrpc')
    else:
        server = xmlrpc.client.ServerProxy('http://172.16.108.41/rpc/xmlrpc')
    token = server.confluence2.login('имя пользователя', 'пароль')

    return server, token

# шаблон страницы - начало
resHtml = """
<!DOCTYPE HTML>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
<form name="input" action="http://172.16.108.216/misc/sign_proc.py" method="get">
"""

server, token = wikiLogin()           # логинимся в Confluence
userName = getUserName(token, signee) # получаем имя текущего пользователя по его логину

res = getSignDate(id, signee)         # получаем дату согласования страницы
if res: # согласование было получено
    resHtml += "<p>Согласовано ({0}, {1})</p>".format(userName, res) # отрисовываем текст
else:   # согласования не было
    if signee.lower() == actual.lower(): # текущий пользователь совпадает с согласующим - отрисовываем кнопку
        resHtml += '<input type="hidden" name="id" value="{0}">'.format(id)
        resHtml += '<input type="hidden" name="signee" value="{0}">'.format(signee)
        resHtml += "Требуется Ваше согласование <input type=\"submit\" value=\"{0}\">".format(userName)
    else: # текущий пользователь не есть согласующий - отрисовываем неактивную кнопку
        resHtml += "Требуется согласование пользователем <input disabled type=\"submit\" value=\"{0}\">".format(userName)

resHtml += "</form></body></html>"

# выводим собранный HTML
sys.stdout.buffer.write(b'Content-Type: text/html;charset=utf-8\n\n')
sys.stdout.buffer.write(resHtml.encode("utf-8"))
