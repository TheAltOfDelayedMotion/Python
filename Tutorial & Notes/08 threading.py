import threading as th

def printing(string):
    print(f"Printing this string: {string}")
    
#Defining a thread
#th.Thread(target=function, args=(<function arguments>,)) YOU MUST PUT A COMMA (idk why)
thread1 = th.Thread(target=printing, args=("String to print",)) 
thread1.start()

#Threading Timers
print("Threading Timer Started")
thread2 = th.Timer(2, printing, args=("Threading Timer Ended!",)) #Again, you must put a comma. 
thread2.start()

