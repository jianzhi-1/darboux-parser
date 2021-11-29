import sys
import re
import time

# DarbouxParser class
class DarbouxParser:

    def __init__(self):
        # Dictionary that maps key to list
        self.hof_dict = dict()
    
    # Takes in a string and see if it matches
    def match(self, hof_key, string, fast=False):
        return self.hof_dict[hof_key](string, fast)
    
    # Takes in a list and construct the hof function
    def construct(self, hof_key, lst):
        for ll in lst:
            for s in ll:
                if len(s) > 0 and s[0] == '"': continue
                if s not in self.hof_dict:
                    self.hof_dict[s] = lambda x, t: False # Initializes empty lambda function
        self.hof_dict[hof_key] = lambda x, t: any([self.matcher_fast(x, l) for l in lst]) if t else any([self.matcher(x, l) for l in lst])

    # Algorithm 1: match string with list
    def matcher(self, s, lst):
        if len(lst) == 0 and s == '': return True
        if len(lst) == 0: return False
        if lst[0][0] == '"':
            mid = lst[0][1:-1]
            if not s.startswith(mid): return False
            return self.matcher(s[len(mid):], lst[1:])
        return any([(self.hof_dict[lst[0]](s[:i], False) and self.matcher(s[i:], lst[1:])) for i in range(len(s) + 1)])
    
    # Algorithm 2: fast match
    def matcher_fast(self, s, lst):
        if len(lst) == 0 and s == '': return True
        if len(lst) == 0: return False
        if lst[0][0] == '"':
            mid = lst[0][1:-1]
            if not s.startswith(mid): return False
            return self.matcher_fast(s[len(mid):], lst[1:])
        
        mark = -1
        for i in range(len(lst)):
            if lst[i][0] == '"':
                mark = i
                break
        if mark == -1: return self.matcher(s, lst)

        mid = lst[mark][1:-1]
        occurrence = [m.start() for m in re.finditer(mid, s)]
        return any([(self.matcher_fast(s[x + len(mid):], lst[mark+1:]) and self.matcher(s[:x], lst[:mark])) for x in occurrence])

# Returns (key_name, list of possible sequences split by "|")
def format_line(line):
    line = line.strip()
    counter = 0

    for i in range(len(line)):
        if line[i] == ":":
            counter = i
            break
    
    k = line[:counter]
    line = line[counter + 1:]
    lst_lst = []

    for l in line.split("|"):
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
    
    return k, lst_lst

def main(fast=False):

    dp = DarbouxParser()

    with open(sys.argv[1]) as f:
        lines = f.readlines()
        for line in lines:
            (k, lst) = format_line(line)
            dp.construct(k, lst)
    print("Match!" if dp.match("start", sys.argv[2], fast) else "No Match!")

if __name__ == "__main__":
    start_time = time.time()
    main()
    normal_time = time.time()
    main(True)
    fast_time = time.time()

    print("--- Status ---")
    print("Normal: %s seconds" % (normal_time - start_time))
    print("Fast: %s seconds" % (fast_time - normal_time))
    print("Diff: %s seconds" % ((fast_time - normal_time) - (normal_time - start_time)))