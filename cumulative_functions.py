
from typing import TypeVar as _TypeVar, Callable as _Fn

_T = _TypeVar('_T')

def get_cumulative_nat_func_from_indexed_accumulator(init: _T, forward: _Fn[[_T, int], _T]):
    vals: list[_T] = [init]

    batch_size = 64
    num_computed = 1

    def func(i: int) -> _T:
        nonlocal num_computed
        while i >= len(vals):
            for _ in range(batch_size):
                vals.append(forward(vals[len(vals) - 1], len(vals) - 1))
            num_computed += batch_size
        return vals[i]
    
    return func

def get_cumulative_int_func_from_indexed_accumulators(init: _T, forward: _Fn[[_T, int], _T], backward: _Fn[[_T, int], _T]):
    right = get_cumulative_nat_func_from_indexed_accumulator(init, forward)
    left = get_cumulative_nat_func_from_indexed_accumulator(init, lambda so_far, i: backward(so_far, -i))

    def func(i: int) -> _T:
        if i >= 0:
            return right(i)
        else:
            return left(-i)
        
    return func

