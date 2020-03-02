web: gunicorn run:APP

def __init__(self, email=None, phoneNumber=None, is_admin=True,
                 username=None, password=None, active=None):
        self.id = UserModel.id
        self.email = email
        self.password = self.generate_pass_hash()
        self.phoneNumber = phoneNumber
        self.username = username
        self.active = active
        self.is_admin = is_admin
        self.created_on = datetime.datetime.now()
        self.db = USERS