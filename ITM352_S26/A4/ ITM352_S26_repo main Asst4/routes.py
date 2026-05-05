from flask import render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import requests
from datetime import datetime, timezone
import os
from __init__ import app, db
from models import Crypto, Poll, Settings, User, PortfolioItem, PredictionVote, PollVote
from security import encrypt_data, decrypt_data
import ccxt
import hashlib

# --- HELPERS ---

def get_market_recommendations():
    """Returns a list of mock market recommendations to display on the dashboard."""
    return [
        {
            'name': 'Bitcoin', 'symbol': 'BTC', 'verdict': 'Strong Buy',
            'sentiment_score': 92, 'reason': 'High institutional adoption and positive ETF inflows.'
        },
        {
            'name': 'Ethereum', 'symbol': 'ETH', 'verdict': 'Buy',
            'sentiment_score': 85, 'reason': 'Upcoming network upgrades and strong DeFi ecosystem.'
        },
        {
            'name': 'Solana', 'symbol': 'SOL', 'verdict': 'Hold',
            'sentiment_score': 65, 'reason': 'High throughput but recent network congestion concerns.'
        }
    ]

def get_currency_data(currency_code):
    """Returns the symbol and the conversion rate relative to 1 USD"""
    rates = {
        'USD': {'symbol': '$', 'rate': 1.0},
        'EUR': {'symbol': '€', 'rate': 0.85},
        'GBP': {'symbol': '£', 'rate': 0.74}
    }
    return rates.get(currency_code, {'symbol': '$', 'rate': 1.0})

# --- PAGE ROUTES ---

@app.route('/', endpoint='portfolio_index')
def portfolio_index_view(): # Renamed function to be unique
    config = Settings.query.first()
    if not config:
        config = Settings()
        db.session.add(config)
        db.session.commit()

    curr_data = get_currency_data(config.currency)
    currency_symbol = curr_data['symbol']
    rate = curr_data['rate']
    recommendations = get_market_recommendations()

    if 'user_id' not in session:
        return render_template('index.html', 
                               portfolio_items=[], 
                               alerts=[], 
                               recommendations=recommendations,
                               settings=config, 
                               currency_symbol=currency_symbol,
                               conversion_rate=rate)

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

    return render_template('index.html', 
                           portfolio_items=portfolio_items, 
                           alerts=alerts, 
                           recommendations=recommendations,
                           settings=config, 
                           currency_symbol=currency_symbol,
                           conversion_rate=rate)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('portfolio_index'))

# --- PREDICTION MARKETS & POLLS ---

@app.route('/api/polymarket_polls')
def get_manifold_polls_sidebar():
    """Fetches a limited set (10) for the sidebar dashboard"""
    try:
        url = "https://api.manifold.markets/v0/search-markets?term=Crypto&limit=10&sort=score&filter=open"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        polls = []
        for market in data:
            if market.get('outcomeType') != 'BINARY': continue
            prob = market.get('probability')
            if prob is None: continue

            polls.append({
                'question': market.get('question'),
                'yes_price': float(prob),
                'no_price': 1.0 - float(prob),
                'id': market.get('slug'),
                'volume': f"${int(market.get('volume', 0)):,}"
            })
        return jsonify(polls)
    except Exception as e:
        print(f"Sidebar Fetch Error: {e}")
        return jsonify([])

@app.route('/api/all_manifold_polls')
def get_all_manifold_polls():
    """Fetches a large list of crypto markets for the dedicated 'All Polls' page"""
    try:
        url = "https://api.manifold.markets/v0/search-markets?term=Crypto&limit=100&sort=score&filter=open"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        polls = []
        for market in data:
            if market.get('outcomeType') != 'BINARY': continue
            prob = market.get('probability')
            if prob is None: continue

            polls.append({
                'question': market.get('question'),
                'yes_price': float(prob),
                'no_price': 1.0 - float(prob),
                'id': market.get('slug'),
                'volume': f"${int(market.get('volume', 0)):,}"
            })
            
        return jsonify(polls)
    except Exception as e:
        print(f"All Polls Fetch Error: {e}")
        return jsonify([])

