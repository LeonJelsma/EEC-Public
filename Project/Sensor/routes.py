import ujson
from state import State
import util
from routing import Router, Route
import network
import sensor

from state import State

router = Router()


@Route(endpoint='/setup', methods=['GET'])
def get_setup_page(request):
    response = open('static\\setup.html', 'r').read()
    return response


@Route(endpoint='/sensor', methods=['GET'])
def get_sensor_page(request):
    response = open('static\\sensor.html', 'r').read()
    return response


@Route(endpoint='/', methods=['GET'])
def get_index(request):
    response = open('static\\index.html', 'r').read()
    return response


@Route(endpoint='/api/accesspoints', methods=['GET'])
def get_access_points(request):
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    networks = nic.scan()
    nic.active(False)
    response = []
    for net in networks:
        response.append(net[0].decode("utf-8"))
    return ujson.dumps(response)


@Route(endpoint='/api/measurement', methods=['GET'])
def get_measurement(request):
    return ujson.dumps(router.sensor.get_measurement())


@Route(endpoint='/favicon.ico', methods=['GET'])
def get_favicon(request):
    return ujson.dumps('')


@Route(endpoint='/api/setup', methods=['POST'])
def post_setup(request):
    lines = request.raw_data.splitlines()
    parameters = ujson.loads(lines[len(lines) - 1])
    print(parameters)
    util.connect_to_network(parameters['SSiD'], parameters['password'])
    state = State()
    state.save_value('SSiD', parameters['SSiD'])
    state.save_value('password', parameters['password'])
    state.save_state()
    if util.wifi_is_connected():
        print('Connected succesfully.')


router.add_route(get_sensor_page)
router.add_route(get_index)
router.add_route(get_setup_page)
router.add_route(get_access_points)
router.add_route(get_favicon)
router.add_route(post_setup)
router.add_route(get_measurement)
