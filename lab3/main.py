from Encryption import *
import io

crypt = None
ans = -1

def main_menu():
    print("Главное меню")
    print("   1) Сгенерировать ключ")
    print("   2) Зашифровать")
    print("   3) Расшифровать")
    print("   4) Выйти")

    crypt = None

    ans = -1
    while ans == -1:
        ans = int(input("> "))
        if not(ans == 1 or ans == 2 or ans == 3 or ans == 4):
            ans = -1
    print("\n")
    if ans == 1:
        gen_key()
    elif ans == 2:
        enc()
    elif ans == 3:
        decr()
    elif ans == 4:
        exit(0)

def gen_key():
    print("Сгенерировать ключ")
    print("   1) Замены")
    print("   2) Перестановки")
    print("   3) Гаммирование")
    
    ans = -1
    while ans == -1:
        ans = int(input("> "))
        if not(ans == 1 or ans == 2 or ans == 3):
            ans = -1 
    if ans == 1:
        gen_key_rep()
    elif ans == 2:
        gen_key_tra()
    elif ans == 3:
        gen_key_gam()        

def gen_key_rep():
    print("\n")
    print("Генерация ключа (замены)")
    crypt = Replacement()
    while True:
        path = input("   Введите путь к алфавиту: ")

        if path.find(".alph") == -1:
            print("   Некорректный путь.")
            continue
        else:
            break

    f_alph = open(path, "r")
    alph = Alphabet(f_alph.read())
    f_alph.close()

    key = crypt.GenerateKey(alph)

    print("   Ключ сгенерировн.")

    f_key = open("replacement.key", "w")
    f_key.write(key.to_str())
    f_key.close()

    print("   Вывести значение ключа? (y/n)")
    a = input("> ")
    if a == 'y':
        print("   Ключ: " + key.to_str())
    print("   Ключ сохранен в файл replacement.key")
    print("\n")
    main_menu()

def gen_key_tra():
    print("\n")
    print("Генерация ключа (перестановки)")
    crypt = Transposition()
    n = 0
    while True:
       k = input("   Введите размер блока перестановки: ")
       if k.isdigit():
           n = int(k)
           break
       else:
           print("   Некорректное значение.")   

    key = crypt.GenerateKey(n)
    print("   Ключ сгенерировн.")

    f_key = open("transposition.key", "w")
    f_key.write(key.to_str())
    f_key.close()

    print("   Вывести значение ключа? (y/n)")
    a = input("> ")
    if a == 'y':
        print("   Ключ: " + key.to_str())
    print("   Ключ сохранен в файл transposition.key")
    print("\n")
    main_menu()

def gen_key_gam():
    print("\n")
    print("Генерация ключа (гаммирование)")
    crypt = Gamming()
    n = 0
    while True:
       k = input("   Введите размер ключа: ")
       if k.isdigit():
           n = int(k)
           break
       else:
           print("   Некорректное значение.")   

    key = crypt.GenerateKey(n)
    print("   Ключ сгенерировн.")

    f_key = open("gamming.key", "w")
    f_key.write(key.to_str())
    f_key.close()

    print("   Вывести значение ключа? (y/n)")
    a = input("> ")
    if a == 'y':
        print("   Ключ: " + key.to_str())
    print("   Ключ сохранен в файл gamming.key")
    print("\n")
    main_menu()

def enc():
    print("Зашифровать")
    print("   1) Замены")
    print("   2) Перестановки")
    print("   3) Гаммирование")
    ans = -1
    while ans == -1:
        ans = int(input("> "))
        if not(ans == 1 or ans == 2 or ans == 3 or ans == 4):
            ans = -1
    print("\n")
    if ans == 1:
        enc_file(0)
    elif ans == 2:
        enc_file(1)
    elif ans == 3:
        enc_file(2)

def enc_file(enc_type):
    s = ""

    if enc_type == 0:
        crypt = Replacement()
        s = "замены"
    elif enc_type == 1:
        crypt = Transposition()
        s = "перестановок"
    elif enc_type == 2:
        crypt = Gamming()
        s = "гаммирования"

    print("Шифрование методом " + s)
    
    txt = ""
    key = None

    t_path = input("   Введите путь к файлу, который надо зашифровать: ")
    f_txt = open(t_path, "r")
    txt = f_txt.read()
    f_txt.close()

    while True:
        path = input("   Введите путь к файлу ключа: ")
        if path.find(".key") == -1:
           print("   Некорректный путь.")
           continue
        else:
            try:
                f_key = open(path, "r")
                key = Key(f_key.read())
                f_key.close()
            except StringIsNotAKeyException:
                print("   Некорректный файл ключа.")
            if key.encode_type == enc_type:
                break
            else:
                print("   Ключ не подходит для данного метода шифрования.")

    enc_txt = crypt.Encrypt(txt, key)
    print("   Текст зашифрован.")
    f_enc = None
    f_enc = open(t_path + ".encrypt", "w")
    f_enc.write(enc_txt)
    f_enc.close()
    print("   Текст сохранен в файл " + t_path + ".encrypt")
    print("\n")
    main_menu()

def decr():
    print("Расшифровать")
    print("   1) Замены")
    print("   2) Перестановки")
    print("   3) Гаммирование")
    ans = -1
    while ans == -1:
        ans = int(input("> "))
        if not(ans == 1 or ans == 2 or ans == 3 or ans == 4):
            ans = -1
    print("\n")
    if ans == 1:
        decr_file(0)
    elif ans == 2:
        decr_file(1)
    elif ans == 3:
        decr_file(2)

def decr_file(enc_type):
    s = ""

    if enc_type == 0:
        crypt = Replacement()
        s = "замены"
    elif enc_type == 1:
        crypt = Transposition()
        s = "перестановок"
    elif enc_type == 2:
        crypt = Gamming()
        s = "гаммирования"

    print("Расшифровать файл (метод " + s + ")")

    txt = ""
    key = None

    t_path = ""
    while True:
        t_path = input("   Введите путь к файлу с шифротекстом: ")
        if t_path.find(".encrypt") == -1:
            print("   Некорректный путь.")
        else:
            break

    f_txt = open(t_path, "r")
    txt = f_txt.read()
    f_txt.close()

    while True:
        path = input("   Введите путь к файлу ключа: ")
        if path.find(".key") == -1:
           print("   Некорректный путь.")
           continue
        else:
            try:
                f_key = open(path, "r")
                key = Key(f_key.read())
                f_key.close()
            except StringIsNotAKeyException:
                print("   Некорректный файл ключа.")
            if key.encode_type == enc_type:
                break
            else:
                print("   Ключ не подходит для данного метода шифрования.")

    enc_txt = crypt.Decrypt(txt, key)
    print("   Текст расшифрован.")
    f_enc = None    
    f_enc = open("decrypted.txt", "w")
    f_enc.write(enc_txt)
    f_enc.close()
    print("   Текст сохранен в файл decrypted.txt")
    print("\n")
    main_menu()

main_menu()