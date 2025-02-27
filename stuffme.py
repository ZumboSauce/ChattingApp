
from boxsdk import Client, OAuth2
auth = OAuth2(access_token='MvTwzjOFoNeaADVm4NC7wx32rBk6DDYp', client_id=None, client_secret=None)
client = Client(auth)
from io import StringIO, BytesIO
import json
##only show content of file if its beginning is not the name of the user ex: Nick can not see nick_a.txt
def NewMessage(folderLen, foldernum = 155251522593):
    folder1 = client.folder(foldernum).get()
    folderLenN = folder1.item_collection["total_count"]
    if(folderLenN != folderLen):
        print('a')
        return True
    else:
        return False
def Incoming(folderLen, foldernum = '155251522593'):
        fileN = client.folder(foldernum).get_items(offset = folderLen-1, sort = 'date')
        for file in fileN:
            filename = client.file(file.id).get().name
            if '.txt' in filename:
                content = file.content().decode('utf-8')
                return ('txt', content)
            elif '.txt' not in filename:
                content = BytesIO()
                file.download_to(content)
                return ('image', content)       
            else:
                None
def firstMessages(folderlen, foldernum = '155251522593'):
    if client.folder(foldernum).get().item_collection['total_count'] == 0:
        client.folder(foldernum).upload_stream(StringIO('Welcome'), file_name = 'systemWelcome.txt')
    fileN = client.folder(foldernum).get_items(offset = (folderlen-20) if folderlen >= 20 else 0 ,sort = 'date')
    i = 0
    messages = []
    for file in fileN:
        i+=1
        print(i)
        filename = client.file(file.id).get().name
        
        if '.txt' in filename:
            content = file.content().decode('utf-8')
            messages.append(('txt', content))
        elif '.txt' not in filename:
            content = BytesIO()
            file.download_to(content)
            messages.append(('image', content))
        else:
            None
    return messages
                
def folderLen(foldernum = '155251522593'):
    folder = client.folder(foldernum).get()
    return folder.item_collection["total_count"]

def send(UserInput, username, ext, foldernum = '155251522593'):
    if ext != '.txt': client.folder(foldernum).upload_stream(UserInput, file_name = (username + ext))
    else: client.folder(foldernum).upload_stream(StringIO(UserInput), file_name = (username + '.txt'))

def createfolder(chatName, username):
    root = 0
    newChat = client.folder(root).create_subfolder(chatName)
    users = client.folder(158852098839).get_items()
    info = None
    for user in users:
        if user.name == username + '.json':
            a = user.content().decode('utf-8')
            info = json.loads(a)
            info[chatName] = newChat.id
            user.delete()
            a = StringIO(json.dumps(info, indent=4))
            client.folder(158852098839).upload_stream(a, file_name = username + '.json')
            break
    return info

def joinchat(foldernum, username):
    users = client.folder(158852098839).get_items()
    for user in users:
        if user.name == username + '.json':
            a = user.content().decode('utf-8')
            info = json.loads(a)
            info[client.folder(folder_id=foldernum).get().name] = foldernum
            client.file(user.id).update_contents(info)
    return info



def signin(username):
    users = client.folder(158852098839).get_items()
    userEx = False
    info = None
    for user in users:
        if user.name == username + '.json':
            a = user.content().decode('utf-8')
            info = json.loads(a)
            print(info)
            return info
    info = dict([('Test', 155251522593)])
    a = StringIO(json.dumps(info, indent=4))
    client.folder(158852098839).upload_stream(a, file_name = username + '.json')
    return info