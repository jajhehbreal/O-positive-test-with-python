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
    
