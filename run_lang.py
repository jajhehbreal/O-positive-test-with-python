# This file is part of O-positive-test-with-python.
# Copyright (C) 2026 jajhehbreal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from sys import exit
from front_end.Lexer import Lexer
from front_end.Parser import Top_level_parser
from numpy import fromiter,dtype

TOKEN_DTYPE = dtype([('type', 'U32'), ('value', 'O'),('line', 'i4'), ('col', 'i4')])

def run_langu(user_input):
    # 1. Lexer produces a generator
    lexer_instance = Lexer(user_input)
    # Stream directly into NumPy.
    tokens_array = fromiter(lexer_instance.tokenize(), dtype=TOKEN_DTYPE)

    if len(tokens_array) == 1 and tokens_array[0]['type'] == 'IDENTIFIER' and tokens_array[0]['value'] == 'exit':
        print('exiting...\nDone')
        exit()

    #print
    print(tokens_array)
    
    # 2. (Optional) convert to NumPy array for density, or just pass the generator
    #    For now, pass the generator directly — it will be converted to list inside the parser.
    #parser = Top_level_parser(lexer.tokenize())
    
    # 3. Parse and get the AST
    #ast = parser.parse_program()
    #return ast
