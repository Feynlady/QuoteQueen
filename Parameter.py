import random
class Parameter(object):
    # these are our parameters, stuff we are asking for/ stuff we are listening for
    def __init__(self, name, poss_vals, req, prompts):
        self.name = name
        self.required = req
        self.prompts = prompts
        self.possible_values = poss_vals
        self.values = []
        #this determines whether these are mandatory parameters,which dont have to be filled (i.e. forceably executed once )
        # like the greeting
        if(len(poss_vals) == 0):
            self.complete = True
        else:
            self.complete = False

    def getPrompt(self):
        r = random.randrange(0, len(self.prompts))
        return self.prompts[r]