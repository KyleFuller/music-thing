
from typing import Callable as _Cbl, Any as _Any
from rep import *
from rep import _frames
from rules import *
from axioms import *
from tactics import *

def succeeds(computation: _Cbl[[], _Any]) -> bool:
    try:
        computation()
        return True
    except:
        return False

def fails(computation: _Cbl[[], _Any]) -> bool:
    return not succeeds(computation)

def test():
    p = Atom("p")
    fact_p = fabricate_fact(p)
    q = Atom("q")
    fact_q = fabricate_fact(q)
    r = Atom("r")

    assert fails(lambda: cond_intro((q, p, q), lambda fact_p: fact_q))
    assert fails(lambda: cond_intro((IF, p, q), lambda fact_p: fact_p))
    assert fails(lambda: cond_intro((IF, p, p), lambda fact_p: fact_q))
    fact_if_p_q = cond_intro((IF, p, q), lambda fact_p: fact_q)
    assert fact_if_p_q.get_value() == (IF, p, q)
    
    frame_length_inner = None
    def failing_derivation(fact_p: Fact):
        nonlocal frame_length_inner
        frame_length_inner = len(_frames)
        return fact_p
    assert len(_frames) == 1
    assert fails(lambda: cond_intro((IF, p, q), failing_derivation))
    assert frame_length_inner == 2
    assert len(_frames) == 1

    stash = []
    assert len(_frames) == 1
    def sneeky_derivation(fact_p: Fact):
        fact_if_q_p = cond_intro((IF, q, p), lambda fact_q: fact_p)
        assert succeeds(lambda: fact_if_p_q.get_value())
        assert succeeds(lambda: fact_if_p_q == fact_if_p_q)
        stash.append(fact_if_q_p) # this fact is not supposed to be valid outside this "hypothetical".
        assert len(_frames) == 2
        return fact_q
    assert len(_frames) == 1
    cond_intro((IF, p, q), sneeky_derivation)
    void_fact_if_q_p = stash[0]
    assert fails(lambda: void_fact_if_q_p.get_value())
    assert fails(lambda: void_fact_if_q_p == void_fact_if_q_p)

    assert fails(lambda: cond_elim(fabricate_fact((q, p, q)), fact_p) == fact_q)
    assert fails(lambda: cond_elim(fabricate_fact((IF, q, q)), fact_p) == fact_q)
    assert fails(lambda: cond_elim(fabricate_fact((IF, p, q)), fact_q))
    assert cond_elim(fact_if_p_q, fact_p) == fact_q

    x = Atom("x")
    y = Atom("y")
    z = Atom("z")
    assert Forall(x, (p, x)) != Forall(x, (q, x))
    assert Forall(x, (p, x)) != Forall(y, (p, x))
    assert Forall(x, (p, x)) != Forall(y, (p, y))
    assert Forall(x, (p, x)) == Forall(x, (p, x))
    assert Exists(x, (p, x)) != Exists(x, (q, x))
    assert Exists(x, (p, x)) != Exists(y, (p, x))
    assert Exists(x, (p, x)) != Exists(y, (p, y))
    assert Exists(x, (p, x)) == Exists(x, (p, x))
    assert Forall(x, (p, x)) != Exists(x, (p, x))
    assert Exists(x, (p, x)) != Forall(x, (p, x))

    f = Atom("f")
    g = Atom("g")
    h = Atom("h")
    assert substitute_atom_for_value((f, x, Exists(x, (x, p))), x, q) == (f, q, Exists(x, (x, p)))    
    fact_forall = fabricate_fact(Forall(x, (f, x, Exists(x, (x, p)))))
    assert universal_elim(fact_forall, (g, f)).get_value() == (f, (g, f), Exists(x, (x, p)))

    w = Atom("w")
    e = Atom("e")
    r = Atom("r")
    
    assert fails(lambda: existential_elim(fabricate_fact(Forall(e, (r, e)))).get_value())
    assert existential_elim(fabricate_fact(Exists(w, (r, e)))).get_value() == (r, e)
    assert existential_elim(fabricate_fact(Exists(e, (r, e)))).get_value() != (r, e)
    
    a = Atom("a")
    b = Atom("b")
    c = Atom("c")

    assert fails(lambda: (f, a).get_value() == (EQ, (f, a), ((f, a),)))
    assert flattening((f, a, b)).get_value() == (EQ, (f, a, b), ((f, a), b))
    assert flattening((f, a, b, c)).get_value() == (EQ, (f, a, b, c), ((f, a), b, c))

    assert reductio(fabricate_fact((IF, p, (AND, q, (NOT, q))))).get_value() == (NOT, p)
    
    assert double_neg_elim(fabricate_fact((NOT, (NOT, p)))).get_value() == p

    assert disj_intro(fabricate_fact(p), q).get_value() == (OR, p, q)

    assert (disj_elim(fabricate_fact((OR, p, q)),
        fabricate_fact((IF, p, r)), fabricate_fact((IF, q, r))).get_value() == r)

    assert bicond_intro(fabricate_fact((IF, p, q)), fabricate_fact((IF, q, p))).get_value() == (IFF, p, q)
    fact_if_p_q, fact_if_q_p = bicond_elim(fabricate_fact((IFF, p, q)))
    assert fact_if_p_q.get_value() == (IF, p, q) and fact_if_q_p.get_value() == (IF, q, p)

    assert eq_intro(a).get_value() == (EQ, a, a)

    assert eq_elim((f, a), (g, a), fabricate_fact((EQ, f, g))).get_value() == (EQ, (f, a), (g, a))
    assert eq_elim((f, a), (f, b), fabricate_fact((EQ, a, b))).get_value() == (EQ, (f, a), (f, b))
    assert (eq_elim(
            Forall(x, (AND, (p, x), Exists(y, (q, (f, p))))), 
            Forall(x, (AND, (f, x), Exists(y, (q, (p, p))))),
            fabricate_fact((EQ, p, f))).get_value()
        ) == (EQ, 
              Forall(x, (AND, (p, x), Exists(y, (q, (f, p))))), 
              Forall(x, (AND, (f, x), Exists(y, (q, (p, p))))))
    
    assert fails(lambda: eq_elim(a, a, (IFF, a, a)))
    assert fails(lambda: eq_elim(Forall(p, p), Forall(q, q), (EQ, p, q)))
    assert fails(lambda: eq_elim((f, a), (f, b), (EQ, a, c)))
    assert fails(lambda: eq_elim((f, a), (g, a), (EQ, f, a)))


test()

