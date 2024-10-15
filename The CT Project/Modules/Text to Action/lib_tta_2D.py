#Text to action for CT-02

#Process -> Check for Request -> if not request, check for conversation
#First prototype: REMOVAL OF QUESTION MARK INSTEAD OF USING AS AN IDENTIFIER 
#-1 if words do not show up in any other sentences

import pickle

request_dictionary = {}
conversational_dictionary = {}
common_words = {}
deletion_repetition = 1

request_final = {}
conversational_final = {}

def training():
    training_file = open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\training_sentences.txt", "r", encoding="UTF-8")
    for sentence in training_file:
        #print(sentence)
        
        sentence = sentence.lower()
        sentence = sentence.split()
        
        for word in sentence:
            #remove ' from training data and replace with is
            if word.find("’s") >= 0:
                if request_dictionary.get("is") != None:
                    request_dictionary["is"] = request_dictionary["is"] + 1
                    
                else:
                    request_dictionary["is"] = 0
            
                word = word.replace("’s", "")
                
            #remove any punctuation from training data and replace with ""
            for letter in word:
                if not (ord(letter) >= 97 and ord(letter) <= 122): 
                    word = word.replace(letter, "")
            
            if request_dictionary.get(word) != None:
                request_dictionary[word] = request_dictionary[word] + 1
                
            else:
                request_dictionary[word] = 0
                
    #print(request_dictionary)    
    training_file.close()
    #print(request_dictionary)
    #print("\n")

    #Commence conversational dictionary
    conversational_file = open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\training_sentences_opp.txt", "r", encoding="UTF-8")
    for sentence in conversational_file:
        #print(sentence)
        
        sentence = sentence.lower()
        sentence = sentence.split()
        
        for word in sentence:
            #remove ' from training data and replace with is
            if word.find("’s") >= 0:
                if conversational_dictionary.get("is") != None:
                    conversational_dictionary["is"] = conversational_dictionary["is"] + 1
                    
                else:
                    conversational_dictionary["is"] = 0
            
                word = word.replace("’s", "")
                
            #remove any punctuation from training data and replace with ""
            for letter in word:
                if not (ord(letter) >= 97 and ord(letter) <= 122): 
                    word = word.replace(letter, "")
            
            if conversational_dictionary.get(word) != None:
                conversational_dictionary[word] = conversational_dictionary[word] + 1
                
            else:
                conversational_dictionary[word] = 0
                
    conversational_file.close()
    #print(conversational_dictionary)
    #print("\n")
    
    request_final = dict(request_dictionary)
    conversational_final = dict(conversational_dictionary)
    #Commence Filtration
    for item in request_dictionary:
        if request_dictionary.get(item) <= deletion_repetition:
            request_final.pop(item)
        
    for item in conversational_dictionary:
        if conversational_dictionary.get(item) <= deletion_repetition:
            conversational_final.pop(item)
            
    print(request_final)
    print(conversational_final)
    
    #Save Dictionary Data
    
    request_data = open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\request_data.pkl", "wb")
    pickle.dump(request_final, request_data)
    request_data.close()
    
    conversational_data = open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\conversational_data.pkl", "wb")
    pickle.dump(conversational_final, conversational_data)
    conversational_data.close()

def view_overlap(): #see which words overlap
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\request_data.pkl", "rb") as req_data:
        req_dict = dict(pickle.load(req_data))
        
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\conversational_data.pkl", "rb") as conv_data:
        conv_dict = dict(pickle.load(conv_data))
        
    for item in req_dict:
        if conv_dict.get(item) != None:
            print(f"Overlap found: {item} | Conv: {conv_dict.get(item)} | Req: {req_dict.get(item)}")

def process(sentence):
    
    phrase = sentence.split()
    sum = 0
    
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\request_data.pkl", "rb") as req_data:
        req_dict = dict(pickle.load(req_data))
        
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data\conversational_data.pkl", "rb") as conv_data:
        conv_dict = dict(pickle.load(conv_data))
    
    #Positive (Request Dict)
    for word in phrase:
        if req_dict.get(word) != None:
            sum += req_dict.get(word)
            
    for word in phrase:
        if conv_dict.get(word) != None:
            sum = sum - conv_dict.get(word)


    print(f"Sentence: {sentence} | Sum: {sum}")
    
    return sum
    
def testForConv():
    wrongly_identified = {}
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\test_sentences1.txt", "r+") as test_data:
        n_sentences = 0
        n_wrongsentences = 0
        for sentence in test_data:
            n_sentences += 1
            sentence = sentence.replace("\n", "")
            sum = process(sentence)
            
            if sum >= 0:
                n_wrongsentences += 1
                print("Wrongly Identified!\n")
                wrongly_identified[sentence] = sum
                
    
    test_data.close()
    
    print("\n")
    print(f"Wrongly Identified Sentences: \n{wrongly_identified}\n")
    print(f"Percentage Accuracy = {(n_sentences-n_wrongsentences)/n_sentences*100}%")
    
def testForReq():
    wrongly_identified = {}
    with open(r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\test_sentences.txt", "r+") as test_data:
        n_sentences = 0
        n_wrongsentences = 0
        for sentence in test_data:
            n_sentences += 1
            sentence = sentence.replace("\n", "")
            sum = process(sentence)
            
            if sum <= 0:
                n_wrongsentences += 1
                print("Wrongly Identified!\n")
                wrongly_identified[sentence] = sum
                
    
    test_data.close()
    
    print("\n")
    print(f"Wrongly Identified Sentences: \n{wrongly_identified}\n")
    print(f"Percentage Accuracy = {(n_sentences-n_wrongsentences)/n_sentences*100}%")
    
            
testForReq()