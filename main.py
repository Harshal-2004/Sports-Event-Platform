from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import logging
from datetime import datetime, timedelta
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
from models.event import Event
from models.service import Service
from models.package import Package
from models.auction import Auction
from models.payment import Payment

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure CORS
CORS(app)


# Get MongoDB URI from environment only
mongo_uri = os.environ.get("MONGODB_URI")
if not mongo_uri:
    logger.error("MONGODB_URI not set in environment variables. Please add it to your .env file.")
    raise RuntimeError("MONGODB_URI not set in environment variables.")
logger.info(f"Connecting to MongoDB at: {mongo_uri}")

try:
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client.sports_events
    
    # Define collections
    events_collection = db.events
    services_collection = db.services
    packages_collection = db.packages
    auctions_collection = db.auctions
    payments_collection = db.payments
    
    # Test connection
    db.command('ping')
    logger.info("Successfully connected to MongoDB!")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_pages(path):
    return send_from_directory('.', path)

@app.route('/sports-auction')
def sports_auction_platform():
    """Serve the sports auction platform page"""
    return send_from_directory('pages', 'sports_auction.html')

@app.route('/api/customize', methods=['POST'])
def customize_event():
    try:
        data = request.get_json()
        logger.info(f"Received event customization request: {data}")

        # Parse date from string to datetime
        event_date = None
        if data.get('eventDate'):
            try:
                event_date = datetime.fromisoformat(data.get('eventDate').replace('Z', '+00:00'))
            except ValueError:
                event_date = datetime.strptime(data.get('eventDate'), '%Y-%m-%d')

        # Create event object
        event = Event(
            sports=data.get('sports', []),
            location=data.get('location'),
            event_date=event_date,
            attendees=data.get('attendees', 0),
            budget=data.get('budget', 0),
            requirements=data.get('requirements', [])
        )

        # Save to database
        result = events_collection.insert_one(event.to_dict())
        event.id = str(result.inserted_id)

        return jsonify({
            "status": "success",
            "message": "Event customization saved successfully",
            "data": event.to_dict()
        })

    except Exception as e:
        logger.error(f"Error customizing event: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Events API endpoints
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        events = list(events_collection.find())
        return jsonify([Event.from_dict(event).to_dict() for event in events])
    except Exception as e:
        logger.error(f"Error getting events: {str(e)}")
        return jsonify([])

# Services API endpoints
@app.route('/api/services', methods=['GET'])
def get_services():
    try:
        services = list(services_collection.find())
        return jsonify([Service.from_dict(service).to_dict() for service in services])
    except Exception as e:
        logger.error(f"Error getting services: {str(e)}")
        return jsonify([])

@app.route('/api/services', methods=['POST'])
def add_service():
    try:
        data = request.get_json()
        service = Service(
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price', 0),
            category=data.get('category')
        )
        
        result = services_collection.insert_one(service.to_dict())
        service.id = str(result.inserted_id)
        
        return jsonify({
            "status": "success",
            "message": "Service added successfully",
            "data": service.to_dict()
        })
    except Exception as e:
        logger.error(f"Error adding service: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Packages API endpoints
@app.route('/api/packages', methods=['GET'])
def get_packages():
    try:
        packages = list(packages_collection.find())
        return jsonify([Package.from_dict(package).to_dict() for package in packages])
    except Exception as e:
        logger.error(f"Error getting packages: {str(e)}")
        return jsonify([])

@app.route('/api/packages', methods=['POST'])
def add_package():
    try:
        data = request.get_json()
        package = Package(
            name=data.get('name'),
            description=data.get('description'),
            services=data.get('services', []),
            price=data.get('price', 0)
        )
        
        result = packages_collection.insert_one(package.to_dict())
        package.id = str(result.inserted_id)
        
        return jsonify({
            "status": "success",
            "message": "Package added successfully",
            "data": package.to_dict()
        })
    except Exception as e:
        logger.error(f"Error adding package: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Auction API endpoints
@app.route('/api/auctions', methods=['GET'])
def get_auctions():
    try:
        # Get all auctions from the database
        auctions = list(auctions_collection.find())
        
        # Convert ObjectId to string for JSON serialization and update status
        now = datetime.utcnow()
        for auction in auctions:
            auction['_id'] = str(auction['_id'])
            end_date = datetime.fromisoformat(auction['end_date'].replace('Z', '+00:00'))
            auction['status'] = 'active' if end_date > now else 'closed'
            
        return jsonify({
            'status': 'success',
            'data': auctions
        })
    except Exception as e:
        logger.error(f"Error getting auctions: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/auctions', methods=['POST'])
def add_auction():
    try:
        data = request.get_json()
        logger.info(f"Received auction data: {data}")
        
        # Validate required fields
        required_fields = ['title', 'description', 'starting_price', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
        
        # Validate end date
        try:
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
            if end_date <= datetime.utcnow():
                return jsonify({'status': 'error', 'message': 'End date must be in the future'}), 400
        except ValueError as e:
            return jsonify({'status': 'error', 'message': 'Invalid end date format'}), 400
        
        # Validate starting price
        try:
            starting_price = float(data['starting_price'])
            if starting_price <= 0:
                return jsonify({'status': 'error', 'message': 'Starting price must be greater than 0'}), 400
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid starting price'}), 400
        
        # Create auction object
        auction = {
            'title': data['title'],
            'description': data['description'],
            'starting_price': starting_price,
            'current_price': starting_price,
            'end_date': data['end_date'],
            'status': 'active',
            'created_at': datetime.utcnow().isoformat(),
            'last_bid_time': None,
            'bids': []
        }
        
        # Insert into database
        result = auctions_collection.insert_one(auction)
        
        if result.inserted_id:
            auction['_id'] = str(result.inserted_id)
            logger.info(f"Created new auction: {auction['title']}")
            return jsonify({
                'status': 'success',
                'message': 'Auction created successfully',
                'data': auction
            })
        else:
            logger.error("Failed to create auction - no inserted_id returned")
            return jsonify({'status': 'error', 'message': 'Failed to create auction'}), 500
            
    except Exception as e:
        logger.error(f"Error creating auction: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/auctions/<auction_id>/bid', methods=['POST'])
def place_bid(auction_id):
    try:
        data = request.get_json()
        logger.info(f"Received bid data for auction {auction_id}: {data}")
        
        if 'bid_amount' not in data:
            return jsonify({'status': 'error', 'message': 'Missing bid amount'}), 400
            
        try:
            bid_amount = float(data['bid_amount'])
            if bid_amount <= 0:
                return jsonify({'status': 'error', 'message': 'Bid amount must be greater than 0'}), 400
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid bid amount'}), 400
        
        # Find the auction
        try:
            auction = auctions_collection.find_one({'_id': ObjectId(auction_id)})
        except Exception as e:
            logger.error(f"Invalid auction ID format: {auction_id}")
            return jsonify({'status': 'error', 'message': 'Invalid auction ID'}), 400
            
        if not auction:
            logger.error(f"Auction not found: {auction_id}")
            return jsonify({'status': 'error', 'message': 'Auction not found'}), 404
            
        # Check if auction is active
        end_date = datetime.fromisoformat(auction['end_date'].replace('Z', '+00:00'))
        if end_date <= datetime.utcnow():
            logger.warning(f"Attempted bid on expired auction: {auction_id}")
            return jsonify({'status': 'error', 'message': 'Auction has ended'}), 400
            
        # Check if bid is higher than current price
        current_price = float(auction.get('current_price', 0))
        if bid_amount <= current_price:
            logger.warning(f"Bid too low: {bid_amount} <= {current_price}")
            return jsonify({'status': 'error', 'message': f'Bid must be higher than current price (${current_price})'}), 400
            
        # Create bid object
        bid = {
            'amount': bid_amount,
            'time': datetime.utcnow().isoformat()
        }
        
        # Update auction with new bid
        result = auctions_collection.update_one(
            {'_id': ObjectId(auction_id)},
            {
                '$set': {
                    'current_price': bid_amount,
                    'last_bid_time': bid['time']
                },
                '$push': {
                    'bids': bid
                }
            }
        )
        
        if result.modified_count > 0:
            logger.info(f"Bid placed successfully: Auction {auction_id}, Amount ${bid_amount}")
            return jsonify({
                'status': 'success',
                'message': 'Bid placed successfully',
                'data': {
                    'auction_id': auction_id,
                    'new_price': bid_amount,
                    'bid_time': bid['time']
                }
            })
        else:
            logger.error(f"Failed to update bid: Auction {auction_id}, Amount ${bid_amount}")
            return jsonify({'status': 'error', 'message': 'Failed to update bid'}), 500
            
    except Exception as e:
        logger.error(f"Error placing bid: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Payment API endpoints
@app.route('/api/payments', methods=['GET'])
def get_payments():
    try:
        payments = list(payments_collection.find())
        return jsonify([Payment.from_dict(payment).to_dict() for payment in payments])
    except Exception as e:
        logger.error(f"Error getting payments: {str(e)}")
        return jsonify([])

@app.route('/api/payments', methods=['POST'])
def create_payment():
    try:
        data = request.get_json()
        
        # Validate payment data
        required_fields = ['amount', 'payment_method', 'order_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }), 400
        
        # Create payment object
        payment = Payment(
            amount=float(data['amount']),
            payment_method=data['payment_method'],
            order_type=data['order_type'],
            order_id=data.get('order_id'),
            status='pending'
        )
        
        # Process payment (mock)
        payment.process_payment()
        
        # Save to database
        result = payments_collection.insert_one(payment.to_dict())
        payment.id = str(result.inserted_id)
        
        return jsonify({
            "status": "success",
            "message": "Payment processed successfully",
            "data": payment.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error processing payment: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
