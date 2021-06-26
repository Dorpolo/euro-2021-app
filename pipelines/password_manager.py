from django.contrib.auth.models import User
from myproject.settings import *

def change_user_password(username: str, new_password: str):
    users = User.objects.filter(username='gilattar')
    user = users[0]
    user.set_password(new_password)
    try:
        user.save()
        print(f"Password has been changed to {new_password} successfully")
    except:
        print('Problem')
    return 'OK'


if __name__ == '__main__':
    configure()
    change_user_password('gilattar', 'G123456')