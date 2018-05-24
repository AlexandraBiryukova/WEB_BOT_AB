file = open("users/393598388.txt","r")
s=file.read()
file.close()
s=s.split('\n')
res=[]
for i in range(len(s)):
	if(s[i]!=''):
		res.append(s[i])
res='\n'.join(res)
file = open("users/393598388.txt","w")
file.write(res)
file.close()
print(res)	