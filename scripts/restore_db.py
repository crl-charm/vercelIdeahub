import pymysql
import os

def restore():
    print("Connecting to database...")
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='ideahub_pos',
        client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS
    )
    try:
        sql_file = os.path.join('database', 'ideahub_pos.sql')
        print(f"Reading SQL file: {sql_file}...")
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Disable foreign key checks to avoid deletion/creation order violations
        with connection.cursor() as cursor:
            print("Disabling foreign key checks...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            
            # Wiping existing tables to avoid duplicate entries
            print("Wiping existing database tables...")
            cursor.execute("SHOW TABLES;")
            tables = [row[0] for row in cursor.fetchall()]
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS `{table}` CASCADE;")
            
            print("Running restoration SQL dump...")
            cursor.execute(sql)
            
            print("Re-enabling foreign key checks...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            
        connection.commit()
        print("Database restoration completed successfully!")
    except Exception as e:
        connection.rollback()
        print(f"Restoration failed: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    restore()
