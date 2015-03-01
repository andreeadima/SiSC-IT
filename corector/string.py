import sys

address1 = sys.argv[1]
address2 = sys.argv[2]


f = open(address1,'r')
text = f.read()
f.close()

length = len(text)    
rez = ''

for i in range(length-1): #fara spatii multiple succesive
    if text[i]==' ' and text[i+1]==' ':
        pass
    else:
        rez+=text[i]
text = rez + text[length-1]
rez = ''
length = len(text)

for i in range(length-1): #fara spatii inainte de . , ! ? ) ]
    if text[i]==' ' and (text[i+1]=='.' or text[i+1]=='!' or text[i+1]==',' or text[i+1]=='?' or text[i+1]==')' or text[i+1]==']'):
        pass
    else:
        rez+=text[i]
text = rez + text[length-1]
rez = text[0]
length = len(text)

for i in range(1,length): #fara spatii dupa ( [
    if text[i]==' ' and (text[i-1]=='(' or text[i-1]=='['):
        pass
    else:
        rez+=text[i]
text = rez
rez = text[0]
length = len(text)

for i in range(1,length): #un singur spatiu dupa . ! , ? ) ]
    if text[i]!=' ' and (text[i-1]=='.' or text[i-1]=='!' or text[i-1]==',' or text[i-1]=='?' or text[i-1]==')' or text[i-1]==']'):
        rez+=' '+ text[i]
    else:
        rez+=text[i]
text = rez
rez = ''
length = len(text)

for i in range(length-1): #un singur spatiu inainte ( [
    if text[i]!=' ' and (text[i+1]=='(' or text[i+1]=='[' ):
        rez+=text[i]+' '
    else:
        rez+=text[i]
text = rez + text[length-1]
length = len(text)

if text[0]==' ':
    rez=chr(9)
else:
    rez=text[0]
for i in range(1,length): #intendare cu tab
    if text[i]==' ' and ord(text[i-1])==10 :
        rez+=chr(9)
    else:
        rez+=text[i]
text = rez


g = open(address2,'w')
g.write(text)
g.close()
