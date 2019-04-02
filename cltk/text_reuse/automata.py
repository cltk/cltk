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

import logging
from cltk.exceptions import InputError

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())

class DeterministicFiniteAutomaton:

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

            >>> A = DeterministicFiniteAutomaton({'q1', 'q2'}, ['0', '1'], 'q1', set())

            Keep in mind that both the starting and final states have to belong
            to Q:

            >>> W = DeterministicFiniteAutomaton({'q1', 'q2'}, ['0', '1'], 'q0', set())
            Traceback (most recent call last):
                ...
            cltk.exceptions.InputError: The specified value is invalid, s must be a member of Q

            >>> W = DeterministicFiniteAutomaton({'q1', 'q2'}, ['0', '1'], 'q1', {'q3'})
            Traceback (most recent call last):
                ...
            cltk.exceptions.InputError: The specified value is invalid, F must be a subset of Q (F∩Q≠∅)

        Adding final states:
            States can be added to F even after initializing

            >>> A.add_final_state('q1')

            >>> A.add_final_state('q3')
            Traceback (most recent call last):
                ...
            cltk.exceptions.InputError: The specified value is invalid, f must be a member of Q

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
            {'q1': {'0': 'q2'}, 'q2': {'1': 'q2', '0': 'q1'}}

            You can not define a transition of unrecognized symbols

            >>> A.add_transition('q1', '2', 'q2')
            Traceback (most recent call last):
                ...
            cltk.exceptions.InputError: The specified value is invalid, f must be a member of S

        Calling the transition function:
            To call δ(qi, u), simply call transition_function:

            >>> A.transition_function('q1', '0')
            'q2'

            The method returns null if the transition is not defined

            >>> A.transition_function('q1', '1')

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

        Complete automaton:
            A complete automaton is well defined for any state and
            input symbol. By calling complete_automaton you are
            essentially creating a new terminating state.

            >>> A.complete_automaton()

            Any undefined transition ends up to the newly defined
            state:

            >>> A.transition_function('q1', '1') == A.term_state
            True

            Every transition from the terminating state, reffers
            back to itself such that δ(term, u) = term

            >>> A.transition_function(A.term_state, '0') == A.term_state
            True

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
            LOG.error("The specified value is invalid, s must be a member of Q")
            raise InputError("The specified value is invalid, s must be a member of Q")
        else:
            self.s = s

        if sum([f not in self.Q for f in F]) != 0:
            LOG.error("The specified value is invalid, F must be a subset of Q (F∩Q≠∅)")
            raise InputError("The specified value is invalid, F must be a subset of Q (F∩Q≠∅)")
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
        if f not in self.Q:
            LOG.error("The specified value is invalid, f must be a member of Q")
            raise InputError("The specified value is invalid, f must be a member of Q")

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
            LOG.error("The specified value is invalid, f must be a member of S")
            raise InputError("The specified value is invalid, f must be a member of S")

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

            if active_state is None:
                return False

        return bool(active_state in self.F)

    def complete_automaton(self):
        """
        Adds missing transition states such that δ(q, u) is defined
        for every state q and any u ∈ S
        """
        self.term_state = object()

        self.Q.add(self.term_state)

        for tv in self.Q:
            for u in self.S:
                try:
                    self.transition[tv][u]
                except:
                    self.add_transition(tv, u, self.term_state)

        for u in self.S:
            self.add_transition(self.term_state, u, self.term_state)


