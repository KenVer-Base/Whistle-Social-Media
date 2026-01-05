from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

# --- TABEL ASOSIASI (Relasi Many-to-Many) ---

# Tabel untuk Fitur 6 (Follow)
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# Tabel untuk Fitur 2 (Like Postingan)
post_likes = db.Table('post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

# Tabel untuk Fitur 5 (Like Comment)
comment_likes = db.Table('comment_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'))
)

# --- MODEL UTAMA ---

class User(UserMixin, db.Model): # Fitur 8 & 9 (Registrasi/Login)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    # Relasi
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    # Logic Follow (Fitur 6)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    # Logic Chat (Fitur 7 - Bonus)
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Logic API Auth (Poin 1) - Mengembalikan data user dalam bentuk JSON dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'followers_count': self.followers.count()
        }

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model): # Fitur 1 (Posting)
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(280)) # Caption wajib
    image_file = db.Column(db.String(100), nullable=True) # Foto (opsional)
    video_file = db.Column(db.String(100), nullable=True) # Video (opsional)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relasi
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    
    # Relasi Likes (Fitur 2)
    likes = db.relationship('User', secondary=post_likes, backref='liked_posts')

    # Logic Mention (Fitur 3) dilakukan di routes.py saat save, bukan di database column


class Comment(db.Model): # Fitur 4 (Comment)
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    # Relasi Like Comment (Fitur 5)
    likes = db.relationship('User', secondary=comment_likes, backref='liked_comments')


class Message(db.Model): # Fitur 7 (Chat Bonus)
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)