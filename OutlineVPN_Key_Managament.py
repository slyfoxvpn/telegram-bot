from outline_vpn.outline_vpn import OutlineVPN

def my_decorator(func):
    def wrapper():
        print("Что-то происходит перед вызовом функции")
        func()
        print("Что-то происходит после вызова функции")
    return wrapper

def init(api_url, cert_sha256 = None):
    global client
    client = OutlineVPN(api_url, cert_sha256)
    return client

def init_check():
    if not 'asfasf' in locals():
        return 43


def get_all_keys():
    if 'client' in globals():
        return client.get_keys()
    else:
        return 43

def get_key(key_to_find):
    if 'client' in globals():
        for key in client.get_keys():
            if key.name == key_to_find:
                return key
            else:
                return 44
    else:
        return 43

# ----------------------------

# def get_all_keys():
#     return client.get_keys()


def get_key(name):
    for key in client.get_keys():
        if key.name == name:
            return key
    return 44


def new_key(name = None):
    if (client.create_key(name)):
        return 0
    else: # Key is exist error??
        return -1 


def rename_key(name, new_name):
    try:
        if (client.rename_key(get_key(name).key_id, new_name)):
            return 0
        else:
            return -1
    except AttributeError:
        return 44

def set_limit(name, limit):
    try:
        if (client.add_data_limit(get_key(name).key_id, 1000 * 1000 * limit)):
            return 0
        else:
            return -1
    except AttributeError:
        return 44

def remove_limit(name):
    try:
        if (client.delete_data_limit(get_key(name).key_id)):
            return 0
        else:
            return -1
    except AttributeError:
        return 44


def remove_key(name):
    try:
        if (client.delete_key(get_key(name).key_id)):
            return 0
        else:
            return -1
    except AttributeError:
        return 44