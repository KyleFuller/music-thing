* Ultimately, the following things need to be present in some way or another:
    * Conjunction introduction.
    * Conjunction elimination.
    * Reductio ad absurdum.
    * Disjunction introduction.
    * Disjunction elimination.
    * Conditional introduction.
    * Conditional elimination.
    * Biconditional introduction.
    * Biconditional elimination.
    * Equality introduction.
    * Equality elimination.
    * Universal introduction.
    * Universal elimination.
    * Existential introduction.
    * Existential elimination.
    * Comprehension: must not allow any funny business.

* Let lowercase letters represent variables.  Unfortuntately, what I wrote below isn't too clear about what needs to be an atom and what can be any value, but if something is used as the first argument to a quantifier, it needs to be an atom.

* Any need for alpha renaming shall be ignored just for the time being.

* Let's say we only use the following built-in symbols:
    * (And p q): a truth function that returns true iff both of its arguments are true.
    * (Not p): a truth function that returns true iff its argument is not true.
    * Forall(x, p): universal quantifier.

* Some Shorthands:
    * (If p q) stands for (Not (And p (Not q)))
    * (Iff p q) stands for (And (If p q) (If q p))
    * Exists(x, p) stands for (Not (Forall x (Not p)))

* Built-in Rules:
    * Propositional Calculus
        * Conjunction Introduction: Fact(p), Fact(q) -> Fact(And p q)
        * Conjunction Elimination: Fact(And p q) -> Fact(p), Fact(q)
        * Reductio Ad Absurdum: p, (Fact(p) -> (And c (Not c))) -> Fact(not p)
        * Double Negation Elimination: Fact(Not (Not p)) -> Fact(p)
    * Predicate Calculus
        * Equality Introduction: a -> Fact(= a a)
        * Equality Elimination: Fact(p[v := a]), p_new@(p[v :∈ {a, b}]), Fact(= x y) -> Fact(p_new)
    * Logic with General Quantification?:
        * Universal Introduction: x, p[v := x], (y -> p[v := y]) -> Fact(Forall(z, p[v := z]))
        * Universal Elimination: Fact(Forall(x, p[v := x])), p[v := a] -> Fact(p[v := a])
        * Comprehension: Exists(X, Forall(x, (Iff (X x) p[v := x]))) -> 
                Fact(Exists(Y, Forall(y, (Iff (Y y) p[v := y])))) 
            where X not in p and v not used as a predicate in p
        