@app.route('/all_polls')
def all_polls():
    config = Settings.query.first()
    return render_template('all_polls.html', settings=config)

# --- RECOMMENDATIONS ---

@app.route('/recommendations')
def recommendations():
    config = Settings.query.first()
    trending_coins = []
    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        response = requests.get(url, timeout=10)
        data = response.json()
        for item in data.get('coins', []):
            coin = item.get('item', {})
            trending_coins.append({
                'id': coin.get('id'),
                'name': coin.get('name'),
                'symbol': coin.get('symbol'),
                'thumb': coin.get('thumb'),
                'market_cap_rank': coin.get('market_cap_rank')
            })
    except Exception as e:
        print(f"Trending Fetch Error: {e}")
        
    return render_template('recommendations.html', trending_coins=trending_coins, settings=config)

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
        try: target_price = float(target_str)
        except ValueError: pass

    try: amount = float(amount_str)
    except ValueError:
        flash('Invalid amount entered.', 'error')
        return redirect(url_for('portfolio_index'))

    if not coin_id:
        flash('Coin ID cannot be empty.', 'error')
        return redirect(url_for('portfolio_index'))

    crypto = Crypto.query.filter(Crypto.name.ilike(coin_id)).first()
    if not crypto:
        crypto = Crypto(name=coin_id, symbol=coin_id.upper())
        db.session.add(crypto)
        db.session.commit()

    user_id = session['user_id']
    item = PortfolioItem.query.filter_by(user_id=user_id, crypto_id=crypto.id).first()
    if item:
        item.amount_owned = amount
        if target_price: item.target_price = target_price
        flash(f'Updated {crypto.name} amount to {amount}.', 'success')
    else:
        new_item = PortfolioItem(user_id=user_id, crypto_id=crypto.id, amount_owned=amount, target_price=target_price)
        db.session.add(new_item)
        flash(f'Added {crypto.name} to your watchlist/portfolio.', 'success')
        
    db.session.commit()
    return redirect(url_for('portfolio_index'))

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
        
    return redirect(url_for('portfolio_index'))

# --- API ROUTES ---

@app.route('/api/portfolio_data')
def portfolio_data():
    if 'user_id' not in session:
        return jsonify({'portfolio_items': [], 'total_value': 0})

    user_id = session['user_id']
    portfolio_items = PortfolioItem.query.filter_by(user_id=user_id).all()

    config = Settings.query.first()
    rate = get_currency_data(config.currency if config else 'USD')['rate']

    data = []
    total_value = 0
    for item in portfolio_items:
        raw_price = (item.crypto.price or 0)
        holding_val = raw_price * (item.amount_owned or 0)
        total_value += holding_val
        
        data.append({
            'item_id': item.id,
            'symbol': item.crypto.symbol,
            'price': raw_price * rate,
            'change_24h': item.crypto.change_24h,
            'market_cap': (item.crypto.market_cap or 0) * rate,
            'last_updated': item.crypto.last_updated.isoformat() if item.crypto.last_updated else None
        })
    
    return jsonify({'portfolio_items': data, 'total_value': total_value * rate})

@app.route('/api/search_coins')
def search_coins():
    query = request.args.get('query', '').strip()
    if not query: return jsonify([])

    try:
        url = f"https://api.coingecko.com/api/v3/search?query={query}"
        response = requests.get(url, timeout=10)
        return jsonify(response.json().get('coins', []))
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

    existing = PredictionVote.query.filter_by(user_id=user_id, coin_symbol=symbol).first()
    if existing:
        return jsonify({'error': 'Already placed a prediction for this coin.'}), 400

    new_vote = PredictionVote(user_id=user_id, coin_symbol=symbol, vote_type=vote_type)
    db.session.add(new_vote)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/create_poll', methods=['POST'])
