import bcrypt


def get_hashed_pass(plain_pass):
    plain_pass = plain_pass.encode("utf-8")
    hash_salt = bcrypt.gensalt(rounds=12)
    pwd = bcrypt.hashpw(plain_pass, salt=hash_salt)
    return pwd

def verify_pass(plain_pass, hashed_pass):
    plain_pass = plain_pass.encode("utf-8")
    hashed_pass = hashed_pass.encode("utf-8")
    return bcrypt.checkpw(plain_pass,hashed_pass)