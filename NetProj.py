import telebot
from random import choice

token = ''

bot = telebot.TeleBot(token)

HELP = """/help - напечатать справку о программе.
/add - добавить задачу в список.
/show - напечатать все существующие задачи.
/random - добавить на сегодня рандомную задачу.
/exit - выйти из программы.

Параметры ввода команд:
/help
/add дата(сегодня, завтра, цифра+месяц) задача(через пробел) @категория_дела(обязательно с @)
/show даты(через пробел)
/random
"""

RANDOM_TASKS = ["погамать в Ов2", "поиграть в бг3", "сделать репетиторскую домашку", "покушац", "принять ванку"]

tasks = {}


def add_todo(date, task, categ):
    date = date.lower()
    if date not in tasks:
        tasks[date] = [task]
        tasks[date].append(categ)

    else:
        tasks[date].append(task)
        tasks[date].append(categ)


@bot.message_handler(commands=['help', "start"])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['add'])
def add(message):
    start_tail, end_tail = 2, 3
    r = _, date, tail, *categ = message.text.split(sep=" ")
    if date.isdigit():
        date = f"{str(r[1])} {str(r[2])}"
        start_tail = 3
    for i in range(len(r)):
        if r[i][0] == "@":
            categ = r[i]
            end_tail = i - 1
    tail = r[start_tail:end_tail + 1]

    if len("".join(tail)) < 3:
        bot.send_message(message.chat.id, f'Задача слишком короткая, попробуйте снова')
    else:
        add_todo(date, tail, categ)
        bot.send_message(message.chat.id, f'Задача {" ".join(tail)} добавлена на дату {date}')


@bot.message_handler(commands=["show"])
def print_(message):
    date = (" ".join(message.text.split()[1:])).split(sep=" ")
    while date:
        if date[0].isdigit():
            date[0] = f"{date[0]} {date[1]}"
            date.remove(date[1])
        if date[0] in tasks:
            t = f"{date[0]}:\n"
            tr = tasks[date[0]]
            for i in range(len(tr) - 1):
                if i % 2 == 0:
                    t += f'- {" ".join(tr[i])} - {tr[i + 1]} \n'
            date.remove(date[0])
        else:
            t = f'Даты {date[0]} нет в вашем списке задач ;('
            date.remove(date[0])
        bot.send_message(message.chat.id, t)


@bot.message_handler(commands=["random"])
def random(message):
    task_r = choice(RANDOM_TASKS)
    add_todo("сегодня", task_r.split(), "@random_task")
    bot.send_message(message.chat.id, f"Задача {task_r} добавлена на сегодня!")


bot.polling(none_stop=True)
