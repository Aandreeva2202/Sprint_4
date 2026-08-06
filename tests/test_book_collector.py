import pytest


from data import *


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.mark.parametrize('book_data', [[book1_1], [book1_1, book1_2], ['А'], ['А'*40]])
    def test_add_new_book_success(self, collector, book_data):
        for book in book_data:
            collector.add_new_book(book)
        for book in book_data:
            assert book in collector.books_genre

    @pytest.mark.parametrize('book_fail', ['', 'А'*41])
    def test_add_new_book_fail_length(self, collector, book_fail):
        collector.add_new_book(book_fail)
        assert book_fail not in collector.books_genre

    def test_add_new_book_double(self, collector):
        collector.add_new_book(book1_1)
        collector.add_new_book(book1_1)
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize(
        'book_and_genre',
        [
            [(book1_1, genre1)],
            [(book1_1, genre1), (book2_1, genre2)],
            [(book1_1, genre1), (book1_2, genre1)]
        ]
    )
    def test_set_book_genre_success(self, collector, book_and_genre):
        for book, genre in book_and_genre:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)
        for book, genre in book_and_genre:
            assert collector.books_genre[book] == genre

    def test_set_book_genre_fail(self, collector):
        collector.set_book_genre(book1_1, genre1)
        assert book1_1 not in collector.books_genre

    def test_set_book_genre_not_genre(self, collector):
        collector.add_new_book(book1_1)
        collector.set_book_genre(book1_1, 'Мелодрама')
        assert collector.books_genre[book1_1] == ''

    @pytest.mark.parametrize(
        'book_data,genre_data',
        [
            [book1_1, genre1],
            [book2_1, genre2],
            [book3_1, genre3],
            [book4_1, genre4],
            [book5_1, genre5]
        ]
    )
    def test_get_book_genre(self, collector, book_data, genre_data):
        collector.add_new_book(book_data)
        collector.set_book_genre(book_data, genre_data)
        book_genre = collector.get_book_genre(book_data)
        assert book_genre == genre_data

    def test_get_book_genre_no_book(self, collector):
        book_genre = collector.get_book_genre(book1_1)
        assert book_genre == None

    @pytest.mark.parametrize(
        'books_and_genres',
        [
            [(book4_1, genre4), (book4_2, genre4)]
        ]
    )
    def test_get_books_with_specific_genre(self, collector, books_and_genres):
        for book, genre in books_and_genres:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)
        books_with_genre = collector.get_books_with_specific_genre(genre4)
        assert books_with_genre == [book4_1, book4_2]

    def test_get_books_with_genre_no_books(self, collector):
        collector.add_new_book(book1_1)
        collector.set_book_genre(book1_1, genre1)
        assert collector.get_books_with_specific_genre(genre2) == []

    def test_get_books_with_genre_non_existent_genre(self, collector):
        assert collector.get_books_with_specific_genre('Мелодрама') == []

    def test_get_books_genre(self, collector):
        collector.add_new_book(book1_1)
        collector.set_book_genre(book1_1, genre1)
        books_genre = collector.get_books_genre()
        assert books_genre == {book1_1: genre1}

    @pytest.mark.parametrize(
        'books_and_genres',
        [
            [(book1_1, genre1)],
            [(book1_1, genre1), (book2_1, genre2)],
            [(book1_1, genre1), (book3_1, genre3)]
        ]
    )
    def test_get_books_for_children(self, collector, books_and_genres):
        for book, genre in books_and_genres:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)
        books_for_children = collector.get_books_for_children()
        assert books_for_children == [book1_1]

    def test_get_books_for_children_nonexistent_genre(self, collector):
        collector.add_new_book(book1_1)
        assert collector.get_books_for_children() == []

    @pytest.mark.parametrize(
        'book_data',
        [
            [book1_1],
            [book1_1, book2_1]
        ]
    )
    def test_add_book_in_favorites(self, collector, book_data):
        for book in book_data:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        for book in book_data:
            assert book in collector.favorites

    def test_add_book_in_favorites_no_book(self, collector):
        collector.add_book_in_favorites(book1_1)
        assert collector.favorites == []

    def test_add_book_in_favorites_double(self, collector):
        collector.add_new_book(book1_1)
        collector.add_book_in_favorites(book1_1)
        collector.add_book_in_favorites(book1_1)
        assert len(collector.favorites) == 1

    @pytest.mark.parametrize(
        'book_data',
        [
            [book1_1],
            [book1_1, book2_1]
        ]
    )
    def test_delete_book_from_favorites(self, collector, book_data):
        for book in book_data:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
            collector.delete_book_from_favorites(book)
        for book in book_data:
            assert book not in collector.favorites

    def test_delete_book_from_favorites_no_book(self, collector):
        collector.delete_book_from_favorites(book1_1)
        assert collector.favorites == []

    @pytest.mark.parametrize(
        'book_data',
        [[book1_1, book2_1]]
    )
    def test_get_list_of_favorites_books(self, collector, book_data):
        for book in book_data:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        favorites_books = collector.get_list_of_favorites_books()
        assert favorites_books == collector.favorites
