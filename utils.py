from typing import TypeVar as _TypeVar, Protocol as _Protocol, Iterable as _Iterable, Collection as _Collection

def linspace(start: float, stop: float, num: int, /) -> _Iterable[float]:
    """
    Returns an iterable of `num` evenly spaced floating point values beginning at `start` and with a spacing of 
    `(stop - start) / num`.  Note that this means that the result will typically not quite reach `stop`.
    """
    step_duration = (stop - start) / num
    return (start + i * step_duration for i in range(num))

def linspace_inclusive(start: float, stop: float, num: int, /) -> _Iterable[float]:
    for el in linspace(start, stop, num - 1):
        yield el
    yield stop

_T = _TypeVar('_T')
class _Addable(_Protocol):

    def __add__(self: _T, other: _T, /) -> _T:
        ...

_T_Addable = _TypeVar('_T_Addable', bound=_Addable)
def cumul_sum(vals: _Iterable[_T_Addable]) -> _Iterable[_T_Addable]:
    """
    Returns an iterable with the cumulative sum of a given iterable of values.
    """
    vals_iterator = iter(vals)
    s = next(vals_iterator)
    yield s
    for val in vals_iterator:
        s += val
        yield s

def iterable_as_collection(iterable: _Iterable[_T]) -> _Collection[_T]:
    """
    Takes an iterable that may or may not be a collection, iterates through the iterable (and therefore exhausts it if
    it is exhaustable), and returns a collection of all elements, in order, from the iterable.  In the case where the 
    given iterable is already a collection, the collection may be the same object as the collection given.
    """
    if isinstance(iterable, _Collection):
        collection: _Collection[_T] = iterable
    else:
        collection: _Collection[_T] = list(iterable)
    return collection

def is_approx(x: float, y: float, tol: float, /):
    return abs(y - x) <= tol