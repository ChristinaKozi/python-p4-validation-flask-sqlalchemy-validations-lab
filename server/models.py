from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Author must have a name')
        existing_author = Author.query.filter(Author.name == name).first()
        if existing_author is not None:
            raise ValueError('No two authors have the same name.')
        return name
        
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if not isinstance(number, str) or len(number) != 10 or not number.isdigit():
            raise ValueError('Phone numbers must be ten digits.')
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates('title')
    def validate_title(self, key, title):
        phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if title is None or title == '':
            raise ValueError('Post must have a title')
        titles = []
        for phrase in phrases:
            if phrase in title:
                titles.append(phrase)
        if not titles:
            raise ValueError("Title must contain clickbait")
        return title

    @validates('content', 'summary')
    def validate_length(self, key, string):
        if key == 'content':
            if len(string) < 250:
                raise ValueError("Post content must be at least 250 characters long.")
        if key == 'summary':
            if len(string) > 250:
                raise ValueError("Summary must be less than 250 characters long.")
        return string
        
    # @validates('summary')
    # def validate_summary(self, key, summary):
    #     if len(summary) > 250:
    #         raise ValueError("Summary must be less than 250 characters long.")
    #     return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be either Fiction or Non-Fiction")
        return category
   
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
