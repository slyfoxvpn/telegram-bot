import libs.Outline_Key_Manager as okm
import urllib3
from config_reader import config

urllib3.disable_warnings() # It is need to fix?

okm.init(config.outline_api.get_secret_value(), debug=True) # Init
okm.get_all_keys() # Get all keys
okm.new_key(name="Example1") # Create new key
okm.get_key("Example1") # Get information about key
okm.rename_key("Example1", "NewExampleName") # Rename from Example1 to NewExampleName
okm.set_limit("NewExampleName", 2048) # Set limit to 2GB
okm.remove_limit("NewExampleName") # Remove limit
okm.remove_key("NewExampleName") # Remove key