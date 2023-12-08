from typing import Any as _Any, Union as _Union
import abc as _abc

Value = _Union['Atom', tuple['Value', ...], 'Quantifier']

class Atom:
    def __init__(self, name: str):
        self._name = name

    def __eq__(self, other: _Any) -> bool:
        return self is other
    
    def __repr__(self) -> str:
        return self._name
    
    def rename(self, new_name: str):
        self._name = new_name

class Fact:
    _value: Value | None

    def get_value(self) -> Value:
        assert self._value != None
        return self._value
    
    def __eq__(self, other: _Any):
        return isinstance(other, Fact) and other.get_value() == self.get_value()

    def __repr__(self) -> str:
        return f"Fact {self._value if self._value != None else 'VOID'}"

    def destroy(self):
        self._value = None

_frames: list[list[Fact]] = [[]]
def fabricate_fact(proposition: Value) -> Fact:
    fact = Fact.__new__(Fact)
    setattr(fact, '_value', proposition)
    _frames[-1].append(fact)
    return fact


class Quantifier(_abc.ABC):
    
    def __init__(self, binding: Atom, body: Value):
        self._binding = binding
        self._body = body

    def __eq__(self, other: _Any) -> bool:
        return (isinstance(other, type(self)) and 
            other._binding == self._binding and 
            other._body == self._body)
    
    def get_binding(self) -> Atom:
        return self._binding
    
    def get_body(self) -> Value:
        return self._body

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._binding}, {self._body})"
    
class Forall(Quantifier):
    pass

class Exists(Quantifier):
    pass

IF = Atom("IF")
AND = Atom("AND")
OR = Atom("OR")
NOT = Atom("NOT")
IFF = Atom("IFF")
EQ = Atom("EQ")
TRUE = Atom("TRUE")