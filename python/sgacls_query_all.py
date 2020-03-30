from pxgrid import PxgridControl
from config import Config
import urllib.request
import base64
import time


def query(config, secret, url, payload):
    # print('query url=' + url)
    # print('  request=' + payload)
    handler = urllib.request.HTTPSHandler(context=config.ssl_context)
    opener = urllib.request.build_opener(handler)
    rest_request = urllib.request.Request(url=url, data=str.encode(payload))
    rest_request.add_header('Content-Type', 'application/json')
    rest_request.add_header('Accept', 'application/json')
    b64 = base64.b64encode((config.node_name + ':' + secret).encode()).decode()
    rest_request.add_header('Authorization', 'Basic ' + b64)
    rest_response = opener.open(rest_request)
    # print('  response status=' + str(rest_response.getcode()))
    # print('  response content=' + rest_response.read().decode())
    return rest_response.read().decode()


if __name__ == '__main__':
    config = Config()
    pxgrid = PxgridControl(config=config)

    while pxgrid.account_activate()['accountState'] != 'ENABLED':
        time.sleep(60)

    # lookup for session service
    service_lookup_response = pxgrid.service_lookup('com.cisco.ise.config.trustsec')
    service = service_lookup_response['services'][0]
    node_name = service['nodeName']
    url = service['properties']['restBaseUrl'] + '/getSecurityGroupAcls'


    url = url.replace('8910', str(config.port))
    
    secret = pxgrid.get_access_secret(node_name)['secret']

    resp = query(config, secret, url, '{}')
    print(resp)
