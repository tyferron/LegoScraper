from commandInterface import *
from timer import *
import multiprocessing
        

if __name__ == "__main__": 
    p1 = multiprocessing.Process(target=userInput())
    p2 = multiprocessing.Process(target=startScheduledTimer)
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    print("done")
