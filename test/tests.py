def test_post_borrows_invalid_book_id(self):
    response = self.client.post("/v1/borrows", json={"book_id": 1000, "reader_id": 1})
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json()["detail"], "Book not found")

def test_post_borrows_invalid_reader_id(self):
    response = self.client.post("/v1/borrows", json={"book_id": 1, "reader_id": 1000})
    self.assertEqual(response.status_code, 404)
    self.assertEqual(response.json()["detail"], "Reader not found")

def test_post_borrows_book_already_borrowed(self):
    book = books.get(1)
    book.borrowed_by = 1
    db.session.commit()

    response = self.client.post("/v1/borrows", json={"book_id": 1, "reader_id": 2})
    self.assertEqual(response.status_code, 409)
    self.assertEqual(response.json()["detail"], "Book already borrowed")