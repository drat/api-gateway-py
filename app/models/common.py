
class Common:

    @classmethod
    def uuid(cls, connect, cursor, start:str, id_for:str, gender:int=-1):
        start = start.upper()
        id_for = id_for.upper()
        gs = ["M", "F"]

        g = gs[gender] if gender != -1 else "X"
        f4chr = "{}{}{}".format(start, id_for, g)

        query = "SELECT max(uuid) as uuid FROM ncs_uuid WHERE uuid LIKE '{}%'".format(f4chr)
        cursor.execute(query)
        result = cursor.fetchone()

        temp_id = uuid = ""
        if result['uuid'] is not None:
            temp_id = result['uuid'][-6:]
        else:
            uuid = "{}AAA000".format(f4chr)

        if temp_id != "":
            f3 = temp_id[0:3]
            l3 = int(temp_id[-3:])
            l3 = l3 + 1

            if(l3 >= 999):
                l3 = "0"

                c1 = f3[0:1]
                c2 = f3[1:2]
                c3 = f3[2:3]

                c1 = ord(c1) + 1
                incre = (c1 - 65) / 26
                c1 = int(65 + (c1 - 65) % 26)

                c2 = ord(c2) + incre
                incre = (c2 - 65) / 26
                c2 = int(65 + (c2 - 65) % 26)

                c3 = ord(c3) + incre
                incre = (c3 - 65) / 26
                c3 = int(65 + (c3 - 65) % 26)

                f3 = chr(c3) + chr(c2) + chr(c1)

            l3 = str(l3).zfill(3)
            uuid = "{}{}{}".format(f4chr, f3, l3)

        try:
            query = "INSERT INTO ncs_uuid(uuid) VALUES ('{}')".format(uuid)
            cursor.execute(query)
            connect.commit()
        except:
            uuid = ""

        return uuid