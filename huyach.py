import rusyllab
import os
import random
import telebot
from PIL import Image, ImageDraw, ImageFont

conc = "ЕЁЮЯЙеёюяй"
vow = "АЭЫОУИаэыоуи"
cons = "БВГДЖЗКЛМНПРСТФХЦЧШЩбвгджзклмнпрстфхцчшщ"
#список всех слогов
##syllables_1 = rusyllab.split_words([word])


def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size

    resized_image = original_image.resize(size)
    width, height = resized_image.size
    resized_image.show()
    resized_image.save(output_image_path)

def check_vow(syllables, word):
    syl = syllables[0]
    first_cons = syl[1:]

    if len(syllables) > 1:
        syllable1 = syllables[1]
        tmp = syllables[:]
        tmp[0] = ""
        raword = tmp
    else:
        syllable1 = " "
        raword = ""
    if syl[0] in conc:
        str = "ху" + "".join(syllables)
        return str.lower()
    elif syl[0] in "Аа":
        str = "хуя" + "".join(first_cons) + "".join(syllables[1:]) ##+ "".join(raword)
        return str.lower()
    elif syl[0] in "Оо":
        str = "хуё"+ "".join(first_cons) + "".join(syllables[1:]) ##+ "".join(raword)
        return str.lower()
    elif syl[0] in "Ээ":
        str = "хуе"+ "".join(first_cons) + "".join(syllables[1:]) ##+ "".join(raword)
        return str.lower()
    elif syl[0] in "ЫИыи":
        str = "хуи" + "".join(first_cons) + "".join(syllables[1:]) ##+ "".join(raword)
        return str.lower()
##    elif syl[0] in "Уу" and syllable1[0] in cons:
##        str = "хуе" + "".join(first_cons) + "".join(raword)
##        return str.lower()
    elif syl[0] in "Уу":
        str = "хую" + "".join(first_cons) + "".join(syllables[1:]) ##"".join(syllables)
        return str.lower()
   
    else:
        return "Ты че, сука, самый умный?"


def check_cons(syllables, word):
    syl = syllables[0]
    tmp = list(syl[:])
    excons = ""
    i = 0
    for let in tmp:
        if let in cons:
            tmp[i] = ""
            i = i + 1
        if i >= 3 and len(syllables) < 2:
            return "хуе" + "".join(syllables)
        if let in conc or let in vow:
            break
    excons = "".join(tmp) + "".join(syllables[1:])
    new_word = rusyllab.split_words([excons])
    result = check_vow(new_word, word)
    return result

def check(word):
    if (len(word.split()) > 1):
        return "Слишком много слов"
    elif len(word) == 1 and word in cons:
        return 'чё'
    elif word == "/start":
        return "Здаров, епт"
    elif(len(word) < 20):
        syllables = rusyllab.split_words([word])
        syl = syllables[0]
        if syl[0] in cons:
            return check_cons(syllables, word)
        else:
            return check_vow(syllables, word)
    else:
        return "Браток, помедленней"



def resize_folder():

    for image in os.listdir('Images'):
        image_path = 'Images/{}{}'.format(os.path.splitext(image)[0], os.path.splitext(image)[1])
        print(image_path)
        image = Image.open(image_path)
        image = image.resize((800,600), Image.ANTIALIAS)
        os.remove(image_path)
        image.save(image_path)


def make_mem(string):
    directory = "Images"
    font = ImageFont.truetype("Attractive-Heavy.ttf", 60)
    image = Image.open(os.path.join(directory, random.choice(os.listdir(directory))))
    drawer = ImageDraw.Draw(image)
    size = font.getsize(string)
    print(str(size))
    drawer.text(((800 - size[0])/2, 500), string,(255,255,255), font)
    return image
##resize_image("Images/1.jpg", "Images/", (800,600))



token = '1094070345:AAH841DzNZkHF7VY_cPKukK2KhAh3LtJfOA'
bot = telebot.TeleBot(token)
##resize_folder()
@bot.message_handler(content_types=['text'])
def send_huya(message):
    text = message.text
    print(text)
    bot.send_photo(message.chat.id, make_mem(check(text)))

bot.polling(none_stop = True)
##word = input()
##print(check("мгла"))
