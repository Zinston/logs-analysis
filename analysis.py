#!/usr/bin/env python
# -*-coding: utf8 -*
"""Prints out reports based on the analysis of a newspaper's database.

It answers the following questions:
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?
"""

import psycopg2
import datetime

DBNAME = "news"


def connect(dbname):
    """Connect to a database and return a cursor.

    Argument:
    dbname (string): the name of the database to connect to.
    """
    db = psycopg2.connect(database=dbname)
    return db.cursor()


def top_articles(top=3):
    """Return the [top] articles with the most views.

    Return a list of tuples (title string, views integer),
    sorted by views descending.

    A view means that article was successfully opened.

    Argument:
    top (integer): the maximum amount of articles to list (default: 3)
    """
    c = connect(DBNAME)

    c.execute("""SELECT title, views
                 FROM articles, pop
                 WHERE pop.path LIKE
                    CONCAT('%', articles.slug, '%')
                 ORDER BY views DESC
                 limit """ + str(top))

    return c.fetchall()


def top_authors():
    """Return every author's number of views.

    Return a list of tuples (name string, views integer),
    sorted by views descending.

    A view means any article by that author was successfully opened.
    """
    c = connect(DBNAME)

    c.execute("""SELECT name, count(*) AS views
                 FROM oeuvre, log
                 WHERE path LIKE
                    CONCAT('%', oeuvre.slug, '%')
                 and path LIKE '/article/%'
                 and status = '200 OK'
                 GROUP BY name
                 ORDER BY views DESC""")

    return c.fetchall()


def error_days():
    """Return all the days when more than 1% of requests lead to errors.

    Return a list of tuples (date date, errors float),
    sorted by views descending.

    A view means any article by that author was successfully opened.
    The errors are show as a fraction, 1.0 being equivalent to 100% errors.
    """
    c = connect(DBNAME)

    c.execute("""SELECT errors.time, errors.errors/count(*)::float AS errpc
                 FROM errors, log
                 WHERE errors.time = log.time::timestamptz::date
                 GROUP BY errors.time, errors.errors
                 HAVING errors.errors/count(*)::float > .01
                 ORDER BY errpc DESC""")

    return c.fetchall()


def analyse():
    """Print out reports in plain text, based on the data in the db.

    It answers the following questions:
    * What are the most popular three articles of all time?
    * Who are the most popular article authors of all time?
    * On which days did more than 1% of requests lead to errors?
    """
    articles = top_articles()
    print 'TOP 3 ARTICLES:'
    for a in articles:
        article = a[0]
        views = a[1]
        print '"%s" — %s views' % (article, str(views))

    authors = top_authors()
    print '\nTOP AUTHORS:'
    for a in authors:
        author = a[0]
        views = a[1]
        print '%s — %s views' % (author, str(views))

    days = error_days()
    print '\nDAYS WITH OVER 1% ERRORS:'
    for d in days:
        date = d[0].strftime("%B %d, %Y")
        pc = round(100 * d[1], 2)
        print '%s — %s%% errors' % (date, str(pc))


if __name__ == '__main__':
    analyse()
