
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
