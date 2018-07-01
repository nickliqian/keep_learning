# This Python page uses the following encoding: utf-8
# !/usr/bin/env python


# -----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  
#
#    Student no:    
#    Student name:  
#
#  NB: pages submitted without a completed copy of this statement
#  will not be marked.  All pages submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
# --------------------------------------------------------------------#


# -----Task Description-----------------------------------------------#
#
#  OUR WORLD
#
#  Countries come in all shapes and sizes.  There is an enormous
#  difference between the population levels of cities in different
#  parts of the world.  In this task you will develop a program
#  that helps visualise the population differences between cities
#  and countries.  To do so you will make use of three different
#  computer languages, Python, SQL and HTML.  You will develop
#  a Python function, show_population, which accesses data in an 
#  SQLite database and uses this to generate HTML documents which
#  visually display a comparison of city population in a country.
#  See the instructions accompanying this page for full details.
#
# --------------------------------------------------------------------#


# -----Acceptance Tests-----------------------------------------------#
#
#  This section contains unit tests that run your program.  You
#  may not change anything in this section.  NB: 'Passing' these
#  tests does NOT mean you have completed the assignment because
#  they do not check the HTML pages produced by your program.
#
"""
##Test 1: China cities > 1m
##>>> show_population(['China'], 1000000, 'Test01') 
##
##Test 2: Aus cities > 100000
##>>> show_population(['Australia'], 100000, 'Test02') 
##
##Test 3 - 2 countries
##>>> show_population(['China', 'Australia'], 1000000, 'Test03') # 

##Test 4 - 3 countries
##>>> show_population(['China', 'India', 'United States'], 10000, 'Test04') 

##Test 5 - 4 countries
##>>> show_population(['Germany', 'New Zealand', 'Austria', 'Australia'], 1000000, 'Test05') 
##
##Test 6 - 6 countries
##>>> show_population(['Indonesia', 'Japan', 'Thailand', 'Taiwan', 'Ireland', 'United Kingdom'], 1000, 'Test06')
##
##Test 7 - empty results set
##>>> show_population(['Australia'], 5000000, 'Test07')

"""

# Get the sql functions
from sqlite3 import *
from math import *

# (You may NOT import any other modules)


##### PUT YOUR show_population FUNCTION HERE
# 连接数据库（不用改）
link = connect("world.db")
c = link.cursor()


# 前置函数
def open_page(name):
    page_write = open(name, 'w')
    return page_write


def write_header(pagename):
    pagename.write("""
    <html>

        <title>
        Test THT2 page
        </title>

    """)


def write_footer(pagename):
    pagename.write("""
    </html>""")


def close_page(pagename):
    pagename.close()


# 主函数
def show_population(list, num, uni):
    numb = "%d" % (num)

    for country in list:
        country1 = "%s" % (country)
        n = 0
        n += 1

        c.execute("SELECT code FROM Country WHERE name = '%s'" % (str(country)))
        for row in c.fetchall():
            short = row[0]
        link.rollback()

        c.execute("SELECT count(*) FROM City WHERE CountryCode = '%s' and population > '%d'" % (str(short), int(num)))
        for row in c.fetchall():
            n = row[0]
        link.rollback()
        nu = "%d" % (n)

        results = ''
        try:
            c.execute("SELECT Name FROM city WHERE CountryCode = '%s' and population > '%d'" % (str(short), int(num)))
            for row in c.fetchall():
                results += row[0] + ' '
            if results == '':
                results = ''
            else:
                results = results[:-1]
        except:
            results = ''
        txt = "%s" % (results)

        pagename = open_page(uni + "_" + country + ".html")
        write_header(pagename)
        pagename.write("""
               <body>
               <h1 align='center'><b>Cities of
          """ + country1 +
                       """               
                            <b></h1>
             
                            <h2 align='center'><b>with population >=
                       """ + numb +
                       """               
                            <b></h2>
             
                            <h2 align='center'><b>city count:
                       """ + nu +
                       """               
                           <b></h2>
             
                           <hr>
             
                           <p><span style="color:random">
                       """ + txt +
                       """
                            </p></span>
             
                           <hr>
             
                           <a href="filname" align="right">Previous Page</a>
                           <a href="filname" align="left">Next Page</a>
             
                           </body>
                            """)
        write_header(pagename)
        close_page(pagename)


if __name__ == "__main__":
    from doctest import testmod
    show_population(['China'], 1000000, 'Test01')
    testmod(verbose=False)

# --------------------------------------------------------------------#
