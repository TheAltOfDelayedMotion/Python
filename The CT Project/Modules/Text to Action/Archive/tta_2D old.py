import pickle
import math
from colorama import Fore

#Dictionaries 
#Z Axis Dictionaries 
request_dictionary = {}
conversational_dictionary = {}
request_final = {}
conversational_final = {}

#X & Y Axis Dictionaries #Will base training off 30 examples
n_xytrain_sentences = 30
google_dictionary = {}
room_dictionary = {}
music_dictionary = {}
alarm_dictionary = {} #Only for alarm setting
timer_dictionary = {} #
calendar_dictionary = {}
log_dictionary = {}
command_dictionary = {} #CT-02 Specific Commands
listofcats = ["google", "room", "music", "alarm", "timer", "calendar", "log", "command"]
listofdicts = [google_dictionary, room_dictionary, music_dictionary, alarm_dictionary, timer_dictionary, calendar_dictionary, log_dictionary, command_dictionary]

'''
Wake me up at 4.22 p.m.
Wake me up at 6.15 a.m.
'''

common_words = {}
deletion_repetition = 1 #Delete trained word if only repeated once

#Paths
T_NEUTRAL = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\train_neutral.txt"
T_REQUEST = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\train_requests.txt"
T_TEST_NEUTRAL = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\test_neutral.txt"
T_TEST_REQUEST = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\test_requests.txt"
T_XY_TRAINING = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\XY_training.txt"

def training():
    request_file = open(T_REQUEST, "r", encoding="UTF-8")
    for sentence in request_file:
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
    request_file.close()
    #print(request_dictionary)
    #print("\n")

    #Commence conversational dictionary
    conversational_file = open(T_NEUTRAL, "r", encoding="UTF-8")
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

def train(loops = 1, cutoff_score = 6): #Number of training loops
    loopnumber = 1
    dictionary_number = -1 #Everytime a header is seen, dictionary_number +1
    n_dictionaries = len(listofdicts)
    
    while loopnumber <= loops:
        loopnumber += 1
        
        #Commence Training for requests
        training_file = open(T_XY_TRAINING, "r", encoding="UTF-8")
        
        #Reading the training file
        for sentence in training_file:
            sentence = sentence.lower()
            
            if sentence.find("///") != -1: #if this is a header line
                sentence = sentence.replace("///", "")
                print(Fore.YELLOW + f"[TTA] Dictionary Training: {sentence}" + Fore.RESET)
                dictionary_number += 1
                
            else:
                if dictionary_number != -1 and dictionary_number < n_dictionaries: #do not allow training to start if start header was not read or if dictionary number exceeds range
                    sentence = sentence.split()
                    
                    for word in sentence:
                        #remove ' from training data and replace with is
                        if word.find("’s") >= 0:
                            if listofdicts[dictionary_number].get("is") != None:
                                listofdicts[dictionary_number]["is"] = listofdicts[dictionary_number]["is"] + 1
                                
                            else:
                                listofdicts[dictionary_number]["is"] = 0
                        
                            word = word.replace("’s", "")

                        if word != "a.m." and word != "p.m.":
                            #remove any punctuation from training data and replace with ""
                            for letter in word:
                                if not (ord(letter) >= 97 and ord(letter) <= 122): 
                                    word = word.replace(letter, "")
                        
                        #writing to dictionary
                        if listofdicts[dictionary_number].get(word) != None: #if it is found in the dictionary!
                            listofdicts[dictionary_number][word] = listofdicts[dictionary_number][word] + 1
                            
                        else: #if it is not, create a new value for it
                            listofdicts[dictionary_number][word] = 0                        
                    
        training_file.close()
        
        for dictionary in listofdicts: #Repeat for all dictionaries
            temp_dict = dict(dictionary)
            print(Fore.LIGHTRED_EX + f"[TTA] Filtering Data..." + Fore.RESET)
            for item in temp_dict:
                if temp_dict.get(item) <= deletion_repetition:
                    dictionary.pop(item)
                    
        for dictionary in listofdicts: #Repeat for all dictionaries
            print(Fore.YELLOW + "[TTA] Scaling Data..." + Fore.RESET)
            for item in dictionary:
                dictionary[item] = dictionary[item]/n_xytrain_sentences

        #Save Dictionary Data
        n = 0
        for dictionary in listofdicts: #Repeat for all dictionaries
            print(Fore.LIGHTGREEN_EX + f"[TTA] Saving Dictionary {n} Data" + Fore.RESET)
            print(dictionary)
            print("\n")
            path = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data" + f"\{n}_data.pkl"
            
            with open(path, "wb") as file:
                pickle.dump(dictionary, file)
            file.close()    
        
            n += 1

