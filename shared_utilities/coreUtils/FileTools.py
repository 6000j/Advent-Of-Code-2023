# a handy useful writing data function helper thing
def write_data(oup, loc):
    '''Writes oup to the file at path loc, using utf-8 encoding'''
    f = open(loc, 'w', encoding='utf-8')
    f.write(oup)
    f.close()

# Reading data
def read_data(loc):
    '''Returns the data from the file at path loc, using utf-8 encoding'''
    f = open(loc, 'r', encoding='utf-8')
    contents = f.read()
    f.close()
    return contents