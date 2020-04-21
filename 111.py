def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


flag = True
while flag:
    flag_internal = True
    while flag_internal:
        num1 = input("Первое число: ")
        if is_digit(num1) == False:
            print("Неверное значение")
            continue
        break

    while flag_internal:
        num2 = input("Второе число: ")
        if is_digit(num2) == False:
            print("Неверное значение")
            continue
        break

    while flag_internal:
        op = input("Введите операцию: ")
        if not (op == '+' or op == '-' or op == '*' or op == '/'):
            print("Неверное значение")
            continue
        break

    if op == '+':
        print("Ответ: ", float(num1) + float(num2))

    if op == '-':
        print("Ответ: ", float(num1) - float(num2))

    if op == '*':
        print("Ответ: ", float(num1) * float(num2))

    if op == '/':
        print("Ответ: ", float(num1) / float(num2))

    input_errors = 0
    res = ''
    while flag_internal:
        res = input("Хотите начать сначала? (y/n)")
        if input_errors >= 3:
            res = 'n'
            break
        if not (res.lower() == 'y' or res.lower() == 'n'):
            input_errors += 1
            print("Неверное значение")
            continue
        break

    if res.lower() == 'y':
        continue
    if res.lower() == 'n':
        break