# def addVector(vector1, vector2): #vector = [magnitude, direction] vector 2 must come after vector 1
#     m1, d1 = vector1
#     m2, d2 = vector2
    
#     if d2 > d1:
#         if m1 == 0:
#             return vector2
        
#         else:
#             basic_a = ((180-(d2-d1))/180) * math.pi
#             m_r = math.sqrt(m1*m1 + m2*m2 -2*m1*m2*(math.cos(basic_a)))
#             d_r = d1 + ((180-(d2-d1))/m_r)*m2
            
#             #print(f"[TTA] M_r: {m_r} | D_r: {d_r}")
#             return [m_r, d_r]
    
#     else:
#         print("Error: Wrong Format!")
#         return None

# def addVectorNew(vector1, vector2):
#     if vector1[1] > vector2[1]: #perform swap if vector 1 > vector 2 in direction
#         v1 = vector2
#         v2 = vector1
        
#     else:
#         v1 = vector1
#         v2 = vector2

#     m1, d1 = v1
#     m2, d2 = v2
    
#     if m1 == 0: #if m1 has a magnitude of 0, that means vector 2 is only applicable
#         return v2
    
#     elif m2 == 0: #if m2 has a magnitude of 0, that means vector 1 is only applicable
#         return v1
    
#     else: #else if both are relevant vectors
#         if d1 == d2: #if both vectors have the same direction, that means that they add directly to each other
#             m_r = m1 + m2
#             d_r = d1
            
#         else:
#             if d2 - d1 < 180: #only for vectors that are seemingly acute
#                 print(f"[BUG] Acute {d2-d1}")
#                 basic_a = ((180-(d2-d1))/180) * math.pi
#                 m_r = math.sqrt(m1*m1 + m2*m2 -2*m1*m2*(math.cos(basic_a)))
#                 d_r = d1 + ((180-(d2-d1))/m_r)*m2
                
#                 #print(f"[TTA] M_r: {m_r} | D_r: {d_r}")

#             elif d2 - d1 == 180:
#                 if m1 > m2:
#                     d_r = d1
#                     m_r = m1 - m2
                    
#                 else:
#                     d_r = d2
#                     m_r = m2 - m1
                    
#             else: #if it is an obtuse angle
#                 print(f"[BUG] Obtuse {d2-d1}")
#                 basic_a = (((d2-d1)-180)/180) *math.pi
#                 m_r = math.sqrt(m1*m1 + m2*m2 -2*m1*m2*(math.cos(basic_a)))
#                 d_r = 360-(((((d2-d1)-180)/m_r)*m2)-d1)
#                 print(((((d2-d1)-180)/m_r)*m2))
                
#                 # if 360-(((((d2-d1)-180)/m_r)*m2)-d1) < d2:
#                 #     0 + (360 - d2)-(360-(((((d2-d1)-180)/m_r)*m2)-d1))
                
                

#         print(d_r)
#         return [m_r, d_r]

def isInRange(min, max, value):
    if value > min and value < max:
        return True

