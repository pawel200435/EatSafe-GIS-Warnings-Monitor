from flask import Blueprint, render_template, request
from app.models import Ostrzezenie

ui_bp = Blueprint('ui', __name__)

@ui_bp.route('/')
def index():
    """
    Renders the main dashboard page.
    Fetches the 10 most recent food warnings to display on initial application load.
    """
    # Fetch latest warnings sorted by publication date descending
    initial_alerts = Ostrzezenie.query.order_by(Ostrzezenie.data_publikacji.desc()).limit(10).all()

    # Pass the initial alerts to the main index template
    return render_template('pages/index.html', alerts=initial_alerts)

@ui_bp.route('/search')
def search_alerts():
    """
    Handles live-search requests triggered by HTMX.
    Filters warnings by product name and returns an HTML partial block.
    """
    search_query = request.args.get('q','').strip()
    if search_query:
        # Filter database records where the 'produkt' column contains the search query (ilike is case-insensitive)
        filtered_alerts = Ostrzezenie.query.filter(Ostrzezenie.produkt.ilike(f'%{search_query}%')).all()
    else:
        # If the search field is cleared, get the 10 most recent warnings
        filtered_alerts = Ostrzezenie.query.order_by(Ostrzezenie.data_publikacji.desc()).limit(10).all()
    
    return render_template('partials/search_results.html', alerts=filtered_alerts)