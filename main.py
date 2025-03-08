
from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import logging
from datetime import datetime, timedelta
from bson import ObjectId
from app import app, mongo, events_collection, services_collection, packages_collection, auctions_collection, payments_collection
from models.event import Event
from models.service import Service
from models.package import Package
from models.auction import Auction
from models.payment import Payment

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_pages(path):
    return send_from_directory('.', path)

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
            participants=int(data.get('participants', 0)),
            requirements=data.get('requirements')
        )

        # Store event in database
        event.save(events_collection)

        logger.info(f"Successfully saved event: {event.to_dict()}")

        return jsonify({
            "status": "success",
            "message": "Event customization request received",
            "data": event.to_dict()
        })

    except Exception as e:
        logger.error(f"Error processing event request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/api/events', methods=['GET'])
def get_events():
    """Endpoint to retrieve all events"""
    all_events = list(events_collection.find())
    events = [Event.from_dict(event).to_dict() for event in all_events]
    return jsonify({
        "status": "success",
        "data": events
    })

# Services API endpoints
@app.route('/api/services', methods=['GET'])
def get_services():
    """Endpoint to retrieve all services"""
    all_services = list(services_collection.find())
    services = [Service.from_dict(service).to_dict() for service in all_services]
    return jsonify({
        "status": "success",
        "data": services
    })

@app.route('/api/services', methods=['POST'])
def add_service():
    """Endpoint to add a new service"""
    try:
        data = request.get_json()
        service = Service(
            name=data.get('name'),
            description=data.get('description'),
            price=float(data.get('price')),
            category=data.get('category')
        )
        service.save(services_collection)
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
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os
import logging
from datetime import datetime
from bson.objectid import ObjectId

from app import app, mongo, events_collection, services_collection, packages_collection, auctions_collection, payments_collection
from models.event import Event
from models.service import Service
from models.package import Package
from models.auction import Auction
from models.payment import Payment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = app.logger

@app.route('/api/packages', methods=['GET'])
def get_packages():
    """Endpoint to retrieve all packages"""
    all_packages = list(packages_collection.find())
    packages = [Package.from_dict(package).to_dict() for package in all_packages]
    return jsonify({
        "status": "success",
        "data": packages
    })

@app.route('/api/packages', methods=['POST'])
def add_package():
    """Endpoint to add a new package"""
    try:
        data = request.get_json()
        package = Package(
            name=data.get('name'),
            description=data.get('description'),
            price=float(data.get('price')),
            features=data.get('features', [])
        )
        package.save(packages_collection)
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
    """Endpoint to retrieve all auctions"""
    all_auctions = list(auctions_collection.find())
    auctions = [Auction.from_dict(auction).to_dict() for auction in all_auctions]
    return jsonify({
        "status": "success",
        "data": auctions
    })

@app.route('/api/auctions', methods=['POST'])
def create_auction():
    """Endpoint to create a new auction"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'starting_price', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }), 400
        
        # Create new auction
        auction = Auction(
            title=data['title'],
            description=data['description'],
            starting_price=float(data['starting_price']),
            current_price=float(data['starting_price']),
            end_date=datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        )
        
        auction.save(auctions_collection)
        
        return jsonify({
            "status": "success",
            "message": "Auction created successfully",
            "data": auction.to_dict()
        })
        
    except Exception as e:
        app.logger.error(f"Error creating auction: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/auctions/<auction_id>/bid', methods=['POST'])
def place_bid(auction_id):
    """Endpoint to place a bid on an auction"""
    try:
        data = request.get_json()
        
        # Validate bid amount
        if 'bid_amount' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing bid amount"
            }), 400
        
        bid_amount = float(data['bid_amount'])
        
        # Find auction
        auction_data = auctions_collection.find_one({"_id": ObjectId(auction_id)})
        if not auction_data:
            return jsonify({
                "status": "error",
                "message": "Auction not found"
            }), 404
        
        auction = Auction.from_dict(auction_data)
        
        # Check if auction is active
        if auction.status != "active" or auction.end_date < datetime.utcnow():
            return jsonify({
                "status": "error",
                "message": "Auction is closed"
            }), 400
        
        # Check if bid is higher than current price
        if bid_amount <= auction.current_price:
            return jsonify({
                "status": "error",
                "message": "Bid must be higher than current price"
            }), 400
        
        # Update auction with new bid
        auction.current_price = bid_amount
        auction.save(auctions_collection)
        
        return jsonify({
            "status": "success",
            "message": "Bid placed successfully",
            "data": auction.to_dict()
        })
        
    except Exception as e:
        app.logger.error(f"Error placing bid: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
def add_auction():
    """Endpoint to add a new auction"""
    try:
        data = request.get_json()
        
        # Parse end date
        end_date = None
        if data.get('end_date'):
            try:
                end_date = datetime.fromisoformat(data.get('end_date').replace('Z', '+00:00'))
            except ValueError:
                end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d')
        else:
            # Default to 7 days from now
            end_date = datetime.utcnow() + timedelta(days=7)
        
        starting_price = float(data.get('starting_price', 0))
        
        auction = Auction(
            title=data.get('title'),
            description=data.get('description'),
            starting_price=starting_price,
            current_price=starting_price,  # Initially same as starting price
            end_date=end_date,
            status="active"
        )
        auction.save(auctions_collection)
        return jsonify({
            "status": "success",
            "message": "Auction added successfully",
            "data": auction.to_dict()
        })
    except Exception as e:
        logger.error(f"Error adding auction: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/api/auctions/<auction_id>/bid', methods=['POST'])
def place_bid(auction_id):
    """Endpoint to place a bid on an auction"""
    try:
        data = request.get_json()
        bid_amount = float(data.get('bid_amount', 0))
        
        # Find the auction
        auction_data = auctions_collection.find_one({'_id': ObjectId(auction_id)})
        
        if not auction_data:
            return jsonify({
                "status": "error",
                "message": "Auction not found"
            }), 404
            
        auction = Auction.from_dict(auction_data)
        
        # Check if auction is active
        if auction.status != "active":
            return jsonify({
                "status": "error",
                "message": f"Auction is {auction.status}, not accepting bids"
            }), 400
            
        # Check if bid is higher than current price
        if bid_amount <= auction.current_price:
            return jsonify({
                "status": "error",
                "message": f"Bid must be higher than current price of {auction.current_price}"
            }), 400
            
        # Update the current price
        auction.current_price = bid_amount
        auction.save(auctions_collection)
        
        return jsonify({
            "status": "success",
            "message": "Bid placed successfully",
            "data": auction.to_dict()
        })
    except Exception as e:
        logger.error(f"Error placing bid: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

# Payment API endpoints
@app.route('/api/payments', methods=['GET'])
def get_payments():
    """Endpoint to retrieve all payments"""
    all_payments = list(payments_collection.find())
    payments = [Payment.from_dict(payment).to_dict() for payment in all_payments]
    return jsonify({
        "status": "success",
        "data": payments
    })

@app.route('/api/payments', methods=['POST'])
def add_payment():
    """Endpoint to add a new payment"""
    try:
        data = request.get_json()
        payment = Payment(
            amount=float(data.get('amount')),
            payment_method=data.get('payment_method'),
            status=data.get('status', 'pending'),
            event_id=data.get('event_id'),
            service_ids=data.get('service_ids', []),
            package_id=data.get('package_id'),
            auction_id=data.get('auction_id'),
            user_info=data.get('user_info', {})
        )
        payment.save(payments_collection)
        return jsonify({
            "status": "success",
            "message": "Payment recorded successfully",
            "data": payment.to_dict()
        })
    except Exception as e:
        logger.error(f"Error recording payment: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
