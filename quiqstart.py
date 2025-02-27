#getting files of a folder has an offset in funciton get_items called offset
# have to try out sort by date in get_items!!! Shit works
import os.path
import boxsdk
from boxsdk import Client, OAuth2
import curses
from curses import wrapper

auth = OAuth2(access_token='RjSNGVyrgo9WsNUhB1erVIWym0Bz5gTl', client_id=None, client_secret=None)
client = Client(auth)

Updog = '155251522593'
def download():
    files = client.folder('155251522593').get_items(limit = 10)
    for file in files:
        ext = client.file(file.id).get()
        if(ext.name == 'cum.png'):
            with open(ext.name, 'wb') as f:
                client.file(ext.id).download_to(f)

def test():
    try:
        new_file = client.folder('155251522593').upload(input())
    except:
        print("File does not exist")
    files = client.folder(Updog).get_items(limit = 10)
    a = input('Enter file to download\n')
    for file in files:
        thing = client.file(file.id).get().name
        if(thing == a):
            print(thing) 

def test2():
    files = client.folder(Updog).get_items(limit = 10, sort = 'date')
    for file in files:
        print(client.file(file.id).get().name)

def test3():
    ##create a new folder object to get all info updates
    updog = client.folder(Updog).get()
    lastsize = updog.item_collection["total_count"]
    while(True):
        folder = client.folder(Updog).get()
        currentsize = folder.item_collection["total_count"]
        if(currentsize != lastsize):
            print("a")
            lastsize = currentsize

def test4():
    files = client.folder(Updog).get_items(limit = 10, sort = 'date')
    for file in files:
        pre, ext = client.file(file.id).get().name.split('.')
        if(ext == 'txt'):
            print(client.file(file.id).content().decode("utf-8"))
        else:
            with open('temp/' + (pre + '.' + ext), 'wb') as f:
                client.file(file.id).download_to(f)
                print('Check the file out at ' + f.name)

def test5():
    folder = client.folder(Updog).get()
    files = client.folder(Updog).get_items(offset = folder.item_collection["total_count"]-1, sort = 'date')
    mylist = []
    for file in files:
        mylist.append(file)
    print(mylist[0])

def main():
    test5()


if __name__ == '__main__':
    main()