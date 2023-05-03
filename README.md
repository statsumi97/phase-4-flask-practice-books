# Flask Practice - Books

This application is being built to track books, publishers, and authors.

## Getting Started

Fork and clone this repo. Use `pipenv install` and `pipenv shell` to begin. Be sure to `cd server`.

There are no tests so be sure to use the `flask shell` and Postman to be certain everything's working correctly!

## Models

You have three models: 

### Book

- `title` (string): Cannot be null, must be unique

- `page_count` (integer): Cannot be null, must be greater than 0

### Publisher

- `name` (string): Cannot be null

- `founding_year` (integer): Cannot be null, must be between 1600 and the current year

### Author

- `name` (string): Cannot be null

- `pen_name` (string)

## Relationships

This is a many-to-many relationship. 

- An author has many books and a book belongs to an author.

- A publisher has many books and a book belongs to a publisher.

- A publisher has many authors and an author has many publishers through books.

`Author --< Book >-- Publisher`

The foreign keys aren't specified so you'll have to determine where they go.

## Seeding

You can either use the `seed.py` to create your seeds or you can seed manually with `flask shell`.

## Routes

Build out these routes:


### Author Routes

#### `GET /authors/:id`

Returns an author with the matching id. If there is no author, returns a message that the author could not be found along with a 404.

Format your author object like so:

```json
    {
        "id": 1,
        "name": "Ursula K. Le Guin",
        "pen_name": null,
        "books": [
            {
                "id": 2,
                "title": "A Wizard of Earthsea",
                "page_count": 150,
                "author_name": "Ursula K. Le Guin",
                "publisher_name": "Random House"
            },
            {
                "id": 3,
                "title": "The Left Hand of Darkness",
                "page_count": 200,
                "author_name": "Ursula K. Le Guin",
                "publisher_name": "Random House"
            },
        ]
    }
```

#### `DELETE /author/:id`

Deletes the author and all associated books from the database. Returns 204 if the author was successfully deleted or 404 and an appropriate message if that author could not be found.


### Book Routes

#### `GET /books`

Returns a list of all books formatted like so:

```json
[
    {
        "id": 1,
        "name": "The Catcher in the Rye",
        "page_count": 234,
        "author_name": "J.D. Salinger",
        "publisher_name": "Little, Brown and Company"
    },
    {
        "id": 2,
        "name": "A Wizard of Earthsea",
        "page_count": 205,
        "author_name": "Ursula K. Le Guin",
        "publisher_name": "Parnassus Press"
    }
]
```

#### `POST /books`

Creates a new book. The book must belong to an author and a publisher. Return the new book details like so:

```json
    {
        "id": 4,
        "name": "The Tombs of Atuan",
        "page_count": 163,
        "author_name": "Ursula K. Le Guin",
        "publisher_name": "Parnassus Press"
    }
```


### Publisher Routes

#### `GET /publishers/:id`

Returns a publisher with the matching id. If there is no publisher, returns a message that the publisher could not be found along with a 404.

```json
{
    "id": 1,
    "name": "Parnassus Press",
    "founding_year": 1849,
    "authors": [
        {
            "id": 1,
            "name": "Ursula K. Le Guin",
            "pen_name": null
        },
        {
            "id": 2,
            "name": "Stephen King",
            "pen_name": "Richard Bachman",
        }
    ]
}
```

*Hint: You may need to pay attention to how you return your data as the author needs to be returned without their books for this route.*
