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

class Lexer:
    __slots__ = ('index', 'source', 'current_char','Token_Type', 'operators','op_trie','DELIMITER','DELIMITER_trie')
    def __init__(self, source_code: str) -> None:
        self.source:str = source_code
        self.index:int = -1
        self.current_char = None
        self.Token_Type = {
    'INT': 'INT',
    'FLOAT': 'FLOAT',
    'OP': 'OP',
    'IDENTIFIER': 'IDENTIFIER',
    'DELIMITER': 'DELIMITER',
}
        
        # Pre allocated syntax registries
        self.operators = {'+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', '/': 'DIVIDE','//': 'FLOOR_DIVIDE',
                        '=': 'ASSIGN','!': 'NOT','!=': 'NOT_EQUAL'}
        self.DELIMITER ={';':'SEMICOLON',':' : 'COLON'}
        #tries
        self.op_trie = self.trie(self.operators)
        self.DELIMITER_trie = self.trie(self.DELIMITER)
        
        self.move_next()

    def trie(self,dicts:dict) -> dict:
        tries = {}
        for _types in dicts:
            node = tries
            for char in _types:
                if char not in node:
                    node[char] = {}
                node = node[char]
            node['_end'] = _types

        return tries

    def move_next(self) -> None:
        self.index += 1
        self.current_char = self.source[self.index] if self.index < len(self.source) else None

    def operator_helper(self):
        OP_Buffer = []
        node = self.op_trie # local var
        last_valid_len = 0

        while self.current_char is not None and self.current_char in node:
            node = node[self.current_char]
            OP_Buffer.append(self.current_char)
            self.move_next()

            if '_end' in node:
                last_valid_len = len(OP_Buffer)

        if last_valid_len == 0:
            start_idx = max(0, self.index - len(OP_Buffer))
            raise SyntaxError(f"Invalid operator sequence starting with '{self.source[start_idx]}'")

        while len(OP_Buffer) > last_valid_len:
            self.index -= 1
            self.current_char = self.source[self.index]
            OP_Buffer.pop()

        lexeme = "".join(OP_Buffer)

        yield (self.Token_Type['OP'], self.operators[lexeme])

    def number_helper(self):
        num_buffer = []

        while self.current_char is not None and self.current_char.isdigit():
            num_buffer.append(self.current_char)
            self.move_next()

        yield (self.Token_Type['INT'], int("".join(num_buffer)))

    def Identifiers_helper(self):
        id_buffer = []
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_buffer.append(self.current_char)
            self.move_next()

        lexeme = "".join(id_buffer)
        yield (self.Token_Type['IDENTIFIER'], lexeme)

    def DELIMITER_helper(self):
        DELIMITER_buffer = []
        node = self.DELIMITER_trie
        last_valid_DELIMITER = 0

        while self.current_char is not None and self.current_char in node:
            node = node[self.current_char]
            DELIMITER_buffer.append(self.current_char) # store
            self.move_next() # eat

            if '_end' in node:
                last_valid_DELIMTER = len(DELIMITER_buffer)

        if last_valid_DELIMITER == 0:
            raise SyntaxError(f"Invalid DELIMITER sequence starting with '{self.source[self.index - len(DELIMITER_buffer)]}'")

        while len(DELIMITER_buffer) > last_valid_DELIMITER:
            self.index -= 1
            self.current_char = self.source[self.index]
            DELIMITER_buffer.pop()

        lexme = ''.join(DELIMITER_buffer)
        yield (self.Token_Type['DELIMITER'],lexme) # index 4 is DELIMITER

    def tokenize(self): 
        
        while self.current_char is not None:
            # 1. Skip Whitespace
            if self.current_char in ' \t\n\r':
                self.move_next()
                continue

            # 2. Match Static Operators
            if self.current_char in self.operators:
                yield from self.operator_helper()
                continue
            # 3. Match Numbers (Optimized List Buffer)
            elif self.current_char.isdigit():
                yield from self.number_helper()
                continue

            # 4. Match Identifiers / Keywords (Allows alphanumeric variable tracking)
            elif self.current_char.isalpha() or self.current_char == '_':
                yield from self.Identifiers_helper()
                continue
                
            elif self.current_char in self.DELIMITER:
                yield from self.DELIMITER_helper()
                continue

            # Fallback: Syntax Error Handling
            raise SyntaxError(f"Illegal character detected in stream: '{self.current_char}'")

    def __call__(self):
        return self.tokenize()
