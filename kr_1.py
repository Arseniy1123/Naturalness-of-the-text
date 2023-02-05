# ------------------Проверка для текста выполнения закона Ципфа-Мальдеброта-------------

import nltk # Библиотека nltk (для работы с токенизацией текста)
import string # Подключаем модуль "string" для работы с пунктуацией
import re # Подключаем модуль "re" для работы с регулярными выражениями (sub)
import matplotlib.pyplot as plt # Для построения графиков

# nltk.download('stopwords')

stri = input('Введите имя файла, с которым будет работа в программе: ')
f = open(stri, "r+", encoding="utf-8") # Открытие файла для работы с ним, кодировка прописана
text = f.read()
text = text.lower()
spec_chars = string.punctuation + '\n\t«»-—–…'
spec_chars = re.sub('-', '', spec_chars) # Нужно, чтобы из слова "кое-где" не пропал дефис
text = re.sub('\n', ' ', text)


def remove(text, chars):
    return "".join([ch for ch in text if ch not in chars])
    

# Удаление спец-символов (знаков пунктуации) из текста 
text = remove(text, spec_chars)
# print(text)


# Подключаем функцию "word_tokenize"
# Разделяем текст на токены
from nltk import word_tokenize
text_tokens = word_tokenize(text)

'''
# Подключение списка стоп-слов в русском языке и удаление их из текста
from nltk.corpus import stopwords
russian_stopwords = stopwords.words("russian")
text_tokens = [token.strip() for token in text_tokens if token not in russian_stopwords]
# print("Tokens:", text_tokens)
'''

# Делаем строку из токенов, чтобы работать в дальнейшем со стеммами
s = ''
for token in text_tokens:
    s += token + ' '

# ПОИСК ОСНОВ СЛОВ
# Подключаем систему snowballstemmer для поиска основы каждого слова из строки s
from nltk.stem import SnowballStemmer

def get_stems(text):
    if not text:
        return []
    
    stemmer = SnowballStemmer("russian") # Выбор языка 
    words = word_tokenize(text) # Разделение текста на токены
    stems = [stemmer.stem(w) for w in words] # Определение основы
    return stems

stems = get_stems(s) # Список стемм

# Добавление в список основы каждого слова и вывод этого списка основ
temp = []
for stem in stems:
    if stem not in temp:
        temp.append(stem)
stems = temp
# print("Stems:", stems) # Печать списка стемм (основ) 

# Подключение анализатора pymorphy2 для получения начальных форм слов
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
st = ''
for token in text_tokens:
    p = morph.parse(token)[0] # Делаем полный разбор, и берем первый вариант разбора (условно "самый вероятный", но не факт что правильный)
    st += p.normal_form + ' ' # Строим строку из начальных форм слов
st1 = word_tokenize(st) # Начальные формы слов

# ВЫВОД СЛОВОФОРМ ТЕКСТА
# print(text_tokens)
count_words = len(text_tokens)
# print(count_words)

d1 = {} 
for i in text_tokens:
    if i in d1:
        d1[i] += 1
    else:
        d1[i] = 1

# print(d1)

# ВЫВОД СЛОВОФОРМ ТЕКСТА И ИХ КОЛИЧЕСТВА
d2 = sorted(dict.items(d1), key=lambda v: v[1], reverse=True)

'''
s1 = int(input('Введите, сколько самых частотных словоформ нужно вывести: '))

for i in range(len(d2)):
    if s1 == 0:
        break
    print(i + 1, '. ', d2[i][0], ' ', d2[i][1], sep = '')
    if i + 1 == s1:
        break
'''    
print()
# Добавление в список начальной формы каждого слова и вывод этого списка
lst = []
for token in st1:
    lst.append(token)
st1 = lst
# print("Normal_form:", st1)

# ВЫВОД ЛЕММ ТЕКСТА
diction_1 = {} 
for i in st1:
    if i in diction_1:
        diction_1[i] += 1
    else:
        diction_1[i] = 1

# print(diction_1)

# ВЫВОД ЛЕММ ТЕКСТА И ИХ КОЛИЧЕСТВА
diction_2 = sorted(dict.items(diction_1), key=lambda v: v[1], reverse=True)

'''
s2 = int(input('Введите, сколько самых частотных лемм нужно вывести: '))

for i in range(len(diction_2)):
    if s2 == 0:
        break
    print(i + 1, '. ', diction_2[i][0], ' ', diction_2[i][1], sep = '')
    if i + 1 == s2:
        break
'''
count_words = len(text_tokens)
print('Количество слов в тексте =', count_words) # Количество слов
print('Количество словоформ в тексте =', len(d2)) # Количество словоформ
print('Количество лемм в тексте =', len(diction_2)) # Количество лемм
const = 0.1 # Для закона Ципфа

