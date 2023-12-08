from rep import *

_x = Atom("_x")
_y = Atom("_y")
_p = Atom("_p")
_q = Atom("_q")
_r = Atom("_r")
_f = Atom("_f")
_g = Atom("_g")

# AND

conj_intro_axiom = fabricate_fact(
    Forall(_p, (IF, _p, 
        Forall(_q, (IF, _q, (AND, _p, _q))))))

left_conj_elim_axiom = fabricate_fact(
    Forall(_p, (Forall(_q, (IF, (AND, _p, _q), _p)))))

right_conj_elim_axiom = fabricate_fact(
    Forall(_p, (Forall(_q, (IF, (AND, _p, _q), _q)))))

# OR

disj_intro_axiom = fabricate_fact(
    Forall(_p, Forall(_q, 
        (IF, _p, (OR, _p, _q)))))

disj_elim_axiom = fabricate_fact(
    Forall(_p, Forall(_q, Forall(_r, 
        (IF, (AND, 
                (OR, _p, _q), 
                (AND, (IF, _p, _r), (IF, _q, _r))),
            _r)))))

# NOT

reductio_axiom = fabricate_fact(
    Forall(_p, Forall(_q, 
        (IF, (IF, _p, (AND, _q, (NOT, _q))),
            (NOT, _p)))))

double_neg_elim_axiom = fabricate_fact(
    Forall(_p, (IF, (NOT, (NOT, _p)), _p)))

# IFF

bicond_intro_axiom = fabricate_fact(
    Forall(_p, Forall(_q,
        (IF, (AND, 
                (IF, _p, _q), 
                (IF, _q, _p)),
            (IFF, _p, _q)))))

bicond_elim_axiom = fabricate_fact(
    Forall(_p, Forall(_q,
        (IF, (IFF, _p, _q),
            (AND, 
                (IF, _p, _q), 
                (IF, _q, _p))))))

# EQ

equality_intro_axiom = fabricate_fact(
    Forall(_x, (EQ, _x, _x)))

eq_elim_axiom_left = fabricate_fact(
    Forall(_f, Forall(_g, 
        (IF, (EQ, _f, _g), 
            Forall(_x, 
                (EQ, (_f, _x), (_g, _x)))))))

eq_elim_axiom_right = fabricate_fact(
    Forall(_x, Forall(_y, 
        (IF, (EQ, _x, _y), 
            Forall(_f, 
                (EQ, (_f, _x), (_f, _y)))))))

# TRUE

truth_axiom = fabricate_fact(
    Forall(_p, 
        (IF, _p, 
            (EQ, _p, TRUE))))


untruth_axiom = fabricate_fact(
    Forall(_p,
        (IF, (NOT, _p), 
            (NOT, (EQ, _p, TRUE)))))
