from flask import Flask, jsonify, request, Response

app = Flask(__name__)
books = [
  {
    "name": "Green Eggs and Ham",
    "price": 7.99,
    "isbn": 9780123213
  },
  {
    "name": 'The Cat In The Hat',
    "price": 6.99,
    "isbn": 120391203
  },
]

def validBookObject(bookObject):
  if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
    return True
  else: 
    return False

#POST /books
@app.route('/books', methods=["POST"])
def add_book():
  request_data = request.get_json()
  if (validBookObject(request_data)):
    new_book = {
      "name": request_data['name'],
      "price": request_data['price'],
      "isbn": request_data['isbn'],
    }
    books.insert(0, new_book)
    response = Response("", 200, mimetype="application/json")
    print(response)
    response.headers['Location'] = '/books/' + str(new_book['isbn'])
    return response
  else:
    invalidObjectErrorMsg = {
      "error": "",
      "helpString": "Data passed in similar to this {'name': 'bookname', 'price': '9.1', 'isbn': 3213123123}"
    }
    response = Response(invalidObjectErrorMsg, status=400, mimetype="application/json")
    return response



#GET /books
@app.route('/books')
def hello_world():
  return jsonify({ 'books': books })

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
  return_value = {}
  for book in books:
    if book['isbn'] == isbn:
      return_value = {
        'name': book['name'],
        'price': book['price']
      }
  return jsonify(return_value)

app.run(port=5000)