import OutlineVPN_Key_Managament as keys
import urllib3
from config_reader import config

urllib3.disable_warnings() # But maybe it is need to fix

# keys.init(config.outline_api.get_secret_value()) # Init
# keys.get_all_keys() # Get all keys
# keys.new_key("Example1") # Create new key
# keys.get_key("Example1") # Get information about key
# keys.rename_key("Example1", "NewExampleName") # Rename from Example1 to NewExampleName
# keys.set_limit("NewExampleName", 2048) # Set limit to 2GB
# keys.remove_limit("NewExampleName")
# keys.remove_key("NewExampleName")

# print(keys.get_all_keys())


