from nfa import NFA


class RegexUtils:
    @staticmethod
    def is_operator(char):
        if "*|.+()".find(char) != -1:
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


def regex_to_nfa(regexp):
    new__regexp = ""
    for index, char in enumerate(regexp):
        new__regexp += char
        if not RegexUtils.is_operator(char) and not RegexUtils.is_operator(regexp[index+1]):
            new__regexp += '.'

    regexp = RegexUtils.to_postfix(new__regexp)
    print(regexp)
    stack_aux = []
    for token in regexp:
        if RegexUtils.is_operator(token):
            aux = stack_aux.pop()
            if token == "*":
                if isinstance(aux, NFA):
                    stack_aux.append(aux.kleene_closure())
                else:
                    stack_aux.append(NFA({'0', '1'}, {('0', aux): {'1'}}, '0', {'1'}).kleene_closure())
            elif token == "|":
                aux2 = stack_aux.pop()
                if isinstance(aux, NFA) == isinstance(aux2, NFA):
                    if isinstance(aux, NFA):
                        stack_aux.append(aux.union(aux2))
                    else:
                        aux_nfa = NFA({'0', '1'}, {('0', aux): {'1'}}, '0', {'1'})
                        stack_aux.append(NFA({'0', '1'}, {('0', aux2): {'1'}}, '0', {'1'}).union(aux_nfa))
                else:
                    if isinstance(aux2, NFA):
                        aux3 = aux
                        aux = aux2
                        aux2 = aux3
                    stack_aux.append(aux.union(NFA({'0', '1'}, {('0', aux2): {'1'}}, '0', {'1'})))
            elif token == ".":
                aux2 = stack_aux.pop()
                if isinstance(aux, NFA) == isinstance(aux2, NFA):
                    if isinstance(aux, NFA):
                        stack_aux.append(aux2.concat(aux))
                    else:
                        aux_nfa = NFA({'0', '1'}, {('0', aux): {'1'}}, '0', {'1'})
                        stack_aux.append(NFA({'0', '1'}, {('0', aux2): {'1'}}, '0', {'1'}).concat(aux_nfa))
                else:
                    if isinstance(aux, NFA):
                        stack_aux.append(NFA({'0', '1'}, {('0', aux2): {'1'}}, '0', {'1'}).concat(aux))
                    else:
                        stack_aux.append(aux2.concat(NFA({'0', '1'}, {('0', aux): {'1'}}, '0', {'1'})))
            else:
                if isinstance(aux, NFA):
                    stack_aux.append(aux.plus_closure())
                else:
                    stack_aux.append(NFA({'0', '1'}, {('0', aux): {'1'}}, '0', {'1'}).plus_closure())
        else:
            stack_aux.append(token)
    return stack_aux.pop()


a_union_b = regex_to_nfa('(abc)*')
a_union_b.print()
a_union_b.rename_all_states()
a_union_b.print()
print('--------------')
