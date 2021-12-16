class Config:

    @classmethod
    def get(cls, cursor, tbl_ext, endpoint, method):
        
        query = " SELECT * FROM `{}config` WHERE published=1 AND".format(tbl_ext)
        query+= " endpoint='{}' AND req_method='{}';".format(endpoint, method)
        cursor.execute(query)
        return cursor.fetchone()