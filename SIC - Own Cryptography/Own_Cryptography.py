alph = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'

key = int(input("Enter a number between 1 to 9:"))
message = input("Enter message:")
len_of_msg = len(message)

def get_value(x):
    lst = []
    for i in range(len(x)):
        if x[i]=='#':
            lst.append('#')
        else:
            lst.append(alph.split().index(x[i]))
    return lst

def get_alph(lst):
    lst1 = []
    for i in range(len(lst)):
        if lst[i]=='#':
            lst1.append('#')
        else:
            lst1.append(alph.split()[lst[i]])
    return lst1

def create_mat(lst):
    mat = []
    if((len(lst)%4)!=0):
        for i in range(4-(len(lst)%4)):
            lst.append("#")
    for i in range(4):
        row = []
        for j in range(i,len(lst),4):
            row.append(lst[j])
        mat.append(row)
    return mat

#Encryption
ip_msg = " ".join(message)
mat = create_mat(ip_msg.split())
print(mat)
temp_mat1 = []
for i in range(len(mat)):
    temp_mat1.append(get_value(mat[i]))

print(temp_mat1)
#print(get_value(mat[0]))
temp_mat2=[]
for i in range(len(temp_mat1)):
    lst_temp=[]
    for x in temp_mat1[i]:
        if x=='#':
            lst_temp.append('#')
        else:
            lst_temp.append((x+len_of_msg+key)%26)
    temp_mat2.append(get_alph(lst_temp))
print(temp_mat2)

encrypted_msq=''
for i in range(len(temp_mat2)):
    for x in temp_mat2[i]:
        encrypted_msq = encrypted_msq+x
print("Encrypted Message : ",encrypted_msq)

#print(get_alph([(num+len_of_msg+key)%26 for num in get_value(mat[0])]))

xxx = get_alph([(num+len_of_msg+key)%26 for num in get_value(mat[0])])

#Decryption
#print("Decryption")
#print([(val-len_of_msg-key)%26 for val in get_value(xxx)])

temp_mat3=[]
for i in range(len(temp_mat2)):
    temp_lst=[]
    for x in get_value(temp_mat2[i]):
        if x=='#':
            temp_lst.append('#')
        else:
            temp_lst.append((x-len_of_msg-key)%26)
    temp_mat3.append(temp_lst)

#print(temp_mat3)

decrypted_msg=''
dec_lst=[]
for i in range(len(temp_mat3[0])):
    for j in range(len(temp_mat3)):
        dec_lst.append(temp_mat3[j][i])

#print(dec_lst)
#print(get_alph(dec_lst))
decrypted_msg = ''.join(get_alph(dec_lst)).replace('#','')

print("Decrypted Message : ",decrypted_msg)