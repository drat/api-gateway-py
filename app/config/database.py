import mysql.connector

class Database:
    mysql_host = "52.76.4.19"
    mysql_user = "root"
    mysql_pass = ""
    mysql_port = 3306
    mysql_db   = "uniapigw"

    # Remotely Mysql database connector
    @classmethod
    def mysql(cls):
        return mysql.connector.connect(
            database           = cls.mysql_db,
            user               = cls.mysql_user,
            password           = cls.mysql_pass,
            host               = cls.mysql_host,
            port               = cls.mysql_port,
            get_warnings       = True,
            raise_on_warnings  = True,
            connection_timeout = 7200
        )

    @classmethod
    def mysql_error(cls):
        return cls.mysql.connector.Error