import copy


class NFA:
    def __init__(self, states, transition, start_state, accept_states):
        self.states = states
        self.transition = transition
        self.start_state = start_state
        self.accept_states = accept_states

    def rename_state(self, old_state, new_state):
        if old_state in self.states:
            self.states.remove(old_state)
            self.states.add(new_state)
            if self.start_state == old_state:
                self.start_state = new_state
            if old_state in self.accept_states:
                self.accept_states.remove(old_state)
                self.accept_states.add(new_state)
            new_transition = {}

            for key in self.transition:
                li = self.transition[key]
                if old_state in li:
                    li.remove(old_state)
                    li.add(new_state)

                if key[0] == old_state:
                    new_transition[(new_state, key[1])] = li
                else:
                    new_transition[key] = li
            self.transition = new_transition

    def rename_all_states(self):
        states_saver = self.states.copy()
        for i, state in enumerate(states_saver):
            self.rename_state(state, str(i))

    def print(self):
        print("{")
        print("\t" + str(self.states))
        print("\t" + str(self.start_state))
        print("\t" + str(self.accept_states))
        print("\t" + str(self.transition))
        print("}\n")

    def accept(self, string):
        result_set = self.compute(string, self.e_closure(self.start_state))
        for result in result_set:
            for eresult in self.e_closure(result):
                if eresult in self.accept_states:
                    return True
        return False

    def next_states(self, state, char='epsilon'):
        input_tuple = (state, char)
        if input_tuple in self.transition:
            return self.transition[input_tuple]
        else:
            return []

    def compute(self, string, states):
        result = set()
        if len(string) == 0:
            return states
        else:
            for state in states:
                for s in self.e_closure(state):
                    result = result.union(self.next_states(s, string[0]))
        return self.compute(string[1:], result)

    def e_closure(self, state):
        set_closure = []
        stack = [state]
        while stack:
            s = stack.pop()
            if s not in set_closure:
                set_closure.append(s)
            for new_state in self.next_states(s):
                if new_state not in set_closure:
                    set_closure.append(new_state)
                    stack.append(new_state)
        return set_closure

    def concat(self, nfa):
        new_states = {'p' + s for s in self.states}.union({'q' + s for s in nfa.states})
        new_start_state = 'p' + self.start_state
        new_accept_states = {'q' + s for s in nfa.accept_states}
        new_transition = {}
        for k, v in self.transition.items():
            new_transition[('p' + k[0], k[1])] = {'p' + s for s in v}
        for k, v in nfa.transition.items():
            new_transition[('q' + k[0], k[1])] = {'q' + s for s in v}
        for state1 in self.accept_states:
            new_transition[('p' + state1, 'epsilon')] = {'q' + nfa.start_state}
        return NFA(new_states, new_transition, new_start_state, new_accept_states)

    def union(self, nfa):
        new_states = {'p' + s for s in self.states}.union({'q' + s for s in nfa.states})
        new_states.add('s' + self.start_state + nfa.start_state)
        new_states.add('f' + self.start_state + nfa.start_state)
        new_start_state = 's' + self.start_state + nfa.start_state
        new_accept_states = {'f' + self.start_state + nfa.start_state}
        new_transition = {}
        for k, v in self.transition.items():
            new_transition[('p' + k[0], k[1])] = {'p' + s for s in v}
        for k, v in nfa.transition.items():
            new_transition[('q' + k[0], k[1])] = {'q' + s for s in v}
        for state in self.accept_states:
            new_transition[('p' + state, 'epsilon')] = {'f' + self.start_state + nfa.start_state}
        for state in nfa.accept_states:
            new_transition[('q' + state, 'epsilon')] = {'f' + self.start_state + nfa.start_state}
        new_transition[('s' + self.start_state + nfa.start_state, 'epsilon')] = {'p' + self.start_state,
                                                                                 'q' + nfa.start_state}
        return NFA(new_states, new_transition, new_start_state, new_accept_states)

    def kleene_closure(self):
        new_nfa = self.plus_closure()
        for key, next_states in new_nfa.transition.items():
            if key[0] == 'q_i' + self.start_state:
                next_states.add('q_f' + self.start_state)
                return new_nfa

    def plus_closure(self):
        new_states = self.states.copy()
        new_states.add('q_i' + self.start_state)
        new_states.add('q_f' + self.start_state)
        new_start_state = 'q_i' + self.start_state
        new_accept_states = {'q_f' + self.start_state}
        new_transition = copy.deepcopy(self.transition)
        new_transition[('q_i' + self.start_state, 'epsilon')] = {self.start_state}
        for state in self.accept_states:
            new_transition[(state, 'epsilon')] = {'q_f' + self.start_state, self.start_state}
        return NFA(new_states, new_transition, new_start_state, new_accept_states)


"""
transition = {('0', 'epsilon'): {'1','3'}, ('1', 'a'): {'2'}, ('3', 'b'): {'4'}, ('2', 'epsilon'): {'5'}, ('4', 'epsilon'): {'5'}}
nfa = NFA({'0', '1', '2', '3', '4', '5'}, transition, '0', {'5'})

trans2 = {('0', '0'): {'0'}, ('0', '1'): {'1'}, ('1', '0'): {'2'}, ('2', '0'): {'1'}, ('2', '1'): {'5'}, ('2', 'epsilon'): {'3'}, ('3', '0'): {'4'}, ('4', '0'): {'3'}, ('4', '1'): {'5'}}
nfa2 = NFA({'0', '1', '2', '3', '4', '5'}, trans2, '0', {'5'})

trans3 = {('1', 'a'): {'2'}, ('2', 'epsilon'): {'3'}, ('3', 'epsilon'): {'4'}, ('4', 'b'): {'5'}}
nfa3 = NFA({'1', '2', '3', '4', '5'}, trans3, '1', {'5'})

trans4 = {('0', 'a'): {'1'}}
nfa4 = NFA({'0', '1'}, trans4, '0', {'1'})

trans6 = {('0', 'b'): {'1'}}
nfa6 = NFA({'0', '1'}, trans6, '0', {'1'})

nfa7 = nfa4.concat(nfa6)
nfa7 = nfa7.kleene_closure()

print(nfa7.accept('ab'))
print(nfa7.accept('ba'))
print(nfa7.accept('ababababababababababab'))
print(nfa7.accept('abababababababababababa'))
print(nfa7.accept(''))
"""
