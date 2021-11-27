import re
import sys

### BNF
### Maybe can convert to tree form? or higher order function form?

### extra: add in regular expression
### visualize out the tree (figure out the cs61a function)

### stack can consist of characters, functions (every symbol is a function)

test = 'correct: "" | "(" correct ")" correct'
# stack ['"("', 'correct', '")"', 'correct']
# stack ['"("', hof, '")"', hof]


#### REMEMBER TO REMOVE THE QUOTATION MARKS!!!

# match string with stack
def matcher(s, st):
    
    if len(st) == 0 and s == "":
        print("matching ", s, st, "result: True")
        return True
    if len(st) == 0:
        print("matching ", s, st, "result: False")
        return False
    if type(st[0]) is str:
        if not s.startswith(st[0]):
            print("matching ", s, st, "result: False")
            return False
        print("matching ", s, st, "result: ", matcher(s[len(st[0]):], st[1:]))
        return matcher(s[len(st[0]):], st[1:])
    print("matching ", s, st, "result: ", any([(st[0](s[:i]) and matcher(s[i:], st[1:])) for i in range(len(s))]))
    return any([(st[0](s[:i]) and matcher(s[i:], st[1:])) for i in range(len(s))])

# DarbouxParser class
class DarbouxParser:

    def __init__(self):
        # maps name to dict
        self.hof_dict = dict()
    
    # Takes in a string and see if it matches
    def match(self, hof_key, string):
        print("matching string: {}".format(string))
        print(self.hof_dict.keys())
        print(self.hof_dict[hof_key])
        return self.hof_dict[hof_key](string)
    
    # Takes in a list and construct the hof function
    def construct(self, hof_key, lst):
        print("constructing {} : {}".format(hof_key, lst))
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                if len(lst[i][j]) > 0 and lst[i][j][0] == '"':
                    continue
                if lst[i][j] not in self.hof_dict:
                    print(lst[i][j], " is defined")
                    self.hof_dict[lst[i][j]] = lambda x: False
                else:
                    lst[i][j] = self.hof_dict[lst[i][j]]
        self.hof_dict[hof_key] = lambda x: any([matcher(x, l) for l in lst])
        print(lst)

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

def format_line(line):
    line = line.strip()
    counter = 0
    for i in range(len(line)):
        if line[i] == ":":
            counter = i
            break
    k = line[:counter]
    line = line[counter + 1:]
    line_lst = line.split("|")
    lst_lst = []
    for l in line_lst:
        l = l.strip()
        lst = []
        prev = 0
        quote = 0
        for i in range(len(l)):
            if l[i] == " " and quote % 2 == 0:
                lst.append(l[prev:i])
                prev = i + 1
                quote = 0
            elif l[i] == '"':
                quote += 1
        lst.append(l[prev:])
        lst_lst.append(lst)
    print(lst_lst)
    return k, lst_lst
    lst = []
    prev = 0
    quote = 0
    for i in range(len(line)):
        if line[i] == " " and quote % 2 == 0:
            lst.append(line[prev:i])
            prev = i + 1
            quote = 0
        elif line[i] == '"':
            quote += 1
    lst.append(line[prev:])
    return lst[0][:-1], lst[1:]

def main():
    # handles input
    print(sys.argv)

    dp = DarbouxParser()

    with open(sys.argv[1]) as f:
        lines = f.readlines()
        for line in lines:
            print(line.strip())
            (k, lst) = format_line(line)
            dp.construct(k, lst)
    
    print(dp.match("start", sys.argv[2]))


if __name__ == "__main__":
    main()