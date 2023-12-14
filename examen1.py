import requests
import mysql.connector


class DataProcessor:
    def __init__(self):
        self.data = []

    def connectDb(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="programador",
                password="123456",
                database="analista",
            )
            return conn
        except mysql.connector.Error as e:
            print("Error al conectar a la base de datos:", e)
            return None

    def obtener_datos_desde_api(self):
        url = "https://raw.githubusercontent.com/panchojarab/iap/main/preES4"
        resultado = requests.get(url)
        if resultado.status_code == 200:
            data = resultado.json()
        for item in data["ResultSet"]["Result"]:
            self.data.append(
                {
                    "title": item["Title"],
                    "fileSize": item["FileSize"],
                    "summary": item["Summary"],
                    "url": item["Thumbnail"]["Url"],
                }
            )

        self.mostrar_info()

    def mostrar_info(self):
        if self.data == []:
            print("No hay resultados")
            return
        for item in self.data:
            print("title: ", item["title"])
            print("fileSize: ", item["fileSize"])
            print("summary: ", item["summary"])
            print("url: ", item["url"])
            print("\n")

    def add_to_database(self):
        if self.data == []:
            print("No hay resultados")
            return
        conn = self.connectDb()
        if conn:
            cursor = conn.cursor()
            try:
                for item in self.data:
                    query = "insert into preparaciones (title, fileSize, summary, url) values(%s, %s, %s, %s)"
                    data = (
                        item["title"],
                        item["fileSize"],
                        item["summary"],
                        item["url"],
                    )
                    cursor.execute(query, data)
                conn.commit()
                conn.close()
                print("Se insertó correctamente a la base de datos")
            except Exception as e:
                print("Error al insertar a la base de datos:", e)
                conn.rollback()
                conn.close()

    def mostrar_menu(self):
        print("1. Convertir")
        print("2. Mostrar resultados")
        print("3. Agregar resultados a la base de datos")
        print("4. Salir \n")

    def main(self):
        while True:
            self.mostrar_menu()
            response = input("Selecciona una opción: ")
            if response == "1":
                self.obtener_datos_desde_api()
            elif response == "2":
                self.mostrar_info()
            elif response == "3":
                self.add_to_database()
            elif response == "4":
                break
            else:
                print("Ingresa una opción válida")


if __name__ == "__main__":
    data_processor = DataProcessor()
    data_processor.main()
