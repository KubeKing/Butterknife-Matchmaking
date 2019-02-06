import json

def loadSent():
    with open('main\sentTo.json') as json_file: 
        return(json.load(json_file))

def overwrite(input):
    with open('main\sentTo.json', 'w') as outfile:
        json.dump(input, outfile)

def sent(email):
    save = loadSent()
    save.remove(email)
    with open('main\sentTo.json', 'w') as outfile:
        json.dump(save, outfile)