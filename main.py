import os
import re
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
from tabulate import tabulate


def proverka_zaprosa(zapros: str) -> str:
    chistiy_zapros = zapros.strip()

    if not re.match(r'^SELECT\b', chistiy_zapros, re.IGNORECASE):
        raise ValueError("Ошибка: разрешены только SELECT-запросы")

    if not re.search(r'\bLIMIT\b', chistiy_zapros, re.IGNORECASE):
        chistiy_zapros = f"{chistiy_zapros.rstrip(';')} LIMIT 5;"

    return chistiy_zapros


def main():
    load_dotenv()

    try:
        podkluchenie = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        kursor = podkluchenie.cursor()

        tekst_zaprosa = input("Введите SQL-запрос:\n")

        try:
            gotoviy_zapros = proverka_zaprosa(tekst_zaprosa)
            kursor.execute(gotoviy_zapros)

            stroki = kursor.fetchall()
            zagolovki = [desc[0] for desc in kursor.description]

            print("\nРезультат:")
            print(tabulate(stroki, headers=zagolovki, tablefmt="psql"))

        except ValueError as oshibka_znacheniya:
            print(oshibka_znacheniya)
        except Error as oshibka_bd:
            print(f"Ошибка выполнения запроса: {oshibka_bd}")

    except Error as oshibka_podklucheniya:
        print(f"Ошибка подключения к PostgreSQL: {oshibka_podklucheniya}")
    finally:
        if 'podkluchenie' in locals() and podkluchenie:
            kursor.close()
            podkluchenie.close()


if __name__ == "__main__":
    main()