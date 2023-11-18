import key_managament as keys

keys.init("https://193.176.179.177:30977/0Z6cpOQ4EV4hixKJfT_jWQ") # Init
keys.get_all_keys() # Get all keys
keys.new_key("Example1") # Create new key
keys.get_key("Example1") # Get information about key
keys.rename_key("Example1", "NewExampleName") # Rename from Example1 to NewExampleName
keys.set_limit("NewExampleName", 2048) # Set limit to 2GB
keys.remove_limit("NewExampleName")
keys.remove_key("NewExampleName")