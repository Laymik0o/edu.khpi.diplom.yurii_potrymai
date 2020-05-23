from fuzzywuzzy import fuzz
from matplotlib import pyplot as plt
from datetime import datetime


# Запоминаем время старта
def set_time_start():
    return datetime.now()


# Получить время работы
def get_time_end(start_time):
    return datetime.now() - start_time


# Отсеить короткие тексты
def check_len(text_1, text_2):
    return len(text_1) > 200 and len(text_2) > 200


# Режит текст на куски нужной длины
def cut_text(text_1, count):
    return [''.join(i) for i in grouper(text_1, count)]


# Разбивает текст на равные части
def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


# Отрисовка гистограмы
def create_gisto(dict_result):
    x_data = dict_result.keys()
    y_data = dict_result.values()
    plt.bar(x_data, y_data)
    plt.title("Гістограма схожості текстів згідно кожного методу")
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()


# Показывать ли гистограму
def show_gisto(obj, dict_result):
    state = obj.checkBox.isChecked()
    if state is True:
        create_gisto(dict_result)


# Самое обычное сравнение в лоб
def use_ratio(text_1, text_2):
    if check_len(text_1, text_2):
        text_1_groups = cut_text(text_1, 10)
        text_2_groups = cut_text(text_2, 10)
        tmp_dict = dict(zip(text_1_groups, text_2_groups))
        list_pros = list()
        for key in tmp_dict:
            list_pros.append(fuzz.ratio(key, tmp_dict[key]))
        return int(sum(list_pros)/len(list_pros))
    else:
        return fuzz.ratio(text_1, text_2)


# Частичное сравнение
def use_partial_ratio(text_1, text_2):
    if check_len(text_1, text_2):
        text_1_groups = cut_text(text_1, 30)
        text_2_groups = cut_text(text_2, 30)
        tmp_dict = dict(zip(text_1_groups, text_2_groups))
        list_pros = list()
        for key in tmp_dict:
            list_pros.append(fuzz.partial_ratio(key, tmp_dict[key]))
        return int(sum(list_pros) / len(list_pros))
    else:
        return fuzz.partial_ratio(text_1, text_2)


# Слова сравниваются друг с другом, независимо от регистра или порядка
def use_token_sort_ratio(text_1, text_2):
    if check_len(text_1, text_2):
        text_1_groups = cut_text(text_1, 50)
        text_2_groups = cut_text(text_2, 50)
        tmp_dict = dict(zip(text_1_groups, text_2_groups))
        list_pros = list()
        for key in tmp_dict:
            list_pros.append(fuzz.token_sort_ratio(key, tmp_dict[key]))
        return int(sum(list_pros) / len(list_pros))
    else:
        return fuzz.token_sort_ratio(text_1, text_2)


# Приравнивает строки, если их отличие заключается в повторении слов.
def use_token_set_ratio(text_1, text_2):
    if check_len(text_1, text_2):
        text_1_groups = cut_text(text_1, 50)
        text_2_groups = cut_text(text_2, 50)
        tmp_dict = dict(zip(text_1_groups, text_2_groups))
        list_pros = list()
        for key in tmp_dict:
            list_pros.append(fuzz.token_set_ratio(key, tmp_dict[key]))
        return int(sum(list_pros) / len(list_pros))
    else:
        return fuzz.token_set_ratio(text_1, text_2)


# Все сразу для демонстрации эфективност
def use_all(text_1, text_2):
    list_result = list()
    list_result.append(use_ratio(text_1, text_2))
    list_result.append(use_partial_ratio(text_1, text_2))
    list_result.append(use_token_sort_ratio(text_1, text_2))
    list_result.append(use_token_set_ratio(text_1, text_2))
    list_ways = ['Посимвольне порівняння', 'Пошук оптимальної частини', 'Не зважаючи на порядок слів',
                 'Ігноруючи повторення слів та розділові знаки']
    return dict(zip(list_ways, list_result))


# Выполнение основной задачи
def start_work(obj):
    if obj.comboBox.currentText() == 'Посимвольне порівняння. Враховуе регістр':
        start_time = set_time_start()
        result = use_ratio(obj.plainTextEdit_1.toPlainText(), obj.plainTextEdit_2.toPlainText())
        obj.listWidget.clear()
        obj.listWidget.addItem('Тексти схожі на {result}%'.format(result=result))
        obj.listWidget.addItem('Виконано за {time} c'.format(time=get_time_end(start_time)))
    elif obj.comboBox.currentText() == 'Пошук оптимальної частини. Враховуе регістр':
        start_time = set_time_start()
        result = use_partial_ratio(obj.plainTextEdit_1.toPlainText(), obj.plainTextEdit_2.toPlainText())
        obj.listWidget.clear()
        obj.listWidget.addItem('Тексти схожі на {result}%'.format(result=result))
        obj.listWidget.addItem('Виконано за {time} c'.format(time=get_time_end(start_time)))
    elif obj.comboBox.currentText() == 'Не зважаючи на порядок слів та регістр':
        start_time = set_time_start()
        result = use_token_sort_ratio(obj.plainTextEdit_1.toPlainText(), obj.plainTextEdit_2.toPlainText())
        obj.listWidget.clear()
        obj.listWidget.addItem('Тексти схожі на {result}%'.format(result=result))
        obj.listWidget.addItem('Виконано за {time} c'.format(time=get_time_end(start_time)))
    elif obj.comboBox.currentText() == 'Ігноруючи повторення слів та розділові знаки':
        start_time = set_time_start()
        result = use_token_set_ratio(obj.plainTextEdit_1.toPlainText(), obj.plainTextEdit_2.toPlainText())
        obj.listWidget.clear()
        obj.listWidget.addItem('Тексти схожі на {result}%'.format(result=result))
        obj.listWidget.addItem('Виконано за {time} c'.format(time=get_time_end(start_time)))
    else:
        start_time = set_time_start()
        dict_result = use_all(obj.plainTextEdit_1.toPlainText(), obj.plainTextEdit_2.toPlainText())
        obj.listWidget.clear()
        for key in dict_result:
            item = '{sposob} -> {result}%'.format(sposob=key, result=dict_result[key])
            obj.listWidget.addItem(item)
        obj.listWidget.addItem('Виконано за {time} c'.format(time=get_time_end(start_time)))
        show_gisto(obj, dict_result)
