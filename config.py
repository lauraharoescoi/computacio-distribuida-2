import configparser

class Configuration:
    CONFIG = None

    @staticmethod
    def set_up():
        if Configuration.CONFIG is None:
            Configuration.CONFIG = configparser.ConfigParser()
            Configuration.CONFIG.read('config.ini')

    @staticmethod
    def get(section, key):
        Configuration.set_up()
        return Configuration.CONFIG[section][key]