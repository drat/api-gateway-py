from collections import defaultdict

class Headers:

    @classmethod
    def get(cls, cursor, tbl_ext, fid):
        
        query = "SELECT header_key,header_value FROM `{}func_header`".format(tbl_ext)
        query = "{} WHERE published=1 AND func_id='{}'".format(query, fid)
        cursor.execute(query)
        result = cursor.fetchall()

        headers = defaultdict()
        if result is not None:
            for row in result:
                headers[row['header_key']] = row['header_value']
        else:
            headers['errors'] = "Header is missing."
        return headers
