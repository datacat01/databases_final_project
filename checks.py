import re

def is_number(n):
    try:
        n1 = float(n)
        return n1
    except ValueError:
        return False


def is_phone_num(p): 
    Pattern = re.compile("38 0[5-9][0-9]{7}") 
    return bool(Pattern.match(p))



if __name__ == "__main__":
    print(is_phone_num('38 0994251454'))