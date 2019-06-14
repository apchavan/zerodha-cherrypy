<p align='center'>
<strong>Zerodha tasks solutions</strong>
</p>

**This repository has solutions for _two_ tasks from Zerodha:**
- [x] A Python script that:- Downloads the Equity Bhavcopy zip from the above page- Extracts and parses the CSV file in it- Writes the records into Redis into appropriate data structures(Fields: code, name, open, high, low, close).
- [x] Simple CherryPy python web application that:- Renders an HTML5 + CSS3 page that lists the top 10 stock entries from the Redis DB in a table- Has a searchbox that lets you search the entries by the 'name' field in Redis and renders it in a table.

**_CherryPy_** web application is hosted on [Heroku](https://www.heroku.com/home) at: https://zerodha-cherrypy.herokuapp.com/
