import threading
from __init__ import app, db
from models import Crypto
from sync_engine import sync_crypto_prices

def start_background_worker():
    # Run the sync engine in a separate thread so it doesn't block the website
    worker_thread = threading.Thread(target=sync_crypto_prices, daemon=True)
    worker_thread.start()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Seed initial data if empty
        if not Crypto.query.first():
            btc = Crypto(name="bitcoin", symbol="BTC", price=64500.00)
            eth = Crypto(name="ethereum", symbol="ETH", price=3450.00)
            db.session.add_all([btc, eth])
            db.session.commit()
    
    # Start the price sync engine automatically
    start_background_worker()
    
    app.run(debug=True, use_reloader=False) # use_reloader=False prevents the thread from starting twice