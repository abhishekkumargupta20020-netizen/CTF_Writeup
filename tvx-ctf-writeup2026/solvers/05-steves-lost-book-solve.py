import base64
s=open('/home/hatch/workspace/user/files/Steves_Lost_Book.txt').read().strip()
print('input:', s)
print('base64:', base64.b64decode(s))
