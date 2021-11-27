import re

### BNF
### Maybe can convert to tree form? or higher order function form?

### extra: add in regular expression
### visualize out the tree (figure out the cs61a function)

### stack can consist of characters, functions (every symbol is a function)

test = '"(" correct ")" correct'
# stack ['"("', 'correct', '")"', 'correct']
# stack ['"("', hof, '")"', hof]


# match string with stack
def matcher(s, st):
    if len(st) == 0 and s == "":
        return True
    if len(st) == 0:
        return False
    if type(st[0]) is str:
        if not s.startswith(st[0]):
            return False
        return matcher(s[len(st[0]):], st[1:])
    return any([(st[0](s[:i]) and matcher(s[i:], st[1:])) for i in range(len(s))])

# DarbouxParser class
class DarbouxParser:

    def __init__(self):
        # maps name to dict
        self.hof_dict = dict()
    
    # Takes in a string and see if it matches
    def match(self, hof_key, string):
        return self.hof_dict[hof_key](string)
    
    # Takes in a list and construct the hof function
    def construct(self, hof_key, lst):
        for i in range(len(lst)):
            if len(lst[i]) > 0 and lst[i][0] == '"':
                continue
            if lst[i] not in self.hof_dict:
                self.hof_dict[lst[i]] = lambda x: False
            else:
                lst[i] = self.hof_dict[lst[i]]
        self.hof_dict[hof_key] = lambda x: matcher(x, lst)

def split(string):
    # split string based on symbols, chars
    return []

def match(string, stack):
    # see if string matches stack
    # returns true if does, false if no
    if string == "" and stack.isEmpty():
        return True
    elif string == "":
        return False
    return True

def test():
    # ((())) symmetric
    # ()()((())) balanced
    return True

def main():
    # handles input
    while True:
        c = input()

if __name__ == "__main__":
    main()