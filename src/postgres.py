import psycopg2


class PG:
    def __init__(self, access_info: dict):
        self.conn = self.get_connection(access_info)
    
    def get_connection(self, access_info: dict) -> psycopg2.extensions.connection:
        return psycopg2.connect(**access_info)

    def close(self):
        if self.conn:
            self.conn.close()

    def insert(self, table: str, columns:list , values: tuple):
        try:
            with self.conn.cursor() as cur:
                cols = ", ".join(columns)
                placeholders = ", ".join(["%s"] * len(values))
                sql = f"insert into {table} ({cols}) values ({placeholders})"
                cur.execute(sql, values)
            
            self.conn.commit()

        except Exception as e:
            print(f"Error inserting into {table}: {e}")
            self.conn.rollback()

        finally:
            self.conn.cursor()
