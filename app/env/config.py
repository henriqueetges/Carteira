import yaml
import os

def env_construct(loader, node):
    env_var = loader.construct_scalar(node)
    value = os.getenv(env_var)
    if value is None:
        return ValueError(f"Variável {env_var} não encontrada no ambiente")
    return value

yaml.add_constructor('!ENV', env_construct, Loader=yaml.SafeLoader)

class Config:
    def __init__(self, env):
        self.env = env
        self.config = self.load_config()  
        self.DB_USER = self.get_var('database_user')
        self.DB_PW = self.get_var('database_pw')
        self.DB_HOST = self.get_var('database_host')
        self.DB_PORT = self.get_var('database_port')
        self.BRAPI_KEY = self.get_var('brapi_key')
    
    def load_config(self):
        with open('app\env\env.yaml','r') as f:
            config_data = yaml.load(f, Loader=yaml.SafeLoader)
        return config_data['environments'].get(self.env)
    
    def get_var(self, key, default=None):
        return self.config.get(key, default)
    

configs = Config('production')
