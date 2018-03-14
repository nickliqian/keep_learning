class Foo(object):
    def __init__(self):
        print("init")
    def __enter__(self):
        print("enter")    
    def __exit__(self):
        print("exit")

with Foo():
    pass

