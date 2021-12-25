line_above = "\n###################################################################################################\n"
line_bottom = "\n###################################################################################################\n\n"

def check_with_yn(conv: str) -> bool:
    print(line_above)
    while True:
        i = input(conv)
        print(line_bottom)
        if i == 'y':
            return True
        elif i == 'n':
            return False 
    
def check_with_quit(conv: str):
    print(line_above)
    i = input(conv)
    print(line_bottom)
    if i == 'quit':
        quit()
    return 


def check_with_enter(conv: str, confirm: str):
    print(line_above)
    print(conv)
    input(confirm)
    print(line_bottom)


def say_something(conv: str):
    print(line_above)
    print(conv)
    print(line_bottom)