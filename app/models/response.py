from collections import defaultdict

class Response:

    @classmethod
    def get(cls, cursor, tbl_pre, fid):
        
        query = "SELECT * FROM `{}func_resp` WHERE".format(tbl_pre)
        query = "{} published=1 AND func_id='{}';".format(query,fid)
        cursor.execute(query)
        result = cursor.fetchall()
        
        params = defaultdict()
        if result is not None:
            for row in result:
                params[row['resp_key']] = {"index":row['resp_val'], "type":row['val_type']}
        return params
