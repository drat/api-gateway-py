class Function:

    @classmethod
    def get(cls, cursor, tbl_ext, endpoint, func):
        
        query = " SELECT * FROM `{}func` WHERE published=1".format(tbl_ext)
        query+= " AND endpoint='{}' AND func_sn='{}';".format(endpoint, func)
        cursor.execute(query)
        return cursor.fetchone()