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

class Bin_Op_Node:

    __slots__ = ('LHS','RHS','OP')

    def __init__(self,LHS,OP,RHS) -> None:
        self.LHS = LHS
        self.OP = OP
        self.RHS = RHS

    def to_string_lines(self,depth =0):
        indentation:str = ' ' * depth

        op = self.OP[1] if isinstance(self.OP, tuple) else self.OP

        yield f"{indentation}BinOpNode('{op}'):"
        yield from self.LHS.to_string_lines(depth + 1)
        yield from self.RHS.to_string_lines(depth + 1)

    def to_string(self) -> str:
        return "\n".join(self.to_string_lines())

    def __repr__(self) -> str:
        return self.to_string()

class UnaryOpNode:
    __slots__ = ('OP', 'RHS')
    def __init__(self, OP, RHS):
        self.OP = OP
        self.RHS = RHS

    def to_string_lines(self, depth=0):
        indentation = ' ' * depth
        op = self.OP[1] if isinstance(self.OP, tuple) else self.OP
        yield f"{indentation}UnaryOpNode('{op}'):"
        yield from self.RHS.to_string_lines(depth + 1)

    def __repr__(self) -> str:
        return "\n".join(self.to_string_lines())

class NumberNode:
    __slots__ = ('value',)
    def __init__(self, value):
        self.value = value

    def to_string_lines(self, depth=0):
        yield f"{' ' * depth}NumberNode({self.value})"

    def __repr__(self) -> str:
        return "\n".join(self.to_string_lines())

class EmptyTupleNode:

    def __repr__(self) -> str:
        return 'EMPTY_TUPLE'
