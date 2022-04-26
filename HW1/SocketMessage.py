import json
import re

class SocketMessage:
    @classmethod
    def from_text(cls, text):
        obj = cls()
        try:
            data = json.loads(text)
            obj.type = data['type']
            obj.message = data['message']
            obj.data = data['data']
            obj.is_valid = True
        except:
            obj.is_valid = False
        return obj

    @classmethod
    def from_message(cls, type, message):
        obj = cls()
        obj.type = type
        obj.message = message
        obj.data = ''
        obj.is_valid = True
        return obj

    @classmethod
    def from_data(cls, command, data):
        obj = cls()
        obj.type = "Command"
        obj.data = data
        obj.message = command
        obj.is_valid = True
        return obj

    def is_error(self):
        return self.type == 'Error'

    def is_command(self):
        return self.type == 'Command'
    
    def stringify(self):
        data_dict = {
            "type": self.type,
            "data": self.data,
            "message": self.message
        }
        return json.dumps(data_dict).encode('ascii')
