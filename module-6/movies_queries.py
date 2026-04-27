import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# use .env file for credentials
secrets = dotenv_values(".env")

# database configuration
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

try:
    # connect to database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\nDatabase user {} connected to MySQL on host {} with database {}\n".format(
        config["user"], config["host"], config["database"]
    ))

    # Query 1: display studio table
    print("-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT studio_id, studio_name FROM studio")

    studios = cursor.fetchall()

    for studio in studios:
        print("Studio ID: {}\nStudio Name: {}\n".format(
            studio[0], studio[1]
        ))

    # Query 2: display genre table
    print("-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT genre_id, genre_name FROM genre")

    genres = cursor.fetchall()

    for genre in genres:
        print("Genre ID: {}\nGenre Name: {}\n".format(
            genre[0], genre[1]
        ))

    # Query 3: films under 2 hours
    print("-- DISPLAYING Short Film RECORDS --")
    cursor.execute(
        "SELECT film_name, film_runtime FROM film WHERE film_runtime < 120"
    )

    short_films = cursor.fetchall()

    for film in short_films:
        print("Film Name: {}\nRuntime: {}\n".format(
            film[0], film[1]
        ))

    # Query 4: film names and directors grouped by director
    print("-- DISPLAYING Director RECORDS in Order --")
    cursor.execute("""
        SELECT film_name, film_director
        FROM film
        GROUP BY film_director, film_name
        ORDER BY film_director
    """)

    directors = cursor.fetchall()

    for director in directors:
        print("Film Name: {}\nDirector: {}\n".format(
            director[0], director[1]
        ))

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")

    else:
        print(err)

finally:
    if 'db' in locals() and db.is_connected():
        db.close()