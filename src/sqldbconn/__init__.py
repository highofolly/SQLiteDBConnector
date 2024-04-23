"""
SqliteDatabaseConnector is a Python module designed for easy interaction with SQLite databases.
With this module, you can create new tables, insert values into existing tables,
retrieve data, and close database connections efficiently.
Simplify your SQLite database management tasks with SqliteDatabaseConnector
"""

__version__ = "1.2404.1"

import sqlite3


class SQLiteTypes:
    # Resulting Affinity: INTEGER
    INTEGER = "INTEGER"
    INT = "INT"
    TINYINT = "TINYINT"
    SMALLINT = "SMALLINT"
    MEDIUMINT = "MEDIUMINT"
    BIGINT = "BIGINT"
    UNSIGNEDBIGINT = "UNSIGNED BIG INT"
    INT2 = "INT2"
    INT8 = "INT8"

    # Resulting Affinity: TEXT
    TEXT = "TEXT"
    CHARACTER = lambda x="20": f"CHARACTER({x})"
    VARCHAR = lambda x="255": f"VARCHAR({x})"
    VARYINGCHARACTER = lambda x="255": f"VARYINGCHARACTER({x})"
    NCHAR = lambda x="55": f"NCHAR({x})"
    NATIVECHARACTER = lambda x="70": f"NATIVECHARACTER({x})"
    NVARCHAR = lambda x="100": f"NVARCHAR({x})"
    CLOB = "CLOB"
    CHAR = "CHAR"

    # Resulting Affinity: BLOB
    BLOB = "BLOB"

    # Resulting Affinity: REAL
    REAL = "REAL"
    DOUBLE = "DOUBLE"
    DOUBLEPRECISION = "DOUBLE PRECISION"
    FLOAT = "FLOAT"

    # Resulting Affinity: NUMERIC
    NUMERIC = "NUMERIC"
    DECIMAL = lambda x="10,5": f"DECIMAL({x})"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    DATETIME = "DATETIME"

    # Other
    UUID = "UUID"
    ARRAY = "ARRAY"
    JSON = "JSON"
    NULL = "NULL"
    NOTNULL = "NOT NULL"
    PRIMARYKEY = "PRIMARY KEY"
    # CHECK = lambda x: f"CHECK({x})"
    # UNIQUE = lambda x: f"UNIQUE({x})"
    # FOREIGNKEY = lambda x: f"FOREIGN KEY({x})"
    # AUTOINCREMENT = lambda x: f"AUTOINCREMENT({x})"


class Table:
    """
    Class that represents a table in a database with methods for initializing, inserting values, getting values, and getting data type
    """

    def __init__(self, database, table_name: str, **kwargs: str):
        """
        Initialize the Table object with database connection, table name, and optional arguments. Create a new table in the database or drop the existing one

        example: Table(db, "test_table",
                        uid=[SQLiteTypes.INTEGER, SQLiteTypes.NOTNULL, SQLiteTypes.PRIMARYKEY],
                        column=[SQLiteTypes.TEXT, SQLiteTypes.NOTNULL])

        :param database: database connection object
        :param table_name: name of the table to be created
        :param kwargs: key-value pairs of columns and their types
        """
        self.db = database
        self.table_name = table_name
        kwargs = {"None": "NULL"} if not kwargs else kwargs
        self.db.cur.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        prompt = ", ".join([f"{key} {' '.join(kwargs[key])}" for key in kwargs])
        print(f"CREATE TABLE {self.table_name}({prompt})")
        self.db.cur.execute(f"CREATE TABLE {self.table_name}({prompt})")
        self.db.con.commit()

    def insert_values(self, **kwargs) -> bool:
        """
        Insert values into the table

        example: Table.insert_values(self, column="TEXT")

        :param kwargs: key-value pairs of columns and values to be inserted
        :return: True if successful
        """
        prompt = ", ".join(f"'{val}'" if isinstance(val, str) else str(val) for val in kwargs.values())
        self.db.cur.execute(f"INSERT INTO {self.table_name}({', '.join(kwargs.keys())}) VALUES({prompt})")
        self.db.con.commit()
        return True

    def get_values(self) -> list:
        """
        Retrieve values from the table

        example: Table.get_values(self)

        :return: list of values retrieved from the table
        """
        return self.db.cur.execute(f"SELECT * FROM {self.table_name}").fetchall()

    def get_type(self, column_name):
        """
        Get the data type of a specific column in the table

        example: Table.get_type(self, "column")

        :param column_name: name of the column
        :return: data type of the specified column
        """
        return SQLiteTypes().__getattribute__(self.db.cur.execute(
            f"SELECT type FROM pragma_table_info('{self.table_name}') WHERE name == '{column_name}'").fetchone()[0])


class Database:
    """
    Class that represents a database connection with methods for initializing, creating tables, and closing the connection
    """

    def __init__(self, file_name: str):
        """
        Initialize the Database object with the database file name and create a connection to the database

        example: Database(file_name)

        :param file_name: name of the database file
        """
        self.con = sqlite3.connect(file_name)
        self.cur = self.con.cursor()

    def create_table(self, table_name: str, **kwargs) -> Table:
        """
        Create a new table in the database using the Table class

        example: Database.create_table(self, "test_table",
                                      uid=[SQLiteTypes.INTEGER, SQLiteTypes.NOTNULL, SQLiteTypes.PRIMARYKEY],
                                      column=[SQLiteTypes.TEXT, SQLiteTypes.NOTNULL])

        :param table_name: name of the table to be created
        :param kwargs: key-value pairs of columns and their types
        :return: Table object representing the created table
        """
        return Table(self, table_name, **kwargs)

    def close(self):
        """
        Close the database connection

        example: Database.close(self)
        """
        self.con.close()
