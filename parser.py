import sys
import re
import time

# DarbouxParser class
class DarbouxParser:

    def __init__(self):
        # a dictionary that maps key to list
        self.hof_dict = dict()
        self.hof_dict_fast = dict()
    
    # Takes in a string and see if it matches
    def match(self, hof_key, string, fast=False):
        if fast: return self.hof_dict_fast[hof_key](string)
        return self.hof_dict[hof_key](string)
    
    # Takes in a list and construct the hof function
    def construct(self, hof_key, lst):
        for ll in lst:
            for s in ll:
                if len(s) > 0 and s[0] == '"': continue
                if s not in self.hof_dict:
                    self.hof_dict[s] = lambda x: False
                    self.hof_dict_fast[s] = lambda x: False
        self.hof_dict[hof_key] = lambda x: any([self.matcher(x, l) for l in lst])
        self.hof_dict_fast[hof_key] = lambda x: any([self.matcher_fast(x, l) for l in lst])
        print(lst)

    # match string with list
    def matcher(self, s, st):
        if len(st) == 0 and s == '': return True
        if len(st) == 0: return False
        if (st[0][0] == '"'):
            mid = st[0][1:-1]
            if not s.startswith(mid): return False
            return self.matcher(s[len(mid):], st[1:])
        return any([(self.hof_dict[st[0]](s[:i]) and self.matcher(s[i:], st[1:])) for i in range(len(s) + 1)])
    
    # fast match
    def matcher_fast(self, s, st):
        if len(st) == 0 and s == '': return True
        if len(st) == 0: return False
        if (st[0][0] == '"'):
            mid = st[0][1:-1]
            if not s.startswith(mid): return False
            return self.matcher_fast(s[len(mid):], st[1:])
        mark = -1
        for i in range(len(st)):
            if (st[i][0] == '"'):
                mark = i
                break
        if mark == -1: return self.matcher(s, st)

        mid = st[mark][1:-1]
        occur = [m.start() for m in re.finditer(mid, s)]
        return any([(self.matcher(s[:x], st[:mark]) and self.matcher_fast(s[x + len(mid):], st[mark+1:])) for x in occur])




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
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

### BNF
### Maybe can convert to tree form? or higher order function form?

### extra: add in regular expression
### visualize out the tree (figure out the cs61a function)

### stack can consist of characters, functions (every symbol is a function)

### SPEECH
### I see the strings as the fixed points in the sequences. so no matter what, 
# # the sequence must match the string at some point
