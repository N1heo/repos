s = input()
ans = 0
costr = ""
anstr = ""
for i in range (len(s)):
    c = 1
    costr = s[i]
    for j in range (i+1 , len (s)):
        if ord(s[j]) >= ord (s[j-1]):
            c = c + 1
            costr = costr + s[j]
        else:
            break
    if c > ans:
        ans = c
        anstr = costr
print ("Longest substring in alphabetical order is:" , anstr)