class NondeterministicFiniteAutomaton:
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

                    >>> B = NondeterministicFiniteAutomaton({'q1', 'q2'}, {'0', '1'}, 'q1', set(), isEpsilon = True)

                    Similarly to the initialization of Deterministic Automata, it is
                    compulsory for both the starting and final states to belong to Q.

                    >>> W = NondeterministicFiniteAutomaton({'q1', 'q2'}, {'0', '1'}, 'q3', set())
                    Traceback (most recent call last):
                        ...
                    cltk.exceptions.InputError: The specified value is invalid, s must be a member of Q


                    >>> W = NondeterministicFiniteAutomaton({'q1', 'q2'}, {'0', '1'}, 'q1', {'q3'})
                    Traceback (most recent call last):
                        ...
                    cltk.exceptions.InputError: The specified value is invalid, F must be a subset of Q (F∩Q≠∅)

                Adding final states:
                    States can be added to F after initializing

                    >>> B.add_final_state('q1')

                    >>> B.add_final_state('q3')
                    Traceback (most recent call last):
                        ...
                    cltk.exceptions.InputError: The specified value is invalid, f must be a member of Q

                Adding transitions:
                    You can either define the transition table by assigning
                    a nested dic to delta at initialization, or manually define
                    each transition

                    >>> B.add_transition('q1', '0', 'q2')

                    >>> B.add_transition('q1', '0', 'q1')

                    >>> B.add_transition('q2', '1', 'q1')

                    >>> B.add_transition('q2', B.epsilon, 'q1')

                    Its transition trie will be:

                    >>> B.transition == {'q1': {'0': {'q2', 'q1'}}, 'q2': {'1': {'q1'}, B.epsilon : {'q1'}}}
                    True

                    The object() is a convenient way to define ε in a computationally easy way.

                Converting to DFA:
                    As you probably realized, because of the recursive nature of the
                    automaton, figuring out whether a given input string is accepted
                    can result into an exponential worst-case, which is downright
                    unacceptable for larger applications. If you recall, we already
                    mentioned that any given NFA has an equivalent DFA, which
                    fortunately offers a quick way for determining its language. This comes
                    at the cost of O(2^n) space, which is still manageable for smaller
                    automata.

                    >>> C = B.convert_to_deterministic()

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
            LOG.error("The specified value is invalid, s must be a member of Q")
            raise InputError("The specified value is invalid, s must be a member of Q")
        else:
            self.s = s

        if sum([f not in self.Q for f in F]) != 0:
            LOG.error("The specified value is invalid, F must be a subset of Q (F∩Q≠∅)")
            raise InputError("The specified value is invalid, F must be a subset of Q (F∩Q≠∅)")
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
        if f not in self.Q:
            LOG.error("The specified value is invalid, f must be a member of Q")
            raise InputError("The specified value is invalid, f must be a member of Q")

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
            LOG.error("The specified value is invalid, f must be a member of S")
            raise InputError("The specified value is invalid, f must be a member of S")

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

    def convert_to_deterministic(self):

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

        return DeterministicFiniteAutomaton(transition.keys(), self.S, " ".join(starting_state), final_states, delta = transition)


class LevenshteinAutomaton(NondeterministicFiniteAutomaton):
    """

    Constructs the levenshtein DFA of a given word. The automaton accepts all words
    with levenshtein_distance(word) <= depth

    You can define the alphabet of a Levenshtein automaton, allowing the automaton
    to recognize regular words.

    >>> D = LevenshteinAutomaton("canis", 2, alphabet = 'abcdefghijklmnopqrstuvwxyz')

    >>> D = D.convert_to_deterministic()

    >>> D.accepted("ca*s")
    True

    >>> D.accepted("ca***s")
    False

    >>> D.accepted("canem")
    True

    Note that the automaton is case-sensitive:

    >>> D.accepted("Canes")
    False

    """

    def __init__(self, word, depth, alphabet = 'abcdefghijklmnopqrstuvwxyz'):

        super().__init__(["q" + str(i * (len(word) + 1) + j) for i in range(depth + 1) for j in range(len(word) + 1)],
                         set(word + "*"), "q0", set(["q" + str((i + 1)*(len(word) + 1) - 1) for i in range(depth + 1)]),
                         isEpsilon = True)

        self.S.add(self.epsilon)
        self.alphabet = alphabet

        for i in range(depth):
            for j in range(len(word)):

                # Correct character
                self.add_transition(("q" + str((len(word) + 1) * i + j)), word[j], "q" + str((len(word) + 1) *
                                                                                             i + j + 1))

                # Insertion
                self.add_transition(("q" + str((len(word) + 1) * i + j)), self.epsilon, "q" + str((len(word) + 1) * (i + 1) + j + 1))

                # Substitution
                self.add_transition("q" + str((len(word) + 1) * i + j), "*", "q" + str((len(word) + 1) *
                                                                                       (i + 1) + j + 1))

                # Deletion
                self.add_transition("q" + str((len(word) + 1) * i + j), "*", "q" + str((len(word) + 1) * (i + 1) + j))

        for j in range(len(word)):
            self.add_transition("q" + str((len(word) + 1) * depth + j), word[j], "q" + str((len(word) + 1) *
                                                                                           depth + j + 1))
        for j in range(depth):
            self.add_transition("q" + str((len(word) + 1) * j + len(word)), "*", "q" + str((len(word) + 1) * (j + 1)
                                                                                               + len(word)))

    def convert_to_deterministic(self):
        A = super(LevenshteinAutomaton, self).convert_to_deterministic()
        return LevenshteinDeterministic(A.Q, A.S, A.s, A.F, A.transition, self.alphabet)


