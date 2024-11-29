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

# Function to fetch search results with pagination
def search_results(keywords_input, offset, limit=100):
    # Get a connection from the pool
    mydb = db_pool.get_connection()
    cursor = mydb.cursor()

    # Call the stored procedure with pagination
    cursor.callproc('SearchKeywordsWithPagination', [keywords_input, offset, limit])

    # Fetch the results
    results = []
    for result in cursor.stored_results():
        results = result.fetchall()
        
    # Close the cursor and connection
    cursor.close()
    mydb.close()

    return results

@app.route('/search', methods=['GET'])
def search():
    # Retrieve keywords and page from query parameters
    keywords_input = request.args.get('keywords', '')
    page = int(request.args.get('page', 1))  # Get page number from request
    limit = int(request.args.get('limit', 100))  # Set the limit (default is 100)
    offset = (page - 1) * limit  # Calculate the offset

    # Split input keywords using regex
    keywords = re.split(r'[,\s;|-]+', keywords_input)
    like_clauses = " ".join([kw.title().strip() for kw in keywords if kw])
    # print(like_clauses)
    # Ensure that keywords are present
    if not like_clauses:
        return jsonify([])  # Return an empty list if no keywords are provided

    try:
        # Fetch the results from the database
        results = search_results(like_clauses, offset, limit)
        # print(results)
        return jsonify({"data": results, "page": page, "has_more": len(results) == limit})
    
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return jsonify({"error": "Database error occurred."}), 500
    except Exception as ex:
        # Log any other exceptions
        print(f"General Error: {ex}")
        return jsonify({"error": "An internal error occurred."}), 500

# @app.route('/')
# def home():
#     return send_from_directory('static', 'index1.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

