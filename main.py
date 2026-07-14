# very importent thing are in ALL CAPS
# THIS WILL TAKE MATHS LIKE 1 + 1 AND TURN THEM INTO ONE PLUS ONE AKA TURN IT INTO ENGLISH TEXT SO JUST OUT PUT TOKENS
from run_lang import run_langu

class Main:
    __slots__ = ('running')
    def __init__(self) -> None:
        self.running = True

    def run(self):
        while self.running:
            user_inputs = input('>>').strip() # the input will be GIVEN to the lexer after LEXING INTO TOKENS we print
            run_langu(user_inputs)

def run():
    main = Main()
    main.run()

if __name__ == '__main__':
    run()