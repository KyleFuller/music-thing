from rep import *
from axioms import *
from rules import *

def conj_intro(fact_p: Fact, fact_q: Fact) -> Fact:
    p = fact_p.get_value()
    q = fact_q.get_value()
    fact_forall_q = cond_elim(universal_elim(conj_intro_axiom, p), fact_p)
    fact_and_p_q = cond_elim(universal_elim(fact_forall_q, q), fact_q)
    return fact_and_p_q

def conj_elim(fact_and_p_q: Fact) -> tuple[Fact, Fact]:
    _, p, q = fact_and_p_q.get_value()

    fact_if_and_p_q_p = universal_elim(universal_elim(left_conj_elim_axiom, p), q)
    fact_if_and_p_q_q = universal_elim(universal_elim(right_conj_elim_axiom, p), q)

    return (cond_elim(fact_if_and_p_q_p, fact_and_p_q), 
            cond_elim(fact_if_and_p_q_q, fact_and_p_q))

def disj_intro(fact_p: Fact, q: Value) -> Fact:
    p = fact_p.get_value()
    fact_or_p_q = cond_elim(universal_elim(universal_elim(disj_intro_axiom, p), q), fact_p)
    return fact_or_p_q

def disj_elim(fact_or_p_q: Fact, fact_if_p_r: Fact, fact_if_q_r: Fact) -> Fact:
    _, p, q = fact_or_p_q.get_value()
    _, _, r = fact_if_p_r.get_value()
    u_elim = universal_elim
    disj_elim_axiom_instantiated = u_elim(u_elim(u_elim(disj_elim_axiom, p), q), r)
    antecedent = conj_intro(fact_or_p_q, conj_intro(fact_if_p_r, fact_if_q_r))
    fact_r = cond_elim(disj_elim_axiom_instantiated, antecedent)
    return fact_r

def reductio(fact_if_p_and_q_not_q: Fact) -> Fact:
    if_p_and_q_not_q = fact_if_p_and_q_not_q.get_value()
    _if, p, (_and, q, (_not, q)) = if_p_and_q_not_q
    fact_not_p = cond_elim(universal_elim(universal_elim(reductio_axiom, p), q), fact_if_p_and_q_not_q)
    return fact_not_p

def double_neg_elim(fact_not_not_p: Fact) -> Fact:
    _not, (_not, p) = fact_not_not_p.get_value()
    fact_p = cond_elim(universal_elim(double_neg_elim_axiom, p), fact_not_not_p)
    return fact_p

def bicond_intro(fact_if_p_q: Fact, fact_if_q_p: Fact) -> Fact:
    _, p, q = fact_if_p_q.get_value()
    u_elim = universal_elim
    axiom_instantiated: Fact = u_elim(u_elim(bicond_intro_axiom, p), q)
    antecedent: Fact = conj_intro(fact_if_p_q, fact_if_q_p)
    fact_iff_p_q = cond_elim(axiom_instantiated, antecedent)
    return fact_iff_p_q

def bicond_elim(fact_iff_p_q: Fact) -> tuple[Fact, Fact]:
    _, p, q = fact_iff_p_q.get_value()
    u_elim = universal_elim
    axiom_instantiated = u_elim(u_elim(bicond_elim_axiom, p), q)
    conj_of_ifs = cond_elim(axiom_instantiated, fact_iff_p_q)
    if_p_q, if_q_p = conj_elim(conj_of_ifs)
    return if_p_q, if_q_p

def eq_intro(a: Value) -> Fact:
    fact_eq_a_a = universal_elim(equality_intro_axiom, a)
    return fact_eq_a_a

def eq_elim_left(f_x: tuple[Value, Value], g: Value, fact_eq_f_g: Fact) -> Fact:
    f, x = f_x
    fact_if_eq_f_g = universal_elim(universal_elim(eq_elim_axiom_left, f), g)
    fact_eq_f_x_g_x = universal_elim(cond_elim(fact_if_eq_f_g, fact_eq_f_g), x)
    return fact_eq_f_x_g_x

def eq_elim_right(f_x: tuple[Value, Value], y: Value, fact_eq_x_y: Fact) -> Fact:
    f, x = f_x
    fact_if_eq_x_y = universal_elim(universal_elim(eq_elim_axiom_right, x), y)
    fact_eq_f_x_f_y = universal_elim(cond_elim(fact_if_eq_x_y, fact_eq_x_y), f)
    return fact_eq_f_x_f_y