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

from .Token import TokenType

class Lexer:
    __slots__ = ('index', 'source', 'current_char', 'operators','op_trie')
    def __init__(self, source_code: str) -> None:
        self.source:str = source_code
        self.index:int = -1
        self.current_char = None
        
        # Pre-allocated O(1) syntax registries
        self.operators = {'+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', '/': 'DIVIDE','//': 'FLOOR_DIVIDE','=': 'ASSIGN'}

        self.op_trie = {}
        for op in self.operators:
            node = self.op_trie
            for char in op:
                if char not in node:
                    node[char] = {}
                node = node[char]
            node['_end'] = op
        
        self.move_next()

    def move_next(self) -> None:
        self.index += 1
        self.current_char = self.source[self.index] if self.index < len(self.source) else None

    def operator_helper(self):
        OP_Buffer = []
        node = self.op_trie # local var
        while self.current_char is not None and self.current_char in node:
            node = node[self.current_char]
            potential_op = "".join(OP_Buffer) + self.current_char
            # big performence killer here and its any key word
            if '_end' in node:
                OP_Buffer.append(self.current_char)
                self.move_next()
            else:
                break

        lexeme = "".join(OP_Buffer)

        while lexeme and '_end' not in node:
            # Backtrack
            self.index -= 1
            self.current_char = self.source[self.index] if self.index >= 0 else None
            lexeme = lexeme[:-1]
            node = self.op_trie
            for char in lexeme:
                node = node[char]

        if lexeme in self.operators:
            return (TokenType.OP, self.operators[lexeme])
        else:
            raise SyntaxError(f"Invalid operator sequence: '{lexeme}'")
            
    def number_helper(self)-> tuple:
        num_buffer = []
        while self.current_char is not None and self.current_char.isdigit():
            num_buffer.append(self.current_char)
            self.move_next()
        return (TokenType.INT, int("".join(num_buffer)))

    def Identifiers_helper(self) -> tuple :
        id_buffer = []
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_buffer.append(self.current_char)
            self.move_next()

        lexeme = "".join(id_buffer)
        return (TokenType.IDENTIFIER, lexeme)

    def tokenize(self): 
        
        while self.current_char is not None:
            # 1. Skip Whitespace
            if self.current_char in ' \t\n\r':
                self.move_next()
                yield
                continue

            # 2. Match Static Operators
            if self.current_char in self.operators:
                yield self.operator_helper()
                continue
            # 3. Match Numbers (Optimized List Buffer)
            elif self.current_char.isdigit():
                yield self.number_helper()
                continue

            # 4. Match Identifiers / Keywords (Allows alphanumeric variable tracking)
            elif self.current_char.isalpha() or self.current_char == '_':
                yield self.Identifiers_helper()
                continue

            # Fallback: Syntax Error Handling
            raise SyntaxError(f"Illegal character detected in stream: '{self.current_char}'")

    def __call__(self):
        return self.tokenize()
