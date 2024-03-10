import requests

class Curtain:
    HOST = 'https://api.switch-bot.com'

    def __init__(self, id: str):
        self.id = id

    def status(self, header: dict):
        response = requests.get(f'{Curtain.HOST}/v1.1/devices/{self.id}/status', headers=header)
        
        return response

    def open(self, header: dict):
        """カーテンを開ける

        Args:
            header (dict): APIヘッダ

        Returns:
            _type_: _description_
        """        
        params = {
            'commandType': 'command',
            'command': 'turnOn',
            'command parameter': 'default',
        }
        response = requests.post(f'{Curtain.HOST}/v1.1/devices/{self.id}/commands', headers=header, json=params)

        return response

    def close(self, header: dict):
        """カーテンを閉める

        Args:
            header (dict): APIヘッダ

        Returns:
            _type_: _description_
        """
        params = {
            'commandType': 'command',
            'command': 'turnOff',
            'command parameter': 'default',
        }
        response = requests.post(f'{Curtain.HOST}/v1.1/devices/{self.id}/commands', headers=header, json=params)

        return response
