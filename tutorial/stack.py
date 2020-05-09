class Stack:
    def __init__(self):     # Init Stack
        self.stack = []     # Empty Stack

    def empty(self):        # Check if Stack is empty
        return len(self.stack) == 0

    def full(self):         # Check if Stack is full
        return False        # no need for max size (dynamically allocated space)

    def push(self, elem):       # Add new element to the Stack
        self.stack.append(elem)         # Push new element

    def pop(self):      # pop last inserted element
        if self.empty():
            return None

        return self.stack.pop(len(self.stack) - 1)      # return value of removed element


def match(c1, c2):       # Check if c1 and c2 match
    if c1 == '(':
        return c2 == ')'

    if c1 == '[':
        return c2 == ']'

    if c1 == '{':
        return c2 == '}'

    return False


def parenMatch(str):    # Main function: returns True if str is balanced
    s = Stack()         # Init empty stack s

    for d in str:       # For ever elem in str
        if d == '(' or d == '[' or d == '{':    # if d is opening parenthesis push to stack
            s.push(d)
        elif d == ')' or d == ']' or d == '}':  # if d is closing parenthesis
            if s.empty():
                print("More right parentheses than left parentheses")
                return False
            else:
                c = s.pop()             # pop paren c from stack
                if not match(c, d):     # check if c and d are not matching
                    print 'Mismatched parentheses:', c,'and', d
                    return False
        else:
            print("Invalid Input")
            return False

    if s.empty():   # if there are no parentheses left str is balanced
        print("Parentheses are balanced properly")
    else:
        print("More left parentheses than right parentheses")

    return s.empty()



# Main
str = raw_input("Give Input Expression without blanks: ")

parenMatch(str)

