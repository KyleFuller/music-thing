from typing import Callable as _Cbl

from rep import *
from rep import _frames

def universal_elim(fact_forall: Fact, value: Value) -> Fact:

    # BUILTIN RULE
    assert isinstance(fact_forall, Fact)
    forall = fact_forall.get_value()
    assert isinstance(forall, Forall)
    binding, body = forall.get_binding(), forall.get_body()
    return fabricate_fact(substitute_atom_for_value(body, binding, value))

def existential_elim(fact_exists: Fact) -> Fact:

    # BUILTIN RULE
    assert isinstance(fact_exists, Fact)
    exists = fact_exists.get_value()
    assert isinstance(exists, Exists)
    binding = exists.get_binding()
    return fabricate_fact(substitute_atom_for_value(exists.get_body(), binding, Atom("<existential_representative>")))

def flattening(uncurried: tuple[Value, ...]) -> Fact:

    # BUILTIN RULE
    
    assert len(uncurried) >= 3
    curried = (
        (uncurried[0], uncurried[1]), 
        *uncurried[2:])
    return fabricate_fact((EQ, uncurried, curried))


def cond_intro(
        if_p_q: tuple[Value, Value, Value], 
        prove_q_from_p: _Cbl[[Fact], Fact]
    ) -> Fact:
    
    # BUILTIN RULE

    _if, p, q = if_p_q
    assert _if == IF
    _frames.append([])
    exception = None
    try:
        assert prove_q_from_p(fabricate_fact(p)).get_value() == q
    except Exception as e:
        exception = e
    finally:
        for fact in _frames[-1]:
            fact.destroy()
        _frames.pop()
        if exception is not None:
            raise exception

    return fabricate_fact((IF, p, q))

def cond_elim(
        fact_if_p_q: Fact,
        fact_p: Fact    
    ) -> Fact:

    # BUILTIN RULE

    if_p_q = fact_if_p_q.get_value()
    assert isinstance(if_p_q, tuple)
    if0, p0, q0 = if_p_q
    p1 = fact_p.get_value()

    assert if0 == IF; assert p1 == p0
    return fabricate_fact(q0)


def eq_elim(a: Value, b: Value, fact_eq: Fact) -> Fact:
    # BUILTIN RULE
    assert isinstance(fact_eq, Fact)
    eq, u, v = fact_eq.get_value()
    assert eq == EQ
    assert are_equal_up_to_items(a, b, (u, v))
    return fabricate_fact((EQ, a, b))

# HELPERS


def substitute_atom_for_value(body: Value, atom: Atom, value: Value) -> Value:
    if isinstance(body, Atom):
        return value if body == atom else body
    elif isinstance(body, Quantifier):
        binding = body.get_binding()
        return (body if binding == atom else 
            type(body)(binding, substitute_atom_for_value(body.get_body(), atom, value)))
    else:
        return tuple(substitute_atom_for_value(subexp, atom, value) for subexp in body)

def are_equal_up_to_items(x: Value, y: Value, items: tuple[Value, ...]) -> bool:
    
    if x in items and y in items:
        return True
    elif not (isinstance(x, Atom) and isinstance(y, Atom) or
            isinstance(x, tuple) and isinstance(y, tuple) or
            isinstance(x, Forall) and isinstance(y, Forall) or
            isinstance(x, Exists) and isinstance(y, Exists)):
        return False
    elif isinstance(x, Atom) and isinstance(y, Atom):
        return x == y
    elif isinstance(x, Quantifier) and isinstance(y, Quantifier):
        return (x.get_binding() == y.get_binding() and 
                are_equal_up_to_items(x.get_body(), y.get_body(), items))
    else:
        return (len(x) == len(y) and 
                all(are_equal_up_to_items(x_el, y_el, items) 
                    for x_el, y_el in zip(x, y)))

def is_definition_well_formed_inner(params: tuple[Atom], definition: tuple[Value]) -> bool:
    if isinstance(definition, Quantifier):
        return False
    
    if isinstance(definition, Atom):
        return True

    func, args = definition[0], definition[1:]
    return func not in params and all(is_definition_well_formed(params, arg) for arg in args)

def is_definition_well_formed(params: tuple[Atom], definition: tuple[Value]) -> bool:

    if isinstance(definition, Atom):
        return definition in params

    return is_definition_well_formed_inner(params, definition)
