from collections import defaultdict
from app.methods.tools import Tools
import urllib

class Auth:

    @classmethod
    def get(cls, cursor, tbl_ext, cid, baseurl):
        
        query = "SELECT * FROM `{}auth` WHERE published=1".format(tbl_ext)
        query = "{} AND config_id='{}'".format(query, cid)
        cursor.execute(query)
        result = cursor.fetchall()

        get_auth  = None
        auth_func = None
        if result is not None:
            auth_data = defaultdict()
            for row in result:
                if row['auth_key'] == 'auth_type':
                    auth_func = row['auth_value']
                else:
                    auth_data[row['auth_key']] = row['auth_value']
            get_auth = getattr(cls, auth_func)(auth_data, baseurl)
        return get_auth

    @classmethod
    def http_auth_basic(cls, data, baseurl):
        string = "{}:{}".format(data['auth_user'], data['auth_pass'])
        return {"baseurl": baseurl, "auth": "Basic " + Tools.b64Encode(string)}

    @classmethod
    def http_auth_get(cls, data, baseurl):
        baseurl = "{}&{}".format(baseurl, urllib.parse.urlencode(data))
        return {"baseurl": baseurl, "auth": None}