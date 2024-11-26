import json
import os
import sys

class library:

    def __init__(self):

        self.file_name = 'library.json'
        if sys.platform == 'linux':
            self.wash_command = 'tput clear'
        elif 'win' in sys.platform:
            self.wash_command = 'cls'
        else:
            self.wash_command = 'clear'


        if not self.file_name in os.listdir('.'):
            open(self.file_name,'w').close()

        with (open(self.file_name, 'r') as book_file):
            try:
                self.books = json.load(book_file)
            except Exception as lol:
                print(lol)
                self.books = {'list_books':[]}

        self.home_library()

    def home_library(self, exception_input:bool=False):

        os.system(self.wash_command)

        print('================================')
        print('Система управления библиотекой')
        print('================================')
        print('1. Добавление книги')
        print('2. Удаление книги')
        print('3. Поиск книг')
        print('4. Отображение всех книг')
        print('5. Изменение статуса книги')
        print('================================')

        if exception_input:
            print('номер опции веден не правильно! попробуйте еще раз\n')
        print('для выбора опции ввдите ее номер и нажмите <<ENTER>>\n')

        try:
            number_func = input('=> ')
        except KeyboardInterrupt:
            os.system(self.wash_command)
            exit()

        try:
            if not number_func in ('1', '2', '3', '4', '5'):
                raise ValueError()
            if number_func == '1':
                self.add_book()
            elif number_func == '2':
                self.del_book()
            elif number_func == '3':
                self.find_book()
            elif number_func == '4':
                self.show_book()
            elif number_func == '5':
                self.change_status_book()
        except ValueError:
            self.home_library(True)

    def hablon(method:'декоратор для методов') -> 'function':
        def func(self, *args, **kwargs):

            os.system(self.wash_command)

            if not any(self.books['list_books']):
                print('===========================')
                print('В библиотеки нет книг')
                print('===========================')
            else:
                try:
                    method(self, *args, **kwargs)
                except Exception as ex:
                    os.system(self.wash_command)
                    print('=============================================')
                    print('Книги с таким параметром нет в библиотеке !')
                    print('=============================================')
                    pass

            print('==============================================================================')
            print('Для возращения в меню введите 1, для выхода любой символ и нажмите <<ENTER>>')
            print('==============================================================================')

            try:
                if input('=> ') == '1':
                    self.home_library()
                else:
                    raise Exception()
            except:
                os.system(self.wash_command)
                pass

        return func

    def add_book(self):

        if not any((book['id'] for book in self.books['list_books'])):
            last_id = 1
        else:
            last_id = max((book['id'] for book in self.books['list_books'])) + 1
        print(f'last_id => {last_id}')

        book = {
                    'id':last_id,
                    'title':None,
                    'author':None,
                    'year':None,
                    'status':'в наличие'
                }

        os.system(self.wash_command)

        try:
            try:
                print('=========================')
                print('Введите название книги')
                print('=========================')
                book['title'] = input('=> ')
                #s.system(self.wash_command)
                print('=======================')
                print('Введите автора книги')
                print('=======================')
                book['author'] = input('=> ')
                #os.system(self.wash_command)
                print('========================================')
                print('Введите год издания (например => 2000)')
                print('========================================')
            except KeyboardInterrupt:
                exit()

            try:
                year = int(input('=> '))
                if 0 < year <= 2024:
                    book['year'] = year
                else:
                    raise Exception
            except KeyboardInterrupt:
                exit()
            except:
                print('==========================================================================')
                print('Год издания указан некорректно, не будет добавлен к информации о  книге!')
                print('==========================================================================')


            os.system(self.wash_command)

            self.books['list_books'].append(book)
            with open(self.file_name, 'w') as file_library:
                file_library.write(json.dumps(self.books))

            print('======================================')
            print('Книга успешно добавлена в библиотеку')
            print('======================================')
            self.template_book_for_view(book)
        except:
            os.system(self.wash_command)
            print('=========================================')
            print('Книга не будет добавлена в библиотеку !')
            print('=========================================')

        print('==============================================================================')
        print('Для возращения в меню введите 1, для выхода любой символ и нажмите <<ENTER>>')
        print('==============================================================================')

        try:
            if input('=> ') == '1':
                self.home_library()
            else:
                raise Exception()
        except:
            os.system(self.wash_command)
            pass

    @hablon
    def del_book(self):

        print('========================================')
        print('Введите id книги, которую нужно удалить')
        print('========================================')

        try:
            id = int(input('=> '))
        except KeyboardInterrupt:
            os.system(self.wash_command)
            exit()

        os.system(self.wash_command)

        find_id =  tuple(book for book in self.books['list_books'] if book['id'] == id)[0]

        self.books['list_books'].remove(find_id)

        with open(self.file_name, 'w') as file_library:
            file_library.write(json.dumps(self.books))

        print('=====================================')
        print('Книга успешно удалена из библиотеки')
        print('=====================================')

    @hablon
    def find_book(self):

        print('===================================================')
        print('Введите автора, название или год для поиска книги')
        print('===================================================')

        try:
            key = input('=> ')
        except KeyboardInterrupt:
            os.system(self.wash_command)
            exit()

        os.system(self.wash_command)

        find_books = tuple(book for book in self.books['list_books'] if book['title'] == key or book['author'] == key or str(book['year']) == key)

        if len(find_books) == 0:
            raise Exception

        for book in find_books:
            self.template_book_for_view(book)
            print('---------------------------------------------------------------------')

    @hablon
    def change_status_book(self):

        print('======================================================')
        print('Введите id книги, которой необходимо изменить статус')
        print('======================================================')

        try:
            id = int(input('=> '))
        except KeyboardInterrupt:
            os.system(self.wash_command)
            exit()

        os.system(self.wash_command)

        book = tuple(book for book in self.books['list_books'] if book['id'] == id)[0]

        self.template_book_for_view(book)

        print('===================================')
        print('Для изменения статуса выберите:\n')
        print('1 => в наличие')
        print('2 => выдана')
        print('===================================')

        try:
            status = input('=> ')

            if not status in ('1', '2'):
                print('tut')
                raise ValueError
            elif status == '1':
                book['status'] = 'в наличие'
            elif status == '2':
                book['status'] = 'выдана'

            try:
                os.system(self.wash_command)

                with open(self.file_name, 'w') as file_library:
                    file_library.write(json.dumps(self.books))

                print('========================')
                print('Статус успешно изменен')
                print('========================')

                self.template_book_for_view(book)
            except:

                os.system(self.wash_command)

                print('=================================')
                print('Статус изменить не получилось !')
                print('=================================')
        except KeyboardInterrupt:
            os.system(self.wash_command)
            exit()
        except ValueError:
            os.system(self.wash_command)
            print('================================')
            print('Введен недопустимый параметр !')
            print('================================')
    @hablon
    def show_book(self):

        for book in self.books['list_books']:
            self.template_book_for_view(book)
            print('---------------------------------------------------------------------')

    def template_book_for_view(self, book:dict):

        max_len = max((len(str(book[key])) for key in book))

        template = '+' + '-' * (7 + max_len) + '+'

        print(template)
        print(f'|id    :{book["id"]}' + ' ' * (max_len - len(str(book["id"]))) + '|')
        print(f'|title :{book["title"]}' + ' ' * (max_len - len(str(book["title"]))) + '|')
        print(f'|author:{book["author"]}' + ' ' * (max_len - len(str(book["author"]))) + '|')
        print(f'|year  :{book["year"]}' + ' ' * (max_len - len(str(book["year"]))) + '|')
        print(f'|status:{book["status"]}' + ' ' * (max_len - len(str(book["status"]))) + '|')
        print(template)

library()