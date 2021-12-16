class Services:

    @classmethod
    def get(cls, cursor, version, service, endpoint):
        
        query = " SELECT * FROM services WHERE published=1 AND version='{}'".format(version)
        query+= " AND service='{}' AND endpoint='{}';".format(service, endpoint)
        cursor.execute(query)
        return cursor.fetchone()