def create_poll():
    data = request.get_json()
    new_question = data.get('question')
    if not new_question:
        return jsonify({'error': 'Question cannot be empty'}), 400
        
    poll = Poll(question=new_question)
    db.session.add(poll)
    db.session.commit()
    return jsonify({'message': 'Poll created successfully!', 'id': poll.id})

@app.route('/api/cast_poll_vote', methods=['POST'])
def cast_poll_vote():
    if 'user_id' not in session:
        return jsonify({'error': 'Login required!'}), 401
    
    data = request.get_json()
    poll_id = data.get('poll_id')
    vote_choice = data.get('vote')
    user_id = session['user_id']

    existing = PollVote.query.filter_by(user_id=user_id, poll_id=poll_id).first()
    if existing:
        return jsonify({'error': 'Already voted on this poll.'}), 400

    poll = Poll.query.get(poll_id)
    if not poll:
        return jsonify({'error': 'Poll not found'}), 404

    db.session.add(PollVote(user_id=user_id, poll_id=poll_id, choice=vote_choice))

    if vote_choice == 'yes':
        poll.yes_votes = (poll.yes_votes or 0) + 1
    else:
        poll.no_votes = (poll.no_votes or 0) + 1
    
    db.session.commit()
    return jsonify({'success': True})

# --- PAGE VIEWS ---

@app.route('/predictive_market/<symbol>')
def predictive_market(symbol):
    symbol = symbol.upper()
    crypto = Crypto.query.filter_by(symbol=symbol).first()
    if not crypto:
        crypto = Crypto(name=symbol.lower(), symbol=symbol)
        db.session.add(crypto)
        db.session.commit()

    all_polls = Poll.query.order_by(Poll.created_at.desc()).all() 
    config = Settings.query.first()
    
    return render_template('predictive_market.html', 
                           crypto=crypto, 
                           polls=all_polls,
                           settings=config)

# --- AUTH & SETTINGS ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username exists.', 'error')
            return redirect(url_for('register'))
        
        manual_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        new_user = User(username=username, password_hash=manual_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        entered_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        if user and user.password_hash == entered_hash:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('portfolio_index'))
            
        flash('Invalid credentials.', 'error')
    return render_template('login.html')

@app.route('/import_exchange', methods=['POST'])
def import_exchange():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if not user.api_key or not user.encrypted_api_secret:
        return redirect(url_for('settings'))

    api_secret = decrypt_data(user.encrypted_api_secret)
    try:
        exchange = ccxt.binance({'apiKey': user.api_key, 'secret': api_secret})
        balances = exchange.fetch_balance()
        totals = balances.get('total', {})
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
        db.session.commit()
    except Exception as e:
        flash(f'Import failed: {e}', 'error')
    return redirect(url_for('settings'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # SAFETY CHECK: If the session has an ID but the database doesn't find the user
    if not user:
        session.clear() # Clear the invalid session
        flash("User session expired or account not found. Please login again.", "error")
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        api_key = request.form.get('api_key', '').strip()
        api_secret = request.form.get('api_secret', '').strip()
        if api_key: 
            user.api_key = api_key
        if api_secret: 
            user.encrypted_api_secret = encrypt_data(api_secret)
        db.session.commit()
        flash("Settings updated successfully!", "success")

    config = Settings.query.first() or Settings()
    return render_template('settings.html', 
                           settings=config,
                           user=user,
                           has_api_secret=bool(user.encrypted_api_secret), 
                           api_key=user.api_key)

@app.route('/api/save_settings', methods=['POST'])
def save_settings():
    data = request.get_json()
    config = Settings.query.first() or Settings()
    config.theme = data.get('theme')
    config.currency = data.get('currency')
    config.alert_enabled = data.get('alert_enabled')
    config.refresh_rate = int(data.get('refresh_rate'))
    db.session.add(config)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Settings updated!'})