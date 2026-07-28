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

from typing import Generator
from fastnumbers import fast_float,fast_int

class Lexer:

    Token_Type = {
    'INT': 'INT',
    'FLOAT': 'FLOAT',
    'STR': 'STRING',
    'OP': 'OP',
    'IDENTIFIER': 'IDENTIFIER',
    'DELIMITER': 'DELIMITER',
    'KEYWORD': 'KEYWORD',
    'TYPE_HINT': 'TYPE'
}
    keywords = {
    'var': 'VAR',
    'const': 'CONST',
    'def': 'DEF',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    'True': 'TRUE',
    'False': 'FALSE',
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR'
}   
    type_hints = {'int':'INT',
    'float':'FLOAT',
    'bool':'BOOL',
    'str':'STRING'
}
    DELIMITER ={';':'SEMICOLON',
    ':' : 'COLON',
    '(':'LEFT_PARENTHESIS',
    ')': 'RIGHT_PARENTHESIS',
    '"':'DOUBLE_QUOTATION',
    "'": 'SINGLE_QUOTATION',
    '.': 'DOT'
}
    SINGLE_OPS = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULTIPLY',
    '/': 'DIVIDE',
    '=': 'ASSIGN',
    '!': 'NOT'
}
    MULTI_OPS  = {'//': 'FLOOR_DIVIDE',
    '!=': 'NOT_EQUAL'
}
    END = {'eof':'EOF','error':'ERROR'}

    __slots__ = ('len','index','source','current_char','ALL_OPS','op_trie','jump_table')
    def __init__(self,source:str):
        self.source:str = source
        self.index:int = -1 # think of this like the program counter
        self.len = len(source)
        self.current_char = source[0] if len(source) > 0 else None  # think of this like cpu registors

        #merge and trie
        self.ALL_OPS = {**self.SINGLE_OPS, **self.MULTI_OPS}
        self.op_trie = self.trie(self.ALL_OPS)

        self.jump_table = self.build_256_jump_table()
        self.next_token()

    def next_token(self,step = 1):
        self.index += step
        self.current_char = self.source[self.index] if self.index < self.len else None

    """===build==="""
    @staticmethod
    def trie(dicts:dict) -> dict:
        root ={} # this i will be the root
        for key in dicts:
            node = root
            for char in key:
                if char not in node: # see if this is already in side the root
                    node[char] = {}
                node = node[char]
            node['_end'] = dicts[key]
        return root

    def build_256_jump_table(self):
        # Use self.XXX to get bound methods
        jump_table = [self.handle_invaild] * 256

        for char in ' \t\r\n':
            jump_table[ord(char)] = self.handle_white_space

        for op in self.SINGLE_OPS.keys(): # for op
            jump_table[ord(op)] = self.handle_op

        for byte in range(48, 58):
            jump_table[byte] = self.handle_numbers

        for byte in list(range(65, 91)) + [95] + list(range(97, 123)):
            jump_table[byte] = self.handle_ident_keyword_typehints

        for delim in self.DELIMITER.keys():
            jump_table[ord(delim)] = self.handle_delimiter

        jump_table[ord('"')] = self.handle_strings
        jump_table[ord("'")] = self.handle_strings

        return jump_table

    """===handlers==="""

    def handle_invaild(self) -> Generator[tuple[str,str|None]]:
        yield (self.END['error'],self.current_char) # yield only stops the program for a moment not end it like return
        self.next_token() # sooooo we can do this and its the parsers job to raise a error we only send a error token

    def handle_white_space(self):
        while self.current_char is not None and self.current_char in ' \t\r\n':
            self.next_token()
            continue

    def handle_op(self) -> Generator[tuple[str,str]]:
        start = self.index # save the start value
        node = self.op_trie
        last_valid_type = None
        last_valid_index = start # keep track for both of the vailds as we need to back track

        while self.index < self.len:
            char = self.current_char # save a instance of the current char like how CPU puts stuff from registors into L1 cache
            if char not in node:
                break
            node = node[char]

            # Check if we have reached a valid token (end marker)
            if '_end' in node:
                last_valid_type = node['_end']
                last_valid_index = self.index + 1  # Mark where this token ends
        
            self.index += 1

        # If we found a valid operator
        
        if last_valid_type is not None:
            # eat the char we already passed
            # track back if needed aka rewrite the index as tires only allow for vaild paths

            # rewind index 
            self.index = last_valid_index
            # reassing the curret char
            self.current_char = self.source[self.index] if self.index < self.len else None

            yield (self.Token_Type['OP'],last_valid_type)
        else:
            # no valid operator matched (shouldn't happen since jump table routed it here)
            raise SyntaxError(f'Invalid operator sequence "{self.source[start]}"')

    def handle_numbers(self) -> Generator[tuple[str,int|float]]:
        start = self.index
        is_float = False
        #INT's
        while self.current_char is not None and self.current_char.isdigit():
            self.next_token()

        # FLOAT's

        if self.current_char == '.': # if we find a dot after a int we mark it as a float
            is_float = True
            self.next_token() # eat the next char
            if self.current_char is None or not self.current_char.isdigit(): # if there are no whole numbers after a dot we raise a error
                raise SyntaxError("Invalid float: expected digits after decimal") # ERROR msg
            
            else:
                while self.current_char is not None and self.current_char.isdigit(): # we start the while loop until the conditon is false
                    self.next_token()
        # for big numbers
        if self.current_char in ('e','E'): # nice to have ig?
            is_float = True
            self.next_token() # eat the char
            if self.current_char in ('+','-'):
                self.next_token()
            elif self.current_char is None or not self.current_char.isdigit():
                raise SyntaxError("Invalid exponent: expected digits")
            else:
                while self.current_char is not None and self.current_char.isdigit():
                    self.next_token()

        num_group = self.source[start:self.index] # group them at one place by using slicing the start is well the start var and the current index is the end with everything in between thats why we have :

        if is_float:
            yield (self.Token_Type['FLOAT'],fast_float(num_group))
        else:
            yield (self.Token_Type['INT'],fast_int(num_group))

    def handle_strings(self):
        char = self.current_char # save the ' or "
        self.next_token() # eat
        result = []

        while self.current_char is not None and char in ('"',"'"):
            self.next_token()

            if self.current_char == '\\':
                self.next_token()  # consume the backslash
                if self.current_char is None:
                    raise SyntaxError("Unterminated escape sequence")

                elif self.current_char == 'n':
                    result.append('\n')
                elif self.current_char == 't':
                    result.append('\t')
                elif self.current_char == 'r':
                    result.append('\r')
                elif self.current_char == '\\':
                    result.append('\\')
                elif self.current_char == char:
                    # Escaped quote (e.g., \' or \")
                    result.append(char)
                else:
                    # If it's an unknown escape, we just keep the backslash and the char
                    result.append('\\')
                    result.append(self.current_char)
            elif  self.current_char == char:
                self.next_token()  # consume the closing quote
                yield (self.Token_Type['STR'], ''.join(result))

            else:
                result.append(self.current_char)
                self.next_token()
                


    def handle_ident_keyword_typehints(self) -> Generator[tuple[str,str]]:
        start = self.index
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            self.next_token()
        word = self.source[start:self.index] # slice into group

        if word in self.keywords:
            yield (self.Token_Type['KEYWORD'], self.keywords[word])
        elif word in self.type_hints:
            yield (self.Token_Type['TYPE_HINT'], self.type_hints[word])
        else:
            yield (self.Token_Type['IDENTIFIER'], word)

    def handle_delimiter(self):
        delim = self.DELIMITER[self.current_char]
        self.next_token()  # <-- MOVE BEFORE YIELD
        yield (self.Token_Type['DELIMITER'], delim)
    """===Main loop==="""
    
    def tokenize(self):
        while self.current_char is not None and self.index < self.len:
            self.source[self.index] if self.index < self.len else None
            if self.current_char is None:
                break
            try:
                byte = ord(self.current_char)
                if byte > 255:
                    raise SyntaxError(f'INVALID CHARACTER USED: {self.current_char}')
                handler = self.jump_table[byte]
                token = handler()
                if token:
                    yield from token
                continue
            except:
                raise SyntaxError(f'INVALID CHARACTER USED: {self.current_char}')
        yield (self.END['eof'], None)
