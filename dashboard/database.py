import sqlite3

class Model:
    def __init__(self):
        self.db_file = "storage.db"
        print("Database connected...")

    def execute_query(self, query, parameters=()):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(query, parameters)
        conn.commit()
        result = c.fetchall()
        conn.close()
        return result

    def selectAll(self):
        query = f"SELECT * FROM {self.db_file}"
        return self.execute_query(query)

    def getById(self, file_id):
        query = f"SELECT * FROM {self.db_file} WHERE id=?"
        return self.execute_query(query, (file_id,))

    def createFileDatabase(self):
        query = f'''CREATE TABLE IF NOT EXISTS {self.db_file}
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, size TEXT)'''
        self.execute_query(query)

    def create(self, file_path, size):
        query = f"INSERT INTO {self.db_file} (name, size) VALUES (?, ?)"
        return self.execute_query(query, (file_path, size))

    def delete(self, file_id):
        query = f"DELETE FROM {self.db_file} WHERE id=?"
        return self.execute_query(query, (file_id,))