class LevenshteinDeterministic(DeterministicFiniteAutomaton):
    """
    Deterministic Levenshtein Automaton.
    """
    def __init__(self, Q, S, s, F, transition, alphabet):
        super().__init__(Q, S, s, F, transition)
        self.alphabet = alphabet

    def transition_function(self, qi, u):
        """
        :param qi: int: current state, qi ∈ Q
        :param u:str: transition character u ∈ S
        :returns Q': int :  δ(qi, u) = q
        """
        try:
            return self.transition[qi][u]
        except KeyError:
            if u in self.alphabet:
                try:
                    return self.transition[qi]['*']
                except KeyError:
                    return None
            return None


def make_worlist_trie(wordlist):
    """
    Creates a nested dictionary representing the trie created
    by the given word list.

    :param wordlist: str list:
    :return: nested dictionary

    >>> make_worlist_trie(['einander', 'einen', 'neben'])
    {'e': {'i': {'n': {'a': {'n': {'d': {'e': {'r': {'__end__': '__end__'}}}}}, 'e': {'n': {'__end__': '__end__'}}}}}, 'n': {'e': {'b': {'e': {'n': {'__end__': '__end__'}}}}}}

    """
    dicts = dict()

    for w in wordlist:
        curr = dicts
        for l in w:
            curr = curr.setdefault(l, {})
        curr['__end__'] = '__end__'

    return dicts

def walk_trie(dicts, w, q, A):
    """
    Helper function for traversing the word trie. It simultaneously keeps
    track of the active Automaton state, producing the intersection of the
    given Automaton and the trie (which is equivalent to a DFA). Once an 
    invalid "terminating" state is reached, the children nodes are immediately
    dismissed from the recursive stack
    """
    
    if q in A.F and '__end__' in dicts:
        yield w

    for key in dicts.keys():
        if key == '__end__':
            continue

        if A.transition_function(q, key) is None:
            return

        try:
            yield from walk_trie(dicts[key], w + key, A.transition_function(q, key), A)
        except:
            return


def spellcheck(word, wordlist, depth = 2):
    """
    Given a word list and a depth parameter, return all words w' in the wordlist
    with LevenshteinDistance(word, w') <= depth

    :param word:
    :param wordlist:

    >>> Dic = ['pes', 'pesse', 'pease', 'peis', 'peisse', 'pise', 'peose', 'poese', 'poisen']
    >>> spellcheck('pece', Dic, depth = 2)
    ['pease', 'peis', 'peose', 'pes', 'pesse', 'pise', 'poese']

    >>> spellcheck('pece', Dic, depth = 3)
    ['pease', 'peis', 'peisse', 'peose', 'pes', 'pesse', 'pise', 'poese']
    """
    Aut = LevenshteinAutomaton(word, depth = depth).convert_to_deterministic()
    W = make_worlist_trie(wordlist)

    return sorted(list(walk_trie(W, '', Aut.s, Aut)))

