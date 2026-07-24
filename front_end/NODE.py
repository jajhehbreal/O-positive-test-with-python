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

class Node:
    __slots__ = ('value','OP','LHS','RHS')
    def __init__(self,value=None,OP =None,LHS = None,RHS = None) -> None:
        self.value = value
        self.OP = OP
        self.LHS = LHS
        self.RHS = RHS

class Bin_Op_Node(Node):

    def to_string_lines(self,depth =0):
        indentation:str = '    ' * depth

        op = self.OP[1] if isinstance(self.OP, tuple) else self.OP

        yield f"{indentation}BinOpNode('{op}'):"
        yield from self.LHS.to_string_lines(depth + 1)
        yield from self.RHS.to_string_lines(depth + 1)

    def to_string(self) -> str:
        return "\n".join(self.to_string_lines())

    def __repr__(self) -> str:
        return self.to_string()

class UnaryOpNode(Node):

    def to_string_lines(self, depth=0):
        indentation = '    ' * depth
        op = self.OP[1] if isinstance(self.OP, tuple) else self.OP
        yield f"{indentation}UnaryOpNode('{op}'):"
        yield from self.RHS.to_string_lines(depth + 1)

    def __repr__(self) -> str:
        return "\n".join(self.to_string_lines())

class NumberNode(Node):

    def to_string_lines(self, depth=0):
        yield f"{'    ' * depth}NumberNode({self.value})"

    def __repr__(self) -> str:
        return "\n".join(self.to_string_lines())

class KeywrodNode(Node):
    def to_string_lines(self,depth=0):
        yield f"{'    ' * depth}KeywordNode({self.value})"

    def __repr__(self) -> str:
        return '\n'.join(self.to_string_lines())

class DelimiterNode(Node):

    def to_string_lines(self,depth=0):
        yield f"{'    ' * depth}DelimiterNode({self.value})"

class EmptyTupleNode:

    def to_string_lines(self,depth =0):
        yield f"{'    ' * depth}EmptyTupleNode(EMPTY_TUPLE)"
    def __repr__(self) -> str:
        return '\n'.join(self.to_string_lines())

class EmptyTupleNode:

    def __repr__(self) -> str:
        return 'EMPTY_TUPLE'
