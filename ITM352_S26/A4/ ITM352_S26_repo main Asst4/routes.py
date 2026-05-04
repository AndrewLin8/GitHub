from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import requests
from datetime import datetime, timezone
import os
from __init__ import app, db
# Ensure PredictionVote is included here
from models import Crypto, User, PortfolioItem, PredictionVote
from security import encrypt_data, decrypt_data
import ccxt

# --- PAGE ROUTES ---

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('index.html', portfolio_items=[], alerts=[])

    user_id = session['user_id']
    portfolio_items = PortfolioItem.query.filter_by(user_id=user_id).all()
    
    alerts = []
    alerts_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'alerts_{user_id}.json')
    if os.path.exists(alerts_file):
        with open(alerts_file, 'r') as f:
            try:
                alerts = json.load(f)
            except json.JSONDecodeError:
                pass

    return render_template('index.html', portfolio_items=portfolio_items, alerts=alerts)

@app.route('/predictive-market')
def predictive_market():
    """Renders the new predictive market page."""
    return render_template('predictive_market.html')

# --- PORTFOLIO MANAGEMENT ---

@app.route('/add_portfolio_item', methods=['POST'])
def add_portfolio_item():
    if 'user_id' not in session:
        flash('Please log in to add items to your portfolio.', 'error')
        return redirect(url_for('login'))

    coin_id = request.form.get('coin_id', '').strip().lower()
    amount_str = request.form.get('amount', '0')
    target_str = request.form.get('target_price', '').strip()

    target_price = None
    if target_str:
        try:
            target_price = float(target_str)
        except ValueError:
            pass

    try:
        amount = float(amount_str)
    except ValueError:
        flash('Invalid amount entered.', 'error')
        return redirect(url_for('index'))

    if not coin_id:
        flash('Coin ID cannot be empty.', 'error')
        return redirect(url_for('index'))

    crypto = Crypto.query.filter(Crypto.name.ilike(coin_id)).first()
    if not crypto:
        crypto = Crypto(name=coin_id, symbol=coin_id.upper())
        db.session.add(crypto)
        db.session.commit()

    user_id = session['user_id']
    item = PortfolioItem.query.filter_by(user_id=user_id, crypto_id=crypto.id).first()
    if item:
        item.amount_owned = amount
        if target_price:
            item.target_price = target_price
        flash(f'Updated {crypto.name} amount to {amount}.', 'success')
    else:
        new_item = PortfolioItem(user_id=user_id, crypto_id=crypto.id, amount_owned=amount, target_price=target_price)
        db.session.add(new_item)
        flash(f'Added {crypto.name} to your watchlist/portfolio.', 'success')
        
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_portfolio_item/<int:item_id>', methods=['POST'])
def delete_portfolio_item(item_id):
    if 'user_id' not in session:
        flash('Please log in to manage your portfolio.', 'error')
        return redirect(url_for('login'))
        
    item = PortfolioItem.query.get(item_id)
    if item and item.user_id == session['user_id']:
        db.session.delete(item)
        db.session.commit()
        flash('Coin removed from your portfolio.', 'success')
        
    return redirect(url_for('index'))

# --- API ROUTES ---

@app.route('/api/portfolio_data')
def portfolio_data():
    if 'user_id' not in session:
        return jsonify({'portfolio_items': [], 'total_value': 0})

    user_id = session['user_id']
    portfolio_items = PortfolioItem.query.filter_by(user_id=user_id).all()

    data = []
    total_value = 0
    for item in portfolio_items:
        # Calculate total value for the header summary
        holding_val = (item.crypto.price or 0) * (item.amount_owned or 0)
        total_value += holding_val
        
        # Note: Ensure your sync_engine or DB stores high/low 
        # For now, we will pass placeholders if they aren't in your DB yet
        data.append({
            'item_id': item.id,
            'symbol': item.crypto.symbol,
            'price': item.crypto.price,
            'high_24h': item.crypto.high_24h if hasattr(item.crypto, 'high_24h') else 0,
            'low_24h': item.crypto.low_24h if hasattr(item.crypto, 'low_24h') else 0,
            'change_24h': item.crypto.change_24h,
            'market_cap': item.crypto.market_cap,
            'last_updated': item.crypto.last_updated.isoformat() if item.crypto.last_updated else None
        })
    
    return jsonify({'portfolio_items': data, 'total_value': total_value})

