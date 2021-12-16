import json
import urllib
from collections import defaultdict

class Argument:

    @classmethod
    def get(cls, cursor, tbl_ext, fid, args_method, func_ep, payload):

        query = "SELECT * FROM `{}func_arg` WHERE".format(tbl_ext)
        query = "{} published=1 AND func_id='{}'".format(query, fid)
        cursor.execute(query)
        result = cursor.fetchall()

        errors = []
        arguments = defaultdict()
        if result is not None:
            for row in result:
                arg_key      = row['arg_key']
                arg_type     = row['arg_type']
                req_arg_key  = row['req_arg_key']
                req_arg_type = row['req_arg_type']
                is_required  = row['is_required']

                if arg_key not in payload and is_required == 1:
                    errors.append({"missingValue": "Field or value is missing for {}.".format(arg_key)})
                elif arg_key in payload:
                    payload_val  = payload[arg_key]
                    payload_type = type(payload_val).__name__
                    if arg_type == payload_type:
                        get_arg = getattr(cls, "type_"+req_arg_type)(payload_val, is_required)
                        if get_arg is not None:
                            arguments[req_arg_key] = get_arg
                        else:
                            errors.append({"missingValue": "Field or value is missing for {}.".format(arg_key)})
                    else:
                        errors.append({"missingType": "Invalid data type for {}.".format(arg_key)})
            if len(errors) < 1:
                arguments = getattr(cls, "ep_"+args_method)(func_ep, arguments)
        else:
            errors.append({"internalError": "Error in Argument"})
        if len(errors) > 0:
            arguments['errors'] = errors
            
        return arguments


    @classmethod
    def type_comma(cls, data, required):
        return None if required==1 and len(data)<1 else ",".join(data)

    @classmethod
    def type_list(cls, data, required):
        return None if required==1 and len(data)<1 else data
    
    @classmethod
    def type_dict(cls, data, required):
        return None if required==1 and len(data)<1 else json.loads(data)

    @classmethod
    def type_integer(cls, data, required):
        return None if required==1 and len(data)<1 else int(data)

    @classmethod
    def type_float(cls, data, required):
        return None if required==1 and len(data)<1 else float(data)

    @classmethod
    def type_bool(cls, data, required):
        return None if required==1 and len(data)<1 else bool(data)

    @classmethod
    def type_str(cls, data, required):
        return None if required==1 and len(data)<1 else str(data)

    @classmethod
    def ep_POST(cls, func_ep, args):
        if func_ep.find("=") > 0:
            new_arg = func_ep.split("=")
            args.update({new_arg[0]: new_arg[1]})
            func_ep = ""
        return {"func_ep": func_ep, "args": args}

    @classmethod
    def ep_GET(cls, func_ep, args):
        ep = "{}&{}".format(func_ep, urllib.parse.urlencode(args))
        return {"func_ep": ep, "args": None}