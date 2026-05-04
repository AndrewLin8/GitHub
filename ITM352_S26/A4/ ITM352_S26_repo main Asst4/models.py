from datetime import datetime, timezone
from __init__ import db

# 1. CRYPTO MARKET DATA MODEL
class Crypto(db.Model):
    # Allows the table to be redefined during circular imports without crashing
    __table_args__ = {'extend_existing': True} 
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=True)
    change_24h = db.Column(db.Float, nullable=True)
    market_cap = db.Column(db.Float, nullable=True)
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Crypto {self.symbol}: ${self.price}>"

# 2. USER ACCOUNT MODEL
class User(db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # API Credentials for Binance Integration
    api_key = db.Column(db.String(256), nullable=True)
    encrypted_api_secret = db.Column(db.String(256), nullable=True)
    
    # User Preferences
    sound_alerts_enabled = db.Column(db.Boolean, default=True) 
    
    # Relationship to link users to their specific portfolio items
    portfolio = db.relationship('PortfolioItem', backref='user', lazy=True)

# 3. PORTFOLIO & WATCHLIST MODEL
class PortfolioItem(db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crypto_id = db.Column(db.Integer, db.ForeignKey('crypto.id'), nullable=False)
    
    # Amount owned (Set to 0 if the user just wants to watch the price)
    amount_owned = db.Column(db.Float, default=0.0)
    
    # Price target for triggering Smart Alerts
    target_price = db.Column(db.Float, nullable=True)
    
    # Links back to the Crypto table to get live prices
    crypto = db.relationship('Crypto')

# 4. PREDICTION MARKET VOTING MODEL
class PredictionVote(db.Model):
    # Combines unique constraint for one-vote-per-user with the extension flag
    __table_args__ = (
        db.UniqueConstraint('user_id', 'coin_symbol', name='_user_coin_uc'),
        {'extend_existing': True}
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coin_symbol = db.Column(db.String(10), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False) # 'up' or 'down'