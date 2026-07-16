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
        
        # Pre allocated syntax registries
        self.operators = {'+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', '/': 'DIVIDE','//': 'FLOOR_DIVIDE','=': 'ASSIGN','!': 'NOT','!=': 'NOT_EQUAL'}

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
        last_valid_len = 0

        while self.current_char is not None and self.current_char in node:
            node = node[self.current_char]

            if '_end' in node:
                OP_Buffer.append(self.current_char)
                self.move_next()
                if '_end' in node:
                    last_valid_len = len(OP_Buffer)

        if last_valid_len == 0:
            raise SyntaxError(f"Invalid operator sequence starting with '{self.source[self.index - len(OP_Buffer)]}'")

        while len(OP_Buffer) > last_valid_len:
            self.index -= 1
            self.current_char = self.source[self.index]
            OP_Buffer.pop()

        lexeme = "".join(OP_Buffer)

        yield (TokenType.OP, self.operators[lexeme])

    def number_helper(self):
        num_buffer = []

        while self.current_char is not None and self.current_char.isdigit():
            num_buffer.append(self.current_char)
            self.move_next()

        yield (TokenType.INT, int("".join(num_buffer)))

    def Identifiers_helper(self):
        id_buffer = []
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            id_buffer.append(self.current_char)
            self.move_next()

        lexeme = "".join(id_buffer)
        yield (TokenType.IDENTIFIER, lexeme)

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

            # Fallback: Syntax Error Handling
            raise SyntaxError(f"Illegal character detected in stream: '{self.current_char}'")

    def __call__(self):
        return self.tokenize()
