import os
import re
import sqlite3 as db


def connect(sql: str, params=None):

    class QueryObject:

        def __init__(self, connect_handler, stmt: str, var: (None, tuple)):
            cursor = connect_handler.cursor()

            try:
                if isinstance(var, tuple):
                    cursor.execute(stmt, var)
                else:
                    cursor.execute(stmt)
            except db.OperationalError as error:
                exit(error)

            if re.match(re.compile("^DELETE|^INSERT|^UPDATE"), stmt):
                connect_handler.commit()
                self.affected_rows = cursor.rowcount
                self.last_row_id = cursor.lastrowid
            else:
                results = cursor.fetchall()
                self.num_of_rows = len(results)
                self.rows = results
            connect_handler.close()

    topic_database = os.path.join(
        os.path.dirname(__file__), "database/NATopics.db"
    )
    if not os.path.exists(topic_database):
        raise FileNotFoundError(
            "cannot find the database '{}'".format(topic_database)
        )
    else:
        return QueryObject(db.connect(topic_database), sql, params)
