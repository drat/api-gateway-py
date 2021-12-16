import json
import requests
import xmltodict
from urllib.parse import unquote

from collections import defaultdict
from app.models.services import Services
from app.models.config import Config
from app.models.function import Function
from app.models.argument import Argument
from app.models.headers import Headers
from app.models.auth import Auth
from app.models.response import Response
from app.response.functions import Functions


class Core:

    @classmethod
    def uagw(cls, cursor, version, service, endpoint, func_sn, payload, query):
        check       = False
        errors      = []
        response    = defaultdict()

        req_url     = {}
        req_payload = {}
        req_method  = "GET"
        req_timeout = 0
        req_headers = defaultdict()

        # get service info
        services = Services.get(cursor, version, service, endpoint)
        if services is not None:
            check      = True
            service    = services['service']
            endpoint   = services['endpoint']
            req_method = services['req_method']
            ep_type    = services['ep_type']

            # get endpoint function info
            func_info = Function.get(cursor, ep_type, endpoint, func_sn)
            if func_info is not None:
                check       = True
                func_id     = func_info['id']
                func_ep     = func_info['func_ep']
                has_headers = func_info['has_headers']
                has_args    = func_info['has_args']
                args_method = func_info['args_method']
                resp_sample = json.loads(func_info['resp_sample'])

                # get arguments
                if has_args == 1:
                    arguments = Argument.get(cursor, ep_type, func_id, args_method, func_ep, payload)
                    if "errors" not in arguments:
                        check   = True
                        func_ep = arguments['func_ep']
                        if arguments['args'] is not None:
                            req_payload = arguments['args']
                    else:
                        check = False
                        errors.append({"missingArgument": arguments['errors']})

                # get headers
                if has_headers == 1 and check == True:
                    header_info = Headers.get(cursor, ep_type, func_id)
                    if "errors" not in header_info:
                        check       = True
                        req_headers = header_info
                    else:
                        check = False
                        errors.append({"missingHeader": header_info['errors']})
            else:
                check = False
                errors.append({"missingFunction": "{}: No such Function.".format(func_sn)})

            # get endpoint configuration info
            if check == True:
                epconfig = Config.get(cursor, ep_type, endpoint, req_method)
                if epconfig is not None:
                    check         = True
                    req_endpoint  = "?"+func_ep if args_method=="GET" else func_ep
                    config_id     = epconfig['id']
                    req_url       = epconfig['baseurl'] + req_endpoint
                    need_auth     = epconfig['need_auth']
                    resp_datatype = epconfig['resp_datatype']
                    req_timeout   = epconfig['req_timeout_msec']

                    # get authentication info
                    if need_auth == 1:
                        epauth = Auth.get(cursor, ep_type, config_id, req_url)
                        if epauth is not None:
                            check   = True
                            req_url = epauth['baseurl']
                            if epauth['auth'] is not None:
                                req_headers['Authorization'] = epauth['auth']
                        else:
                            check = False
                            errors.append({"missingAuth": "Authorization is not set."})
                else:
                    check = False
                    errors.append({"missingConfig": "Configuration is not set."})
        else:
            check = False
            errors.append({
                "missingServiceOrModule": "{} or {}: No such Service/Module.".format(service,endpoint)
            })

        # Ready to request to API
        if check == True:
            request_info = {
                "url": unquote(req_url),
                "method": req_method,
                "timeout": req_timeout,
                "payload": req_payload,
                "headers": req_headers
            }
            print(request_info)

            apiResponse = requests.request(
                req_method,
                unquote(req_url),
                headers=req_headers,
                data=json.dumps(req_payload),
                timeout=req_timeout
            )

            # Parse API response
            json_parse  = getattr(cls, "parse_"+resp_datatype)(apiResponse.text)
            result_data = cls.getSpecificData(json_parse, resp_sample)
            if type(result_data).__name__ == 'list' and len(result_data) == 1:
                result_data = result_data[0]

            # Checking if there is any special function for data parsing
            if hasattr(Functions, func_sn):
                result_data = getattr(Functions, func_sn)(cursor, ep_type, result_data)

            # Getting data to exchange the response-result index
            params = Response.get(cursor, ep_type, func_id)
            if len(params) > 0:
                result_data = cls.exchangeMultiDictIndex(result_data, params)

            response['success'] = result_data
        else:
            response['error'] = errors

        return response


    # Data is being taken from a specific index
    @classmethod
    def getSpecificData(cls, data, resp_sample):
        for key,row in resp_sample.items():
            if type(row).__name__ == 'list':
                return data[key] if key in data else {}
            else:
                return cls.getSpecificData(data[key], row)

    @classmethod
    def exchangeMultiDictIndex(cls, data, params):
        reversed_data = []
        data_type = type(data).__name__

        if data_type == 'dict' or data_type == 'OrderedDict':
            reversed_data = cls.exchangeSingleDictIndex(data, params)
        elif data_type == 'list':
            for data_row in data:
                reversed_data.append(cls.exchangeSingleDictIndex(data_row, params))
        else:
            reversed_data = data
        return reversed_data

    @classmethod
    def exchangeSingleDictIndex(cls, data, params):
        reverse_index = defaultdict()
        for key,row in params.items():
            index = row['index']
            ktype = row['type']
            if key in data:
                reverse_index[index] = getattr(cls, "parse_"+ktype)(data[key])
        return reverse_index


    @classmethod
    def parse_json(cls, data):
        return json.loads(data)

    @classmethod
    def parse_xml(cls, data):
        return xmltodict.parse(data)

    @classmethod
    def parse_integer(cls, data):
        return int(data)

    @classmethod
    def parse_float(cls, data):
        return float(data)

    @classmethod
    def parse_bool(cls, data):
        return bool(data)

    @classmethod
    def parse_string(cls, data):
        return str(data)