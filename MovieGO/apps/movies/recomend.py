import sqlite3

def recomend():
    sqlite_connection = sqlite3.connect('db.sqlite3')
    cur = sqlite_connection.cursor()
    one_result = cur.execute("""SELECT title, avg(value) FROM movies_movie  JOIN movies_rating ON movies_movie.id  =  movies_rating.ratings_id JOIN movies_ratingstar ON movies_rating.star_id = movies_ratingstar.id  GROUP BY movies_movie.id HAVING avg(value) > 1.0 LIMIT 5""").fetchall()
    print( one_result)

recomend()

