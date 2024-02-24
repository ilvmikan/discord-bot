import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print("Conexão bem-sucedida ao banco de dados.")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexão encerrada.")

    def execute_query(self, query, values=None):
        try:
            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Erro ao executar a consulta: {e}")

class UserProfile:
    def __init__(self, db_name):
        self.db = Database(db_name)
        self.db.connect()


    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            id_discord TEXT UNIQUE,
            description TEXT,
            background_image TEXT'
        )
        """
        self.db.execute_query(query)


    def create_user_profile(self, id_discord, description=None, image_url=None):
        query_check = "SELECT id_discord FROM users WHERE id_discord = ?"
        values_check = (id_discord,)
        self.db.cursor.execute(query_check, values_check)

        if self.db.cursor.fetchone():
            print("Usuário já existe na tabela.")
            return False

        query_insert = "INSERT INTO users (id_discord, description, background_image) VALUES (?, ?, ?)"
        values_insert = (id_discord, description, image_url)
        self.db.execute_query(query_insert, values_insert)
        print("Perfil do usuário criado com sucesso.")


    def show_user_profile(self, user_id):
        query = "SELECT description, background_image FROM users WHERE id_discord = ?"
        values = (user_id,)

        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchone()
        if result:
            return result[0], result[1]
        else:
            return "Descrição não encontrada no banco de dados.", "https://i.pinimg.com/564x/b1/90/a2/b190a2ac5f6912ff2d976f3c753c0331.jpg"
    

    def edit_description(self, user_id, new_description):
        query_update = "UPDATE users SET description = ? WHERE id_discord = ?"
        values_update = (new_description, user_id)
        self.db.execute_query(query_update, values_update)
        print("Descrição do usuário atualizada com sucesso.")



    def edit_image(self, user_id, new_image):
        query_update = "UPDATE users SET background_image = ? WHERE id_discord = ?"
        values_update = (new_image, user_id)
        self.db.execute_query(query_update, values_update)
        print("Descrição do usuário atualizada com sucesso.")







        



















































