import pandas
'''
    This is the Quote_data class (our model/ our data). The database is loaded into here as a Pandas Dataframe. 
    The actions we do on our data are also done here (selection etc).
'''
class Quote_data(object):
    def __init__(self):
        self.database = pandas.read_json('quotes.json')
        self.keywords = {}
        for x in self.database['Tags']:
            for y in x:
                if y not in self.keywords.keys():
                    self.keywords[y] = 1
                else:
                    self.keywords[y] += 1
        self.category ={}
        for x in self.database['Category']:
            if x not in self.category.keys():
                self.category[x] = 1
            else:
                self.category[x] += 1
        print(self.category)
        print(self.keywords)

    def select(self, data, column, word):
        if column in data.columns:
            product = data[data[column].str.contains(word, regex = False)]
            #print(product)
            if(len(product) > 0):
                return product
            else:
                print('TOO SPECIFIC; NOT ENOUGH QUOTES')
        return data
Quote_data = Quote_data()


