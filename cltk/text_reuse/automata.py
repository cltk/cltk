"""
Constructs Levenshtein automata

At first, both the NFA and DFA classes inherited from a common Automaton class.
I found that treating the two as separate entities, results in more comprehensive
documentation in the price of succinctness.

This is the third iteration of the algorithm, the first one used transition
matrices for representing automata but this proved to be a massive waste
of space for anything non-trivial. In addition, instead of the usual
intuitiveness that accompanies such approaches, I had to deal with
countless of indexing errors and even the slightest of optimizations
became overbearing (e.g. minimizing an automaton and deleting unreachable
states, required either costly operations or error-prone hacks).

After a brief experimenting with more traditional graph approaches,
I eventually tried trie-like nested dictionaries. This came with
a whole set of new problems (can't use unhashable types as dictionary,
traversing a nested dictionary is not as direct as a matrix etc), but
the overall code is more understandable for someone already familiar
with the subject matter.
"""

__author__ = ['Eleftheria Chatziargyriou <ele.hatzy@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


class DFA:

    """
        Define Deterministic finite automaton

        Explanation:

            A DFA is a finite state machine (note that it is not
            Turing equivalent) represented by a 5-tuple (Q, Σ, δ, s, F)

            Q: Finite set of states (the nodes of the DFA)

            Σ: Finite set of input symbols (the alphabet of the automaton)

            δ: Transition function δ: QxS -> Q

            s: Start state, s ∈ Q

            f: Finite set of final states  F ⊆ Q

        Initialization:
            A deterministic automaton is defined in a way closely related
            to its mathematical notation.

            >>> A = DFA({'q1', 'q2'}, ['0', '1'], 'q1', set())

        Adding final states:
            States can be added to F even after initializing

            >>> A.add_final_state('q1')

        Adding transitions:
            You can either define the transition table by assigning
            a nested dic (see further down for example) to the delta
            parameter at initialization, or manually define each
            transition

            >>> A.add_transition('q1', '0', 'q2')

            >>> A.add_transition('q2', '1', 'q2')

            >>> A.add_transition('q2', '0', 'q1')

            The equivalent transition trie will be this:

            >>> A.transition
            {'q1': {0: 'q2'}, 'q2': {1: 'q2', 0: 'q1'}}

        Calling the transition function:
            To call δ(qi, u), simply call transition_function:

            >>> A.transition_function('q1', '0')
            'q2'

            The method returns null if the transition is not defined

            >>> A.transition_function('q1', '1')
            None

        Accepted input strings:
            Determining whether an input belongs to the language
            recognized by a DFA A only is O(|w|) time, in contrast
            to the exponential solution of the equivalnet problem
            using a nondeterministic automaton.

            Since the automaton is simple, we can deduce its language
            without the need for any calculations: (01*0)*

            Now on to testing

            >>> A.accepted('01000')
            True

            >>> A.accepted('010011001110')
            True

            >>> A.accepted('100100')
            False
    """

    def __init__(self, Q, S, s, F, delta = False):
        """
        :param Q: set: Set of states Q: q0, q1, ... qn
        :param S: str set: Set of symbols recognized by the automaton
        :param s: int: The starting state q_s1
        :param F: int set: Set of accepted states {q'0, ... q'|F|)
        :param delta: Nq*|S| int transition matrix (defaults to empty transition matrix)
        """

        self.Q = Q
        self.S = S

        if s not in self.Q:
            print("The specified value is invalid, s must be a member of Q")
            raise ValueError
        else:
            self.s = s

        if sum([f not in self.Q for f in F]) != 0:
            print("The specified value is invalid, F must be a subset of Q (F∩Q≠∅)")
            raise ValueError
        else:
            self.F = F

        if delta:
            self.transition = delta
        else:
            self.transition = {}

    def add_final_state(self, f):

        """
        :param f: int , the state qi to be added to F, epsilon is
        conventionally defined as the last node (q_|S|)
        """
        if f not in  self.Q:
            print("The specified value is invalid, f must be a member of Q")
            raise ValueError

        self.F.add(f)

    def add_transition(self, qi, u, qj):
        """
        :param qi:int: current state, qi ∈ Q
        :param u:str: transition character u ∈ S
        :param qj:int: target state, qj ∈ Q, δ(qi, u) = qj

        If δ(qi, u) is already defined, the method replaces the
        already existent transition to qj.
        """
        if u not in self.S:
            print("The specified value is invalid, f must be a member of S")
            raise ValueError

        try:
            self.transition[qi][u] = qj
        except KeyError:
            self.transition[qi] = dict()
            self.transition[qi][u] = qj


    def transition_function(self, qi, u):
        """
        :param qi: int: current state, qi ∈ Q
        :param u:str: transition character u ∈ S
        :returns Q': int :  δ(qi, u) = q
        """
        try:
            return self.transition[qi][u]
        except KeyError:
            return None

    def accepted(self, w):

        active_state = self.s

        for k in w:
            active_state = self.transition_function(active_state, k)

            if active_state == None:
                return False

        return bool(active_state in self.F)

class NFA():
    """
            Define Nondeterministic finite automaton

                Explanation:

                    A NFA is a finite state machine (note that it is not
                    Turing equivalent) represented by a 5-tuple (Q, Σ, δ, s, F)

                    Q: Finite set of states (the nodes of the DFA)

                    Σ: Finite set of input symbols (the alphabet of the automaton)

                    δ: Transition function δ: QxS -> P(Q)

                    s: Start state, s ∈ Q

                    f: Finite set of final states  F ⊆ Q

                    As you can probably see, NFAs are nearly identical to DFAs. The difference
                    lies in the transition function, which maps to the powerset of Q instead of
                    Q itself. This is where its more important properties derive from, namely
                    nondeterminism (essentially being able to simultaneously "process" different
                    states)

                    A generalization of NFA allows ε-moves, allowing for empty strings to be
                    considered as valid input of the transition function (δ(q, ε) can be defined).
                    While this remains equivalent to both its specialized form and the viscerally
                    simpler DFA, it poses some additional problems when converting it to a strictly
                    deterministic form.

                Initialization:
                    NFA initialization is nearly identical to that of a DFA, with two key
                    differences:
                      - the transition function maps to a set rather than a value q⊆Q
                      - an additional parameter isEpsilon (defaults to False) is defined
                        indicating whether the instanced NFA allows for ε-moves

                    >>> B = NFA({'q1', 'q2'}, {'0', '1'}, 'q1', set(), isEpsilon = True)

                Adding final states:
                    States can be added to F after initializing

                    >>> B.add_final_state('q1')

                Adding transitions:
                    You can either define the transition table by assigning
                    a nested dic to delta at initialization, or manually define
                    each transition

                    >>> B.add_transition('q1', '0', 'q2')

                    >>> B.add_transition('q1', '0', 'q1')

                    >>> B.add_transition('q2', '1', 'q1')

                    >>> B.add_transition('q2', B.epsilon, 'q1')

                    Its transition trie will be:

                    >>> B.transition

                    {'q1': {'0': {'q2', 'q1'}}, 'q2': {'1': {'q1'}, <object object at 0x0000026E598BC0C0>: {'q1'}}}

                    The object() is a convenient way to define ε in a computationally easy way.

                Converting to DFA:
                    As you probably realized, because of the recursive nature of the
                    automaton, figuring out whether a given input string is accepted
                    can result into an exponential worst-case, which is downright
                    unacceptable for larger applications. If you recall, we already
                    mentioned that any given NFA has an equivalent DFA, which
                    fortunately offers a quick way for determining its language. This comes
                    at the cost of O(2^n) space, which is still managable for smaller
                    automata.

                    >>> C = B.to_DFA

                    >>> C.accepted("000")
                    True

    """

    def __init__(self, Q, S, s, F, delta = False, isEpsilon = False):
        """
        :param Q: set: Set of states Q: q0, q1, ... qn
        :param S: str set: Set of symbols recognized by the automaton
        :param s: int: The starting state q_s1
        :param F: int set: Set of accepted states {q'0, ... q'|F|)
        :param delta: Nq*|S| int transition matrix (defaults to empty transition matrix)
        """

        self.Q = Q
        self.S = S
        self.epsilon = object()
        self.isEpsilon = isEpsilon

        if self.isEpsilon: self.S.add(self.epsilon)

        if s not in self.Q:
            print("The specified value is invalid, s must be a member of Q")
            raise ValueError
        else:
            self.s = s

        if sum([f not in self.Q for f in F]) != 0:
            print("The specified value is invalid, F must be a subset of Q (F∩Q≠∅)")
            raise ValueError
        else:
            self.F = F

        if delta:
            self.transition = delta
        else:
            self.transition = {}

    def add_final_state(self, f):

        """
        :param f: int , the state qi to be added to F, epsilon is
        conventionally defined as the last node (q_|S|)
        """
        if f not in  self.Q:
            print("The specified value is invalid, f must be a member of Q")
            raise ValueError

        self.F.add(f)

    def add_transition(self, qi, u, qj):
        """
        :param qi:int: current state, qi ∈ Q
        :param u:str: transition character u ∈ S
        :param qj:int: target state, qj ∈ Q, δ(qi, u) = qj

        If δ(qi, u) is already defined, the method replaces the
        already existent transition to qj.
        """
        if u not in self.S:
            print("The specified value is invalid, f must be a member of S")
            raise ValueError

        try:
            self.transition[qi][u].add(qj)

        except KeyError:
            try:
                self.transition[qi][u] = {qj}
            except KeyError:
                self.transition[qi] = dict()
                self.transition[qi][u] = {qj}

    def transition_function(self, qi, u):
        """
        :param qi: int: current state, qi ∈ Q
        :param u:str: transition character u ∈ S
        :returns Q': int :  δ(qi, u) = q
        """
        try:
            return self.transition[qi][u]
        except KeyError:
            return None

    def to_DFA(self):

        starting_state = tuple([self.s])

        #Calculate E(q), q ∈ Q

        if self.isEpsilon:

            E = {}

            for q in self.Q:
                visited_q0 = [q]
                active_q0 = [q]

                while active_q0:
                    q1 = active_q0.pop(0)

                    try:
                        for t in self.transition_function(q1, self.epsilon):
                            if t not in visited_q0:
                                visited_q0.append(t)
                                active_q0.append(t)
                    except:
                        pass

                E[q] = sorted(visited_q0)
            starting_state = E[self.s]

        transition = {}
        final_states = set()

        active_states = [starting_state]

        visited_states = [starting_state]

        while active_states:
            q = tuple(active_states.pop(0))
            str_q = " ".join(sorted(q))

            if str_q not in transition:
                transition[str_q] = {}

                if self.F.intersection(set(q)) != set():
                    final_states.add(str_q)

            S = set().union(*[set(self.transition[t].keys()) for t in q if t in self.transition])
            S.discard(self.epsilon)

            for s in S:
                states = set().union(*[self.transition_function(t, s) for t in q if self.transition_function(t, s)])
                states = sorted(list(set().union(*[E[state] for state in states])))

                transition[str_q][s] = " ".join(states)

                if states not in visited_states:
                    visited_states.append(states)
                    active_states.append(states)

        return DFA(transition.keys(), self.S, " ".join(starting_state), final_states, delta = transition)


def levenshtein_automata(word, depth):

    """
    Constructs the levenshtein DFA of a given word. The automata accepts all words
    with levenshtein_distance(word) <= depth

    >>> D = levenshtein_automata("canis", 2)

    >>> D = D.to_DFA()

    >>> D.accepted("ca*s")
    True

    >>> D.accepted("ca***s")
    False
    """

    D = NFA(["q" + str(i * (len(word) + 1) + j) for i in range(depth + 1) for j in range(len(word) + 1)], set(word + "*"),
            "q0", set(["q" + str((i + 1) * (len(word) + 1) - 1) for i in range(depth + 1)]), isEpsilon=True)

    for i in range(depth):
        for j in range(len(word)):

            # Correct character
            D.add_transition(("q" + str((len(word) + 1) * i + j)), word[j],"q" + str((len(word) + 1) * i + j + 1))

            # Insertion
            D.add_transition(("q" + str((len(word) + 1) * i + j)), D.epsilon, "q" + str((len(word) + 1) * (i + 1) + j + 1))

            # Substitution
            D.add_transition("q" + str((len(word) + 1) * i + j), "*", "q" + str((len(word) + 1) * (i + 1) + j + 1))

            # Deletion
            D.add_transition("q" + str((len(word) + 1) * i + j), "*", "q" + str((len(word) + 1) * (i + 1) + j))

    for j in range(len(word)):
        D.add_transition("q" + str((len(word) + 1) * depth + j), word[j], "q" + str((len(word) + 1) * depth + j + 1))
    return D

