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
    * Comprehension: must not allow any funny business (but unfortunately it still does).

* Let lowercase letters represent variables.  Unfortuntately, what I wrote below isn't too clear about what needs to be an atom and what can be any value, but if something is used as the first argument to a quantifier, it needs to be an atom.

* Let's say we only use the following built-in symbols:
    * (And p q): true iff both p and q are true.
    * (Not p): true iff p is not true.
    * (= a b): equality.
    * Forall(x, p): universal quantifier.

* Built-in Rules:
    * Propositional Calculus
        * Conjunction Introduction: Fact(p), Fact(q) -> Fact(And p q)
        * Conjunction Elimination: Fact(And p q) -> Fact(p), Fact(q)
        * Reductio Ad Absurdum: p, (Fact(p) -> Fact(And c (Not c))) -> Fact(not p)
        * Double Negation Elimination: Fact(Not (Not p)) -> Fact(p)
    * Predicate Calculus
        * Self-Identicality: a -> Fact(= a a)
        * Substitution of Equals: Fact(p[v :∈ {a, b}]), p_new@(p[v :∈ {a, b}]), Fact(= a b) -> Fact(p_new)
        * Truth: Fact(p) -> Fact(= p True)
        * Untruth: Fact(Not p) -> Fact(Not (= p True))
    * Unordered Quantified Logic
        * Universal Introduction: (y -> Fact(p[v := y])) -> Fact(Forall(z, p[v := z]))
        * Universal Elimination: Fact(Forall(x, p[v := x])), p[v := a] -> Fact(p[v := a])
        * Comprehension: Forall(x, (= (f0 x) e[v := x])) -> Fact(Forall(y, (= (f1 y) e[v := y]))) where f0 not in e and v not used as a function in e
            * This does not work;  If there is an identity function, then 
            Russell's Paradox can still be implemented.

* How it is now:
    * Built-in Rules:
        * Conditional Elimination -- To be able to have conditionals.
        * Universal Elimination -- To be able to generalize.
        * Existential Elimination -- To be able to have existentials.

        * Conditional Introduction -- To be able to capture derivation.
        * Comprehension -- To be able to get new functions from existing ones.

        * Flattening -- To be able to use a compact, n-ary syntax for multi-argument functions while ensuring all functions can still be spoken of as unary functions.

    * Axioms:
        * Equality Introduction -- To have everything be self-equal.
        * Equality Elimination Left -- Allows equating function applications based on equal functions.
        * Equality Elimination Right -- Allows equating function applications based on equal arguments.
        * Truth -- That which holds is equal to true.
        * Untruth -- That which does not hold is unequal to true.



-------- A new system, as the above system is fatally flawed --------

* Core principle: one mustn't be able to use functions to determine whether or 
not a value is null.  

Built-in functions:
* And
    * And T T = T
    * And F _ = F
* Or
    * Or T _ = T
    * Or F T = T
    * Or F F = F
* Not
    * Not F = T
    * Not T = F
* If
    * If F _ = T
    * If T T = T
    * If T F = F
* Eq
    * Eq x x = T
    * Eq _@(-N) _@(-N) = F
Non-function forms:
* ForAll
    * ForAll x T = T
    * ForAll x _@(T|F) = F
* Exists x <statement>
    * Exists x F = F
    * Exists x _@(T|F) = T
* IS_VALUE
    * IS_VALUE N = F
    * IS_VALUE _ = T
* IS_BOOL
    * IS_BOOL T = T
    * IS_BOOL F = T
    * IS_BOOL _ = F

Axioms and Rules:
* Conditional Intro
    * (ϕ! |-> ψ!) |-> (If ϕ ψ)!
* Conditional Elim
    * (If ϕ ψ)!, ϕ! |-> ψ!
* Reductio
    * (ForAll ϕ (ForAll ψ 
        (IF (And (IS_BOOL ϕ) (IS_BOOL ψ))
            (If (If ϕ (And ψ (Not ψ))) (Not ϕ)))))!
* Double Negation Elim
    * (ForAll ϕ
        (IF (IS_BOOL ϕ)
            (If (NOT (NOT ϕ)) ϕ)))!
* Equality Intro
    * (ForAll a
        (IF (IS_VALUE a)
            (Eq a a)))
* Equality Elim
    * IS_VALUE(p0@(p[v := _@(a|b)])), p1@(p[v := _@(a|b)]), (Eq a b)! |-> (Eq p0 p1)!
* Null Substitution
    * p0@(p[v := _]), p1@(p[v := N]) |-> (If HasValue(p1), (Eq p0 p1))
* Truth
    * (ForAll ϕ
        (IF IS_VALUE(ϕ)
            (If ϕ (Eq ϕ T))))
* Falsehood
    * (ForAll ϕ
        (IF IS_VALUE(ϕ)
            (If (Not ϕ) (Eq ϕ F))))
* Value Intro
    * (ForAll a
        (IF (Exists b (And (IS_VALUE b) (Eq a b)))
            (IS_VALUE a)))
* Universal Elim
* Existential Elim
* Comprehension
* Nonexistence of Value-Checking Function.
