## SQLiteDBConnector
Is a [Python](https://www.python.org/) module designed for easy interaction with [SQLite](https://www.sqlite.org/) databases.
<br>Simplify your SQLite database management tasks with SQLiteDBConnector
## Documentation
#### Install
```
git clone https://github.com/highofolly/SQLiteDBConnector.git
```
#### Example
```
bd = Database("database.db")
tb = bd.create_table("test_table",
                     uid=[SQLiteTypes.INTEGER, SQLiteTypes.NOTNULL, SQLiteTypes.PRIMARYKEY],
                     column=[SQLiteTypes.TEXT, SQLiteTypes.NOTNULL])
tb.insert_values(column="test")
print(tb.get_values())
bd.close()
```
This code creates a SQLite database file with the file name "database.db", then creates a table with 2 columns (uid INTEGER NOT NULL PRIMARY KEY, column TEXT NOT NULL). Then inserts the value into the second column, displays the table values and closes the connection
