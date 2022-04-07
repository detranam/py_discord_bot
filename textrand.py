import random
class RandomText:
    def __init__(self,filepath):
        randofile = []

        for line in open(filepath):
            randofile.append(line)
        
        self.linecount = len(randofile)
        self.lines = randofile

    def rand_message(self):
        return self.lines[random.randrange(0,self.linecount)]