print()
print('ЧАСТОТЫ СЛОВОФОРМ')

freq_formwords = [] # Относительные частоты словоформ 
rang_formwords = [] # Ранги словоформ
freq_formwords_tsipf = [] # Относительные частоты словоформ (закон Ципфа)
for i in range(len(d2)):
    freq_formwords.append(d2[i][1] / count_words) # Относительная частота словоформы
    rang_formwords.append(i + 1) # Ранг словоформы
    freq_formwords_tsipf.append(const / (i + 1)) # ЗАКОН ЦИПФА
    if i == 500: # Для больших текстов
        break

sub_freq_formwords = [] # Для оценки естественности текста в случае словоформ (прикладная задача)
for i in range(len(diction_2)):
    sub_freq_formwords.append(abs(d2[i][1] / count_words - const / (i + 1)) / (d2[i][1] / count_words))

str1 = int(input('Введите, частоту скольких самых частотных словоформ нужно вывести: '))
# ВЫВОД ЧАСТОТ СЛОВОФОРМ
for i in range(len(d2)):
    if str1 == 0:
        break
    print(i + 1, '. ', d2[i][0], ' - ', d2[i][1] / count_words, sep = '')
    if i + 1 == str1:
        break

print()
print('ЧАСТОТЫ ЛЕММ')

freq_lemmas = [] # Относительные частоты лемм
rang_lemmas = [] # Ранги лемм
freq_lemmas_tsipf = [] # Относительные частоты лемм (закон Ципфа)
for i in range(len(diction_2)):
    freq_lemmas.append(diction_2[i][1] / count_words) # Относительная частота леммы
    rang_lemmas.append(i + 1) # Ранг леммы
    freq_lemmas_tsipf.append(const / (i + 1)) # ЗАКОН ЦИПФА
    if i == 500: # Для больших текстов
        break

sub_freq_lemmas = [] # Для оценки естественности текста в случае лемм (прикладная задача)
for i in range(len(diction_2)):
    sub_freq_lemmas.append(abs(diction_2[i][1] / count_words - const / (i + 1)) / (diction_2[i][1] / count_words))

str2 = int(input('Введите, частоту скольких самых частотных лемм нужно вывести: '))
# ВЫВОД ЧАСТОТ ЛЕММ
for i in range(len(diction_2)):
    if str2 == 0:
        break
    print(i + 1, '. ', diction_2[i][0], ' - ', diction_2[i][1] / count_words, sep = '')
    if i + 1 == str2:
        break

# Подсчет естественности текста (пояснения по подсчету указаны в README)
sum_freq_formwords = sum(sub_freq_formwords)
sum_freq_lemmas = sum(sub_freq_lemmas)
sum_freq_formwords /= count_words
sum_freq_lemmas /= count_words

ans_formwords = (1 - sum_freq_formwords) * 100
ans_lemmas = (1 - sum_freq_lemmas) * 100
ans = (ans_formwords + ans_lemmas) / 2
print()
# print(ans_formwords)
# print(ans_lemmas)
print('Естественность текста = ', round(ans), '%', sep = '')
if ans > 50:
    print('У текста хороший уровень естественности.')
else:
    print('У текста не очень хороший уровень естественности.')

    
# Построение графика зависимости относительной частоты от ранга СЛОВОФОРМЫ
plt.plot(rang_formwords, freq_formwords, label = 'Реальный', color = 'green') # Реальный график (определение - README)
plt.plot(rang_formwords, freq_formwords_tsipf, label = 'Ожидаемый', color = 'yellow') # Ожидаемый график (определение - README)
plt.title('Зависимость относительной частоты от ранга словоформы', color = 'blue') # Заголовок графика
plt.xlabel('Ранг словоформы', color = 'red') # Название оси Х
plt.ylabel('Относительная частота', color = 'red') # Название оси Y
plt.legend() # Для отображения на графике подписей, что означает каждый график
plt.show() # Отображение графика

# Построение графика зависимости относительной частоты от ранга ЛЕММЫ
plt.plot(rang_lemmas, freq_lemmas, label = 'Реальный', color = 'green') # Реальный график (определение - README)
plt.plot(rang_lemmas, freq_lemmas_tsipf, label = 'Ожидаемый', color = 'yellow') # Ожидаемый график (определение - README)
plt.title('Зависимость относительной частоты от ранга леммы', color = 'blue') # Заголовок графика
plt.xlabel('Ранг леммы', color = 'red') # Название оси Х
plt.ylabel('Относительная частота', color = 'red') # Название оси Y
plt.legend() # Для отображения на графике подписей, что означает каждый график
plt.show() # Отображение графика

