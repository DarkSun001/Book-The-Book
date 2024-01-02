import requests

BASE_URL = "http://127.0.0.1:8000"

def menu():
    print("BookIT Client")
    print("1. Listing the books")
    print("2. Getting a book")
    print("3. Creating a book")
    print("4. Deleting a book")
    print("0. Exit")

def list_books():
    response = requests.get(f"{BASE_URL}/book")
    if response.status_code == 200:
        books = response.json()
        print("List of all books:")
        for book in books["List of all books"]:
            print(f"ID: {book['book_id']}, Name: {book['name_of_book']}")
    else:
        print("Failed to fetch the list of books.")

def get_book():
    book_id = input("Enter the ID of the book you want to get: ")
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    if response.status_code == 200:
        book = response.json()
        print("Details about the selected book:")
        print(f"ID: {book['book_id']}")
        print(f"Name: {book['name_of_book']}")
        print(f"Release Date: {book['release_date']}")
        print(f"Author Name: {book['author_name']}")
        print(f"Number of Pages: {book['number_of_pages']}")
    elif response.status_code == 404:
        print("Book not found.")
    else:
        print("Failed to get the book details.")

def create_book():
    book_data = {
        "books_name": input("Enter the name of the book: "),
        "release_date": input("Enter the release date of the book (YYYY-MM-DD): "),
        "author_name": input("Enter the author's name: "),
        "number_of_pages": int(input("Enter the number of pages: "))
    }
    response = requests.post(f"{BASE_URL}/book", json=book_data)
    if response.status_code == 201:
        book_id = response.json().get("id")
        print(f"New book created successfully with ID: {book_id}")
    elif response.status_code == 400:
        print("Invalid book data. Please check the input.")
    else:
        print("Failed to create the book.")

def delete_book():
    book_id = input("Enter the ID of the book you want to delete: ")
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    if response.status_code == 200:
        print("Book deleted successfully.")
    elif response.status_code == 404:
        print("Book not found.")
    else:
        print("Failed to delete the book.")

if __name__ == '__main__':
    while True:
        menu()
        choice = input("Enter your choice (1/2/3/4/0): ")
        if choice == '1':
            list_books()
        elif choice == '2':
            get_book()
        elif choice == '3':
            create_book()
        elif choice == '4':
            delete_book()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")
