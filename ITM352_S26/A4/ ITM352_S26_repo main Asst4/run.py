# run.py
import threading
from __init__ import app, db
import routes
from sync_engine import sync_crypto_prices

def start_background_worker():
    """Starts the price syncing and alert engine in a separate thread."""
    # daemon=True ensures the thread exits when the main program stops
    worker_thread = threading.Thread(target=sync_crypto_prices, daemon=True)
    worker_thread.start()

if __name__ == '__main__':
    # Initialize the database and seed data if necessary
    with app.app_context():
        db.create_all()
        print("--- Database Tables Verified ---")
    
    # Start the background sync engine before launching the web server
    start_background_worker()
    
    # Explicitly print the access link for better visibility
    print("\n" + "="*40)
    print("  CRYPTO DASHBOARD ACTIVE")
    print("  URL: http://127.0.0.1:5001")
    print("="*40 + "\n")
    
    # use_reloader=False prevents the background thread from starting twice
    app.run(debug=True, use_reloader=False, port=5001)