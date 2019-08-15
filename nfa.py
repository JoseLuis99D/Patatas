class NFA:
    def __init__(self, states, transition, start_state, accept_states):
        self.states = states
        self.transition = transition
        self.start_state = start_state
        self.accept_states = accept_states
    def next_states(self, state, char='epsilon'):
        input = (state, char)
        if input in self.transition:
            return self.transition[input]
        else:
            return []
    def compute(self, string, states):
        result = set()
        if len(string) == 0:
            return states
        else:
            for state in states:
                for s in self.eclousure(state):
                    result = result.union(self.next_states(s, string[0]))
        return self.compute(string[1:], result)
    def eclousure(self, state):
        set_clousure = []
        stack = [state]
        while stack!=[]:
            s = stack.pop()
            if s not in set_clousure:
                set_clousure.append(s)
                for new_state in self.next_states(s):
                    if new_state not in set_clousure:
                        set_clousure.append(new_state)
                        stack.append(new_state)
        return set_clousure

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
            new_transition[('p' + state1, 'epsilon')] = 'q' + nfa.start_state
        return NFA(new_states, new_transition, new_start_state, new_accept_states)

    def union(self, nfa):
        new_states = {'p' + s for s in self.states}.union({'q' + s for s in nfa.states})
        new_states.add('s' + self.start_state + nfa.start_state)
        new_start_state = 's' + self.start_state + nfa.start_state
        new_accept_states = {'p' + s for s in self.accept_states}.union({'q' + s for s in nfa.accept_states})
        new_transition = {}
        for k, v in self.transition.items():
            new_transition[('p' + k[0], k[1])] = {'p' + s for s in v}
        for k, v in nfa.transition.items():
            new_transition[('q' + k[0], k[1])] = {'q' + s for s in v}
        new_transition[('s' + self.start_state + nfa.start_state, 'epsilon')] = 'p' + self.start_state
        new_transition[('s' + self.start_state + nfa.start_state, 'epsilon')] = 'q' + nfa.start_state
        return NFA(new_states, new_transition, new_start_state, new_accept_states)


#transition = {('0', 'epsilon'): {'1','3'}, ('1', 'a'): {'2'}, ('3', 'b'): {'4'}, ('2', 'epsilon'): {'5'}, ('4', 'epsilon'): {'5'}}
#nfa = NFA({'0', '1', '2', '3', '4', '5'}, transition, '0', {'5'})
#print(nfa.eclousure('0'))
#print(nfa.eclousure('1'))
#print(nfa.eclousure('2'))

t = {('0', 'a'): {'1'}, ('1', 'b'): {'1'}, ('1', 'a'): {'2'}}
nfa = NFA({'0', '1', '2'}, t, '0', {'2'})
print(nfa.compute('abbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbba', nfa.eclousure(nfa.start_state)))

# transition1 = {('1', 'a'): '2'}
# nfa1 = NFA({'1', '2'}, transition1, '1', {'2'})
# transition2 = {('3', 'b'): '4'}
# nfa2 = NFA({'3', '4'}, transition2, '3', {'4'})
# nf3 = nfa1.union(nfa2)
# print(nf3.states)
