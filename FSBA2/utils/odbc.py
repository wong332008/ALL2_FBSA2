from .__import import *
from .searching import *

def columnDesc(description):
    return [(l[0], *typeStr_and_justify(l[1]), l[3], l[6]) for l in description]

def typeStr_and_justify(code):
    """
    DECIMAL = 0
    TINY = 1
    SHORT = 2
    LONG = 3
    FLOAT = 4
    DOUBLE = 5
    NULL = 6
    TIMESTAMP = 7
    LONGLONG = 8
    INT24 = 9
    DATE = 10
    TIME = 11
    DATETIME = 12
    YEAR = 13
    NEWDATE = 14
    VARCHAR = 15
    BIT = 16
    JSON = 245
    NEWDECIMAL = 246
    ENUM = 247
    SET = 248
    TINY_BLOB = 249
    MEDIUM_BLOB = 250
    LONG_BLOB = 251
    BLOB = 252
    VAR_STRING = 253
    STRING = 254
    GEOMETRY = 255

    CHAR = TINY
    INTERVAL = ENUM
    """
    # integral
    if binarysearch([0, 1, 2, 3, 8, 9, 16], code):
        return ("d", False)
    # floating point
    if code <= 5:
        return ("f", False)
    # NULL
    if code == 6:
        return ("r", False)
    # string
    return ("s", True)


# Connect to the database
def __connectDB(host, user, pw, db, charset="utf8mb4", *argv, **kwargs):
    debug(argv)
    debug(kwargs)
    return pymysql.connect(host=host,
                           user=user, 
                           password=pw,
                           db=db,
                           charset=charset,
                           cursorclass=pymysql.cursors.DictCursor)

def connectDB():
    return __connectDB(host="localhost",
                       user="all_proj",
                       pw="all_proj",
                       db="all_proj")

# connection = connectDB()
# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `customers` (givenName, surname) VALUE (%s, %s)"
#         cursor.execute(sql, ("leo", "sin"))
# 
#     connection.commit()
# 
#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT * FROM customers"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         desc = cursor.description
#         "(name, type_code, display_size, internal_size, precision, scale, null_ok)"
#         print(columnDesc(desc))
#         columnDesc(desc)
#         format_str_lst = ["%" + str(x[2]) + x[1] for x in columnDesc(desc)]
#         format_str = " | ".join(format_str_lst)
# 
#         print(format_str % tuple(l[0] for l in desc))
#         format_str = "   ".join(format_str_lst)
#         for row in result:
#             print(format_str % tuple(row.values()))
# 
# finally:
#     connection.close()

def query(table, columns="", condition="", join=""):
    con = connectDB()
    try:
        with con.cursor() as c:
            sql = "SELECT %s FROM %s" % ("*" if columns == "" else columns, table) \
                    + ("" if condition == "" else (" WHERE " + condition))\
                    + ("" if join == "" else (" INNER JOIN " + join))
            debug(sql)
            c.execute(sql)
            result = c.fetchall()
            cols = [l[0] for l in c.description]
            return (columnDesc(c.description), cols, [[row[col] for col in cols] for row in result])
    finally:
        con.close()

def insert(table, columns=[], values=[]):
    con = connectDB()
    cols = "" if columns == [] else "(" + ", ".join(columns) + ") "
    debug(cols)
    if values == []:
        error("values == []")

    vals = "VALUES (" + ", ".join(values) + ")"
    debug(vals)

    if len(columns) > 0 and len(columns) != len(values):
        error("len(columns) > 0 BUT len(columns) != len(values)")

    try:
        with con.cursor() as c:
            sql = "INSERT INTO %s %s%s" % (table, cols, vals)
            debug(sql)
            c.execute(sql)
            con.commit()
            ret = c.lastrowid
            debug("c.lastrowid:", ret)
            return ret
    finally:
        con.close()

def update(table, column_and_values=[], condition=""):
    con = connectDB()
    if column_and_values == []:
        error("column_and_values == []")
    debug(column_and_values)
    col_and_val_lst = ["%s = %s" for (col, val) in column_and_values]
    debug(col_and_val_lst)
    col_and_val_SQL = ", ".join(col_and_val_lst)
    debug(col_and_val_SQL)

    try:
        with con.cursor() as c:
            sql = "UPDATE %s SET %s %s" % (table, col_and_val_SQL, "" if condition == "" else "WHERE " + condition)
            debug(sql)
            c.execute(sql)
            con.commit()
            rc = c.rowcount
            debug("row affected: %d" % rc)
            return rc
    finally:
        con.close()

def delete(table, condition=""):
    if condition == "":
        warning("deleting all in %s, condition = \"\"" % table)
    con = connectDB()
    try:
        with con.cursor() as c:
            sql = "DELETE FROM %s%s" % (table, "" if condition == "" else "WHERE %s" % condition)
            debug(sql)
            c.execute(sql)
            con.commit()
            rc = c.rowcount
            debug("row affected: %d" % rc)
            return rc
    finally:
        con.close()

