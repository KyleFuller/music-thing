from typing import Callable as _Fn, cast as _cast
import operator as _op
from functools import partial as _partial


_RVFn = _Fn[[float], float]

def scale_input(x_factor: float, f: _RVFn, /) -> _RVFn:
    """ returns a function x * x_factor |-> f(x). """
    return lambda x: f(x / x_factor)

def scale_output(y_factor: float, f: _RVFn, /) -> _RVFn:
    """ returns a function x |-> f(x) * y_factor. """
    return lambda x: f(x) * y_factor

def scale_2d(x_factor: float, y_factor: float, f: _RVFn, /) ->_RVFn:
    """ returns a function x * x_factor |-> f(x) * y_factor. """
    return scale_output(y_factor, scale_input(x_factor, f))

def translate_input(x_offset: float, f: _RVFn, /) -> _RVFn:
    """ returns a function x + x_offset |-> f(x). """
    return lambda x: f(x - x_offset)

def translate_output(y_offset: float, f: _RVFn, /) -> _RVFn:
    """ returns a function x |-> f(x) + y_offset. """
    return lambda x: f(x) + y_offset

def translate_2d(x_offset: float, y_offset: float, f: _RVFn, /) -> _RVFn:
    """ returns a function x + x_offset |-> f(x) + y_offset. """
    return translate_output(y_offset, translate_input(x_offset, f))

def combine(binop: _Fn[[float, float], float], f: _RVFn, g: _RVFn, /) -> _RVFn:
    """ returns a function x |-> binop(f(x), g(x)). """
    return lambda x: binop(f(x), g(x))

add, sub, mul, div, mod, pow = (
    _cast(_Fn[[_RVFn, _RVFn], _RVFn], _partial(combine, scalar_op)) 
        for scalar_op in (
            _op.add, _op.sub, _op.mul, _op.truediv, _op.mod, _op.pow))
