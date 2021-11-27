import sys
import re
import time

# DarbouxParser class
class DarbouxParser:

    def __init__(self):
        # a dictionary that maps key to list
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
                    self.hof_dict[s] = lambda x, t: False
        self.hof_dict[hof_key] = lambda x, t: any([self.matcher_fast(x, l) for l in lst]) if t else any([self.matcher(x, l) for l in lst])

    # match string with list
    def matcher(self, s, st):
        if len(st) == 0 and s == '': return True
        if len(st) == 0: return False
        if st[0][0] == '"':
            mid = st[0][1:-1]
            if not s.startswith(mid): return False
            return self.matcher(s[len(mid):], st[1:])
        return any([(self.hof_dict[st[0]](s[:i], False) and self.matcher(s[i:], st[1:])) for i in range(len(s) + 1)])
    
    # fast match
    def matcher_fast(self, s, st):
        if len(st) == 0 and s == '': return True
        if len(st) == 0: return False
        if st[0][0] == '"':
            mid = st[0][1:-1]
            if not s.startswith(mid): return False
            return self.matcher_fast(s[len(mid):], st[1:])
        
        mark = -1
        for i in range(len(st)):
            if st[i][0] == '"':
                mark = i
                break
        if mark == -1: return self.matcher(s, st)

        mid = st[mark][1:-1]
        occurrence = [m.start() for m in re.finditer(mid, s)]
        return any([(self.matcher(s[:x], st[:mark]) and self.matcher_fast(s[x + len(mid):], st[mark+1:])) for x in occurrence])

# returns (key_name, list of possible sequences split by "|")
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

def main():

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