import os
import threading
print(__name__)
print(os.path.abspath(__name__))
print(__file__)
print(os.path.abspath(__file__))


print(threading.enumerate())
print(threading.activeCount())
print(threading.get_ident())
