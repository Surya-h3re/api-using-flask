from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from flask import abort, make_response , request

app = Flask(__name__)


auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'surya':
        return 'suryapass'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


books = [
    {
        'book_id': 1,
        'title': u'The alphabets',
        'author':u'surya',
        'description': u'alphabets in english', 
        'price': 60,
        'total_pages':50
    },
    {
        'book_id': 2,
        'title': u'My journey',
        'author':u'suryakant',
        'description': u'my journey from the beginning', 
        'price': 360,
        'total_pages':250
    }
]

@app.route('/books', methods=['POST'])
@auth.login_required
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books[-1]['book_id'] + 1,
        'title': request.json['title'],
        'author': request.json.get('author', ""),
        'description': request.json.get('description', ""),
        'price': request.json.get('price', ""),
        'total_pages': request.json.get('total_pages', ""),
    }
    books.append(book)
    return jsonify({'book': book}), 201
#curl -u surya:suryapass -i -H "Content-Type: application/json" -X POST -d "{\"title\":\"Read a book\",\"author\":\"new author\",\"description\":\"add the book description\",\"price\":100,\"total_pages\":200}" http://localhost:5000/books


@app.route('/books', methods=['GET'])
@auth.login_required
def get_books():
    return jsonify({'books': books})
#curl -u surya:suryapass -i http://localhost:5000/books


@app.route('/books/<int:book_id>', methods=['GET'])
@auth.login_required
def get_book(book_id):
    book = [book for book in books if book['book_id'] == book_id]
    if len(book) == 0:
        abort(404)
    return jsonify({'book': book[0]})
#curl -u surya:suryapass -i http://localhost:5000/books/2


@app.route('/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    book = [book for book in books if book['book_id'] == book_id]
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({'result': 'Book Deleted'})
#curl -u surya:suryapass -i -H "Content-Type: application/json" -X DELETE  http://localhost:5000/books/2


@app.route('/books/<int:book_id>', methods=['PUT'])
@auth.login_required
def update_book(book_id):
    book = [book for book in books if book['book_id'] == book_id]
    if len(book) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'author' in request.json and type(request.json['author']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'price' in request.json and type(request.json['price']) is not int:
        abort(400)
    if 'total_pages' in request.json and type(request.json['total_pages']) is not int:
        abort(400)
    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['description'] = request.json.get('description', book[0]['description'])
    book[0]['total_pages'] = request.json.get('total_pages', book[0]['total_pages'])
    book[0]['price'] = request.json.get('price', book[0]['price'])
    book[0]['author'] = request.json.get('author', book[0]['author'])
    return jsonify({'book': book[0]})
#curl -u surya:suryapass -i -H "Content-Type: application/json" -X PUT -d "{\"author\":\"updated_author\"}" http://localhost:5000/books/2


if __name__ == '__main__':
    app.run(debug=True)