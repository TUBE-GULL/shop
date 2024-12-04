import aiosqlite 
import os

class DataBase:

    def __init__(self, db_name='./db/DataBase.db'):
        self.db_name = db_name

    def _ensure_db_directory(self):
        db_directory = os.path.dirname(self.db_name)
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)
            print('base data successfully create')
        else:
            print('the data is already there')

    async def create_table_user(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(''' 
                    CREATE TABLE IF NOT EXISTS data_users(
                    user_name TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                );
                ''')
            await db.commit()

    async def create_table_admin(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS data_admin(
                    user_name TEXT,
                    password TEXT  
                );
                ''')
            await db.commit()

    async def create_table_card(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS data_card(s
                    name TEXT,
                    "group" TEXT,  
                    price INTEGER,
                    unit TEXT,
                    quantity INTEGER  
                );
                ''')
            await db.commit()

    
    async def add_user_database_in_table(self, table_name: str, user_name: str, password: str):
        """
        Добавляет нового пользователя в указанную таблицу базы данных, если его еще нет.
    
        Функция проверяет уникальность пользователя по имени (`user_name`) в таблице базы данных. 
        Если пользователь с таким именем уже существует, новая запись не будет добавлена.
    
        :param table_name: Имя таблицы, в которую нужно добавить пользователя.
        :type table_name: str
        :param user_name: Имя пользователя, которое нужно сохранить в таблице.
        :type user_name: str
        :param password: Пароль пользователя, который будет сохранен в таблице.
        :type password: str
        
        :return: 
            - `True`, если пользователь был успешно добавлен.
            - `False`, если пользователь с таким именем уже существует или произошла ошибка.
        :rtype: bool
        
        :raises:
            - Печатает сообщение об ошибке, если возникает ошибка при работе с базой данных.
        """
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute(
                    f'''INSERT OR IGNORE INTO {table_name} (user_name, password) VALUES (?, ?)''',
                    (user_name, password)
                )
                await db.commit()
    
                # Проверяем, была ли добавлена строка
                if cursor.rowcount > 0:
                    print(f"Пользователь '{user_name}' успешно добавлен.")
                    return True
                else:
                    print(f"Пользователь '{user_name}' уже существует.")
                    return False
    
        except aiosqlite.Error as e:
            print(f"Ошибка при добавлении пользователя '{user_name}': {e}")
            return False



    # для записи 
    async def write_database(self, table_name: str, user_name: str, column: str, value: any):
        """
        Универсальная функция для обновления значения в указанной таблице.

        :param table_name: Имя таблицы, в которой нужно обновить данные (например, 'data_users').
        :param user_name: Значение для фильтрации (например, имя пользователя для строки, которую нужно обновить).
        :param column: Имя столбца, в который нужно записать новое значение.
        :param value: Новое значение для указанного столбца.
        :raises ValueError: Если переданы недопустимые значения таблицы или столбца.
        :raises aiosqlite.Error: Если произошла ошибка при выполнении запроса в SQLite.
        """
        allowed_tables = ["data_users", "data_admin", "data_card"]
        allowed_columns = {
            "data_users": ["user_name", "password"],
            "data_admin": ["user_name", "password"],
            "data_card": ["name", "group", "price", "unit", "quantity"]
        }

    
        if table_name not in allowed_tables:
            raise ValueError(f"Never name table: {table_name}")
        
        if column not in allowed_columns.get(table_name, []):
            raise ValueError(f"Never name column '{column}' for table '{table_name}'")

        try:
            async with aiosqlite.connect(self.db_name) as db:
                query = f'UPDATE {table_name} SET {column} = ? WHERE name = ?'
                await db.execute(query, (value, user_name))
                await db.commit()

        except aiosqlite.Error as e:
            # Логгируем и выбрасываем ошибку для обработки на более высоком уровне
            print(f"Ошибка при выполнении запроса: {e}")
            raise



    # для чтения  ok !
    async def read_database(self, table_name: str, user_name :str, columns:list ):
       
        """
        Универсальная функция для чтения значений из указанных столбцов таблицы для пользователя с данным user_name.

        :param user_name: идентификатор пользователя
        :param columns: список столбцов, которые нужно запросить
        :return: tuple с значениями выбранных столбцов или None, если данных нет
        """
        columns_str = ", ".join(columns)
        
        async with aiosqlite.connect(self.db_name) as db:
            query = f"SELECT {columns_str} FROM {table_name} WHERE user_name = ?"
        
            
            async with db.execute(query, (user_name,)) as cursor:
                results = await cursor.fetchone()
                if results is not None:
                    return results
                else:
                    return None
                
        