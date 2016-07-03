import argparse
import urllib2
import socket
import json

API_LOCATION = 'http://192.241.178.181/'

# Check if connected to internet
def checkInternet():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection(('8.8.8.8', 53), 2)
        return True
    except:
        pass
    return False

# Function to pull from the leaderboard
def leaderboard():
    response = urllib2.urlopen(API_LOCATION + 'tempData/leaderboard.json')
    data = json.loads(response.read())
    data = data[:count]
    print('                         ' + 'NYCSL Leaderboard')
    print('___________________________________________________________________')
    print('| Place |        User        |       School       |     Score     |')
    print('|-------|--------------------|--------------------|---------------|')
    for i in data:
        print('| ' + str(i[u'rank']) + (' '*(6-len(str(i[u'rank'])))) + '| '
            + str(i[u'user'][u'name'])[:20] + (' '* (19-len(str(i[u'user'][u'name'])[:20]))) + '| '
            + str(i[u'user'][u'school'][u'name'])[:20] + (' '* (19-len(str(i[u'user'][u'school'][u'name'])[:20]))) + '| '
            + str(i[u'score']) + (' '* (14-len(str(i[u'score'])))) + '|'
        )

# Function to upload to the server
def upload():
    pass

# Function to manage user account locally
def user():
    pass

# All the argparsing stuff
parser = argparse.ArgumentParser(description='A command line interface for nycsl.io.')
parser.add_argument('filename', nargs='?', help='The filename of the of the file being uploaded/graded')
parser.add_argument('-l', '--leaderboard', dest='func', action='store_const', const=leaderboard, help='Show current leaderboard.')
parser.add_argument('-c', '--count', default=10, type=int, help='# of places to show in the leaderboard')
parser.add_argument('-u', '--upload', dest='func', action='store_const', const=upload, help='Upload the file to the nycsl.io server.')
parser.add_argument('--user', dest="func", action='store_const', const=user, help='Login or logout of your account locally.')
# parser.add_argument('-g', '--grade', dest='func', action='store_const', const=grade, help='Grade the file without uploading to the server.')
parser.add_argument('-v', '--version', action='version', version="0.1.0", help='Show version')

if __name__ == '__main__':
    args = parser.parse_args()
    if not checkInternet():
        parser.exit('No internet connection')
    count = args.count
    args.func()
