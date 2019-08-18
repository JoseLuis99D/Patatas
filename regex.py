from nfa import NFA


def regex_to_nfa(regexp):
    regexp = RegexUtils.to_postfix(regexp)
    print(regexp)
    stack_aux = []
    regexp_nfa = None
    for token in regexp:
        if RegexUtils.is_operator(token):
            if token == "*":
                if regexp_nfa:
                    regexp_nfa = regexp_nfa.kleene_closure()
                else:
                    regexp_nfa = NFA({'0', '1'}, {('0', stack_aux.pop()): {'1'}}, '0', {'1'}).kleene_closure()
            elif token == "|":
                if regexp_nfa:
                    regexp_nfa = regexp_nfa.union(NFA({'0', '1'}, {('0', stack_aux.pop()): {'1'}}, '0', {'1'}))
                else:
                    aux_nfa = NFA({'0', '1'}, {('0', stack_aux.pop()): {'1'}}, '0', {'1'})
                    regexp_nfa = NFA({'0', '1'}, {('0', stack_aux.pop()): {'1'}}, '0', {'1'}).union(aux_nfa)
            elif token == ".":
                if regexp_nfa:
                    regexp_nfa = regexp_nfa.concat(NFA({'0', '1'}, {('0', stack_aux.pop()): {'1'}}, '0', {'1'}))
                else:
                    aux_nfa = NFA({'0', '1'}, {('0', stack_aux.pop()): {'1'}}, '0', {'1'})
                    regexp_nfa = NFA({'0', '1'}, {('0', stack_aux.pop()): {'1'}}, '0', {'1'}).concat(aux_nfa)
            else:
                if regexp_nfa:
                    regexp_nfa = regexp_nfa.plus_closure()
                else:
                    regexp_nfa = NFA({'0', '1'}, {('0', stack_aux.pop()): {'1'}}, '0', {'1'}).plus_closure()
        else:
            stack_aux.append(token)
    return regexp_nfa


class RegexUtils:
    @staticmethod
    def is_operator(char):
        if char == '*' or char == '|' or char == '.' or char == '+':
            return True
        return False

    @staticmethod
    def has_less_or_equal_priority(char, operator):
        operators = {'*': 3, '+': 3, '.': 2, '|': 1, '(': 0}
        return operators[char] <= operators[operator]

    @staticmethod
    def to_postfix(infix):
        stack = []
        postfix = ''
        for c in infix:
            if c == '(':
                stack.append(c)
            elif c == ')':
                while not stack[-1] == '(':
                    postfix = postfix + stack[-1]
                    stack.pop()
                stack.pop()
            elif RegexUtils.is_operator(c):
                while (stack != []) and (stack[-1] != '(') and (RegexUtils.has_less_or_equal_priority(c, stack[-1])):
                    postfix = postfix + stack[-1]
                    stack.pop()
                stack.append(c)
            else:
                postfix = postfix + c
        while stack:
            postfix = postfix + stack[-1]
            stack.pop()
        return list(postfix)


a_union_b = regex_to_nfa('a|b*')
a_union_b.print()
print('--------------')
