from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# write your models here!

class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    pen_name = db.Column(db.String)

    #Add relationship
    books = db.relationship('Book', back_populates = 'author')

    #Add serialization rules
    serialize_rules = ('-books.author', )

    #Add validations
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError
        else:
            return value
    
    def __repr__(self):
        return f'<Author {self.id}: {self.name}>'
    

class Publisher(db.Model, SerializerMixin):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    founding_year = db.Column(db.Integer, nullable = False)

    #Add relationship
    books = db.relationship('Book', back_populates = 'publisher')

    #Add validations
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError
        else:
            return value
    
    @validates('founding_year')
    def validate_founding_year(self, key, value):
        if value >= 1600 and value <= 2024:
            return value
        else:
            raise ValueError
    
    def __repr__(self):
        return f'<Publisher {self.id}: {self.name}>'


class Book(db.Model, SerializerMixin):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, unique = True, nullable = False)
    page_count = db.Column(db.Integer, nullable = False)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'))

    #Add relationships
    author = db.relationship('Author', back_populates = 'books')
    publisher = db.relationship('Publisher', back_populates = 'books')

    #Add validations
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError
        else:
            return value
    
    @validates('page_count')
    def validate_page_count(self, key, value):
        if value > 0:
            return value
        else:
            raise ValueError
    
    def __repr__(self):
        return f'<Book {self.id}>'

