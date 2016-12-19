

def getUsername():
    with open('tech-company-founders-list.txt', 'r') as mydatafile:
        data = mydatafile.readlines()
    return data

def write_to_file(username):
    with open("tech-company-founders-list-new_updated.txt", 'a') as f:
        f.write(username + "\n")

user_list = getUsername()
print("user list : " + str(len(user_list)))
flag = 0
for user in user_list:
    print(user)

    if (flag == 1):
        write_to_file(user.strip('\n'))

    if(user == "brattray\n"):
        flag = 1







