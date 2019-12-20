import re

def is_number(n):
    try:
        n1 = float(n)
        return n1
    except ValueError:
        return False


if __name__ == "__main__":
    print(is_phone_num('38 0994251454'))