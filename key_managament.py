from outline_vpn.outline_vpn import OutlineVPN


def init(api_url, cert_sha256 = None):
    global key_managament_client
    key_managament_client = OutlineVPN(api_url, cert_sha256)
    return key_managament_client


def get_all_keys():
    return key_managament_client.get_keys()


def get_key(name):
    for key in key_managament_client.get_keys():
        if key.name == name:
            return key
    return None


def new_key(name = None):
    return key_managament_client.create_key(name)


def rename_key(name, new_name):
    key_to_rename = get_key(name)
    if (key_to_rename):
        return key_managament_client.rename_key(key_to_rename.key_id, new_name)
    return None


def set_limit(name, limit):
    key_to_limit = get_key(name)
    if (key_to_limit):
        return key_managament_client.add_data_limit(key_to_limit.key_id, 1000 * 1000 * limit)
    return None


def remove_limit(name):
    key_to_remove_limit = get_key(name)
    if (key_to_remove_limit):
        return key_managament_client.delete_data_limit(key_to_remove_limit.key_id)
    return None


def remove_key(name):
    key_to_remove = get_key(name)
    if (key_to_remove):
        return key_managament_client.delete_key(key_to_remove.key_id)
    return False