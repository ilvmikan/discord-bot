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

    """
        MELHORAR O CÓDIGO DEPOIS, PELO MENOS FUNCIONA
    """

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            id_discord TEXT UNIQUE,
            description TEXT,
            background_image TEXT,
            color_red INTEGER DEFAULT 0,
            color_green INTEGER DEFAULT 0,
            color_blue INTEGER DEFAULT 255
        )
        """
        self.db.execute_query(query)


    def delete_table_content(self):
        delete_query = "DELETE FROM users"
        self.db.execute_query(delete_query)
        
        num_rows_affected = self.db.cursor.rowcount

        if num_rows_affected > 0:
            return 'Deletado!'
        return 'Erro ao deletar'


    def create_user_profile(self, id_discord, description=None, image_url=None, color=(0, 0, 255)):
        query_check = "SELECT id_discord FROM users WHERE id_discord = ?"
        values_check = (id_discord,)
        self.db.cursor.execute(query_check, values_check)

        if self.db.cursor.fetchone():
            print("Usuário já existe na tabela.")
            return False

        query_insert = """
            INSERT INTO users (id_discord, description, background_image, color_red, color_green, color_blue)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        values_insert = (id_discord, description, image_url, color[0], color[1], color[2])
        self.db.execute_query(query_insert, values_insert)
        print("Perfil do usuário criado com sucesso!!")


    def show_user_profile(self, user_id):
        query = "SELECT description, background_image, color_red, color_green, color_blue FROM users WHERE id_discord = ?"
        values = (user_id,)

        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchone()

        if result:
            return result[0], result[1], (result[2], result[3], result[4])
        else:
            return (
                "Utilize !profile create <desc> <img_url> para criar seu perfil",
                "https://i.pinimg.com/564x/b1/90/a2/b190a2ac5f6912ff2d976f3c753c0331.jpg",
                (0, 0, 255)
            )


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



    def edit_color(self, user_id, r, g, b):
        query_update = "UPDATE users SET color_red = ?, color_green = ?, color_blue = ? WHERE id_discord = ?"
        values_update = (r, g, b, user_id)
        self.db.execute_query(query_update, values_update)
        print("Cor do usuário atualizada com sucesso.")

    
    def profile_config(self, user_id):
        query = "SELECT id_discord, description, background_image, color_red, color_green, color_blue FROM users WHERE id_discord = ?"
        values = (user_id,)

        self.db.cursor.execute(query, values)
        result = self.db.cursor.fetchone()

        return result








        



















































