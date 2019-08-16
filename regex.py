from nfa import NFA

class Regex:
    def __init__(self, regexp):
        tokens = Regex.toPostfix(regexp)
        print(tokens)
        translation = []
        i = 0
        for token in tokens:
            if token == '*':
                translation[i-1] = translation.pop(i-1).kleene_clousure()
                i-=1
            elif token == '+':
                translation[i-1] = translation.pop(i-1).plus_clousure()
                i-=1
            elif token == '.':
                translation[i-2] = translation.pop(i-2).concat(translation.pop(i-1))
                i-=2
            elif token == '|':
                print(i)
                translation[i-2] = translation.pop(i-2).union(translation.pop(i-1))
                i-=2
            elif type(token) == str:
                translation.append(NFA({'0', '1'}, {('0', token): '1'}, '0', {'1'}))
                i+=1
        translation[0].print()


    def isOperand(char):
        if char=='*' or char=='|' or char=='.' or char=='+':
            return True
        return False
    def hasLessOrEqualPriority(char, operator):
        operators = {'*':  3, '+': 3, '.': 2, '|': 1, '(': 0}
        return operators[char] <= operators[operator]
    def toPostfix(infix):
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
            elif Regex.isOperand(c):
                while (stack != []) and (stack[-1] != '(') and (Regex.hasLessOrEqualPriority(c, stack[-1])):
                    postfix = postfix + stack[-1]
                    stack.pop()
                stack.append(c)
            else:
                postfix = postfix + c

        while stack != []:
            postfix = postfix + stack[-1]
            stack.pop()
        return list(postfix)


#print(Regex.toPostfix('a|b*.c'))
a = Regex('a')
print('--------------')
b = Regex('a|b')
print('--------------')
c = Regex('b')