def addVectorListNew(vectors):
    x_forces = []
    y_forces = []
    for vector in vectors: #find the x & y component of each vector
        magnitude, direction = vector
        
        if direction == 360: #just in case
            direction = 0
        if isInRange(0, 90, direction): #quadrant 1 (+x, +y)
            a = 90 - direction
            a = (a/180)*math.pi #convert to radians
            Fx = math.cos(a) * magnitude
            Fy = math.sin(a) * magnitude
        elif isInRange(90, 180, direction): #quadrant 2 (+x, -y)
            a = direction - 90
            a = (a/180)*math.pi #convert to radians
            Fx = math.cos(a) * magnitude
            Fy = -(math.sin(a) * magnitude)
        elif isInRange(180, 270, direction): #quadrant 3 (-x, -y)
            a = 270 - direction
            a = (a/180)*math.pi #convert to radians
            Fx = -(math.cos(a) * magnitude)
            Fy = -(math.sin(a) * magnitude)
        elif isInRange(270, 360, direction): #quadrant 4 (-x, +y)
            a = direction - 270
            a = (a/180)*math.pi #convert to radians
            Fx = -(math.cos(a) * magnitude)
            Fy = math.sin(a) * magnitude
            
        elif direction == 0:
            Fx = 0
            Fy = magnitude
        elif direction == 90:
            Fx = magnitude
            Fy = 0
        elif direction == 180:
            Fx = 0
            Fy = -magnitude
        elif direction == 270: 
            Fx = -magnitude
            Fy = 0
        else:
            print(Fore.RED + "Direction Error" + Fore.RESET)
            
        x_forces.append(Fx)
        y_forces.append(Fy)
        
        #direction cannot be 360 as already adjusted in front
        
    #Sum of X & Y forces
    x_rf = 0
    y_rf = 0
    for force in x_forces:
        x_rf += force
        
    for force in y_forces:
        y_rf += force
        
    r_magnitude = math.sqrt((x_rf*x_rf)+(y_rf*y_rf)) #pythagoeras theorem
    
    if r_magnitude != 0:
        #finding the heading/direction via quadrant
        if x_rf > 0: #if resultant x force is positive
            if y_rf > 0: #quadrant 1
                r_direction = 90 - (math.atan(abs(y_rf)/abs(x_rf))/math.pi)*180   
            
            elif y_rf < 0: #quadrant 2
                r_direction = 90 + (math.atan(abs(y_rf)/abs(x_rf))/math.pi)*180
                
            else: #equals to zero
                r_direction = 90
        
        elif x_rf < 0:
            if y_rf > 0: #quadrant 4
                r_direction = (math.atan(abs(y_rf)/abs(x_rf))/math.pi)*180 + 270
            
            elif y_rf < 0: #quadrant 2
                r_direction = 270 - (math.atan(abs(y_rf)/abs(x_rf))/math.pi)*180
                
            else: #equals to zero
                r_direction = 270
            
        else: #x = 0
            if y_rf > 0: 
                r_direction = 0
                
            elif y_rf < 0:
                r_direction = 180
                
        return [r_magnitude, r_direction]
    
    else:
        return [0, 0]
        
# def addVectorList(vectors):
#     #Vector Calculation
#     n = 0
#     vector_storage = []
#     #first loop is seperate due to the possibility of odd number of vectors
    
#     print(Fore.LIGHTMAGENTA_EX + f"0th V_A Cycle: {vectors}" + Fore.RESET) 
#     while n < len(vectors):
#         current_v = vectors[n] 
#         try:
#             next_v = vectors[vectors.index(current_v) + 1]
#         except IndexError: #for odd number of vectors
#             print(Fore.RED + "[TTA] ODD!! Next Vector not Found" + Fore.RESET)
#             next_v = [0, 360]
        
#         r_vector = addVectorNew(current_v, next_v)
#         #print(f"[TTA] Resultant Vector: {r_vector}")
#         vector_storage.append(r_vector)
#         n += 2
    
