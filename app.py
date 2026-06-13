from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure local SQLite Database paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'players.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------------------------------------
# DATABASE SCHEMA MODEL WITH IMAGERY COLUMNS
# ----------------------------------------------------
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)       # Handles dynamic deep linking (/player/1)
    name = db.Column(db.String(100), nullable=False)
    home_name = db.Column(db.String(100))
    number = db.Column(db.String(10))
    position = db.Column(db.String(100))
    club = db.Column(db.String(100))
    foot = db.Column(db.String(20))
    joined_date = db.Column(db.String(50))
    contract_expiry = db.Column(db.String(50))
    birth_date = db.Column(db.String(50))
    citizenship = db.Column(db.String(100))
    photo_url = db.Column(db.String(500))              # Dynamic image profile URL
    logo_url = db.Column(db.String(500))     
    featured_photo_url = db.Column(db.String(500))          # Dynamic club logo icon URL
    transfers = db.relationship('TransferHistory', backref='player', lazy=True, cascade="all, delete-orphan")
    stats = db.relationship('PerformanceData', backref='player', lazy=True, cascade="all, delete-orphan")

class TransferHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    season = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(50))
    left_club = db.Column(db.String(100))
    joined_club = db.Column(db.String(100))
    joined_club_logo = db.Column(db.String(500))  #



class PerformanceData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    competition = db.Column(db.String(100), default="NPFL")
    competition_logo = db.Column(db.String(500)) # URL to league logo
    matches = db.Column(db.Integer, default=0)
    goals = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)    
# ----------------------------------------------------
# ROUTING HANDLERS
# ----------------------------------------------------

# Root URL redirect route for usability fallback
@app.route('/', methods=['GET'])
def index():
    # If someone lands on the absolute root base url, point them directly to Player #1 profile layout
    from flask import redirect, url_for
    return redirect(url_for('player_profile', player_id=1))

# Main template rendering route
@app.route('/player/<int:player_id>', methods=['GET'])
def player_profile(player_id):
    player = Player.query.get_or_404(player_id)
    return render_template('profile.html', player=player)

# Background async JSON API processing engine endpoint 
@app.route('/player/<int:player_id>/update', methods=['POST'])
def update_player(player_id):
    player = Player.query.get_or_404(player_id)
    data = request.get_json()
    
    # Capture structured text data updates
    player.name = data.get('name', player.name)
    player.number = data.get('number', player.number)
    player.club = data.get('club', player.club)
    player.position = data.get('position', player.position)
    player.birth_date = data.get('birthDate', player.birth_date)
    player.home_name = data.get('homeName', player.home_name)
    player.foot = data.get('foot', player.foot)
    player.joined_date = data.get('joinedDate', player.joined_date)
    player.contract_expiry = data.get('contract', player.contract_expiry)
    
    # Capture dynamic image source path transformations 
    player.photo_url = data.get('photoUrl', player.photo_url)
    player.logo_url = data.get('logoUrl', player.logo_url)
    player.featured_photo_url = data.get('featuredPhotoUrl', player.featured_photo_url)

    
    db.session.commit()
    return jsonify({"status": "success", "message": "Player database changes committed cleanly!"})

# Setup seeder arrays to auto-build profiles on fresh deployments
def seed_initial_data():
    if Player.query.count() == 0:
        player1 = Player(
            id=1,
            name="Olorunnishola Shile",
            home_name="Olorunnishola Shile",
            number="#10",
            position="Central Midfielder and Defensive Midfielder",
            club="Ikorodu City FC",
            foot="right",
            joined_date="Jan 1, 2026",
            contract_expiry="-",
            birth_date="03/10/2004 (22)",
            citizenship="Nigeria",
            photo_url="https://www.image2url.com/r2/default/images/1781133664238-ed00ca0d-8419-4d37-9c46-9036da50d4ce.jpeg",
            logo_url="https://images.unsplash.com/photo-1518152006812-edab29b069ac?w=100",
            # featured_photo_url="https://www.image2url.com/r2/default/images/1781178544859-4c9941bb-90cc-4b88-844b-2c60ba560756.jpeg"
        )
        t1 = TransferHistory(season="25/26", date="Jan 1, 2026", left_club="Kwara United Academy", joined_club="Ikorodu City", joined_club_logo="https://images.unsplash.com/photo-1518152006812-edab29b069ac?w=50")
        t2 = TransferHistory(season="24/26", date="Aug 12, 2024", left_club="Soccer Pro", joined_club="Kwara United Academy", joined_club_logo="https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?w=50")
        t3 = TransferHistory(season="22/24", date="Feb 05, 2022", left_club="Youth System", joined_club="Soccer Pro", joined_club_logo="https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=50")
        
        player1.transfers.extend([t1, t2, t3])
        
        p_stats = PerformanceData(
            competition="NPFL",
            competition_logo="https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=50", 
            matches=27,
            goals=10,
            assists=6
        )    
        player1.stats.append(p_stats)
        db.session.add(player1)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()      # Auto-generates local players.db schema instance file
        seed_initial_data()  # Generates initial player tables parameters
    print("Flask Server Database initialized successfully.")
     
     
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


