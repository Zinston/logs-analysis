CREATE OR REPLACE VIEW pop AS
	SELECT path,
		   count(*) AS views
	FROM log
	WHERE path LIKE '/article/%'
		AND status = '200 OK'
	GROUP BY path;

CREATE OR REPLACE VIEW oeuvre AS
	SELECT name,
		   title,
		   slug
	FROM authors,
		 articles
	WHERE articles.author = authors.id;

CREATE OR REPLACE VIEW errors AS
	SELECT time::timestamptz::date,
		   count(*) AS errors
	FROM log
	WHERE not status = '200 OK'
	GROUP BY time::timestamptz::date;