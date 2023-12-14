from typing import Union as _Union

Formula = _Union['Atom', 'Application', 'Quantification']
Application = tuple['Formula', ...]
Quantification = tuple['Quantifier', 'Atom', 'Formula']

class Atom('_NamedObject'): pass
class Quantifier('_NamedObject'): pass
    
class _NamedObject:

    def __init__(self, name: str, obj, /):
        self._name = name
        self._obj = obj

    def __eq__(self, other) -> bool:
        return isinstance(other, _NamedObject) and self._obj == other._obj or self._obj == other
    
    def __hash__(self) -> int:
        return hash(self._obj)
        
    def __str__(self) -> str:
        return self._name
    
