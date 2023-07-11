from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_borrow_valid_book_and_reader():
    response = client.post("/v1/borrows", json={"book_id": 1, "reader_id": 2})

    assert response.status_code == 200
    assert response.json()["message"] == "Book borrowed"

def test_borrow_invalid_book_id():
    response = client.post("/v1/borrows", json={"book_id": 999, "reader_id": 2})

    assert response.status_code == 400
    assert response.json()["error"] == "Invalid book ID"

def test_borrow_invalid_reader_id():
    response = client.post("/v1/borrows", json={"book_id": 1, "reader_id": 999})

    assert response.status_code == 400
    assert response.json()["error"] == "Invalid reader ID"

def test_borrow_book_already_borrowed():
    book = Book(id=1, title="The Hitchhiker's Guide to the Galaxy")
    reader = Reader(id=2, name="Arthur Dent")
    db.session.add(book)
    db.session.add(reader)
    db.session.commit()

    book.borrower_id = reader.id
    db.session.commit()

    response = client.post("/v1/borrows", json={"book_id": 1, "reader_id": 2})

    assert response.status_code == 400
    assert response.json()["error"] == "Book is already borrowed"