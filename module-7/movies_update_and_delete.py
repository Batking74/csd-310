import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# load credentials
secrets = dotenv_values(".env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True,
}


def show_films(cursor, title):
    print("\n-- {} --".format(title))

    query = """
        SELECT film.film_name,
               film.film_director,
               genre.genre_name,
               studio.studio_name
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """

    cursor.execute(query)
    films = cursor.fetchall()

    for film in films:
        print("Film Name: {}".format(film[0]))
        print("Director: {}".format(film[1]))
        print("Genre Name ID: {}".format(film[2]))
        print("Studio Name: {}\n".format(film[3]))


try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\nConnected to MySQL database\n")

    # DISPLAY FILMS
    show_films(cursor, "DISPLAYING FILMS")
    cursor.execute("""
    INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, genre_id, studio_id)
    VALUES (
        'Star Wars',
        '1977',
        121,
        'George Lucas',
        (SELECT genre_id FROM genre WHERE genre_name = 'SciFi' LIMIT 1),
        (SELECT studio_id FROM studio WHERE studio_name = '20th Century Fox' LIMIT 1)
    )
""")
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # UPDATE Alien → Horror
    cursor.execute("""
        UPDATE film
        SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror' LIMIT 1)
        WHERE film_name = 'Alien'
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

    # DELETE Gladiator
    cursor.execute("""
        DELETE FROM film WHERE film_name = 'Gladiator'
    """)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

finally:
    if "db" in locals() and db.is_connected():
        db.close()
