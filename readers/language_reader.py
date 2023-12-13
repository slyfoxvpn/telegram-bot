import configparser

class LanguageManager:
    def __init__(self, file_path):
        self.config = configparser.ConfigParser()
        self.config.read(file_path)


    def get_section_keys(self, section='default'):
        return dict(self.config.items(section))
    

lang_manager = LanguageManager('langs/ru_ru.lang')
lang = lang_manager.get_section_keys()