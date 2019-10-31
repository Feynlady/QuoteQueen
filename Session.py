import random
from Quote_Data import Quote_data
from Parameter import Parameter
import re
'''
    This is the Session Object (our controller). 
'''
class Session(object):
    # Quote_data (our model / database etc.) is referenced via a static variable
    data = Quote_data

    def __init__(self):
        #List Of Parameters (stuff we base our prompts on / stuff we are listening out for)
        self.parameters = self.getParameters()
        #Current parameter (our current focus in conversation, if you will)
        self.current = self.parameters[0]
        #Pandas Dataframe with the quotes, which match the current information given
        self.plausibleQuotes = Session.data.database
        #TODO: We should also keep track of what database selection has been done already (i.e. columns and value of selection) That would be a dictionary initiated here I recckon.
    def input_processor(self,user_input):
        #simple preprocessing the input
        #TODO: more preprocessing (Removing stopwords, tokenization, stemming?, spellchecking? the worlds our oyster here really)
        user_input = user_input.lower()
        re.sub("[^a-zA-Z0-9_ <>=']", "", user_input)
        #scan the input for parameter values on cleaned input
        uinput_split = user_input.split()
        if self.current.name != 'End':
            self.getParamValues(uinput_split)
    def getParamValues(self,uinput_split):
        for x in uinput_split:
            for y in self.parameters:
                if x in y.possible_values.keys():
                    y.values.append(x)
                    y.complete = True
                    self.plausibleQuotes = Quote_data.select(self.plausibleQuotes,y.name,x)
                    print('len', len(self.plausibleQuotes))
        #print('CURRENT', self.current.name, ' complete ', self.current.complete )
        # change the current parameter, if all parameters have been filled, we set current to the end parameter
        #we need to see if this is actually what we want (entering life on the first line will automatically fill the parameter for tags and category)
        while(self.current.complete == True and self.current.name != 'End'):
            temp = self.parameters.index(self.current)
            if temp < len(self.parameters)-1:
                self.current = self.parameters[temp+1]
            else:
                self.current = self.parameters[len(self.parameters)-1]
    def reply(self, user_input):
        '''Generate response to user input'''
        self.input_processor(user_input)
        #get new prompts for still open parameters
        prompt = self.current.getPrompt()
        #if we have filled all parameters, then return a random quote of those matching the users inputs
        #as mentioned earlier we are done atm when all parameters are filled, but more user input could give us more suitable quotes
        # (but being careful that we still have a plausible quote left)
        if self.current.name== 'End':
            if(len(self.plausibleQuotes) >0):
                r = random.randrange(0,len(self.plausibleQuotes))
                quote = self.plausibleQuotes.iloc[r]
                prompt = quote[0], ' from ', quote[1]
        return prompt
    #these are the parameters we have at the minute, but I am thinking about making each category (we have 32) a parameter each.
    #we have about 25 000 tags, so these could be tokenized etc.
    def getParameters(self):
        param = []
        param.append(Parameter('Greeting', {}, False,
                  ['Hello, can I interest you in a quote?',
                   'Hey there! Do you want a quote?',
                    'Goooooood Morning. A quote?']))
        keywords = Parameter('Tags', Session.data.keywords, True,
                             ['This is a prompt for the the keywords'])
        category = Parameter('Category',Session.data.category, True,
                             ['Tell me more about what kind of quote you would like',
                              'What mood are you in?',
                              'Which genre would you like?'])
        param.append(category)
        param.append(keywords)
        param.append(Parameter('End', {}, False,
                               ['END']))
        return param