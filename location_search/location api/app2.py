from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
import re
from mysql.connector import pooling

app = Flask(__name__, static_folder='static', static_url_path='')

# Database connection pool
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "saurabh123",
    "database": "api_scrap",
    "pool_name": "mypool",
    "pool_size": 5
}

db_pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)

# Generator function to lazily fetch search results in batches
def search_generator(keywords_input):
    # Get a connection from the pool
    mydb = db_pool.get_connection()
    cursor = mydb.cursor()

    # Call the stored procedure
    cursor.callproc('SearchKeywords', [keywords_input])

    # Fetch and yield results lazily in batches of 100
    for result in cursor.stored_results():
        while True:
            rows = result.fetchmany(100)  # Fetch up to 100 rows
            if not rows:
                break
            for row in rows:
                yield row[0]  # Return the keyword_search column

    # Close the cursor and connection
    cursor.close()
    mydb.close()

@app.route('/search', methods=['GET'])
def search():
    # Retrieve keywords from query parameters
    keywords_input = request.args.get('keywords', '')
    like_clauses = []

    # Split input keywords using regex
    keywords = re.split(r'[,\s;|-]+', keywords_input)
    for keyword in keywords:
        keyword = keyword.strip()
        if keyword:  # Check if keyword is not empty
            like_clauses.append(keyword.title())

    like_clauses = " ".join(like_clauses)
    print(like_clauses)
    # Ensure that keywords are present
    if not like_clauses:
        return jsonify([])  # Return an empty list if no keywords are provided

    # Use the generator to return results one by one
    try:
        results = list(search_generator(like_clauses))
        return jsonify(results)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
