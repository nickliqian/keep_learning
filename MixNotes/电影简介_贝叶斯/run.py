from sqlite3 import *
from math import *


def init_db():
    db = connect(database='world.db')
    return db.cursor(), db


def query_data(country_name, count, db_cursor):
    sql = "select city.Name from country,city where city.CountryCode=country.code" \
          " and country.name='{}' and city.population>={} order by city.Population".format(country_name, count)
    db_cursor.execute(sql)
    results = db_cursor.fetchall()
    print(results)
    return results, len(results)


def get_color(num):
    colours = ['aqua', 'black', 'blue', 'fuchsia', 'gray',
               'green', 'lime', 'maroon', 'navy', 'olive',
               'purple', 'red', 'silver', 'teal', 'yellow']
    return colours[(len(colours) % (num+1))-1]


def show_population(country_list, count, test):
    db_cursor, db = init_db()

    for country in country_list:

        results, city_count = query_data(country, count, db_cursor)

        filename = open(test + "_" + country + ".html", 'w')
        filename.write("<html><body><h1 align='center'>cities of{}</h1>"
                       "<h3 align='center'>with population>={}</h3>"
                       "<h3 align='center'>city count:{}</h3><hr><p>"
                       .format(country, count, city_count))
        for i in range(len(results)):
            filename.write('<span style="font-size:{}px; color:{}"> {}</span>'
                           .format(city_count - i, get_color(i), results[i][0]))
        filename.write('</p><div><a href="" align="right">Previous Page</a>'
                       '<a href="" align="left">Next Page</a></div></body></html>')
        filename.close()
    db_cursor.close()
    db.close()


if __name__ == "__main__":
    show_population(['Germany', 'New Zealand', 'Austria', 'Australia'], 1000000, 'Test05')