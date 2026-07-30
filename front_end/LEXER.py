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
    'STR': 'STR',
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

    __slots__ = ('length','index','source','current_char','jump_table','multi_by_first','ALL_OPS')
    def __init__(self,source:str):
        self.source:str = source
        self.index:int = -1 # think of this like the program counter
        self.length = len(source)
        self.current_char = None  # think of this like cpu registors

        #for OP
        self.multi_by_first: dict[str, list[str]] = {}
        for op in self.MULTI_OPS:
            self.multi_by_first.setdefault(op[0],[]).append(op)
        for first in self.multi_by_first:
            self.multi_by_first[first].sort(key=len,reverse=True)

        self.ALL_OPS =  {**self.SINGLE_OPS, **self.MULTI_OPS}

        self.jump_table = self.build_256_jump_table()
        self.next_token()

    def next_token(self,step = 1):
        self.index += step
        self.current_char = self.source[self.index] if self.index < self.length else None

    """===build==="""


    def build_256_jump_table(self):
        # Use self.name to get bound methods
        jump_table = [self.handle_invalid] * 256

        for char in ' \t\r\n':
            jump_table[ord(char)] = self.handle_white_space

        for op in self.SINGLE_OPS.keys(): # for op only
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

    def handle_invalid(self) -> Generator[tuple[str,str|None]]:
        char = self.current_char # like L1 cache
        self.next_token()
        yield (self.END['error'],char)

    def handle_white_space(self):
        while self.current_char is not None and self.current_char in ' \t\r\n':
            self.next_token()
            continue

    def handle_op(self) -> Generator[tuple[str,str]]:
        char = self.current_char # save the instance of the current char like L1 cache
        candidates = self.multi_by_first.get(char)

        if candidates is not None:
            for cand in candidates:
                end = self.index + len(cand)
                if end <= self.lenght and self.source[self.index:end] == cand:
                    self.next_token(step=len(cand))
                    yield (self.Token_Type['OP'], self.ALL_OPS[cand])
                    return # keep return or the func will not end

        # 2. Fall back to single-character operator
        if char in self.SINGLE_OPS:
            self.next_token()  # consume the single char
            yield (self.Token_Type['OP'], self.SINGLE_OPS[char])
        else:
            # Shouldn't happen if jump table routed it here
            raise SyntaxError(f"Invalid operator sequence: '{char}'")



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
            if self.current_char is None or not self.current_char.isdigit():
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
        quote = self.current_char
        self.next_token()
        result = []

        while self.current_char is not None and self.current_char != quote:
            if self.current_char == '\\':
                self.next_token()
                if self.current_char is None:
                    raise SyntaxError("Unterminated escape sequence")
                escapes = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', quote: quote}
                result.append(escapes.get(self.current_char, self.current_char))
            else:
                result.append(self.current_char)
            self.next_token()  # uniform advance

        if self.current_char != quote:
            raise SyntaxError("Unterminated string literal")

        self.next_token()  # eat closing quote
        yield (self.Token_Type['STR'], ''.join(result))


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

    def handle_delimiter(self) -> Generator[tuple[str,str]]:
        delim = self.DELIMITER[self.current_char]
        self.next_token()  # <-- MOVE BEFORE YIELD
        yield (self.Token_Type['DELIMITER'], delim)
    """===Main loop==="""
    
    def tokenize(self) -> Generator:
        while self.current_char is not None and self.index < self.length:
            byte = ord(self.current_char)
            if byte > 255: # ASCLL is 256 so if the number is bigger then 255 use a error
                raise SyntaxError(f'INVALID CHARACTER USED: {self.current_char}')
            handler = self.jump_table[byte]
            token = handler()
            if token:
                yield from token
        yield (self.END['eof'], None)
