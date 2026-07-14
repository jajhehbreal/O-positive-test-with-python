from sys import exit
from front_end.LEXER import Lexer
from numpy import fromiter,dtype

TOKEN_DTYPE = dtype([('type', 'U32'), ('value', 'O')])

def run_langu(user_input):
    lexer_instance = Lexer(user_input)
    # Stream directly into NumPy.
    tokens_array = fromiter(lexer_instance(), dtype=TOKEN_DTYPE)

    if len(tokens_array) == 1 and tokens_array[0]['type'] == 'IDENTIFIER' and tokens_array[0]['value'] == 'exit':
        print('exiting...\nDone')
        exit()

    #print
    print(tokens_array)
    
