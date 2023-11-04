from typing import Iterable as _Iterable, Iterator as _Iterator, Literal as _Literal
from queue import PriorityQueue as _PriorityQueue

_ZeroOrOne = _Literal[0] | _Literal[1]

def get_bounds_iterator(intervals: _Iterable[tuple[float, float]]
        ) -> _Iterator[tuple[float, _ZeroOrOne]]:
    
    """ Takes an iterable of intervals each of format (start, stop), and returns
    an iterable of interval boundaries (position, kind), where position is the
    position of the boundary and kind is the kind of the boundary, 0 for an 
    interval start and 1 for an interval stop.  The iterable returned is in 
    ascending order of position, and its evaluation is fully demand-driven. """

    intervals_itr = iter(intervals)
    del intervals

    pq: _PriorityQueue[tuple[float, _ZeroOrOne]] = _PriorityQueue()
    def put_next_interval():
        interval = next(intervals_itr, None)
        if interval is not None:
            start, stop = interval
            assert stop >= start
            pq.put((start, 0))
            pq.put((stop, 1))

    put_next_interval()
    while pq.qsize() != 0:
        position, kind = pq.get()
        yield (position, kind)
        if kind == 0:
            put_next_interval()

def test():
    """ Diagram of following test case.
              11111111112222222222
    012345678901234567890123456789
     |--|
      |-----|
       |---|
          |------|
                |--|
                    |-------|
                      |----|
              11111111112222222222
    012345678901234567890123456789
    """
    assert (
            list(get_bounds_iterator(
                [(1, 4), (2, 8), (3, 7), (6, 13), (11, 14), (16, 24), (18, 23)]))
        == 
            [(1, 0), (2, 0), (3, 0), (4, 1), (6, 0), (7, 1), (8, 1), (11, 0), 
                (13, 1), (14, 1), (16, 0), (18, 0), (23, 1), (24, 1)]
    )
    print("Test passed. ")