#     final_vectors = list(vector_storage)
#     print(Fore.LIGHTMAGENTA_EX + f"1st V_A Cycle: {final_vectors}" + Fore.RESET) 
    
#     #final vector addition
#     while len(final_vectors) != 1:
#         temp_vectors = []
#         n = 0
        
#         #Goes through final_vectors once and stores n/2 vector list as temp_vectors
#         while n < len(final_vectors):
#             v_r = addVectorNew(final_vectors[n], final_vectors[n+1])
#             temp_vectors.append(v_r)
#             n += 2
            
#         final_vectors = list(temp_vectors) #change final_vectors at the end
#         print(Fore.LIGHTMAGENTA_EX + f"2nd V_A Cycle: {final_vectors}" + Fore.RESET)
    
#     #print(final_vectors)
#     return final_vectors[0]
        
def process(sentence):   
    theta = 360/len(listofcats) #Basic angle (Based on how many categories)
    dict_direction = {}
    
    a = 0
    for category in listofcats:
        dict_direction[a] = category
        a += theta

    sentence = sentence.lower()
    sentence = sentence.split()
    n_words = len(sentence)
    
    sentence_vectors = []
    dictionaries_data = []
    
    x = 0
    for dictionary in listofdicts:
        path = r"C:\Users\delay\OneDrive\Documents\Code & Programs\Visual Studio Code\Python\The CT Project\Modules\Text to Action\Data" + f"\{x}_data.pkl"
        with open(path, "rb") as dict_data:
            dictionaries_data.append(dict(pickle.load(dict_data)))
        x+=1
        
    for word in sentence: #word by word
        print(Fore.LIGHTCYAN_EX + f"[TTA] Calculating Vector for '{word}'" + Fore.RESET)
        angle = 0
        vectors = [] #should be storing all the vectors for each word
        
        for dictionary in dictionaries_data: #go through dictionary by dictionary
            if dictionary.get(word) != None: #if word is found
                magnitude = dictionary.get(word)
                direction = angle
                
            else: #if word is not found
                magnitude = 0
                direction = angle
            
            #print(Fore.YELLOW + f"Vector '{word}': M:{magnitude}, D{direction}" + Fore.RESET)
            vectors.append([magnitude, direction]) #[[Magnitude, Direction], [M1, D1]]
            angle = angle + theta #each dictionary has a different direction
            
        #Vector Calculation
        resultant_vector = addVectorListNew(vectors)
        if (round(resultant_vector[1]/theta) * 45) == 360:
            category = dict_direction.get(0)
        else:
            category = dict_direction.get(round(resultant_vector[1]/theta) * 45)
        print(Fore.GREEN + f"[TTA] Word: {word} | M:{resultant_vector[0]} D:{resultant_vector[1]} | Cat: {category}" + Fore.RESET + "\n")

        sentence_vectors.append(resultant_vector)
        
    #Filtration
    #print(Fore.LIGHTGREEN_EX + f"[TTA] Begin Filtration")
    temp_vectors = list(sentence_vectors)
    for vector in sentence_vectors:
        if vector[0] == 0:
            temp_vectors.pop(temp_vectors.index(vector))
            
    sentence_vectors = list(temp_vectors)

    #Vector Calculation for Sentence 
    print(Fore.LIGHTCYAN_EX + f"[TTA] Calculating Vector for '{sentence}'" + Fore.RESET)
    resultant_vector = addVectorListNew(sentence_vectors)
    resultant_vector = [resultant_vector[0]/n_words, resultant_vector[1]]
    
    print(Fore.GREEN + f"[TTA] Resultant Vector: {resultant_vector}" + Fore.RESET)

    #print(dict_direction)
    if (round(resultant_vector[1]/theta) * 45) == 360:
        category = dict_direction.get(0)
        
    else:
        category = dict_direction.get(round(resultant_vector[1]/theta) * 45)
    
    print(Fore.GREEN + f"[TTA] Category: {category}" + Fore.RESET)
    return category

# train()
# process("open my blinds")