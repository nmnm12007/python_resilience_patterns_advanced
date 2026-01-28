def reverse_words(s:str) -> list:
    list_1 = s.split()
    list_new = []
    l = len(list_1)

    for i in range(l, 0, -1):
        j = i
        
        list_new.append(list_1[j-1])
    return list_new

    
if __name__ == '__main__':
    reverse_words("hello world from python 5 5 ")
    