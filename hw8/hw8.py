from csv import DictReader, DictWriter
from os.path import exists


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_info():
    while True:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Слишком короткое имя")
            second_name = input("Введите фамилию: ")
            if len(second_name) < 4:
                raise NameError("Слишком короткая фамилия")
            phone_number = input("Введите номер телефона: ")
            if len(phone_number) < 11:
                raise NameError("Слишком короткий номер телефона")
        except NameError as err:
            print(err)
        else:
            return [first_name, second_name, phone_number]


def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['№', 'first_name', 'second_name', 'phone_number'])
        f_w.writeheader()


def write_file(file_name):
    if not validate_files(file_name):
        return

    user_data = get_info()
    res = read_file(file_name)
    if res is None:
        count = 1
    else:
        count = len(res) + 1
    new_obj = {'№': str(count), 'first_name': user_data[0], 'second_name': user_data[1], 'phone_number': user_data[2]}
    res.append(new_obj)
    standard_write(file_name, res)
    print("Данные успешно записаны.")


def read_file(file_name):
    if not validate_files(file_name):
        return

    with open(file_name, encoding='utf-8') as data:
        f_r = DictReader(data)
        return list(f_r)


def print_file(file_name):
    if not validate_files(file_name):
        return

    records = read_file(file_name)
    if records:
        for record in records:
            print(f"{record['№']}. {record['first_name']} {record['second_name']}: {record['phone_number']}")
    else:
        print("Файл пуст.")


def remove_row(file_name):
    if not validate_files(file_name):
        return

    res = read_file(file_name)
    row_numbers = [int(num) for num in input("Введите через пробел номера строк для удаления: ").split() if
                   num.isdigit() and 1 <= int(num) <= len(res)]

    if not row_numbers:
        print("Нет корректных номеров строк для удаления.")
        return

    row_numbers_set = set(row_numbers)
    remaining_rows = [row for row in res if int(row['№']) not in row_numbers_set]

    for i, row in enumerate(remaining_rows):
        row['№'] = str(i + 1)

    standard_write(file_name, remaining_rows)
    print(f"Строки с номерами {', '.join(map(str, row_numbers))} удалены.")


def standard_write(file_name, res):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['№', 'first_name', 'second_name', 'phone_number'])
        f_w.writeheader()
        f_w.writerows(res)


def copy_data(file_name):
    if not validate_files(file_name):
        return

    command = input("Введите 'cf' для копирования файла или 'cr' для копирования строк: ").lower()
    if command == "cf":
        copy_file(file_name)
    elif command == "cr":
        copy_row(file_name)
    else:
        print("Некорректная команда, попробуйте снова.")


def copy_file(file_name):
    if not validate_files(file_name):
        return

    copied_file_name = input("Введите название нового файла: ") + ".csv"
    data = read_file(file_name)
    standard_write(copied_file_name, data)
    print(f"Данные успешно скопированы из {file_name} в {copied_file_name}")


def copy_row(file_name):
    copied_file_name = input("Введите название файла в который хотите скопировать строку: ") + ".csv"

    if not validate_files(file_name):
        return

    res = read_file(file_name)
    copied_res = read_file(copied_file_name)
    row_numbers = [int(num) - 1 for num in input(f"Введите номера строк через пробел, которые хотите скопировать из "
                                                 f"{file_name} в {copied_file_name}: ").split() if num.isdigit() and
                   1 <= int(num) <= len(res)]
    for row_number in row_numbers:
        copied_row = res[row_number]
        copied_row['№'] = str(len(copied_res) + 1)
        copied_res.append(copied_row)
    standard_write(copied_file_name, copied_res)
    print("Строки успешно скопированы.")


def find_record(file_name):
    if not validate_files(file_name):
        return

    criterion = input("Введите характеристику для поиска (№, first_name, second_name, phone_number): ")
    if criterion not in ['№', 'first_name', 'second_name', 'phone_number']:
        print("Некорректная характеристика для поиска.")
        return

    value = input(f"Введите значение для поиска по {criterion}: ").split()
    records = read_file(file_name)
    results = [record for record in records if record[criterion] in value]

    if results:
        for result in results:
            print(f"{result['№']}. {result['first_name']} {result['second_name']}: {result['phone_number']}")
    else:
        print("Запись не найдена.")


def validate_files(*files):
    all_files_exist = True
    for file in files:
        if not exists(file):
            print(f"Файл {file} отсутствует, пожалуйста, создайте файл.")
            command = input(f"Хотите создать файл {file}? Напишите Да или Нет: ").lower()
            if command == "да":
                create_file(file)
            else:
                all_files_exist = False
    return all_files_exist


def main():
    file_name = "phonebook.csv"
    commands = {
        "q": lambda: print("До свидания!"),
        "w": lambda: write_file(file_name),
        "r": lambda: print_file(file_name),
        "d": lambda: remove_row(file_name),
        "c": lambda: copy_data(file_name),
        "f": lambda: find_record(file_name)
    }

    while True:
        command = input("\n1. Для выхода из программы - 'q'\n2. Для записи данных - 'w'\n3. Для "
                        "чтения данных - 'r'\n4. Для удаления данных - 'd'\n5. Для копирования - 'c'\n6. Для "
                        "поиска данных - 'f'\nВведите команду: ").lower()
        if command in commands:
            if command == "q":
                commands[command]()
                break
            else:
                commands[command]()
        else:
            print("Некорректная команда, попробуйте снова.")


if __name__ == "__main__":
    main()
