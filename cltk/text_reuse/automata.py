"""
Constructs NF and DF Automata

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

import itertools

def powerset(S):
    """
    Constructs the powerset of a list

    >>> powerset([1, 2, 3])
    {(1, 2), (1, 3), (1,), (2,), (3,), (1, 2, 3), (), (2, 3)}
    """

    return set([k for i in range(len(S) + 1) for k in list(itertools.combinations(S, i))])

class DFA:

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

