import psycopg2
from config import config

postgres_commands = (
    """
    DROP TABLE orders;
    """,
    """
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        number INTEGER NOT NULL, 
        cost_dollar INTEGER NOT NULL,
        delivery_date DATE NOT NULL,
        cost_rubles NUMERIC NOT NULL
    );
    """,
    """
    INSERT INTO orders (order_id, number, cost_dollar, delivery_date, cost_rubles)
    VALUES ({0}, {1}, {2}, '{3}', {4});
    """,
)


def db_manage(configuration, command):
    conn = None
    try:
        conn = psycopg2.connect(**configuration)
        cursor = conn.cursor()

        cursor.execute(command)

        cursor.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()

    cursor.execute('select version()')

    db_version = cursor.fetchone()
    print(db_version)

    cursor.close()
    conn.commit()