@app.route('/api/search_coins')
def search_coins():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])

    try:
        url = f"https://api.coingecko.com/api/v3/search?query={query}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return jsonify(data.get('coins', []))
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify([]), 500

# --- PREDICTION MARKET API ---

@app.route('/api/get_votes/<symbol>')
def get_votes(symbol):
    symbol = symbol.upper()
    up_count = PredictionVote.query.filter_by(coin_symbol=symbol, vote_type='up').count()
    down_count = PredictionVote.query.filter_by(coin_symbol=symbol, vote_type='down').count()
    
    total = up_count + down_count
    if total == 0:
        return jsonify({'up_pct': 50, 'down_pct': 50, 'total': 0})
    
    up_pct = round((up_count / total) * 100)
    return jsonify({'up_pct': up_pct, 'down_pct': 100 - up_pct, 'total': total})

@app.route('/api/cast_vote', methods=['POST'])
def cast_vote():
    if 'user_id' not in session:
        return jsonify({'error': 'You must be logged in to vote!'}), 401
    
    data = request.get_json()
    symbol = data.get('symbol').upper()
    vote_type = data.get('type')
    user_id = session['user_id']

    # Server-side block for double voting
    existing = PredictionVote.query.filter_by(user_id=user_id, coin_symbol=symbol).first()
    if existing:
        return jsonify({'error': 'You have already placed a prediction for this coin.'}), 400

    new_vote = PredictionVote(user_id=user_id, coin_symbol=symbol, vote_type=vote_type)
    db.session.add(new_vote)
    db.session.commit()
    
    return jsonify({'success': True})

# --- AUTH & SETTINGS ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username exists.', 'error')
            return redirect(url_for('register'))
        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in!', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials.', 'error')
    return render_template('login.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        api_key = request.form.get('api_key', '').strip()
        api_secret = request.form.get('api_secret', '').strip()
        
        if api_key: 
            user.api_key = api_key
        if api_secret: 
            user.encrypted_api_secret = encrypt_data(api_secret)
        
        # Save sound preference from the checkbox
        user.sound_alerts_enabled = 'enable_sound' in request.form
        
        db.session.commit()
        flash('Settings saved!', 'success')
        
    return render_template('settings.html', 
                           has_api_secret=bool(user.encrypted_api_secret), 
                           api_key=user.api_key,
                           sound_enabled=user.sound_alerts_enabled)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- EXCHANGE IMPORT (CCXT) ---

@app.route('/import_exchange', methods=['POST'])
def import_exchange():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user.api_key or not user.encrypted_api_secret:
        flash('Missing API credentials.', 'error')
        return redirect(url_for('settings'))

    api_secret = decrypt_data(user.encrypted_api_secret)
    try:
        exchange = ccxt.binance({'apiKey': user.api_key, 'secret': api_secret})
        balances = exchange.fetch_balance()
        totals = balances.get('total', {})
        imported = 0
        for symbol, amount in totals.items():
            amt = float(amount or 0)
            if amt <= 0: continue
            crypto = Crypto.query.filter_by(symbol=symbol.upper()).first()
            if not crypto:
                crypto = Crypto(name=symbol.lower(), symbol=symbol.upper())
                db.session.add(crypto)
                db.session.commit()
            item = PortfolioItem.query.filter_by(user_id=user.id, crypto_id=crypto.id).first()
            if item: item.amount_owned = amt
            else:
                db.session.add(PortfolioItem(user_id=user.id, crypto_id=crypto.id, amount_owned=amt))
            imported += 1
        db.session.commit()
        flash(f'Imported {imported} holdings.', 'success')
    except Exception as e:
        flash(f'Import failed: {e}', 'error')
    return redirect(url_for('settings'))