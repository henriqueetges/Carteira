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
    
    def load_config(self):
        with open('app\env\env.yaml','r') as f:
            config_data = yaml.load(f, Loader=yaml.SafeLoader)
        return config_data['environments'].get(self.env)
    
    def get_var(self, key, default=None):
        return self.config.get(key, default)
    
