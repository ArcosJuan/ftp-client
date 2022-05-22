import sys
import os


class Display:
    EXIT_METHODS=[sys.exit]

    @classmethod
    def add_exit_methods(cls, methods:list): cls.EXIT_METHODS.extend(methods)


    @classmethod
    def ask_question(cls, question: str):
        """ Receives a question, asks it to the user and returns his answer.
            Also catches the user's exit attempts 
            and redirects them to the save method.
        """

        print(question)
        answ = input()
        print('')

        if answ == 'quit' or answ == 'exit': [method() for method in cls.EXIT_METHODS]
        else: return answ


    @staticmethod
    def clear(): os.system('cls' if os.name=='nt' else 'clear')

