def parse_temperature(message, url_fragment):
    new_msg = {
        'sensor': url_fragment + str(message['id']) + '/',
        'temperature': message['measurement']['temperature']
    }
    return new_msg


def parse_ambient(message, url_fragment):
    new_msg = {
        'sensor': url_fragment + message['sensor'],
        'humidity': message['measurement']['humidity'],
        'air_quality': message['measurement']['air_quality'],
        'temperature': message['measurement']['temperature'],

    }
    return new_msg


def parse_power(message, url_fragment):
    new_msg = {
        'sensor': url_fragment + message['sensor'],
        'power': message['measurement']['power']
    }
    return new_msg
