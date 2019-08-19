from nfa import NFA


class Regex:
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
            elif Regex.is_operator(c):
                while (stack != []) and (stack[-1] != '(') and (Regex.has_less_or_equal_priority(c, stack[-1])):
                    postfix = postfix + stack[-1]
                    stack.pop()
                stack.append(c)
            else:
                postfix = postfix + c
        while stack:
            postfix = postfix + stack[-1]
            stack.pop()
        return list(postfix)

    @staticmethod
    def regex_to_nfa(regexp):
        new__regexp = ""
        for index, char in enumerate(regexp):
            new__regexp += char
            if not Regex.is_operator(char) and not Regex.is_operator(regexp[index + 1]):
                new__regexp += '.'

        regexp = Regex.to_postfix(new__regexp)
        print(regexp)
        stack_aux = []
        for token in regexp:
            if Regex.is_operator(token):
                if token == "*":
                    stack_aux.append(stack_aux.pop().kleene_closure())
                elif token == "|":
                    stack_aux.append(stack_aux.pop().concat(stack_aux.pop()))
                elif token == ".":
                    stack_aux.append(stack_aux.pop(-2).concat(stack_aux.pop(-1)))
                else:
                    stack_aux.append(stack_aux.pop().plus_closure())
            else:
                stack_aux.append(NFA({'0', '1'}, {('0', token): {'1'}}, '0', {'1'}))
        return stack_aux.pop()


a_union_b = Regex.regex_to_nfa('(abc)*')
a_union_b.print()
a_union_b.rename_all_states()
a_union_b.print()
print('--------------')
