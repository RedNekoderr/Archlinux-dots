import json

words_list = []

with open('whitelist.txt', encoding='utf-8') as read:
    for i in read:
        word = i.lower().split('\n')[0]
        if word != '':
            words_list.append(word)

with open('whitelist.json', 'w', encoding='utf-8') as write:
    json.dump(words_list, write)
