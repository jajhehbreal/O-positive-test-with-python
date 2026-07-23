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


class Pratt_Parser:

    Binding_Power = {'PLUS': 10,'MINUS': 10,
                    'MULTIPLY': 20,'DIVIDE': 20,'FLOOR_DIVIDE': 20}

    def __init__(self,token_stream) -> None:
        self.token = list(token_stream)
        self.index = 0
        self.peek_token = None
        self.next_token()

    def next_token(self):
        if self.index < len(self.token):
            # FETCH: read the token at the current PC address
            self.peek_token = self.token[self.index]
            # INCREMENT PC (point to the next instruction)
            self.index += 1
        else:
            # End of program (EOF)
            self.peek_token = None

    def parse(self):
        """Start parsing expressions with binding power 0."""
        return self.expression(0)

    def expression(self, min_bp):

        token = self.peek_token
        if token is None:
            raise SyntaxError("Unexpected end of input while parsing expression")

        match  token:

            case ('INT', value) | ('FLOAT', value):
                self.next_token()
                left = value

            case ('OP','('):

                self.next_token()
                left = self.expression(0)
                if self.peek_token and self.peek_token == ('OP',')'):
                    self.next_token()

                else:
                    raise SyntaxError("Expected ')'")
            case _:
                raise SyntaxError(f"Unexpected token: {token}")

        while (self.peek_token and self.peek_token[0] == 'OP' and  
            self.peek_token[1] in self.Binding_Power and
            self.Binding_Power[self.peek_token[1]] >= min_bp):

            op = self.peek_token[1] # store
            self.next_token() # eat

            right = self.expression(self.Binding_Power[op] + 1)

            left = (op, left, right)
        
        return left
