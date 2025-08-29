# PUT route for updating chimney support connection

from flask import Blueprint, request, jsonify, current_app, send_file, make_response
from app import db
from app.models import (
    User, Inspector, Company, Inspection, ChimneySpecification, FireplaceSpecification,
    CombustibleMaterials, HearthFloorProtection, EnclosureVentilation, FireplaceSafetyFeatures,
    ChimneySupportConnection, AtticRadiationProtection, RoofExteriorProtection, ChimneyHeightClearance,
    FireCodesCompliance, ReportDetails, FireplaceInsertChimneySpecification, FireplaceInsertFireplaceSpecification,
    FireplaceInsertMaterialsClearances, FireplaceInsertEmberPadFloorProtection, FireplaceInsertChimneySupportConnection,
    FireplaceInsertFireplaceSafetyFeatures, FireplaceInsertLinerApplianceChecks, FireplaceInsertApplianceMasonryChecks,
    FireplaceInsertCOAlarmsLiners, FireplaceInsertChimneyLinerJointsDetails, FireplaceInsertHearthSupport,
    FireplaceInsertClearances, FireplaceInsertClearancesLiners, FireplaceInsertLinerDetails, FireplaceInsertJointsDetails,
    FireplaceInsertChimneyHeightClearance, FireplaceInsertChimneySupports, FireplaceInsertChimneySaddlesFireCode,
    MasonryChimneySpecification, MasonryFireplaceSpecification, MasonryFireplaceConstructionDetails,
    MasonryCombustionAirRequirements, MasonryChimneyStructure, MasonryHearthConstruction, MasonryFireplaceComponents,
    MasonryFireplaceClearances, MasonryChimneyLinersInstallation, MasonryJointDetails, MasonryChimneyStabilityCaps,
    MasonryClearancesSupports, MasonryChimneySaddlesFireCode, MasonryCOAlarms, PelletInsertChimneyLiners, PelletInsertChimneySaddlesFireCode, PelletInsertChimneySpecification, PelletInsertChimneyStabilityCaps, PelletInsertChimneySupportConnection, PelletInsertChimneySupports, PelletInsertCOAlarmsLiners, PelletInsertEmberPadFloorProtection, PelletInsertFireplaceSafetyFeatures, PelletInsertFireplaceSpecifications, PelletInsertLinerApplianceChecks1, PelletInsertLinerApplianceChecks2, PelletInsertLinerVentComponents, PelletInsertMasonryFireplaceConstruction1, PelletInsertMasonryFireplaceConstruction2, PelletInsertMaterialsClearances, PelletInsertChimneyJointsLinerDetails,
    WoodStoveManufacturedChimneyComponentsSupports, WoodStoveManufacturedChimneyInspection, WoodStoveManufacturedChimneyStructureClearances, WoodStoveManufacturedClearancesShielding, WoodStoveManufacturedCombustionAirCOAlarm, WoodStoveManufacturedEmberPadFloorProtection, WoodStoveManufacturedFireCodesCompliance, WoodStoveManufacturedFluePipeChimneyConnection, WoodStoveManufacturedFluePipeComponents, WoodStoveManufacturedFluePipeInfoClearances, WoodStoveManufacturedFluePipeOrientationJoints,
    WoodStoveMasonryChimneyConstructionLiners, WoodStoveMasonryChimneyLinersInstallation, WoodStoveMasonryChimneyLiners, WoodStoveMasonryChimneyConstruction, WoodStoveMasonryChimneySaddles, WoodStoveMasonryChimneySpecifications, WoodStoveMasonryChimneyStabilityCaps, WoodStoveMasonryChimneySupports, WoodStoveMasonryClearancesShielding, WoodStoveMasonryCombustibleMaterials, WoodStoveMasonryEmberPadFloorProtection, WoodStoveMasonryFireplaceSpecifications, WoodStoveMasonryFluePipeOrientationJoints1, WoodStoveMasonryFluePipeOrientationJoints2, WoodStoveMasonryFluePipesConnections1, WoodStoveMasonryFluePipesConnections2, WoodStoveMasonryWallShieldingFloorProtection
)
from datetime import datetime
import base64
import io
import json
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from PIL import Image as PILImage
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from app import mail

main = Blueprint('main', __name__)
@main.route('/api/chimney-support-connection/<int:inspection_id>', methods=['PUT'])
def update_chimney_support_connection(inspection_id):
    """Update chimney support connection for an inspection"""
    data = request.get_json()
    try:
        chimney_support_connection = ChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_support_connection:
            return jsonify({'error': 'Chimney support connection not found'}), 404
        # Update fields from data
        for key, value in data.items():
            if hasattr(chimney_support_connection, key):
                setattr(chimney_support_connection, key, value)
        db.session.commit()
        return jsonify(chimney_support_connection.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET route for chimney support connection
@main.route('/api/chimney-support-connection/<int:inspection_id>', methods=['GET'])
def get_chimney_support_connection(inspection_id):
    """Get chimney support connection for an inspection"""
    try:
        chimney_support_connection = ChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_support_connection:
            return jsonify({'error': 'Chimney support connection not found'}), 404
        return jsonify(chimney_support_connection.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@main.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SHF Inspection App - Support</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f7;
                color: #1d1d1f;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            h1 {
                color: #1d1d1f;
                border-bottom: 3px solid #007aff;
                padding-bottom: 10px;
                margin-bottom: 30px;
            }
            h2 {
                color: #1d1d1f;
                margin-top: 30px;
                margin-bottom: 15px;
            }
            .contact-info {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }
            .contact-item {
                margin: 10px 0;
                display: flex;
                align-items: center;
            }
            .contact-item strong {
                min-width: 100px;
                display: inline-block;
            }
            a {
                color: #007aff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .app-info {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
            }
            .footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #e5e5e7;
                font-size: 14px;
                color: #86868b;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>SHF Inspection App - Support</h1>
            
            <div class="app-info">
                <h2>About the App</h2>
                <p>SHF Inspection App is a professional tool designed for certified WETT inspectors to conduct comprehensive solid fuel heating system inspections. The app helps create detailed inspection reports for chimneys, fireplaces, and wood-burning systems.</p>
            </div>

            <h2>Need Help?</h2>
            <p>We're here to help you get the most out of the SHF Inspection App. Below you'll find various ways to get support and answers to your questions.</p>

            <div class="contact-info">
                <h3>Contact Information</h3>
                <div class="contact-item">
                    <strong>Email:</strong> <a href="mailto:support@shfinspection.me">support@shfinspection.me</a>
                </div>
                <div class="contact-item">
                    <strong>Response Time:</strong> We typically respond within 24 hours during business days
                </div>
                <div class="contact-item">
                    <strong>Business Hours:</strong> Monday - Friday, 9:00 AM - 5:00 PM EST
                </div>
            </div>

            <h2>Frequently Asked Questions</h2>
            
            <h3>How do I create my first inspection report?</h3>
            <p>After logging in, tap the "New Inspection" button and fill out the required information including client details, inspection date, and form type. The app will guide you through each section of the inspection process.</p>

            <h3>Can I edit a report after it's been created?</h3>
            <p>Yes, you can edit inspection reports that are in "Draft" status. Once a report is finalized and sent to the client, it cannot be modified to maintain integrity of the inspection record.</p>

            <h3>How do I export or share my inspection reports?</h3>
            <p>Completed reports can be exported as PDF files and shared via email directly from the app. You can also save reports to your device's file system.</p>

            <h3>Is my data secure?</h3>
            <p>Yes, all inspection data is encrypted and securely stored. We follow industry best practices for data protection and comply with applicable privacy regulations.</p>

            <h3>Do I need an internet connection to use the app?</h3>
            <p>While the app can work offline for creating and editing reports, an internet connection is required for syncing data, user authentication, and sending reports.</p>

            <h2>Technical Support</h2>
            <p>If you're experiencing technical issues with the app, please include the following information when contacting support:</p>
            <ul>
                <li>Device model and operating system version</li>
                <li>App version number</li>
                <li>Description of the issue and steps to reproduce it</li>
                <li>Any error messages you're seeing</li>
            </ul>

            <h2>Feature Requests</h2>
            <p>We value your feedback! If you have suggestions for new features or improvements, please send them to <a href="mailto:feedback@shfinspection.me">feedback@shfinspection.me</a>.</p>

            <h2>Training and Resources</h2>
            <p>For WETT certification information and training resources, please visit the official WETT website at <a href="https://www.wettinc.ca" target="_blank">www.wettinc.ca</a>.</p>

            <div class="footer">
                <p>&copy; 2025 SHF Inspection App. All rights reserved.</p>
                <p>This app is designed for use by certified WETT inspectors only.</p>
            </div>
        </div>
    </body>
    </html>
    '''

@main.route('/health')
def health():
    return {'status': 'healthy', 'message': 'Flask app is running'}

# User Management Routes
@main.route('/api/users', methods=['POST'])
def create_or_update_user():
    """Create or update a user"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
        
        email = data['email']
        clerk_user_id = data.get('clerk_user_id')
        password_hash = data.get('password_hash')
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Update existing user
            if clerk_user_id:
                user.clerk_user_id = clerk_user_id
            if password_hash:
                user.password_hash = password_hash
            user.updated_at = datetime.utcnow()
        else:
            # Create new user
            user = User(
                email=email,
                clerk_user_id=clerk_user_id,
                password_hash=password_hash
            )
            db.session.add(user)
        
        db.session.commit()
        return jsonify(user.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/users/<email>', methods=['GET'])
def get_user(email):
    """Get user by email"""
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Include related data
        user_data = user.to_dict()
        if user.inspector:
            user_data['inspector'] = user.inspector.to_dict()
        if user.company:
            user_data['company'] = user.company.to_dict()
            
        return jsonify(user_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/users/<email>/complete-profile', methods=['GET'])
def get_complete_profile(email):
    """Get complete user profile including inspector and company details"""
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if user has complete profile
        if not user.inspector or not user.company:
            return jsonify({'error': 'Incomplete profile'}), 404
        
        profile_data = {
            'user': user.to_dict(),
            'inspector': user.inspector.to_dict(),
            'company': user.company.to_dict()
        }
        
        return jsonify(profile_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Inspector Details Routes
@main.route('/api/inspector', methods=['POST'])
def create_or_update_inspector():
    """Create or update inspector details"""
    try:
        data = request.get_json()
        
        required_fields = ['user_email', 'name', 'wett_number', 'province']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['user_email']).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if inspector exists
        inspector = Inspector.query.filter_by(user_id=user.id).first()
        
        if inspector:
            # Update existing inspector
            inspector.name = data['name']
            inspector.wett_number = data['wett_number']
            inspector.province = data['province']
            inspector.updated_at = datetime.utcnow()
        else:
            # Create new inspector
            inspector = Inspector(
                user_id=user.id,
                name=data['name'],
                wett_number=data['wett_number'],
                province=data['province']
            )
            db.session.add(inspector)
        
        db.session.commit()
        return jsonify(inspector.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Company Details Routes
@main.route('/api/company', methods=['POST'])
def create_or_update_company():
    """Create or update company details"""
    try:
        data = request.get_json()
        
        required_fields = ['user_email', 'company_name', 'address', 'company_email', 'phone']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['user_email']).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if company exists
        company = Company.query.filter_by(user_id=user.id).first()
        
        if company:
            # Update existing company
            company.company_name = data['company_name']
            company.address = data['address']
            company.website = data.get('website')
            company.company_email = data['company_email']
            company.phone = data['phone']
            company.logo = data.get('logo')
            company.updated_at = datetime.utcnow()
        else:
            # Create new company
            company = Company(
                user_id=user.id,
                company_name=data['company_name'],
                address=data['address'],
                website=data.get('website'),
                company_email=data['company_email'],
                phone=data['phone'],
                logo=data.get('logo')
            )
            db.session.add(company)
        
        db.session.commit()
        return jsonify(company.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Complete Profile Route
@main.route('/api/complete-profile', methods=['POST'])
def complete_profile():
    """Complete user profile with all details at once"""
    try:
        data = request.get_json()
        
        # Validate required data structure
        if not data or 'user' not in data or 'inspector' not in data or 'company' not in data:
            return jsonify({'error': 'Missing user, inspector, or company data'}), 400
        
        user_data = data['user']
        inspector_data = data['inspector']
        company_data = data['company']
        
        if 'email' not in user_data:
            return jsonify({'error': 'User email is required'}), 400
        
        email = user_data['email']
        
        # Find or create user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                clerk_user_id=user_data.get('clerk_user_id'),
                password_hash=user_data.get('password_hash')
            )
            db.session.add(user)
            db.session.flush()  # Get user ID
        
        # Create or update inspector
        inspector = Inspector.query.filter_by(user_id=user.id).first()
        if inspector:
            inspector.name = inspector_data['name']
            inspector.wett_number = inspector_data['wett_number']
            inspector.province = inspector_data['province']
            inspector.updated_at = datetime.utcnow()
        else:
            inspector = Inspector(
                user_id=user.id,
                name=inspector_data['name'],
                wett_number=inspector_data['wett_number'],
                province=inspector_data['province']
            )
            db.session.add(inspector)
        
        # Create or update company
        company = Company.query.filter_by(user_id=user.id).first()
        if company:
            company.company_name = company_data['company_name']
            company.address = company_data['address']
            company.website = company_data.get('website')
            company.company_email = company_data['company_email']
            company.phone = company_data['phone']
            company.logo = company_data.get('logo')
            company.updated_at = datetime.utcnow()
        else:
            company = Company(
                user_id=user.id,
                company_name=company_data['company_name'],
                address=company_data['address'],
                website=company_data.get('website'),
                company_email=company_data['company_email'],
                phone=company_data['phone'],
                logo=company_data.get('logo')
            )
            db.session.add(company)
        
        db.session.commit()
        
        # Return complete profile
        return jsonify({
            'user': user.to_dict(),
            'inspector': inspector.to_dict(),
            'company': company.to_dict(),
            'message': 'Profile completed successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Inspection Routes
@main.route('/api/inspections', methods=['POST'])
def create_inspection():
    """Create a new inspection"""
    try:
        data = request.get_json()
        
        required_fields = ['user_email', 'title']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['user_email']).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        inspection = Inspection(
            user_id=user.id,
            title=data['title'],
            form_type=data.get('form_type'),
            client_name=data.get('client_name'),
            client_address=data.get('client_address'),
            inspection_date=datetime.fromisoformat(data['inspection_date']) if data.get('inspection_date') else None,
            status=data.get('status', 'draft'),
            form_data=data.get('form_data')
        )
        
        db.session.add(inspection)
        db.session.commit()
        
        return jsonify(inspection.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/inspections/<int:inspection_id>', methods=['GET'])
def get_inspection(inspection_id):
    """Get a specific inspection by ID"""
    try:
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        return jsonify(inspection.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/inspections/<int:inspection_id>', methods=['PUT'])
def update_inspection(inspection_id):
    """Update an existing inspection"""
    try:
        data = request.get_json()
        print(f"Updating inspection {inspection_id} with data: {data}")
        
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            print(f"Inspection {inspection_id} not found in database")
            return jsonify({'error': 'Inspection form not found'}), 404
        
        print(f"Found inspection: {inspection.to_dict()}")
        
        # Update fields if provided
        if 'title' in data:
            inspection.title = data['title']
        if 'form_type' in data:
            inspection.form_type = data['form_type']
        if 'client_name' in data:
            inspection.client_name = data['client_name']
        if 'client_address' in data:
            inspection.client_address = data['client_address']
        if 'inspection_date' in data:
            inspection.inspection_date = datetime.fromisoformat(data['inspection_date']) if data['inspection_date'] else None
        if 'status' in data:
            inspection.status = data['status']
        if 'form_data' in data:
            inspection.form_data = data['form_data']
        
        inspection.updated_at = datetime.utcnow()
        db.session.commit()
        
        print(f"Updated inspection: {inspection.to_dict()}")
        return jsonify(inspection.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating inspection: {e}")
        return jsonify({'error': str(e)}), 500

@main.route('/api/inspections/<user_email>', methods=['GET'])
def get_user_inspections(user_email):
    """Get all inspections for a user"""
    try:
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        inspections = Inspection.query.filter_by(user_id=user.id).all()
        return jsonify([inspection.to_dict() for inspection in inspections]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Chimney Specification Routes
@main.route('/api/chimney-specifications', methods=['POST'])
def create_chimney_specification():
    """Create or update chimney specifications for an inspection"""
    try:
        data = request.get_json()
        
        if not data or 'inspection_id' not in data:
            return jsonify({'error': 'Inspection ID is required'}), 400
        
        inspection_id = data['inspection_id']
        
        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Check if chimney specification already exists for this inspection
        chimney_spec = ChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        
        if chimney_spec:
            # Update existing chimney specification
            chimney_spec.inspection_discussed = data.get('inspectionDiscussed')
            chimney_spec.building_permits = data.get('buildingPermits')
            chimney_spec.time_of_day = data.get('timeOfDay')
            chimney_spec.weather_conditions = data.get('weatherConditions')
            chimney_spec.roofing_type = data.get('roofingType')
            chimney_spec.roof_accessed = data.get('roofAccessed')
            chimney_spec.attic_accessed = data.get('atticAccessed')
            chimney_spec.chimney_make_model = data.get('chimneyMakeModel')
            chimney_spec.chimney_listed = data.get('chimneyListed')
            chimney_spec.flue_size = data.get('flueSize')
            chimney_spec.installation_manual = data.get('installationManual')
            chimney_spec.certification_standard = data.get('certificationStandard')
            chimney_spec.listing_agency = data.get('listingAgency')
            chimney_spec.comments = data.get('comments')
            chimney_spec.suitable = data.get('suitable')
            chimney_spec.installation = data.get('installation')
            chimney_spec.chimney_installed_by = data.get('chimneyInstalledBy')
            chimney_spec.inspection_date = data.get('date')
            chimney_spec.updated_at = datetime.utcnow()
        else:
            # Create new chimney specification
            chimney_spec = ChimneySpecification(
                inspection_id=inspection_id,
                inspection_discussed=data.get('inspectionDiscussed'),
                building_permits=data.get('buildingPermits'),
                time_of_day=data.get('timeOfDay'),
                weather_conditions=data.get('weatherConditions'),
                roofing_type=data.get('roofingType'),
                roof_accessed=data.get('roofAccessed'),
                attic_accessed=data.get('atticAccessed'),
                chimney_make_model=data.get('chimneyMakeModel'),
                chimney_listed=data.get('chimneyListed'),
                flue_size=data.get('flueSize'),
                installation_manual=data.get('installationManual'),
                certification_standard=data.get('certificationStandard'),
                listing_agency=data.get('listingAgency'),
                comments=data.get('comments'),
                suitable=data.get('suitable'),
                installation=data.get('installation'),
                chimney_installed_by=data.get('chimneyInstalledBy'),
                inspection_date=data.get('date')
            )
            db.session.add(chimney_spec)
        
        db.session.commit()
        return jsonify(chimney_spec.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/chimney-specifications/<int:inspection_id>', methods=['GET'])
def get_chimney_specification(inspection_id):
    """Get chimney specifications for an inspection"""
    try:
        chimney_spec = ChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_spec:
            return jsonify({'error': 'Chimney specifications not found'}), 404
        
        return jsonify(chimney_spec.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/chimney-specifications/<int:inspection_id>', methods=['PUT'])
def update_chimney_specification(inspection_id):
    """Update chimney specifications for an inspection"""
    try:
        data = request.get_json()
        
        chimney_spec = ChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_spec:
            return jsonify({'error': 'Chimney specifications not found'}), 404
        
        # Update fields if provided
        if 'inspectionDiscussed' in data:
            chimney_spec.inspection_discussed = data['inspectionDiscussed']
        if 'buildingPermits' in data:
            chimney_spec.building_permits = data['buildingPermits']
        if 'timeOfDay' in data:
            chimney_spec.time_of_day = data['timeOfDay']
        if 'weatherConditions' in data:
            chimney_spec.weather_conditions = data['weatherConditions']
        if 'roofingType' in data:
            chimney_spec.roofing_type = data['roofingType']
        if 'roofAccessed' in data:
            chimney_spec.roof_accessed = data['roofAccessed']
        if 'atticAccessed' in data:
            chimney_spec.attic_accessed = data['atticAccessed']
        if 'chimneyMakeModel' in data:
            chimney_spec.chimney_make_model = data['chimneyMakeModel']
        if 'chimneyListed' in data:
            chimney_spec.chimney_listed = data['chimneyListed']
        if 'flueSize' in data:
            chimney_spec.flue_size = data['flueSize']
        if 'installationManual' in data:
            chimney_spec.installation_manual = data['installationManual']
        if 'certificationStandard' in data:
            chimney_spec.certification_standard = data['certificationStandard']
        if 'listingAgency' in data:
            chimney_spec.listing_agency = data['listingAgency']
        if 'comments' in data:
            chimney_spec.comments = data['comments']
        if 'suitable' in data:
            chimney_spec.suitable = data['suitable']
        if 'installation' in data:
            chimney_spec.installation = data['installation']
        if 'chimneyInstalledBy' in data:
            chimney_spec.chimney_installed_by = data['chimneyInstalledBy']
        if 'date' in data:
            chimney_spec.inspection_date = data['date']
        
        chimney_spec.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(chimney_spec.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/chimney-specifications/<int:inspection_id>', methods=['DELETE'])
def delete_chimney_specification(inspection_id):
    """Delete chimney specifications for an inspection"""
    try:
        chimney_spec = ChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_spec:
            return jsonify({'error': 'Chimney specifications not found'}), 404
        
        db.session.delete(chimney_spec)
        db.session.commit()
        
        return jsonify({'message': 'Chimney specifications deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Specification Routes
@main.route('/api/fireplace-specifications', methods=['POST'])
def create_fireplace_specification():
    """Create or update fireplace specifications for an inspection"""
    try:
        data = request.get_json()
        
        if not data or 'inspection_id' not in data:
            return jsonify({'error': 'Inspection ID is required'}), 400
        
        inspection_id = data['inspection_id']
        
        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Check if fireplace specification already exists for this inspection
        fireplace_spec = FireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()
        
        if fireplace_spec:
            # Update existing fireplace specification
            fireplace_spec.fireplace_model_serial = data.get('fireplaceModelSerial')
            fireplace_spec.installation_manual = data.get('installationManual')
            fireplace_spec.listing_agency = data.get('listingAgency')
            fireplace_spec.certification_standard = data.get('certificationStandard')
            fireplace_spec.fan_blower_attached = data.get('fanBlowerAttached')
            fireplace_spec.comments = data.get('comments')
            fireplace_spec.suitable = data.get('suitable')
            fireplace_spec.mobile_home_approved = data.get('mobileHomeApproved')
            fireplace_spec.installed_in = data.get('installedIn')
            fireplace_spec.installed_in_other = data.get('installedInOther')
            fireplace_spec.appliance_location = data.get('applianceLocation')
            fireplace_spec.appliance_location_other = data.get('applianceLocationOther')
            fireplace_spec.appliance_installed_by = data.get('applianceInstalledBy')
            fireplace_spec.inspection_date = data.get('date')
            fireplace_spec.updated_at = datetime.utcnow()
        else:
            # Create new fireplace specification
            fireplace_spec = FireplaceSpecification(
                inspection_id=inspection_id,
                fireplace_model_serial=data.get('fireplaceModelSerial'),
                installation_manual=data.get('installationManual'),
                listing_agency=data.get('listingAgency'),
                certification_standard=data.get('certificationStandard'),
                fan_blower_attached=data.get('fanBlowerAttached'),
                comments=data.get('comments'),
                suitable=data.get('suitable'),
                mobile_home_approved=data.get('mobileHomeApproved'),
                installed_in=data.get('installedIn'),
                installed_in_other=data.get('installedInOther'),
                appliance_location=data.get('applianceLocation'),
                appliance_location_other=data.get('applianceLocationOther'),
                appliance_installed_by=data.get('applianceInstalledBy'),
                inspection_date=data.get('date')
            )
            db.session.add(fireplace_spec)
        
        db.session.commit()
        return jsonify(fireplace_spec.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-specifications/<int:inspection_id>', methods=['GET'])
def get_fireplace_specification(inspection_id):
    """Get fireplace specifications for an inspection"""
    try:
        fireplace_spec = FireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()
        if not fireplace_spec:
            return jsonify({'error': 'Fireplace specifications not found'}), 404
        
        return jsonify(fireplace_spec.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-specifications/<int:inspection_id>', methods=['PUT'])
def update_fireplace_specification(inspection_id):
    """Update fireplace specifications for an inspection"""
    try:
        data = request.get_json()
        
        fireplace_spec = FireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()
        if not fireplace_spec:
            return jsonify({'error': 'Fireplace specifications not found'}), 404
        
        # Update fields if provided
        if 'fireplaceModelSerial' in data:
            fireplace_spec.fireplace_model_serial = data['fireplaceModelSerial']
        if 'installationManual' in data:
            fireplace_spec.installation_manual = data['installationManual']
        if 'listingAgency' in data:
            fireplace_spec.listing_agency = data['listingAgency']
        if 'certificationStandard' in data:
            fireplace_spec.certification_standard = data['certificationStandard']
        if 'fanBlowerAttached' in data:
            fireplace_spec.fan_blower_attached = data['fanBlowerAttached']
        if 'comments' in data:
            fireplace_spec.comments = data['comments']
        if 'suitable' in data:
            fireplace_spec.suitable = data['suitable']
        if 'mobileHomeApproved' in data:
            fireplace_spec.mobile_home_approved = data['mobileHomeApproved']
        if 'installedIn' in data:
            fireplace_spec.installed_in = data['installedIn']
        if 'installedInOther' in data:
            fireplace_spec.installed_in_other = data['installedInOther']
        if 'applianceLocation' in data:
            fireplace_spec.appliance_location = data['applianceLocation']
        if 'applianceLocationOther' in data:
            fireplace_spec.appliance_location_other = data['applianceLocationOther']
        if 'applianceInstalledBy' in data:
            fireplace_spec.appliance_installed_by = data['applianceInstalledBy']
        if 'date' in data:
            fireplace_spec.inspection_date = data['date']
        
        fireplace_spec.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(fireplace_spec.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-specifications/<int:inspection_id>', methods=['DELETE'])
def delete_fireplace_specification(inspection_id):
    """Delete fireplace specifications for an inspection"""
    try:
        fireplace_spec = FireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()
        if not fireplace_spec:
            return jsonify({'error': 'Fireplace specifications not found'}), 404
        
        db.session.delete(fireplace_spec)
        db.session.commit()
        
        return jsonify({'message': 'Fireplace specifications deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Combustible Materials Routes
@main.route('/api/combustible-materials', methods=['POST'])
def create_combustible_materials():
    """Create or update combustible materials for an inspection"""
    try:
        data = request.get_json()
        
        if not data or 'inspection_id' not in data:
            return jsonify({'error': 'Inspection ID is required'}), 400
        
        inspection_id = data['inspection_id']
        
        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Check if combustible materials already exists for this inspection
        combustible_materials = CombustibleMaterials.query.filter_by(inspection_id=inspection_id).first()
        
        if combustible_materials:
            # Update existing combustible materials
            # Material Clearances
            combustible_materials.material_clearances_required = data.get('materialClearances', {}).get('requiredValue')
            combustible_materials.material_clearances_present = data.get('materialClearances', {}).get('presentValue')
            combustible_materials.material_clearances_compliance = data.get('materialClearances', {}).get('codeCompliance')
            combustible_materials.material_clearances_photos = data.get('materialClearances', {}).get('photos')
            
            # Right Side Legs
            combustible_materials.right_side_legs_required = data.get('rightSideLegs', {}).get('requiredValue')
            combustible_materials.right_side_legs_present = data.get('rightSideLegs', {}).get('presentValue')
            combustible_materials.right_side_legs_compliance = data.get('rightSideLegs', {}).get('codeCompliance')
            combustible_materials.right_side_legs_photos = data.get('rightSideLegs', {}).get('photos')
            
            # Left Side Legs
            combustible_materials.left_side_legs_required = data.get('leftSideLegs', {}).get('requiredValue')
            combustible_materials.left_side_legs_present = data.get('leftSideLegs', {}).get('presentValue')
            combustible_materials.left_side_legs_compliance = data.get('leftSideLegs', {}).get('codeCompliance')
            combustible_materials.left_side_legs_photos = data.get('leftSideLegs', {}).get('photos')
            
            # Combustible Facing
            combustible_materials.combustible_facing_required = data.get('combustibleFacing', {}).get('requiredValue')
            combustible_materials.combustible_facing_present = data.get('combustibleFacing', {}).get('presentValue')
            combustible_materials.combustible_facing_compliance = data.get('combustibleFacing', {}).get('codeCompliance')
            combustible_materials.combustible_facing_photos = data.get('combustibleFacing', {}).get('photos')
            
            # Combustible Side Wall
            combustible_materials.combustible_side_wall_required = data.get('combustibleSideWall', {}).get('requiredValue')
            combustible_materials.combustible_side_wall_present = data.get('combustibleSideWall', {}).get('presentValue')
            combustible_materials.combustible_side_wall_compliance = data.get('combustibleSideWall', {}).get('codeCompliance')
            combustible_materials.combustible_side_wall_photos = data.get('combustibleSideWall', {}).get('photos')
            
            # Fireplace Beavers
            combustible_materials.fireplace_beaver_required = data.get('fireplaceBeaver', {}).get('requiredValue')
            combustible_materials.fireplace_beaver_present = data.get('fireplaceBeaver', {}).get('presentValue')
            combustible_materials.fireplace_beaver_compliance = data.get('fireplaceBeaver', {}).get('codeCompliance')
            combustible_materials.fireplace_beaver_photos = data.get('fireplaceBeaver', {}).get('photos')
            
            combustible_materials.updated_at = datetime.utcnow()
        else:
            # Create new combustible materials
            combustible_materials = CombustibleMaterials(
                inspection_id=inspection_id,
                # Material Clearances
                material_clearances_required=data.get('materialClearances', {}).get('requiredValue'),
                material_clearances_present=data.get('materialClearances', {}).get('presentValue'),
                material_clearances_compliance=data.get('materialClearances', {}).get('codeCompliance'),
                material_clearances_photos=data.get('materialClearances', {}).get('photos'),
                # Right Side Logs
                right_side_logs_required=data.get('rightSideLogs', {}).get('requiredValue'),
                right_side_logs_present=data.get('rightSideLogs', {}).get('presentValue'),
                right_side_logs_compliance=data.get('rightSideLogs', {}).get('codeCompliance'),
                right_side_logs_photos=data.get('rightSideLogs', {}).get('photos'),
                # Left Side Logs
                left_side_logs_required=data.get('leftSideLogs', {}).get('requiredValue'),
                left_side_logs_present=data.get('leftSideLogs', {}).get('presentValue'),
                left_side_logs_compliance=data.get('leftSideLogs', {}).get('codeCompliance'),
                left_side_logs_photos=data.get('leftSideLogs', {}).get('photos'),
                # Combustible Facing
                combustible_facing_required=data.get('combustibleFacing', {}).get('requiredValue'),
                combustible_facing_present=data.get('combustibleFacing', {}).get('presentValue'),
                combustible_facing_compliance=data.get('combustibleFacing', {}).get('codeCompliance'),
                combustible_facing_photos=data.get('combustibleFacing', {}).get('photos'),
                # Combustible Side Wall
                combustible_side_wall_required=data.get('combustibleSideWall', {}).get('requiredValue'),
                combustible_side_wall_present=data.get('combustibleSideWall', {}).get('presentValue'),
                combustible_side_wall_compliance=data.get('combustibleSideWall', {}).get('codeCompliance'),
                combustible_side_wall_photos=data.get('combustibleSideWall', {}).get('photos'),
                # Fireplace Beavers
                fireplace_beaver_required=data.get('fireplaceBeaver', {}).get('requiredValue'),
                fireplace_beaver_present=data.get('fireplaceBeaver', {}).get('presentValue'),
                fireplace_beaver_compliance=data.get('fireplaceBeaver', {}).get('codeCompliance'),
                fireplace_beaver_photos=data.get('fireplaceBeaver', {}).get('photos')
            )
            db.session.add(combustible_materials)
        
        db.session.commit()
        return jsonify(combustible_materials.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/combustible-materials/<int:inspection_id>', methods=['GET'])
def get_combustible_materials(inspection_id):
    """Get combustible materials for an inspection"""
    try:
        combustible_materials = CombustibleMaterials.query.filter_by(inspection_id=inspection_id).first()
        if not combustible_materials:
            return jsonify({'error': 'Combustible materials not found'}), 404
        
        return jsonify(combustible_materials.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/combustible-materials/<int:inspection_id>', methods=['PUT'])
def update_combustible_materials(inspection_id):
    """Update combustible materials for an inspection"""
    try:
        data = request.get_json()
        
        combustible_materials = CombustibleMaterials.query.filter_by(inspection_id=inspection_id).first()
        if not combustible_materials:
            return jsonify({'error': 'Combustible materials not found'}), 404
        
        # Update Material Clearances
        if 'materialClearances' in data:
            material_clearances = data['materialClearances']
            combustible_materials.material_clearances_required = material_clearances.get('requiredValue')
            combustible_materials.material_clearances_present = material_clearances.get('presentValue')
            combustible_materials.material_clearances_compliance = material_clearances.get('codeCompliance')
            combustible_materials.material_clearances_photos = material_clearances.get('photos')
        
        # Update Right Side Logs
        if 'rightSideLogs' in data:
            right_side_logs = data['rightSideLogs']
            combustible_materials.right_side_logs_required = right_side_logs.get('requiredValue')
            combustible_materials.right_side_logs_present = right_side_logs.get('presentValue')
            combustible_materials.right_side_logs_compliance = right_side_logs.get('codeCompliance')
            combustible_materials.right_side_logs_photos = right_side_logs.get('photos')
        
        # Update Left Side Logs
        if 'leftSideLogs' in data:
            left_side_logs = data['leftSideLogs']
            combustible_materials.left_side_logs_required = left_side_logs.get('requiredValue')
            combustible_materials.left_side_logs_present = left_side_logs.get('presentValue')
            combustible_materials.left_side_logs_compliance = left_side_logs.get('codeCompliance')
            combustible_materials.left_side_logs_photos = left_side_logs.get('photos')
        
        # Update Combustible Facing
        if 'combustibleFacing' in data:
            combustible_facing = data['combustibleFacing']
            combustible_materials.combustible_facing_required = combustible_facing.get('requiredValue')
            combustible_materials.combustible_facing_present = combustible_facing.get('presentValue')
            combustible_materials.combustible_facing_compliance = combustible_facing.get('codeCompliance')
            combustible_materials.combustible_facing_photos = combustible_facing.get('photos')
        
        # Update Combustible Side Wall
        if 'combustibleSideWall' in data:
            combustible_side_wall = data['combustibleSideWall']
            combustible_materials.combustible_side_wall_required = combustible_side_wall.get('requiredValue')
            combustible_materials.combustible_side_wall_present = combustible_side_wall.get('presentValue')
            combustible_materials.combustible_side_wall_compliance = combustible_side_wall.get('codeCompliance')
            combustible_materials.combustible_side_wall_photos = combustible_side_wall.get('photos')
        
        # Update Fireplace Beavers
        if 'fireplaceBeaver' in data:
            fireplace_beaver = data['fireplaceBeaver']
            combustible_materials.fireplace_beaver_required = fireplace_beaver.get('requiredValue')
            combustible_materials.fireplace_beaver_present = fireplace_beaver.get('presentValue')
            combustible_materials.fireplace_beaver_compliance = fireplace_beaver.get('codeCompliance')
            combustible_materials.fireplace_beaver_photos = fireplace_beaver.get('photos')
        
        combustible_materials.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(combustible_materials.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/combustible-materials/<int:inspection_id>', methods=['DELETE'])
def delete_combustible_materials(inspection_id):
    """Delete combustible materials for an inspection"""
    try:
        combustible_materials = CombustibleMaterials.query.filter_by(inspection_id=inspection_id).first()
        if not combustible_materials:
            return jsonify({'error': 'Combustible materials not found'}), 404
        
        db.session.delete(combustible_materials)
        db.session.commit()
        
        return jsonify({'message': 'Combustible materials deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Hearth Floor Protection Routes
@main.route('/api/hearth-floor-protection', methods=['POST'])
def create_hearth_floor_protection():
    """Create or update hearth floor protection for an inspection"""
    try:
        data = request.get_json()
        
        if not data or 'inspection_id' not in data:
            return jsonify({'error': 'Inspection ID is required'}), 400
        
        inspection_id = data['inspection_id']
        
        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Check if hearth floor protection already exists for this inspection
        hearth_floor_protection = HearthFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        
        if hearth_floor_protection:
            # Update existing hearth floor protection
            # Ember Strip
            hearth_floor_protection.ember_strip_required = data.get('emberStrip', {}).get('requiredValue')
            hearth_floor_protection.ember_strip_present = data.get('emberStrip', {}).get('presentValue')
            hearth_floor_protection.ember_strip_compliance = data.get('emberStrip', {}).get('codeCompliance')
            hearth_floor_protection.ember_strip_photos = data.get('emberStrip', {}).get('photos')
            
            # Hearth Extension Front
            hearth_floor_protection.hearth_extension_front_required = data.get('hearthExtensionFront', {}).get('requiredValue')
            hearth_floor_protection.hearth_extension_front_present = data.get('hearthExtensionFront', {}).get('presentValue')
            hearth_floor_protection.hearth_extension_front_compliance = data.get('hearthExtensionFront', {}).get('codeCompliance')
            hearth_floor_protection.hearth_extension_front_photos = data.get('hearthExtensionFront', {}).get('photos')
            
            # Hearth Extension Right Side
            hearth_floor_protection.hearth_extension_right_required = data.get('hearthExtensionRightSide', {}).get('requiredValue')
            hearth_floor_protection.hearth_extension_right_present = data.get('hearthExtensionRightSide', {}).get('presentValue')
            hearth_floor_protection.hearth_extension_right_compliance = data.get('hearthExtensionRightSide', {}).get('codeCompliance')
            hearth_floor_protection.hearth_extension_right_photos = data.get('hearthExtensionRightSide', {}).get('photos')
            
            # Hearth Extension Left Side
            hearth_floor_protection.hearth_extension_left_required = data.get('hearthExtensionLeftSide', {}).get('requiredValue')
            hearth_floor_protection.hearth_extension_left_present = data.get('hearthExtensionLeftSide', {}).get('presentValue')
            hearth_floor_protection.hearth_extension_left_compliance = data.get('hearthExtensionLeftSide', {}).get('codeCompliance')
            hearth_floor_protection.hearth_extension_left_photos = data.get('hearthExtensionLeftSide', {}).get('photos')
            
            # Hearth Material
            hearth_floor_protection.hearth_material_required = data.get('hearthMaterial', {}).get('requiredValue')
            hearth_floor_protection.hearth_material_present = data.get('hearthMaterial', {}).get('presentValue')
            hearth_floor_protection.hearth_material_compliance = data.get('hearthMaterial', {}).get('codeCompliance')
            hearth_floor_protection.hearth_material_photos = data.get('hearthMaterial', {}).get('photos')
            
            # Floor Radiation Protection
            hearth_floor_protection.floor_radiation_protection_required = data.get('floorRadiationProtection', {}).get('requiredValue')
            hearth_floor_protection.floor_radiation_protection_present = data.get('floorRadiationProtection', {}).get('presentValue')
            hearth_floor_protection.floor_radiation_protection_compliance = data.get('floorRadiationProtection', {}).get('codeCompliance')
            hearth_floor_protection.floor_radiation_protection_photos = data.get('floorRadiationProtection', {}).get('photos')
            
            hearth_floor_protection.updated_at = datetime.utcnow()
        else:
            # Create new hearth floor protection
            hearth_floor_protection = HearthFloorProtection(
                inspection_id=inspection_id,
                # Ember Strip
                ember_strip_required=data.get('emberStrip', {}).get('requiredValue'),
                ember_strip_present=data.get('emberStrip', {}).get('presentValue'),
                ember_strip_compliance=data.get('emberStrip', {}).get('codeCompliance'),
                ember_strip_photos=data.get('emberStrip', {}).get('photos'),
                # Hearth Extension Front
                hearth_extension_front_required=data.get('hearthExtensionFront', {}).get('requiredValue'),
                hearth_extension_front_present=data.get('hearthExtensionFront', {}).get('presentValue'),
                hearth_extension_front_compliance=data.get('hearthExtensionFront', {}).get('codeCompliance'),
                hearth_extension_front_photos=data.get('hearthExtensionFront', {}).get('photos'),
                # Hearth Extension Right Side
                hearth_extension_right_required=data.get('hearthExtensionRightSide', {}).get('requiredValue'),
                hearth_extension_right_present=data.get('hearthExtensionRightSide', {}).get('presentValue'),
                hearth_extension_right_compliance=data.get('hearthExtensionRightSide', {}).get('codeCompliance'),
                hearth_extension_right_photos=data.get('hearthExtensionRightSide', {}).get('photos'),
                # Hearth Extension Left Side
                hearth_extension_left_required=data.get('hearthExtensionLeftSide', {}).get('requiredValue'),
                hearth_extension_left_present=data.get('hearthExtensionLeftSide', {}).get('presentValue'),
                hearth_extension_left_compliance=data.get('hearthExtensionLeftSide', {}).get('codeCompliance'),
                hearth_extension_left_photos=data.get('hearthExtensionLeftSide', {}).get('photos'),
                # Hearth Material
                hearth_material_required=data.get('hearthMaterial', {}).get('requiredValue'),
                hearth_material_present=data.get('hearthMaterial', {}).get('presentValue'),
                hearth_material_compliance=data.get('hearthMaterial', {}).get('codeCompliance'),
                hearth_material_photos=data.get('hearthMaterial', {}).get('photos'),
                # Floor Radiation Protection
                floor_radiation_protection_required=data.get('floorRadiationProtection', {}).get('requiredValue'),
                floor_radiation_protection_present=data.get('floorRadiationProtection', {}).get('presentValue'),
                floor_radiation_protection_compliance=data.get('floorRadiationProtection', {}).get('codeCompliance'),
                floor_radiation_protection_photos=data.get('floorRadiationProtection', {}).get('photos')
            )
            db.session.add(hearth_floor_protection)
        
        db.session.commit()
        return jsonify(hearth_floor_protection.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/hearth-floor-protection/<int:inspection_id>', methods=['GET'])
def get_hearth_floor_protection(inspection_id):
    """Get hearth floor protection for an inspection"""
    try:
        hearth_floor_protection = HearthFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not hearth_floor_protection:
            return jsonify({'error': 'Hearth floor protection not found'}), 404
        
        return jsonify(hearth_floor_protection.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/hearth-floor-protection/<int:inspection_id>', methods=['PUT'])
def update_hearth_floor_protection(inspection_id):
    """Update hearth floor protection for an inspection"""
    try:
        data = request.get_json()
        
        hearth_floor_protection = HearthFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not hearth_floor_protection:
            return jsonify({'error': 'Hearth floor protection not found'}), 404
        
        # Update Ember Strip
        if 'emberStrip' in data:
            ember_strip = data['emberStrip']
            hearth_floor_protection.ember_strip_required = ember_strip.get('requiredValue')
            hearth_floor_protection.ember_strip_present = ember_strip.get('presentValue')
            hearth_floor_protection.ember_strip_compliance = ember_strip.get('codeCompliance')
            hearth_floor_protection.ember_strip_photos = ember_strip.get('photos')
        
        # Update Hearth Extension Front
        if 'hearthExtensionFront' in data:
            hearth_extension_front = data['hearthExtensionFront']
            hearth_floor_protection.hearth_extension_front_required = hearth_extension_front.get('requiredValue')
            hearth_floor_protection.hearth_extension_front_present = hearth_extension_front.get('presentValue')
            hearth_floor_protection.hearth_extension_front_compliance = hearth_extension_front.get('codeCompliance')
            hearth_floor_protection.hearth_extension_front_photos = hearth_extension_front.get('photos')
        
        # Update Hearth Extension Right Side
        if 'hearthExtensionRightSide' in data:
            hearth_extension_right = data['hearthExtensionRightSide']
            hearth_floor_protection.hearth_extension_right_required = hearth_extension_right.get('requiredValue')
            hearth_floor_protection.hearth_extension_right_present = hearth_extension_right.get('presentValue')
            hearth_floor_protection.hearth_extension_right_compliance = hearth_extension_right.get('codeCompliance')
            hearth_floor_protection.hearth_extension_right_photos = hearth_extension_right.get('photos')
        
        # Update Hearth Extension Left Side
        if 'hearthExtensionLeftSide' in data:
            hearth_extension_left = data['hearthExtensionLeftSide']
            hearth_floor_protection.hearth_extension_left_required = hearth_extension_left.get('requiredValue')
            hearth_floor_protection.hearth_extension_left_present = hearth_extension_left.get('presentValue')
            hearth_floor_protection.hearth_extension_left_compliance = hearth_extension_left.get('codeCompliance')
            hearth_floor_protection.hearth_extension_left_photos = hearth_extension_left.get('photos')
        
        # Update Hearth Material
        if 'hearthMaterial' in data:
            hearth_material = data['hearthMaterial']
            hearth_floor_protection.hearth_material_required = hearth_material.get('requiredValue')
            hearth_floor_protection.hearth_material_present = hearth_material.get('presentValue')
            hearth_floor_protection.hearth_material_compliance = hearth_material.get('codeCompliance')
            hearth_floor_protection.hearth_material_photos = hearth_material.get('photos')
        
        # Update Floor Radiation Protection
        if 'floorRadiationProtection' in data:
            floor_radiation_protection = data['floorRadiationProtection']
            hearth_floor_protection.floor_radiation_protection_required = floor_radiation_protection.get('requiredValue')
            hearth_floor_protection.floor_radiation_protection_present = floor_radiation_protection.get('presentValue')
            hearth_floor_protection.floor_radiation_protection_compliance = floor_radiation_protection.get('codeCompliance')
            hearth_floor_protection.floor_radiation_protection_photos = floor_radiation_protection.get('photos')
        
        hearth_floor_protection.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(hearth_floor_protection.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/hearth-floor-protection/<int:inspection_id>', methods=['DELETE'])
def delete_hearth_floor_protection(inspection_id):
    """Delete hearth floor protection for an inspection"""
    try:
        hearth_floor_protection = HearthFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not hearth_floor_protection:
            return jsonify({'error': 'Hearth floor protection not found'}), 404
        
        db.session.delete(hearth_floor_protection)
        db.session.commit()
        
        return jsonify({'message': 'Hearth floor protection deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Enclosure Ventilation Routes
@main.route('/api/enclosure-ventilation', methods=['POST'])
def create_enclosure_ventilation():
    """Create or update enclosure ventilation for an inspection"""
    try:
        data = request.get_json()
        
        if not data or 'inspection_id' not in data:
            return jsonify({'error': 'Inspection ID is required'}), 400
        
        inspection_id = data['inspection_id']
        
        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Check if enclosure ventilation already exists for this inspection
        enclosure_ventilation = EnclosureVentilation.query.filter_by(inspection_id=inspection_id).first()
        
        if enclosure_ventilation:
            # Update existing enclosure ventilation
            # Ceiling Height
            enclosure_ventilation.ceiling_height_required = data.get('ceilingHeight', {}).get('requiredValue')
            enclosure_ventilation.ceiling_height_present = data.get('ceilingHeight', {}).get('presentValue')
            enclosure_ventilation.ceiling_height_compliance = data.get('ceilingHeight', {}).get('codeCompliance')
            enclosure_ventilation.ceiling_height_photos = data.get('ceilingHeight', {}).get('photos')
            
            # Fireplace Enclosured
            enclosure_ventilation.fireplace_enclosured_required = data.get('fireplaceEnclosured', {}).get('requiredValue')
            enclosure_ventilation.fireplace_enclosured_present = data.get('fireplaceEnclosured', {}).get('presentValue')
            enclosure_ventilation.fireplace_enclosured_compliance = data.get('fireplaceEnclosured', {}).get('codeCompliance')
            enclosure_ventilation.fireplace_enclosured_photos = data.get('fireplaceEnclosured', {}).get('photos')
            
            # Clearance Within Enclosure
            enclosure_ventilation.clearance_within_enclosure_required = data.get('clearanceWithinEnclosure', {}).get('requiredValue')
            enclosure_ventilation.clearance_within_enclosure_present = data.get('clearanceWithinEnclosure', {}).get('presentValue')
            enclosure_ventilation.clearance_within_enclosure_compliance = data.get('clearanceWithinEnclosure', {}).get('codeCompliance')
            enclosure_ventilation.clearance_within_enclosure_photos = data.get('clearanceWithinEnclosure', {}).get('photos')
            
            # Gravity Vent Clearance
            enclosure_ventilation.gravity_vent_clearance_required = data.get('gravityVentClearance', {}).get('requiredValue')
            enclosure_ventilation.gravity_vent_clearance_present = data.get('gravityVentClearance', {}).get('presentValue')
            enclosure_ventilation.gravity_vent_clearance_compliance = data.get('gravityVentClearance', {}).get('codeCompliance')
            enclosure_ventilation.gravity_vent_clearance_photos = data.get('gravityVentClearance', {}).get('photos')
            
            # Gravity Vent Grille Clearance
            enclosure_ventilation.gravity_vent_grille_clearance_required = data.get('gravityVentGrilleClearance', {}).get('requiredValue')
            enclosure_ventilation.gravity_vent_grille_clearance_present = data.get('gravityVentGrilleClearance', {}).get('presentValue')
            enclosure_ventilation.gravity_vent_grille_clearance_compliance = data.get('gravityVentGrilleClearance', {}).get('codeCompliance')
            enclosure_ventilation.gravity_vent_grille_clearance_photos = data.get('gravityVentGrilleClearance', {}).get('photos')
            
            # Hearth Materials (REMOVED - doubled question)
            # (No code for hearth materials, as per client WETT forms and Figma)
            
            # Central Heating Kit
            enclosure_ventilation.central_heating_kit_required = data.get('centralHeatingKit', {}).get('requiredValue')
            enclosure_ventilation.central_heating_kit_present = data.get('centralHeatingKit', {}).get('presentValue')
            enclosure_ventilation.central_heating_kit_compliance = data.get('centralHeatingKit', {}).get('codeCompliance')
            enclosure_ventilation.central_heating_kit_photos = data.get('centralHeatingKit', {}).get('photos')
            
            enclosure_ventilation.updated_at = datetime.utcnow()
        else:
            # Create new enclosure ventilation
            enclosure_ventilation = EnclosureVentilation(
                inspection_id=inspection_id,
                # Ceiling Height
                ceiling_height_required=data.get('ceilingHeight', {}).get('requiredValue'),
                ceiling_height_present=data.get('ceilingHeight', {}).get('presentValue'),
                ceiling_height_compliance=data.get('ceilingHeight', {}).get('codeCompliance'),
                ceiling_height_photos=data.get('ceilingHeight', {}).get('photos'),
                # Fireplace Enclosured
                fireplace_enclosured_required=data.get('fireplaceEnclosured', {}).get('requiredValue'),
                fireplace_enclosured_present=data.get('fireplaceEnclosured', {}).get('presentValue'),
                fireplace_enclosured_compliance=data.get('fireplaceEnclosured', {}).get('codeCompliance'),
                fireplace_enclosured_photos=data.get('fireplaceEnclosured', {}).get('photos'),
                # Clearance Within Enclosure
                clearance_within_enclosure_required=data.get('clearanceWithinEnclosure', {}).get('requiredValue'),
                clearance_within_enclosure_present=data.get('clearanceWithinEnclosure', {}).get('presentValue'),
                clearance_within_enclosure_compliance=data.get('clearanceWithinEnclosure', {}).get('codeCompliance'),
                clearance_within_enclosure_photos=data.get('clearanceWithinEnclosure', {}).get('photos'),
                # Gravity Vent Clearance
                gravity_vent_clearance_required=data.get('gravityVentClearance', {}).get('requiredValue'),
                gravity_vent_clearance_present=data.get('gravityVentClearance', {}).get('presentValue'),
                gravity_vent_clearance_compliance=data.get('gravityVentClearance', {}).get('codeCompliance'),
                gravity_vent_clearance_photos=data.get('gravityVentClearance', {}).get('photos'),
                # Gravity Vent Grille Clearance
                gravity_vent_grille_clearance_required=data.get('gravityVentGrilleClearance', {}).get('requiredValue'),
                gravity_vent_grille_clearance_present=data.get('gravityVentGrilleClearance', {}).get('presentValue'),
                gravity_vent_grille_clearance_compliance=data.get('gravityVentGrilleClearance', {}).get('codeCompliance'),
                gravity_vent_grille_clearance_photos=data.get('gravityVentGrilleClearance', {}).get('photos'),
                # Hearth Materials
                hearth_materials_required=data.get('hearthMaterials', {}).get('requiredValue'),
                hearth_materials_present=data.get('hearthMaterials', {}).get('presentValue'),
                hearth_materials_compliance=data.get('hearthMaterials', {}).get('codeCompliance'),
                hearth_materials_photos=data.get('hearthMaterials', {}).get('photos'),
                # Central Heating Kit
                central_heating_kit_required=data.get('centralHeatingKit', {}).get('requiredValue'),
                central_heating_kit_present=data.get('centralHeatingKit', {}).get('presentValue'),
                central_heating_kit_compliance=data.get('centralHeatingKit', {}).get('codeCompliance'),
                central_heating_kit_photos=data.get('centralHeatingKit', {}).get('photos')
            )
            db.session.add(enclosure_ventilation)
        
        db.session.commit()
        return jsonify(enclosure_ventilation.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/enclosure-ventilation/<int:inspection_id>', methods=['GET'])
def get_enclosure_ventilation(inspection_id):
    """Get enclosure ventilation for an inspection"""
    try:
        enclosure_ventilation = EnclosureVentilation.query.filter_by(inspection_id=inspection_id).first()
        if not enclosure_ventilation:
            return jsonify({'error': 'Enclosure ventilation not found'}), 404
        
        return jsonify(enclosure_ventilation.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/enclosure-ventilation/<int:inspection_id>', methods=['PUT'])
def update_enclosure_ventilation(inspection_id):
    """Update enclosure ventilation for an inspection"""
    try:
        data = request.get_json()
        
        enclosure_ventilation = EnclosureVentilation.query.filter_by(inspection_id=inspection_id).first()
        if not enclosure_ventilation:
            return jsonify({'error': 'Enclosure ventilation not found'}), 404
        
        # Update Ceiling Height
        if 'ceilingHeight' in data:
            ceiling_height = data['ceilingHeight']
            enclosure_ventilation.ceiling_height_required = ceiling_height.get('requiredValue')
            enclosure_ventilation.ceiling_height_present = ceiling_height.get('presentValue')
            enclosure_ventilation.ceiling_height_compliance = ceiling_height.get('codeCompliance')
            enclosure_ventilation.ceiling_height_photos = ceiling_height.get('photos')
        
        # Update Fireplace Enclosured
        if 'fireplaceEnclosured' in data:
            fireplace_enclosured = data['fireplaceEnclosured']
            enclosure_ventilation.fireplace_enclosured_required = fireplace_enclosured.get('requiredValue')
            enclosure_ventilation.fireplace_enclosured_present = fireplace_enclosured.get('presentValue')
            enclosure_ventilation.fireplace_enclosured_compliance = fireplace_enclosured.get('codeCompliance')
            enclosure_ventilation.fireplace_enclosured_photos = fireplace_enclosured.get('photos')
        
        # Update Clearance Within Enclosure
        if 'clearanceWithinEnclosure' in data:
            clearance_within_enclosure = data['clearanceWithinEnclosure']
            enclosure_ventilation.clearance_within_enclosure_required = clearance_within_enclosure.get('requiredValue')
            enclosure_ventilation.clearance_within_enclosure_present = clearance_within_enclosure.get('presentValue')
            enclosure_ventilation.clearance_within_enclosure_compliance = clearance_within_enclosure.get('codeCompliance')
            enclosure_ventilation.clearance_within_enclosure_photos = clearance_within_enclosure.get('photos')
        
        # Update Gravity Vent Clearance
        if 'gravityVentClearance' in data:
            gravity_vent_clearance = data['gravityVentClearance']
            enclosure_ventilation.gravity_vent_clearance_required = gravity_vent_clearance.get('requiredValue')
            enclosure_ventilation.gravity_vent_clearance_present = gravity_vent_clearance.get('presentValue')
            enclosure_ventilation.gravity_vent_clearance_compliance = gravity_vent_clearance.get('codeCompliance')
            enclosure_ventilation.gravity_vent_clearance_photos = gravity_vent_clearance.get('photos')
        
        # Update Gravity Vent Grille Clearance
        if 'gravityVentGrilleClearance' in data:
            gravity_vent_grille_clearance = data['gravityVentGrilleClearance']
            enclosure_ventilation.gravity_vent_grille_clearance_required = gravity_vent_grille_clearance.get('requiredValue')
            enclosure_ventilation.gravity_vent_grille_clearance_present = gravity_vent_grille_clearance.get('presentValue')
            enclosure_ventilation.gravity_vent_grille_clearance_compliance = gravity_vent_grille_clearance.get('codeCompliance')
            enclosure_ventilation.gravity_vent_grille_clearance_photos = gravity_vent_grille_clearance.get('photos')
        
        # Update Hearth Materials
        if 'hearthMaterials' in data:
            hearth_materials = data['hearthMaterials']
            enclosure_ventilation.hearth_materials_required = hearth_materials.get('requiredValue')
            enclosure_ventilation.hearth_materials_present = hearth_materials.get('presentValue')
            enclosure_ventilation.hearth_materials_compliance = hearth_materials.get('codeCompliance')
            enclosure_ventilation.hearth_materials_photos = hearth_materials.get('photos')
        
        # Update Central Heating Kit
        if 'centralHeatingKit' in data:
            central_heating_kit = data['centralHeatingKit']
            enclosure_ventilation.central_heating_kit_required = central_heating_kit.get('requiredValue')
            enclosure_ventilation.central_heating_kit_present = central_heating_kit.get('presentValue')
            enclosure_ventilation.central_heating_kit_compliance = central_heating_kit.get('codeCompliance')
            enclosure_ventilation.central_heating_kit_photos = central_heating_kit.get('photos')
        
        enclosure_ventilation.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(enclosure_ventilation.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/enclosure-ventilation/<int:inspection_id>', methods=['DELETE'])
def delete_enclosure_ventilation(inspection_id):
    """Delete enclosure ventilation for an inspection"""
    try:
        enclosure_ventilation = EnclosureVentilation.query.filter_by(inspection_id=inspection_id).first()
        if not enclosure_ventilation:
            return jsonify({'error': 'Enclosure ventilation not found'}), 404
        
        db.session.delete(enclosure_ventilation)
        db.session.commit()
        
        return jsonify({'message': 'Enclosure ventilation deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Safety Features Routes
@main.route('/api/fireplace-safety-features', methods=['POST'])
def create_fireplace_safety_features():
    """Create or update fireplace safety features for an inspection"""
    try:
        data = request.get_json()
        
        if not data or 'inspection_id' not in data:
            return jsonify({'error': 'Inspection ID is required'}), 400
        
        inspection_id = data['inspection_id']
        
        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Check if fireplace safety features already exists for this inspection
        fireplace_safety_features = FireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()
        
        if fireplace_safety_features:
            # Update existing fireplace safety features
            # Glass Doors
            fireplace_safety_features.glass_doors_required = data.get('glassDoors', {}).get('requiredValue')
            fireplace_safety_features.glass_doors_present = data.get('glassDoors', {}).get('presentValue')
            fireplace_safety_features.glass_doors_compliance = data.get('glassDoors', {}).get('codeCompliance')
            fireplace_safety_features.glass_doors_photos = data.get('glassDoors', {}).get('photos')
            
            # Fire Screen
            fireplace_safety_features.fire_screen_required = data.get('fireScreen', {}).get('requiredValue')
            fireplace_safety_features.fire_screen_present = data.get('fireScreen', {}).get('presentValue')
            fireplace_safety_features.fire_screen_compliance = data.get('fireScreen', {}).get('codeCompliance')
            fireplace_safety_features.fire_screen_photos = data.get('fireScreen', {}).get('photos')
            
            # Chase Framing Size
            fireplace_safety_features.chase_framing_size_required = data.get('chaseFramingSize', {}).get('requiredValue')
            fireplace_safety_features.chase_framing_size_present = data.get('chaseFramingSize', {}).get('presentValue')
            fireplace_safety_features.chase_framing_size_compliance = data.get('chaseFramingSize', {}).get('codeCompliance')
            fireplace_safety_features.chase_framing_size_photos = data.get('chaseFramingSize', {}).get('photos')
            
            # Chase Insulated (air/vapour barriered and drywall/sheathing)
            fireplace_safety_features.chase_insulated_required = data.get('chaseInsulated', {}).get('requiredValue')
            fireplace_safety_features.chase_insulated_present = data.get('chaseInsulated', {}).get('presentValue')
            fireplace_safety_features.chase_insulated_compliance = data.get('chaseInsulated', {}).get('codeCompliance')
            fireplace_safety_features.chase_insulated_photos = data.get('chaseInsulated', {}).get('photos')
            
            # Chase Clear of Debris
            fireplace_safety_features.chase_clear_of_debris_required = data.get('chaseClearOfDebris', {}).get('requiredValue')
            fireplace_safety_features.chase_clear_of_debris_present = data.get('chaseClearOfDebris', {}).get('presentValue')
            fireplace_safety_features.chase_clear_of_debris_compliance = data.get('chaseClearOfDebris', {}).get('codeCompliance')
            fireplace_safety_features.chase_clear_of_debris_photos = data.get('chaseClearOfDebris', {}).get('photos')
            
            # Outdoor Combustion Air
            fireplace_safety_features.outdoor_combustion_air_required = data.get('outdoorCombustionAir', {}).get('requiredValue')
            fireplace_safety_features.outdoor_combustion_air_present = data.get('outdoorCombustionAir', {}).get('presentValue')
            fireplace_safety_features.outdoor_combustion_air_compliance = data.get('outdoorCombustionAir', {}).get('codeCompliance')
            fireplace_safety_features.outdoor_combustion_air_photos = data.get('outdoorCombustionAir', {}).get('photos')
            
            fireplace_safety_features.updated_at = datetime.utcnow()
        else:
            # Create new fireplace safety features
            fireplace_safety_features = FireplaceSafetyFeatures(
                inspection_id=inspection_id,
                # Glass Doors
                glass_doors_required=data.get('glassDoors', {}).get('requiredValue'),
                glass_doors_present=data.get('glassDoors', {}).get('presentValue'),
                glass_doors_compliance=data.get('glassDoors', {}).get('codeCompliance'),
                glass_doors_photos=data.get('glassDoors', {}).get('photos'),
                # Fire Screen
                fire_screen_required=data.get('fireScreen', {}).get('requiredValue'),
                fire_screen_present=data.get('fireScreen', {}).get('presentValue'),
                fire_screen_compliance=data.get('fireScreen', {}).get('codeCompliance'),
                fire_screen_photos=data.get('fireScreen', {}).get('photos'),
                # Chase Framing Size
                chase_framing_size_required=data.get('chaseFramingSize', {}).get('requiredValue'),
                chase_framing_size_present=data.get('chaseFramingSize', {}).get('presentValue'),
                chase_framing_size_compliance=data.get('chaseFramingSize', {}).get('codeCompliance'),
                chase_framing_size_photos=data.get('chaseFramingSize', {}).get('photos'),
                # Chase Insulated
                chase_insulated_required=data.get('chaseInsulated', {}).get('requiredValue'),
                chase_insulated_present=data.get('chaseInsulated', {}).get('presentValue'),
                chase_insulated_compliance=data.get('chaseInsulated', {}).get('codeCompliance'),
                chase_insulated_photos=data.get('chaseInsulated', {}).get('photos'),
                # Chase Clear of Debris
                chase_clear_of_debris_required=data.get('chaseClearOfDebris', {}).get('requiredValue'),
                chase_clear_of_debris_present=data.get('chaseClearOfDebris', {}).get('presentValue'),
                chase_clear_of_debris_compliance=data.get('chaseClearOfDebris', {}).get('codeCompliance'),
                chase_clear_of_debris_photos=data.get('chaseClearOfDebris', {}).get('photos'),
                # Outdoor Combustion Air
                outdoor_combustion_air_required=data.get('outdoorCombustionAir', {}).get('requiredValue'),
                outdoor_combustion_air_present=data.get('outdoorCombustionAir', {}).get('presentValue'),
                outdoor_combustion_air_compliance=data.get('outdoorCombustionAir', {}).get('codeCompliance'),
                outdoor_combustion_air_photos=data.get('outdoorCombustionAir', {}).get('photos')
            )
            db.session.add(fireplace_safety_features)
        
        db.session.commit()
        return jsonify(fireplace_safety_features.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-safety-features/<int:inspection_id>', methods=['GET'])
def get_fireplace_safety_features(inspection_id):
    """Get fireplace safety features for an inspection"""
    try:
        fireplace_safety_features = FireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()
        if not fireplace_safety_features:
            return jsonify({'error': 'Fireplace safety features not found'}), 404
        
        return jsonify(fireplace_safety_features.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-safety-features/<int:inspection_id>', methods=['PUT'])
def update_fireplace_safety_features(inspection_id):
    """Update fireplace safety features for an inspection"""
    try:
        data = request.get_json()
        
        fireplace_safety_features = FireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()
        if not fireplace_safety_features:
            return jsonify({'error': 'Fireplace safety features not found'}), 404
        
        # Update Glass Doors
        if 'glassDoors' in data:
            glass_doors = data['glassDoors']
            fireplace_safety_features.glass_doors_required = glass_doors.get('requiredValue')
            fireplace_safety_features.glass_doors_present = glass_doors.get('presentValue')
            fireplace_safety_features.glass_doors_compliance = glass_doors.get('codeCompliance')
            fireplace_safety_features.glass_doors_photos = glass_doors.get('photos')
        
        # Update Fire Screen
        if 'fireScreen' in data:
            fire_screen = data['fireScreen']
            fireplace_safety_features.fire_screen_required = fire_screen.get('requiredValue')
            fireplace_safety_features.fire_screen_present = fire_screen.get('presentValue')
            fireplace_safety_features.fire_screen_compliance = fire_screen.get('codeCompliance')
            fireplace_safety_features.fire_screen_photos = fire_screen.get('photos')
        
        # Update Chase Framing Size
        if 'chaseFramingSize' in data:
            chase_framing_size = data['chaseFramingSize']
            fireplace_safety_features.chase_framing_size_required = chase_framing_size.get('requiredValue')
            fireplace_safety_features.chase_framing_size_present = chase_framing_size.get('presentValue')
            fireplace_safety_features.chase_framing_size_compliance = chase_framing_size.get('codeCompliance')
            fireplace_safety_features.chase_framing_size_photos = chase_framing_size.get('photos')
        
        # Update Chase Insulated
        if 'chaseInsulated' in data:
            chase_insulated = data['chaseInsulated']
            fireplace_safety_features.chase_insulated_required = chase_insulated.get('requiredValue')
            fireplace_safety_features.chase_insulated_present = chase_insulated.get('presentValue')
            fireplace_safety_features.chase_insulated_compliance = chase_insulated.get('codeCompliance')
            fireplace_safety_features.chase_insulated_photos = chase_insulated.get('photos')
        
        # Update Chase Clear of Debris
        if 'chaseClearOfDebris' in data:
            chase_clear_of_debris = data['chaseClearOfDebris']
            fireplace_safety_features.chase_clear_of_debris_required = chase_clear_of_debris.get('requiredValue')
            fireplace_safety_features.chase_clear_of_debris_present = chase_clear_of_debris.get('presentValue')
            fireplace_safety_features.chase_clear_of_debris_compliance = chase_clear_of_debris.get('codeCompliance')
            fireplace_safety_features.chase_clear_of_debris_photos = chase_clear_of_debris.get('photos')
        
        # Update Outdoor Combustion Air
        if 'outdoorCombustionAir' in data:
            outdoor_combustion_air = data['outdoorCombustionAir']
            fireplace_safety_features.outdoor_combustion_air_required = outdoor_combustion_air.get('requiredValue')
            fireplace_safety_features.outdoor_combustion_air_present = outdoor_combustion_air.get('presentValue')
            fireplace_safety_features.outdoor_combustion_air_compliance = outdoor_combustion_air.get('codeCompliance')
            fireplace_safety_features.outdoor_combustion_air_photos = outdoor_combustion_air.get('photos')
        
        fireplace_safety_features.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(fireplace_safety_features.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-safety-features/<int:inspection_id>', methods=['DELETE'])
def delete_fireplace_safety_features(inspection_id):
    """Delete fireplace safety features for an inspection"""
    try:
        fireplace_safety_features = FireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()
        if not fireplace_safety_features:
            return jsonify({'error': 'Fireplace safety features not found'}), 404
        
        db.session.delete(fireplace_safety_features)
        db.session.commit()
        
        return jsonify({'message': 'Fireplace safety features deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Chimney Support Connection Routes
@main.route('/api/chimney-support-connection', methods=['POST'])
def create_chimney_support_connection():
    """Create or update chimney support connection for an inspection"""
    try:
        data = request.get_json()
        
        if not data or 'inspection_id' not in data:
            return jsonify({'error': 'Inspection ID is required'}), 400
        
        inspection_id = data['inspection_id']
        
        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Check if chimney support connection already exists for this inspection
        chimney_support_connection = ChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()
        
        if chimney_support_connection:
            # Update existing chimney support connection
            # Fire Resistant Solid Chase
            chimney_support_connection.fire_resistant_solid_chase_required = data.get('fireResistantSolidChase', {}).get('requiredValue')
            chimney_support_connection.fire_resistant_solid_chase_present = data.get('fireResistantSolidChase', {}).get('presentValue')
            chimney_support_connection.fire_resistant_solid_chase_compliance = data.get('fireResistantSolidChase', {}).get('codeCompliance')
            chimney_support_connection.fire_resistant_solid_chase_photos = data.get('fireResistantSolidChase', {}).get('photos')
            
            # Properly Secured Chase
            chimney_support_connection.properly_secured_chase_required = data.get('properlySecuredChase', {}).get('requiredValue')
            chimney_support_connection.properly_secured_chase_present = data.get('properlySecuredChase', {}).get('presentValue')
            chimney_support_connection.properly_secured_chase_compliance = data.get('properlySecuredChase', {}).get('codeCompliance')
            chimney_support_connection.properly_secured_chase_photos = data.get('properlySecuredChase', {}).get('photos')
            
            # Is Proper
            chimney_support_connection.is_proper_required = data.get('isProper', {}).get('requiredValue')
            chimney_support_connection.is_proper_present = data.get('isProper', {}).get('presentValue')
            chimney_support_connection.is_proper_compliance = data.get('isProper', {}).get('codeCompliance')
            chimney_support_connection.is_proper_photos = data.get('isProper', {}).get('photos')
            
            # Fire Retardant Clearances
            chimney_support_connection.fire_retardant_clearances_required = data.get('fireRetardantClearances', {}).get('requiredValue')
            chimney_support_connection.fire_retardant_clearances_present = data.get('fireRetardantClearances', {}).get('presentValue')
            chimney_support_connection.fire_retardant_clearances_compliance = data.get('fireRetardantClearances', {}).get('codeCompliance')
            chimney_support_connection.fire_retardant_clearances_photos = data.get('fireRetardantClearances', {}).get('photos')
            
            # Foundation Footing Connection
            chimney_support_connection.foundation_footing_connection_required = data.get('foundationFootingConnection', {}).get('requiredValue')
            chimney_support_connection.foundation_footing_connection_present = data.get('foundationFootingConnection', {}).get('presentValue')
            chimney_support_connection.foundation_footing_connection_compliance = data.get('foundationFootingConnection', {}).get('codeCompliance')
            chimney_support_connection.foundation_footing_connection_photos = data.get('foundationFootingConnection', {}).get('photos')
            
            # Well Supported
            chimney_support_connection.well_supported_required = data.get('wellSupported', {}).get('requiredValue')
            chimney_support_connection.well_supported_present = data.get('wellSupported', {}).get('presentValue')
            chimney_support_connection.well_supported_compliance = data.get('wellSupported', {}).get('codeCompliance')
            chimney_support_connection.well_supported_photos = data.get('wellSupported', {}).get('photos')
            
            # Windows Foundation Aesthetic
            chimney_support_connection.windows_foundation_aesthetic_required = data.get('windowsFoundationAesthetic', {}).get('requiredValue')
            chimney_support_connection.windows_foundation_aesthetic_present = data.get('windowsFoundationAesthetic', {}).get('presentValue')
            chimney_support_connection.windows_foundation_aesthetic_compliance = data.get('windowsFoundationAesthetic', {}).get('codeCompliance')
            chimney_support_connection.windows_foundation_aesthetic_photos = data.get('windowsFoundationAesthetic', {}).get('photos')
            
            # Roof System
            chimney_support_connection.roof_system_required = data.get('roofSystem', {}).get('requiredValue')
            chimney_support_connection.roof_system_present = data.get('roofSystem', {}).get('presentValue')
            chimney_support_connection.roof_system_compliance = data.get('roofSystem', {}).get('codeCompliance')
            chimney_support_connection.roof_system_photos = data.get('roofSystem', {}).get('photos')
            
            # Penetrating
            chimney_support_connection.penetrating_required = data.get('penetrating', {}).get('requiredValue')
            chimney_support_connection.penetrating_present = data.get('penetrating', {}).get('presentValue')
            chimney_support_connection.penetrating_compliance = data.get('penetrating', {}).get('codeCompliance')
            chimney_support_connection.penetrating_photos = data.get('penetrating', {}).get('photos')
            
            # CO Alarm Sections
            chimney_support_connection.co_alarm_same_room_bcbc_required = data.get('coAlarmSameRoomBCBC', {}).get('requiredValue')
            chimney_support_connection.co_alarm_same_room_bcbc_present = data.get('coAlarmSameRoomBCBC', {}).get('presentValue')
            chimney_support_connection.co_alarm_same_room_bcbc_compliance = data.get('coAlarmSameRoomBCBC', {}).get('codeCompliance')
            chimney_support_connection.co_alarm_same_room_bcbc_photos = data.get('coAlarmSameRoomBCBC', {}).get('photos')

            chimney_support_connection.co_alarm_same_room_nbcabc_required = data.get('coAlarmSameRoomNBCABC', {}).get('requiredValue')
            chimney_support_connection.co_alarm_same_room_nbcabc_present = data.get('coAlarmSameRoomNBCABC', {}).get('presentValue')
            chimney_support_connection.co_alarm_same_room_nbcabc_compliance = data.get('coAlarmSameRoomNBCABC', {}).get('codeCompliance')
            chimney_support_connection.co_alarm_same_room_nbcabc_photos = data.get('coAlarmSameRoomNBCABC', {}).get('photos')

            chimney_support_connection.co_alarm_present_obc_required = data.get('coAlarmPresentOBC', {}).get('requiredValue')
            chimney_support_connection.co_alarm_present_obc_present = data.get('coAlarmPresentOBC', {}).get('presentValue')
            chimney_support_connection.co_alarm_present_obc_compliance = data.get('coAlarmPresentOBC', {}).get('codeCompliance')
            chimney_support_connection.co_alarm_present_obc_photos = data.get('coAlarmPresentOBC', {}).get('photos')

            # Note fields
            chimney_support_connection.clearance_requirements = data.get('clearanceRequirements')
            chimney_support_connection.note_required_value = data.get('noteRequiredValue')
            chimney_support_connection.note_present_value = data.get('notePresentValue')
            chimney_support_connection.note_code_compliance = data.get('noteCodeCompliance')
            
            chimney_support_connection.updated_at = datetime.utcnow()
        else:
            # Create new chimney support connection
            chimney_support_connection = ChimneySupportConnection(
                inspection_id=inspection_id,
                # Fire Resistant Solid Chase
                fire_resistant_solid_chase_required=data.get('fireResistantSolidChase', {}).get('requiredValue'),
                fire_resistant_solid_chase_present=data.get('fireResistantSolidChase', {}).get('presentValue'),
                fire_resistant_solid_chase_compliance=data.get('fireResistantSolidChase', {}).get('codeCompliance'),
                fire_resistant_solid_chase_photos=data.get('fireResistantSolidChase', {}).get('photos'),
                # Properly Secured Chase
                properly_secured_chase_required=data.get('properlySecuredChase', {}).get('requiredValue'),
                properly_secured_chase_present=data.get('properlySecuredChase', {}).get('presentValue'),
                properly_secured_chase_compliance=data.get('properlySecuredChase', {}).get('codeCompliance'),
                properly_secured_chase_photos=data.get('properlySecuredChase', {}).get('photos'),
                # Is Proper
                is_proper_required=data.get('isProper', {}).get('requiredValue'),
                is_proper_present=data.get('isProper', {}).get('presentValue'),
                is_proper_compliance=data.get('isProper', {}).get('codeCompliance'),
                is_proper_photos=data.get('isProper', {}).get('photos'),
                # Fire Retardant Clearances
                fire_retardant_clearances_required=data.get('fireRetardantClearances', {}).get('requiredValue'),
                fire_retardant_clearances_present=data.get('fireRetardantClearances', {}).get('presentValue'),
                fire_retardant_clearances_compliance=data.get('fireRetardantClearances', {}).get('codeCompliance'),
                fire_retardant_clearances_photos=data.get('fireRetardantClearances', {}).get('photos'),
                # Foundation Footing Connection
                foundation_footing_connection_required=data.get('foundationFootingConnection', {}).get('requiredValue'),
                foundation_footing_connection_present=data.get('foundationFootingConnection', {}).get('presentValue'),
                foundation_footing_connection_compliance=data.get('foundationFootingConnection', {}).get('codeCompliance'),
                foundation_footing_connection_photos=data.get('foundationFootingConnection', {}).get('photos'),
                # Well Supported
                well_supported_required=data.get('wellSupported', {}).get('requiredValue'),
                well_supported_present=data.get('wellSupported', {}).get('presentValue'),
                well_supported_compliance=data.get('wellSupported', {}).get('codeCompliance'),
                well_supported_photos=data.get('wellSupported', {}).get('photos'),
                # Windows Foundation Aesthetic
                windows_foundation_aesthetic_required=data.get('windowsFoundationAesthetic', {}).get('requiredValue'),
                windows_foundation_aesthetic_present=data.get('windowsFoundationAesthetic', {}).get('presentValue'),
                windows_foundation_aesthetic_compliance=data.get('windowsFoundationAesthetic', {}).get('codeCompliance'),
                windows_foundation_aesthetic_photos=data.get('windowsFoundationAesthetic', {}).get('photos'),
                # Roof System
                roof_system_required=data.get('roofSystem', {}).get('requiredValue'),
                roof_system_present=data.get('roofSystem', {}).get('presentValue'),
                roof_system_compliance=data.get('roofSystem', {}).get('codeCompliance'),
                roof_system_photos=data.get('roofSystem', {}).get('photos'),
                # Penetrating
                penetrating_required=data.get('penetrating', {}).get('requiredValue'),
                penetrating_present=data.get('penetrating', {}).get('presentValue'),
                penetrating_compliance=data.get('penetrating', {}).get('codeCompliance'),
                penetrating_photos=data.get('penetrating', {}).get('photos')
            )
            db.session.add(chimney_support_connection)
        
        db.session.commit()
        return jsonify(chimney_support_connection.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating/updating chimney support connection: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/api/chimney-support-connection/<int:inspection_id>', methods=['DELETE'])
def delete_chimney_support_connection(inspection_id):
    """Delete chimney support connection for an inspection"""
    try:
        chimney_support_connection = ChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_support_connection:
            return jsonify({'error': 'Chimney support connection not found'}), 404
        
        db.session.delete(chimney_support_connection)
        db.session.commit()
        
        return jsonify({'message': 'Chimney support connection deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Attic Radiation Protection Routes
@main.route('/api/attic-radiation-protection', methods=['POST'])
def create_attic_radiation_protection():
    """Create or update attic radiation protection for an inspection"""
    try:
        data = request.get_json()
        
        if not data or 'inspection_id' not in data:
            return jsonify({'error': 'Inspection ID is required'}), 400
        
        inspection_id = data['inspection_id']
        
        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Check if attic radiation protection already exists for this inspection
        attic_radiation_protection = AtticRadiationProtection.query.filter_by(inspection_id=inspection_id).first()
        
        if attic_radiation_protection:
            # Update existing attic radiation protection
            # Wall Support Brand
            attic_radiation_protection.wall_support_brand_required = data.get('wallSupportBrand', {}).get('requiredValue')
            attic_radiation_protection.wall_support_brand_present = data.get('wallSupportBrand', {}).get('presentValue')
            attic_radiation_protection.wall_support_brand_compliance = data.get('wallSupportBrand', {}).get('codeCompliance')
            attic_radiation_protection.wall_support_brand_photos = data.get('wallSupportBrand', {}).get('photos')
            
            # Attic Radiation Shield
            attic_radiation_protection.attic_radiation_shield_required = data.get('atticRadiationShield', {}).get('requiredValue')
            attic_radiation_protection.attic_radiation_shield_present = data.get('atticRadiationShield', {}).get('presentValue')
            attic_radiation_protection.attic_radiation_shield_compliance = data.get('atticRadiationShield', {}).get('codeCompliance')
            attic_radiation_protection.attic_radiation_shield_photos = data.get('atticRadiationShield', {}).get('photos')
            
            # Attic Shield Above Insulation
            attic_radiation_protection.attic_shield_above_insulation_required = data.get('atticShieldAboveInsulation', {}).get('requiredValue')
            attic_radiation_protection.attic_shield_above_insulation_present = data.get('atticShieldAboveInsulation', {}).get('presentValue')
            attic_radiation_protection.attic_shield_above_insulation_compliance = data.get('atticShieldAboveInsulation', {}).get('codeCompliance')
            attic_radiation_protection.attic_shield_above_insulation_photos = data.get('atticShieldAboveInsulation', {}).get('photos')
            
            # Other Radiation Shields
            attic_radiation_protection.other_radiation_shields_required = data.get('otherRadiationShields', {}).get('requiredValue')
            attic_radiation_protection.other_radiation_shields_present = data.get('otherRadiationShields', {}).get('presentValue')
            attic_radiation_protection.other_radiation_shields_compliance = data.get('otherRadiationShields', {}).get('codeCompliance')
            attic_radiation_protection.other_radiation_shields_photos = data.get('otherRadiationShields', {}).get('photos')
            
            # Enclosed Through Living Space
            attic_radiation_protection.enclosed_through_living_space_required = data.get('enclosedThroughLivingSpace', {}).get('requiredValue')
            attic_radiation_protection.enclosed_through_living_space_present = data.get('enclosedThroughLivingSpace', {}).get('presentValue')
            attic_radiation_protection.enclosed_through_living_space_compliance = data.get('enclosedThroughLivingSpace', {}).get('codeCompliance')
            attic_radiation_protection.enclosed_through_living_space_photos = data.get('enclosedThroughLivingSpace', {}).get('photos')
            
            attic_radiation_protection.updated_at = datetime.utcnow()
        else:
            # Create new attic radiation protection
            attic_radiation_protection = AtticRadiationProtection(
                inspection_id=inspection_id,
                # Wall Support Brand
                wall_support_brand_required=data.get('wallSupportBrand', {}).get('requiredValue'),
                wall_support_brand_present=data.get('wallSupportBrand', {}).get('presentValue'),
                wall_support_brand_compliance=data.get('wallSupportBrand', {}).get('codeCompliance'),
                wall_support_brand_photos=data.get('wallSupportBrand', {}).get('photos'),
                # Attic Radiation Shield
                attic_radiation_shield_required=data.get('atticRadiationShield', {}).get('requiredValue'),
                attic_radiation_shield_present=data.get('atticRadiationShield', {}).get('presentValue'),
                attic_radiation_shield_compliance=data.get('atticRadiationShield', {}).get('codeCompliance'),
                attic_radiation_shield_photos=data.get('atticRadiationShield', {}).get('photos'),
                # Attic Shield Above Insulation
                attic_shield_above_insulation_required=data.get('atticShieldAboveInsulation', {}).get('requiredValue'),
                attic_shield_above_insulation_present=data.get('atticShieldAboveInsulation', {}).get('presentValue'),
                attic_shield_above_insulation_compliance=data.get('atticShieldAboveInsulation', {}).get('codeCompliance'),
                attic_shield_above_insulation_photos=data.get('atticShieldAboveInsulation', {}).get('photos'),
                # Other Radiation Shields
                other_radiation_shields_required=data.get('otherRadiationShields', {}).get('requiredValue'),
                other_radiation_shields_present=data.get('otherRadiationShields', {}).get('presentValue'),
                other_radiation_shields_compliance=data.get('otherRadiationShields', {}).get('codeCompliance'),
                other_radiation_shields_photos=data.get('otherRadiationShields', {}).get('photos'),
                # Enclosed Through Living Space
                enclosed_through_living_space_required=data.get('enclosedThroughLivingSpace', {}).get('requiredValue'),
                enclosed_through_living_space_present=data.get('enclosedThroughLivingSpace', {}).get('presentValue'),
                enclosed_through_living_space_compliance=data.get('enclosedThroughLivingSpace', {}).get('codeCompliance'),
                enclosed_through_living_space_photos=data.get('enclosedThroughLivingSpace', {}).get('photos')
            )
            db.session.add(attic_radiation_protection)
        
        db.session.commit()
        return jsonify(attic_radiation_protection.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/attic-radiation-protection/<int:inspection_id>', methods=['GET'])
def get_attic_radiation_protection(inspection_id):
    """Get attic radiation protection for an inspection"""
    try:
        attic_radiation_protection = AtticRadiationProtection.query.filter_by(inspection_id=inspection_id).first()
        if not attic_radiation_protection:
            return jsonify({'error': 'Attic radiation protection not found'}), 404
        
        return jsonify(attic_radiation_protection.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/attic-radiation-protection/<int:inspection_id>', methods=['PUT'])
def update_attic_radiation_protection(inspection_id):
    """Update attic radiation protection for an inspection"""
    try:
        data = request.get_json()
        
        attic_radiation_protection = AtticRadiationProtection.query.filter_by(inspection_id=inspection_id).first()
        if not attic_radiation_protection:
            return jsonify({'error': 'Attic radiation protection not found'}), 404
        
        # Update Wall Support Brand
        if 'wallSupportBrand' in data:
            wall_support_brand = data['wallSupportBrand']
            attic_radiation_protection.wall_support_brand_required = wall_support_brand.get('requiredValue')
            attic_radiation_protection.wall_support_brand_present = wall_support_brand.get('presentValue')
            attic_radiation_protection.wall_support_brand_compliance = wall_support_brand.get('codeCompliance')
            attic_radiation_protection.wall_support_brand_photos = wall_support_brand.get('photos')
        
        # Update Attic Radiation Shield
        if 'atticRadiationShield' in data:
            attic_radiation_shield = data['atticRadiationShield']
            attic_radiation_protection.attic_radiation_shield_required = attic_radiation_shield.get('requiredValue')
            attic_radiation_protection.attic_radiation_shield_present = attic_radiation_shield.get('presentValue')
            attic_radiation_protection.attic_radiation_shield_compliance = attic_radiation_shield.get('codeCompliance')
            attic_radiation_protection.attic_radiation_shield_photos = attic_radiation_shield.get('photos')
        
        # Update Attic Shield Above Insulation
        if 'atticShieldAboveInsulation' in data:
            attic_shield_above_insulation = data['atticShieldAboveInsulation']
            attic_radiation_protection.attic_shield_above_insulation_required = attic_shield_above_insulation.get('requiredValue')
            attic_radiation_protection.attic_shield_above_insulation_present = attic_shield_above_insulation.get('presentValue')
            attic_radiation_protection.attic_shield_above_insulation_compliance = attic_shield_above_insulation.get('codeCompliance')
            attic_radiation_protection.attic_shield_above_insulation_photos = attic_shield_above_insulation.get('photos')
        
        # Update Other Radiation Shields
        if 'otherRadiationShields' in data:
            other_radiation_shields = data['otherRadiationShields']
            attic_radiation_protection.other_radiation_shields_required = other_radiation_shields.get('requiredValue')
            attic_radiation_protection.other_radiation_shields_present = other_radiation_shields.get('presentValue')
            attic_radiation_protection.other_radiation_shields_compliance = other_radiation_shields.get('codeCompliance')
            attic_radiation_protection.other_radiation_shields_photos = other_radiation_shields.get('photos')
        
        # Update Enclosed Through Living Space
        if 'enclosedThroughLivingSpace' in data:
            enclosed_through_living_space = data['enclosedThroughLivingSpace']
            attic_radiation_protection.enclosed_through_living_space_required = enclosed_through_living_space.get('requiredValue')
            attic_radiation_protection.enclosed_through_living_space_present = enclosed_through_living_space.get('presentValue')
            attic_radiation_protection.enclosed_through_living_space_compliance = enclosed_through_living_space.get('codeCompliance')
            attic_radiation_protection.enclosed_through_living_space_photos = enclosed_through_living_space.get('photos')
        
        attic_radiation_protection.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(attic_radiation_protection.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/attic-radiation-protection/<int:inspection_id>', methods=['DELETE'])
def delete_attic_radiation_protection(inspection_id):
    """Delete attic radiation protection for an inspection"""
    try:
        attic_radiation_protection = AtticRadiationProtection.query.filter_by(inspection_id=inspection_id).first()
        if not attic_radiation_protection:
            return jsonify({'error': 'Attic radiation protection not found'}), 404
        
        db.session.delete(attic_radiation_protection)
        db.session.commit()
        
        return jsonify({'message': 'Attic radiation protection deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Roof Exterior Protection Routes
@main.route('/api/roof-exterior-protection', methods=['POST'])
def create_roof_exterior_protection():
    """Create or update roof exterior protection for an inspection"""
    try:
        data = request.get_json()
        
        if not data or 'inspection_id' not in data:
            return jsonify({'error': 'Inspection ID is required'}), 400
        
        inspection_id = data['inspection_id']
        
        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Check if roof exterior protection already exists for this inspection
        roof_exterior_protection = RoofExteriorProtection.query.filter_by(inspection_id=inspection_id).first()
        
        if roof_exterior_protection:
            # Update existing roof exterior protection
            # Roof Flashing Storm Collar
            roof_exterior_protection.roof_flashing_storm_collar_required = data.get('roofFlashingStormCollar', {}).get('requiredValue')
            roof_exterior_protection.roof_flashing_storm_collar_present = data.get('roofFlashingStormCollar', {}).get('presentValue')
            roof_exterior_protection.roof_flashing_storm_collar_compliance = data.get('roofFlashingStormCollar', {}).get('codeCompliance')
            roof_exterior_protection.roof_flashing_storm_collar_photos = data.get('roofFlashingStormCollar', {}).get('photos')
            
            # Rain Cap
            roof_exterior_protection.rain_cap_required = data.get('rainCap', {}).get('requiredValue')
            roof_exterior_protection.rain_cap_present = data.get('rainCap', {}).get('presentValue')
            roof_exterior_protection.rain_cap_compliance = data.get('rainCap', {}).get('codeCompliance')
            roof_exterior_protection.rain_cap_photos = data.get('rainCap', {}).get('photos')
            
            # Rain Cap Spark Arrestor
            roof_exterior_protection.rain_cap_spark_arrestor_required = data.get('rainCapSparkArrestor', {}).get('requiredValue')
            roof_exterior_protection.rain_cap_spark_arrestor_present = data.get('rainCapSparkArrestor', {}).get('presentValue')
            roof_exterior_protection.rain_cap_spark_arrestor_compliance = data.get('rainCapSparkArrestor', {}).get('codeCompliance')
            roof_exterior_protection.rain_cap_spark_arrestor_photos = data.get('rainCapSparkArrestor', {}).get('photos')
            
            # Roof Braces
            roof_exterior_protection.roof_braces_required = data.get('roofBraces', {}).get('requiredValue')
            roof_exterior_protection.roof_braces_present = data.get('roofBraces', {}).get('presentValue')
            roof_exterior_protection.roof_braces_compliance = data.get('roofBraces', {}).get('codeCompliance')
            roof_exterior_protection.roof_braces_photos = data.get('roofBraces', {}).get('photos')
            
            # Roof Braces Solidly Anchored
            roof_exterior_protection.roof_braces_solidly_anchored_required = data.get('roofBracesSolidlyAnchored', {}).get('requiredValue')
            roof_exterior_protection.roof_braces_solidly_anchored_present = data.get('roofBracesSolidlyAnchored', {}).get('presentValue')
            roof_exterior_protection.roof_braces_solidly_anchored_compliance = data.get('roofBracesSolidlyAnchored', {}).get('codeCompliance')
            roof_exterior_protection.roof_braces_solidly_anchored_photos = data.get('roofBracesSolidlyAnchored', {}).get('photos')
            
            roof_exterior_protection.updated_at = datetime.utcnow()
        else:
            # Create new roof exterior protection
            roof_exterior_protection = RoofExteriorProtection(
                inspection_id=inspection_id,
                # Roof Flashing Storm Collar
                roof_flashing_storm_collar_required=data.get('roofFlashingStormCollar', {}).get('requiredValue'),
                roof_flashing_storm_collar_present=data.get('roofFlashingStormCollar', {}).get('presentValue'),
                roof_flashing_storm_collar_compliance=data.get('roofFlashingStormCollar', {}).get('codeCompliance'),
                roof_flashing_storm_collar_photos=data.get('roofFlashingStormCollar', {}).get('photos'),
                # Rain
                rain_required=data.get('rain', {}).get('requiredValue'),
                rain_present=data.get('rain', {}).get('presentValue'),
                rain_compliance=data.get('rain', {}).get('codeCompliance'),
                rain_photos=data.get('rain', {}).get('photos'),
                # Rain Cap Spark Arrestor
                rain_cap_spark_arrestor_required=data.get('rainCapSparkArrestor', {}).get('requiredValue'),
                rain_cap_spark_arrestor_present=data.get('rainCapSparkArrestor', {}).get('presentValue'),
                rain_cap_spark_arrestor_compliance=data.get('rainCapSparkArrestor', {}).get('codeCompliance'),
                rain_cap_spark_arrestor_photos=data.get('rainCapSparkArrestor', {}).get('photos'),
                # Roof Braces
                roof_braces_required=data.get('roofBraces', {}).get('requiredValue'),
                roof_braces_present=data.get('roofBraces', {}).get('presentValue'),
                roof_braces_compliance=data.get('roofBraces', {}).get('codeCompliance'),
                roof_braces_photos=data.get('roofBraces', {}).get('photos'),
                # Roof Braces Solidly Anchored
                roof_braces_solidly_anchored_required=data.get('roofBracesSolidlyAnchored', {}).get('requiredValue'),
                roof_braces_solidly_anchored_present=data.get('roofBracesSolidlyAnchored', {}).get('presentValue'),
                roof_braces_solidly_anchored_compliance=data.get('roofBracesSolidlyAnchored', {}).get('codeCompliance'),
                roof_braces_solidly_anchored_photos=data.get('roofBracesSolidlyAnchored', {}).get('photos')
            )
            db.session.add(roof_exterior_protection)
        
        db.session.commit()
        return jsonify(roof_exterior_protection.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/roof-exterior-protection/<int:inspection_id>', methods=['GET'])
def get_roof_exterior_protection(inspection_id):
    """Get roof exterior protection for an inspection"""
    try:
        roof_exterior_protection = RoofExteriorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not roof_exterior_protection:
            return jsonify({'error': 'Roof exterior protection not found'}), 404
        
        return jsonify(roof_exterior_protection.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/roof-exterior-protection/<int:inspection_id>', methods=['PUT'])
def update_roof_exterior_protection(inspection_id):
    """Update roof exterior protection for an inspection"""
    try:
        data = request.get_json()
        
        roof_exterior_protection = RoofExteriorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not roof_exterior_protection:
            return jsonify({'error': 'Roof exterior protection not found'}), 404
        
        # Update Roof Flashing Storm Collar
        if 'roofFlashingStormCollar' in data:
            roof_flashing_storm_collar = data['roofFlashingStormCollar']
            roof_exterior_protection.roof_flashing_storm_collar_required = roof_flashing_storm_collar.get('requiredValue')
            roof_exterior_protection.roof_flashing_storm_collar_present = roof_flashing_storm_collar.get('presentValue')
            roof_exterior_protection.roof_flashing_storm_collar_compliance = roof_flashing_storm_collar.get('codeCompliance')
            roof_exterior_protection.roof_flashing_storm_collar_photos = roof_flashing_storm_collar.get('photos')
        
        # Update Rain
        if 'rain' in data:
            rain = data['rain']
            roof_exterior_protection.rain_required = rain.get('requiredValue')
            roof_exterior_protection.rain_present = rain.get('presentValue')
            roof_exterior_protection.rain_compliance = rain.get('codeCompliance')
            roof_exterior_protection.rain_photos = rain.get('photos')
        
        # Update Rain Cap Spark Arrestor
        if 'rainCapSparkArrestor' in data:
            rain_cap_spark_arrestor = data['rainCapSparkArrestor']
            roof_exterior_protection.rain_cap_spark_arrestor_required = rain_cap_spark_arrestor.get('requiredValue')
            roof_exterior_protection.rain_cap_spark_arrestor_present = rain_cap_spark_arrestor.get('presentValue')
            roof_exterior_protection.rain_cap_spark_arrestor_compliance = rain_cap_spark_arrestor.get('codeCompliance')
            roof_exterior_protection.rain_cap_spark_arrestor_photos = rain_cap_spark_arrestor.get('photos')
        
        # Update Roof Braces
        if 'roofBraces' in data:
            roof_braces = data['roofBraces']
            roof_exterior_protection.roof_braces_required = roof_braces.get('requiredValue')
            roof_exterior_protection.roof_braces_present = roof_braces.get('presentValue')
            roof_exterior_protection.roof_braces_compliance = roof_braces.get('codeCompliance')
            roof_exterior_protection.roof_braces_photos = roof_braces.get('photos')
        
        # Update Roof Braces Solidly Anchored
        if 'roofBracesSolidlyAnchored' in data:
            roof_braces_solidly_anchored = data['roofBracesSolidlyAnchored']
            roof_exterior_protection.roof_braces_solidly_anchored_required = roof_braces_solidly_anchored.get('requiredValue')
            roof_exterior_protection.roof_braces_solidly_anchored_present = roof_braces_solidly_anchored.get('presentValue')
            roof_exterior_protection.roof_braces_solidly_anchored_compliance = roof_braces_solidly_anchored.get('codeCompliance')
            roof_exterior_protection.roof_braces_solidly_anchored_photos = roof_braces_solidly_anchored.get('photos')
        
        roof_exterior_protection.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(roof_exterior_protection.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/roof-exterior-protection/<int:inspection_id>', methods=['DELETE'])
def delete_roof_exterior_protection(inspection_id):
    """Delete roof exterior protection for an inspection"""
    try:
        roof_exterior_protection = RoofExteriorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not roof_exterior_protection:
            return jsonify({'error': 'Roof exterior protection not found'}), 404
        
        db.session.delete(roof_exterior_protection)
        db.session.commit()
        
        return jsonify({'message': 'Roof exterior protection deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Chimney Height Clearance Routes
@main.route('/api/chimney-height-clearance', methods=['POST'])
def create_chimney_height_clearance():
    """Create or update chimney height clearance for an inspection"""
    try:
        data = request.get_json()
        
        if not data or 'inspection_id' not in data:
            return jsonify({'error': 'Inspection ID is required'}), 400
        
        inspection_id = data['inspection_id']
        
        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Check if chimney height clearance already exists for this inspection
        chimney_height_clearance = ChimneyHeightClearance.query.filter_by(inspection_id=inspection_id).first()
        
        if chimney_height_clearance:
            # Update existing chimney height clearance
            # Height Above Roof Surface
            chimney_height_clearance.height_above_roof_surface_required = data.get('heightAboveRoofSurface', {}).get('requiredValue')
            chimney_height_clearance.height_above_roof_surface_present = data.get('heightAboveRoofSurface', {}).get('presentValue')
            chimney_height_clearance.height_above_roof_surface_compliance = data.get('heightAboveRoofSurface', {}).get('codeCompliance')
            chimney_height_clearance.height_above_roof_surface_photos = data.get('heightAboveRoofSurface', {}).get('photos')
            
            # Height Within 3m
            chimney_height_clearance.height_within_3m_required = data.get('heightWithin3m', {}).get('requiredValue')
            chimney_height_clearance.height_within_3m_present = data.get('heightWithin3m', {}).get('presentValue')
            chimney_height_clearance.height_within_3m_compliance = data.get('heightWithin3m', {}).get('codeCompliance')
            chimney_height_clearance.height_within_3m_photos = data.get('heightWithin3m', {}).get('photos')
            
            # Cap Height Above Chase
            chimney_height_clearance.cap_height_above_chase_required = data.get('capHeightAboveChase', {}).get('requiredValue')
            chimney_height_clearance.cap_height_above_chase_present = data.get('capHeightAboveChase', {}).get('presentValue')
            chimney_height_clearance.cap_height_above_chase_compliance = data.get('capHeightAboveChase', {}).get('codeCompliance')
            chimney_height_clearance.cap_height_above_chase_photos = data.get('capHeightAboveChase', {}).get('photos')
            
            # Chimney Clearance to Combustibles
            chimney_height_clearance.chimney_clearance_to_combustibles_required = data.get('chimneyClearanceToCombustibles', {}).get('requiredValue')
            chimney_height_clearance.chimney_clearance_to_combustibles_present = data.get('chimneyClearanceToCombustibles', {}).get('presentValue')
            chimney_height_clearance.chimney_clearance_to_combustibles_compliance = data.get('chimneyClearanceToCombustibles', {}).get('codeCompliance')
            chimney_height_clearance.chimney_clearance_to_combustibles_photos = data.get('chimneyClearanceToCombustibles', {}).get('photos')
            
            # Within 3m Area Enclosed
            chimney_height_clearance.within_3m_area_enclosed_required = data.get('within3mAreaEnclosed', {}).get('requiredValue')
            chimney_height_clearance.within_3m_area_enclosed_present = data.get('within3mAreaEnclosed', {}).get('presentValue')
            chimney_height_clearance.within_3m_area_enclosed_compliance = data.get('within3mAreaEnclosed', {}).get('codeCompliance')
            chimney_height_clearance.within_3m_area_enclosed_photos = data.get('within3mAreaEnclosed', {}).get('photos')
            
            # Final Note
            if 'finalNote' in data:
                final_note = data['finalNote']
                chimney_height_clearance.final_note_clearance_requirements = final_note.get('clearanceRequirements')
                chimney_height_clearance.final_note_required_value = final_note.get('requiredValue')
                chimney_height_clearance.final_note_present_value = final_note.get('presentValue')
                chimney_height_clearance.final_note_code_compliance = final_note.get('codeCompliance')
                chimney_height_clearance.final_note_photos = final_note.get('photos')
            
            chimney_height_clearance.updated_at = datetime.utcnow()
        else:
            # Create new chimney height clearance
            chimney_height_clearance = ChimneyHeightClearance(
                inspection_id=inspection_id,
                # Height Above Roof Surface
                height_above_roof_surface_required=data.get('heightAboveRoofSurface', {}).get('requiredValue'),
                height_above_roof_surface_present=data.get('heightAboveRoofSurface', {}).get('presentValue'),
                height_above_roof_surface_compliance=data.get('heightAboveRoofSurface', {}).get('codeCompliance'),
                height_above_roof_surface_photos=data.get('heightAboveRoofSurface', {}).get('photos'),
                # Height Within 3m
                height_within_3m_required=data.get('heightWithin3m', {}).get('requiredValue'),
                height_within_3m_present=data.get('heightWithin3m', {}).get('presentValue'),
                height_within_3m_compliance=data.get('heightWithin3m', {}).get('codeCompliance'),
                height_within_3m_photos=data.get('heightWithin3m', {}).get('photos'),
                # Cap Height Above Chase
                cap_height_above_chase_required=data.get('capHeightAboveChase', {}).get('requiredValue'),
                cap_height_above_chase_present=data.get('capHeightAboveChase', {}).get('presentValue'),
                cap_height_above_chase_compliance=data.get('capHeightAboveChase', {}).get('codeCompliance'),
                cap_height_above_chase_photos=data.get('capHeightAboveChase', {}).get('photos'),
                # Chimney Clearance to Combustibles
                chimney_clearance_to_combustibles_required=data.get('chimneyClearanceToCombustibles', {}).get('requiredValue'),
                chimney_clearance_to_combustibles_present=data.get('chimneyClearanceToCombustibles', {}).get('presentValue'),
                chimney_clearance_to_combustibles_compliance=data.get('chimneyClearanceToCombustibles', {}).get('codeCompliance'),
                chimney_clearance_to_combustibles_photos=data.get('chimneyClearanceToCombustibles', {}).get('photos'),
                # Within 3m Area Enclosed
                within_3m_area_enclosed_required=data.get('within3mAreaEnclosed', {}).get('requiredValue'),
                within_3m_area_enclosed_present=data.get('within3mAreaEnclosed', {}).get('presentValue'),
                within_3m_area_enclosed_compliance=data.get('within3mAreaEnclosed', {}).get('codeCompliance'),
                within_3m_area_enclosed_photos=data.get('within3mAreaEnclosed', {}).get('photos'),
                # Final Note
                final_note_clearance_requirements=data.get('finalNote', {}).get('clearanceRequirements'),
                final_note_required_value=data.get('finalNote', {}).get('requiredValue'),
                final_note_present_value=data.get('finalNote', {}).get('presentValue'),
                final_note_code_compliance=data.get('finalNote', {}).get('codeCompliance'),
                final_note_photos=data.get('finalNote', {}).get('photos')
            )
            db.session.add(chimney_height_clearance)
        
        db.session.commit()
        return jsonify(chimney_height_clearance.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/chimney-height-clearance/<int:inspection_id>', methods=['GET'])
def get_chimney_height_clearance(inspection_id):
    """Get chimney height clearance for an inspection"""
    try:
        chimney_height_clearance = ChimneyHeightClearance.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_height_clearance:
            return jsonify({'error': 'Chimney height clearance not found'}), 404
        
        return jsonify(chimney_height_clearance.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/chimney-height-clearance/<int:inspection_id>', methods=['PUT'])
def update_chimney_height_clearance(inspection_id):
    """Update chimney height clearance for an inspection"""
    try:
        data = request.get_json()
        
        chimney_height_clearance = ChimneyHeightClearance.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_height_clearance:
            return jsonify({'error': 'Chimney height clearance not found'}), 404
        
        # Update Height Above Roof Surface
        if 'heightAboveRoofSurface' in data:
            height_above_roof_surface = data['heightAboveRoofSurface']
            chimney_height_clearance.height_above_roof_surface_required = height_above_roof_surface.get('requiredValue')
            chimney_height_clearance.height_above_roof_surface_present = height_above_roof_surface.get('presentValue')
            chimney_height_clearance.height_above_roof_surface_compliance = height_above_roof_surface.get('codeCompliance')
            chimney_height_clearance.height_above_roof_surface_photos = height_above_roof_surface.get('photos')

        # Update Height Within 3m
        if 'heightWithin3m' in data:
            height_within_3m = data['heightWithin3m']
            chimney_height_clearance.height_within_3m_required = height_within_3m.get('requiredValue')
            chimney_height_clearance.height_within_3m_present = height_within_3m.get('presentValue')
            chimney_height_clearance.height_within_3m_compliance = height_within_3m.get('codeCompliance')
            chimney_height_clearance.height_within_3m_photos = height_within_3m.get('photos')

        # Update Cap Height Above Chase
        if 'capHeightAboveChase' in data:
            cap_height_above_chase = data['capHeightAboveChase']
            chimney_height_clearance.cap_height_above_chase_required = cap_height_above_chase.get('requiredValue')
            chimney_height_clearance.cap_height_above_chase_present = cap_height_above_chase.get('presentValue')
            chimney_height_clearance.cap_height_above_chase_compliance = cap_height_above_chase.get('codeCompliance')
            chimney_height_clearance.cap_height_above_chase_photos = cap_height_above_chase.get('photos')

        # Update Chimney Clearance to Combustibles
        if 'chimneyClearanceToCombustibles' in data:
            chimney_clearance_to_combustibles = data['chimneyClearanceToCombustibles']
            chimney_height_clearance.chimney_clearance_to_combustibles_required = chimney_clearance_to_combustibles.get('requiredValue')
            chimney_height_clearance.chimney_clearance_to_combustibles_present = chimney_clearance_to_combustibles.get('presentValue')
            chimney_height_clearance.chimney_clearance_to_combustibles_compliance = chimney_clearance_to_combustibles.get('codeCompliance')
            chimney_height_clearance.chimney_clearance_to_combustibles_photos = chimney_clearance_to_combustibles.get('photos')

        # Update Within 3m Area Enclosed
        if 'within3mAreaEnclosed' in data:
            within_3m_area_enclosed = data['within3mAreaEnclosed']
            chimney_height_clearance.within_3m_area_enclosed_required = within_3m_area_enclosed.get('requiredValue')
            chimney_height_clearance.within_3m_area_enclosed_present = within_3m_area_enclosed.get('presentValue')
            chimney_height_clearance.within_3m_area_enclosed_compliance = within_3m_area_enclosed.get('codeCompliance')
            chimney_height_clearance.within_3m_area_enclosed_photos = within_3m_area_enclosed.get('photos')

        # Update Final Note
        if 'finalNote' in data:
            final_note = data['finalNote']
            chimney_height_clearance.final_note_clearance_requirements = final_note.get('clearanceRequirements')
            chimney_height_clearance.final_note_required_value = final_note.get('requiredValue')
            chimney_height_clearance.final_note_present_value = final_note.get('presentValue')
            chimney_height_clearance.final_note_code_compliance = final_note.get('codeCompliance')
            chimney_height_clearance.final_note_photos = final_note.get('photos')
        
        chimney_height_clearance.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(chimney_height_clearance.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/chimney-height-clearance/<int:inspection_id>', methods=['DELETE'])
def delete_chimney_height_clearance(inspection_id):
    """Delete chimney height clearance for an inspection"""
    try:
        chimney_height_clearance = ChimneyHeightClearance.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_height_clearance:
            return jsonify({'error': 'Chimney height clearance not found'}), 404
        
        db.session.delete(chimney_height_clearance)
        db.session.commit()
        
        return jsonify({'message': 'Chimney height clearance deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fire Codes Compliance API Functions
@main.route('/api/fire-codes-compliance', methods=['POST'])
def create_fire_codes_compliance():
    try:
        from app.models import FireCodesCompliance
        
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400
        
        # Check if record already exists
        existing_record = FireCodesCompliance.query.filter_by(inspection_id=inspection_id).first()
        
        if existing_record:
            # Update existing record
            existing_record.fire_code_1_condition = data.get('fireCode1', {}).get('condition')
            existing_record.fire_code_1_comments = data.get('fireCode1', {}).get('comments')
            existing_record.fire_code_1_compliance = data.get('fireCode1', {}).get('codeCompliance')
            existing_record.fire_code_1_photos = data.get('fireCode1', {}).get('photos', [])
            
            existing_record.fire_code_2_condition = data.get('fireCode2', {}).get('condition')
            existing_record.fire_code_2_comments = data.get('fireCode2', {}).get('comments')
            existing_record.fire_code_2_compliance = data.get('fireCode2', {}).get('codeCompliance')
            existing_record.fire_code_2_photos = data.get('fireCode2', {}).get('photos', [])
            
            existing_record.fire_code_3_condition = data.get('fireCode3', {}).get('condition')
            existing_record.fire_code_3_comments = data.get('fireCode3', {}).get('comments')
            existing_record.fire_code_3_compliance = data.get('fireCode3', {}).get('codeCompliance')
            existing_record.fire_code_3_photos = data.get('fireCode3', {}).get('photos', [])
            
            existing_record.fire_code_4_condition = data.get('fireCode4', {}).get('condition')
            existing_record.fire_code_4_comments = data.get('fireCode4', {}).get('comments')
            existing_record.fire_code_4_compliance = data.get('fireCode4', {}).get('codeCompliance')
            existing_record.fire_code_4_photos = data.get('fireCode4', {}).get('photos', [])
            
            existing_record.updated_at = datetime.utcnow()
            
            db.session.commit()
            return jsonify(existing_record.to_dict()), 200
        
        # Create new record
        fire_codes = FireCodesCompliance(
            inspection_id=inspection_id,
            fire_code_1_condition=data.get('fireCode1', {}).get('condition'),
            fire_code_1_comments=data.get('fireCode1', {}).get('comments'),
            fire_code_1_compliance=data.get('fireCode1', {}).get('codeCompliance'),
            fire_code_1_photos=data.get('fireCode1', {}).get('photos', []),
            
            fire_code_2_condition=data.get('fireCode2', {}).get('condition'),
            fire_code_2_comments=data.get('fireCode2', {}).get('comments'),
            fire_code_2_compliance=data.get('fireCode2', {}).get('codeCompliance'),
            fire_code_2_photos=data.get('fireCode2', {}).get('photos', []),
            
            fire_code_3_condition=data.get('fireCode3', {}).get('condition'),
            fire_code_3_comments=data.get('fireCode3', {}).get('comments'),
            fire_code_3_compliance=data.get('fireCode3', {}).get('codeCompliance'),
            fire_code_3_photos=data.get('fireCode3', {}).get('photos', []),
            
            fire_code_4_condition=data.get('fireCode4', {}).get('condition'),
            fire_code_4_comments=data.get('fireCode4', {}).get('comments'),
            fire_code_4_compliance=data.get('fireCode4', {}).get('codeCompliance'),
            fire_code_4_photos=data.get('fireCode4', {}).get('photos', [])
        )
        
        db.session.add(fire_codes)
        db.session.commit()
        
        return jsonify(fire_codes.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fire-codes-compliance/<int:inspection_id>', methods=['GET'])
def get_fire_codes_compliance(inspection_id):
    try:
        from app.models import FireCodesCompliance
        
        fire_codes = FireCodesCompliance.query.filter_by(inspection_id=inspection_id).first()
        if not fire_codes:
            return jsonify({'error': 'Fire codes compliance not found'}), 404
        
        return jsonify(fire_codes.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fire-codes-compliance/<int:inspection_id>', methods=['PUT'])
def update_fire_codes_compliance(inspection_id):
    try:
        from app.models import FireCodesCompliance
        
        fire_codes = FireCodesCompliance.query.filter_by(inspection_id=inspection_id).first()
        if not fire_codes:
            return jsonify({'error': 'Fire codes compliance not found'}), 404
        
        data = request.get_json()
        
        # Update Fire Code 1
        if 'fireCode1' in data:
            fire_codes.fire_code_1_condition = data['fireCode1'].get('condition')
            fire_codes.fire_code_1_comments = data['fireCode1'].get('comments')
            fire_codes.fire_code_1_compliance = data['fireCode1'].get('codeCompliance')
            fire_codes.fire_code_1_photos = data['fireCode1'].get('photos', [])
        
        # Update Fire Code 2
        if 'fireCode2' in data:
            fire_codes.fire_code_2_condition = data['fireCode2'].get('condition')
            fire_codes.fire_code_2_comments = data['fireCode2'].get('comments')
            fire_codes.fire_code_2_compliance = data['fireCode2'].get('codeCompliance')
            fire_codes.fire_code_2_photos = data['fireCode2'].get('photos', [])
        
        # Update Fire Code 3
        if 'fireCode3' in data:
            fire_codes.fire_code_3_condition = data['fireCode3'].get('condition')
            fire_codes.fire_code_3_comments = data['fireCode3'].get('comments')
            fire_codes.fire_code_3_compliance = data['fireCode3'].get('codeCompliance')
            fire_codes.fire_code_3_photos = data['fireCode3'].get('photos', [])
        
        # Update Fire Code 4
        if 'fireCode4' in data:
            fire_codes.fire_code_4_condition = data['fireCode4'].get('condition')
            fire_codes.fire_code_4_comments = data['fireCode4'].get('comments')
            fire_codes.fire_code_4_compliance = data['fireCode4'].get('codeCompliance')
            fire_codes.fire_code_4_photos = data['fireCode4'].get('photos', [])
        
        fire_codes.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(fire_codes.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fire-codes-compliance/<int:inspection_id>', methods=['DELETE'])
def delete_fire_codes_compliance(inspection_id):
    try:
        from app.models import FireCodesCompliance
        
        fire_codes = FireCodesCompliance.query.filter_by(inspection_id=inspection_id).first()
        if not fire_codes:
            return jsonify({'error': 'Fire codes compliance not found'}), 404
        
        db.session.delete(fire_codes)
        db.session.commit()
        
        return jsonify({'message': 'Fire codes compliance deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Report Details API Functions
@main.route('/api/report-details', methods=['POST'])
def create_report_details():
    try:
        from app.models import ReportDetails
        
        data = request.get_json()
        print(f"DEBUG: Received report details data: {data}")
        
        inspection_id = data.get('inspection_id')
        
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400
        
        # Check if record already exists
        existing_record = ReportDetails.query.filter_by(inspection_id=inspection_id).first()
        
        if existing_record:
            # Update existing record
            customer_sig = data.get('customerSignature')
            inspector_sig = data.get('inspectorSignature')
            
            print(f"DEBUG: Updating existing record with customer signature length: {len(str(customer_sig)) if customer_sig else 0}")
            print(f"DEBUG: Updating existing record with inspector signature length: {len(str(inspector_sig)) if inspector_sig else 0}")
            
            # Validate signatures are not identical (if both provided)
            if customer_sig and inspector_sig and customer_sig == inspector_sig:
                print("WARNING: Customer and inspector signatures are identical - this may indicate a problem")
                return jsonify({
                    'error': 'Customer and inspector signatures cannot be identical',
                    'code': 'DUPLICATE_SIGNATURES'
                }), 400
            
            existing_record.photos_taken = data.get('photosTaken')
            existing_record.number_of_photos_taken = data.get('numberOfPhotosTaken')
            existing_record.number_of_photos_in_checklist = data.get('numberOfPhotosInChecklist')
            existing_record.number_of_photos_in_reports = data.get('numberOfPhotosInReports')
            existing_record.comments_observations = data.get('commentsObservations')
            existing_record.customer_signature = customer_sig
            existing_record.customer_signature_date = data.get('customerSignatureDate')
            existing_record.inspector_signature = inspector_sig
            existing_record.inspector_signature_date = data.get('inspectorSignatureDate')
            existing_record.updated_at = datetime.utcnow()
            
            print(f"DEBUG: After update - customer signature length: {len(str(existing_record.customer_signature)) if existing_record.customer_signature else 0}")
            print(f"DEBUG: After update - inspector signature length: {len(str(existing_record.inspector_signature)) if existing_record.inspector_signature else 0}")
            print(f"DEBUG: After update - signatures are same: {existing_record.customer_signature == existing_record.inspector_signature}")
            
            db.session.commit()
            return jsonify(existing_record.to_dict()), 200
        
        # Create new record
        customer_sig = data.get('customerSignature')
        inspector_sig = data.get('inspectorSignature')
        
        print(f"DEBUG: Creating new record with customer signature length: {len(str(customer_sig)) if customer_sig else 0}")
        print(f"DEBUG: Creating new record with inspector signature length: {len(str(inspector_sig)) if inspector_sig else 0}")
        
        # Validate signatures are not identical (if both provided)
        if customer_sig and inspector_sig and customer_sig == inspector_sig:
            print("WARNING: Customer and inspector signatures are identical - this may indicate a problem")
            return jsonify({
                'error': 'Customer and inspector signatures cannot be identical',
                'code': 'DUPLICATE_SIGNATURES'
            }), 400
        
        report_details = ReportDetails(
            inspection_id=inspection_id,
            photos_taken=data.get('photosTaken'),
            number_of_photos_taken=data.get('numberOfPhotosTaken'),
            number_of_photos_in_checklist=data.get('numberOfPhotosInChecklist'),
            number_of_photos_in_reports=data.get('numberOfPhotosInReports'),
            comments_observations=data.get('commentsObservations'),
            customer_signature=customer_sig,
            customer_signature_date=data.get('customerSignatureDate'),
            inspector_signature=inspector_sig,
            inspector_signature_date=data.get('inspectorSignatureDate')
        )
        
        print(f"DEBUG: After creation - customer signature length: {len(str(report_details.customer_signature)) if report_details.customer_signature else 0}")
        print(f"DEBUG: After creation - inspector signature length: {len(str(report_details.inspector_signature)) if report_details.inspector_signature else 0}")
        print(f"DEBUG: After creation - signatures are same: {report_details.customer_signature == report_details.inspector_signature}")
        
        db.session.add(report_details)
        db.session.commit()
        
        return jsonify(report_details.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/report-details/<int:inspection_id>', methods=['GET'])
def get_report_details(inspection_id):
    try:
        from app.models import ReportDetails
        
        report_details = ReportDetails.query.filter_by(inspection_id=inspection_id).first()
        if not report_details:
            return jsonify({'error': 'Report details not found'}), 404
        
        return jsonify(report_details.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/report-details/<int:inspection_id>', methods=['PUT'])
def update_report_details(inspection_id):
    try:
        data = request.get_json()
        report_details = ReportDetails.query.filter_by(inspection_id=inspection_id).first()
        if not report_details:
            return jsonify({'error': 'Report details not found'}), 404
        
        if 'photosTaken' in data:
            report_details.photos_taken = data['photosTaken']
        if 'numberOfPhotosTaken' in data:
            report_details.number_of_photos_taken = data['numberOfPhotosTaken']
        if 'numberOfPhotosInChecklist' in data:
            report_details.number_of_photos_in_checklist = data['numberOfPhotosInChecklist']
        if 'numberOfPhotosInReports' in data:
            report_details.number_of_photos_in_reports = data['numberOfPhotosInReports']
        if 'commentsObservations' in data:
            report_details.comments_observations = data['commentsObservations']
        if 'customerSignature' in data:
            report_details.customer_signature = data['customerSignature']
        if 'customerSignatureDate' in data:
            report_details.customer_signature_date = data['customerSignatureDate']
        if 'inspectorSignature' in data:
            report_details.inspector_signature = data['inspectorSignature']
        if 'inspectorSignatureDate' in data:
            report_details.inspector_signature_date = data['inspectorSignatureDate']
        
        db.session.commit()
        return jsonify(report_details.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/report-details/<int:inspection_id>', methods=['DELETE'])
def delete_report_details(inspection_id):
    try:
        report_details = ReportDetails.query.filter_by(inspection_id=inspection_id).first()
        if not report_details:
            return jsonify({'error': 'Report details not found'}), 404
        
        db.session.delete(report_details)
        db.session.commit()
        
        return jsonify({'message': 'Report details deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/generate-report/<int:inspection_id>', methods=['GET'])
def generate_pdf_report(inspection_id):
    """Generate PDF report using the new integrated PDF generation system"""
    try:
        # Import necessary modules for backward compatibility
        from flask import make_response
        import io
        import base64
        import os
        from datetime import datetime
        
        # Use the new integrated PDF generation system
        # We'll call the internal PDF generation method instead of using external API calls
        
        # Fetch inspection data directly from database (similar to old approach)
        from app.models import (
            Inspection, User, Inspector, Company, ChimneySpecification,
            FireplaceSpecification, CombustibleMaterials, HearthFloorProtection,
            EnclosureVentilation, FireplaceSafetyFeatures, ChimneySupportConnection,
            AtticRadiationProtection, RoofExteriorProtection, ChimneyHeightClearance,
            FireCodesCompliance, ReportDetails, PelletInsertChimneySpecification,
            PelletInsertChimneyStabilityCaps, PelletInsertChimneySupportConnection,
            PelletInsertChimneySupports, PelletInsertCOAlarmsLiners, PelletInsertEmberPadFloorProtection, PelletInsertFireplaceSafetyFeatures, PelletInsertFireplaceSpecifications,             PelletInsertLinerApplianceChecks1, PelletInsertLinerApplianceChecks2, PelletInsertLinerVentComponents, PelletInsertMasonryFireplaceConstruction1, PelletInsertMasonryFireplaceConstruction2, PelletInsertMaterialsClearances,
            PelletInsertChimneyJointsLinerDetails, PelletInsertChimneyLiners,
            WoodStoveManufacturedChimneyComponentsSupports, WoodStoveManufacturedChimneyInspection,
            WoodStoveManufacturedChimneyStructureClearances, WoodStoveManufacturedClearancesShielding,
            WoodStoveManufacturedCombustionAirCOAlarm, WoodStoveManufacturedEmberPadFloorProtection,
            WoodStoveManufacturedFireCodesCompliance, WoodStoveManufacturedFluePipeChimneyConnection,
            WoodStoveManufacturedFluePipeComponents, WoodStoveManufacturedFluePipeInfoClearances,
            WoodStoveManufacturedFluePipeOrientationJoints, WoodStoveMasonryChimneyConstructionLiners,
            WoodStoveMasonryChimneyConstruction, WoodStoveMasonryChimneyLinersInstallation, WoodStoveMasonryChimneyLiners, WoodStoveMasonryChimneySaddles, WoodStoveMasonryChimneySpecifications, WoodStoveMasonryChimneyStabilityCaps
        )
        
        # Get inspection and verify it exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404
        
        # Get user and related data
        user = User.query.get(inspection.user_id)
        if not user:
            return jsonify({'error': 'User not found for this inspection'}), 404
            
        # Build inspection data structure for new PDF generator
        inspection_data = inspection.to_dict()
        
        # Ensure all inspection fields are properly included
        print(f"DEBUG: Original inspection client_name: '{inspection.client_name}'")
        print(f"DEBUG: Original inspection title: '{inspection.title}'")
        print(f"DEBUG: Original inspection form_data: {inspection.form_data}")
        
        # Extract client name from form_data if not in main field (for backward compatibility)
        client_name = inspection.client_name
        if not client_name and inspection.form_data:
            requested_by = inspection.form_data.get('requestedBy', {})
            if requested_by and requested_by.get('name'):
                client_name = requested_by['name']
                print(f"DEBUG: Extracted client_name from form_data: '{client_name}'")
        
        # Determine form type display name
        form_type_display = {
            'factory-built': 'Factory-Built Fireplace',
            'fireplace-insert': 'Fireplace Insert',
            'masonry': 'Masonry Fireplace',
            'pellet-insert': 'Pellet Insert',
            'wood-stove-manufactured': 'Manufactured Wood Stove',
            'wood-stove-masonry': 'Masonry Wood Stove'
        }.get(inspection.form_type or 'factory-built', 'Standard Inspection')

        inspection_data.update({
            'title': inspection.title or 'Inspection Report',
            'client_name': client_name or 'Not specified',
            'client_address': inspection.client_address or 'Not specified',
            'inspection_date': inspection.inspection_date.strftime('%Y-%m-%d') if inspection.inspection_date else None,
            'form_type': form_type_display,
            'status': inspection.status or 'draft'
        })
        
        print(f"DEBUG: Final inspection_data client_name: '{inspection_data.get('client_name')}'")
        print(f"DEBUG: Final inspection_data title: '{inspection_data.get('title')}')")
        
        # Add all related form sections to inspection_data based on form_type
        form_type = inspection.form_type

        if form_type == 'fireplace-insert':
            # Fetch fireplace-insert specific data
            if inspection.fireplace_insert_chimney_specifications:
                inspection_data['chimneySpecification'] = [spec.to_dict() for spec in inspection.fireplace_insert_chimney_specifications]

            if inspection.fireplace_insert_fireplace_specifications:
                inspection_data['fireplaceSpecification'] = [spec.to_dict() for spec in inspection.fireplace_insert_fireplace_specifications]

            if inspection.fireplace_insert_materials_clearances:
                inspection_data['materialsClearances'] = inspection.fireplace_insert_materials_clearances.to_dict()

            if inspection.fireplace_insert_ember_pad_floor_protection:
                inspection_data['emberPadFloorProtection'] = inspection.fireplace_insert_ember_pad_floor_protection.to_dict()

            if inspection.fireplace_insert_fireplace_safety_features:
                inspection_data['fireplaceSafetyFeatures'] = inspection.fireplace_insert_fireplace_safety_features.to_dict()

            if inspection.fireplace_insert_chimney_support_connection:
                inspection_data['chimneySupportConnection'] = inspection.fireplace_insert_chimney_support_connection.to_dict()

            if inspection.fireplace_insert_liner_appliance_checks:
                inspection_data['linerApplianceChecks'] = inspection.fireplace_insert_liner_appliance_checks.to_dict()

            if inspection.fireplace_insert_appliance_masonry_checks:
                inspection_data['applianceMasonryChecks'] = inspection.fireplace_insert_appliance_masonry_checks.to_dict()

            if inspection.fireplace_insert_co_alarms_liners:
                inspection_data['coAlarmsLiners'] = inspection.fireplace_insert_co_alarms_liners.to_dict()

            if inspection.fireplace_insert_chimney_liner_joints_details:
                inspection_data['chimneyLinerJointsDetails'] = inspection.fireplace_insert_chimney_liner_joints_details.to_dict()

            if inspection.fireplace_insert_hearth_support:
                inspection_data['hearthSupport'] = inspection.fireplace_insert_hearth_support.to_dict()

            if inspection.fireplace_insert_clearances:
                inspection_data['clearances'] = inspection.fireplace_insert_clearances.to_dict()

            if inspection.fireplace_insert_clearances_liners:
                inspection_data['clearancesLiners'] = inspection.fireplace_insert_clearances_liners.to_dict()

            if inspection.fireplace_insert_liner_details:
                inspection_data['linerDetails'] = inspection.fireplace_insert_liner_details.to_dict()

            if inspection.fireplace_insert_joints_details:
                inspection_data['jointsDetails'] = inspection.fireplace_insert_joints_details.to_dict()

            if inspection.fireplace_insert_chimney_height_clearance:
                inspection_data['chimneyHeightClearance'] = inspection.fireplace_insert_chimney_height_clearance.to_dict()

            if inspection.fireplace_insert_chimney_supports:
                inspection_data['chimneySupports'] = inspection.fireplace_insert_chimney_supports.to_dict()

            if inspection.fireplace_insert_chimney_saddles_fire_code:
                inspection_data['chimneySaddlesFireCode'] = inspection.fireplace_insert_chimney_saddles_fire_code.to_dict()

            # Report details for fireplace-insert (uses the same ReportDetails model)
            if inspection.report_details:
                report_details_data = inspection.report_details.to_dict()
                print(f"DEBUG: Report Details from database: {report_details_data}")
                inspection_data['reportDetails'] = report_details_data

        elif form_type == 'masonry':
            # Fetch masonry specific data
            if inspection.masonry_chimney_specifications:
                inspection_data['masonryChimneySpecification'] = inspection.masonry_chimney_specifications.to_dict()

            if inspection.masonry_fireplace_specifications:
                inspection_data['masonryFireplaceSpecification'] = inspection.masonry_fireplace_specifications.to_dict()

            if inspection.masonry_fireplace_construction_details:
                inspection_data['masonryFireplaceConstructionDetails'] = inspection.masonry_fireplace_construction_details.to_dict()

            if inspection.masonry_combustion_air_requirements:
                inspection_data['masonryCombustionAirRequirements'] = inspection.masonry_combustion_air_requirements.to_dict()

            if inspection.masonry_chimney_structure:
                inspection_data['masonryChimneyStructure'] = inspection.masonry_chimney_structure.to_dict()

            if inspection.masonry_hearth_construction:
                inspection_data['masonryHearthConstruction'] = inspection.masonry_hearth_construction.to_dict()

            if inspection.masonry_fireplace_components:
                inspection_data['masonryFireplaceComponents'] = inspection.masonry_fireplace_components.to_dict()

            if inspection.masonry_fireplace_clearances:
                inspection_data['masonryFireplaceClearances'] = inspection.masonry_fireplace_clearances.to_dict()

            if inspection.masonry_chimney_liners_installation:
                inspection_data['masonryChimneyLinersInstallation'] = inspection.masonry_chimney_liners_installation.to_dict()

            if inspection.masonry_joint_details:
                inspection_data['masonryJointDetails'] = inspection.masonry_joint_details.to_dict()

            if inspection.masonry_chimney_stability_caps:
                inspection_data['masonryChimneyStabilityCaps'] = inspection.masonry_chimney_stability_caps.to_dict()

            if inspection.masonry_clearances_supports:
                inspection_data['masonryClearancesSupports'] = inspection.masonry_clearances_supports.to_dict()

            if inspection.masonry_chimney_saddles_fire_code:
                inspection_data['masonryChimneySaddlesFireCode'] = inspection.masonry_chimney_saddles_fire_code.to_dict()

            if inspection.masonry_co_alarms:
                inspection_data['masonryCOAlarms'] = inspection.masonry_co_alarms.to_dict()

            # Report details for masonry (uses the same ReportDetails model)
            if inspection.report_details:
                report_details_data = inspection.report_details.to_dict()
                print(f"DEBUG: Report Details from database: {report_details_data}")
                inspection_data['reportDetails'] = report_details_data

        elif form_type == 'pellet-insert':
            # Fetch pellet insert specific data
            if inspection.pellet_insert_chimney_liners:
                inspection_data['pelletInsertChimneyLiners'] = inspection.pellet_insert_chimney_liners.to_dict()

            if inspection.pellet_insert_chimney_joints_liner_details:
                inspection_data['pelletInsertChimneyJointsLinerDetails'] = inspection.pellet_insert_chimney_joints_liner_details.to_dict()

            if inspection.pellet_insert_chimney_saddles_fire_code:
                inspection_data['pelletInsertChimneySaddlesFireCode'] = inspection.pellet_insert_chimney_saddles_fire_code.to_dict()

            if inspection.pellet_insert_chimney_specifications:
                inspection_data['pelletInsertChimneySpecifications'] = inspection.pellet_insert_chimney_specifications.to_dict()

            if inspection.pellet_insert_chimney_stability_caps:
                inspection_data['pelletInsertChimneyStabilityCaps'] = inspection.pellet_insert_chimney_stability_caps.to_dict()

            if inspection.pellet_insert_chimney_support_connection:
                inspection_data['pelletInsertChimneySupportConnection'] = inspection.pellet_insert_chimney_support_connection.to_dict()

            if inspection.pellet_insert_chimney_supports:
                inspection_data['pelletInsertChimneySupports'] = inspection.pellet_insert_chimney_supports.to_dict()

            if inspection.pellet_insert_co_alarms_liners:
                inspection_data['pelletInsertCOAlarmsLiners'] = inspection.pellet_insert_co_alarms_liners.to_dict()

            if inspection.pellet_insert_ember_pad_floor_protection:
                inspection_data['pelletInsertEmberPadFloorProtection'] = inspection.pellet_insert_ember_pad_floor_protection.to_dict()

            if inspection.pellet_insert_fireplace_safety_features:
                inspection_data['pelletInsertFireplaceSafetyFeatures'] = inspection.pellet_insert_fireplace_safety_features.to_dict()

            if inspection.pellet_insert_fireplace_specifications:
                inspection_data['pelletInsertFireplaceSpecifications'] = inspection.pellet_insert_fireplace_specifications.to_dict()

            if inspection.pellet_insert_liner_appliance_checks_1:
                inspection_data['pelletInsertLinerApplianceChecks1'] = inspection.pellet_insert_liner_appliance_checks_1.to_dict()

            if inspection.pellet_insert_liner_appliance_checks_2:
                inspection_data['pelletInsertLinerApplianceChecks2'] = inspection.pellet_insert_liner_appliance_checks_2.to_dict()

            if inspection.pellet_insert_liner_vent_components:
                inspection_data['pelletInsertLinerVentComponents'] = inspection.pellet_insert_liner_vent_components.to_dict()

            if inspection.pellet_insert_masonry_fireplace_construction_1:
                inspection_data['pelletInsertMasonryFireplaceConstruction1'] = inspection.pellet_insert_masonry_fireplace_construction_1.to_dict()

            if inspection.pellet_insert_masonry_fireplace_construction_2:
                inspection_data['pelletInsertMasonryFireplaceConstruction2'] = inspection.pellet_insert_masonry_fireplace_construction_2.to_dict()

            if inspection.pellet_insert_materials_clearances:
                inspection_data['pelletInsertMaterialsClearances'] = inspection.pellet_insert_materials_clearances.to_dict()

            # Report details for pellet insert (uses the same ReportDetails model)
            if inspection.report_details:
                report_details_data = inspection.report_details.to_dict()
                print(f"DEBUG: Report Details from database: {report_details_data}")
                inspection_data['reportDetails'] = report_details_data

        elif form_type == 'wood-stove-manufactured':
            # Fetch wood stove manufactured specific data
            if inspection.wood_stove_manufactured_chimney_inspection:
                inspection_data['woodStoveManufacturedChimneyInspection'] = inspection.wood_stove_manufactured_chimney_inspection.to_dict()

            if inspection.wood_stove_manufactured_chimney_components_supports:
                inspection_data['woodStoveManufacturedChimneyComponentsSupports'] = inspection.wood_stove_manufactured_chimney_components_supports.to_dict()

            if inspection.wood_stove_manufactured_chimney_structure_clearances:
                inspection_data['woodStoveManufacturedChimneyStructureClearances'] = inspection.wood_stove_manufactured_chimney_structure_clearances.to_dict()

            if inspection.wood_stove_manufactured_clearances_shielding:
                inspection_data['woodStoveManufacturedClearancesShielding'] = inspection.wood_stove_manufactured_clearances_shielding.to_dict()

            if inspection.wood_stove_manufactured_combustion_air_co_alarm:
                inspection_data['woodStoveManufacturedCombustionAirCOAlarm'] = inspection.wood_stove_manufactured_combustion_air_co_alarm.to_dict()

            if inspection.wood_stove_manufactured_ember_pad_floor_protection:
                inspection_data['woodStoveManufacturedEmberPadFloorProtection'] = inspection.wood_stove_manufactured_ember_pad_floor_protection.to_dict()

            if inspection.wood_stove_manufactured_fire_codes_compliance:
                inspection_data['woodStoveManufacturedFireCodesCompliance'] = inspection.wood_stove_manufactured_fire_codes_compliance.to_dict()

            if inspection.wood_stove_manufactured_flue_pipe_chimney_connection:
                inspection_data['woodStoveManufacturedFluePipeChimneyConnection'] = inspection.wood_stove_manufactured_flue_pipe_chimney_connection.to_dict()

            if inspection.wood_stove_manufactured_flue_pipe_components:
                inspection_data['woodStoveManufacturedFluePipeComponents'] = inspection.wood_stove_manufactured_flue_pipe_components.to_dict()

            if inspection.wood_stove_manufactured_flue_pipe_info_clearances:
                inspection_data['woodStoveManufacturedFluePipeInfoClearances'] = inspection.wood_stove_manufactured_flue_pipe_info_clearances.to_dict()

            if inspection.wood_stove_manufactured_flue_pipe_orientation_joints:
                inspection_data['woodStoveManufacturedFluePipeOrientationJoints'] = inspection.wood_stove_manufactured_flue_pipe_orientation_joints.to_dict()

            # Report details for wood stove manufactured (uses the same ReportDetails model)
            if inspection.report_details:
                report_details_data = inspection.report_details.to_dict()
                print(f"DEBUG: Report Details from database: {report_details_data}")
                inspection_data['reportDetails'] = report_details_data

        elif form_type == 'wood-stove-masonry':
            # Fetch wood stove masonry specific data
            if inspection.wood_stove_masonry_chimney_construction:
                inspection_data['woodStoveMasonryChimneyConstruction'] = inspection.wood_stove_masonry_chimney_construction.to_dict()

            if inspection.wood_stove_masonry_chimney_construction_liners:
                inspection_data['woodStoveMasonryChimneyConstructionLiners'] = inspection.wood_stove_masonry_chimney_construction_liners.to_dict()

            if inspection.wood_stove_masonry_chimney_liners_installation:
                inspection_data['woodStoveMasonryChimneyLinersInstallation'] = inspection.wood_stove_masonry_chimney_liners_installation.to_dict()

            if inspection.wood_stove_masonry_chimney_liners:
                inspection_data['woodStoveMasonryChimneyLiners'] = inspection.wood_stove_masonry_chimney_liners.to_dict()

            if inspection.wood_stove_masonry_chimney_saddles:
                inspection_data['woodStoveMasonryChimneySaddles'] = inspection.wood_stove_masonry_chimney_saddles.to_dict()

            if inspection.wood_stove_masonry_chimney_specifications:
                inspection_data['woodStoveMasonryChimneySpecifications'] = inspection.wood_stove_masonry_chimney_specifications.to_dict()

            if inspection.wood_stove_masonry_chimney_stability_caps:
                inspection_data['woodStoveMasonryChimneyStabilityCaps'] = inspection.wood_stove_masonry_chimney_stability_caps.to_dict()

            # Report details for wood stove masonry (uses the same ReportDetails model)
            if inspection.report_details:
                report_details_data = inspection.report_details.to_dict()
                print(f"DEBUG: Report Details from database: {report_details_data}")
                inspection_data['reportDetails'] = report_details_data

        else:
            # Fetch factory-built data (existing logic)
            if inspection.chimney_specifications:
                inspection_data['chimneySpecification'] = [spec.to_dict() for spec in inspection.chimney_specifications]

            if inspection.fireplace_specifications:
                inspection_data['fireplaceSpecification'] = [spec.to_dict() for spec in inspection.fireplace_specifications]

            if inspection.combustible_materials:
                inspection_data['combustibleMaterials'] = [materials.to_dict() for materials in inspection.combustible_materials]

            if inspection.hearth_floor_protection:
                inspection_data['hearthFloorProtection'] = inspection.hearth_floor_protection.to_dict()
        
            if inspection.enclosure_ventilation:
                inspection_data['enclosureVentilation'] = inspection.enclosure_ventilation.to_dict()

            if inspection.fireplace_safety_features:
                inspection_data['fireplaceSafetyFeatures'] = inspection.fireplace_safety_features.to_dict()

            if inspection.chimney_support_connection:
                inspection_data['chimneySupportConnection'] = inspection.chimney_support_connection.to_dict()

            if inspection.attic_radiation_protection:
                inspection_data['atticRadiationProtection'] = inspection.attic_radiation_protection.to_dict()

            if inspection.roof_exterior_protection:
                inspection_data['roofExteriorProtection'] = inspection.roof_exterior_protection.to_dict()

            if inspection.chimney_height_clearance:
                inspection_data['chimneyHeightClearance'] = inspection.chimney_height_clearance.to_dict()

            if inspection.fire_codes_compliance:
                inspection_data['fireCodesCompliance'] = inspection.fire_codes_compliance.to_dict()

            if inspection.report_details:
                report_details_data = inspection.report_details.to_dict()
                print(f"DEBUG: Report Details from database: {report_details_data}")
                inspection_data['reportDetails'] = report_details_data
        
        # Build user data structure
        user_data = user.to_dict()
        if user.inspector:
            user_data['inspector'] = user.inspector.to_dict()
        if user.company:
            user_data['company'] = user.company.to_dict()
        
        # Use the new PDF generation system (import from the updated main.py location)
        # Since we're integrating this, we'll create the PDF generator class here
        try:
            # Import the new PDF generation class
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
            from PIL import Image as PILImage
            
            # Create the integrated PDF generation class
            class SHFInspectionReportPDF:
                def __init__(self):
                    self.styles = getSampleStyleSheet()
                    self.setup_custom_styles()
                    
                def setup_custom_styles(self):
                    """Setup custom styles for the PDF with SHF branding"""
                    # Define SHF brand colors
                    primary_color = colors.HexColor('#F59E42')  # SHF Orange
                    secondary_color = colors.HexColor('#374151')  # Dark gray
                    accent_color = colors.HexColor('#845EF7')  # Purple
                    
                    # Title style
                    self.styles.add(ParagraphStyle(
                        name='SHFTitle',
                        parent=self.styles['Title'],
                        fontSize=24,
                        spaceAfter=30,
                        alignment=TA_CENTER,
                        textColor=primary_color,
                        fontName='Helvetica-Bold'
                    ))
                    
                    # Section header style
                    self.styles.add(ParagraphStyle(
                        name='SHFSectionHeader',
                        parent=self.styles['Heading1'],
                        fontSize=16,
                        spaceAfter=12,
                        spaceBefore=20,
                        textColor=secondary_color,
                        fontName='Helvetica-Bold',
                        borderWidth=1,
                        borderColor=primary_color,
                        borderPadding=8,
                        backColor=colors.HexColor('#F3F4F6')
                    ))
                    
                    # Subsection header style
                    self.styles.add(ParagraphStyle(
                        name='SHFSubsectionHeader',
                        parent=self.styles['Heading2'],
                        fontSize=14,
                        spaceAfter=8,
                        spaceBefore=12,
                        textColor=accent_color,
                        fontName='Helvetica-Bold'
                    ))
                    
                    # Field styles
                    self.styles.add(ParagraphStyle(
                        name='SHFFieldLabel',
                        parent=self.styles['Normal'],
                        fontSize=10,
                        textColor=colors.black,
                        fontName='Helvetica-Bold'
                    ))
                    
                    self.styles.add(ParagraphStyle(
                        name='SHFFieldValue',
                        parent=self.styles['Normal'],
                        fontSize=10,
                        textColor=colors.black
                    ))
                    
                    # Compliance styles with SHF colors
                    self.styles.add(ParagraphStyle(
                        name='SHFComplianceYes',
                        parent=self.styles['Normal'],
                        fontSize=10,
                        textColor=colors.green,
                        fontName='Helvetica-Bold'
                    ))
                    
                    self.styles.add(ParagraphStyle(
                        name='SHFComplianceNo',
                        parent=self.styles['Normal'],
                        fontSize=10,
                        textColor=colors.red,
                        fontName='Helvetica-Bold'
                    ))

                def base64_to_image(self, base64_string, max_width=300, max_height=200):
                    """Convert base64 string or URL to ReportLab Image with enhanced error handling"""
                    try:
                        if not base64_string or not isinstance(base64_string, str):
                            return None
                        
                        # If it's a URL, fetch image bytes
                        if base64_string.startswith('http://') or base64_string.startswith('https://'):
                            try:
                                import requests
                                resp = requests.get(base64_string, timeout=10)
                                if resp.status_code != 200:
                                    return None
                                image_data = resp.content
                            except Exception as fetch_err:
                                print(f"Error fetching image URL: {fetch_err}")
                                return None
                        else:
                            # Handle data URL format
                            if base64_string.startswith('data:image/'):
                                base64_string = base64_string.split(',')[1]
                            
                            # Clean and validate base64 data
                            base64_string = base64_string.strip()
                            
                            # Fix padding
                            padding_needed = 4 - (len(base64_string) % 4)
                            if padding_needed != 4:
                                base64_string += '=' * padding_needed
                            
                            # Decode base64
                            image_data = base64.b64decode(base64_string)
                        
                        # Validate image data
                        if len(image_data) < 10:
                            return None
                            
                        # Check for valid image headers
                        is_valid_image = (
                            image_data.startswith(b'\xff\xd8\xff') or  # JPEG
                            image_data.startswith(b'\x89PNG') or       # PNG
                            image_data.startswith(b'GIF87a') or        # GIF
                            image_data.startswith(b'GIF89a') or        # GIF
                            (image_data.startswith(b'RIFF') and b'WEBP' in image_data[:12])  # WEBP
                        )
                        
                        if not is_valid_image:
                            return None
                        
                        # Process with PIL
                        pil_image = PILImage.open(io.BytesIO(image_data))
                        
                        # Convert to RGB if needed
                        if pil_image.mode in ('RGBA', 'LA', 'P'):
                            background = PILImage.new('RGB', pil_image.size, (255, 255, 255))
                            if pil_image.mode == 'P':
                                pil_image = pil_image.convert('RGBA')
                            if pil_image.mode in ('RGBA', 'LA'):
                                background.paste(pil_image, mask=pil_image.split()[-1])
                            else:
                                background.paste(pil_image)
                            pil_image = background
                        elif pil_image.mode != 'RGB':
                            pil_image = pil_image.convert('RGB')
                        
                        # Resize if needed
                        pil_image.thumbnail((max_width, max_height), PILImage.Resampling.LANCZOS)
                        
                        # Save to BytesIO
                        img_buffer = io.BytesIO()
                        pil_image.save(img_buffer, format='JPEG', quality=85)
                        img_buffer.seek(0)
                        
                        # Create ReportLab Image
                        return Image(img_buffer, width=pil_image.width, height=pil_image.height)
                        
                    except Exception as e:
                        print(f"Error converting base64/URL to image: {e}")
                        return None

                def format_compliance_status(self, status):
                    """Format compliance status with SHF styling"""
                    if not status:
                        return Paragraph("N/A", self.styles['SHFFieldValue'])
                    
                    if not isinstance(status, str):
                        status = str(status)
                    
                    status_map = {
                        'yes': ('✅ YES - COMPLIANT', 'SHFComplianceYes'),
                        'no': ('❌ NO - NON-COMPLIANT', 'SHFComplianceNo'),
                        'ufi': ('⚠️ UNABLE TO INSPECT', 'SHFFieldValue'),
                        'na': ('N/A - NOT APPLICABLE', 'SHFFieldValue')
                    }
                    
                    status_text, style = status_map.get(status.lower(), (status.upper(), 'SHFFieldValue'))
                    return Paragraph(status_text, self.styles[style])

                def create_field_table(self, label, value, compliance=None):
                    """Create a formatted table for a field with robust error handling"""
                    try:
                        # DEBUG: Print what we're processing
                        print(f"DEBUG: Processing field - Label: '{label}', Value type: {type(value)}, Value length: {len(str(value)) if value else 0}")
                        
                        # SAFETY: Clean and validate label first
                        if not isinstance(label, str):
                            label = str(label)
                        
                        # Clean the label and ensure it's safe
                        label = label.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
                        if len(label) > 100:
                            label = label[:100] + "..."
                        
                        # Format value properly
                        if value is None:
                            formatted_value = "Not specified"
                        elif isinstance(value, list):
                            formatted_value = ", ".join(str(v) for v in value if v)
                        elif isinstance(value, dict):
                            # Handle nested dict structures from the new API format
                            if 'requiredValue' in value:
                                formatted_value = value.get('requiredValue', 'Not specified')
                            elif 'presentValue' in value:
                                formatted_value = value.get('presentValue', 'Not specified')
                            else:
                                formatted_value = str(value)
                        else:
                            formatted_value = str(value)
                        
                        # CRITICAL: Prevent layout errors from long content
                        if isinstance(formatted_value, str):
                            # DEBUG: More detailed logging
                            if len(formatted_value) > 1000:
                                print(f"DEBUG: Large content detected - Label: '{label}', Length: {len(formatted_value)}")
                                print(f"DEBUG: Content preview: '{formatted_value[:200]}...'")
                            
                            # Handle signature fields specially (improved detection)
                            label_lower = label.lower()
                            is_signature_field = (
                                'signature' in label_lower or
                                'sign' in label_lower or
                                label_lower.endswith('signature') or
                                'customer' in label_lower and 'signature' in label_lower
                            )
                            
                            if is_signature_field:
                                print(f"DEBUG: Signature field detected: '{label}', Content length: {len(formatted_value)}")
                                # For signature fields, always use a safe display value
                                formatted_value = "✅ Digital signature captured"
                            
                            # Handle any base64 or data URI content
                            elif formatted_value.startswith('data:'):
                                print(f"DEBUG: Data URI detected: '{label}', Content length: {len(formatted_value)}")
                                if 'image' in formatted_value[:50]:
                                    formatted_value = "📷 Image attachment"
                                else:
                                    formatted_value = "📄 Data attachment"
                            
                            # AGGRESSIVE: Prevent any string from causing layout issues  
                            elif len(formatted_value) > 100:  # Very aggressive truncation
                                print(f"DEBUG: Long content truncated: '{label}', Original length: {len(formatted_value)}")
                                formatted_value = formatted_value[:100] + "... (truncated)"
                            
                            # Clean problematic characters that could cause layout issues
                            formatted_value = formatted_value.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
                            
                            # FINAL SAFETY: Absolutely no content over 150 chars
                            if len(formatted_value) > 150:
                                formatted_value = "Content truncated for PDF layout"
                        
                        # Ensure both label and value are strings and reasonable length
                        safe_label = str(label)[:50]  # Truncate label aggressively
                        safe_value = str(formatted_value)[:200]  # Truncate value aggressively
                        
                        return self._create_safe_table(safe_label, safe_value, compliance)
                        
                    except Exception as e:
                        print(f"Error in create_field_table for label '{label}': {e}")
                        # Return a completely safe fallback table
                        return self._create_fallback_table(str(label)[:30], "Error displaying content")

                def _create_safe_table(self, label, value, compliance=None):
                    """Create table with extra safety measures"""
                    try:
                        # Final safety check on value
                        if len(str(value)) > 200:
                            value = str(value)[:200] + "..."
                        
                        # Create paragraphs with extra safety
                        try:
                            label_paragraph = Paragraph(f"<b>{label}:</b>", self.styles['SHFFieldLabel'])
                        except:
                            label_paragraph = Paragraph("<b>Field:</b>", self.styles['SHFFieldLabel'])
                        
                        try:
                            value_paragraph = Paragraph(str(value), self.styles['SHFFieldValue'])
                        except:
                            value_paragraph = Paragraph("Content unavailable", self.styles['SHFFieldValue'])
                        
                        if compliance:
                            data = [[
                                label_paragraph,
                                value_paragraph,
                                self.format_compliance_status(compliance)
                            ]]
                            col_widths = [2*inch, 3*inch, 1.5*inch]
                        else:
                            data = [[
                                label_paragraph,
                                value_paragraph
                            ]]
                            col_widths = [2*inch, 4.5*inch]
                        
                        table = Table(data, colWidths=col_widths)
                        table.setStyle(TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('FONTSIZE', (0, 0), (-1, -1), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                            ('TOPPADDING', (0, 0), (-1, -1), 2),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
                        ]))
                        
                        return table
                        
                    except Exception as e:
                        print(f"Error in _create_safe_table for {label}: {e}")
                        return self._create_fallback_table(label, "Display error")

                def _create_fallback_table(self, label, value):
                    """Create a completely safe fallback table"""
                    try:
                        # Use plain text instead of Paragraph to avoid any formatting issues
                        data = [[f"{label}:", str(value)]]
                        
                        table = Table(data, colWidths=[2*inch, 4.5*inch])
                        table.setStyle(TableStyle([
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('FONTSIZE', (0, 0), (-1, -1), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                            ('TOPPADDING', (0, 0), (-1, -1), 2),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
                        ]))
                        
                        return table
                        
                    except Exception as e:
                        print(f"Error even in fallback table: {e}")
                        # Return a spacer if all else fails
                        return Spacer(1, 20)

                def format_field_label(self, field_name):
                    """Convert field names to properly formatted labels with correct spacing"""
                    import re
                    
                    # Handle special cases
                    special_cases = {
                        # Main section names
                        'fireCode1': 'Fire Code 1',
                        'fireCode2': 'Fire Code 2', 
                        'fireCode3': 'Fire Code 3',
                        'fireCode4': 'Fire Code 4',
                        'hearthFloorProtection': 'Hearth & Floor Protection',
                        'enclosureVentilation': 'Enclosure & Ventilation',
                        'chimneySupportConnection': 'Chimney Support & Connection',
                        'atticRadiationProtection': 'Attic & Radiation Protection',
                        'roofExteriorProtection': 'Roof & Exterior Protection',
                        'chimneyHeightClearance': 'Chimney Height & Clearance',
                        'fireCodesCompliance': 'Fire Codes Compliance',
                        'reportDetails': 'Report Details',
                        
                        # Common sub-heading field names
                        'ceilingHeight': 'Ceiling Height',
                        'fireplaceEnclosured': 'Fireplace Enclosured',
                        'clearanceWithinEnclosure': 'Clearance Within Enclosure',
                        'gravityVentClearance': 'Gravity Vent Clearance',
                        'gravityVentGrilleClearance': 'Gravity Vent Grille Clearance',
                        'hearthMaterials': 'Hearth Materials',
                        'centralHeatingKit': 'Central Heating Kit',
                        'glassDoors': 'Glass Doors',
                        'fireScreen': 'Fire Screen',
                        'chaseFramingSize': 'Chase Framing Size',
                        'chaseInsulated': 'Chase Insulated',
                        'chaseClearOfDebris': 'Chase Clear Of Debris',
                        'outdoorCombustionAir': 'Outdoor Combustion Air',
                        'emberStrip': 'Ember Strip',
                        'hearthExtensionFront': 'Hearth Extension Front',
                        'hearthExtensionRightSide': 'Hearth Extension Right Side',
                        'hearthExtensionLeftSide': 'Hearth Extension Left Side',
                        'hearthMaterial': 'Hearth Material',
                        'floorRadiationProtection': 'Floor Radiation Protection',
                        'materialClearances': 'Material Clearances',
                        'rightSideLogs': 'Right Side Logs',
                        'leftSideLogs': 'Left Side Logs',
                        'combustibleFacing': 'Combustible Facing',
                        'combustibleSideWall': 'Combustible Side Wall',
                        
                        # CO Alarm sections matching frontend
                        'coAlarmSameRoomBCBC': 'Is CO alarm present in same room with solid-fuel-burning appliance? (9.32.4.2.3 BCBC)',
                        'coAlarmSameRoomNBCABC': 'Is CO alarm present in same room with solid-fuel-burning appliance? (9.32.3.9.3 NBC/ABC)',
                        'coAlarmPresentOBC': 'Is CO alarm present? (9.33.4.2 OBC)',
                        
                        # Chimney Support & Connection sections matching frontend
                        'fireResistantSolidChase': '26. Fireplace/chimney connection (anchor plate)',
                        'properlySecuredChase': '27. Wall support/band',
                        'isProper': '28. Distance between supports',
                        'fireRetardantClearances': '29. Chimney offsets',
                        'foundationFootingConnection': '30. Offset support',
                        'wellSupported': '31. Firestopping',
                        
                        'fireplaceBeaver': 'Fireplace Louvres',
                        # 'windowsFoundationAesthetic': 'Windows Foundation Aesthetic',
                        # 'roofSystem': 'Roof System',
                        # 'penetrating': 'Penetrating',
                        'wallSupportBrand': 'Wall Support Brand',
                        'atticRadiationShield': 'Attic Radiation Shield',
                        'atticShieldAboveInsulation': 'Attic Shield Above Insulation',
                        'otherRadiationShields': 'Other Radiation Shields',
                        'enclosedThroughLivingSpace': 'Enclosed Through Living Space',
                        'roofFlashingStormCollar': 'Roof Flashing Storm Collar',
                        'rainCapSparkArrestor': 'Rain Cap Spark Arrestor',
                        'roofBraces': 'Roof Braces',
                        'roofBracesSolidlyAnchored': 'Roof Braces Solidly Anchored',
                        'heightAboveRoofSurface': 'Height Above Roof Surface',
                        'heightWithin3m': 'Height Within 3m',
                        'capHeightAboveChase': 'Cap Height Above Chase',
                        'chimneyClearanceToCombustibles': 'Chimney Clearance To Combustibles',
                        'within3mAreaEnclosed': 'Within 3m Area Enclosed',
                        'horizontalClearances': 'Horizontal Clearances',
                        'obstructionsEquipment': 'Obstructions Equipment',
                        
                        # Report Details field names
                        'photosTaken': 'Photos Taken',
                        'numberOfPhotosTaken': 'Number Of Photos Taken',
                        'numberOfPhotosInChecklist': 'Number Of Photos In Checklist',
                        'numberOfPhotosInReports': 'Number Of Photos In Reports',
                        'commentsObservations': 'Comments & Observations',
                        'customerSignature': 'Customer Signature',
                        'customerSignatureDate': 'Customer Signature Date',
                        'inspectorSignature': 'Inspector Signature',
                        'inspectorSignatureDate': 'Inspector Signature Date'
                    }
                    
                    if field_name in special_cases:
                        return special_cases[field_name]
                    
                    # For other fields, use improved spacing logic
                    # Replace underscores with spaces first
                    formatted = field_name.replace('_', ' ')
                    
                    # Handle camelCase by adding spaces before capital letters
                    formatted = re.sub(r'([a-z])([A-Z])', r'\1 \2', formatted)
                    
                    # Handle numbers by adding space before them
                    formatted = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', formatted)
                    
                    # Title case the result
                    return formatted.title()

                def generate_fire_codes_section(self, data, story):
                    """Generate Fire Codes Compliance section with detailed information matching the screen"""
                    # Define the fire codes with their details as shown in the screen
                    fire_codes_info = {
                        'fireCode1': {
                            'number':"47",
                            'title': 'Fire Code = 2.6.1.4. Chimneys, Flues and Flue Pipes',
                            'description': '(1.) Every chimney, flue and flue pipe shall be inspected to identify any dangerous condition.\n\n'
                                           'a) at intervals not greater than 12 months\n'
                                           'b) at the time of addition of any appliance\n'
                                           'c) after any chimney fire.'
                        },
                        'fireCode2': {
                            'number': '48',
                            'title': 'Fire Code = 2.6.1.4. Chimneys, Flues and Flue Pipes',
                            'description': '(2.) Chimneys, Flues and Flue Pipes shall be cleaned as often as necessary to keep them free from dangerous accumulations of combustible deposits.\n\n'
                                           'Appendix A – A.2.6.1.4\n'
                                           '(2.) The presence in a chimney of deposits of soot or creosote in excess of 3 mm thick will indicate the need for immediate cleaning, possible modification of burning procedures and more frequent inspections.'
                        },
                        'fireCode3': {
                            'number': '49',
                            'title': 'Fire Code = 2.6.1.4. Chimneys, Flues and Flue Pipes',
                            'description': '(3.) A chimney, or flue pipe shall be replaced or repaired to eliminate\n'
                                           'a) any structural deficiency or decay\n\n'
                                           'Appendix A – A.2.6.1.4\n'
                                           '(3.) (a) Structural deficiencies are deviations from required construction, such as the absence of a liner or inadequate design of supports or ties. Instances of decay are cracking, settling, crumbling mortar, distortion, advanced corrosion, separation of sections, or loose or broken supports.'
                        },
                        'fireCode4': {
                             'number': '50',
                            'title': 'Fire Code = 2.6.1.4.',
                            'description': '(3.) A chimney, flue, or flue pipe shall be replaced or repaired to eliminate\n'
                                           '(b). all abandoned or unused openings that are not effectively sealed in a manner that would prevent the passage of fire or smoke.'
                        }
                    }
                    
                    # Process each fire code
                    for fire_code_key, fire_code_info in fire_codes_info.items():
                        fire_code_data = data.get(fire_code_key, {})
                        
                        if fire_code_data:  # Only show if data exists
                            # Add fire code header
                            story.append(Paragraph(f"{fire_code_info['number']}. {fire_code_info['title']}", self.styles['SHFSubsectionHeader']))
                            story.append(Paragraph(fire_code_info['description'], self.styles['SHFFieldValue']))
                            story.append(Spacer(1, 8))
                            
                            # Add condition, comments, and compliance
                            condition = fire_code_data.get('condition', '')
                            comments = fire_code_data.get('comments', '')
                            compliance = fire_code_data.get('codeCompliance', '')
                            photos = fire_code_data.get('photos', [])
                            
                            if condition:
                                try:
                                    story.append(self.create_field_table("Condition", condition, compliance))
                                except Exception as e:
                                    story.append(Paragraph(f"<b>Condition:</b> {condition}", self.styles['SHFFieldValue']))
                            
                            if comments:
                                try:
                                    story.append(self.create_field_table("Comments", comments))
                                except Exception as e:
                                    story.append(Paragraph(f"<b>Comments:</b> {comments}", self.styles['SHFFieldValue']))
                            
                            if compliance:
                                try:
                                    story.append(self.create_field_table("Code Compliance", compliance))
                                except Exception as e:
                                    story.append(Paragraph(f"<b>Code Compliance:</b> {compliance}", self.styles['SHFFieldValue']))
                            
                            # Add photos if any
                            if photos and len(photos) > 0:
                                self.add_photos_section(photos, story)
                            
                            story.append(Spacer(1, 16))

                def add_photos_section(self, photos, story):
                    """Add photos to the story if they exist"""
                    if not photos or len(photos) == 0:
                        return
                        
                    story.append(Paragraph("<b>Photos:</b>", self.styles['SHFFieldLabel']))
                    
                    # Group photos in rows of 2
                    for i in range(0, len(photos), 2):
                        photo_row = []
                        for j in range(2):
                            if i + j < len(photos):
                                img = self.base64_to_image(photos[i + j], 200, 150)
                                if img:
                                    photo_row.append(img)
                                else:
                                    photo_row.append(Paragraph("[Image not available]", self.styles['SHFFieldValue']))
                            else:
                                photo_row.append("")  # Empty cell
                        
                        if photo_row:
                            photo_table = Table([photo_row], colWidths=[3*inch, 3*inch])
                            photo_table.setStyle(TableStyle([
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                            ]))
                            story.append(photo_table)
                            story.append(Spacer(1, 10))

                def generate_chimney_support_connection_section(self, data, story):
                    """Generate Chimney Support & Connection section with proper ordering and CO alarm note"""
                    # Define the order of sections as they appear in the frontend
                    section_order = [
                        ('coAlarmSameRoomBCBC', 'Is CO alarm present in same room with solid-fuel-burning appliance? (9.32.4.2.3 BCBC)'),
                        ('coAlarmSameRoomNBCABC', 'Is CO alarm present in same room with solid-fuel-burning appliance? (9.32.3.9.3 NBC/ABC)'),
                        ('coAlarmPresentOBC', 'Is CO alarm present? (9.33.4.2 OBC)'),
                        ('fireResistantSolidChase', 'Fireplace/chimney connection (anchor plate)'),
                        ('properlySecuredChase', 'Wall support/band'),
                        ('isProper', 'Distance between supports'),
                        ('fireRetardantClearances', 'Chimney offsets'),
                        ('foundationFootingConnection', 'Offset support'),
                        ('wellSupported', 'Firestopping'),

                    ]
                    
                    co_alarm_sections_processed = 0
                    
                    # Process each section in the defined order
                    for section_key, section_title in section_order:
                        section_data = data.get(section_key)
                        
                        if section_data and isinstance(section_data, dict):
                            # Add section header
                            story.append(Paragraph(section_title, self.styles['SHFSubsectionHeader']))
                            
                            # Extract values
                            required_val = section_data.get('requiredValue')
                            present_val = section_data.get('presentValue')
                            compliance_val = section_data.get('codeCompliance')
                            photos = section_data.get('photos', [])
                            
                            # Display required value
                            if required_val:
                                story.append(self.create_field_table("Required", required_val))
                            
                            # Display present value
                            if present_val:
                                story.append(self.create_field_table("Present", present_val))
                            
                            # Display compliance
                            if compliance_val:
                                story.append(self.create_field_table("Code Compliance", compliance_val))
                            
                            # Add photos if any
                            if photos and len(photos) > 0:
                                self.add_photos_section(photos, story)
                            
                            story.append(Spacer(1, 12))
                            
                            # Track CO alarm sections
                            if section_key in ['coAlarmSameRoomBCBC', 'coAlarmSameRoomNBCABC', 'coAlarmPresentOBC']:
                                co_alarm_sections_processed += 1
                                
                                # Add note after all CO alarm sections are processed
                                if co_alarm_sections_processed == 3:
                                    story.append(Paragraph("<b>Important Note:</b>", self.styles['SHFFieldLabel']))
                                    story.append(Paragraph(
                                        "It is the homeowner's responsibility to ensure that the CO alarm is in working condition and installed in accordance with applicable codes.",
                                        self.styles['SHFFieldValue']
                                    ))
                                    story.append(Paragraph(
                                        "<b>NOTE:</b> WETT inspectors do not test the CO alarm, they just note if it is present.",
                                        self.styles['SHFFieldValue']
                                    ))
                                    story.append(Spacer(1, 16))
                    
                    # Process any other fields that might not be in the predefined order
                    processed_keys = set(dict(section_order).keys())
                    # Exclude specific fields that should not appear in the report
                    excluded_fields = {'windowsFoundationAesthetic', 'roofSystem', 'penetrating'}
                    for key, value in data.items():
                        if key not in processed_keys and key not in ['id', 'inspection_id', 'created_at', 'updated_at'] and key not in excluded_fields and value:
                            if isinstance(value, dict) and any(k in value for k in ['requiredValue', 'presentValue', 'codeCompliance']):
                                # Format the field name
                                formatted_label = self.format_field_label(key)
                                story.append(Paragraph(formatted_label, self.styles['SHFSubsectionHeader']))
                                
                                required_val = value.get('requiredValue')
                                present_val = value.get('presentValue')
                                compliance_val = value.get('codeCompliance')
                                photos = value.get('photos', [])
                                
                                if required_val:
                                    story.append(self.create_field_table("Required", required_val))
                                if present_val:
                                    story.append(self.create_field_table("Present", present_val))
                                if compliance_val:
                                    story.append(self.create_field_table("Code Compliance", compliance_val))
                                if photos and len(photos) > 0:
                                    self.add_photos_section(photos, story)
                                
                                story.append(Spacer(1, 12))

                def generate_complete_pdf(self, inspection_data, user_data):
                    """Generate complete PDF and return as BytesIO"""
                    # Create PDF in memory
                    pdf_buffer = io.BytesIO()
                    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch)
                    story = []
                    
                    # Generate header section
                    self.generate_header_section(inspection_data, user_data, story)
                    
                    # Generate all sections
                    self.generate_all_sections(inspection_data, story)
                    
                    # Build PDF
                    doc.build(story)
                    pdf_buffer.seek(0)
                    return pdf_buffer

                def generate_header_section(self, inspection_data, user_data, story):
                    """Generate the header section with SHF branding"""
                    # SHF Title
                    story.append(Paragraph("SHF INSPECTION REPORT", self.styles['SHFTitle']))
                    story.append(Spacer(1, 20))
                    
                    # Company information
                    if 'company' in user_data:
                        company = user_data['company']
                        story.append(Paragraph("INSPECTION COMPANY", self.styles['SHFSectionHeader']))
                        
                        company_data = [
                            ['Company:', company.get('company_name', 'SHF Inspection Services')],
                            ['Address:', company.get('address', 'Not specified')],
                            ['Phone:', company.get('phone', 'Not specified')],
                            ['Email:', company.get('company_email', 'Not specified')],
                            ['Website:', company.get('website', 'Not specified')]
                        ]
                        
                        company_table = Table(company_data, colWidths=[1.5*inch, 4*inch])
                        company_table.setStyle(TableStyle([
                            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, -1), 10),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
                        ]))
                        story.append(company_table)
                        
                        # Include company logo if available (URL or base64)
                        try:
                            logo = company.get('logo')
                            if isinstance(logo, str) and len(logo.strip()) > 0:
                                logo_img = self.base64_to_image(logo, 120, 60)
                                if logo_img:
                                    story.append(Spacer(1, 6))
                                    story.append(Paragraph("Company Logo:", self.styles['SHFFieldLabel']))
                                    story.append(logo_img)
                        except Exception as e:
                            print(f"DEBUG: Error rendering company logo: {e}")
                        
                        story.append(Spacer(1, 15))
                    
                    # Inspector information
                    if 'inspector' in user_data:
                        inspector = user_data['inspector']
                        story.append(Paragraph("INSPECTOR INFORMATION", self.styles['SHFSectionHeader']))
                        
                        inspector_data = [
                            ['Inspector:', inspector.get('name', 'Not specified')],
                            ['WETT Number:', inspector.get('wett_number', 'Not specified')],
                            ['Province:', inspector.get('province', 'Not specified')]
                        ]
                        
                        inspector_table = Table(inspector_data, colWidths=[1.5*inch, 4*inch])
                        inspector_table.setStyle(TableStyle([
                            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, -1), 10),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
                        ]))
                        story.append(inspector_table)
                        story.append(Spacer(1, 15))
                    
                    # Inspection basic information
                    story.append(Paragraph("INSPECTION DETAILS", self.styles['SHFSectionHeader']))
                    
                    inspection_info = [
                        ['Inspection Title:', inspection_data.get('title', 'Not specified')],
                        ['Client Name:', inspection_data.get('client_name', 'Not specified')],
                        ['Client Address:', inspection_data.get('client_address', 'Not specified')],
                        ['Inspection Date:', inspection_data.get('inspection_date', 'Not specified')],
                        ['Form Type:', inspection_data.get('form_type', 'Not specified').title()],
                        ['Status:', inspection_data.get('status', 'Not specified').title()],
                        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                    ]
                    
                    inspection_table = Table(inspection_info, colWidths=[1.5*inch, 4*inch])
                    inspection_table.setStyle(TableStyle([
                        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
                    ]))
                    story.append(inspection_table)
                    story.append(PageBreak())

                def generate_all_sections(self, inspection_data, story):
                    """Generate all inspection sections with SHF formatting"""
                    form_type = inspection_data.get('form_type', 'factory-built')

                    if form_type == 'fireplace-insert':
                        # Generate fireplace-insert sections
                        sections_to_generate = [
                            ('1. CHIMNEY SPECIFICATION', inspection_data.get('chimneySpecification')),
                            ('2. FIREPLACE SPECIFICATION', inspection_data.get('fireplaceSpecification')),
                            ('3. MATERIALS & CLEARANCES', inspection_data.get('materialsClearances')),
                            ('4. EMBER PAD & FLOOR PROTECTION', inspection_data.get('emberPadFloorProtection')),
                            ('5. FIREPLACE SAFETY FEATURES', inspection_data.get('fireplaceSafetyFeatures')),
                            ('6. CHIMNEY SUPPORT & CONNECTION', inspection_data.get('chimneySupportConnection')),
                            ('7. LINER & APPLIANCE CHECKS', inspection_data.get('linerApplianceChecks')),
                            ('8. APPLIANCE & MASONRY CHECKS', inspection_data.get('applianceMasonryChecks')),
                            ('9. CO ALARMS & LINERS', inspection_data.get('coAlarmsLiners')),
                            ('10. CHIMNEY LINER & JOINTS DETAILS', inspection_data.get('chimneyLinerJointsDetails')),
                            ('11. HEARTH & SUPPORT', inspection_data.get('hearthSupport')),
                            ('12. CLEARANCES', inspection_data.get('clearances')),
                            ('13. CLEARANCES & LINERS', inspection_data.get('clearancesLiners')),
                            ('14. LINER DETAILS', inspection_data.get('linerDetails')),
                            ('15. JOINTS DETAILS', inspection_data.get('jointsDetails')),
                            ('16. CHIMNEY HEIGHT & CLEARANCE', inspection_data.get('chimneyHeightClearance')),
                            ('17. CHIMNEY SUPPORTS', inspection_data.get('chimneySupports')),
                            ('18. CHIMNEY SADDLES & FIRE CODE', inspection_data.get('chimneySaddlesFireCode')),
                            ('19. REPORT DETAILS', inspection_data.get('reportDetails'))
                        ]
                    elif form_type == 'masonry':
                        # Generate masonry sections
                        sections_to_generate = [
                            ('1. CHIMNEY SPECIFICATION', inspection_data.get('masonryChimneySpecification')),
                            ('2. FIREPLACE SPECIFICATION', inspection_data.get('masonryFireplaceSpecification')),
                            ('3. FIREPLACE CONSTRUCTION DETAILS', inspection_data.get('masonryFireplaceConstructionDetails')),
                            ('4. COMBUSTION AIR REQUIREMENTS', inspection_data.get('masonryCombustionAirRequirements')),
                            ('5. CHIMNEY STRUCTURE', inspection_data.get('masonryChimneyStructure')),
                            ('6. HEARTH CONSTRUCTION', inspection_data.get('masonryHearthConstruction')),
                            ('7. FIREPLACE COMPONENTS', inspection_data.get('masonryFireplaceComponents')),
                            ('8. FIREPLACE CLEARANCES', inspection_data.get('masonryFireplaceClearances')),
                            ('9. CHIMNEY LINERS INSTALLATION', inspection_data.get('masonryChimneyLinersInstallation')),
                            ('10. JOINT DETAILS', inspection_data.get('masonryJointDetails')),
                            ('11. CHIMNEY STABILITY & CAPS', inspection_data.get('masonryChimneyStabilityCaps')),
                            ('12. CLEARANCES & SUPPORTS', inspection_data.get('masonryClearancesSupports')),
                            ('13. CHIMNEY SADDLES & FIRE CODE', inspection_data.get('masonryChimneySaddlesFireCode')),
                            ('14. CO ALARMS', inspection_data.get('masonryCOAlarms')),
                            ('15. REPORT DETAILS', inspection_data.get('reportDetails'))
                        ]
                    elif form_type == 'pellet-insert':
                        # Generate pellet insert sections
                        sections_to_generate = [
                            ('1. CHIMNEY SPECIFICATIONS', inspection_data.get('pelletInsertChimneySpecifications')),
                            ('2. FIREPLACE SPECIFICATIONS', inspection_data.get('pelletInsertFireplaceSpecifications')),
                            ('3. LINER & APPLIANCE CHECKS I', inspection_data.get('pelletInsertLinerApplianceChecks1')),
                            ('4. LINER & APPLIANCE CHECKS II', inspection_data.get('pelletInsertLinerApplianceChecks2')),
                            ('5. LINER & VENT COMPONENTS', inspection_data.get('pelletInsertLinerVentComponents')),
                            ('6. MASONRY FIREPLACE CONSTRUCTION I', inspection_data.get('pelletInsertMasonryFireplaceConstruction1')),
                            ('7. MASONRY FIREPLACE CONSTRUCTION II', inspection_data.get('pelletInsertMasonryFireplaceConstruction2')),
                            ('8. MATERIALS & CLEARANCES', inspection_data.get('pelletInsertMaterialsClearances')),
                            ('9. CHIMNEY SUPPORT & CONNECTION', inspection_data.get('pelletInsertChimneySupportConnection')),
                            ('10. CHIMNEY SUPPORTS', inspection_data.get('pelletInsertChimneySupports')),
                            ('11. CO ALARMS & LINERS', inspection_data.get('pelletInsertCOAlarmsLiners')),
                            ('12. EMBER PAD & FLOOR PROTECTION', inspection_data.get('pelletInsertEmberPadFloorProtection')),
                            ('13. FIREPLACE SAFETY FEATURES', inspection_data.get('pelletInsertFireplaceSafetyFeatures')),
                            ('14. CHIMNEY STABILITY AND CAPS', inspection_data.get('pelletInsertChimneyStabilityCaps')),
                            ('15. CHIMNEY LINERS', inspection_data.get('pelletInsertChimneyLiners')),
                            ('16. CHIMNEY JOINTS & LINER DETAILS', inspection_data.get('pelletInsertChimneyJointsLinerDetails')),
                            ('17. CHIMNEY SADDLES & FIRE CODE', inspection_data.get('pelletInsertChimneySaddlesFireCode')),
                            ('18. REPORT DETAILS', inspection_data.get('reportDetails'))
                        ]
                    else:
                        # Generate factory-built sections (existing logic)
                        sections_to_generate = [
                            ('1. CHIMNEY SPECIFICATION', inspection_data.get('chimneySpecification')),
                            ('2. FIREPLACE SPECIFICATION', inspection_data.get('fireplaceSpecification')),
                            ('3. COMBUSTIBLE MATERIALS', inspection_data.get('combustibleMaterials')),
                            ('4. HEARTH & FLOOR PROTECTION', inspection_data.get('hearthFloorProtection')),
                            ('5. ENCLOSURE & VENTILATION', inspection_data.get('enclosureVentilation')),
                            ('6. FIREPLACE SAFETY FEATURES', inspection_data.get('fireplaceSafetyFeatures')),
                            ('7. CHIMNEY SUPPORT & CONNECTION', inspection_data.get('chimneySupportConnection')),
                            ('8. ATTIC & RADIATION PROTECTION', inspection_data.get('atticRadiationProtection')),
                            ('9. ROOF & EXTERIOR PROTECTION', inspection_data.get('roofExteriorProtection')),
                            ('10. CHIMNEY HEIGHT & CLEARANCE', inspection_data.get('chimneyHeightClearance')),
                            ('11. FIRE CODES COMPLIANCE', inspection_data.get('fireCodesCompliance')),
                            ('12. REPORT DETAILS', inspection_data.get('reportDetails'))
                        ]

                    # Generate sections for the determined form type
                    for section_title, section_data in sections_to_generate:
                        if section_data:
                            self.generate_section(section_title, section_data, story)

                def generate_section(self, title, data, story):
                    """Generate a section with improved formatting and problem content handling"""
                    story.append(Paragraph(title, self.styles['SHFSectionHeader']))
                    
                    if isinstance(data, list) and len(data) > 0:
                        data = data[0]  # Take first item if it's a list
                    
                    if not isinstance(data, dict):
                        story.append(Paragraph("No data available for this section", self.styles['SHFFieldValue']))
                        story.append(PageBreak())
                        return
                    
                    # Initialize tracking variables at the beginning
                    processed_fields = set()
                    problematic_fields = []
                    
                    # Special handling for Fire Codes Compliance to show detailed information
                    if title == '11. FIRE CODES COMPLIANCE':
                        self.generate_fire_codes_section(data, story)
                        story.append(PageBreak())
                        return
                    
                    # Special handling for Chimney Support & Connection to add CO alarm note
                    if title == '7. CHIMNEY SUPPORT & CONNECTION':
                        self.generate_chimney_support_connection_section(data, story)
                        story.append(PageBreak())
                        return
                    
                    # Special handling for Report Details: render signatures as images when available
                    if title == '12. REPORT DETAILS':
                        try:
                            print(f"DEBUG: Full Report Details data keys: {list(data.keys())}")
                            print(f"DEBUG: Report Details data: {data}")
                            
                            cust_sig = data.get('customerSignature') or data.get('customer_signature')
                            insp_sig = data.get('inspectorSignature') or data.get('inspector_signature')
                            
                            print(f"DEBUG: Customer signature data length: {len(str(cust_sig)) if cust_sig else 0}")
                            print(f"DEBUG: Inspector signature data length: {len(str(insp_sig)) if insp_sig else 0}")
                            print(f"DEBUG: Customer signature first 50 chars: {str(cust_sig)[:50] if cust_sig else 'None'}")
                            print(f"DEBUG: Inspector signature first 50 chars: {str(insp_sig)[:50] if insp_sig else 'None'}")
                            print(f"DEBUG: Signatures are identical: {cust_sig == insp_sig}")
                            
                            # Process customer signature
                            if isinstance(cust_sig, str) and len(cust_sig.strip()) > 0:
                                print(f"DEBUG: Processing customer signature...")
                                sig_img = self.base64_to_image(cust_sig, 200, 100)
                                if sig_img:
                                    story.append(Paragraph("Customer Signature:", self.styles['SHFFieldLabel']))
                                    story.append(sig_img)
                                    story.append(Spacer(1, 6))
                                else:
                                    story.append(Paragraph("Customer Signature: ✅ Digital signature captured", self.styles['SHFFieldValue']))
                                    story.append(Spacer(1, 6))
                            else:
                                story.append(Paragraph("Customer Signature: Not provided", self.styles['SHFFieldValue']))
                                story.append(Spacer(1, 6))
                            
                            # Process inspector signature
                            if isinstance(insp_sig, str) and len(insp_sig.strip()) > 0:
                                print(f"DEBUG: Processing inspector signature...")
                                sig_img = self.base64_to_image(insp_sig, 200, 100)
                                if sig_img:
                                    story.append(Paragraph("Inspector Signature:", self.styles['SHFFieldLabel']))
                                    story.append(sig_img)
                                    story.append(Spacer(1, 6))
                                else:
                                    story.append(Paragraph("Inspector Signature: ✅ Digital signature captured", self.styles['SHFFieldValue']))
                                    story.append(Spacer(1, 6))
                            else:
                                story.append(Paragraph("Inspector Signature: Not provided", self.styles['SHFFieldValue']))
                                story.append(Spacer(1, 6))
                                    
                        except Exception as e:
                            print(f"DEBUG: Error rendering signatures: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Mark signature fields as processed to avoid duplication in regular field processing
                        processed_fields.update(['customerSignature', 'customer_signature', 'inspectorSignature', 'inspector_signature'])
                    
                    # Handle different data structures
                    for key, value in data.items():
                        if key in ['id', 'inspection_id', 'created_at', 'updated_at'] or key in processed_fields:
                            continue
                        
                        # Exclude specific fields that should not appear in the report
                        excluded_fields = {'windowsFoundationAesthetic', 'roofSystem', 'penetrating'}
                        if key in excluded_fields:
                            continue
                            
                        # Check if this field might be problematic
                        is_problematic = False
                        if isinstance(value, str) and len(value) > 1000:
                            is_problematic = True
                            print(f"DEBUG: Problematic field detected: '{key}', Length: {len(value)}")
                        elif isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                if isinstance(sub_value, str) and len(sub_value) > 1000:
                                    is_problematic = True
                                    print(f"DEBUG: Problematic nested field detected: '{key}.{sub_key}', Length: {len(sub_value)}")
                                    break
                        
                        if is_problematic:
                            problematic_fields.append((key, value))
                            continue  # Skip processing this field in normal flow
                        
                        # Handle nested structures (new API format)
                        if isinstance(value, dict) and any(k in value for k in ['requiredValue', 'presentValue', 'codeCompliance']):
                            processed_fields.add(key)
                            story.append(Paragraph(self.format_field_label(key), self.styles['SHFSubsectionHeader']))
                            
                            required_val = value.get('requiredValue')
                            present_val = value.get('presentValue')
                            compliance_val = value.get('codeCompliance')
                            photos = value.get('photos', [])
                            
                            try:
                                # Only show required value and compliance together if both exist
                                if required_val and compliance_val:
                                    story.append(self.create_field_table("Required", required_val, compliance_val))
                                elif required_val:
                                    story.append(self.create_field_table("Required", required_val))
                                
                                # Only show present value without compliance (to avoid duplication)
                                if present_val:
                                    story.append(self.create_field_table("Present", present_val))
                                
                                # Handle other fields but exclude compliance-related ones
                                for extra_key, extra_val in value.items():
                                        if extra_key in ['requiredValue', 'presentValue', 'codeCompliance', 'photos']:
                                            continue
                                        if isinstance(extra_val, str) and extra_val.strip():
                                            story.append(self.create_field_table(self.format_field_label(extra_key), extra_val))
                            except Exception as e:
                                print(f"DEBUG: Error creating table for {key}: {e}")
                                # Add as simple paragraph instead
                                story.append(Paragraph(f"<b>{self.format_field_label(key)}:</b> Content could not be displayed in table format", self.styles['SHFFieldValue']))
                            
                            if photos and len(photos) > 0:
                                self.add_photos_section(photos, story)
                            
                            story.append(Spacer(1, 10))
                            
                        # Handle other field types (only if not already processed as nested structure)
                        elif not key.endswith('_photos') and not key.endswith('_compliance') and value is not None and not isinstance(value, dict):
                            processed_fields.add(key)
                            label = self.format_field_label(key)
                            
                            # Check for compliance field only if this is a required/present field
                            compliance = None
                            if key.endswith('_required') or key.endswith('_present'):
                                compliance_key = key.replace('_required', '_compliance').replace('_present', '_compliance')
                                compliance = data.get(compliance_key) if compliance_key in data else None
                                # Mark compliance field as processed to avoid duplication
                                if compliance:
                                    processed_fields.add(compliance_key)
                            
                            try:
                                story.append(self.create_field_table(label, value, compliance))
                            except Exception as e:
                                print(f"DEBUG: Error creating table for {label}: {e}")
                                # Add as simple paragraph instead
                                story.append(Paragraph(f"<b>{label}:</b> Content could not be displayed in table format", self.styles['SHFFieldValue']))
                    
                    # After processing fields, include any top-level *_photos arrays (only for sections without nested structures)
                    try:
                        # Check if this section has nested photo structures (like CombustibleMaterials)
                        has_nested_photos = any(
                            isinstance(v, dict) and 'photos' in v 
                            for v in data.values() 
                            if isinstance(v, dict)
                        )
                        
                        # Only process top-level photos if no nested photo structures exist
                        if not has_nested_photos:
                            for k, v in data.items():
                                if isinstance(k, str) and k.endswith('_photos') and isinstance(v, list) and len(v) > 0:
                                    # Append a small header for context
                                    subsection = self.format_field_label(k.replace('_photos', ''))
                                    story.append(Paragraph(subsection + " Photos", self.styles['SHFSubsectionHeader']))
                                    self.add_photos_section(v, story)
                                    story.append(Spacer(1, 8))
                    except Exception as e:
                        print(f"DEBUG: Error adding top-level photos: {e}")
                    
                    # Handle problematic fields as simple paragraphs outside of tables
                    if problematic_fields:
                        story.append(Paragraph("Additional Information", self.styles['SHFSubsectionHeader']))
                        for key, value in problematic_fields:
                            label = self.format_field_label(key)
                            # Just show that the field exists but don't display problematic content
                            story.append(Paragraph(f"<b>{label}:</b> Content available (not displayed due to size)", self.styles['SHFFieldValue']))
                            story.append(Spacer(1, 5))
                    
                    story.append(PageBreak())
            
            # Create and use the PDF generator
            pdf_generator = SHFInspectionReportPDF()
            pdf_buffer = pdf_generator.generate_complete_pdf(inspection_data, user_data)
            
            # Create filename
            client_name = inspection_data.get('client_name') or 'Unknown_Client'
            safe_client_name = str(client_name).replace(' ', '_').replace('/', '_')
            date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"SHF_Inspection_Report_{safe_client_name}_{date_str}.pdf"
            
            # Create reports directory if it doesn't exist
            reports_dir = "reports"
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            # Save the PDF to the server (optional)
            pdf_path = f"reports/{filename}"
            with open(pdf_path, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            
            # Create response
            response = make_response(pdf_buffer.getvalue())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
            
            return response
            
        except ImportError as import_error:
            print(f"Import error in PDF generation: {import_error}")
            return jsonify({'error': f'PDF generation dependencies not available: {str(import_error)}'}), 500
            
    except Exception as e:
        print(f"Error in generate_pdf_report: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to generate PDF report: {str(e)}'}), 500

@main.route('/api/send-report-email/<int:inspection_id>', methods=['POST'])
def send_report_email(inspection_id):
    """Send PDF report via email"""
    try:
        # Get email data from request
        data = request.get_json()
        sender_email = data.get('from')
        recipient_email = data.get('to')
        bcc_email = data.get('bcc')
        email_body = data.get('description', 'Please find attached the inspection report for your review.')
        
        # Validate required fields
        if not sender_email or not recipient_email:
            return jsonify({'error': 'Sender and recipient emails are required'}), 400
        
        # Generate PDF report using the existing function
        pdf_response = generate_pdf_report(inspection_id)
        
        # Check if PDF generation was successful
        # If it's a tuple, it means there was an error (status_code != 200)
        if isinstance(pdf_response, tuple):
            return jsonify({'error': 'Failed to generate PDF report'}), 500
            
        # If it's a Response object, get the data
        pdf_data = pdf_response.get_data()
        
        # Import Flask-Mail components
        from flask_mail import Message
        from app import mail
        
        # Get inspection details for email subject
        inspection = Inspection.query.get_or_404(inspection_id)
        
        # Create email message
        subject = f"Inspection Report #{inspection_id} - {inspection.title or 'Inspection Report'}"
        
        msg = Message(
            subject=subject,
            sender=sender_email,
            recipients=[recipient_email]
        )
        
        # Add BCC if provided
        if bcc_email:
            msg.bcc = [bcc_email]
        
        # Set email body
        msg.body = email_body
        
        # Attach PDF
        filename = f"inspection_report_{inspection_id}.pdf"
        msg.attach(filename, "application/pdf", pdf_data)
        
        # Send email
        mail.send(msg)
        
        return jsonify({
            'message': 'Email sent successfully',
            'inspection_id': inspection_id,
            'recipient': recipient_email
        }), 200
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({'error': 'Failed to send email: ' + str(e)}), 500


# Delete User Account API Endpoint
@main.route('/api/users/<email>/delete-account', methods=['DELETE'])
def delete_user_account(email):
    """
    Delete a user account and all associated data
    This will cascade delete all related records
    """
    try:
        # Find the user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_id = user.id
        
        # Log the deletion attempt
        print(f"Starting deletion process for user: {email} (ID: {user_id})")
        
        # Delete all related data in the correct order to avoid foreign key constraints
        
        # 1. Delete all inspection-related data first
        inspections = Inspection.query.filter_by(user_id=user_id).all()
        
        for inspection in inspections:
            inspection_id = inspection.id
            print(f"Deleting data for inspection ID: {inspection_id}")
            
            # Delete all checklist section data
            ChimneySpecification.query.filter_by(inspection_id=inspection_id).delete()
            FireplaceSpecification.query.filter_by(inspection_id=inspection_id).delete()
            CombustibleMaterials.query.filter_by(inspection_id=inspection_id).delete()
            HearthFloorProtection.query.filter_by(inspection_id=inspection_id).delete()
            EnclosureVentilation.query.filter_by(inspection_id=inspection_id).delete()
            FireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).delete()
            ChimneySupportConnection.query.filter_by(inspection_id=inspection_id).delete()
            AtticRadiationProtection.query.filter_by(inspection_id=inspection_id).delete()
            RoofExteriorProtection.query.filter_by(inspection_id=inspection_id).delete()
            ChimneyHeightClearance.query.filter_by(inspection_id=inspection_id).delete()
            FireCodesCompliance.query.filter_by(inspection_id=inspection_id).delete()
            ReportDetails.query.filter_by(inspection_id=inspection_id).delete()
        
        # 2. Delete all inspections
        Inspection.query.filter_by(user_id=user_id).delete()
        
        # 3. Delete inspector and company profiles (these should cascade automatically due to model relationships)
        Inspector.query.filter_by(user_id=user_id).delete()
        Company.query.filter_by(user_id=user_id).delete()
        
        # 4. Finally delete the user account
        db.session.delete(user)
        
        # Commit all deletions
        db.session.commit()
        
        print(f"Successfully deleted user account: {email}")
        
        return jsonify({
            'message': 'User account and all associated data deleted successfully',
            'deleted_user_email': email
        }), 200
        
    except Exception as e:
        # Rollback any partial changes
        db.session.rollback()
        
        error_message = f"Error deleting user account: {str(e)}"
        print(error_message)
        
        return jsonify({
            'error': 'Failed to delete user account',
            'details': str(e)
        }), 500

# NEW: Validate checklist completeness for an inspection (images optional)
@main.route('/api/checklist/validate/<int:inspection_id>', methods=['POST'])
def validate_checklist(inspection_id):
    """Validate which checklist sections are complete (ignoring images) and update the inspection.
    Returns a summary with per-section status, updated completedSections, and overall status.
    """
    try:
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        form_type = inspection.form_type or 'factory-built'

        if form_type == 'masonry':
            # Define the section IDs for masonry forms
            all_sections = [
                'inspection-details', 'chimney-specifications', 'fireplace-specifications', 'fireplace-construction-details', 'combustion-air-requirements', 'chimney-structure', 'hearth-construction', 'fireplace-components', 'fireplace-clearances', 'chimney-liners-installation', 'joint-details', 'chimney-stability-caps', 'clearances-supports', 'chimney-saddles-fire-code', 'co-alarms', 'dates-signatures'
            ]

            # Map section IDs to model classes for masonry forms
            section_model_map = {
                'chimney-specifications': MasonryChimneySpecification,
                'fireplace-specifications': MasonryFireplaceSpecification,
                'fireplace-construction-details': MasonryFireplaceConstructionDetails,
                'combustion-air-requirements': MasonryCombustionAirRequirements,
                'chimney-structure': MasonryChimneyStructure,
                'hearth-construction': MasonryHearthConstruction,
                'fireplace-components': MasonryFireplaceComponents,
                'fireplace-clearances': MasonryFireplaceClearances,
                'chimney-liners-installation': MasonryChimneyLinersInstallation,
                'joint-details': MasonryJointDetails,
                'chimney-stability-caps': MasonryChimneyStabilityCaps,
                'clearances-supports': MasonryClearancesSupports,
                'chimney-saddles-fire-code': MasonryChimneySaddlesFireCode,
                'co-alarms': MasonryCOAlarms,
                # 'inspection-details' and 'dates-signatures' are kept in inspection.form_data
            }
        elif form_type == 'fireplace-insert':
            # Define the section IDs for fireplace-insert forms
            all_sections = [
                'inspection-details', 'chimney-specifications', 'fireplace-specifications',
                'materials-clearances', 'ember-pad-floor-protection', 'chimney-support-connection',
                'fireplace-safety-features', 'liner-appliance-checks', 'appliance-masonry-checks',
                'co-alarms-liners', 'chimney-liner-joints-details', 'hearth-support',
                'clearances', 'clearances-liners', 'liner-details', 'joints-details',
                'chimney-height-clearance', 'chimney-supports', 'chimney-saddles-fire-code',
                'dates-signatures'
            ]

            # Map section IDs to model classes for fireplace-insert forms
            section_model_map = {
                'chimney-specifications': FireplaceInsertChimneySpecification,
                'fireplace-specifications': FireplaceInsertFireplaceSpecification,
                'materials-clearances': FireplaceInsertMaterialsClearances,
                'ember-pad-floor-protection': FireplaceInsertEmberPadFloorProtection,
                'chimney-support-connection': FireplaceInsertChimneySupportConnection,
                'fireplace-safety-features': FireplaceInsertFireplaceSafetyFeatures,
                'liner-appliance-checks': FireplaceInsertLinerApplianceChecks,
                'appliance-masonry-checks': FireplaceInsertApplianceMasonryChecks,
                'co-alarms-liners': FireplaceInsertCOAlarmsLiners,
                'chimney-liner-joints-details': FireplaceInsertChimneyLinerJointsDetails,
                'hearth-support': FireplaceInsertHearthSupport,
                'clearances': FireplaceInsertClearances,
                'clearances-liners': FireplaceInsertClearancesLiners,
                'liner-details': FireplaceInsertLinerDetails,
                'joints-details': FireplaceInsertJointsDetails,
                'chimney-height-clearance': FireplaceInsertChimneyHeightClearance,
                'chimney-supports': FireplaceInsertChimneySupports,
                'chimney-saddles-fire-code': FireplaceInsertChimneySaddlesFireCode,
                # 'inspection-details' and 'dates-signatures' are kept in inspection.form_data
            }
        elif form_type == 'pellet-insert':
            # Define the section IDs for pellet-insert forms
            all_sections = [
                'inspection-details', 'chimney-specifications', 'chimney-supports', 'chimney-stability-caps', 'chimney-joints-liner-details', 'chimney-liners', 'dates-signatures'
            ]

            # Map section IDs to model classes for pellet-insert forms
            section_model_map = {
                'chimney-specifications': PelletInsertChimneySpecification,
                'chimney-supports': PelletInsertChimneySupports,
                'chimney-stability-caps': PelletInsertChimneyStabilityCaps,
                'chimney-joints-liner-details': PelletInsertChimneyJointsLinerDetails,
                'chimney-liners': PelletInsertChimneyLiners,
                # 'inspection-details' and 'dates-signatures' are kept in inspection.form_data
            }
        elif form_type == 'wood-stove-manufactured':
            # Define the section IDs for wood-stove-manufactured forms
            all_sections = [
                'inspection-details', 'chimney-inspection', 'chimney-components-supports', 'chimney-structure-clearances', 'clearances-shielding', 'combustion-air-co-alarm', 'ember-pad-floor-protection', 'fire-codes-compliance', 'flue-pipe-chimney-connection', 'flue-pipe-components', 'flue-pipe-info-clearances', 'flue-pipe-orientation-joints', 'dates-signatures'
            ]

            # Map section IDs to model classes for wood-stove-manufactured forms
            section_model_map = {
                'chimney-inspection': WoodStoveManufacturedChimneyInspection,
                'chimney-components-supports': WoodStoveManufacturedChimneyComponentsSupports,
                'chimney-structure-clearances': WoodStoveManufacturedChimneyStructureClearances,
                'clearances-shielding': WoodStoveManufacturedClearancesShielding,
                'combustion-air-co-alarm': WoodStoveManufacturedCombustionAirCOAlarm,
                'ember-pad-floor-protection': WoodStoveManufacturedEmberPadFloorProtection,
                'fire-codes-compliance': WoodStoveManufacturedFireCodesCompliance,
                'flue-pipe-chimney-connection': WoodStoveManufacturedFluePipeChimneyConnection,
                'flue-pipe-components': WoodStoveManufacturedFluePipeComponents,
                'flue-pipe-info-clearances': WoodStoveManufacturedFluePipeInfoClearances,
                'flue-pipe-orientation-joints': WoodStoveManufacturedFluePipeOrientationJoints,
                # 'inspection-details' and 'dates-signatures' are kept in inspection.form_data
            }
        elif form_type == 'wood-stove-masonry':
            # Define the section IDs for wood-stove-masonry forms
            all_sections = [
                'inspection-details', 'fireplace-specifications', 'chimney-construction', 'chimney-construction-liners', 'chimney-liners', 'chimney-liners-installation', 'chimney-saddles-fire-code', 'chimney-specifications', 'chimney-stability-caps', 'chimney-supports', 'clearances-shielding', 'combustible-materials', 'ember-pad-floor-protection', 'flue-pipe-orientation-joints-1', 'flue-pipe-orientation-joints-2', 'flue-pipes-connections-1', 'flue-pipes-connections-2', 'wall-shielding-floor-protection', 'dates-signatures'
            ]

            # Map section IDs to model classes for wood-stove-masonry forms
            section_model_map = {
                'fireplace-specifications': WoodStoveMasonryFireplaceSpecifications,
                'chimney-construction': WoodStoveMasonryChimneyConstruction,
                'chimney-construction-liners': WoodStoveMasonryChimneyConstructionLiners,
                'chimney-liners': WoodStoveMasonryChimneyLiners,
                'chimney-liners-installation': WoodStoveMasonryChimneyLinersInstallation,
                'chimney-saddles-fire-code': WoodStoveMasonryChimneySaddles,
                'chimney-specifications': WoodStoveMasonryChimneySpecifications,
                'chimney-stability-caps': WoodStoveMasonryChimneyStabilityCaps,
                'chimney-supports': WoodStoveMasonryChimneySupports,
                'clearances-shielding': WoodStoveMasonryClearancesShielding,
                'combustible-materials': WoodStoveMasonryCombustibleMaterials,
                'ember-pad-floor-protection': WoodStoveMasonryEmberPadFloorProtection,
                'flue-pipe-orientation-joints-1': WoodStoveMasonryFluePipeOrientationJoints1,
                'flue-pipe-orientation-joints-2': WoodStoveMasonryFluePipeOrientationJoints2,
                'flue-pipes-connections-1': WoodStoveMasonryFluePipesConnections1,
                'flue-pipes-connections-2': WoodStoveMasonryFluePipesConnections2,
                'wall-shielding-floor-protection': WoodStoveMasonryWallShieldingFloorProtection,
                # 'inspection-details' and 'dates-signatures' are kept in inspection.form_data
            }
        else:
            # Define the section IDs for factory-built forms (original implementation)
            all_sections = [
                'inspection-details', 'chimney-specifications', 'fireplace-specifications',
                'combustible-materials', 'hearth-floor-protection', 'enclosure-ventilation',
                'fireplace-safety', 'chimney-support', 'attic-radiation', 'roof-exterior',
                'chimney-height', 'fire-codes', 'dates-signatures'
            ]

            # Map section IDs to model classes for factory-built forms
            section_model_map = {
                'chimney-specifications': ChimneySpecification,
                'fireplace-specifications': FireplaceSpecification,
                'combustible-materials': CombustibleMaterials,
                'hearth-floor-protection': HearthFloorProtection,
                'enclosure-ventilation': EnclosureVentilation,
                'fireplace-safety': FireplaceSafetyFeatures,
                'chimney-support': ChimneySupportConnection,
                'attic-radiation': AtticRadiationProtection,
                'roof-exterior': RoofExteriorProtection,
                'chimney-height': ChimneyHeightClearance,
                'fire-codes': FireCodesCompliance,
                # 'inspection-details' and 'dates-signatures' are kept in inspection.form_data
            }

        form_data = inspection.form_data or {}
        checklist_data = form_data.get('checklistData', {}) or {}

        def has_non_image_content(value):
            """Recursively check if there is any non-empty, non-photo field value."""
            print(f"DEBUG: Checking value: {value} (type: {type(value)})")
            if value is None:
                print("DEBUG: Value is None, returning False")
                return False
            if isinstance(value, (int, float)):
                print("DEBUG: Value is number, returning True")
                return True
            if isinstance(value, str):
                result = value.strip() != ''
                print(f"DEBUG: Value is string, stripped='{value.strip()}', returning {result}")
                return result
            if isinstance(value, list):
                # A list is considered content if any element (that is not a photo-only) has content
                # If it's a list of strings (e.g., photo URLs), ignore if key implied 'photos' at parent level
                print(f"DEBUG: Value is list with {len(value)} items")
                return any(has_non_image_content(v) for v in value)
            if isinstance(value, dict):
                print(f"DEBUG: Value is dict with keys: {list(value.keys())}")
                for k, v in value.items():
                    # Skip photo fields by name
                    if isinstance(k, str) and k.lower() == 'photos':
                        print(f"DEBUG: Skipping photos field: {k}")
                        continue
                    if has_non_image_content(v):
                        print(f"DEBUG: Found content in dict field {k}")
                        return True
                print("DEBUG: No content found in dict")
                return False
            print(f"DEBUG: Value is {type(value)}, returning False")
            return False

        def section_complete_from_checklist(section_id):
            section_obj = checklist_data.get(section_id)
            if not section_obj:
                return False
            return has_non_image_content(section_obj)

        def section_complete_from_model(model_cls):
            instance = model_cls.query.filter_by(inspection_id=inspection_id).first()
            if not instance:
                print(f"DEBUG: No instance found for {model_cls.__name__} with inspection_id {inspection_id}")
                return False

            print(f"DEBUG: Checking {model_cls.__name__} for inspection_id {inspection_id}")

            # Check if any non-photo, non-meta column has a value
            for col in instance.__table__.columns:
                name = col.name
                if name in ('id', 'inspection_id', 'created_at', 'updated_at'):
                    continue
                if name.endswith('_photos'):
                    continue
                try:
                    val = getattr(instance, name)
                    print(f"DEBUG: Column {name} = {val} (type: {type(val)})")
                    if has_non_image_content(val):
                        print(f"DEBUG: Column {name} has content, marking section as complete")
                        return True
                except Exception as e:
                    print(f"DEBUG: Error checking column {name}: {e}")
                    continue

            print(f"DEBUG: No content found in {model_cls.__name__}")
            return False

        per_section_status = {}
        for section_id in all_sections:
            complete = section_complete_from_checklist(section_id)
            if not complete and section_id in section_model_map:
                complete = section_complete_from_model(section_model_map[section_id])
            # For 'inspection-details' and 'dates-signatures', rely on checklist_data only
            per_section_status[section_id] = bool(complete)

        completed_sections = [s for s, is_done in per_section_status.items() if is_done]
        is_all_complete = all(per_section_status.get(s, False) for s in all_sections)

        # Update inspection.form_data and status
        updated_form_data = dict(form_data)
        updated_form_data['checklistData'] = checklist_data
        updated_form_data['completedSections'] = completed_sections
        inspection.form_data = updated_form_data
        inspection.status = 'completed' if is_all_complete else 'in-progress'
        inspection.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'inspection_id': inspection_id,
            'allSections': all_sections,
            'perSectionStatus': per_section_status,
            'completedSections': completed_sections,
            'status': inspection.status
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==========================================
# FIREPLACE-INSERT FORM ROUTES
# ==========================================

# Fireplace Insert Chimney Specification Routes
@main.route('/api/fireplace-insert/chimney-specifications', methods=['POST'])
def create_fireplace_insert_chimney_specification():
    """Create fireplace insert chimney specification for an inspection"""
    data = request.get_json()
    try:
        print(f"DEBUG: Creating chimney specification with data: {data}")
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if already exists
        existing = FireplaceInsertChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Chimney specification already exists for this inspection'}), 400

        chimney_spec = FireplaceInsertChimneySpecification(inspection_id=inspection_id)
        for key, value in data.items():
            if hasattr(chimney_spec, key) and key != 'inspection_id':
                print(f"DEBUG: Setting {key} = {value}")
                setattr(chimney_spec, key, value)
            else:
                print(f"DEBUG: Skipping field {key} - not found on model or is inspection_id")

        db.session.add(chimney_spec)
        db.session.commit()
        result = chimney_spec.to_dict()
        print(f"DEBUG: Created chimney specification: {result}")
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: Error creating chimney specification: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-specifications/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_chimney_specification(inspection_id):
    """Get fireplace insert chimney specification for an inspection"""
    try:
        print(f"DEBUG: Getting chimney specification for inspection_id: {inspection_id}")
        chimney_spec = FireplaceInsertChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_spec:
            print(f"DEBUG: No chimney specification found for inspection_id: {inspection_id}")
            return jsonify({'error': 'Chimney specification not found'}), 404
        data = chimney_spec.to_dict()
        print(f"DEBUG: Found chimney specification data: {data}")
        return jsonify(data), 200
    except Exception as e:
        print(f"DEBUG: Error getting chimney specification: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-specifications/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_chimney_specification(inspection_id):
    """Update fireplace insert chimney specification for an inspection"""
    data = request.get_json()
    try:
        chimney_spec = FireplaceInsertChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_spec:
            return jsonify({'error': 'Chimney specification not found'}), 404

        for key, value in data.items():
            if hasattr(chimney_spec, key):
                print(f"DEBUG: Updating {key} = {value}")
                setattr(chimney_spec, key, value)
            else:
                print(f"DEBUG: Skipping field {key} - not found on model")

        db.session.commit()
        return jsonify(chimney_spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Fireplace Specification Routes
@main.route('/api/fireplace-insert/fireplace-specifications', methods=['POST'])
def create_fireplace_insert_fireplace_specification():
    """Create fireplace insert fireplace specification for an inspection"""
    data = request.get_json()
    try:
        print(f"DEBUG: Creating fireplace specification with data: {data}")
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertFireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Fireplace specification already exists for this inspection'}), 400

        fireplace_spec = FireplaceInsertFireplaceSpecification(inspection_id=inspection_id)
        for key, value in data.items():
            if hasattr(fireplace_spec, key) and key != 'inspection_id':
                print(f"DEBUG: Updating fireplace spec {key} = {value}")
                setattr(fireplace_spec, key, value)
            else:
                print(f"DEBUG: Skipping field {key} - not found on fireplace spec model")

        db.session.add(fireplace_spec)
        db.session.commit()
        result = fireplace_spec.to_dict()
        print(f"DEBUG: Created fireplace specification: {result}")
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: Error creating fireplace specification: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/fireplace-specifications/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_fireplace_specification(inspection_id):
    """Get fireplace insert fireplace specification for an inspection"""
    try:
        print(f"DEBUG: Getting fireplace specification for inspection_id: {inspection_id}")
        fireplace_spec = FireplaceInsertFireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()
        if not fireplace_spec:
            print(f"DEBUG: No fireplace specification found for inspection_id: {inspection_id}")
            return jsonify({'error': 'Fireplace specification not found'}), 404
        data = fireplace_spec.to_dict()
        print(f"DEBUG: Found fireplace specification data: {data}")
        return jsonify(data), 200
    except Exception as e:
        print(f"DEBUG: Error getting fireplace specification: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/fireplace-specifications/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_fireplace_specification(inspection_id):
    """Update fireplace insert fireplace specification for an inspection"""
    data = request.get_json()
    try:
        fireplace_spec = FireplaceInsertFireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()
        if not fireplace_spec:
            return jsonify({'error': 'Fireplace specification not found'}), 404

        for key, value in data.items():
            if hasattr(fireplace_spec, key):
                print(f"DEBUG: Updating fireplace spec {key} = {value}")
                setattr(fireplace_spec, key, value)
            else:
                print(f"DEBUG: Skipping field {key} - not found on fireplace spec model")

        db.session.commit()
        return jsonify(fireplace_spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Materials & Clearances Routes
@main.route('/api/fireplace-insert/materials-clearances', methods=['POST'])
def create_fireplace_insert_materials_clearances():
    """Create fireplace insert materials & clearances for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertMaterialsClearances.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Materials & clearances already exists for this inspection'}), 400

        materials_clearances = FireplaceInsertMaterialsClearances(inspection_id=inspection_id)

        # Map nested section data to individual fields
        section_mappings = {
            'combustibleMantle': 'combustible_mantle',
            'topTrimFacing': 'top_trim_facing',
            'sideTrimFacingRight': 'side_trim_facing_right',
            'sideTrimFacingLeft': 'side_trim_facing_left',
            'combustibleSideWall': 'combustible_side_wall'
        }

        for frontend_key, db_prefix in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    # Map individual fields
                    setattr(materials_clearances, f'{db_prefix}_required_uncertified', section_data.get('requiredUncertified'))
                    setattr(materials_clearances, f'{db_prefix}_required_certified', section_data.get('requiredCertified'))
                    setattr(materials_clearances, f'{db_prefix}_present', section_data.get('presentValue'))
                    setattr(materials_clearances, f'{db_prefix}_compliance', section_data.get('codeCompliance'))
                    setattr(materials_clearances, f'{db_prefix}_photos', section_data.get('photos'))

        # Handle additional notes
        if 'additionalNotes' in data:
            materials_clearances.additional_notes = data['additionalNotes']

        db.session.add(materials_clearances)
        db.session.commit()
        return jsonify(materials_clearances.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/materials-clearances/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_materials_clearances(inspection_id):
    """Get fireplace insert materials & clearances for an inspection"""
    try:
        materials_clearances = FireplaceInsertMaterialsClearances.query.filter_by(inspection_id=inspection_id).first()
        if not materials_clearances:
            return jsonify({'error': 'Materials & clearances not found'}), 404
        return jsonify(materials_clearances.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/materials-clearances/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_materials_clearances(inspection_id):
    """Update fireplace insert materials & clearances for an inspection"""
    data = request.get_json()
    try:
        materials_clearances = FireplaceInsertMaterialsClearances.query.filter_by(inspection_id=inspection_id).first()
        if not materials_clearances:
            return jsonify({'error': 'Materials & clearances not found'}), 404

        # Map nested section data to individual fields
        section_mappings = {
            'combustibleMantle': 'combustible_mantle',
            'topTrimFacing': 'top_trim_facing',
            'sideTrimFacingRight': 'side_trim_facing_right',
            'sideTrimFacingLeft': 'side_trim_facing_left',
            'combustibleSideWall': 'combustible_side_wall'
        }

        for frontend_key, db_prefix in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    # Map individual fields
                    setattr(materials_clearances, f'{db_prefix}_required_uncertified', section_data.get('requiredUncertified'))
                    setattr(materials_clearances, f'{db_prefix}_required_certified', section_data.get('requiredCertified'))
                    setattr(materials_clearances, f'{db_prefix}_present', section_data.get('presentValue'))
                    setattr(materials_clearances, f'{db_prefix}_compliance', section_data.get('codeCompliance'))
                    setattr(materials_clearances, f'{db_prefix}_photos', section_data.get('photos'))

        # Handle additional notes
        if 'additionalNotes' in data:
            materials_clearances.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(materials_clearances.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Ember Pad & Floor Protection Routes
@main.route('/api/fireplace-insert/ember-pad-floor-protection', methods=['POST'])
def create_fireplace_insert_ember_pad_floor_protection():
    """Create fireplace insert ember pad & floor protection for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Ember pad & floor protection already exists for this inspection'}), 400

        ember_pad_floor = FireplaceInsertEmberPadFloorProtection(inspection_id=inspection_id)

        # Map nested section data to individual fields
        section_mappings = {
            'emberpadMaterial': {
                'prefix': 'emberpad_material',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'emberpadFront': {
                'prefix': 'emberpad_front',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'emberpadRightSide': {
                'prefix': 'emberpad_right_side',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'emberpadLeftSide': {
                'prefix': 'emberpad_left_side',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'floorProtectionMaterial': {
                'prefix': 'floor_protection_material',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'radiantFloorProtection': {
                'prefix': 'radiant_floor_protection',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'floorProtectionFront': {
                'prefix': 'floor_protection_front',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'floorProtectionRightSide': {
                'prefix': 'floor_protection_right_side',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'floorProtectionLeftSide': {
                'prefix': 'floor_protection_left_side',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            }
        }

        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for field in mapping['fields']:
                        if field in section_data:
                            db_field_name = f'{prefix}_required_uncertified' if field == 'requiredUncertified' else \
                                          f'{prefix}_required_certified' if field == 'requiredCertified' else \
                                          f'{prefix}_required' if field == 'requiredValue' else \
                                          f'{prefix}_present' if field == 'presentValue' else \
                                          f'{prefix}_compliance' if field == 'codeCompliance' else \
                                          f'{prefix}_photos' if field == 'photos' else f'{prefix}_{field}'
                            setattr(ember_pad_floor, db_field_name, section_data[field])

        # Handle additional notes
        if 'additionalNotes' in data:
            ember_pad_floor.additional_notes = data['additionalNotes']

        db.session.add(ember_pad_floor)
        db.session.commit()
        return jsonify(ember_pad_floor.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/ember-pad-floor-protection/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_ember_pad_floor_protection(inspection_id):
    """Get fireplace insert ember pad & floor protection for an inspection"""
    try:
        ember_pad_floor = FireplaceInsertEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not ember_pad_floor:
            return jsonify({'error': 'Ember pad & floor protection not found'}), 404
        return jsonify(ember_pad_floor.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/ember-pad-floor-protection/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_ember_pad_floor_protection(inspection_id):
    """Update fireplace insert ember pad & floor protection for an inspection"""
    data = request.get_json()
    try:
        ember_pad_floor = FireplaceInsertEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not ember_pad_floor:
            return jsonify({'error': 'Ember pad & floor protection not found'}), 404

        # Map nested section data to individual fields
        section_mappings = {
            'emberpadMaterial': {
                'prefix': 'emberpad_material',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'emberpadFront': {
                'prefix': 'emberpad_front',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'emberpadRightSide': {
                'prefix': 'emberpad_right_side',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'emberpadLeftSide': {
                'prefix': 'emberpad_left_side',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'floorProtectionMaterial': {
                'prefix': 'floor_protection_material',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'radiantFloorProtection': {
                'prefix': 'radiant_floor_protection',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'floorProtectionFront': {
                'prefix': 'floor_protection_front',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'floorProtectionRightSide': {
                'prefix': 'floor_protection_right_side',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'floorProtectionLeftSide': {
                'prefix': 'floor_protection_left_side',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            }
        }

        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for field in mapping['fields']:
                        if field in section_data:
                            db_field_name = f'{prefix}_required_uncertified' if field == 'requiredUncertified' else \
                                          f'{prefix}_required_certified' if field == 'requiredCertified' else \
                                          f'{prefix}_required' if field == 'requiredValue' else \
                                          f'{prefix}_present' if field == 'presentValue' else \
                                          f'{prefix}_compliance' if field == 'codeCompliance' else \
                                          f'{prefix}_photos' if field == 'photos' else f'{prefix}_{field}'
                            setattr(ember_pad_floor, db_field_name, section_data[field])

        # Handle additional notes
        if 'additionalNotes' in data:
            ember_pad_floor.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(ember_pad_floor.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Chimney Support & Connection Routes
@main.route('/api/fireplace-insert/chimney-support-connection', methods=['POST'])
def create_fireplace_insert_chimney_support_connection():
    """Create fireplace insert chimney support & connection for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Chimney support & connection already exists for this inspection'}), 400

        chimney_support = FireplaceInsertChimneySupportConnection(inspection_id=inspection_id)

        # Map nested section data to individual fields
        section_mappings = {
            'electricalOutletWires': {
                'prefix': 'electrical_outlet_wires',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'fireplaceModification': {
                'prefix': 'fireplace_modification',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos', 'hasFireplaceBeenModified']
            },
            'coAlarmSolidFuel': {
                'prefix': 'co_alarm_solid_fuel',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'coAlarmSolidFuelNbc': {
                'prefix': 'co_alarm_solid_fuel_nbc',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'generalCoAlarm': {
                'prefix': 'general_co_alarm',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'notesResponsibility': {
                'prefix': 'notes_responsibility',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos', 'condition']
            }
        }

        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for field in mapping['fields']:
                        if field in section_data:
                            if field == 'hasFireplaceBeenModified':
                                # Convert boolean to string for database
                                value = 'yes' if section_data[field] else 'no'
                                setattr(chimney_support, f'{prefix}_has_been_modified', value)
                            else:
                                db_field_name = f'{prefix}_required_uncertified' if field == 'requiredUncertified' else \
                                              f'{prefix}_required_certified' if field == 'requiredCertified' else \
                                              f'{prefix}_required' if field == 'requiredValue' else \
                                              f'{prefix}_present' if field == 'presentValue' else \
                                              f'{prefix}_compliance' if field == 'codeCompliance' else \
                                              f'{prefix}_photos' if field == 'photos' else \
                                              f'{prefix}_condition' if field == 'condition' else f'{prefix}_{field}'

                                # Convert boolean values to strings for database storage
                                value = section_data[field]
                                if field == 'presentValue' and isinstance(value, bool):
                                    value = 'yes' if value else 'no'

                                setattr(chimney_support, db_field_name, value)

        # Handle additional notes
        if 'additionalNotes' in data:
            chimney_support.additional_notes = data['additionalNotes']

        db.session.add(chimney_support)
        db.session.commit()
        return jsonify(chimney_support.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-support-connection/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_chimney_support_connection(inspection_id):
    """Get fireplace insert chimney support & connection for an inspection"""
    try:
        chimney_support = FireplaceInsertChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_support:
            return jsonify({'error': 'Chimney support & connection not found'}), 404
        return jsonify(chimney_support.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-support-connection/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_chimney_support_connection(inspection_id):
    """Update fireplace insert chimney support & connection for an inspection"""
    data = request.get_json()
    try:
        chimney_support = FireplaceInsertChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_support:
            return jsonify({'error': 'Chimney support & connection not found'}), 404

        # Map nested section data to individual fields
        section_mappings = {
            'electricalOutletWires': {
                'prefix': 'electrical_outlet_wires',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'fireplaceModification': {
                'prefix': 'fireplace_modification',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos', 'hasFireplaceBeenModified']
            },
            'coAlarmSolidFuel': {
                'prefix': 'co_alarm_solid_fuel',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'coAlarmSolidFuelNbc': {
                'prefix': 'co_alarm_solid_fuel_nbc',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'generalCoAlarm': {
                'prefix': 'general_co_alarm',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'notesResponsibility': {
                'prefix': 'notes_responsibility',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos', 'condition']
            }
        }

        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for field in mapping['fields']:
                        if field in section_data:
                            if field == 'hasFireplaceBeenModified':
                                # Convert boolean to string for database
                                value = 'yes' if section_data[field] else 'no'
                                setattr(chimney_support, f'{prefix}_has_been_modified', value)
                            else:
                                db_field_name = f'{prefix}_required_uncertified' if field == 'requiredUncertified' else \
                                              f'{prefix}_required_certified' if field == 'requiredCertified' else \
                                              f'{prefix}_required' if field == 'requiredValue' else \
                                              f'{prefix}_present' if field == 'presentValue' else \
                                              f'{prefix}_compliance' if field == 'codeCompliance' else \
                                              f'{prefix}_photos' if field == 'photos' else \
                                              f'{prefix}_condition' if field == 'condition' else f'{prefix}_{field}'

                                # Convert boolean values to strings for database storage
                                value = section_data[field]
                                if field == 'presentValue' and isinstance(value, bool):
                                    value = 'yes' if value else 'no'

                                setattr(chimney_support, db_field_name, value)

        # Handle additional notes
        if 'additionalNotes' in data:
            chimney_support.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(chimney_support.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Fireplace Safety Features Routes
@main.route('/api/fireplace-insert/fireplace-safety-features', methods=['POST'])
def create_fireplace_insert_fireplace_safety_features():
    """Create fireplace insert fireplace safety features for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertFireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Fireplace safety features already exists for this inspection'}), 400

        safety_features = FireplaceInsertFireplaceSafetyFeatures(inspection_id=inspection_id)

        # Define mapping between frontend sections and backend fields
        section_mappings = {
            'manufacturerModel': {
                'prefix': 'manufacturer_model',
                'fields': ['manufacturer', 'model', 'listingAgency', 'isListingAgencyManualAvailable', 'presentValue', 'codeCompliance', 'photos']
            },
            'certification': {
                'prefix': 'certification',
                'fields': ['certificationStandard', 'listingAgencyCertification', 'diameter', 'comments', 'presentValue', 'codeCompliance', 'photos']
            },
            'linerFromAppliance': {
                'prefix': 'liner_from_appliance',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'connectionToLiner': {
                'prefix': 'connection_to_liner',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'continuousLiner': {
                'prefix': 'continuous_liner',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'connectors': {
                'prefix': 'connectors',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'linerBaseTee': {
                'prefix': 'liner_base_tee',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            }
        }

        # Process each section
        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for field in mapping['fields']:
                        if field in section_data:
                            db_field_name = f'{prefix}_{field.lower().replace("agency", "agency").replace("standard", "standard").replace("uncertified", "uncertified").replace("certified", "certified").replace("compliance", "compliance")}'

                            # Handle special field name mappings
                            if field == 'manufacturer':
                                db_field_name = f'{prefix}_manufacturer'
                            elif field == 'model':
                                db_field_name = f'{prefix}_model'
                            elif field == 'listingAgency':
                                db_field_name = f'{prefix}_listing_agency'
                            elif field == 'isListingAgencyManualAvailable':
                                db_field_name = f'{prefix}_is_listing_agency_manual_available'
                            elif field == 'certificationStandard':
                                db_field_name = f'{prefix}_certification_standard'
                            elif field == 'listingAgencyCertification':
                                db_field_name = f'{prefix}_listing_agency_certification'
                            elif field == 'requiredValue':
                                db_field_name = f'{prefix}_required_value'
                            elif field == 'requiredUncertified':
                                db_field_name = f'{prefix}_required_uncertified'
                            elif field == 'requiredCertified':
                                db_field_name = f'{prefix}_required_certified'
                            elif field == 'presentValue':
                                db_field_name = f'{prefix}_present_value'
                            elif field == 'codeCompliance':
                                db_field_name = f'{prefix}_code_compliance'
                            elif field == 'photos':
                                db_field_name = f'{prefix}_photos'

                            # Convert boolean values to strings for database storage
                            value = section_data[field]
                            if field == 'requiredValue' and isinstance(value, bool):
                                value = 'yes' if value else 'no'
                            elif field == 'isListingAgencyManualAvailable' and isinstance(value, bool):
                                value = 'yes' if value else 'no'

                            setattr(safety_features, db_field_name, value)

        # Handle additional notes
        if 'additionalNotes' in data:
            safety_features.additional_notes = data['additionalNotes']

        db.session.add(safety_features)
        db.session.commit()
        return jsonify(safety_features.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/fireplace-safety-features/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_fireplace_safety_features(inspection_id):
    """Get fireplace insert fireplace safety features for an inspection"""
    try:
        safety_features = FireplaceInsertFireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()
        if not safety_features:
            return jsonify({'error': 'Fireplace safety features not found'}), 404
        return jsonify(safety_features.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/fireplace-safety-features/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_fireplace_safety_features(inspection_id):
    """Update fireplace insert fireplace safety features for an inspection"""
    data = request.get_json()
    try:
        safety_features = FireplaceInsertFireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()
        if not safety_features:
            return jsonify({'error': 'Fireplace safety features not found'}), 404

        # Define mapping between frontend sections and backend fields
        section_mappings = {
            'manufacturerModel': {
                'prefix': 'manufacturer_model',
                'fields': ['manufacturer', 'model', 'listingAgency', 'isListingAgencyManualAvailable', 'presentValue', 'codeCompliance', 'photos']
            },
            'certification': {
                'prefix': 'certification',
                'fields': ['certificationStandard', 'listingAgencyCertification', 'diameter', 'comments', 'presentValue', 'codeCompliance', 'photos']
            },
            'linerFromAppliance': {
                'prefix': 'liner_from_appliance',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'connectionToLiner': {
                'prefix': 'connection_to_liner',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'continuousLiner': {
                'prefix': 'continuous_liner',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'connectors': {
                'prefix': 'connectors',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'linerBaseTee': {
                'prefix': 'liner_base_tee',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            }
        }

        # Process each section
        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for field in mapping['fields']:
                        if field in section_data:
                            db_field_name = f'{prefix}_{field.lower().replace("agency", "agency").replace("standard", "standard").replace("uncertified", "uncertified").replace("certified", "certified").replace("compliance", "compliance")}'

                            # Handle special field name mappings
                            if field == 'manufacturer':
                                db_field_name = f'{prefix}_manufacturer'
                            elif field == 'model':
                                db_field_name = f'{prefix}_model'
                            elif field == 'listingAgency':
                                db_field_name = f'{prefix}_listing_agency'
                            elif field == 'isListingAgencyManualAvailable':
                                db_field_name = f'{prefix}_is_listing_agency_manual_available'
                            elif field == 'certificationStandard':
                                db_field_name = f'{prefix}_certification_standard'
                            elif field == 'listingAgencyCertification':
                                db_field_name = f'{prefix}_listing_agency_certification'
                            elif field == 'requiredValue':
                                db_field_name = f'{prefix}_required_value'
                            elif field == 'requiredUncertified':
                                db_field_name = f'{prefix}_required_uncertified'
                            elif field == 'requiredCertified':
                                db_field_name = f'{prefix}_required_certified'
                            elif field == 'presentValue':
                                db_field_name = f'{prefix}_present_value'
                            elif field == 'codeCompliance':
                                db_field_name = f'{prefix}_code_compliance'
                            elif field == 'photos':
                                db_field_name = f'{prefix}_photos'

                            # Convert boolean values to strings for database storage
                            value = section_data[field]
                            if field == 'requiredValue' and isinstance(value, bool):
                                value = 'yes' if value else 'no'
                            elif field == 'isListingAgencyManualAvailable' and isinstance(value, bool):
                                value = 'yes' if value else 'no'

                            setattr(safety_features, db_field_name, value)

        # Handle additional notes
        if 'additionalNotes' in data:
            safety_features.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(safety_features.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Liner & Appliance Checks Routes
@main.route('/api/fireplace-insert/liner-appliance-checks', methods=['POST'])
def create_fireplace_insert_liner_appliance_checks():
    """Create fireplace insert liner & appliance checks for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertLinerApplianceChecks.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Liner & appliance checks already exists for this inspection'}), 400

        liner_checks = FireplaceInsertLinerApplianceChecks(inspection_id=inspection_id)

        # Define mapping between frontend sections and backend fields
        section_mappings = {
            'linerBaseTeeSupport': {
                'prefix': 'liner_base_tee_support',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'linerFlashingStormCollar': {
                'prefix': 'liner_flashing_storm_collar',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'insulatedLiner': {
                'prefix': 'insulated_liner',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'clearanceRequirements': {
                'prefix': 'clearance_requirements',
                'fields': ['enterData']
            }
        }

        # Process each section
        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for field in mapping['fields']:
                        if field in section_data:
                            db_field_name = f'{prefix}_{field.lower().replace("uncertified", "uncertified").replace("certified", "certified").replace("compliance", "compliance")}'

                            # Handle special field name mappings
                            if field == 'requiredValue':
                                db_field_name = f'{prefix}_required_value'
                            elif field == 'requiredUncertified':
                                db_field_name = f'{prefix}_required_uncertified'
                            elif field == 'requiredCertified':
                                db_field_name = f'{prefix}_required_certified'
                            elif field == 'presentValue':
                                db_field_name = f'{prefix}_present_value'
                            elif field == 'codeCompliance':
                                db_field_name = f'{prefix}_code_compliance'
                            elif field == 'photos':
                                db_field_name = f'{prefix}_photos'
                            elif field == 'enterData':
                                db_field_name = f'{prefix}_enter_data'

                            # Convert boolean values to strings for database storage
                            value = section_data[field]
                            if field == 'requiredValue' and isinstance(value, bool):
                                value = 'yes' if value else 'no'

                            setattr(liner_checks, db_field_name, value)

        # Handle additional notes
        if 'additionalNotes' in data:
            liner_checks.additional_notes = data['additionalNotes']

        db.session.add(liner_checks)
        db.session.commit()
        return jsonify(liner_checks.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/liner-appliance-checks/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_liner_appliance_checks(inspection_id):
    """Get fireplace insert liner & appliance checks for an inspection"""
    try:
        liner_checks = FireplaceInsertLinerApplianceChecks.query.filter_by(inspection_id=inspection_id).first()
        if not liner_checks:
            return jsonify({'error': 'Liner & appliance checks not found'}), 404
        return jsonify(liner_checks.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/liner-appliance-checks/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_liner_appliance_checks(inspection_id):
    """Update fireplace insert liner & appliance checks for an inspection"""
    data = request.get_json()
    try:
        liner_checks = FireplaceInsertLinerApplianceChecks.query.filter_by(inspection_id=inspection_id).first()
        if not liner_checks:
            return jsonify({'error': 'Liner & appliance checks not found'}), 404

        # Define mapping between frontend sections and backend fields
        section_mappings = {
            'linerBaseTeeSupport': {
                'prefix': 'liner_base_tee_support',
                'fields': ['requiredValue', 'presentValue', 'codeCompliance', 'photos']
            },
            'linerFlashingStormCollar': {
                'prefix': 'liner_flashing_storm_collar',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'insulatedLiner': {
                'prefix': 'insulated_liner',
                'fields': ['requiredUncertified', 'requiredCertified', 'presentValue', 'codeCompliance', 'photos']
            },
            'clearanceRequirements': {
                'prefix': 'clearance_requirements',
                'fields': ['enterData']
            }
        }

        # Process each section
        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for field in mapping['fields']:
                        if field in section_data:
                            db_field_name = f'{prefix}_{field.lower().replace("uncertified", "uncertified").replace("certified", "certified").replace("compliance", "compliance")}'

                            # Handle special field name mappings
                            if field == 'requiredValue':
                                db_field_name = f'{prefix}_required_value'
                            elif field == 'requiredUncertified':
                                db_field_name = f'{prefix}_required_uncertified'
                            elif field == 'requiredCertified':
                                db_field_name = f'{prefix}_required_certified'
                            elif field == 'presentValue':
                                db_field_name = f'{prefix}_present_value'
                            elif field == 'codeCompliance':
                                db_field_name = f'{prefix}_code_compliance'
                            elif field == 'photos':
                                db_field_name = f'{prefix}_photos'
                            elif field == 'enterData':
                                db_field_name = f'{prefix}_enter_data'

                            # Convert boolean values to strings for database storage
                            value = section_data[field]
                            if field == 'requiredValue' and isinstance(value, bool):
                                value = 'yes' if value else 'no'

                            setattr(liner_checks, db_field_name, value)

        # Handle additional notes
        if 'additionalNotes' in data:
            liner_checks.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(liner_checks.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Appliance & Masonry Checks Routes
@main.route('/api/fireplace-insert/appliance-masonry-checks', methods=['POST'])
def create_fireplace_insert_appliance_masonry_checks():
    """Create fireplace insert appliance & masonry checks for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertApplianceMasonryChecks.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Appliance & masonry checks already exists for this inspection'}), 400

        masonry_checks = FireplaceInsertApplianceMasonryChecks(inspection_id=inspection_id)

        # Define mapping between frontend sections and backend fields
        section_mappings = {
            'applianceStandard': {
                'prefix': 'appliance_standard',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos']
            },
            'footings': {
                'prefix': 'footings',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos']
            },
            'fireplaceChimneys': {
                'prefix': 'fireplace_chimneys',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos', 'height', 'width', 'total', 'fluesRequired']
            },
            'lintelsArches': {
                'prefix': 'lintels_arches',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos']
            },
            'obcLintelsArches': {
                'prefix': 'obc_lintels_arches',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos']
            },
            'corbelling': {
                'prefix': 'corbelling',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos']
            }
        }

        # Process each section
        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for field in mapping['fields']:
                        if field in section_data:
                            db_field_name = f'{prefix}_{field.lower().replace("compliance", "compliance")}'

                            # Handle special field name mappings
                            if field == 'condition':
                                db_field_name = f'{prefix}_condition'
                            elif field == 'comments':
                                db_field_name = f'{prefix}_comments'
                            elif field == 'codeCompliance':
                                db_field_name = f'{prefix}_code_compliance'
                            elif field == 'photos':
                                db_field_name = f'{prefix}_photos'
                            elif field == 'height':
                                db_field_name = f'{prefix}_height'
                            elif field == 'width':
                                db_field_name = f'{prefix}_width'
                            elif field == 'total':
                                db_field_name = f'{prefix}_total'
                            elif field == 'fluesRequired':
                                db_field_name = f'{prefix}_flues_required'

                            setattr(masonry_checks, db_field_name, section_data[field])

        # Handle additional notes
        if 'additionalNotes' in data:
            masonry_checks.additional_notes = data['additionalNotes']

        db.session.add(masonry_checks)
        db.session.commit()
        return jsonify(masonry_checks.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/appliance-masonry-checks/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_appliance_masonry_checks(inspection_id):
    """Get fireplace insert appliance & masonry checks for an inspection"""
    try:
        masonry_checks = FireplaceInsertApplianceMasonryChecks.query.filter_by(inspection_id=inspection_id).first()
        if not masonry_checks:
            return jsonify({'error': 'Appliance & masonry checks not found'}), 404
        return jsonify(masonry_checks.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/appliance-masonry-checks/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_appliance_masonry_checks(inspection_id):
    """Update fireplace insert appliance & masonry checks for an inspection"""
    data = request.get_json()
    try:
        masonry_checks = FireplaceInsertApplianceMasonryChecks.query.filter_by(inspection_id=inspection_id).first()
        if not masonry_checks:
            return jsonify({'error': 'Appliance & masonry checks not found'}), 404

        # Define mapping between frontend sections and backend fields
        section_mappings = {
            'applianceStandard': {
                'prefix': 'appliance_standard',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos']
            },
            'footings': {
                'prefix': 'footings',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos']
            },
            'fireplaceChimneys': {
                'prefix': 'fireplace_chimneys',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos', 'height', 'width', 'total', 'fluesRequired']
            },
            'lintelsArches': {
                'prefix': 'lintels_arches',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos']
            },
            'obcLintelsArches': {
                'prefix': 'obc_lintels_arches',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos']
            },
            'corbelling': {
                'prefix': 'corbelling',
                'fields': ['condition', 'comments', 'codeCompliance', 'photos']
            }
        }

        # Process each section
        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for field in mapping['fields']:
                        if field in section_data:
                            db_field_name = f'{prefix}_{field.lower().replace("compliance", "compliance")}'

                            # Handle special field name mappings
                            if field == 'condition':
                                db_field_name = f'{prefix}_condition'
                            elif field == 'comments':
                                db_field_name = f'{prefix}_comments'
                            elif field == 'codeCompliance':
                                db_field_name = f'{prefix}_code_compliance'
                            elif field == 'photos':
                                db_field_name = f'{prefix}_photos'
                            elif field == 'height':
                                db_field_name = f'{prefix}_height'
                            elif field == 'width':
                                db_field_name = f'{prefix}_width'
                            elif field == 'total':
                                db_field_name = f'{prefix}_total'
                            elif field == 'fluesRequired':
                                db_field_name = f'{prefix}_flues_required'

                            setattr(masonry_checks, db_field_name, section_data[field])

        # Handle additional notes
        if 'additionalNotes' in data:
            masonry_checks.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(masonry_checks.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert CO Alarms & Liners Routes
@main.route('/api/fireplace-insert/co-alarms-liners', methods=['POST'])
def create_fireplace_insert_co_alarms_liners():
    """Create fireplace insert CO alarms & liners for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertCOAlarmsLiners.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'CO alarms & liners already exists for this inspection'}), 400

        co_alarms_liners = FireplaceInsertCOAlarmsLiners(inspection_id=inspection_id)

        # Handle nested section data
        section_mappings = {
            'abcCombustionAir': {
                'condition': 'abc_combustion_air_condition',
                'comments': 'abc_combustion_air_comments',
                'codeCompliance': 'abc_combustion_air_code_compliance',
                'photos': 'abc_combustion_air_photos'
            },
            'nbcCombustionAir': {
                'condition': 'nbc_combustion_air_condition',
                'comments': 'nbc_combustion_air_comments',
                'codeCompliance': 'nbc_combustion_air_code_compliance',
                'photos': 'nbc_combustion_air_photos'
            },
            'obcCombustionAir': {
                'condition': 'obc_combustion_air_condition',
                'comments': 'obc_combustion_air_comments',
                'codeCompliance': 'obc_combustion_air_code_compliance',
                'photos': 'obc_combustion_air_photos'
            },
            'brickSteelLiners': {
                'condition': 'brick_steel_liners_condition',
                'comments': 'brick_steel_liners_comments',
                'codeCompliance': 'brick_steel_liners_code_compliance',
                'photos': 'brick_steel_liners_photos'
            },
            'firebrickLiners1': {
                'condition': 'firebrick_liners_1_condition',
                'comments': 'firebrick_liners_1_comments',
                'codeCompliance': 'firebrick_liners_1_code_compliance',
                'photos': 'firebrick_liners_1_photos'
            },
            'firebrickLiners2': {
                'condition': 'firebrick_liners_2_condition',
                'comments': 'firebrick_liners_2_comments',
                'codeCompliance': 'firebrick_liners_2_code_compliance',
                'photos': 'firebrick_liners_2_photos'
            }
        }

        for section_key, section_data in data.items():
            if section_key in section_mappings and isinstance(section_data, dict):
                field_mappings = section_mappings[section_key]
                for frontend_field, backend_field in field_mappings.items():
                    if frontend_field in section_data:
                        setattr(co_alarms_liners, backend_field, section_data[frontend_field])

        # Handle additional_notes if present
        if 'additionalNotes' in data:
            co_alarms_liners.additional_notes = data['additionalNotes']

        db.session.add(co_alarms_liners)
        db.session.commit()
        return jsonify(co_alarms_liners.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/co-alarms-liners/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_co_alarms_liners(inspection_id):
    """Get fireplace insert CO alarms & liners for an inspection"""
    try:
        co_alarms_liners = FireplaceInsertCOAlarmsLiners.query.filter_by(inspection_id=inspection_id).first()
        if not co_alarms_liners:
            return jsonify({'error': 'CO alarms & liners not found'}), 404
        return jsonify(co_alarms_liners.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/co-alarms-liners/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_co_alarms_liners(inspection_id):
    """Update fireplace insert CO alarms & liners for an inspection"""
    data = request.get_json()
    try:
        co_alarms_liners = FireplaceInsertCOAlarmsLiners.query.filter_by(inspection_id=inspection_id).first()
        if not co_alarms_liners:
            return jsonify({'error': 'CO alarms & liners not found'}), 404

        # Handle nested section data
        section_mappings = {
            'abcCombustionAir': {
                'condition': 'abc_combustion_air_condition',
                'comments': 'abc_combustion_air_comments',
                'codeCompliance': 'abc_combustion_air_code_compliance',
                'photos': 'abc_combustion_air_photos'
            },
            'nbcCombustionAir': {
                'condition': 'nbc_combustion_air_condition',
                'comments': 'nbc_combustion_air_comments',
                'codeCompliance': 'nbc_combustion_air_code_compliance',
                'photos': 'nbc_combustion_air_photos'
            },
            'obcCombustionAir': {
                'condition': 'obc_combustion_air_condition',
                'comments': 'obc_combustion_air_comments',
                'codeCompliance': 'obc_combustion_air_code_compliance',
                'photos': 'obc_combustion_air_photos'
            },
            'brickSteelLiners': {
                'condition': 'brick_steel_liners_condition',
                'comments': 'brick_steel_liners_comments',
                'codeCompliance': 'brick_steel_liners_code_compliance',
                'photos': 'brick_steel_liners_photos'
            },
            'firebrickLiners1': {
                'condition': 'firebrick_liners_1_condition',
                'comments': 'firebrick_liners_1_comments',
                'codeCompliance': 'firebrick_liners_1_code_compliance',
                'photos': 'firebrick_liners_1_photos'
            },
            'firebrickLiners2': {
                'condition': 'firebrick_liners_2_condition',
                'comments': 'firebrick_liners_2_comments',
                'codeCompliance': 'firebrick_liners_2_code_compliance',
                'photos': 'firebrick_liners_2_photos'
            }
        }

        for section_key, section_data in data.items():
            if section_key in section_mappings and isinstance(section_data, dict):
                field_mappings = section_mappings[section_key]
                for frontend_field, backend_field in field_mappings.items():
                    if frontend_field in section_data:
                        setattr(co_alarms_liners, backend_field, section_data[frontend_field])

        # Handle additional_notes if present
        if 'additionalNotes' in data:
            co_alarms_liners.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(co_alarms_liners.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Chimney Liner & Joints Details Routes
@main.route('/api/fireplace-insert/chimney-liner-joints-details', methods=['POST'])
def create_fireplace_insert_chimney_liner_joints_details():
    """Create fireplace insert chimney liner & joints details for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertChimneyLinerJointsDetails.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Chimney liner & joints details already exists for this inspection'}), 400

        chimney_liner_details = FireplaceInsertChimneyLinerJointsDetails(inspection_id=inspection_id)
        for key, value in data.items():
            if hasattr(chimney_liner_details, key) and key != 'inspection_id':
                setattr(chimney_liner_details, key, value)

        db.session.add(chimney_liner_details)
        db.session.commit()
        return jsonify(chimney_liner_details.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-liner-joints-details/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_chimney_liner_joints_details(inspection_id):
    """Get fireplace insert chimney liner & joints details for an inspection"""
    try:
        chimney_liner_details = FireplaceInsertChimneyLinerJointsDetails.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_liner_details:
            return jsonify({'error': 'Chimney liner & joints details not found'}), 404
        return jsonify(chimney_liner_details.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-liner-joints-details/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_chimney_liner_joints_details(inspection_id):
    """Update fireplace insert chimney liner & joints details for an inspection"""
    data = request.get_json()
    try:
        chimney_liner_details = FireplaceInsertChimneyLinerJointsDetails.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_liner_details:
            return jsonify({'error': 'Chimney liner & joints details not found'}), 404

        for key, value in data.items():
            if hasattr(chimney_liner_details, key):
                setattr(chimney_liner_details, key, value)

        db.session.commit()
        return jsonify(chimney_liner_details.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Hearth Support Routes
@main.route('/api/fireplace-insert/hearth-support', methods=['POST'])
def create_fireplace_insert_hearth_support():
    """Create fireplace insert hearth support for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertHearthSupport.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Hearth support already exists for this inspection'}), 400

        hearth_support = FireplaceInsertHearthSupport(inspection_id=inspection_id)

        # Define mapping between frontend sections and backend fields
        section_mappings = {
            'hearthExtension': {
                'prefix': 'hearth_extension'
            },
            'hearthSupport1': {
                'prefix': 'hearth_support_1'
            },
            'hearthSupport2': {
                'prefix': 'hearth_support_2'
            },
            'smokeChamberSlope': {
                'prefix': 'smoke_chamber_slope'
            },
            'wallThickness': {
                'prefix': 'wall_thickness'
            },
            'clearanceToOpening': {
                'prefix': 'clearance_to_opening'
            }
        }

        # Define field name mapping from frontend to backend
        field_mappings = {
            'condition': 'condition',
            'comments': 'comments',
            'codeCompliance': 'compliance',
            'photos': 'photos'
        }

        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for frontend_field, backend_field in field_mappings.items():
                        if frontend_field in section_data:
                            db_field_name = f'{prefix}_{backend_field}'
                            value = section_data[frontend_field]
                            setattr(hearth_support, db_field_name, value)

        db.session.add(hearth_support)
        db.session.commit()
        return jsonify(hearth_support.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/hearth-support/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_hearth_support(inspection_id):
    """Get fireplace insert hearth support for an inspection"""
    try:
        hearth_support = FireplaceInsertHearthSupport.query.filter_by(inspection_id=inspection_id).first()
        if not hearth_support:
            return jsonify({'error': 'Hearth support not found'}), 404
        return jsonify(hearth_support.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/hearth-support/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_hearth_support(inspection_id):
    """Update fireplace insert hearth support for an inspection"""
    data = request.get_json()
    try:
        hearth_support = FireplaceInsertHearthSupport.query.filter_by(inspection_id=inspection_id).first()
        if not hearth_support:
            return jsonify({'error': 'Hearth support not found'}), 404

        # Define mapping between frontend sections and backend fields
        section_mappings = {
            'hearthExtension': {
                'prefix': 'hearth_extension'
            },
            'hearthSupport1': {
                'prefix': 'hearth_support_1'
            },
            'hearthSupport2': {
                'prefix': 'hearth_support_2'
            },
            'smokeChamberSlope': {
                'prefix': 'smoke_chamber_slope'
            },
            'wallThickness': {
                'prefix': 'wall_thickness'
            },
            'clearanceToOpening': {
                'prefix': 'clearance_to_opening'
            }
        }

        # Define field name mapping from frontend to backend
        field_mappings = {
            'condition': 'condition',
            'comments': 'comments',
            'codeCompliance': 'compliance',
            'photos': 'photos'
        }

        for frontend_key, mapping in section_mappings.items():
            if frontend_key in data:
                section_data = data[frontend_key]
                if isinstance(section_data, dict):
                    prefix = mapping['prefix']
                    for frontend_field, backend_field in field_mappings.items():
                        if frontend_field in section_data:
                            db_field_name = f'{prefix}_{backend_field}'
                            value = section_data[frontend_field]
                            setattr(hearth_support, db_field_name, value)

        db.session.commit()
        return jsonify(hearth_support.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Clearances Routes
@main.route('/api/fireplace-insert/clearances', methods=['POST'])
def create_fireplace_insert_clearances():
    """Create fireplace insert clearances for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertClearances.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Clearances already exists for this inspection'}), 400

        clearances = FireplaceInsertClearances(inspection_id=inspection_id)

        # Handle nested section data from frontend
        section_mappings = {
            'metalExposedInterior': 'metal_exposed_interior',
            'clearanceCombustibleFraming1': 'clearance_combustible_framing_1',
            'clearanceCombustibleFraming3': 'clearance_combustible_framing_3',
            'heatCirculatingDuctOutlets': 'heat_circulating_duct_outlets',
            'fireplaceInsertsApplianceStandard': 'fireplace_inserts_appliance_standard',
            'fireplaceInsertsInstallation': 'fireplace_inserts_installation'
        }

        for section_key, db_prefix in section_mappings.items():
            if section_key in data and isinstance(data[section_key], dict):
                section_data = data[section_key]
                setattr(clearances, f'{db_prefix}_condition', section_data.get('condition'))
                setattr(clearances, f'{db_prefix}_comments', section_data.get('comments'))
                setattr(clearances, f'{db_prefix}_code_compliance', section_data.get('codeCompliance'))
                setattr(clearances, f'{db_prefix}_photos', section_data.get('photos'))

        # Handle additional_notes
        if 'additional_notes' in data:
            clearances.additional_notes = data['additional_notes']

        db.session.add(clearances)
        db.session.commit()
        return jsonify(clearances.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/clearances/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_clearances(inspection_id):
    """Get fireplace insert clearances for an inspection"""
    try:
        clearances = FireplaceInsertClearances.query.filter_by(inspection_id=inspection_id).first()
        if not clearances:
            return jsonify({'error': 'Clearances not found'}), 404
        return jsonify(clearances.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/clearances/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_clearances(inspection_id):
    """Update fireplace insert clearances for an inspection"""
    data = request.get_json()
    try:
        clearances = FireplaceInsertClearances.query.filter_by(inspection_id=inspection_id).first()
        if not clearances:
            return jsonify({'error': 'Clearances not found'}), 404

        # Handle nested section data from frontend
        section_mappings = {
            'metalExposedInterior': 'metal_exposed_interior',
            'clearanceCombustibleFraming1': 'clearance_combustible_framing_1',
            'clearanceCombustibleFraming3': 'clearance_combustible_framing_3',
            'heatCirculatingDuctOutlets': 'heat_circulating_duct_outlets',
            'fireplaceInsertsApplianceStandard': 'fireplace_inserts_appliance_standard',
            'fireplaceInsertsInstallation': 'fireplace_inserts_installation'
        }

        for section_key, db_prefix in section_mappings.items():
            if section_key in data and isinstance(data[section_key], dict):
                section_data = data[section_key]
                setattr(clearances, f'{db_prefix}_condition', section_data.get('condition'))
                setattr(clearances, f'{db_prefix}_comments', section_data.get('comments'))
                setattr(clearances, f'{db_prefix}_code_compliance', section_data.get('codeCompliance'))
                setattr(clearances, f'{db_prefix}_photos', section_data.get('photos'))

        # Handle additional_notes
        if 'additional_notes' in data:
            clearances.additional_notes = data['additional_notes']

        db.session.commit()
        return jsonify(clearances.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Clearances & Liners Routes
@main.route('/api/fireplace-insert/clearances-liners', methods=['POST'])
def create_fireplace_insert_clearances_liners():
    """Create fireplace insert clearances & liners for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertClearancesLiners.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Clearances & liners already exists for this inspection'}), 400

        clearances_liners = FireplaceInsertClearancesLiners(inspection_id=inspection_id)

        # Map nested frontend data to flattened database fields
        if 'obcInstallation' in data:
            clearances_liners.obc_installation_condition = data['obcInstallation'].get('condition', '')
            clearances_liners.obc_installation_comments = data['obcInstallation'].get('comments', '')
            clearances_liners.obc_installation_code_compliance = data['obcInstallation'].get('codeCompliance')
            clearances_liners.obc_installation_photos = data['obcInstallation'].get('photos', [])

        if 'nfcClearances' in data:
            clearances_liners.nfc_clearances_condition = data['nfcClearances'].get('condition', '')
            clearances_liners.nfc_clearances_comments = data['nfcClearances'].get('comments', '')
            clearances_liners.nfc_clearances_code_compliance = data['nfcClearances'].get('codeCompliance')
            clearances_liners.nfc_clearances_photos = data['nfcClearances'].get('photos', [])

        if 'clearanceCombustibleMaterials' in data:
            clearances_liners.clearance_combustible_materials_condition = data['clearanceCombustibleMaterials'].get('condition', '')
            clearances_liners.clearance_combustible_materials_comments = data['clearanceCombustibleMaterials'].get('comments', '')
            clearances_liners.clearance_combustible_materials_code_compliance = data['clearanceCombustibleMaterials'].get('codeCompliance')
            clearances_liners.clearance_combustible_materials_photos = data['clearanceCombustibleMaterials'].get('photos', [])

        if 'wallThickness' in data:
            clearances_liners.wall_thickness_condition = data['wallThickness'].get('condition', '')
            clearances_liners.wall_thickness_comments = data['wallThickness'].get('comments', '')
            clearances_liners.wall_thickness_code_compliance = data['wallThickness'].get('codeCompliance')
            clearances_liners.wall_thickness_photos = data['wallThickness'].get('photos', [])

        if 'liningMaterials' in data:
            clearances_liners.lining_materials_condition = data['liningMaterials'].get('condition', '')
            clearances_liners.lining_materials_comments = data['liningMaterials'].get('comments', '')
            clearances_liners.lining_materials_code_compliance = data['liningMaterials'].get('codeCompliance')
            clearances_liners.lining_materials_photos = data['liningMaterials'].get('photos', [])

        if 'clayLiners' in data:
            clearances_liners.clay_liners_condition = data['clayLiners'].get('condition', '')
            clearances_liners.clay_liners_comments = data['clayLiners'].get('comments', '')
            clearances_liners.clay_liners_code_compliance = data['clayLiners'].get('codeCompliance')
            clearances_liners.clay_liners_photos = data['clayLiners'].get('photos', [])

        if 'additionalNotes' in data:
            clearances_liners.additional_notes = data['additionalNotes']

        db.session.add(clearances_liners)
        db.session.commit()
        return jsonify(clearances_liners.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/clearances-liners/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_clearances_liners(inspection_id):
    """Get fireplace insert clearances & liners for an inspection"""
    try:
        clearances_liners = FireplaceInsertClearancesLiners.query.filter_by(inspection_id=inspection_id).first()
        if not clearances_liners:
            return jsonify({'error': 'Clearances & liners not found'}), 404
        return jsonify(clearances_liners.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/clearances-liners/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_clearances_liners(inspection_id):
    """Update fireplace insert clearances & liners for an inspection"""
    data = request.get_json()
    try:
        clearances_liners = FireplaceInsertClearancesLiners.query.filter_by(inspection_id=inspection_id).first()
        if not clearances_liners:
            return jsonify({'error': 'Clearances & liners not found'}), 404

        # Map nested frontend data to flattened database fields
        if 'obcInstallation' in data:
            clearances_liners.obc_installation_condition = data['obcInstallation'].get('condition', '')
            clearances_liners.obc_installation_comments = data['obcInstallation'].get('comments', '')
            clearances_liners.obc_installation_code_compliance = data['obcInstallation'].get('codeCompliance')
            clearances_liners.obc_installation_photos = data['obcInstallation'].get('photos', [])

        if 'nfcClearances' in data:
            clearances_liners.nfc_clearances_condition = data['nfcClearances'].get('condition', '')
            clearances_liners.nfc_clearances_comments = data['nfcClearances'].get('comments', '')
            clearances_liners.nfc_clearances_code_compliance = data['nfcClearances'].get('codeCompliance')
            clearances_liners.nfc_clearances_photos = data['nfcClearances'].get('photos', [])

        if 'clearanceCombustibleMaterials' in data:
            clearances_liners.clearance_combustible_materials_condition = data['clearanceCombustibleMaterials'].get('condition', '')
            clearances_liners.clearance_combustible_materials_comments = data['clearanceCombustibleMaterials'].get('comments', '')
            clearances_liners.clearance_combustible_materials_code_compliance = data['clearanceCombustibleMaterials'].get('codeCompliance')
            clearances_liners.clearance_combustible_materials_photos = data['clearanceCombustibleMaterials'].get('photos', [])

        if 'wallThickness' in data:
            clearances_liners.wall_thickness_condition = data['wallThickness'].get('condition', '')
            clearances_liners.wall_thickness_comments = data['wallThickness'].get('comments', '')
            clearances_liners.wall_thickness_code_compliance = data['wallThickness'].get('codeCompliance')
            clearances_liners.wall_thickness_photos = data['wallThickness'].get('photos', [])

        if 'liningMaterials' in data:
            clearances_liners.lining_materials_condition = data['liningMaterials'].get('condition', '')
            clearances_liners.lining_materials_comments = data['liningMaterials'].get('comments', '')
            clearances_liners.lining_materials_code_compliance = data['liningMaterials'].get('codeCompliance')
            clearances_liners.lining_materials_photos = data['liningMaterials'].get('photos', [])

        if 'clayLiners' in data:
            clearances_liners.clay_liners_condition = data['clayLiners'].get('condition', '')
            clearances_liners.clay_liners_comments = data['clayLiners'].get('comments', '')
            clearances_liners.clay_liners_code_compliance = data['clayLiners'].get('codeCompliance')
            clearances_liners.clay_liners_photos = data['clayLiners'].get('photos', [])

        if 'additionalNotes' in data:
            clearances_liners.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(clearances_liners.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Liner Details Routes
@main.route('/api/fireplace-insert/liner-details', methods=['POST'])
def create_fireplace_insert_liner_details():
    """Create fireplace insert liner details for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertLinerDetails.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Liner details already exists for this inspection'}), 400

        liner_details = FireplaceInsertLinerDetails(inspection_id=inspection_id)

        # Map nested frontend data to flattened database fields
        if 'inclinedChimneyFlues' in data:
            liner_details.inclined_chimney_flues_condition = data['inclinedChimneyFlues'].get('condition', '')
            liner_details.inclined_chimney_flues_comments = data['inclinedChimneyFlues'].get('comments', '')
            liner_details.inclined_chimney_flues_code_compliance = data['inclinedChimneyFlues'].get('codeCompliance')
            liner_details.inclined_chimney_flues_photos = data['inclinedChimneyFlues'].get('photos', [])

        if 'firebrickLiners' in data:
            liner_details.firebrick_liners_condition = data['firebrickLiners'].get('condition', '')
            liner_details.firebrick_liners_comments = data['firebrickLiners'].get('comments', '')
            liner_details.firebrick_liners_code_compliance = data['firebrickLiners'].get('codeCompliance')
            liner_details.firebrick_liners_photos = data['firebrickLiners'].get('photos', [])

        if 'concreteLiners' in data:
            liner_details.concrete_liners_condition = data['concreteLiners'].get('condition', '')
            liner_details.concrete_liners_comments = data['concreteLiners'].get('comments', '')
            liner_details.concrete_liners_code_compliance = data['concreteLiners'].get('codeCompliance')
            liner_details.concrete_liners_photos = data['concreteLiners'].get('photos', [])

        if 'metalLiners' in data:
            liner_details.metal_liners_condition = data['metalLiners'].get('condition', '')
            liner_details.metal_liners_comments = data['metalLiners'].get('comments', '')
            liner_details.metal_liners_code_compliance = data['metalLiners'].get('codeCompliance')
            liner_details.metal_liners_photos = data['metalLiners'].get('photos', [])

        if 'ovalChimneyFlues' in data:
            liner_details.oval_chimney_flues_condition = data['ovalChimneyFlues'].get('condition', '')
            liner_details.oval_chimney_flues_comments = data['ovalChimneyFlues'].get('comments', '')
            liner_details.oval_chimney_flues_code_compliance = data['ovalChimneyFlues'].get('codeCompliance')
            liner_details.oval_chimney_flues_photos = data['ovalChimneyFlues'].get('photos', [])

        if 'separationOfFlueLiners' in data:
            liner_details.separation_of_flue_liners_condition = data['separationOfFlueLiners'].get('condition', '')
            liner_details.separation_of_flue_liners_comments = data['separationOfFlueLiners'].get('comments', '')
            liner_details.separation_of_flue_liners_code_compliance = data['separationOfFlueLiners'].get('codeCompliance')
            liner_details.separation_of_flue_liners_photos = data['separationOfFlueLiners'].get('photos', [])

        if 'additionalNotes' in data:
            liner_details.additional_notes = data['additionalNotes']

        db.session.add(liner_details)
        db.session.commit()
        return jsonify(liner_details.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/liner-details/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_liner_details(inspection_id):
    """Get fireplace insert liner details for an inspection"""
    try:
        liner_details = FireplaceInsertLinerDetails.query.filter_by(inspection_id=inspection_id).first()
        if not liner_details:
            return jsonify({'error': 'Liner details not found'}), 404
        return jsonify(liner_details.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/liner-details/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_liner_details(inspection_id):
    """Update fireplace insert liner details for an inspection"""
    data = request.get_json()
    try:
        liner_details = FireplaceInsertLinerDetails.query.filter_by(inspection_id=inspection_id).first()
        if not liner_details:
            return jsonify({'error': 'Liner details not found'}), 404

        # Map nested frontend data to flattened database fields
        if 'inclinedChimneyFlues' in data:
            liner_details.inclined_chimney_flues_condition = data['inclinedChimneyFlues'].get('condition', '')
            liner_details.inclined_chimney_flues_comments = data['inclinedChimneyFlues'].get('comments', '')
            liner_details.inclined_chimney_flues_code_compliance = data['inclinedChimneyFlues'].get('codeCompliance')
            liner_details.inclined_chimney_flues_photos = data['inclinedChimneyFlues'].get('photos', [])

        if 'firebrickLiners' in data:
            liner_details.firebrick_liners_condition = data['firebrickLiners'].get('condition', '')
            liner_details.firebrick_liners_comments = data['firebrickLiners'].get('comments', '')
            liner_details.firebrick_liners_code_compliance = data['firebrickLiners'].get('codeCompliance')
            liner_details.firebrick_liners_photos = data['firebrickLiners'].get('photos', [])

        if 'concreteLiners' in data:
            liner_details.concrete_liners_condition = data['concreteLiners'].get('condition', '')
            liner_details.concrete_liners_comments = data['concreteLiners'].get('comments', '')
            liner_details.concrete_liners_code_compliance = data['concreteLiners'].get('codeCompliance')
            liner_details.concrete_liners_photos = data['concreteLiners'].get('photos', [])

        if 'metalLiners' in data:
            liner_details.metal_liners_condition = data['metalLiners'].get('condition', '')
            liner_details.metal_liners_comments = data['metalLiners'].get('comments', '')
            liner_details.metal_liners_code_compliance = data['metalLiners'].get('codeCompliance')
            liner_details.metal_liners_photos = data['metalLiners'].get('photos', [])

        if 'ovalChimneyFlues' in data:
            liner_details.oval_chimney_flues_condition = data['ovalChimneyFlues'].get('condition', '')
            liner_details.oval_chimney_flues_comments = data['ovalChimneyFlues'].get('comments', '')
            liner_details.oval_chimney_flues_code_compliance = data['ovalChimneyFlues'].get('codeCompliance')
            liner_details.oval_chimney_flues_photos = data['ovalChimneyFlues'].get('photos', [])

        if 'separationOfFlueLiners' in data:
            liner_details.separation_of_flue_liners_condition = data['separationOfFlueLiners'].get('condition', '')
            liner_details.separation_of_flue_liners_comments = data['separationOfFlueLiners'].get('comments', '')
            liner_details.separation_of_flue_liners_code_compliance = data['separationOfFlueLiners'].get('codeCompliance')
            liner_details.separation_of_flue_liners_photos = data['separationOfFlueLiners'].get('photos', [])

        if 'additionalNotes' in data:
            liner_details.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(liner_details.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Joints Details Routes
@main.route('/api/fireplace-insert/joints-details', methods=['POST'])
def create_fireplace_insert_joints_details():
    """Create fireplace insert joints details for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertJointsDetails.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Joints details already exists for this inspection'}), 400

        joints_details = FireplaceInsertJointsDetails(inspection_id=inspection_id)

        # Map nested frontend data to flattened database fields
        if 'jointsSealing' in data:
            joints_details.joints_sealing_condition = data['jointsSealing'].get('condition', '')
            joints_details.joints_sealing_comments = data['jointsSealing'].get('comments', '')
            joints_details.joints_sealing_code_compliance = data['jointsSealing'].get('codeCompliance')
            joints_details.joints_sealing_photos = data['jointsSealing'].get('photos', [])

        if 'jointsFlush' in data:
            joints_details.joints_flush_condition = data['jointsFlush'].get('condition', '')
            joints_details.joints_flush_comments = data['jointsFlush'].get('comments', '')
            joints_details.joints_flush_code_compliance = data['jointsFlush'].get('codeCompliance')
            joints_details.joints_flush_photos = data['jointsFlush'].get('photos', [])

        if 'linerInstallation' in data:
            joints_details.liner_installation_condition = data['linerInstallation'].get('condition', '')
            joints_details.liner_installation_comments = data['linerInstallation'].get('comments', '')
            joints_details.liner_installation_code_compliance = data['linerInstallation'].get('codeCompliance')
            joints_details.liner_installation_photos = data['linerInstallation'].get('photos', [])

        if 'linerSpaces' in data:
            joints_details.liner_spaces_condition = data['linerSpaces'].get('condition', '')
            joints_details.liner_spaces_comments = data['linerSpaces'].get('comments', '')
            joints_details.liner_spaces_code_compliance = data['linerSpaces'].get('codeCompliance')
            joints_details.liner_spaces_photos = data['linerSpaces'].get('photos', [])

        if 'mortarForLiners' in data:
            joints_details.mortar_for_liners_condition = data['mortarForLiners'].get('condition', '')
            joints_details.mortar_for_liners_comments = data['mortarForLiners'].get('comments', '')
            joints_details.mortar_for_liners_code_compliance = data['mortarForLiners'].get('codeCompliance')
            joints_details.mortar_for_liners_photos = data['mortarForLiners'].get('photos', [])

        if 'linerExtension' in data:
            joints_details.liner_extension_condition = data['linerExtension'].get('condition', '')
            joints_details.liner_extension_comments = data['linerExtension'].get('comments', '')
            joints_details.liner_extension_code_compliance = data['linerExtension'].get('codeCompliance')
            joints_details.liner_extension_photos = data['linerExtension'].get('photos', [])

        if 'additionalNotes' in data:
            joints_details.additional_notes = data['additionalNotes']

        db.session.add(joints_details)
        db.session.commit()
        return jsonify(joints_details.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/joints-details/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_joints_details(inspection_id):
    """Get fireplace insert joints details for an inspection"""
    try:
        joints_details = FireplaceInsertJointsDetails.query.filter_by(inspection_id=inspection_id).first()
        if not joints_details:
            return jsonify({'error': 'Joints details not found'}), 404
        return jsonify(joints_details.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/joints-details/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_joints_details(inspection_id):
    """Update fireplace insert joints details for an inspection"""
    data = request.get_json()
    try:
        joints_details = FireplaceInsertJointsDetails.query.filter_by(inspection_id=inspection_id).first()
        if not joints_details:
            return jsonify({'error': 'Joints details not found'}), 404

        # Map nested frontend data to flattened database fields
        if 'jointsSealing' in data:
            joints_details.joints_sealing_condition = data['jointsSealing'].get('condition', '')
            joints_details.joints_sealing_comments = data['jointsSealing'].get('comments', '')
            joints_details.joints_sealing_code_compliance = data['jointsSealing'].get('codeCompliance')
            joints_details.joints_sealing_photos = data['jointsSealing'].get('photos', [])

        if 'jointsFlush' in data:
            joints_details.joints_flush_condition = data['jointsFlush'].get('condition', '')
            joints_details.joints_flush_comments = data['jointsFlush'].get('comments', '')
            joints_details.joints_flush_code_compliance = data['jointsFlush'].get('codeCompliance')
            joints_details.joints_flush_photos = data['jointsFlush'].get('photos', [])

        if 'linerInstallation' in data:
            joints_details.liner_installation_condition = data['linerInstallation'].get('condition', '')
            joints_details.liner_installation_comments = data['linerInstallation'].get('comments', '')
            joints_details.liner_installation_code_compliance = data['linerInstallation'].get('codeCompliance')
            joints_details.liner_installation_photos = data['linerInstallation'].get('photos', [])

        if 'linerSpaces' in data:
            joints_details.liner_spaces_condition = data['linerSpaces'].get('condition', '')
            joints_details.liner_spaces_comments = data['linerSpaces'].get('comments', '')
            joints_details.liner_spaces_code_compliance = data['linerSpaces'].get('codeCompliance')
            joints_details.liner_spaces_photos = data['linerSpaces'].get('photos', [])

        if 'mortarForLiners' in data:
            joints_details.mortar_for_liners_condition = data['mortarForLiners'].get('condition', '')
            joints_details.mortar_for_liners_comments = data['mortarForLiners'].get('comments', '')
            joints_details.mortar_for_liners_code_compliance = data['mortarForLiners'].get('codeCompliance')
            joints_details.mortar_for_liners_photos = data['mortarForLiners'].get('photos', [])

        if 'linerExtension' in data:
            joints_details.liner_extension_condition = data['linerExtension'].get('condition', '')
            joints_details.liner_extension_comments = data['linerExtension'].get('comments', '')
            joints_details.liner_extension_code_compliance = data['linerExtension'].get('codeCompliance')
            joints_details.liner_extension_photos = data['linerExtension'].get('photos', [])

        if 'additionalNotes' in data:
            joints_details.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(joints_details.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Chimney Height & Clearance Routes
@main.route('/api/fireplace-insert/chimney-height-clearance', methods=['POST'])
def create_fireplace_insert_chimney_height_clearance():
    """Create fireplace insert chimney height & clearance for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertChimneyHeightClearance.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Chimney height & clearance already exists for this inspection'}), 400

        chimney_height_clearance = FireplaceInsertChimneyHeightClearance(inspection_id=inspection_id)

        # Map nested frontend data to flattened database fields
        if 'chimneyFluesHeight' in data:
            chimney_height_clearance.chimney_flues_height_required_height = data['chimneyFluesHeight'].get('requiredHeight', '')
            chimney_height_clearance.chimney_flues_height_present_height = data['chimneyFluesHeight'].get('presentHeight', '')
            chimney_height_clearance.chimney_flues_height_required_width = data['chimneyFluesHeight'].get('requiredWidth', '')
            chimney_height_clearance.chimney_flues_height_present_width = data['chimneyFluesHeight'].get('presentWidth', '')
            chimney_height_clearance.chimney_flues_height_required_vertical = data['chimneyFluesHeight'].get('requiredVertical', '')
            chimney_height_clearance.chimney_flues_height_present_vertical = data['chimneyFluesHeight'].get('presentVertical', '')
            chimney_height_clearance.chimney_flues_height_condition = data['chimneyFluesHeight'].get('condition', '')
            chimney_height_clearance.chimney_flues_height_comments = data['chimneyFluesHeight'].get('comments', '')
            chimney_height_clearance.chimney_flues_height_code_compliance = data['chimneyFluesHeight'].get('codeCompliance')
            chimney_height_clearance.chimney_flues_height_photos = data['chimneyFluesHeight'].get('photos', [])

        if 'lateralStability' in data:
            chimney_height_clearance.lateral_stability_condition = data['lateralStability'].get('condition', '')
            chimney_height_clearance.lateral_stability_comments = data['lateralStability'].get('comments', '')
            chimney_height_clearance.lateral_stability_code_compliance = data['lateralStability'].get('codeCompliance')
            chimney_height_clearance.lateral_stability_photos = data['lateralStability'].get('photos', [])

        if 'chimneyCaps1' in data:
            chimney_height_clearance.chimney_caps_1_condition = data['chimneyCaps1'].get('condition', '')
            chimney_height_clearance.chimney_caps_1_comments = data['chimneyCaps1'].get('comments', '')
            chimney_height_clearance.chimney_caps_1_code_compliance = data['chimneyCaps1'].get('codeCompliance')
            chimney_height_clearance.chimney_caps_1_photos = data['chimneyCaps1'].get('photos', [])

        if 'chimneyCaps2' in data:
            chimney_height_clearance.chimney_caps_2_condition = data['chimneyCaps2'].get('condition', '')
            chimney_height_clearance.chimney_caps_2_comments = data['chimneyCaps2'].get('comments', '')
            chimney_height_clearance.chimney_caps_2_code_compliance = data['chimneyCaps2'].get('codeCompliance')
            chimney_height_clearance.chimney_caps_2_photos = data['chimneyCaps2'].get('photos', [])

        if 'chimneyCaps3' in data:
            chimney_height_clearance.chimney_caps_3_condition = data['chimneyCaps3'].get('condition', '')
            chimney_height_clearance.chimney_caps_3_comments = data['chimneyCaps3'].get('comments', '')
            chimney_height_clearance.chimney_caps_3_code_compliance = data['chimneyCaps3'].get('codeCompliance')
            chimney_height_clearance.chimney_caps_3_photos = data['chimneyCaps3'].get('photos', [])

        if 'additionalNotes' in data:
            chimney_height_clearance.additional_notes = data['additionalNotes']

        db.session.add(chimney_height_clearance)
        db.session.commit()
        return jsonify(chimney_height_clearance.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-height-clearance/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_chimney_height_clearance(inspection_id):
    """Get fireplace insert chimney height & clearance for an inspection"""
    try:
        chimney_height_clearance = FireplaceInsertChimneyHeightClearance.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_height_clearance:
            return jsonify({'error': 'Chimney height & clearance not found'}), 404
        return jsonify(chimney_height_clearance.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-height-clearance/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_chimney_height_clearance(inspection_id):
    """Update fireplace insert chimney height & clearance for an inspection"""
    data = request.get_json()
    try:
        chimney_height_clearance = FireplaceInsertChimneyHeightClearance.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_height_clearance:
            return jsonify({'error': 'Chimney height & clearance not found'}), 404

        # Map nested frontend data to flattened database fields
        if 'chimneyFluesHeight' in data:
            chimney_height_clearance.chimney_flues_height_required_height = data['chimneyFluesHeight'].get('requiredHeight', '')
            chimney_height_clearance.chimney_flues_height_present_height = data['chimneyFluesHeight'].get('presentHeight', '')
            chimney_height_clearance.chimney_flues_height_required_width = data['chimneyFluesHeight'].get('requiredWidth', '')
            chimney_height_clearance.chimney_flues_height_present_width = data['chimneyFluesHeight'].get('presentWidth', '')
            chimney_height_clearance.chimney_flues_height_required_vertical = data['chimneyFluesHeight'].get('requiredVertical', '')
            chimney_height_clearance.chimney_flues_height_present_vertical = data['chimneyFluesHeight'].get('presentVertical', '')
            chimney_height_clearance.chimney_flues_height_condition = data['chimneyFluesHeight'].get('condition', '')
            chimney_height_clearance.chimney_flues_height_comments = data['chimneyFluesHeight'].get('comments', '')
            chimney_height_clearance.chimney_flues_height_code_compliance = data['chimneyFluesHeight'].get('codeCompliance')
            chimney_height_clearance.chimney_flues_height_photos = data['chimneyFluesHeight'].get('photos', [])

        if 'lateralStability' in data:
            chimney_height_clearance.lateral_stability_condition = data['lateralStability'].get('condition', '')
            chimney_height_clearance.lateral_stability_comments = data['lateralStability'].get('comments', '')
            chimney_height_clearance.lateral_stability_code_compliance = data['lateralStability'].get('codeCompliance')
            chimney_height_clearance.lateral_stability_photos = data['lateralStability'].get('photos', [])

        if 'chimneyCaps1' in data:
            chimney_height_clearance.chimney_caps_1_condition = data['chimneyCaps1'].get('condition', '')
            chimney_height_clearance.chimney_caps_1_comments = data['chimneyCaps1'].get('comments', '')
            chimney_height_clearance.chimney_caps_1_code_compliance = data['chimneyCaps1'].get('codeCompliance')
            chimney_height_clearance.chimney_caps_1_photos = data['chimneyCaps1'].get('photos', [])

        if 'chimneyCaps2' in data:
            chimney_height_clearance.chimney_caps_2_condition = data['chimneyCaps2'].get('condition', '')
            chimney_height_clearance.chimney_caps_2_comments = data['chimneyCaps2'].get('comments', '')
            chimney_height_clearance.chimney_caps_2_code_compliance = data['chimneyCaps2'].get('codeCompliance')
            chimney_height_clearance.chimney_caps_2_photos = data['chimneyCaps2'].get('photos', [])

        if 'chimneyCaps3' in data:
            chimney_height_clearance.chimney_caps_3_condition = data['chimneyCaps3'].get('condition', '')
            chimney_height_clearance.chimney_caps_3_comments = data['chimneyCaps3'].get('comments', '')
            chimney_height_clearance.chimney_caps_3_code_compliance = data['chimneyCaps3'].get('codeCompliance')
            chimney_height_clearance.chimney_caps_3_photos = data['chimneyCaps3'].get('photos', [])

        if 'additionalNotes' in data:
            chimney_height_clearance.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(chimney_height_clearance.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Chimney Supports Routes
@main.route('/api/fireplace-insert/chimney-supports', methods=['POST'])
def create_fireplace_insert_chimney_supports():
    """Create fireplace insert chimney supports for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertChimneySupports.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Chimney supports already exists for this inspection'}), 400

        chimney_supports = FireplaceInsertChimneySupports(inspection_id=inspection_id)

        # Map nested frontend data to flattened database fields
        if 'flashing' in data:
            chimney_supports.flashing_condition = data['flashing'].get('condition', '')
            chimney_supports.flashing_comments = data['flashing'].get('comments', '')
            chimney_supports.flashing_code_compliance = data['flashing'].get('codeCompliance')
            chimney_supports.flashing_photos = data['flashing'].get('photos', [])

        if 'clearanceCombustible1' in data:
            chimney_supports.clearance_combustible_1_condition = data['clearanceCombustible1'].get('condition', '')
            chimney_supports.clearance_combustible_1_comments = data['clearanceCombustible1'].get('comments', '')
            chimney_supports.clearance_combustible_1_code_compliance = data['clearanceCombustible1'].get('codeCompliance')
            chimney_supports.clearance_combustible_1_photos = data['clearanceCombustible1'].get('photos', [])

        if 'clearanceCombustible3' in data:
            chimney_supports.clearance_combustible_3_condition = data['clearanceCombustible3'].get('condition', '')
            chimney_supports.clearance_combustible_3_comments = data['clearanceCombustible3'].get('comments', '')
            chimney_supports.clearance_combustible_3_code_compliance = data['clearanceCombustible3'].get('codeCompliance')
            chimney_supports.clearance_combustible_3_photos = data['clearanceCombustible3'].get('photos', [])

        if 'sealingSpaces' in data:
            chimney_supports.sealing_spaces_condition = data['sealingSpaces'].get('condition', '')
            chimney_supports.sealing_spaces_comments = data['sealingSpaces'].get('comments', '')
            chimney_supports.sealing_spaces_code_compliance = data['sealingSpaces'].get('codeCompliance')
            chimney_supports.sealing_spaces_photos = data['sealingSpaces'].get('photos', [])

        if 'supportJoistsBeams' in data:
            chimney_supports.support_joists_beams_condition = data['supportJoistsBeams'].get('condition', '')
            chimney_supports.support_joists_beams_comments = data['supportJoistsBeams'].get('comments', '')
            chimney_supports.support_joists_beams_code_compliance = data['supportJoistsBeams'].get('codeCompliance')
            chimney_supports.support_joists_beams_photos = data['supportJoistsBeams'].get('photos', [])

        if 'roofMasonryIntersection' in data:
            chimney_supports.roof_masonry_intersection_condition = data['roofMasonryIntersection'].get('condition', '')
            chimney_supports.roof_masonry_intersection_comments = data['roofMasonryIntersection'].get('comments', '')
            chimney_supports.roof_masonry_intersection_code_compliance = data['roofMasonryIntersection'].get('codeCompliance')
            chimney_supports.roof_masonry_intersection_photos = data['roofMasonryIntersection'].get('photos', [])

        if 'additionalNotes' in data:
            chimney_supports.additional_notes = data['additionalNotes']

        db.session.add(chimney_supports)
        db.session.commit()
        return jsonify(chimney_supports.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-supports/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_chimney_supports(inspection_id):
    """Get fireplace insert chimney supports for an inspection"""
    try:
        chimney_supports = FireplaceInsertChimneySupports.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_supports:
            return jsonify({'error': 'Chimney supports not found'}), 404
        return jsonify(chimney_supports.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-supports/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_chimney_supports(inspection_id):
    """Update fireplace insert chimney supports for an inspection"""
    data = request.get_json()
    try:
        chimney_supports = FireplaceInsertChimneySupports.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_supports:
            return jsonify({'error': 'Chimney supports not found'}), 404

        # Map nested frontend data to flattened database fields
        if 'flashing' in data:
            chimney_supports.flashing_condition = data['flashing'].get('condition', '')
            chimney_supports.flashing_comments = data['flashing'].get('comments', '')
            chimney_supports.flashing_code_compliance = data['flashing'].get('codeCompliance')
            chimney_supports.flashing_photos = data['flashing'].get('photos', [])

        if 'clearanceCombustible1' in data:
            chimney_supports.clearance_combustible_1_condition = data['clearanceCombustible1'].get('condition', '')
            chimney_supports.clearance_combustible_1_comments = data['clearanceCombustible1'].get('comments', '')
            chimney_supports.clearance_combustible_1_code_compliance = data['clearanceCombustible1'].get('codeCompliance')
            chimney_supports.clearance_combustible_1_photos = data['clearanceCombustible1'].get('photos', [])

        if 'clearanceCombustible3' in data:
            chimney_supports.clearance_combustible_3_condition = data['clearanceCombustible3'].get('condition', '')
            chimney_supports.clearance_combustible_3_comments = data['clearanceCombustible3'].get('comments', '')
            chimney_supports.clearance_combustible_3_code_compliance = data['clearanceCombustible3'].get('codeCompliance')
            chimney_supports.clearance_combustible_3_photos = data['clearanceCombustible3'].get('photos', [])

        if 'sealingSpaces' in data:
            chimney_supports.sealing_spaces_condition = data['sealingSpaces'].get('condition', '')
            chimney_supports.sealing_spaces_comments = data['sealingSpaces'].get('comments', '')
            chimney_supports.sealing_spaces_code_compliance = data['sealingSpaces'].get('codeCompliance')
            chimney_supports.sealing_spaces_photos = data['sealingSpaces'].get('photos', [])

        if 'supportJoistsBeams' in data:
            chimney_supports.support_joists_beams_condition = data['supportJoistsBeams'].get('condition', '')
            chimney_supports.support_joists_beams_comments = data['supportJoistsBeams'].get('comments', '')
            chimney_supports.support_joists_beams_code_compliance = data['supportJoistsBeams'].get('codeCompliance')
            chimney_supports.support_joists_beams_photos = data['supportJoistsBeams'].get('photos', [])

        if 'roofMasonryIntersection' in data:
            chimney_supports.roof_masonry_intersection_condition = data['roofMasonryIntersection'].get('condition', '')
            chimney_supports.roof_masonry_intersection_comments = data['roofMasonryIntersection'].get('comments', '')
            chimney_supports.roof_masonry_intersection_code_compliance = data['roofMasonryIntersection'].get('codeCompliance')
            chimney_supports.roof_masonry_intersection_photos = data['roofMasonryIntersection'].get('photos', [])

        if 'additionalNotes' in data:
            chimney_supports.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(chimney_supports.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Fireplace Insert Chimney Saddles & Fire Code Routes
@main.route('/api/fireplace-insert/chimney-saddles-fire-code', methods=['POST'])
def create_fireplace_insert_chimney_saddles_fire_code():
    """Create fireplace insert chimney saddles & fire code for an inspection"""
    data = request.get_json()
    try:
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        existing = FireplaceInsertChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Chimney saddles & fire code already exists for this inspection'}), 400

        chimney_saddles_fire_code = FireplaceInsertChimneySaddlesFireCode(inspection_id=inspection_id)

        # Map nested frontend data to flattened database fields
        if 'chimneySaddles' in data:
            chimney_saddles_fire_code.chimney_saddles_condition = data['chimneySaddles'].get('condition', '')
            chimney_saddles_fire_code.chimney_saddles_comments = data['chimneySaddles'].get('comments', '')
            chimney_saddles_fire_code.chimney_saddles_code_compliance = data['chimneySaddles'].get('codeCompliance')
            chimney_saddles_fire_code.chimney_saddles_photos = data['chimneySaddles'].get('photos', [])

        if 'fireCodeInspection' in data:
            chimney_saddles_fire_code.fire_code_inspection_condition = data['fireCodeInspection'].get('condition', '')
            chimney_saddles_fire_code.fire_code_inspection_comments = data['fireCodeInspection'].get('comments', '')
            chimney_saddles_fire_code.fire_code_inspection_code_compliance = data['fireCodeInspection'].get('codeCompliance')
            chimney_saddles_fire_code.fire_code_inspection_photos = data['fireCodeInspection'].get('photos', [])

        if 'fireCodeCleaning' in data:
            chimney_saddles_fire_code.fire_code_cleaning_condition = data['fireCodeCleaning'].get('condition', '')
            chimney_saddles_fire_code.fire_code_cleaning_comments = data['fireCodeCleaning'].get('comments', '')
            chimney_saddles_fire_code.fire_code_cleaning_code_compliance = data['fireCodeCleaning'].get('codeCompliance')
            chimney_saddles_fire_code.fire_code_cleaning_photos = data['fireCodeCleaning'].get('photos', [])

        if 'fireCodeStructuralDeficiency' in data:
            chimney_saddles_fire_code.fire_code_structural_deficiency_condition = data['fireCodeStructuralDeficiency'].get('condition', '')
            chimney_saddles_fire_code.fire_code_structural_deficiency_comments = data['fireCodeStructuralDeficiency'].get('comments', '')
            chimney_saddles_fire_code.fire_code_structural_deficiency_code_compliance = data['fireCodeStructuralDeficiency'].get('codeCompliance')
            chimney_saddles_fire_code.fire_code_structural_deficiency_photos = data['fireCodeStructuralDeficiency'].get('photos', [])

        if 'fireCodeAbandonedOpenings' in data:
            chimney_saddles_fire_code.fire_code_abandoned_openings_condition = data['fireCodeAbandonedOpenings'].get('condition', '')
            chimney_saddles_fire_code.fire_code_abandoned_openings_comments = data['fireCodeAbandonedOpenings'].get('comments', '')
            chimney_saddles_fire_code.fire_code_abandoned_openings_code_compliance = data['fireCodeAbandonedOpenings'].get('codeCompliance')
            chimney_saddles_fire_code.fire_code_abandoned_openings_photos = data['fireCodeAbandonedOpenings'].get('photos', [])

        if 'additionalNotes' in data:
            chimney_saddles_fire_code.additional_notes = data['additionalNotes']

        db.session.add(chimney_saddles_fire_code)
        db.session.commit()
        return jsonify(chimney_saddles_fire_code.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-saddles-fire-code/<int:inspection_id>', methods=['GET'])
def get_fireplace_insert_chimney_saddles_fire_code(inspection_id):
    """Get fireplace insert chimney saddles & fire code for an inspection"""
    try:
        chimney_saddles_fire_code = FireplaceInsertChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_saddles_fire_code:
            return jsonify({'error': 'Chimney saddles & fire code not found'}), 404
        return jsonify(chimney_saddles_fire_code.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/fireplace-insert/chimney-saddles-fire-code/<int:inspection_id>', methods=['PUT'])
def update_fireplace_insert_chimney_saddles_fire_code(inspection_id):
    """Update fireplace insert chimney saddles & fire code for an inspection"""
    data = request.get_json()
    try:
        chimney_saddles_fire_code = FireplaceInsertChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()
        if not chimney_saddles_fire_code:
            return jsonify({'error': 'Chimney saddles & fire code not found'}), 404

        # Map nested frontend data to flattened database fields
        if 'chimneySaddles' in data:
            chimney_saddles_fire_code.chimney_saddles_condition = data['chimneySaddles'].get('condition', '')
            chimney_saddles_fire_code.chimney_saddles_comments = data['chimneySaddles'].get('comments', '')
            chimney_saddles_fire_code.chimney_saddles_code_compliance = data['chimneySaddles'].get('codeCompliance')
            chimney_saddles_fire_code.chimney_saddles_photos = data['chimneySaddles'].get('photos', [])

        if 'fireCodeInspection' in data:
            chimney_saddles_fire_code.fire_code_inspection_condition = data['fireCodeInspection'].get('condition', '')
            chimney_saddles_fire_code.fire_code_inspection_comments = data['fireCodeInspection'].get('comments', '')
            chimney_saddles_fire_code.fire_code_inspection_code_compliance = data['fireCodeInspection'].get('codeCompliance')
            chimney_saddles_fire_code.fire_code_inspection_photos = data['fireCodeInspection'].get('photos', [])

        if 'fireCodeCleaning' in data:
            chimney_saddles_fire_code.fire_code_cleaning_condition = data['fireCodeCleaning'].get('condition', '')
            chimney_saddles_fire_code.fire_code_cleaning_comments = data['fireCodeCleaning'].get('comments', '')
            chimney_saddles_fire_code.fire_code_cleaning_code_compliance = data['fireCodeCleaning'].get('codeCompliance')
            chimney_saddles_fire_code.fire_code_cleaning_photos = data['fireCodeCleaning'].get('photos', [])

        if 'fireCodeStructuralDeficiency' in data:
            chimney_saddles_fire_code.fire_code_structural_deficiency_condition = data['fireCodeStructuralDeficiency'].get('condition', '')
            chimney_saddles_fire_code.fire_code_structural_deficiency_comments = data['fireCodeStructuralDeficiency'].get('comments', '')
            chimney_saddles_fire_code.fire_code_structural_deficiency_code_compliance = data['fireCodeStructuralDeficiency'].get('codeCompliance')
            chimney_saddles_fire_code.fire_code_structural_deficiency_photos = data['fireCodeStructuralDeficiency'].get('photos', [])

        if 'fireCodeAbandonedOpenings' in data:
            chimney_saddles_fire_code.fire_code_abandoned_openings_condition = data['fireCodeAbandonedOpenings'].get('condition', '')
            chimney_saddles_fire_code.fire_code_abandoned_openings_comments = data['fireCodeAbandonedOpenings'].get('comments', '')
            chimney_saddles_fire_code.fire_code_abandoned_openings_code_compliance = data['fireCodeAbandonedOpenings'].get('codeCompliance')
            chimney_saddles_fire_code.fire_code_abandoned_openings_photos = data['fireCodeAbandonedOpenings'].get('photos', [])

        if 'additionalNotes' in data:
            chimney_saddles_fire_code.additional_notes = data['additionalNotes']

        db.session.commit()
        return jsonify(chimney_saddles_fire_code.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Chimney Liners routes
@main.route('/api/pellet-insert/chimney-liners', methods=['POST'])
def create_pellet_insert_chimney_liners():
    """Create pellet insert chimney liners for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert chimney liners already exist
        existing_liners = PelletInsertChimneyLiners.query.filter_by(inspection_id=inspection_id).first()
        if existing_liners:
            return jsonify({'error': 'Pellet insert chimney liners already exist for this inspection'}), 400

        # Create new pellet insert chimney liners
        liners = PelletInsertChimneyLiners(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'liningMaterials' in form_data:
            section = form_data['liningMaterials']
            liners.lining_materials_condition = section.get('condition', '')
            liners.lining_materials_comments = section.get('comments', '')
            liners.lining_materials_code_compliance = section.get('codeCompliance')
            liners.lining_materials_photos = section.get('photos', [])

        if 'clayLiners' in form_data:
            section = form_data['clayLiners']
            liners.clay_liners_condition = section.get('condition', '')
            liners.clay_liners_comments = section.get('comments', '')
            liners.clay_liners_code_compliance = section.get('codeCompliance')
            liners.clay_liners_photos = section.get('photos', [])

        if 'inclinedChimneyFlues' in form_data:
            section = form_data['inclinedChimneyFlues']
            liners.inclined_chimney_flues_condition = section.get('condition', '')
            liners.inclined_chimney_flues_comments = section.get('comments', '')
            liners.inclined_chimney_flues_code_compliance = section.get('codeCompliance')
            liners.inclined_chimney_flues_photos = section.get('photos', [])

        if 'firebrickLiners' in form_data:
            section = form_data['firebrickLiners']
            liners.firebrick_liners_condition = section.get('condition', '')
            liners.firebrick_liners_comments = section.get('comments', '')
            liners.firebrick_liners_code_compliance = section.get('codeCompliance')
            liners.firebrick_liners_photos = section.get('photos', [])

        if 'concreteLiners' in form_data:
            section = form_data['concreteLiners']
            liners.concrete_liners_condition = section.get('condition', '')
            liners.concrete_liners_comments = section.get('comments', '')
            liners.concrete_liners_code_compliance = section.get('codeCompliance')
            liners.concrete_liners_photos = section.get('photos', [])

        if 'metalLiners' in form_data:
            section = form_data['metalLiners']
            liners.metal_liners_condition = section.get('condition', '')
            liners.metal_liners_comments = section.get('comments', '')
            liners.metal_liners_code_compliance = section.get('codeCompliance')
            liners.metal_liners_photos = section.get('photos', [])

        if 'ovalChimneyFlues' in form_data:
            section = form_data['ovalChimneyFlues']
            liners.oval_chimney_flues_condition = section.get('condition', '')
            liners.oval_chimney_flues_comments = section.get('comments', '')
            liners.oval_chimney_flues_code_compliance = section.get('codeCompliance')
            liners.oval_chimney_flues_photos = section.get('photos', [])

        if 'separationOfFlueLiners' in form_data:
            section = form_data['separationOfFlueLiners']
            liners.separation_of_flue_liners_condition = section.get('condition', '')
            liners.separation_of_flue_liners_comments = section.get('comments', '')
            liners.separation_of_flue_liners_code_compliance = section.get('codeCompliance')
            liners.separation_of_flue_liners_photos = section.get('photos', [])

        db.session.add(liners)
        db.session.commit()
        return jsonify(liners.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-liners/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_chimney_liners(inspection_id):
    """Get pellet insert chimney liners for an inspection."""
    try:
        liners = PelletInsertChimneyLiners.query.filter_by(inspection_id=inspection_id).first()

        if not liners:
            return jsonify({'error': 'Pellet insert chimney liners not found'}), 404

        return jsonify(liners.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-liners/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_chimney_liners(inspection_id):
    """Update pellet insert chimney liners for an inspection."""
    try:
        data = request.get_json()

        liners = PelletInsertChimneyLiners.query.filter_by(inspection_id=inspection_id).first()

        if not liners:
            return jsonify({'error': 'Pellet insert chimney liners not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'liningMaterials' in form_data:
            section = form_data['liningMaterials']
            liners.lining_materials_condition = section.get('condition', '')
            liners.lining_materials_comments = section.get('comments', '')
            liners.lining_materials_code_compliance = section.get('codeCompliance')
            liners.lining_materials_photos = section.get('photos', [])

        if 'clayLiners' in form_data:
            section = form_data['clayLiners']
            liners.clay_liners_condition = section.get('condition', '')
            liners.clay_liners_comments = section.get('comments', '')
            liners.clay_liners_code_compliance = section.get('codeCompliance')
            liners.clay_liners_photos = section.get('photos', [])

        if 'inclinedChimneyFlues' in form_data:
            section = form_data['inclinedChimneyFlues']
            liners.inclined_chimney_flues_condition = section.get('condition', '')
            liners.inclined_chimney_flues_comments = section.get('comments', '')
            liners.inclined_chimney_flues_code_compliance = section.get('codeCompliance')
            liners.inclined_chimney_flues_photos = section.get('photos', [])

        if 'firebrickLiners' in form_data:
            section = form_data['firebrickLiners']
            liners.firebrick_liners_condition = section.get('condition', '')
            liners.firebrick_liners_comments = section.get('comments', '')
            liners.firebrick_liners_code_compliance = section.get('codeCompliance')
            liners.firebrick_liners_photos = section.get('photos', [])

        if 'concreteLiners' in form_data:
            section = form_data['concreteLiners']
            liners.concrete_liners_condition = section.get('condition', '')
            liners.concrete_liners_comments = section.get('comments', '')
            liners.concrete_liners_code_compliance = section.get('codeCompliance')
            liners.concrete_liners_photos = section.get('photos', [])

        if 'metalLiners' in form_data:
            section = form_data['metalLiners']
            liners.metal_liners_condition = section.get('condition', '')
            liners.metal_liners_comments = section.get('comments', '')
            liners.metal_liners_code_compliance = section.get('codeCompliance')
            liners.metal_liners_photos = section.get('photos', [])

        if 'ovalChimneyFlues' in form_data:
            section = form_data['ovalChimneyFlues']
            liners.oval_chimney_flues_condition = section.get('condition', '')
            liners.oval_chimney_flues_comments = section.get('comments', '')
            liners.oval_chimney_flues_code_compliance = section.get('codeCompliance')
            liners.oval_chimney_flues_photos = section.get('photos', [])

        if 'separationOfFlueLiners' in form_data:
            section = form_data['separationOfFlueLiners']
            liners.separation_of_flue_liners_condition = section.get('condition', '')
            liners.separation_of_flue_liners_comments = section.get('comments', '')
            liners.separation_of_flue_liners_code_compliance = section.get('codeCompliance')
            liners.separation_of_flue_liners_photos = section.get('photos', [])

        db.session.commit()
        return jsonify(liners.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-liners/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_chimney_liners(inspection_id):
    """Delete pellet insert chimney liners for an inspection."""
    try:
        liners = PelletInsertChimneyLiners.query.filter_by(inspection_id=inspection_id).first()

        if not liners:
            return jsonify({'error': 'Pellet insert chimney liners not found'}), 404

        db.session.delete(liners)
        db.session.commit()
        return jsonify({'message': 'Pellet insert chimney liners deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Chimney Saddles Fire Code routes
@main.route('/api/pellet-insert/chimney-saddles-fire-code', methods=['POST'])
def create_pellet_insert_chimney_saddles_fire_code():
    """Create pellet insert chimney saddles fire code for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert chimney saddles fire code already exist
        existing_saddles = PelletInsertChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()
        if existing_saddles:
            return jsonify({'error': 'Pellet insert chimney saddles fire code already exist for this inspection'}), 400

        # Create new pellet insert chimney saddles fire code
        saddles = PelletInsertChimneySaddlesFireCode(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'chimneySaddles' in form_data:
            section = form_data['chimneySaddles']
            saddles.chimney_saddles_condition = section.get('condition', '')
            saddles.chimney_saddles_comments = section.get('comments', '')
            saddles.chimney_saddles_code_compliance = section.get('codeCompliance')
            saddles.chimney_saddles_photos = section.get('photos', [])

        if 'fireCode1' in form_data:
            section = form_data['fireCode1']
            saddles.fire_code_1_condition = section.get('condition', '')
            saddles.fire_code_1_comments = section.get('comments', '')
            saddles.fire_code_1_code_compliance = section.get('codeCompliance')
            saddles.fire_code_1_photos = section.get('photos', [])

        if 'fireCode2' in form_data:
            section = form_data['fireCode2']
            saddles.fire_code_2_condition = section.get('condition', '')
            saddles.fire_code_2_comments = section.get('comments', '')
            saddles.fire_code_2_code_compliance = section.get('codeCompliance')
            saddles.fire_code_2_photos = section.get('photos', [])

        if 'fireCode3' in form_data:
            section = form_data['fireCode3']
            saddles.fire_code_3_condition = section.get('condition', '')
            saddles.fire_code_3_comments = section.get('comments', '')
            saddles.fire_code_3_code_compliance = section.get('codeCompliance')
            saddles.fire_code_3_photos = section.get('photos', [])

        if 'fireCode4' in form_data:
            section = form_data['fireCode4']
            saddles.fire_code_4_condition = section.get('condition', '')
            saddles.fire_code_4_comments = section.get('comments', '')
            saddles.fire_code_4_code_compliance = section.get('codeCompliance')
            saddles.fire_code_4_photos = section.get('photos', [])

        if 'fireCode5' in form_data:
            section = form_data['fireCode5']
            saddles.fire_code_5_condition = section.get('condition', '')
            saddles.fire_code_5_comments = section.get('comments', '')
            saddles.fire_code_5_code_compliance = section.get('codeCompliance')
            saddles.fire_code_5_photos = section.get('photos', [])

        db.session.add(saddles)
        db.session.commit()
        return jsonify(saddles.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-saddles-fire-code/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_chimney_saddles_fire_code(inspection_id):
    """Get pellet insert chimney saddles fire code for an inspection."""
    try:
        saddles = PelletInsertChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()

        if not saddles:
            return jsonify({'error': 'Pellet insert chimney saddles fire code not found'}), 404

        return jsonify(saddles.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-saddles-fire-code/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_chimney_saddles_fire_code(inspection_id):
    """Update pellet insert chimney saddles fire code for an inspection."""
    try:
        data = request.get_json()

        saddles = PelletInsertChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()

        if not saddles:
            return jsonify({'error': 'Pellet insert chimney saddles fire code not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'chimneySaddles' in form_data:
            section = form_data['chimneySaddles']
            saddles.chimney_saddles_condition = section.get('condition', '')
            saddles.chimney_saddles_comments = section.get('comments', '')
            saddles.chimney_saddles_code_compliance = section.get('codeCompliance')
            saddles.chimney_saddles_photos = section.get('photos', [])

        if 'fireCode1' in form_data:
            section = form_data['fireCode1']
            saddles.fire_code_1_condition = section.get('condition', '')
            saddles.fire_code_1_comments = section.get('comments', '')
            saddles.fire_code_1_code_compliance = section.get('codeCompliance')
            saddles.fire_code_1_photos = section.get('photos', [])

        if 'fireCode2' in form_data:
            section = form_data['fireCode2']
            saddles.fire_code_2_condition = section.get('condition', '')
            saddles.fire_code_2_comments = section.get('comments', '')
            saddles.fire_code_2_code_compliance = section.get('codeCompliance')
            saddles.fire_code_2_photos = section.get('photos', [])

        if 'fireCode3' in form_data:
            section = form_data['fireCode3']
            saddles.fire_code_3_condition = section.get('condition', '')
            saddles.fire_code_3_comments = section.get('comments', '')
            saddles.fire_code_3_code_compliance = section.get('codeCompliance')
            saddles.fire_code_3_photos = section.get('photos', [])

        if 'fireCode4' in form_data:
            section = form_data['fireCode4']
            saddles.fire_code_4_condition = section.get('condition', '')
            saddles.fire_code_4_comments = section.get('comments', '')
            saddles.fire_code_4_code_compliance = section.get('codeCompliance')
            saddles.fire_code_4_photos = section.get('photos', [])

        if 'fireCode5' in form_data:
            section = form_data['fireCode5']
            saddles.fire_code_5_condition = section.get('condition', '')
            saddles.fire_code_5_comments = section.get('comments', '')
            saddles.fire_code_5_code_compliance = section.get('codeCompliance')
            saddles.fire_code_5_photos = section.get('photos', [])

        db.session.commit()
        return jsonify(saddles.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-saddles-fire-code/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_chimney_saddles_fire_code(inspection_id):
    """Delete pellet insert chimney saddles fire code for an inspection."""
    try:
        saddles = PelletInsertChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()

        if not saddles:
            return jsonify({'error': 'Pellet insert chimney saddles fire code not found'}), 404

        db.session.delete(saddles)
        db.session.commit()
        return jsonify({'message': 'Pellet insert chimney saddles fire code deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Chimney Specification routes
@main.route('/api/pellet-insert/chimney-specification', methods=['POST'])
def create_pellet_insert_chimney_specification():
    """Create pellet insert chimney specification for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert chimney specification already exists
        existing_spec = PelletInsertChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Pellet insert chimney specification already exists for this inspection'}), 400

        # Create new pellet insert chimney specification
        spec = PelletInsertChimneySpecification(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Inspection details
        spec.inspection_discussed = form_data.get('inspectionDiscussed')
        spec.building_permits_available = form_data.get('buildingPermitsAvailable')
        spec.time_of_day = form_data.get('timeOfDay')
        spec.weather_conditions = form_data.get('weatherConditions')
        spec.roofing_type_material = form_data.get('roofingTypeMaterial')
        spec.roof_accessed = form_data.get('roofAccessed')
        spec.attic_accessed = form_data.get('atticAccessed')

        # Construction details
        spec.chimney_constructed_with_building = form_data.get('chimneyConstructedWithBuilding')
        spec.approximate_age = form_data.get('approximateAge')
        spec.chimney_shell = form_data.get('chimneyShell')
        spec.rain_cap = form_data.get('rainCap')
        spec.chimney_location = form_data.get('chimneyLocation')
        spec.height_from_firebox_floor = form_data.get('heightFromFireboxFloor')
        spec.flue_size = form_data.get('flueSize')
        spec.size_of_flue = form_data.get('sizeOfFlue')
        spec.material_of_flue = form_data.get('materialOfFlue')
        spec.chimney_lined_with = form_data.get('chimneyLinedWith')

        # Installation details
        spec.chimney_installed_by = form_data.get('chimneyInstalledBy')
        spec.chimney_installed_by_unknown = form_data.get('chimneyInstalledByUnknown', False)
        spec.chimney_installation_date = form_data.get('date')

        # Fireplace details
        spec.fireplace_location = form_data.get('fireplaceLocation')
        spec.installed_in = form_data.get('installedIn')
        spec.fireplace_location_building = form_data.get('fireplaceLocation2')
        spec.other_location_specify = form_data.get('othersSpecify')
        spec.fireplace_installed_by = form_data.get('fireplaceInstalledBy')
        spec.fireplace_installed_by_unknown = form_data.get('fireplaceInstalledByUnknown', False)
        spec.fireplace_installation_date = form_data.get('date2')
        spec.fireplace_location_final = form_data.get('fireplaceLocation3')
        spec.shares_venting_system = form_data.get('sharesVentingSystem')

        # Assessment details
        spec.comments_condition = form_data.get('commentsCondition')
        spec.suitable = form_data.get('suitable')

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-specification/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_chimney_specification(inspection_id):
    """Get pellet insert chimney specification for an inspection."""
    try:
        spec = PelletInsertChimneySpecification.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Pellet insert chimney specification not found'}), 404

        return jsonify(spec.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-specification/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_chimney_specification(inspection_id):
    """Update pellet insert chimney specification for an inspection."""
    try:
        data = request.get_json()

        spec = PelletInsertChimneySpecification.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Pellet insert chimney specification not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Inspection details
        spec.inspection_discussed = form_data.get('inspectionDiscussed')
        spec.building_permits_available = form_data.get('buildingPermitsAvailable')
        spec.time_of_day = form_data.get('timeOfDay')
        spec.weather_conditions = form_data.get('weatherConditions')
        spec.roofing_type_material = form_data.get('roofingTypeMaterial')
        spec.roof_accessed = form_data.get('roofAccessed')
        spec.attic_accessed = form_data.get('atticAccessed')

        # Construction details
        spec.chimney_constructed_with_building = form_data.get('chimneyConstructedWithBuilding')
        spec.approximate_age = form_data.get('approximateAge')
        spec.chimney_shell = form_data.get('chimneyShell')
        spec.rain_cap = form_data.get('rainCap')
        spec.chimney_location = form_data.get('chimneyLocation')
        spec.height_from_firebox_floor = form_data.get('heightFromFireboxFloor')
        spec.flue_size = form_data.get('flueSize')
        spec.size_of_flue = form_data.get('sizeOfFlue')
        spec.material_of_flue = form_data.get('materialOfFlue')
        spec.chimney_lined_with = form_data.get('chimneyLinedWith')

        # Installation details
        spec.chimney_installed_by = form_data.get('chimneyInstalledBy')
        spec.chimney_installed_by_unknown = form_data.get('chimneyInstalledByUnknown', False)
        spec.chimney_installation_date = form_data.get('date')

        # Fireplace details
        spec.fireplace_location = form_data.get('fireplaceLocation')
        spec.installed_in = form_data.get('installedIn')
        spec.fireplace_location_building = form_data.get('fireplaceLocation2')
        spec.other_location_specify = form_data.get('othersSpecify')
        spec.fireplace_installed_by = form_data.get('fireplaceInstalledBy')
        spec.fireplace_installed_by_unknown = form_data.get('fireplaceInstalledByUnknown', False)
        spec.fireplace_installation_date = form_data.get('date2')
        spec.fireplace_location_final = form_data.get('fireplaceLocation3')
        spec.shares_venting_system = form_data.get('sharesVentingSystem')

        # Assessment details
        spec.comments_condition = form_data.get('commentsCondition')
        spec.suitable = form_data.get('suitable')

        db.session.commit()
        return jsonify(spec.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-specification/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_chimney_specification(inspection_id):
    """Delete pellet insert chimney specification for an inspection."""
    try:
        spec = PelletInsertChimneySpecification.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Pellet insert chimney specification not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Pellet insert chimney specification deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Chimney Stability Caps routes
@main.route('/api/pellet-insert/chimney-stability-caps', methods=['POST'])
def create_pellet_insert_chimney_stability_caps():
    """Create pellet insert chimney stability caps for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert chimney stability caps already exists
        existing_caps = PelletInsertChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()
        if existing_caps:
            return jsonify({'error': 'Pellet insert chimney stability caps already exists for this inspection'}), 400

        # Create new pellet insert chimney stability caps
        caps = PelletInsertChimneyStabilityCaps(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'heightOfChimneyFlues' in form_data:
            section = form_data['heightOfChimneyFlues']
            caps.height_of_chimney_flues_condition = section.get('condition', '')
            caps.height_of_chimney_flues_comments = section.get('comments', '')
            caps.height_of_chimney_flues_code_compliance = section.get('codeCompliance')
            caps.height_of_chimney_flues_photos = section.get('photos', [])
            caps.height_of_chimney_flues_required_height = section.get('requiredHeight', '')
            caps.height_of_chimney_flues_present_height = section.get('presentHeight', '')
            caps.height_of_chimney_flues_required_width = section.get('requiredWidth', '')
            caps.height_of_chimney_flues_present_width = section.get('presentWidth', '')
            caps.height_of_chimney_flues_required_vertical = section.get('requiredVertical', '')
            caps.height_of_chimney_flues_present_vertical = section.get('presentVertical', '')

        if 'lateralStability' in form_data:
            section = form_data['lateralStability']
            caps.lateral_stability_condition = section.get('condition', '')
            caps.lateral_stability_comments = section.get('comments', '')
            caps.lateral_stability_code_compliance = section.get('codeCompliance')
            caps.lateral_stability_photos = section.get('photos', [])

        if 'chimneyCaps1' in form_data:
            section = form_data['chimneyCaps1']
            caps.chimney_caps_1_condition = section.get('condition', '')
            caps.chimney_caps_1_comments = section.get('comments', '')
            caps.chimney_caps_1_code_compliance = section.get('codeCompliance')
            caps.chimney_caps_1_photos = section.get('photos', [])

        if 'chimneyCaps2' in form_data:
            section = form_data['chimneyCaps2']
            caps.chimney_caps_2_condition = section.get('condition', '')
            caps.chimney_caps_2_comments = section.get('comments', '')
            caps.chimney_caps_2_code_compliance = section.get('codeCompliance')
            caps.chimney_caps_2_photos = section.get('photos', [])

        if 'chimneyCaps3' in form_data:
            section = form_data['chimneyCaps3']
            caps.chimney_caps_3_condition = section.get('condition', '')
            caps.chimney_caps_3_comments = section.get('comments', '')
            caps.chimney_caps_3_code_compliance = section.get('codeCompliance')
            caps.chimney_caps_3_photos = section.get('photos', [])

        if 'chimneyCaps4' in form_data:
            section = form_data['chimneyCaps4']
            caps.chimney_caps_4_condition = section.get('condition', '')
            caps.chimney_caps_4_comments = section.get('comments', '')
            caps.chimney_caps_4_code_compliance = section.get('codeCompliance')
            caps.chimney_caps_4_photos = section.get('photos', [])

        db.session.add(caps)
        db.session.commit()
        return jsonify(caps.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-stability-caps/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_chimney_stability_caps(inspection_id):
    """Get pellet insert chimney stability caps for an inspection."""
    try:
        caps = PelletInsertChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()

        if not caps:
            return jsonify({'error': 'Pellet insert chimney stability caps not found'}), 404

        return jsonify(caps.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-stability-caps/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_chimney_stability_caps(inspection_id):
    """Update pellet insert chimney stability caps for an inspection."""
    try:
        data = request.get_json()

        caps = PelletInsertChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()

        if not caps:
            return jsonify({'error': 'Pellet insert chimney stability caps not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'heightOfChimneyFlues' in form_data:
            section = form_data['heightOfChimneyFlues']
            caps.height_of_chimney_flues_condition = section.get('condition', '')
            caps.height_of_chimney_flues_comments = section.get('comments', '')
            caps.height_of_chimney_flues_code_compliance = section.get('codeCompliance')
            caps.height_of_chimney_flues_photos = section.get('photos', [])
            caps.height_of_chimney_flues_required_height = section.get('requiredHeight', '')
            caps.height_of_chimney_flues_present_height = section.get('presentHeight', '')
            caps.height_of_chimney_flues_required_width = section.get('requiredWidth', '')
            caps.height_of_chimney_flues_present_width = section.get('presentWidth', '')
            caps.height_of_chimney_flues_required_vertical = section.get('requiredVertical', '')
            caps.height_of_chimney_flues_present_vertical = section.get('presentVertical', '')

        if 'lateralStability' in form_data:
            section = form_data['lateralStability']
            caps.lateral_stability_condition = section.get('condition', '')
            caps.lateral_stability_comments = section.get('comments', '')
            caps.lateral_stability_code_compliance = section.get('codeCompliance')
            caps.lateral_stability_photos = section.get('photos', [])

        if 'chimneyCaps1' in form_data:
            section = form_data['chimneyCaps1']
            caps.chimney_caps_1_condition = section.get('condition', '')
            caps.chimney_caps_1_comments = section.get('comments', '')
            caps.chimney_caps_1_code_compliance = section.get('codeCompliance')
            caps.chimney_caps_1_photos = section.get('photos', [])

        if 'chimneyCaps2' in form_data:
            section = form_data['chimneyCaps2']
            caps.chimney_caps_2_condition = section.get('condition', '')
            caps.chimney_caps_2_comments = section.get('comments', '')
            caps.chimney_caps_2_code_compliance = section.get('codeCompliance')
            caps.chimney_caps_2_photos = section.get('photos', [])

        if 'chimneyCaps3' in form_data:
            section = form_data['chimneyCaps3']
            caps.chimney_caps_3_condition = section.get('condition', '')
            caps.chimney_caps_3_comments = section.get('comments', '')
            caps.chimney_caps_3_code_compliance = section.get('codeCompliance')
            caps.chimney_caps_3_photos = section.get('photos', [])

        if 'chimneyCaps4' in form_data:
            section = form_data['chimneyCaps4']
            caps.chimney_caps_4_condition = section.get('condition', '')
            caps.chimney_caps_4_comments = section.get('comments', '')
            caps.chimney_caps_4_code_compliance = section.get('codeCompliance')
            caps.chimney_caps_4_photos = section.get('photos', [])

        db.session.commit()
        return jsonify(caps.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-stability-caps/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_chimney_stability_caps(inspection_id):
    """Delete pellet insert chimney stability caps for an inspection."""
    try:
        caps = PelletInsertChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()

        if not caps:
            return jsonify({'error': 'Pellet insert chimney stability caps not found'}), 404

        db.session.delete(caps)
        db.session.commit()
        return jsonify({'message': 'Pellet insert chimney stability caps deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Chimney Support Connection routes
@main.route('/api/pellet-insert/chimney-support-connection', methods=['POST'])
def create_pellet_insert_chimney_support_connection():
    """Create pellet insert chimney support connection for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert chimney support connection already exists
        existing_connection = PelletInsertChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()
        if existing_connection:
            return jsonify({'error': 'Pellet insert chimney support connection already exists for this inspection'}), 400

        # Create new pellet insert chimney support connection
        connection = PelletInsertChimneySupportConnection(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'electricalOutlet' in form_data:
            section = form_data['electricalOutlet']
            connection.electrical_outlet_required_value_uncertified = section.get('requiredValueUncertified', '')
            connection.electrical_outlet_required_value_certified = section.get('requiredValueCertified', '')
            connection.electrical_outlet_present_value = section.get('presentValue')
            connection.electrical_outlet_code_compliance = section.get('codeCompliance')
            connection.electrical_outlet_photos = section.get('photos', [])

        if 'fireplaceModified' in form_data:
            section = form_data['fireplaceModified']
            connection.fireplace_modified_required_value_uncertified = section.get('requiredValueUncertified', '')
            connection.fireplace_modified_required_value_certified = section.get('requiredValueCertified', '')
            connection.fireplace_modified_present_value = section.get('presentValue')
            connection.fireplace_modified_code_compliance = section.get('codeCompliance')
            connection.fireplace_modified_photos = section.get('photos', [])

        if 'coAlarmBCBC' in form_data:
            section = form_data['coAlarmBCBC']
            connection.co_alarm_bcbc_required_value = section.get('requiredValue', '')
            connection.co_alarm_bcbc_present_value = section.get('presentValue')
            connection.co_alarm_bcbc_code_compliance = section.get('codeCompliance')
            connection.co_alarm_bcbc_photos = section.get('photos', [])

        if 'coAlarmNBC' in form_data:
            section = form_data['coAlarmNBC']
            connection.co_alarm_nbc_required_value = section.get('requiredValue', '')
            connection.co_alarm_nbc_present_value = section.get('presentValue')
            connection.co_alarm_nbc_code_compliance = section.get('codeCompliance')
            connection.co_alarm_nbc_photos = section.get('photos', [])

        if 'coAlarmOBC' in form_data:
            section = form_data['coAlarmOBC']
            connection.co_alarm_obc_required_value = section.get('requiredValue', '')
            connection.co_alarm_obc_present_value = section.get('presentValue')
            connection.co_alarm_obc_code_compliance = section.get('codeCompliance')
            connection.co_alarm_obc_photos = section.get('photos', [])

        if 'condition' in form_data:
            section = form_data['condition']
            connection.condition_required_value_uncertified = section.get('requiredValueUncertified', '')
            connection.condition_required_value_certified = section.get('requiredValueCertified', '')
            connection.condition_present_value = section.get('presentValue', '')
            connection.condition_code_compliance = section.get('codeCompliance')
            connection.condition_photos = section.get('photos', [])

        db.session.add(connection)
        db.session.commit()
        return jsonify(connection.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-support-connection/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_chimney_support_connection(inspection_id):
    """Get pellet insert chimney support connection for an inspection."""
    try:
        connection = PelletInsertChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()

        if not connection:
            return jsonify({'error': 'Pellet insert chimney support connection not found'}), 404

        return jsonify(connection.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-support-connection/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_chimney_support_connection(inspection_id):
    """Update pellet insert chimney support connection for an inspection."""
    try:
        data = request.get_json()

        connection = PelletInsertChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()

        if not connection:
            return jsonify({'error': 'Pellet insert chimney support connection not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'electricalOutlet' in form_data:
            section = form_data['electricalOutlet']
            connection.electrical_outlet_required_value_uncertified = section.get('requiredValueUncertified', '')
            connection.electrical_outlet_required_value_certified = section.get('requiredValueCertified', '')
            connection.electrical_outlet_present_value = section.get('presentValue')
            connection.electrical_outlet_code_compliance = section.get('codeCompliance')
            connection.electrical_outlet_photos = section.get('photos', [])

        if 'fireplaceModified' in form_data:
            section = form_data['fireplaceModified']
            connection.fireplace_modified_required_value_uncertified = section.get('requiredValueUncertified', '')
            connection.fireplace_modified_required_value_certified = section.get('requiredValueCertified', '')
            connection.fireplace_modified_present_value = section.get('presentValue')
            connection.fireplace_modified_code_compliance = section.get('codeCompliance')
            connection.fireplace_modified_photos = section.get('photos', [])

        if 'coAlarmBCBC' in form_data:
            section = form_data['coAlarmBCBC']
            connection.co_alarm_bcbc_required_value = section.get('requiredValue', '')
            connection.co_alarm_bcbc_present_value = section.get('presentValue')
            connection.co_alarm_bcbc_code_compliance = section.get('codeCompliance')
            connection.co_alarm_bcbc_photos = section.get('photos', [])

        if 'coAlarmNBC' in form_data:
            section = form_data['coAlarmNBC']
            connection.co_alarm_nbc_required_value = section.get('requiredValue', '')
            connection.co_alarm_nbc_present_value = section.get('presentValue')
            connection.co_alarm_nbc_code_compliance = section.get('codeCompliance')
            connection.co_alarm_nbc_photos = section.get('photos', [])

        if 'coAlarmOBC' in form_data:
            section = form_data['coAlarmOBC']
            connection.co_alarm_obc_required_value = section.get('requiredValue', '')
            connection.co_alarm_obc_present_value = section.get('presentValue')
            connection.co_alarm_obc_code_compliance = section.get('codeCompliance')
            connection.co_alarm_obc_photos = section.get('photos', [])

        if 'condition' in form_data:
            section = form_data['condition']
            connection.condition_required_value_uncertified = section.get('requiredValueUncertified', '')
            connection.condition_required_value_certified = section.get('requiredValueCertified', '')
            connection.condition_present_value = section.get('presentValue', '')
            connection.condition_code_compliance = section.get('codeCompliance')
            connection.condition_photos = section.get('photos', [])

        db.session.commit()
        return jsonify(connection.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-support-connection/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_chimney_support_connection(inspection_id):
    """Delete pellet insert chimney support connection for an inspection."""
    try:
        connection = PelletInsertChimneySupportConnection.query.filter_by(inspection_id=inspection_id).first()

        if not connection:
            return jsonify({'error': 'Pellet insert chimney support connection not found'}), 404

        db.session.delete(connection)
        db.session.commit()
        return jsonify({'message': 'Pellet insert chimney support connection deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Chimney Supports routes
@main.route('/api/pellet-insert/chimney-supports', methods=['POST'])
def create_pellet_insert_chimney_supports():
    """Create pellet insert chimney supports for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert chimney supports already exists
        existing_supports = PelletInsertChimneySupports.query.filter_by(inspection_id=inspection_id).first()
        if existing_supports:
            return jsonify({'error': 'Pellet insert chimney supports already exists for this inspection'}), 400

        # Create new pellet insert chimney supports
        supports = PelletInsertChimneySupports(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'flashing' in form_data:
            section = form_data['flashing']
            supports.flashing_condition = section.get('condition', '')
            supports.flashing_comments = section.get('comments', '')
            supports.flashing_code_compliance = section.get('codeCompliance')
            supports.flashing_photos = section.get('photos', [])

        if 'clearanceFromCombustibleMaterials1' in form_data:
            section = form_data['clearanceFromCombustibleMaterials1']
            supports.clearance_from_combustible_materials_1_condition = section.get('condition', '')
            supports.clearance_from_combustible_materials_1_comments = section.get('comments', '')
            supports.clearance_from_combustible_materials_1_code_compliance = section.get('codeCompliance')
            supports.clearance_from_combustible_materials_1_photos = section.get('photos', [])

        if 'clearanceFromCombustibleMaterials2' in form_data:
            section = form_data['clearanceFromCombustibleMaterials2']
            supports.clearance_from_combustible_materials_2_condition = section.get('condition', '')
            supports.clearance_from_combustible_materials_2_comments = section.get('comments', '')
            supports.clearance_from_combustible_materials_2_code_compliance = section.get('codeCompliance')
            supports.clearance_from_combustible_materials_2_photos = section.get('photos', [])

        if 'sealingOfSpaces' in form_data:
            section = form_data['sealingOfSpaces']
            supports.sealing_of_spaces_condition = section.get('condition', '')
            supports.sealing_of_spaces_comments = section.get('comments', '')
            supports.sealing_of_spaces_code_compliance = section.get('codeCompliance')
            supports.sealing_of_spaces_photos = section.get('photos', [])

        if 'supportOfJoistsOrBeams' in form_data:
            section = form_data['supportOfJoistsOrBeams']
            supports.support_of_joists_or_beams_condition = section.get('condition', '')
            supports.support_of_joists_or_beams_comments = section.get('comments', '')
            supports.support_of_joists_or_beams_code_compliance = section.get('codeCompliance')
            supports.support_of_joists_or_beams_photos = section.get('photos', [])

        if 'intersectionOfShingleRoofsAndMasonry' in form_data:
            section = form_data['intersectionOfShingleRoofsAndMasonry']
            supports.intersection_of_shingle_roofs_and_masonry_condition = section.get('condition', '')
            supports.intersection_of_shingle_roofs_and_masonry_comments = section.get('comments', '')
            supports.intersection_of_shingle_roofs_and_masonry_code_compliance = section.get('codeCompliance')
            supports.intersection_of_shingle_roofs_and_masonry_photos = section.get('photos', [])

        db.session.add(supports)
        db.session.commit()
        return jsonify(supports.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-supports/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_chimney_supports(inspection_id):
    """Get pellet insert chimney supports for an inspection."""
    try:
        supports = PelletInsertChimneySupports.query.filter_by(inspection_id=inspection_id).first()

        if not supports:
            return jsonify({'error': 'Pellet insert chimney supports not found'}), 404

        return jsonify(supports.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-supports/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_chimney_supports(inspection_id):
    """Update pellet insert chimney supports for an inspection."""
    try:
        data = request.get_json()

        supports = PelletInsertChimneySupports.query.filter_by(inspection_id=inspection_id).first()

        if not supports:
            return jsonify({'error': 'Pellet insert chimney supports not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'flashing' in form_data:
            section = form_data['flashing']
            supports.flashing_condition = section.get('condition', '')
            supports.flashing_comments = section.get('comments', '')
            supports.flashing_code_compliance = section.get('codeCompliance')
            supports.flashing_photos = section.get('photos', [])

        if 'clearanceFromCombustibleMaterials1' in form_data:
            section = form_data['clearanceFromCombustibleMaterials1']
            supports.clearance_from_combustible_materials_1_condition = section.get('condition', '')
            supports.clearance_from_combustible_materials_1_comments = section.get('comments', '')
            supports.clearance_from_combustible_materials_1_code_compliance = section.get('codeCompliance')
            supports.clearance_from_combustible_materials_1_photos = section.get('photos', [])

        if 'clearanceFromCombustibleMaterials2' in form_data:
            section = form_data['clearanceFromCombustibleMaterials2']
            supports.clearance_from_combustible_materials_2_condition = section.get('condition', '')
            supports.clearance_from_combustible_materials_2_comments = section.get('comments', '')
            supports.clearance_from_combustible_materials_2_code_compliance = section.get('codeCompliance')
            supports.clearance_from_combustible_materials_2_photos = section.get('photos', [])

        if 'sealingOfSpaces' in form_data:
            section = form_data['sealingOfSpaces']
            supports.sealing_of_spaces_condition = section.get('condition', '')
            supports.sealing_of_spaces_comments = section.get('comments', '')
            supports.sealing_of_spaces_code_compliance = section.get('codeCompliance')
            supports.sealing_of_spaces_photos = section.get('photos', [])

        if 'supportOfJoistsOrBeams' in form_data:
            section = form_data['supportOfJoistsOrBeams']
            supports.support_of_joists_or_beams_condition = section.get('condition', '')
            supports.support_of_joists_or_beams_comments = section.get('comments', '')
            supports.support_of_joists_or_beams_code_compliance = section.get('codeCompliance')
            supports.support_of_joists_or_beams_photos = section.get('photos', [])

        if 'intersectionOfShingleRoofsAndMasonry' in form_data:
            section = form_data['intersectionOfShingleRoofsAndMasonry']
            supports.intersection_of_shingle_roofs_and_masonry_condition = section.get('condition', '')
            supports.intersection_of_shingle_roofs_and_masonry_comments = section.get('comments', '')
            supports.intersection_of_shingle_roofs_and_masonry_code_compliance = section.get('codeCompliance')
            supports.intersection_of_shingle_roofs_and_masonry_photos = section.get('photos', [])

        db.session.commit()
        return jsonify(supports.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-supports/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_chimney_supports(inspection_id):
    """Delete pellet insert chimney supports for an inspection."""
    try:
        supports = PelletInsertChimneySupports.query.filter_by(inspection_id=inspection_id).first()

        if not supports:
            return jsonify({'error': 'Pellet insert chimney supports not found'}), 404

        db.session.delete(supports)
        db.session.commit()
        return jsonify({'message': 'Pellet insert chimney supports deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert CO Alarms Liners routes
@main.route('/api/pellet-insert/co-alarms-liners', methods=['POST'])
def create_pellet_insert_co_alarms_liners():
    """Create pellet insert CO alarms liners for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert CO alarms liners already exists
        existing_co_alarms_liners = PelletInsertCOAlarmsLiners.query.filter_by(inspection_id=inspection_id).first()
        if existing_co_alarms_liners:
            return jsonify({'error': 'Pellet insert CO alarms liners already exists for this inspection'}), 400

        # Create new pellet insert CO alarms liners
        co_alarms_liners = PelletInsertCOAlarmsLiners(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'abcBcbcNbcCombustionAir' in form_data:
            section = form_data['abcBcbcNbcCombustionAir']
            co_alarms_liners.abc_bcbc_nbc_combustion_air_condition = section.get('condition', '')
            co_alarms_liners.abc_bcbc_nbc_combustion_air_comments = section.get('comments', '')
            co_alarms_liners.abc_bcbc_nbc_combustion_air_code_compliance = section.get('codeCompliance')
            co_alarms_liners.abc_bcbc_nbc_combustion_air_photos = section.get('photos', [])

        if 'nbcAbcCombustionAir' in form_data:
            section = form_data['nbcAbcCombustionAir']
            co_alarms_liners.nbc_abc_combustion_air_condition = section.get('condition', '')
            co_alarms_liners.nbc_abc_combustion_air_comments = section.get('comments', '')
            co_alarms_liners.nbc_abc_combustion_air_code_compliance = section.get('codeCompliance')
            co_alarms_liners.nbc_abc_combustion_air_photos = section.get('photos', [])

        if 'sObcCombustionAir' in form_data:
            section = form_data['sObcCombustionAir']
            co_alarms_liners.s_obc_combustion_air_condition = section.get('condition', '')
            co_alarms_liners.s_obc_combustion_air_comments = section.get('comments', '')
            co_alarms_liners.s_obc_combustion_air_code_compliance = section.get('codeCompliance')
            co_alarms_liners.s_obc_combustion_air_photos = section.get('photos', [])

        if 'brickOrSteelLiners' in form_data:
            section = form_data['brickOrSteelLiners']
            co_alarms_liners.brick_or_steel_liners_condition = section.get('condition', '')
            co_alarms_liners.brick_or_steel_liners_comments = section.get('comments', '')
            co_alarms_liners.brick_or_steel_liners_code_compliance = section.get('codeCompliance')
            co_alarms_liners.brick_or_steel_liners_photos = section.get('photos', [])

        if 'firebrickLiners1' in form_data:
            section = form_data['firebrickLiners1']
            co_alarms_liners.firebrick_liners_1_condition = section.get('condition', '')
            co_alarms_liners.firebrick_liners_1_comments = section.get('comments', '')
            co_alarms_liners.firebrick_liners_1_code_compliance = section.get('codeCompliance')
            co_alarms_liners.firebrick_liners_1_photos = section.get('photos', [])

        if 'firebrickLiners2' in form_data:
            section = form_data['firebrickLiners2']
            co_alarms_liners.firebrick_liners_2_condition = section.get('condition', '')
            co_alarms_liners.firebrick_liners_2_comments = section.get('comments', '')
            co_alarms_liners.firebrick_liners_2_code_compliance = section.get('codeCompliance')
            co_alarms_liners.firebrick_liners_2_photos = section.get('photos', [])

        db.session.add(co_alarms_liners)
        db.session.commit()
        return jsonify(co_alarms_liners.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/co-alarms-liners/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_co_alarms_liners(inspection_id):
    """Get pellet insert CO alarms liners for an inspection."""
    try:
        co_alarms_liners = PelletInsertCOAlarmsLiners.query.filter_by(inspection_id=inspection_id).first()

        if not co_alarms_liners:
            return jsonify({'error': 'Pellet insert CO alarms liners not found'}), 404

        return jsonify(co_alarms_liners.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/co-alarms-liners/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_co_alarms_liners(inspection_id):
    """Update pellet insert CO alarms liners for an inspection."""
    try:
        data = request.get_json()

        co_alarms_liners = PelletInsertCOAlarmsLiners.query.filter_by(inspection_id=inspection_id).first()

        if not co_alarms_liners:
            return jsonify({'error': 'Pellet insert CO alarms liners not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'abcBcbcNbcCombustionAir' in form_data:
            section = form_data['abcBcbcNbcCombustionAir']
            co_alarms_liners.abc_bcbc_nbc_combustion_air_condition = section.get('condition', '')
            co_alarms_liners.abc_bcbc_nbc_combustion_air_comments = section.get('comments', '')
            co_alarms_liners.abc_bcbc_nbc_combustion_air_code_compliance = section.get('codeCompliance')
            co_alarms_liners.abc_bcbc_nbc_combustion_air_photos = section.get('photos', [])

        if 'nbcAbcCombustionAir' in form_data:
            section = form_data['nbcAbcCombustionAir']
            co_alarms_liners.nbc_abc_combustion_air_condition = section.get('condition', '')
            co_alarms_liners.nbc_abc_combustion_air_comments = section.get('comments', '')
            co_alarms_liners.nbc_abc_combustion_air_code_compliance = section.get('codeCompliance')
            co_alarms_liners.nbc_abc_combustion_air_photos = section.get('photos', [])

        if 'sObcCombustionAir' in form_data:
            section = form_data['sObcCombustionAir']
            co_alarms_liners.s_obc_combustion_air_condition = section.get('condition', '')
            co_alarms_liners.s_obc_combustion_air_comments = section.get('comments', '')
            co_alarms_liners.s_obc_combustion_air_code_compliance = section.get('codeCompliance')
            co_alarms_liners.s_obc_combustion_air_photos = section.get('photos', [])

        if 'brickOrSteelLiners' in form_data:
            section = form_data['brickOrSteelLiners']
            co_alarms_liners.brick_or_steel_liners_condition = section.get('condition', '')
            co_alarms_liners.brick_or_steel_liners_comments = section.get('comments', '')
            co_alarms_liners.brick_or_steel_liners_code_compliance = section.get('codeCompliance')
            co_alarms_liners.brick_or_steel_liners_photos = section.get('photos', [])

        if 'firebrickLiners1' in form_data:
            section = form_data['firebrickLiners1']
            co_alarms_liners.firebrick_liners_1_condition = section.get('condition', '')
            co_alarms_liners.firebrick_liners_1_comments = section.get('comments', '')
            co_alarms_liners.firebrick_liners_1_code_compliance = section.get('codeCompliance')
            co_alarms_liners.firebrick_liners_1_photos = section.get('photos', [])

        if 'firebrickLiners2' in form_data:
            section = form_data['firebrickLiners2']
            co_alarms_liners.firebrick_liners_2_condition = section.get('condition', '')
            co_alarms_liners.firebrick_liners_2_comments = section.get('comments', '')
            co_alarms_liners.firebrick_liners_2_code_compliance = section.get('codeCompliance')
            co_alarms_liners.firebrick_liners_2_photos = section.get('photos', [])

        db.session.commit()
        return jsonify(co_alarms_liners.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/co-alarms-liners/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_co_alarms_liners(inspection_id):
    """Delete pellet insert CO alarms liners for an inspection."""
    try:
        co_alarms_liners = PelletInsertCOAlarmsLiners.query.filter_by(inspection_id=inspection_id).first()

        if not co_alarms_liners:
            return jsonify({'error': 'Pellet insert CO alarms liners not found'}), 404

        db.session.delete(co_alarms_liners)
        db.session.commit()
        return jsonify({'message': 'Pellet insert CO alarms liners deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Ember Pad Floor Protection routes
@main.route('/api/pellet-insert/ember-pad-floor-protection', methods=['POST'])
def create_pellet_insert_ember_pad_floor_protection():
    """Create pellet insert ember pad floor protection for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert ember pad floor protection already exists
        existing_ember_pad_floor_protection = PelletInsertEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if existing_ember_pad_floor_protection:
            return jsonify({'error': 'Pellet insert ember pad floor protection already exists for this inspection'}), 400

        # Create new pellet insert ember pad floor protection
        ember_pad_floor_protection = PelletInsertEmberPadFloorProtection(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'emberPadFront' in form_data:
            section = form_data['emberPadFront']
            ember_pad_floor_protection.ember_pad_front_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.ember_pad_front_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.ember_pad_front_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.ember_pad_front_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.ember_pad_front_photos = section.get('photos', [])

        if 'emberPadRightSide' in form_data:
            section = form_data['emberPadRightSide']
            ember_pad_floor_protection.ember_pad_right_side_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.ember_pad_right_side_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.ember_pad_right_side_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.ember_pad_right_side_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.ember_pad_right_side_photos = section.get('photos', [])

        if 'emberPadLeftSide' in form_data:
            section = form_data['emberPadLeftSide']
            ember_pad_floor_protection.ember_pad_left_side_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.ember_pad_left_side_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.ember_pad_left_side_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.ember_pad_left_side_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.ember_pad_left_side_photos = section.get('photos', [])

        if 'floorProtectionMaterial' in form_data:
            section = form_data['floorProtectionMaterial']
            ember_pad_floor_protection.floor_protection_material_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.floor_protection_material_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.floor_protection_material_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.floor_protection_material_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.floor_protection_material_photos = section.get('photos', [])

        if 'radiantFloorProtection' in form_data:
            section = form_data['radiantFloorProtection']
            ember_pad_floor_protection.radiant_floor_protection_required_value = section.get('requiredValue', '')
            ember_pad_floor_protection.radiant_floor_protection_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.radiant_floor_protection_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.radiant_floor_protection_photos = section.get('photos', [])

        if 'floorProtectionFront' in form_data:
            section = form_data['floorProtectionFront']
            ember_pad_floor_protection.floor_protection_front_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.floor_protection_front_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.floor_protection_front_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.floor_protection_front_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.floor_protection_front_photos = section.get('photos', [])

        if 'floorProtectionRightSide' in form_data:
            section = form_data['floorProtectionRightSide']
            ember_pad_floor_protection.floor_protection_right_side_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.floor_protection_right_side_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.floor_protection_right_side_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.floor_protection_right_side_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.floor_protection_right_side_photos = section.get('photos', [])

        if 'floorProtectionLeftSide' in form_data:
            section = form_data['floorProtectionLeftSide']
            ember_pad_floor_protection.floor_protection_left_side_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.floor_protection_left_side_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.floor_protection_left_side_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.floor_protection_left_side_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.floor_protection_left_side_photos = section.get('photos', [])

        db.session.add(ember_pad_floor_protection)
        db.session.commit()
        return jsonify(ember_pad_floor_protection.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/ember-pad-floor-protection/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_ember_pad_floor_protection(inspection_id):
    """Get pellet insert ember pad floor protection for an inspection."""
    try:
        ember_pad_floor_protection = PelletInsertEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()

        if not ember_pad_floor_protection:
            return jsonify({'error': 'Pellet insert ember pad floor protection not found'}), 404

        return jsonify(ember_pad_floor_protection.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/ember-pad-floor-protection/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_ember_pad_floor_protection(inspection_id):
    """Update pellet insert ember pad floor protection for an inspection."""
    try:
        data = request.get_json()

        ember_pad_floor_protection = PelletInsertEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()

        if not ember_pad_floor_protection:
            return jsonify({'error': 'Pellet insert ember pad floor protection not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'emberPadFront' in form_data:
            section = form_data['emberPadFront']
            ember_pad_floor_protection.ember_pad_front_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.ember_pad_front_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.ember_pad_front_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.ember_pad_front_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.ember_pad_front_photos = section.get('photos', [])

        if 'emberPadRightSide' in form_data:
            section = form_data['emberPadRightSide']
            ember_pad_floor_protection.ember_pad_right_side_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.ember_pad_right_side_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.ember_pad_right_side_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.ember_pad_right_side_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.ember_pad_right_side_photos = section.get('photos', [])

        if 'emberPadLeftSide' in form_data:
            section = form_data['emberPadLeftSide']
            ember_pad_floor_protection.ember_pad_left_side_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.ember_pad_left_side_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.ember_pad_left_side_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.ember_pad_left_side_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.ember_pad_left_side_photos = section.get('photos', [])

        if 'floorProtectionMaterial' in form_data:
            section = form_data['floorProtectionMaterial']
            ember_pad_floor_protection.floor_protection_material_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.floor_protection_material_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.floor_protection_material_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.floor_protection_material_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.floor_protection_material_photos = section.get('photos', [])

        if 'radiantFloorProtection' in form_data:
            section = form_data['radiantFloorProtection']
            ember_pad_floor_protection.radiant_floor_protection_required_value = section.get('requiredValue', '')
            ember_pad_floor_protection.radiant_floor_protection_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.radiant_floor_protection_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.radiant_floor_protection_photos = section.get('photos', [])

        if 'floorProtectionFront' in form_data:
            section = form_data['floorProtectionFront']
            ember_pad_floor_protection.floor_protection_front_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.floor_protection_front_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.floor_protection_front_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.floor_protection_front_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.floor_protection_front_photos = section.get('photos', [])

        if 'floorProtectionRightSide' in form_data:
            section = form_data['floorProtectionRightSide']
            ember_pad_floor_protection.floor_protection_right_side_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.floor_protection_right_side_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.floor_protection_right_side_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.floor_protection_right_side_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.floor_protection_right_side_photos = section.get('photos', [])

        if 'floorProtectionLeftSide' in form_data:
            section = form_data['floorProtectionLeftSide']
            ember_pad_floor_protection.floor_protection_left_side_required_uncertified = section.get('requiredValueUncertified', '')
            ember_pad_floor_protection.floor_protection_left_side_required_certified = section.get('requiredValueCertified', '')
            ember_pad_floor_protection.floor_protection_left_side_present_value = section.get('presentValue', '')
            ember_pad_floor_protection.floor_protection_left_side_code_compliance = section.get('codeCompliance')
            ember_pad_floor_protection.floor_protection_left_side_photos = section.get('photos', [])

        db.session.commit()
        return jsonify(ember_pad_floor_protection.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/ember-pad-floor-protection/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_ember_pad_floor_protection(inspection_id):
    """Delete pellet insert ember pad floor protection for an inspection."""
    try:
        ember_pad_floor_protection = PelletInsertEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()

        if not ember_pad_floor_protection:
            return jsonify({'error': 'Pellet insert ember pad floor protection not found'}), 404

        db.session.delete(ember_pad_floor_protection)
        db.session.commit()
        return jsonify({'message': 'Pellet insert ember pad floor protection deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Fireplace Safety Features routes
@main.route('/api/pellet-insert/fireplace-safety-features', methods=['POST'])
def create_pellet_insert_fireplace_safety_features():
    """Create pellet insert fireplace safety features for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert fireplace safety features already exists
        existing_fireplace_safety_features = PelletInsertFireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()
        if existing_fireplace_safety_features:
            return jsonify({'error': 'Pellet insert fireplace safety features already exists for this inspection'}), 400

        # Create new pellet insert fireplace safety features
        fireplace_safety_features = PelletInsertFireplaceSafetyFeatures(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'basicInfo' in form_data:
            basic_info = form_data['basicInfo']
            fireplace_safety_features.basic_info_manufacturer = basic_info.get('manufacturer', '')
            fireplace_safety_features.basic_info_model = basic_info.get('model', '')
            fireplace_safety_features.basic_info_listing_agency = basic_info.get('listingAgency', '')
            fireplace_safety_features.basic_info_is_listing_agency_manually_available = basic_info.get('isListingAgencyManuallyAvailable', '')
            fireplace_safety_features.basic_info_certification_standard = basic_info.get('certificationStandard', '')
            fireplace_safety_features.basic_info_listing_agency_type = basic_info.get('listingAgencyType', '')
            fireplace_safety_features.basic_info_diameter = basic_info.get('diameter', '')
            fireplace_safety_features.basic_info_comments = basic_info.get('comments', '')

        if 'linerFromTopToTop' in form_data:
            section = form_data['linerFromTopToTop']
            fireplace_safety_features.liner_from_top_to_top_required_value = section.get('requiredValue', '')
            fireplace_safety_features.liner_from_top_to_top_present_value = section.get('presentValue', '')
            fireplace_safety_features.liner_from_top_to_top_code_compliance = section.get('codeCompliance')
            fireplace_safety_features.liner_from_top_to_top_photos = section.get('photos', [])

        if 'connectionToStainlessSteel' in form_data:
            section = form_data['connectionToStainlessSteel']
            fireplace_safety_features.connection_to_stainless_steel_required_value = section.get('requiredValue', '')
            fireplace_safety_features.connection_to_stainless_steel_comments = section.get('comments', '')
            fireplace_safety_features.connection_to_stainless_steel_code_compliance = section.get('codeCompliance')
            fireplace_safety_features.connection_to_stainless_steel_photos = section.get('photos', [])

        if 'continuousLiner' in form_data:
            section = form_data['continuousLiner']
            fireplace_safety_features.continuous_liner_required_value = section.get('requiredValue', '')
            fireplace_safety_features.continuous_liner_present_value = section.get('presentValue', '')
            fireplace_safety_features.continuous_liner_code_compliance = section.get('codeCompliance')
            fireplace_safety_features.continuous_liner_photos = section.get('photos', [])

        if 'totalLengthEVL' in form_data:
            section = form_data['totalLengthEVL']
            fireplace_safety_features.total_length_evl_required_value = section.get('requiredValue', '')
            fireplace_safety_features.total_length_evl_present_value = section.get('presentValue', '')
            fireplace_safety_features.total_length_evl_code_compliance = section.get('codeCompliance')
            fireplace_safety_features.total_length_evl_photos = section.get('photos', [])

        if 'linerVentBaseTee' in form_data:
            section = form_data['linerVentBaseTee']
            fireplace_safety_features.liner_vent_base_tee_required_value = section.get('requiredValue', '')
            fireplace_safety_features.liner_vent_base_tee_present_value = section.get('presentValue', '')
            fireplace_safety_features.liner_vent_base_tee_code_compliance = section.get('codeCompliance')
            fireplace_safety_features.liner_vent_base_tee_photos = section.get('photos', [])

        db.session.add(fireplace_safety_features)
        db.session.commit()
        return jsonify(fireplace_safety_features.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/fireplace-safety-features/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_fireplace_safety_features(inspection_id):
    """Get pellet insert fireplace safety features for an inspection."""
    try:
        fireplace_safety_features = PelletInsertFireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()

        if not fireplace_safety_features:
            return jsonify({'error': 'Pellet insert fireplace safety features not found'}), 404

        return jsonify(fireplace_safety_features.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/fireplace-safety-features/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_fireplace_safety_features(inspection_id):
    """Update pellet insert fireplace safety features for an inspection."""
    try:
        data = request.get_json()

        fireplace_safety_features = PelletInsertFireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()

        if not fireplace_safety_features:
            return jsonify({'error': 'Pellet insert fireplace safety features not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'basicInfo' in form_data:
            basic_info = form_data['basicInfo']
            fireplace_safety_features.basic_info_manufacturer = basic_info.get('manufacturer', '')
            fireplace_safety_features.basic_info_model = basic_info.get('model', '')
            fireplace_safety_features.basic_info_listing_agency = basic_info.get('listingAgency', '')
            fireplace_safety_features.basic_info_is_listing_agency_manually_available = basic_info.get('isListingAgencyManuallyAvailable', '')
            fireplace_safety_features.basic_info_certification_standard = basic_info.get('certificationStandard', '')
            fireplace_safety_features.basic_info_listing_agency_type = basic_info.get('listingAgencyType', '')
            fireplace_safety_features.basic_info_diameter = basic_info.get('diameter', '')
            fireplace_safety_features.basic_info_comments = basic_info.get('comments', '')

        if 'linerFromTopToTop' in form_data:
            section = form_data['linerFromTopToTop']
            fireplace_safety_features.liner_from_top_to_top_required_value = section.get('requiredValue', '')
            fireplace_safety_features.liner_from_top_to_top_present_value = section.get('presentValue', '')
            fireplace_safety_features.liner_from_top_to_top_code_compliance = section.get('codeCompliance')
            fireplace_safety_features.liner_from_top_to_top_photos = section.get('photos', [])

        if 'connectionToStainlessSteel' in form_data:
            section = form_data['connectionToStainlessSteel']
            fireplace_safety_features.connection_to_stainless_steel_required_value = section.get('requiredValue', '')
            fireplace_safety_features.connection_to_stainless_steel_comments = section.get('comments', '')
            fireplace_safety_features.connection_to_stainless_steel_code_compliance = section.get('codeCompliance')
            fireplace_safety_features.connection_to_stainless_steel_photos = section.get('photos', [])

        if 'continuousLiner' in form_data:
            section = form_data['continuousLiner']
            fireplace_safety_features.continuous_liner_required_value = section.get('requiredValue', '')
            fireplace_safety_features.continuous_liner_present_value = section.get('presentValue', '')
            fireplace_safety_features.continuous_liner_code_compliance = section.get('codeCompliance')
            fireplace_safety_features.continuous_liner_photos = section.get('photos', [])

        if 'totalLengthEVL' in form_data:
            section = form_data['totalLengthEVL']
            fireplace_safety_features.total_length_evl_required_value = section.get('requiredValue', '')
            fireplace_safety_features.total_length_evl_present_value = section.get('presentValue', '')
            fireplace_safety_features.total_length_evl_code_compliance = section.get('codeCompliance')
            fireplace_safety_features.total_length_evl_photos = section.get('photos', [])

        if 'linerVentBaseTee' in form_data:
            section = form_data['linerVentBaseTee']
            fireplace_safety_features.liner_vent_base_tee_required_value = section.get('requiredValue', '')
            fireplace_safety_features.liner_vent_base_tee_present_value = section.get('presentValue', '')
            fireplace_safety_features.liner_vent_base_tee_code_compliance = section.get('codeCompliance')
            fireplace_safety_features.liner_vent_base_tee_photos = section.get('photos', [])

        db.session.commit()
        return jsonify(fireplace_safety_features.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/fireplace-safety-features/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_fireplace_safety_features(inspection_id):
    """Delete pellet insert fireplace safety features for an inspection."""
    try:
        fireplace_safety_features = PelletInsertFireplaceSafetyFeatures.query.filter_by(inspection_id=inspection_id).first()

        if not fireplace_safety_features:
            return jsonify({'error': 'Pellet insert fireplace safety features not found'}), 404

        db.session.delete(fireplace_safety_features)
        db.session.commit()
        return jsonify({'message': 'Pellet insert fireplace safety features deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Fireplace Specifications routes
@main.route('/api/pellet-insert/fireplace-specifications', methods=['POST'])
def create_pellet_insert_fireplace_specifications():
    """Create pellet insert fireplace specifications for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert fireplace specifications already exists
        existing_fireplace_specifications = PelletInsertFireplaceSpecifications.query.filter_by(inspection_id=inspection_id).first()
        if existing_fireplace_specifications:
            return jsonify({'error': 'Pellet insert fireplace specifications already exists for this inspection'}), 400

        # Create new pellet insert fireplace specifications
        fireplace_specifications = PelletInsertFireplaceSpecifications(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        fireplace_specifications.fireplace_make_model_serial = form_data.get('fireplaceMakeModelSerial', '')
        fireplace_specifications.installation_manual_available = form_data.get('installationManualAvailable', '')
        fireplace_specifications.certification_standard = form_data.get('certificationStandard', '')
        fireplace_specifications.listing_agency = form_data.get('listingAgency', '')
        fireplace_specifications.appliance_type = form_data.get('applianceType', '')
        fireplace_specifications.flu_collar_size = form_data.get('fluCollarSize', '')
        fireplace_specifications.fan_blower_attached = form_data.get('fanBlowerAttached', '')
        fireplace_specifications.comments_condition = form_data.get('commentsCondition', '')
        fireplace_specifications.suitable = form_data.get('suitable', '')
        fireplace_specifications.installed_in = form_data.get('installedIn', '')
        fireplace_specifications.specify_installed_in = form_data.get('specifyInstalledIn', '')
        fireplace_specifications.appliance_location = form_data.get('applianceLocation', '')
        fireplace_specifications.specify_appliance_location = form_data.get('specifyApplianceLocation', '')
        fireplace_specifications.appliance_installed_by = form_data.get('applianceInstalledBy', '')
        fireplace_specifications.appliance_installed_by_unknown = form_data.get('applianceInstalledByUnknown', False)
        fireplace_specifications.comments = form_data.get('comments', '')

        db.session.add(fireplace_specifications)
        db.session.commit()
        return jsonify(fireplace_specifications.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/fireplace-specifications/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_fireplace_specifications(inspection_id):
    """Get pellet insert fireplace specifications for an inspection."""
    try:
        fireplace_specifications = PelletInsertFireplaceSpecifications.query.filter_by(inspection_id=inspection_id).first()

        if not fireplace_specifications:
            return jsonify({'error': 'Pellet insert fireplace specifications not found'}), 404

        return jsonify(fireplace_specifications.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/fireplace-specifications/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_fireplace_specifications(inspection_id):
    """Update pellet insert fireplace specifications for an inspection."""
    try:
        data = request.get_json()

        fireplace_specifications = PelletInsertFireplaceSpecifications.query.filter_by(inspection_id=inspection_id).first()

        if not fireplace_specifications:
            return jsonify({'error': 'Pellet insert fireplace specifications not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        fireplace_specifications.fireplace_make_model_serial = form_data.get('fireplaceMakeModelSerial', '')
        fireplace_specifications.installation_manual_available = form_data.get('installationManualAvailable', '')
        fireplace_specifications.certification_standard = form_data.get('certificationStandard', '')
        fireplace_specifications.listing_agency = form_data.get('listingAgency', '')
        fireplace_specifications.appliance_type = form_data.get('applianceType', '')
        fireplace_specifications.flu_collar_size = form_data.get('fluCollarSize', '')
        fireplace_specifications.fan_blower_attached = form_data.get('fanBlowerAttached', '')
        fireplace_specifications.comments_condition = form_data.get('commentsCondition', '')
        fireplace_specifications.suitable = form_data.get('suitable', '')
        fireplace_specifications.installed_in = form_data.get('installedIn', '')
        fireplace_specifications.specify_installed_in = form_data.get('specifyInstalledIn', '')
        fireplace_specifications.appliance_location = form_data.get('applianceLocation', '')
        fireplace_specifications.specify_appliance_location = form_data.get('specifyApplianceLocation', '')
        fireplace_specifications.appliance_installed_by = form_data.get('applianceInstalledBy', '')
        fireplace_specifications.appliance_installed_by_unknown = form_data.get('applianceInstalledByUnknown', False)
        fireplace_specifications.comments = form_data.get('comments', '')

        db.session.commit()
        return jsonify(fireplace_specifications.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/fireplace-specifications/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_fireplace_specifications(inspection_id):
    """Delete pellet insert fireplace specifications for an inspection."""
    try:
        fireplace_specifications = PelletInsertFireplaceSpecifications.query.filter_by(inspection_id=inspection_id).first()

        if not fireplace_specifications:
            return jsonify({'error': 'Pellet insert fireplace specifications not found'}), 404

        db.session.delete(fireplace_specifications)
        db.session.commit()
        return jsonify({'message': 'Pellet insert fireplace specifications deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Liner Appliance Checks 1 routes
@main.route('/api/pellet-insert/liner-appliance-checks-1', methods=['POST'])
def create_pellet_insert_liner_appliance_checks_1():
    """Create pellet insert liner appliance checks 1 for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert liner appliance checks 1 already exists
        existing_checks = PelletInsertLinerApplianceChecks1.query.filter_by(inspection_id=inspection_id).first()
        if existing_checks:
            return jsonify({'error': 'Pellet insert liner appliance checks 1 already exists for this inspection'}), 400

        # Create new pellet insert liner appliance checks 1
        checks = PelletInsertLinerApplianceChecks1(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Liner/vent base tee support
        checks.liner_vent_base_tee_support_required_value = form_data.get('linerVentBaseTeeSupport', {}).get('requiredValue', '')
        checks.liner_vent_base_tee_support_present_value = form_data.get('linerVentBaseTeeSupport', {}).get('presentValue', '')
        checks.liner_vent_base_tee_support_code_compliance = form_data.get('linerVentBaseTeeSupport', {}).get('codeCompliance', '')
        checks.liner_vent_base_tee_support_photos = form_data.get('linerVentBaseTeeSupport', {}).get('photos', [])

        # Liner/vent/flashing/storm collar
        checks.liner_vent_flashing_storm_collar_required_value = form_data.get('linerVentFlashingStormCollar', {}).get('requiredValue', '')
        checks.liner_vent_flashing_storm_collar_present_value = form_data.get('linerVentFlashingStormCollar', {}).get('presentValue', '')
        checks.liner_vent_flashing_storm_collar_code_compliance = form_data.get('linerVentFlashingStormCollar', {}).get('codeCompliance', '')
        checks.liner_vent_flashing_storm_collar_photos = form_data.get('linerVentFlashingStormCollar', {}).get('photos', [])

        # Insulated liner
        checks.insulated_liner_required_value = form_data.get('insulatedLiner', {}).get('requiredValue', '')
        checks.insulated_liner_present_value = form_data.get('insulatedLiner', {}).get('presentValue', '')
        checks.insulated_liner_code_compliance = form_data.get('insulatedLiner', {}).get('codeCompliance', '')
        checks.insulated_liner_photos = form_data.get('insulatedLiner', {}).get('photos', [])

        # Appliance Vent adaptor
        checks.appliance_vent_adaptor_required_value = form_data.get('applianceVentAdaptor', {}).get('requiredValue', '')
        checks.appliance_vent_adaptor_present_value = form_data.get('applianceVentAdaptor', {}).get('presentValue', '')
        checks.appliance_vent_adaptor_code_compliance = form_data.get('applianceVentAdaptor', {}).get('codeCompliance', '')
        checks.appliance_vent_adaptor_photos = form_data.get('applianceVentAdaptor', {}).get('photos', [])

        # Vent sealing
        checks.vent_sealing_required_value = form_data.get('ventSealing', {}).get('requiredValue', '')
        checks.vent_sealing_present_value = form_data.get('ventSealing', {}).get('presentValue', '')
        checks.vent_sealing_code_compliance = form_data.get('ventSealing', {}).get('codeCompliance', '')
        checks.vent_sealing_photos = form_data.get('ventSealing', {}).get('photos', [])

        # Liner/vent condition - Acceptable?
        checks.liner_vent_condition_acceptable_required_value = form_data.get('linerVentConditionAcceptable', {}).get('requiredValue', '')
        checks.liner_vent_condition_acceptable_present_value = form_data.get('linerVentConditionAcceptable', {}).get('presentValue', '')
        checks.liner_vent_condition_acceptable_code_compliance = form_data.get('linerVentConditionAcceptable', {}).get('codeCompliance', '')
        checks.liner_vent_condition_acceptable_photos = form_data.get('linerVentConditionAcceptable', {}).get('photos', [])

        db.session.add(checks)
        db.session.commit()
        return jsonify(checks.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/liner-appliance-checks-1/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_liner_appliance_checks_1(inspection_id):
    """Get pellet insert liner appliance checks 1 for an inspection."""
    try:
        checks = PelletInsertLinerApplianceChecks1.query.filter_by(inspection_id=inspection_id).first()

        if not checks:
            return jsonify({'error': 'Pellet insert liner appliance checks 1 not found'}), 404

        return jsonify(checks.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/liner-appliance-checks-1/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_liner_appliance_checks_1(inspection_id):
    """Update pellet insert liner appliance checks 1 for an inspection."""
    try:
        data = request.get_json()

        checks = PelletInsertLinerApplianceChecks1.query.filter_by(inspection_id=inspection_id).first()

        if not checks:
            return jsonify({'error': 'Pellet insert liner appliance checks 1 not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Liner/vent base tee support
        checks.liner_vent_base_tee_support_required_value = form_data.get('linerVentBaseTeeSupport', {}).get('requiredValue', '')
        checks.liner_vent_base_tee_support_present_value = form_data.get('linerVentBaseTeeSupport', {}).get('presentValue', '')
        checks.liner_vent_base_tee_support_code_compliance = form_data.get('linerVentBaseTeeSupport', {}).get('codeCompliance', '')
        checks.liner_vent_base_tee_support_photos = form_data.get('linerVentBaseTeeSupport', {}).get('photos', [])

        # Liner/vent/flashing/storm collar
        checks.liner_vent_flashing_storm_collar_required_value = form_data.get('linerVentFlashingStormCollar', {}).get('requiredValue', '')
        checks.liner_vent_flashing_storm_collar_present_value = form_data.get('linerVentFlashingStormCollar', {}).get('presentValue', '')
        checks.liner_vent_flashing_storm_collar_code_compliance = form_data.get('linerVentFlashingStormCollar', {}).get('codeCompliance', '')
        checks.liner_vent_flashing_storm_collar_photos = form_data.get('linerVentFlashingStormCollar', {}).get('photos', [])

        # Insulated liner
        checks.insulated_liner_required_value = form_data.get('insulatedLiner', {}).get('requiredValue', '')
        checks.insulated_liner_present_value = form_data.get('insulatedLiner', {}).get('presentValue', '')
        checks.insulated_liner_code_compliance = form_data.get('insulatedLiner', {}).get('codeCompliance', '')
        checks.insulated_liner_photos = form_data.get('insulatedLiner', {}).get('photos', [])

        # Appliance Vent adaptor
        checks.appliance_vent_adaptor_required_value = form_data.get('applianceVentAdaptor', {}).get('requiredValue', '')
        checks.appliance_vent_adaptor_present_value = form_data.get('applianceVentAdaptor', {}).get('presentValue', '')
        checks.appliance_vent_adaptor_code_compliance = form_data.get('applianceVentAdaptor', {}).get('codeCompliance', '')
        checks.appliance_vent_adaptor_photos = form_data.get('applianceVentAdaptor', {}).get('photos', [])

        # Vent sealing
        checks.vent_sealing_required_value = form_data.get('ventSealing', {}).get('requiredValue', '')
        checks.vent_sealing_present_value = form_data.get('ventSealing', {}).get('presentValue', '')
        checks.vent_sealing_code_compliance = form_data.get('ventSealing', {}).get('codeCompliance', '')
        checks.vent_sealing_photos = form_data.get('ventSealing', {}).get('photos', [])

        # Liner/vent condition - Acceptable?
        checks.liner_vent_condition_acceptable_required_value = form_data.get('linerVentConditionAcceptable', {}).get('requiredValue', '')
        checks.liner_vent_condition_acceptable_present_value = form_data.get('linerVentConditionAcceptable', {}).get('presentValue', '')
        checks.liner_vent_condition_acceptable_code_compliance = form_data.get('linerVentConditionAcceptable', {}).get('codeCompliance', '')
        checks.liner_vent_condition_acceptable_photos = form_data.get('linerVentConditionAcceptable', {}).get('photos', [])

        db.session.commit()
        return jsonify(checks.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/liner-appliance-checks-1/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_liner_appliance_checks_1(inspection_id):
    """Delete pellet insert liner appliance checks 1 for an inspection."""
    try:
        checks = PelletInsertLinerApplianceChecks1.query.filter_by(inspection_id=inspection_id).first()

        if not checks:
            return jsonify({'error': 'Pellet insert liner appliance checks 1 not found'}), 404

        db.session.delete(checks)
        db.session.commit()
        return jsonify({'message': 'Pellet insert liner appliance checks 1 deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Liner Appliance Checks 2 routes
@main.route('/api/pellet-insert/liner-appliance-checks-2', methods=['POST'])
def create_pellet_insert_liner_appliance_checks_2():
    """Create pellet insert liner appliance checks 2 for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert liner appliance checks 2 already exists
        existing_checks = PelletInsertLinerApplianceChecks2.query.filter_by(inspection_id=inspection_id).first()
        if existing_checks:
            return jsonify({'error': 'Pellet insert liner appliance checks 2 already exists for this inspection'}), 400

        # Create new pellet insert liner appliance checks 2
        checks = PelletInsertLinerApplianceChecks2(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Appliance Standard
        checks.appliance_standard_condition = form_data.get('applianceStandard', {}).get('condition', '')
        checks.appliance_standard_comments = form_data.get('applianceStandard', {}).get('comments', '')
        checks.appliance_standard_code_compliance = form_data.get('applianceStandard', {}).get('codeCompliance', '')
        checks.appliance_standard_photos = form_data.get('applianceStandard', {}).get('photos', [])

        # Footings
        checks.footings_condition = form_data.get('footings', {}).get('condition', '')
        checks.footings_comments = form_data.get('footings', {}).get('comments', '')
        checks.footings_code_compliance = form_data.get('footings', {}).get('codeCompliance', '')
        checks.footings_photos = form_data.get('footings', {}).get('photos', [])

        # Fireplace Chimneys
        checks.fireplace_chimneys_condition = form_data.get('fireplaceChimneys', {}).get('condition', '')
        checks.fireplace_chimneys_comments = form_data.get('fireplaceChimneys', {}).get('comments', '')
        checks.fireplace_chimneys_code_compliance = form_data.get('fireplaceChimneys', {}).get('codeCompliance', '')
        checks.fireplace_chimneys_photos = form_data.get('fireplaceChimneys', {}).get('photos', [])
        checks.fireplace_chimneys_fireball_opening_height = form_data.get('fireplaceChimneys', {}).get('fireballOpeningHeight', '')
        checks.fireplace_chimneys_fireball_opening_width = form_data.get('fireplaceChimneys', {}).get('fireballOpeningWidth', '')
        checks.fireplace_chimneys_fireball_opening_total = form_data.get('fireplaceChimneys', {}).get('fireballOpeningTotal', '')
        checks.fireplace_chimneys_flue_size_required = form_data.get('fireplaceChimneys', {}).get('flueSizeRequired', '')

        # ABC/BCBC/NBC Lintels
        checks.abc_bcbc_nbc_lintels_condition = form_data.get('abcBcbcNbcLintels', {}).get('condition', '')
        checks.abc_bcbc_nbc_lintels_comments = form_data.get('abcBcbcNbcLintels', {}).get('comments', '')
        checks.abc_bcbc_nbc_lintels_code_compliance = form_data.get('abcBcbcNbcLintels', {}).get('codeCompliance', '')
        checks.abc_bcbc_nbc_lintels_photos = form_data.get('abcBcbcNbcLintels', {}).get('photos', [])

        # OBC Lintels
        checks.obc_lintels_condition = form_data.get('obcLintels', {}).get('condition', '')
        checks.obc_lintels_comments = form_data.get('obcLintels', {}).get('comments', '')
        checks.obc_lintels_code_compliance = form_data.get('obcLintels', {}).get('codeCompliance', '')
        checks.obc_lintels_photos = form_data.get('obcLintels', {}).get('photos', [])

        # Corbelling
        checks.corbelling_condition = form_data.get('corbelling', {}).get('condition', '')
        checks.corbelling_comments = form_data.get('corbelling', {}).get('comments', '')
        checks.corbelling_code_compliance = form_data.get('corbelling', {}).get('codeCompliance', '')
        checks.corbelling_photos = form_data.get('corbelling', {}).get('photos', [])

        db.session.add(checks)
        db.session.commit()
        return jsonify(checks.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/liner-appliance-checks-2/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_liner_appliance_checks_2(inspection_id):
    """Get pellet insert liner appliance checks 2 for an inspection."""
    try:
        checks = PelletInsertLinerApplianceChecks2.query.filter_by(inspection_id=inspection_id).first()

        if not checks:
            return jsonify({'error': 'Pellet insert liner appliance checks 2 not found'}), 404

        return jsonify(checks.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/liner-appliance-checks-2/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_liner_appliance_checks_2(inspection_id):
    """Update pellet insert liner appliance checks 2 for an inspection."""
    try:
        data = request.get_json()

        checks = PelletInsertLinerApplianceChecks2.query.filter_by(inspection_id=inspection_id).first()

        if not checks:
            return jsonify({'error': 'Pellet insert liner appliance checks 2 not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Appliance Standard
        checks.appliance_standard_condition = form_data.get('applianceStandard', {}).get('condition', '')
        checks.appliance_standard_comments = form_data.get('applianceStandard', {}).get('comments', '')
        checks.appliance_standard_code_compliance = form_data.get('applianceStandard', {}).get('codeCompliance', '')
        checks.appliance_standard_photos = form_data.get('applianceStandard', {}).get('photos', [])

        # Footings
        checks.footings_condition = form_data.get('footings', {}).get('condition', '')
        checks.footings_comments = form_data.get('footings', {}).get('comments', '')
        checks.footings_code_compliance = form_data.get('footings', {}).get('codeCompliance', '')
        checks.footings_photos = form_data.get('footings', {}).get('photos', [])

        # Fireplace Chimneys
        checks.fireplace_chimneys_condition = form_data.get('fireplaceChimneys', {}).get('condition', '')
        checks.fireplace_chimneys_comments = form_data.get('fireplaceChimneys', {}).get('comments', '')
        checks.fireplace_chimneys_code_compliance = form_data.get('fireplaceChimneys', {}).get('codeCompliance', '')
        checks.fireplace_chimneys_photos = form_data.get('fireplaceChimneys', {}).get('photos', [])
        checks.fireplace_chimneys_fireball_opening_height = form_data.get('fireplaceChimneys', {}).get('fireballOpeningHeight', '')
        checks.fireplace_chimneys_fireball_opening_width = form_data.get('fireplaceChimneys', {}).get('fireballOpeningWidth', '')
        checks.fireplace_chimneys_fireball_opening_total = form_data.get('fireplaceChimneys', {}).get('fireballOpeningTotal', '')
        checks.fireplace_chimneys_flue_size_required = form_data.get('fireplaceChimneys', {}).get('flueSizeRequired', '')

        # ABC/BCBC/NBC Lintels
        checks.abc_bcbc_nbc_lintels_condition = form_data.get('abcBcbcNbcLintels', {}).get('condition', '')
        checks.abc_bcbc_nbc_lintels_comments = form_data.get('abcBcbcNbcLintels', {}).get('comments', '')
        checks.abc_bcbc_nbc_lintels_code_compliance = form_data.get('abcBcbcNbcLintels', {}).get('codeCompliance', '')
        checks.abc_bcbc_nbc_lintels_photos = form_data.get('abcBcbcNbcLintels', {}).get('photos', [])

        # OBC Lintels
        checks.obc_lintels_condition = form_data.get('obcLintels', {}).get('condition', '')
        checks.obc_lintels_comments = form_data.get('obcLintels', {}).get('comments', '')
        checks.obc_lintels_code_compliance = form_data.get('obcLintels', {}).get('codeCompliance', '')
        checks.obc_lintels_photos = form_data.get('obcLintels', {}).get('photos', [])

        # Corbelling
        checks.corbelling_condition = form_data.get('corbelling', {}).get('condition', '')
        checks.corbelling_comments = form_data.get('corbelling', {}).get('comments', '')
        checks.corbelling_code_compliance = form_data.get('corbelling', {}).get('codeCompliance', '')
        checks.corbelling_photos = form_data.get('corbelling', {}).get('photos', [])

        db.session.commit()
        return jsonify(checks.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/liner-appliance-checks-2/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_liner_appliance_checks_2(inspection_id):
    """Delete pellet insert liner appliance checks 2 for an inspection."""
    try:
        checks = PelletInsertLinerApplianceChecks2.query.filter_by(inspection_id=inspection_id).first()

        if not checks:
            return jsonify({'error': 'Pellet insert liner appliance checks 2 not found'}), 404

        db.session.delete(checks)
        db.session.commit()
        return jsonify({'message': 'Pellet insert liner appliance checks 2 deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Liner Vent Components routes
@main.route('/api/pellet-insert/liner-vent-components', methods=['POST'])
def create_pellet_insert_liner_vent_components():
    """Create pellet insert liner vent components for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert liner vent components already exists
        existing_components = PelletInsertLinerVentComponents.query.filter_by(inspection_id=inspection_id).first()
        if existing_components:
            return jsonify({'error': 'Pellet insert liner vent components already exists for this inspection'}), 400

        # Create new pellet insert liner vent components
        components = PelletInsertLinerVentComponents(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Firebrick Liners
        components.firebrick_liners_condition = form_data.get('firebrickLiners', {}).get('condition', '')
        components.firebrick_liners_comments = form_data.get('firebrickLiners', {}).get('comments', '')
        components.firebrick_liners_code_compliance = form_data.get('firebrickLiners', {}).get('codeCompliance', '')
        components.firebrick_liners_photos = form_data.get('firebrickLiners', {}).get('photos', [])

        # Steel Liners
        components.steel_liners_condition = form_data.get('steelLiners', {}).get('condition', '')
        components.steel_liners_comments = form_data.get('steelLiners', {}).get('comments', '')
        components.steel_liners_code_compliance = form_data.get('steelLiners', {}).get('codeCompliance', '')
        components.steel_liners_photos = form_data.get('steelLiners', {}).get('photos', [])

        # Thickness of Walls 1
        components.thickness_of_walls_1_condition = form_data.get('thicknessOfWalls1', {}).get('condition', '')
        components.thickness_of_walls_1_comments = form_data.get('thicknessOfWalls1', {}).get('comments', '')
        components.thickness_of_walls_1_code_compliance = form_data.get('thicknessOfWalls1', {}).get('codeCompliance', '')
        components.thickness_of_walls_1_photos = form_data.get('thicknessOfWalls1', {}).get('photos', [])

        # Thickness of Walls 2
        components.thickness_of_walls_2_condition = form_data.get('thicknessOfWalls2', {}).get('condition', '')
        components.thickness_of_walls_2_comments = form_data.get('thicknessOfWalls2', {}).get('comments', '')
        components.thickness_of_walls_2_code_compliance = form_data.get('thicknessOfWalls2', {}).get('codeCompliance', '')
        components.thickness_of_walls_2_photos = form_data.get('thicknessOfWalls2', {}).get('photos', [])

        # Fire Chamber Dimensions
        components.fire_chamber_dimensions_condition = form_data.get('fireChamberDimensions', {}).get('condition', '')
        components.fire_chamber_dimensions_comments = form_data.get('fireChamberDimensions', {}).get('comments', '')
        components.fire_chamber_dimensions_code_compliance = form_data.get('fireChamberDimensions', {}).get('codeCompliance', '')
        components.fire_chamber_dimensions_photos = form_data.get('fireChamberDimensions', {}).get('photos', [])

        # Hearth Extension
        components.hearth_extension_condition = form_data.get('hearthExtension', {}).get('condition', '')
        components.hearth_extension_comments = form_data.get('hearthExtension', {}).get('comments', '')
        components.hearth_extension_code_compliance = form_data.get('hearthExtension', {}).get('codeCompliance', '')
        components.hearth_extension_photos = form_data.get('hearthExtension', {}).get('photos', [])

        db.session.add(components)
        db.session.commit()
        return jsonify(components.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/liner-vent-components/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_liner_vent_components(inspection_id):
    """Get pellet insert liner vent components for an inspection."""
    try:
        components = PelletInsertLinerVentComponents.query.filter_by(inspection_id=inspection_id).first()

        if not components:
            return jsonify({'error': 'Pellet insert liner vent components not found'}), 404

        return jsonify(components.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/liner-vent-components/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_liner_vent_components(inspection_id):
    """Update pellet insert liner vent components for an inspection."""
    try:
        data = request.get_json()

        components = PelletInsertLinerVentComponents.query.filter_by(inspection_id=inspection_id).first()

        if not components:
            return jsonify({'error': 'Pellet insert liner vent components not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Firebrick Liners
        components.firebrick_liners_condition = form_data.get('firebrickLiners', {}).get('condition', '')
        components.firebrick_liners_comments = form_data.get('firebrickLiners', {}).get('comments', '')
        components.firebrick_liners_code_compliance = form_data.get('firebrickLiners', {}).get('codeCompliance', '')
        components.firebrick_liners_photos = form_data.get('firebrickLiners', {}).get('photos', [])

        # Steel Liners
        components.steel_liners_condition = form_data.get('steelLiners', {}).get('condition', '')
        components.steel_liners_comments = form_data.get('steelLiners', {}).get('comments', '')
        components.steel_liners_code_compliance = form_data.get('steelLiners', {}).get('codeCompliance', '')
        components.steel_liners_photos = form_data.get('steelLiners', {}).get('photos', [])

        # Thickness of Walls 1
        components.thickness_of_walls_1_condition = form_data.get('thicknessOfWalls1', {}).get('condition', '')
        components.thickness_of_walls_1_comments = form_data.get('thicknessOfWalls1', {}).get('comments', '')
        components.thickness_of_walls_1_code_compliance = form_data.get('thicknessOfWalls1', {}).get('codeCompliance', '')
        components.thickness_of_walls_1_photos = form_data.get('thicknessOfWalls1', {}).get('photos', [])

        # Thickness of Walls 2
        components.thickness_of_walls_2_condition = form_data.get('thicknessOfWalls2', {}).get('condition', '')
        components.thickness_of_walls_2_comments = form_data.get('thicknessOfWalls2', {}).get('comments', '')
        components.thickness_of_walls_2_code_compliance = form_data.get('thicknessOfWalls2', {}).get('codeCompliance', '')
        components.thickness_of_walls_2_photos = form_data.get('thicknessOfWalls2', {}).get('photos', [])

        # Fire Chamber Dimensions
        components.fire_chamber_dimensions_condition = form_data.get('fireChamberDimensions', {}).get('condition', '')
        components.fire_chamber_dimensions_comments = form_data.get('fireChamberDimensions', {}).get('comments', '')
        components.fire_chamber_dimensions_code_compliance = form_data.get('fireChamberDimensions', {}).get('codeCompliance', '')
        components.fire_chamber_dimensions_photos = form_data.get('fireChamberDimensions', {}).get('photos', [])

        # Hearth Extension
        components.hearth_extension_condition = form_data.get('hearthExtension', {}).get('condition', '')
        components.hearth_extension_comments = form_data.get('hearthExtension', {}).get('comments', '')
        components.hearth_extension_code_compliance = form_data.get('hearthExtension', {}).get('codeCompliance', '')
        components.hearth_extension_photos = form_data.get('hearthExtension', {}).get('photos', [])

        db.session.commit()
        return jsonify(components.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/liner-vent-components/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_liner_vent_components(inspection_id):
    """Delete pellet insert liner vent components for an inspection."""
    try:
        components = PelletInsertLinerVentComponents.query.filter_by(inspection_id=inspection_id).first()

        if not components:
            return jsonify({'error': 'Pellet insert liner vent components not found'}), 404

        db.session.delete(components)
        db.session.commit()
        return jsonify({'message': 'Pellet insert liner vent components deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Masonry Fireplace Construction 1 routes
@main.route('/api/pellet-insert/masonry-fireplace-construction-1', methods=['POST'])
def create_pellet_insert_masonry_fireplace_construction_1():
    """Create pellet insert masonry fireplace construction 1 for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert masonry fireplace construction 1 already exists
        existing_construction = PelletInsertMasonryFireplaceConstruction1.query.filter_by(inspection_id=inspection_id).first()
        if existing_construction:
            return jsonify({'error': 'Pellet insert masonry fireplace construction 1 already exists for this inspection'}), 400

        # Create new pellet insert masonry fireplace construction 1
        construction = PelletInsertMasonryFireplaceConstruction1(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Hearth Extension
        construction.hearth_extension_condition = form_data.get('hearthExtension', {}).get('condition', '')
        construction.hearth_extension_comments = form_data.get('hearthExtension', {}).get('comments', '')
        construction.hearth_extension_code_compliance = form_data.get('hearthExtension', {}).get('codeCompliance', '')
        construction.hearth_extension_photos = form_data.get('hearthExtension', {}).get('photos', [])

        # Support of Hearth 1
        construction.support_of_hearth_1_condition = form_data.get('supportOfHearth1', {}).get('condition', '')
        construction.support_of_hearth_1_comments = form_data.get('supportOfHearth1', {}).get('comments', '')
        construction.support_of_hearth_1_code_compliance = form_data.get('supportOfHearth1', {}).get('codeCompliance', '')
        construction.support_of_hearth_1_photos = form_data.get('supportOfHearth1', {}).get('photos', [])

        # Support of Hearth 2
        construction.support_of_hearth_2_condition = form_data.get('supportOfHearth2', {}).get('condition', '')
        construction.support_of_hearth_2_comments = form_data.get('supportOfHearth2', {}).get('comments', '')
        construction.support_of_hearth_2_code_compliance = form_data.get('supportOfHearth2', {}).get('codeCompliance', '')
        construction.support_of_hearth_2_photos = form_data.get('supportOfHearth2', {}).get('photos', [])

        # Slope of Smoke Chamber
        construction.slope_of_smoke_chamber_condition = form_data.get('slopeOfSmokeChamber', {}).get('condition', '')
        construction.slope_of_smoke_chamber_comments = form_data.get('slopeOfSmokeChamber', {}).get('comments', '')
        construction.slope_of_smoke_chamber_code_compliance = form_data.get('slopeOfSmokeChamber', {}).get('codeCompliance', '')
        construction.slope_of_smoke_chamber_photos = form_data.get('slopeOfSmokeChamber', {}).get('photos', [])

        # Wall Thickness
        construction.wall_thickness_condition = form_data.get('wallThickness', {}).get('condition', '')
        construction.wall_thickness_comments = form_data.get('wallThickness', {}).get('comments', '')
        construction.wall_thickness_code_compliance = form_data.get('wallThickness', {}).get('codeCompliance', '')
        construction.wall_thickness_photos = form_data.get('wallThickness', {}).get('photos', [])

        # Clearance to Fireplace Opening
        construction.clearance_to_fireplace_opening_condition = form_data.get('clearanceToFireplaceOpening', {}).get('condition', '')
        construction.clearance_to_fireplace_opening_comments = form_data.get('clearanceToFireplaceOpening', {}).get('comments', '')
        construction.clearance_to_fireplace_opening_code_compliance = form_data.get('clearanceToFireplaceOpening', {}).get('codeCompliance', '')
        construction.clearance_to_fireplace_opening_photos = form_data.get('clearanceToFireplaceOpening', {}).get('photos', [])

        db.session.add(construction)
        db.session.commit()
        return jsonify(construction.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/masonry-fireplace-construction-1/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_masonry_fireplace_construction_1(inspection_id):
    """Get pellet insert masonry fireplace construction 1 for an inspection."""
    try:
        construction = PelletInsertMasonryFireplaceConstruction1.query.filter_by(inspection_id=inspection_id).first()

        if not construction:
            return jsonify({'error': 'Pellet insert masonry fireplace construction 1 not found'}), 404

        return jsonify(construction.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/masonry-fireplace-construction-1/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_masonry_fireplace_construction_1(inspection_id):
    """Update pellet insert masonry fireplace construction 1 for an inspection."""
    try:
        data = request.get_json()

        construction = PelletInsertMasonryFireplaceConstruction1.query.filter_by(inspection_id=inspection_id).first()

        if not construction:
            return jsonify({'error': 'Pellet insert masonry fireplace construction 1 not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Hearth Extension
        construction.hearth_extension_condition = form_data.get('hearthExtension', {}).get('condition', '')
        construction.hearth_extension_comments = form_data.get('hearthExtension', {}).get('comments', '')
        construction.hearth_extension_code_compliance = form_data.get('hearthExtension', {}).get('codeCompliance', '')
        construction.hearth_extension_photos = form_data.get('hearthExtension', {}).get('photos', [])

        # Support of Hearth 1
        construction.support_of_hearth_1_condition = form_data.get('supportOfHearth1', {}).get('condition', '')
        construction.support_of_hearth_1_comments = form_data.get('supportOfHearth1', {}).get('comments', '')
        construction.support_of_hearth_1_code_compliance = form_data.get('supportOfHearth1', {}).get('codeCompliance', '')
        construction.support_of_hearth_1_photos = form_data.get('supportOfHearth1', {}).get('photos', [])

        # Support of Hearth 2
        construction.support_of_hearth_2_condition = form_data.get('supportOfHearth2', {}).get('condition', '')
        construction.support_of_hearth_2_comments = form_data.get('supportOfHearth2', {}).get('comments', '')
        construction.support_of_hearth_2_code_compliance = form_data.get('supportOfHearth2', {}).get('codeCompliance', '')
        construction.support_of_hearth_2_photos = form_data.get('supportOfHearth2', {}).get('photos', [])

        # Slope of Smoke Chamber
        construction.slope_of_smoke_chamber_condition = form_data.get('slopeOfSmokeChamber', {}).get('condition', '')
        construction.slope_of_smoke_chamber_comments = form_data.get('slopeOfSmokeChamber', {}).get('comments', '')
        construction.slope_of_smoke_chamber_code_compliance = form_data.get('slopeOfSmokeChamber', {}).get('codeCompliance', '')
        construction.slope_of_smoke_chamber_photos = form_data.get('slopeOfSmokeChamber', {}).get('photos', [])

        # Wall Thickness
        construction.wall_thickness_condition = form_data.get('wallThickness', {}).get('condition', '')
        construction.wall_thickness_comments = form_data.get('wallThickness', {}).get('comments', '')
        construction.wall_thickness_code_compliance = form_data.get('wallThickness', {}).get('codeCompliance', '')
        construction.wall_thickness_photos = form_data.get('wallThickness', {}).get('photos', [])

        # Clearance to Fireplace Opening
        construction.clearance_to_fireplace_opening_condition = form_data.get('clearanceToFireplaceOpening', {}).get('condition', '')
        construction.clearance_to_fireplace_opening_comments = form_data.get('clearanceToFireplaceOpening', {}).get('comments', '')
        construction.clearance_to_fireplace_opening_code_compliance = form_data.get('clearanceToFireplaceOpening', {}).get('codeCompliance', '')
        construction.clearance_to_fireplace_opening_photos = form_data.get('clearanceToFireplaceOpening', {}).get('photos', [])

        db.session.commit()
        return jsonify(construction.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/masonry-fireplace-construction-1/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_masonry_fireplace_construction_1(inspection_id):
    """Delete pellet insert masonry fireplace construction 1 for an inspection."""
    try:
        construction = PelletInsertMasonryFireplaceConstruction1.query.filter_by(inspection_id=inspection_id).first()

        if not construction:
            return jsonify({'error': 'Pellet insert masonry fireplace construction 1 not found'}), 404

        db.session.delete(construction)
        db.session.commit()
        return jsonify({'message': 'Pellet insert masonry fireplace construction 1 deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Masonry Fireplace Construction 2 routes
@main.route('/api/pellet-insert/masonry-fireplace-construction-2', methods=['POST'])
def create_pellet_insert_masonry_fireplace_construction_2():
    """Create pellet insert masonry fireplace construction 2 for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert masonry fireplace construction 2 already exists
        existing_construction = PelletInsertMasonryFireplaceConstruction2.query.filter_by(inspection_id=inspection_id).first()
        if existing_construction:
            return jsonify({'error': 'Pellet insert masonry fireplace construction 2 already exists for this inspection'}), 400

        # Create new pellet insert masonry fireplace construction 2
        construction = PelletInsertMasonryFireplaceConstruction2(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Material located in the interior
        construction.material_located_in_interior_condition = form_data.get('materialLocatedInInterior', {}).get('condition', '')
        construction.material_located_in_interior_comments = form_data.get('materialLocatedInInterior', {}).get('comments', '')
        construction.material_located_in_interior_code_compliance = form_data.get('materialLocatedInInterior', {}).get('codeCompliance', '')
        construction.material_located_in_interior_photos = form_data.get('materialLocatedInInterior', {}).get('photos', [])

        # Clearance to Combustible Framing 1
        construction.clearance_to_combustible_framing_1_condition = form_data.get('clearanceToCombustibleFraming1', {}).get('condition', '')
        construction.clearance_to_combustible_framing_1_comments = form_data.get('clearanceToCombustibleFraming1', {}).get('comments', '')
        construction.clearance_to_combustible_framing_1_code_compliance = form_data.get('clearanceToCombustibleFraming1', {}).get('codeCompliance', '')
        construction.clearance_to_combustible_framing_1_photos = form_data.get('clearanceToCombustibleFraming1', {}).get('photos', [])

        # Clearance to Combustible Framing 2
        construction.clearance_to_combustible_framing_2_condition = form_data.get('clearanceToCombustibleFraming2', {}).get('condition', '')
        construction.clearance_to_combustible_framing_2_comments = form_data.get('clearanceToCombustibleFraming2', {}).get('comments', '')
        construction.clearance_to_combustible_framing_2_code_compliance = form_data.get('clearanceToCombustibleFraming2', {}).get('codeCompliance', '')
        construction.clearance_to_combustible_framing_2_photos = form_data.get('clearanceToCombustibleFraming2', {}).get('photos', [])

        # Heat-Circulating Duct Outlets
        construction.heat_circulating_duct_outlets_condition = form_data.get('heatCirculatingDuctOutlets', {}).get('condition', '')
        construction.heat_circulating_duct_outlets_comments = form_data.get('heatCirculatingDuctOutlets', {}).get('comments', '')
        construction.heat_circulating_duct_outlets_code_compliance = form_data.get('heatCirculatingDuctOutlets', {}).get('codeCompliance', '')
        construction.heat_circulating_duct_outlets_photos = form_data.get('heatCirculatingDuctOutlets', {}).get('photos', [])

        # ABC/BCBC/NBC Fireplace Inserts
        construction.abc_bcbc_nbc_fireplace_inserts_condition = form_data.get('abcBcbcNbcFireplaceInserts', {}).get('condition', '')
        construction.abc_bcbc_nbc_fireplace_inserts_comments = form_data.get('abcBcbcNbcFireplaceInserts', {}).get('comments', '')
        construction.abc_bcbc_nbc_fireplace_inserts_code_compliance = form_data.get('abcBcbcNbcFireplaceInserts', {}).get('codeCompliance', '')
        construction.abc_bcbc_nbc_fireplace_inserts_photos = form_data.get('abcBcbcNbcFireplaceInserts', {}).get('photos', [])

        # OBC Fireplace Inserts
        construction.obc_fireplace_inserts_condition = form_data.get('obcFireplaceInserts', {}).get('condition', '')
        construction.obc_fireplace_inserts_comments = form_data.get('obcFireplaceInserts', {}).get('comments', '')
        construction.obc_fireplace_inserts_code_compliance = form_data.get('obcFireplaceInserts', {}).get('codeCompliance', '')
        construction.obc_fireplace_inserts_photos = form_data.get('obcFireplaceInserts', {}).get('photos', [])

        # Cleanout
        construction.cleanout_condition = form_data.get('cleanout', {}).get('condition', '')
        construction.cleanout_comments = form_data.get('cleanout', {}).get('comments', '')
        construction.cleanout_code_compliance = form_data.get('cleanout', {}).get('codeCompliance', '')
        construction.cleanout_photos = form_data.get('cleanout', {}).get('photos', [])

        # Clearance from Combustible Materials
        construction.clearance_from_combustible_materials_condition = form_data.get('clearanceFromCombustibleMaterials', {}).get('condition', '')
        construction.clearance_from_combustible_materials_comments = form_data.get('clearanceFromCombustibleMaterials', {}).get('comments', '')
        construction.clearance_from_combustible_materials_code_compliance = form_data.get('clearanceFromCombustibleMaterials', {}).get('codeCompliance', '')
        construction.clearance_from_combustible_materials_photos = form_data.get('clearanceFromCombustibleMaterials', {}).get('photos', [])

        # Wall Thickness
        construction.wall_thickness_condition = form_data.get('wallThickness', {}).get('condition', '')
        construction.wall_thickness_comments = form_data.get('wallThickness', {}).get('comments', '')
        construction.wall_thickness_code_compliance = form_data.get('wallThickness', {}).get('codeCompliance', '')
        construction.wall_thickness_photos = form_data.get('wallThickness', {}).get('photos', [])

        db.session.add(construction)
        db.session.commit()
        return jsonify(construction.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/masonry-fireplace-construction-2/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_masonry_fireplace_construction_2(inspection_id):
    """Get pellet insert masonry fireplace construction 2 for an inspection."""
    try:
        construction = PelletInsertMasonryFireplaceConstruction2.query.filter_by(inspection_id=inspection_id).first()

        if not construction:
            return jsonify({'error': 'Pellet insert masonry fireplace construction 2 not found'}), 404

        return jsonify(construction.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/masonry-fireplace-construction-2/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_masonry_fireplace_construction_2(inspection_id):
    """Update pellet insert masonry fireplace construction 2 for an inspection."""
    try:
        data = request.get_json()

        construction = PelletInsertMasonryFireplaceConstruction2.query.filter_by(inspection_id=inspection_id).first()

        if not construction:
            return jsonify({'error': 'Pellet insert masonry fireplace construction 2 not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Material located in the interior
        construction.material_located_in_interior_condition = form_data.get('materialLocatedInInterior', {}).get('condition', '')
        construction.material_located_in_interior_comments = form_data.get('materialLocatedInInterior', {}).get('comments', '')
        construction.material_located_in_interior_code_compliance = form_data.get('materialLocatedInInterior', {}).get('codeCompliance', '')
        construction.material_located_in_interior_photos = form_data.get('materialLocatedInInterior', {}).get('photos', [])

        # Clearance to Combustible Framing 1
        construction.clearance_to_combustible_framing_1_condition = form_data.get('clearanceToCombustibleFraming1', {}).get('condition', '')
        construction.clearance_to_combustible_framing_1_comments = form_data.get('clearanceToCombustibleFraming1', {}).get('comments', '')
        construction.clearance_to_combustible_framing_1_code_compliance = form_data.get('clearanceToCombustibleFraming1', {}).get('codeCompliance', '')
        construction.clearance_to_combustible_framing_1_photos = form_data.get('clearanceToCombustibleFraming1', {}).get('photos', [])

        # Clearance to Combustible Framing 2
        construction.clearance_to_combustible_framing_2_condition = form_data.get('clearanceToCombustibleFraming2', {}).get('condition', '')
        construction.clearance_to_combustible_framing_2_comments = form_data.get('clearanceToCombustibleFraming2', {}).get('comments', '')
        construction.clearance_to_combustible_framing_2_code_compliance = form_data.get('clearanceToCombustibleFraming2', {}).get('codeCompliance', '')
        construction.clearance_to_combustible_framing_2_photos = form_data.get('clearanceToCombustibleFraming2', {}).get('photos', [])

        # Heat-Circulating Duct Outlets
        construction.heat_circulating_duct_outlets_condition = form_data.get('heatCirculatingDuctOutlets', {}).get('condition', '')
        construction.heat_circulating_duct_outlets_comments = form_data.get('heatCirculatingDuctOutlets', {}).get('comments', '')
        construction.heat_circulating_duct_outlets_code_compliance = form_data.get('heatCirculatingDuctOutlets', {}).get('codeCompliance', '')
        construction.heat_circulating_duct_outlets_photos = form_data.get('heatCirculatingDuctOutlets', {}).get('photos', [])

        # ABC/BCBC/NBC Fireplace Inserts
        construction.abc_bcbc_nbc_fireplace_inserts_condition = form_data.get('abcBcbcNbcFireplaceInserts', {}).get('condition', '')
        construction.abc_bcbc_nbc_fireplace_inserts_comments = form_data.get('abcBcbcNbcFireplaceInserts', {}).get('comments', '')
        construction.abc_bcbc_nbc_fireplace_inserts_code_compliance = form_data.get('abcBcbcNbcFireplaceInserts', {}).get('codeCompliance', '')
        construction.abc_bcbc_nbc_fireplace_inserts_photos = form_data.get('abcBcbcNbcFireplaceInserts', {}).get('photos', [])

        # OBC Fireplace Inserts
        construction.obc_fireplace_inserts_condition = form_data.get('obcFireplaceInserts', {}).get('condition', '')
        construction.obc_fireplace_inserts_comments = form_data.get('obcFireplaceInserts', {}).get('comments', '')
        construction.obc_fireplace_inserts_code_compliance = form_data.get('obcFireplaceInserts', {}).get('codeCompliance', '')
        construction.obc_fireplace_inserts_photos = form_data.get('obcFireplaceInserts', {}).get('photos', [])

        # Cleanout
        construction.cleanout_condition = form_data.get('cleanout', {}).get('condition', '')
        construction.cleanout_comments = form_data.get('cleanout', {}).get('comments', '')
        construction.cleanout_code_compliance = form_data.get('cleanout', {}).get('codeCompliance', '')
        construction.cleanout_photos = form_data.get('cleanout', {}).get('photos', [])

        # Clearance from Combustible Materials
        construction.clearance_from_combustible_materials_condition = form_data.get('clearanceFromCombustibleMaterials', {}).get('condition', '')
        construction.clearance_from_combustible_materials_comments = form_data.get('clearanceFromCombustibleMaterials', {}).get('comments', '')
        construction.clearance_from_combustible_materials_code_compliance = form_data.get('clearanceFromCombustibleMaterials', {}).get('codeCompliance', '')
        construction.clearance_from_combustible_materials_photos = form_data.get('clearanceFromCombustibleMaterials', {}).get('photos', [])

        # Wall Thickness
        construction.wall_thickness_condition = form_data.get('wallThickness', {}).get('condition', '')
        construction.wall_thickness_comments = form_data.get('wallThickness', {}).get('comments', '')
        construction.wall_thickness_code_compliance = form_data.get('wallThickness', {}).get('codeCompliance', '')
        construction.wall_thickness_photos = form_data.get('wallThickness', {}).get('photos', [])

        db.session.commit()
        return jsonify(construction.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/masonry-fireplace-construction-2/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_masonry_fireplace_construction_2(inspection_id):
    """Delete pellet insert masonry fireplace construction 2 for an inspection."""
    try:
        construction = PelletInsertMasonryFireplaceConstruction2.query.filter_by(inspection_id=inspection_id).first()

        if not construction:
            return jsonify({'error': 'Pellet insert masonry fireplace construction 2 not found'}), 404

        db.session.delete(construction)
        db.session.commit()
        return jsonify({'message': 'Pellet insert masonry fireplace construction 2 deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Materials Clearances routes
@main.route('/api/pellet-insert/materials-clearances', methods=['POST'])
def create_pellet_insert_materials_clearances():
    """Create pellet insert materials clearances for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert materials clearances already exists
        existing_clearances = PelletInsertMaterialsClearances.query.filter_by(inspection_id=inspection_id).first()
        if existing_clearances:
            return jsonify({'error': 'Pellet insert materials clearances already exists for this inspection'}), 400

        # Create new pellet insert materials clearances
        clearances = PelletInsertMaterialsClearances(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Combustible Mantle
        clearances.combustible_mantle_required_value_uncertified = form_data.get('combustibleMantle', {}).get('requiredValueUncertified', '')
        clearances.combustible_mantle_required_value_certified = form_data.get('combustibleMantle', {}).get('requiredValueCertified', '')
        clearances.combustible_mantle_present_value = form_data.get('combustibleMantle', {}).get('presentValue', '')
        clearances.combustible_mantle_code_compliance = form_data.get('combustibleMantle', {}).get('codeCompliance', '')
        clearances.combustible_mantle_photos = form_data.get('combustibleMantle', {}).get('photos', [])

        # Top Trim Facing
        clearances.top_trim_facing_required_value_uncertified = form_data.get('topTrimFacing', {}).get('requiredValueUncertified', '')
        clearances.top_trim_facing_required_value_certified = form_data.get('topTrimFacing', {}).get('requiredValueCertified', '')
        clearances.top_trim_facing_present_value = form_data.get('topTrimFacing', {}).get('presentValue', '')
        clearances.top_trim_facing_code_compliance = form_data.get('topTrimFacing', {}).get('codeCompliance', '')
        clearances.top_trim_facing_photos = form_data.get('topTrimFacing', {}).get('photos', [])

        # Side Trim Facing Right
        clearances.side_trim_facing_right_required_value_uncertified = form_data.get('sideTrimFacingRight', {}).get('requiredValueUncertified', '')
        clearances.side_trim_facing_right_required_value_certified = form_data.get('sideTrimFacingRight', {}).get('requiredValueCertified', '')
        clearances.side_trim_facing_right_present_value = form_data.get('sideTrimFacingRight', {}).get('presentValue', '')
        clearances.side_trim_facing_right_code_compliance = form_data.get('sideTrimFacingRight', {}).get('codeCompliance', '')
        clearances.side_trim_facing_right_photos = form_data.get('sideTrimFacingRight', {}).get('photos', [])

        # Side Trim Facing Left
        clearances.side_trim_facing_left_required_value_uncertified = form_data.get('sideTrimFacingLeft', {}).get('requiredValueUncertified', '')
        clearances.side_trim_facing_left_required_value_certified = form_data.get('sideTrimFacingLeft', {}).get('requiredValueCertified', '')
        clearances.side_trim_facing_left_present_value = form_data.get('sideTrimFacingLeft', {}).get('presentValue', '')
        clearances.side_trim_facing_left_code_compliance = form_data.get('sideTrimFacingLeft', {}).get('codeCompliance', '')
        clearances.side_trim_facing_left_photos = form_data.get('sideTrimFacingLeft', {}).get('photos', [])

        # Combustible Side Wall
        clearances.combustible_side_wall_required_value_uncertified = form_data.get('combustibleSideWall', {}).get('requiredValueUncertified', '')
        clearances.combustible_side_wall_required_value_certified = form_data.get('combustibleSideWall', {}).get('requiredValueCertified', '')
        clearances.combustible_side_wall_present_value = form_data.get('combustibleSideWall', {}).get('presentValue', '')
        clearances.combustible_side_wall_code_compliance = form_data.get('combustibleSideWall', {}).get('codeCompliance', '')
        clearances.combustible_side_wall_photos = form_data.get('combustibleSideWall', {}).get('photos', [])

        # Ember Pad Material
        clearances.ember_pad_material_required_value_uncertified = form_data.get('emberPadMaterial', {}).get('requiredValueUncertified', '')
        clearances.ember_pad_material_required_value_certified = form_data.get('emberPadMaterial', {}).get('requiredValueCertified', '')
        clearances.ember_pad_material_present_value = form_data.get('emberPadMaterial', {}).get('presentValue', '')
        clearances.ember_pad_material_code_compliance = form_data.get('emberPadMaterial', {}).get('codeCompliance', '')
        clearances.ember_pad_material_photos = form_data.get('emberPadMaterial', {}).get('photos', [])

        db.session.add(clearances)
        db.session.commit()
        return jsonify(clearances.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/materials-clearances/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_materials_clearances(inspection_id):
    """Get pellet insert materials clearances for an inspection."""
    try:
        clearances = PelletInsertMaterialsClearances.query.filter_by(inspection_id=inspection_id).first()

        if not clearances:
            return jsonify({'error': 'Pellet insert materials clearances not found'}), 404

        return jsonify(clearances.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/materials-clearances/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_materials_clearances(inspection_id):
    """Update pellet insert materials clearances for an inspection."""
    try:
        data = request.get_json()

        clearances = PelletInsertMaterialsClearances.query.filter_by(inspection_id=inspection_id).first()

        if not clearances:
            return jsonify({'error': 'Pellet insert materials clearances not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        # Combustible Mantle
        clearances.combustible_mantle_required_value_uncertified = form_data.get('combustibleMantle', {}).get('requiredValueUncertified', '')
        clearances.combustible_mantle_required_value_certified = form_data.get('combustibleMantle', {}).get('requiredValueCertified', '')
        clearances.combustible_mantle_present_value = form_data.get('combustibleMantle', {}).get('presentValue', '')
        clearances.combustible_mantle_code_compliance = form_data.get('combustibleMantle', {}).get('codeCompliance', '')
        clearances.combustible_mantle_photos = form_data.get('combustibleMantle', {}).get('photos', [])

        # Top Trim Facing
        clearances.top_trim_facing_required_value_uncertified = form_data.get('topTrimFacing', {}).get('requiredValueUncertified', '')
        clearances.top_trim_facing_required_value_certified = form_data.get('topTrimFacing', {}).get('requiredValueCertified', '')
        clearances.top_trim_facing_present_value = form_data.get('topTrimFacing', {}).get('presentValue', '')
        clearances.top_trim_facing_code_compliance = form_data.get('topTrimFacing', {}).get('codeCompliance', '')
        clearances.top_trim_facing_photos = form_data.get('topTrimFacing', {}).get('photos', [])

        # Side Trim Facing Right
        clearances.side_trim_facing_right_required_value_uncertified = form_data.get('sideTrimFacingRight', {}).get('requiredValueUncertified', '')
        clearances.side_trim_facing_right_required_value_certified = form_data.get('sideTrimFacingRight', {}).get('requiredValueCertified', '')
        clearances.side_trim_facing_right_present_value = form_data.get('sideTrimFacingRight', {}).get('presentValue', '')
        clearances.side_trim_facing_right_code_compliance = form_data.get('sideTrimFacingRight', {}).get('codeCompliance', '')
        clearances.side_trim_facing_right_photos = form_data.get('sideTrimFacingRight', {}).get('photos', [])

        # Side Trim Facing Left
        clearances.side_trim_facing_left_required_value_uncertified = form_data.get('sideTrimFacingLeft', {}).get('requiredValueUncertified', '')
        clearances.side_trim_facing_left_required_value_certified = form_data.get('sideTrimFacingLeft', {}).get('requiredValueCertified', '')
        clearances.side_trim_facing_left_present_value = form_data.get('sideTrimFacingLeft', {}).get('presentValue', '')
        clearances.side_trim_facing_left_code_compliance = form_data.get('sideTrimFacingLeft', {}).get('codeCompliance', '')
        clearances.side_trim_facing_left_photos = form_data.get('sideTrimFacingLeft', {}).get('photos', [])

        # Combustible Side Wall
        clearances.combustible_side_wall_required_value_uncertified = form_data.get('combustibleSideWall', {}).get('requiredValueUncertified', '')
        clearances.combustible_side_wall_required_value_certified = form_data.get('combustibleSideWall', {}).get('requiredValueCertified', '')
        clearances.combustible_side_wall_present_value = form_data.get('combustibleSideWall', {}).get('presentValue', '')
        clearances.combustible_side_wall_code_compliance = form_data.get('combustibleSideWall', {}).get('codeCompliance', '')
        clearances.combustible_side_wall_photos = form_data.get('combustibleSideWall', {}).get('photos', [])

        # Ember Pad Material
        clearances.ember_pad_material_required_value_uncertified = form_data.get('emberPadMaterial', {}).get('requiredValueUncertified', '')
        clearances.ember_pad_material_required_value_certified = form_data.get('emberPadMaterial', {}).get('requiredValueCertified', '')
        clearances.ember_pad_material_present_value = form_data.get('emberPadMaterial', {}).get('presentValue', '')
        clearances.ember_pad_material_code_compliance = form_data.get('emberPadMaterial', {}).get('codeCompliance', '')
        clearances.ember_pad_material_photos = form_data.get('emberPadMaterial', {}).get('photos', [])

        db.session.commit()
        return jsonify(clearances.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/materials-clearances/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_materials_clearances(inspection_id):
    """Delete pellet insert materials clearances for an inspection."""
    try:
        clearances = PelletInsertMaterialsClearances.query.filter_by(inspection_id=inspection_id).first()

        if not clearances:
            return jsonify({'error': 'Pellet insert materials clearances not found'}), 404

        db.session.delete(clearances)
        db.session.commit()
        return jsonify({'message': 'Pellet insert materials clearances deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Pellet Insert Chimney Joints Liner Details routes
@main.route('/api/pellet-insert/chimney-joints-liner-details', methods=['POST'])
def create_pellet_insert_chimney_joints_liner_details():
    """Create pellet insert chimney joints liner details for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if pellet insert chimney joints liner details already exist
        existing_details = PelletInsertChimneyJointsLinerDetails.query.filter_by(inspection_id=inspection_id).first()
        if existing_details:
            return jsonify({'error': 'Pellet insert chimney joints liner details already exist for this inspection'}), 400

        # Create new pellet insert chimney joints liner details
        details = PelletInsertChimneyJointsLinerDetails(inspection_id=inspection_id)

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'jointsInChimneyLiners1' in form_data:
            section = form_data['jointsInChimneyLiners1']
            details.joints_in_chimney_liners_1_condition = section.get('condition', '')
            details.joints_in_chimney_liners_1_comments = section.get('comments', '')
            details.joints_in_chimney_liners_1_code_compliance = section.get('codeCompliance')
            details.joints_in_chimney_liners_1_photos = section.get('photos', [])

        if 'jointsInChimneyLiners2' in form_data:
            section = form_data['jointsInChimneyLiners2']
            details.joints_in_chimney_liners_2_condition = section.get('condition', '')
            details.joints_in_chimney_liners_2_comments = section.get('comments', '')
            details.joints_in_chimney_liners_2_code_compliance = section.get('codeCompliance')
            details.joints_in_chimney_liners_2_photos = section.get('photos', [])

        if 'installationOfChimneyLiners' in form_data:
            section = form_data['installationOfChimneyLiners']
            details.installation_of_chimney_liners_condition = section.get('condition', '')
            details.installation_of_chimney_liners_comments = section.get('comments', '')
            details.installation_of_chimney_liners_code_compliance = section.get('codeCompliance')
            details.installation_of_chimney_liners_photos = section.get('photos', [])

        if 'spacesBetweenLinersAndSurroundingMasonry' in form_data:
            section = form_data['spacesBetweenLinersAndSurroundingMasonry']
            details.spaces_between_liners_and_surrounding_masonry_condition = section.get('condition', '')
            details.spaces_between_liners_and_surrounding_masonry_comments = section.get('comments', '')
            details.spaces_between_liners_and_surrounding_masonry_code_compliance = section.get('codeCompliance')
            details.spaces_between_liners_and_surrounding_masonry_photos = section.get('photos', [])

        if 'mortarForChimneyLiners' in form_data:
            section = form_data['mortarForChimneyLiners']
            details.mortar_for_chimney_liners_condition = section.get('condition', '')
            details.mortar_for_chimney_liners_comments = section.get('comments', '')
            details.mortar_for_chimney_liners_code_compliance = section.get('codeCompliance')
            details.mortar_for_chimney_liners_photos = section.get('photos', [])

        if 'extensionOfChimneyLiners' in form_data:
            section = form_data['extensionOfChimneyLiners']
            details.extension_of_chimney_liners_condition = section.get('condition', '')
            details.extension_of_chimney_liners_comments = section.get('comments', '')
            details.extension_of_chimney_liners_code_compliance = section.get('codeCompliance')
            details.extension_of_chimney_liners_photos = section.get('photos', [])

        db.session.add(details)
        db.session.commit()
        return jsonify(details.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-joints-liner-details/<int:inspection_id>', methods=['GET'])
def get_pellet_insert_chimney_joints_liner_details(inspection_id):
    """Get pellet insert chimney joints liner details for an inspection."""
    try:
        details = PelletInsertChimneyJointsLinerDetails.query.filter_by(inspection_id=inspection_id).first()

        if not details:
            return jsonify({'error': 'Pellet insert chimney joints liner details not found'}), 404

        return jsonify(details.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-joints-liner-details/<int:inspection_id>', methods=['PUT'])
def update_pellet_insert_chimney_joints_liner_details(inspection_id):
    """Update pellet insert chimney joints liner details for an inspection."""
    try:
        data = request.get_json()

        details = PelletInsertChimneyJointsLinerDetails.query.filter_by(inspection_id=inspection_id).first()

        if not details:
            return jsonify({'error': 'Pellet insert chimney joints liner details not found'}), 404

        # Map frontend data to model fields
        form_data = data.get('formData', {})

        if 'jointsInChimneyLiners1' in form_data:
            section = form_data['jointsInChimneyLiners1']
            details.joints_in_chimney_liners_1_condition = section.get('condition', '')
            details.joints_in_chimney_liners_1_comments = section.get('comments', '')
            details.joints_in_chimney_liners_1_code_compliance = section.get('codeCompliance')
            details.joints_in_chimney_liners_1_photos = section.get('photos', [])

        if 'jointsInChimneyLiners2' in form_data:
            section = form_data['jointsInChimneyLiners2']
            details.joints_in_chimney_liners_2_condition = section.get('condition', '')
            details.joints_in_chimney_liners_2_comments = section.get('comments', '')
            details.joints_in_chimney_liners_2_code_compliance = section.get('codeCompliance')
            details.joints_in_chimney_liners_2_photos = section.get('photos', [])

        if 'installationOfChimneyLiners' in form_data:
            section = form_data['installationOfChimneyLiners']
            details.installation_of_chimney_liners_condition = section.get('condition', '')
            details.installation_of_chimney_liners_comments = section.get('comments', '')
            details.installation_of_chimney_liners_code_compliance = section.get('codeCompliance')
            details.installation_of_chimney_liners_photos = section.get('photos', [])

        if 'spacesBetweenLinersAndSurroundingMasonry' in form_data:
            section = form_data['spacesBetweenLinersAndSurroundingMasonry']
            details.spaces_between_liners_and_surrounding_masonry_condition = section.get('condition', '')
            details.spaces_between_liners_and_surrounding_masonry_comments = section.get('comments', '')
            details.spaces_between_liners_and_surrounding_masonry_code_compliance = section.get('codeCompliance')
            details.spaces_between_liners_and_surrounding_masonry_photos = section.get('photos', [])

        if 'mortarForChimneyLiners' in form_data:
            section = form_data['mortarForChimneyLiners']
            details.mortar_for_chimney_liners_condition = section.get('condition', '')
            details.mortar_for_chimney_liners_comments = section.get('comments', '')
            details.mortar_for_chimney_liners_code_compliance = section.get('codeCompliance')
            details.mortar_for_chimney_liners_photos = section.get('photos', [])

        if 'extensionOfChimneyLiners' in form_data:
            section = form_data['extensionOfChimneyLiners']
            details.extension_of_chimney_liners_condition = section.get('condition', '')
            details.extension_of_chimney_liners_comments = section.get('comments', '')
            details.extension_of_chimney_liners_code_compliance = section.get('codeCompliance')
            details.extension_of_chimney_liners_photos = section.get('photos', [])

        db.session.commit()
        return jsonify(details.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/pellet-insert/chimney-joints-liner-details/<int:inspection_id>', methods=['DELETE'])
def delete_pellet_insert_chimney_joints_liner_details(inspection_id):
    """Delete pellet insert chimney joints liner details for an inspection."""
    try:
        details = PelletInsertChimneyJointsLinerDetails.query.filter_by(inspection_id=inspection_id).first()

        if not details:
            return jsonify({'error': 'Pellet insert chimney joints liner details not found'}), 404

        db.session.delete(details)
        db.session.commit()
        return jsonify({'message': 'Pellet insert chimney joints liner details deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Chimney Specifications routes
@main.route('/api/masonry-chimney-specifications', methods=['POST'])
def create_masonry_chimney_specification():
    """Create masonry chimney specifications for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry chimney specifications already exist
        existing_spec = MasonryChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry chimney specifications already exist for this inspection'}), 400

        # Create new masonry chimney specifications
        spec = MasonryChimneySpecification(inspection_id=inspection_id)

        # Map frontend data to model fields
        spec.chimney_constructed_in_building = data.get('chimneyConstructedInBuilding', '')
        spec.approximate_age = data.get('approximateAge', '')
        spec.shell = data.get('shell', '')
        spec.rain_cap = data.get('rainCap', '')
        spec.number_of_flues = data.get('numberOfFlues', '')
        spec.size_of_flue = data.get('sizeOfFlue', '')
        spec.material_of_flue = data.get('materialOfFlue', '')
        spec.chimney_location = data.get('chimneyLocation', '')
        spec.height_from_firebox_floor = data.get('heightFromFireboxFloor', '')
        spec.chimney_lined_with = data.get('chimneyLinedWith', '')
        spec.chimney_installed_by = data.get('chimneyInstalledBy', '')
        spec.is_unknown_installer = data.get('isUnknownInstaller', False)
        spec.installation_date = data.get('date', '')
        spec.comments = data.get('comments', '')
        spec.suitable = data.get('suitable', '')

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-specifications/<int:inspection_id>', methods=['GET'])
def get_masonry_chimney_specification(inspection_id):
    """Get masonry chimney specifications for an inspection."""
    try:
        spec = MasonryChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry chimney specifications not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-specifications/<int:inspection_id>', methods=['PUT'])
def update_masonry_chimney_specification(inspection_id):
    """Update masonry chimney specifications for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryChimneySpecification.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry chimney specifications not found'}), 404

        # Update model fields
        spec.chimney_constructed_in_building = data.get('chimneyConstructedInBuilding', spec.chimney_constructed_in_building)
        spec.approximate_age = data.get('approximateAge', spec.approximate_age)
        spec.shell = data.get('shell', spec.shell)
        spec.rain_cap = data.get('rainCap', spec.rain_cap)
        spec.number_of_flues = data.get('numberOfFlues', spec.number_of_flues)
        spec.size_of_flue = data.get('sizeOfFlue', spec.size_of_flue)
        spec.material_of_flue = data.get('materialOfFlue', spec.material_of_flue)
        spec.chimney_location = data.get('chimneyLocation', spec.chimney_location)
        spec.height_from_firebox_floor = data.get('heightFromFireboxFloor', spec.height_from_firebox_floor)
        spec.chimney_lined_with = data.get('chimneyLinedWith', spec.chimney_lined_with)
        spec.chimney_installed_by = data.get('chimneyInstalledBy', spec.chimney_installed_by)
        spec.is_unknown_installer = data.get('isUnknownInstaller', spec.is_unknown_installer)
        spec.installation_date = data.get('date', spec.installation_date)
        spec.comments = data.get('comments', spec.comments)
        spec.suitable = data.get('suitable', spec.suitable)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-specifications/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_chimney_specification(inspection_id):
    """Delete masonry chimney specifications for an inspection."""
    try:
        spec = MasonryChimneySpecification.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry chimney specifications not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry chimney specifications deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Fireplace Specifications routes
@main.route('/api/masonry-fireplace-specifications', methods=['POST'])
def create_masonry_fireplace_specification():
    """Create masonry fireplace specifications for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry fireplace specifications already exist
        existing_spec = MasonryFireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry fireplace specifications already exist for this inspection'}), 400

        # Create new masonry fireplace specifications
        spec = MasonryFireplaceSpecification(inspection_id=inspection_id)

        # Map frontend data to model fields
        spec.inspection_discussed = data.get('inspectionDiscussed', '')
        spec.building_permits_available = data.get('buildingPermitsAvailable', '')
        spec.time_of_day = data.get('timeOfDay', '')
        spec.weather_conditions = data.get('weatherConditions', '')
        spec.roofing_type = data.get('roofingType', '')
        spec.roof_accessed = data.get('roofAccessed', '')
        spec.attic_accessed = data.get('atticAccessed', '')
        spec.fireplace_constructed_in_building = data.get('fireplaceConstructedInBuilding', '')
        spec.approximate_age = data.get('approximateAge', '')
        spec.fireplace_location = data.get('fireplaceLocation', '')
        spec.fireplace_type = data.get('fireplaceType', '')
        spec.certification_standard = data.get('certificationStandard', '')
        spec.listing_agency = data.get('listingAgency', '')
        spec.fireplace_location_in_building = data.get('fireplaceLocation2', '')
        spec.other_location = data.get('otherLocation', '')
        spec.fan_blower_attached = data.get('fanBlowerAttached', '')
        spec.installed_in = data.get('installedIn', '')
        spec.fireplace_installed_by = data.get('fireplaceInstalledBy', '')
        spec.is_unknown_installer = data.get('isUnknownInstaller', False)
        spec.installation_date = data.get('date', '')
        spec.comments = data.get('comments', '')

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-specifications/<int:inspection_id>', methods=['GET'])
def get_masonry_fireplace_specification(inspection_id):
    """Get masonry fireplace specifications for an inspection."""
    try:
        spec = MasonryFireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry fireplace specifications not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-specifications/<int:inspection_id>', methods=['PUT'])
def update_masonry_fireplace_specification(inspection_id):
    """Update masonry fireplace specifications for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryFireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry fireplace specifications not found'}), 404

        # Update model fields
        spec.inspection_discussed = data.get('inspectionDiscussed', spec.inspection_discussed)
        spec.building_permits_available = data.get('buildingPermitsAvailable', spec.building_permits_available)
        spec.time_of_day = data.get('timeOfDay', spec.time_of_day)
        spec.weather_conditions = data.get('weatherConditions', spec.weather_conditions)
        spec.roofing_type = data.get('roofingType', spec.roofing_type)
        spec.roof_accessed = data.get('roofAccessed', spec.roof_accessed)
        spec.attic_accessed = data.get('atticAccessed', spec.attic_accessed)
        spec.fireplace_constructed_in_building = data.get('fireplaceConstructedInBuilding', spec.fireplace_constructed_in_building)
        spec.approximate_age = data.get('approximateAge', spec.approximate_age)
        spec.fireplace_location = data.get('fireplaceLocation', spec.fireplace_location)
        spec.fireplace_type = data.get('fireplaceType', spec.fireplace_type)
        spec.certification_standard = data.get('certificationStandard', spec.certification_standard)
        spec.listing_agency = data.get('listingAgency', spec.listing_agency)
        spec.fireplace_location_in_building = data.get('fireplaceLocation2', spec.fireplace_location_in_building)
        spec.other_location = data.get('otherLocation', spec.other_location)
        spec.fan_blower_attached = data.get('fanBlowerAttached', spec.fan_blower_attached)
        spec.installed_in = data.get('installedIn', spec.installed_in)
        spec.fireplace_installed_by = data.get('fireplaceInstalledBy', spec.fireplace_installed_by)
        spec.is_unknown_installer = data.get('isUnknownInstaller', spec.is_unknown_installer)
        spec.installation_date = data.get('date', spec.installation_date)
        spec.comments = data.get('comments', spec.comments)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-specifications/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_fireplace_specification(inspection_id):
    """Delete masonry fireplace specifications for an inspection."""
    try:
        spec = MasonryFireplaceSpecification.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry fireplace specifications not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry fireplace specifications deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Fireplace Construction Details routes
@main.route('/api/masonry-fireplace-construction-details', methods=['POST'])
def create_masonry_fireplace_construction_details():
    """Create masonry fireplace construction details for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry fireplace construction details already exist
        existing_spec = MasonryFireplaceConstructionDetails.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry fireplace construction details already exist for this inspection'}), 400

        # Create new masonry fireplace construction details
        spec = MasonryFireplaceConstructionDetails(inspection_id=inspection_id)

        # Map frontend data to model fields
        spec.height = data.get('height', '')
        spec.width = data.get('width', '')
        spec.total = data.get('total', '')

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'fireplaceChimneys' in form_data:
            spec.fireplace_chimneys_condition = form_data['fireplaceChimneys'].get('condition', '')
            spec.fireplace_chimneys_comments = form_data['fireplaceChimneys'].get('comments', '')
            spec.fireplace_chimneys_code_compliance = form_data['fireplaceChimneys'].get('codeCompliance', '')
            spec.fireplace_chimneys_photos = form_data['fireplaceChimneys'].get('photos', [])

        if 'lintelsArches' in form_data:
            spec.lintels_arches_condition = form_data['lintelsArches'].get('condition', '')
            spec.lintels_arches_comments = form_data['lintelsArches'].get('comments', '')
            spec.lintels_arches_code_compliance = form_data['lintelsArches'].get('codeCompliance', '')
            spec.lintels_arches_photos = form_data['lintelsArches'].get('photos', [])

        if 'obcLintelsArches' in form_data:
            spec.obc_lintels_arches_condition = form_data['obcLintelsArches'].get('condition', '')
            spec.obc_lintels_arches_comments = form_data['obcLintelsArches'].get('comments', '')
            spec.obc_lintels_arches_code_compliance = form_data['obcLintelsArches'].get('codeCompliance', '')
            spec.obc_lintels_arches_photos = form_data['obcLintelsArches'].get('photos', [])

        if 'corbelling' in form_data:
            spec.corbelling_condition = form_data['corbelling'].get('condition', '')
            spec.corbelling_comments = form_data['corbelling'].get('comments', '')
            spec.corbelling_code_compliance = form_data['corbelling'].get('codeCompliance', '')
            spec.corbelling_photos = form_data['corbelling'].get('photos', [])

        if 'combustionAir' in form_data:
            spec.combustion_air_condition = form_data['combustionAir'].get('condition', '')
            spec.combustion_air_comments = form_data['combustionAir'].get('comments', '')
            spec.combustion_air_code_compliance = form_data['combustionAir'].get('codeCompliance', '')
            spec.combustion_air_photos = form_data['combustionAir'].get('photos', [])

        if 'nbcCombustionAir' in form_data:
            spec.nbc_combustion_air_condition = form_data['nbcCombustionAir'].get('condition', '')
            spec.nbc_combustion_air_comments = form_data['nbcCombustionAir'].get('comments', '')
            spec.nbc_combustion_air_code_compliance = form_data['nbcCombustionAir'].get('codeCompliance', '')
            spec.nbc_combustion_air_photos = form_data['nbcCombustionAir'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-construction-details/<int:inspection_id>', methods=['GET'])
def get_masonry_fireplace_construction_details(inspection_id):
    """Get masonry fireplace construction details for an inspection."""
    try:
        spec = MasonryFireplaceConstructionDetails.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry fireplace construction details not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-construction-details/<int:inspection_id>', methods=['PUT'])
def update_masonry_fireplace_construction_details(inspection_id):
    """Update masonry fireplace construction details for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryFireplaceConstructionDetails.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry fireplace construction details not found'}), 404

        # Update model fields
        spec.height = data.get('height', spec.height)
        spec.width = data.get('width', spec.width)
        spec.total = data.get('total', spec.total)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'fireplaceChimneys' in form_data:
            spec.fireplace_chimneys_condition = form_data['fireplaceChimneys'].get('condition', spec.fireplace_chimneys_condition)
            spec.fireplace_chimneys_comments = form_data['fireplaceChimneys'].get('comments', spec.fireplace_chimneys_comments)
            spec.fireplace_chimneys_code_compliance = form_data['fireplaceChimneys'].get('codeCompliance', spec.fireplace_chimneys_code_compliance)
            spec.fireplace_chimneys_photos = form_data['fireplaceChimneys'].get('photos', spec.fireplace_chimneys_photos)

        if 'lintelsArches' in form_data:
            spec.lintels_arches_condition = form_data['lintelsArches'].get('condition', spec.lintels_arches_condition)
            spec.lintels_arches_comments = form_data['lintelsArches'].get('comments', spec.lintels_arches_comments)
            spec.lintels_arches_code_compliance = form_data['lintelsArches'].get('codeCompliance', spec.lintels_arches_code_compliance)
            spec.lintels_arches_photos = form_data['lintelsArches'].get('photos', spec.lintels_arches_photos)

        if 'obcLintelsArches' in form_data:
            spec.obc_lintels_arches_condition = form_data['obcLintelsArches'].get('condition', spec.obc_lintels_arches_condition)
            spec.obc_lintels_arches_comments = form_data['obcLintelsArches'].get('comments', spec.obc_lintels_arches_comments)
            spec.obc_lintels_arches_code_compliance = form_data['obcLintelsArches'].get('codeCompliance', spec.obc_lintels_arches_code_compliance)
            spec.obc_lintels_arches_photos = form_data['obcLintelsArches'].get('photos', spec.obc_lintels_arches_photos)

        if 'corbelling' in form_data:
            spec.corbelling_condition = form_data['corbelling'].get('condition', spec.corbelling_condition)
            spec.corbelling_comments = form_data['corbelling'].get('comments', spec.corbelling_comments)
            spec.corbelling_code_compliance = form_data['corbelling'].get('codeCompliance', spec.corbelling_code_compliance)
            spec.corbelling_photos = form_data['corbelling'].get('photos', spec.corbelling_photos)

        if 'combustionAir' in form_data:
            spec.combustion_air_condition = form_data['combustionAir'].get('condition', spec.combustion_air_condition)
            spec.combustion_air_comments = form_data['combustionAir'].get('comments', spec.combustion_air_comments)
            spec.combustion_air_code_compliance = form_data['combustionAir'].get('codeCompliance', spec.combustion_air_code_compliance)
            spec.combustion_air_photos = form_data['combustionAir'].get('photos', spec.combustion_air_photos)

        if 'nbcCombustionAir' in form_data:
            spec.nbc_combustion_air_condition = form_data['nbcCombustionAir'].get('condition', spec.nbc_combustion_air_condition)
            spec.nbc_combustion_air_comments = form_data['nbcCombustionAir'].get('comments', spec.nbc_combustion_air_comments)
            spec.nbc_combustion_air_code_compliance = form_data['nbcCombustionAir'].get('codeCompliance', spec.nbc_combustion_air_code_compliance)
            spec.nbc_combustion_air_photos = form_data['nbcCombustionAir'].get('photos', spec.nbc_combustion_air_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-construction-details/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_fireplace_construction_details(inspection_id):
    """Delete masonry fireplace construction details for an inspection."""
    try:
        spec = MasonryFireplaceConstructionDetails.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry fireplace construction details not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry fireplace construction details deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Combustion Air Requirements routes
@main.route('/api/masonry-combustion-air-requirements', methods=['POST'])
def create_masonry_combustion_air_requirements():
    """Create masonry combustion air requirements for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry combustion air requirements already exist
        existing_spec = MasonryCombustionAirRequirements.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry combustion air requirements already exist for this inspection'}), 400

        # Create new masonry combustion air requirements
        spec = MasonryCombustionAirRequirements(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'obcCombustionAir' in form_data:
            spec.obc_combustion_air_condition = form_data['obcCombustionAir'].get('condition', '')
            spec.obc_combustion_air_comments = form_data['obcCombustionAir'].get('comments', '')
            spec.obc_combustion_air_code_compliance = form_data['obcCombustionAir'].get('codeCompliance', '')
            spec.obc_combustion_air_photos = form_data['obcCombustionAir'].get('photos', [])

        if 'brickSteelLiners' in form_data:
            spec.brick_steel_liners_condition = form_data['brickSteelLiners'].get('condition', '')
            spec.brick_steel_liners_comments = form_data['brickSteelLiners'].get('comments', '')
            spec.brick_steel_liners_code_compliance = form_data['brickSteelLiners'].get('codeCompliance', '')
            spec.brick_steel_liners_photos = form_data['brickSteelLiners'].get('photos', [])

        if 'firebrickLiners1' in form_data:
            spec.firebrick_liners_1_condition = form_data['firebrickLiners1'].get('condition', '')
            spec.firebrick_liners_1_comments = form_data['firebrickLiners1'].get('comments', '')
            spec.firebrick_liners_1_code_compliance = form_data['firebrickLiners1'].get('codeCompliance', '')
            spec.firebrick_liners_1_photos = form_data['firebrickLiners1'].get('photos', [])

        if 'firebrickLiners2' in form_data:
            spec.firebrick_liners_2_condition = form_data['firebrickLiners2'].get('condition', '')
            spec.firebrick_liners_2_comments = form_data['firebrickLiners2'].get('comments', '')
            spec.firebrick_liners_2_code_compliance = form_data['firebrickLiners2'].get('codeCompliance', '')
            spec.firebrick_liners_2_photos = form_data['firebrickLiners2'].get('photos', [])

        if 'firebrickLiners3' in form_data:
            spec.firebrick_liners_3_condition = form_data['firebrickLiners3'].get('condition', '')
            spec.firebrick_liners_3_comments = form_data['firebrickLiners3'].get('comments', '')
            spec.firebrick_liners_3_code_compliance = form_data['firebrickLiners3'].get('codeCompliance', '')
            spec.firebrick_liners_3_photos = form_data['firebrickLiners3'].get('photos', [])

        if 'steelLiners' in form_data:
            spec.steel_liners_condition = form_data['steelLiners'].get('condition', '')
            spec.steel_liners_comments = form_data['steelLiners'].get('comments', '')
            spec.steel_liners_code_compliance = form_data['steelLiners'].get('codeCompliance', '')
            spec.steel_liners_photos = form_data['steelLiners'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-combustion-air-requirements/<int:inspection_id>', methods=['GET'])
def get_masonry_combustion_air_requirements(inspection_id):
    """Get masonry combustion air requirements for an inspection."""
    try:
        spec = MasonryCombustionAirRequirements.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry combustion air requirements not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-combustion-air-requirements/<int:inspection_id>', methods=['PUT'])
def update_masonry_combustion_air_requirements(inspection_id):
    """Update masonry combustion air requirements for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryCombustionAirRequirements.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry combustion air requirements not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'obcCombustionAir' in form_data:
            spec.obc_combustion_air_condition = form_data['obcCombustionAir'].get('condition', spec.obc_combustion_air_condition)
            spec.obc_combustion_air_comments = form_data['obcCombustionAir'].get('comments', spec.obc_combustion_air_comments)
            spec.obc_combustion_air_code_compliance = form_data['obcCombustionAir'].get('codeCompliance', spec.obc_combustion_air_code_compliance)
            spec.obc_combustion_air_photos = form_data['obcCombustionAir'].get('photos', spec.obc_combustion_air_photos)

        if 'brickSteelLiners' in form_data:
            spec.brick_steel_liners_condition = form_data['brickSteelLiners'].get('condition', spec.brick_steel_liners_condition)
            spec.brick_steel_liners_comments = form_data['brickSteelLiners'].get('comments', spec.brick_steel_liners_comments)
            spec.brick_steel_liners_code_compliance = form_data['brickSteelLiners'].get('codeCompliance', spec.brick_steel_liners_code_compliance)
            spec.brick_steel_liners_photos = form_data['brickSteelLiners'].get('photos', spec.brick_steel_liners_photos)

        if 'firebrickLiners1' in form_data:
            spec.firebrick_liners_1_condition = form_data['firebrickLiners1'].get('condition', spec.firebrick_liners_1_condition)
            spec.firebrick_liners_1_comments = form_data['firebrickLiners1'].get('comments', spec.firebrick_liners_1_comments)
            spec.firebrick_liners_1_code_compliance = form_data['firebrickLiners1'].get('codeCompliance', spec.firebrick_liners_1_code_compliance)
            spec.firebrick_liners_1_photos = form_data['firebrickLiners1'].get('photos', spec.firebrick_liners_1_photos)

        if 'firebrickLiners2' in form_data:
            spec.firebrick_liners_2_condition = form_data['firebrickLiners2'].get('condition', spec.firebrick_liners_2_condition)
            spec.firebrick_liners_2_comments = form_data['firebrickLiners2'].get('comments', spec.firebrick_liners_2_comments)
            spec.firebrick_liners_2_code_compliance = form_data['firebrickLiners2'].get('codeCompliance', spec.firebrick_liners_2_code_compliance)
            spec.firebrick_liners_2_photos = form_data['firebrickLiners2'].get('photos', spec.firebrick_liners_2_photos)

        if 'firebrickLiners3' in form_data:
            spec.firebrick_liners_3_condition = form_data['firebrickLiners3'].get('condition', spec.firebrick_liners_3_condition)
            spec.firebrick_liners_3_comments = form_data['firebrickLiners3'].get('comments', spec.firebrick_liners_3_comments)
            spec.firebrick_liners_3_code_compliance = form_data['firebrickLiners3'].get('codeCompliance', spec.firebrick_liners_3_code_compliance)
            spec.firebrick_liners_3_photos = form_data['firebrickLiners3'].get('photos', spec.firebrick_liners_3_photos)

        if 'steelLiners' in form_data:
            spec.steel_liners_condition = form_data['steelLiners'].get('condition', spec.steel_liners_condition)
            spec.steel_liners_comments = form_data['steelLiners'].get('comments', spec.steel_liners_comments)
            spec.steel_liners_code_compliance = form_data['steelLiners'].get('codeCompliance', spec.steel_liners_code_compliance)
            spec.steel_liners_photos = form_data['steelLiners'].get('photos', spec.steel_liners_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-combustion-air-requirements/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_combustion_air_requirements(inspection_id):
    """Delete masonry combustion air requirements for an inspection."""
    try:
        spec = MasonryCombustionAirRequirements.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry combustion air requirements not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry combustion air requirements deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Chimney Structure routes
@main.route('/api/masonry-chimney-structure', methods=['POST'])
def create_masonry_chimney_structure():
    """Create masonry chimney structure for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry chimney structure already exists
        existing_spec = MasonryChimneyStructure.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry chimney structure already exists for this inspection'}), 400

        # Create new masonry chimney structure
        spec = MasonryChimneyStructure(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'thicknessWalls1' in form_data:
            spec.thickness_walls_1_condition = form_data['thicknessWalls1'].get('condition', '')
            spec.thickness_walls_1_comments = form_data['thicknessWalls1'].get('comments', '')
            spec.thickness_walls_1_code_compliance = form_data['thicknessWalls1'].get('codeCompliance', '')
            spec.thickness_walls_1_photos = form_data['thicknessWalls1'].get('photos', [])

        if 'thicknessWalls2' in form_data:
            spec.thickness_walls_2_condition = form_data['thicknessWalls2'].get('condition', '')
            spec.thickness_walls_2_comments = form_data['thicknessWalls2'].get('comments', '')
            spec.thickness_walls_2_code_compliance = form_data['thicknessWalls2'].get('codeCompliance', '')
            spec.thickness_walls_2_photos = form_data['thicknessWalls2'].get('photos', [])

        if 'fireChamberDimensions' in form_data:
            spec.fire_chamber_dimensions_condition = form_data['fireChamberDimensions'].get('condition', '')
            spec.fire_chamber_dimensions_comments = form_data['fireChamberDimensions'].get('comments', '')
            spec.fire_chamber_dimensions_code_compliance = form_data['fireChamberDimensions'].get('codeCompliance', '')
            spec.fire_chamber_dimensions_photos = form_data['fireChamberDimensions'].get('photos', [])

        if 'hearthExtension1' in form_data:
            spec.hearth_extension_1_condition = form_data['hearthExtension1'].get('condition', '')
            spec.hearth_extension_1_comments = form_data['hearthExtension1'].get('comments', '')
            spec.hearth_extension_1_code_compliance = form_data['hearthExtension1'].get('codeCompliance', '')
            spec.hearth_extension_1_photos = form_data['hearthExtension1'].get('photos', [])

        if 'hearthExtension2' in form_data:
            spec.hearth_extension_2_condition = form_data['hearthExtension2'].get('condition', '')
            spec.hearth_extension_2_comments = form_data['hearthExtension2'].get('comments', '')
            spec.hearth_extension_2_code_compliance = form_data['hearthExtension2'].get('codeCompliance', '')
            spec.hearth_extension_2_photos = form_data['hearthExtension2'].get('photos', [])

        if 'supportOfHearth' in form_data:
            spec.support_of_hearth_condition = form_data['supportOfHearth'].get('condition', '')
            spec.support_of_hearth_comments = form_data['supportOfHearth'].get('comments', '')
            spec.support_of_hearth_code_compliance = form_data['supportOfHearth'].get('codeCompliance', '')
            spec.support_of_hearth_photos = form_data['supportOfHearth'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-structure/<int:inspection_id>', methods=['GET'])
def get_masonry_chimney_structure(inspection_id):
    """Get masonry chimney structure for an inspection."""
    try:
        spec = MasonryChimneyStructure.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry chimney structure not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-structure/<int:inspection_id>', methods=['PUT'])
def update_masonry_chimney_structure(inspection_id):
    """Update masonry chimney structure for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryChimneyStructure.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry chimney structure not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'thicknessWalls1' in form_data:
            spec.thickness_walls_1_condition = form_data['thicknessWalls1'].get('condition', spec.thickness_walls_1_condition)
            spec.thickness_walls_1_comments = form_data['thicknessWalls1'].get('comments', spec.thickness_walls_1_comments)
            spec.thickness_walls_1_code_compliance = form_data['thicknessWalls1'].get('codeCompliance', spec.thickness_walls_1_code_compliance)
            spec.thickness_walls_1_photos = form_data['thicknessWalls1'].get('photos', spec.thickness_walls_1_photos)

        if 'thicknessWalls2' in form_data:
            spec.thickness_walls_2_condition = form_data['thicknessWalls2'].get('condition', spec.thickness_walls_2_condition)
            spec.thickness_walls_2_comments = form_data['thicknessWalls2'].get('comments', spec.thickness_walls_2_comments)
            spec.thickness_walls_2_code_compliance = form_data['thicknessWalls2'].get('codeCompliance', spec.thickness_walls_2_code_compliance)
            spec.thickness_walls_2_photos = form_data['thicknessWalls2'].get('photos', spec.thickness_walls_2_photos)

        if 'fireChamberDimensions' in form_data:
            spec.fire_chamber_dimensions_condition = form_data['fireChamberDimensions'].get('condition', spec.fire_chamber_dimensions_condition)
            spec.fire_chamber_dimensions_comments = form_data['fireChamberDimensions'].get('comments', spec.fire_chamber_dimensions_comments)
            spec.fire_chamber_dimensions_code_compliance = form_data['fireChamberDimensions'].get('codeCompliance', spec.fire_chamber_dimensions_code_compliance)
            spec.fire_chamber_dimensions_photos = form_data['fireChamberDimensions'].get('photos', spec.fire_chamber_dimensions_photos)

        if 'hearthExtension1' in form_data:
            spec.hearth_extension_1_condition = form_data['hearthExtension1'].get('condition', spec.hearth_extension_1_condition)
            spec.hearth_extension_1_comments = form_data['hearthExtension1'].get('comments', spec.hearth_extension_1_comments)
            spec.hearth_extension_1_code_compliance = form_data['hearthExtension1'].get('codeCompliance', spec.hearth_extension_1_code_compliance)
            spec.hearth_extension_1_photos = form_data['hearthExtension1'].get('photos', spec.hearth_extension_1_photos)

        if 'hearthExtension2' in form_data:
            spec.hearth_extension_2_condition = form_data['hearthExtension2'].get('condition', spec.hearth_extension_2_condition)
            spec.hearth_extension_2_comments = form_data['hearthExtension2'].get('comments', spec.hearth_extension_2_comments)
            spec.hearth_extension_2_code_compliance = form_data['hearthExtension2'].get('codeCompliance', spec.hearth_extension_2_code_compliance)
            spec.hearth_extension_2_photos = form_data['hearthExtension2'].get('photos', spec.hearth_extension_2_photos)

        if 'supportOfHearth' in form_data:
            spec.support_of_hearth_condition = form_data['supportOfHearth'].get('condition', spec.support_of_hearth_condition)
            spec.support_of_hearth_comments = form_data['supportOfHearth'].get('comments', spec.support_of_hearth_comments)
            spec.support_of_hearth_code_compliance = form_data['supportOfHearth'].get('codeCompliance', spec.support_of_hearth_code_compliance)
            spec.support_of_hearth_photos = form_data['supportOfHearth'].get('photos', spec.support_of_hearth_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-structure/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_chimney_structure(inspection_id):
    """Delete masonry chimney structure for an inspection."""
    try:
        spec = MasonryChimneyStructure.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry chimney structure not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry chimney structure deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Hearth Construction routes
@main.route('/api/masonry-hearth-construction', methods=['POST'])
def create_masonry_hearth_construction():
    """Create masonry hearth construction for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry hearth construction already exists
        existing_spec = MasonryHearthConstruction.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry hearth construction already exists for this inspection'}), 400

        # Create new masonry hearth construction
        spec = MasonryHearthConstruction(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'supportOfHearth' in form_data:
            spec.support_of_hearth_condition = form_data['supportOfHearth'].get('condition', '')
            spec.support_of_hearth_comments = form_data['supportOfHearth'].get('comments', '')
            spec.support_of_hearth_code_compliance = form_data['supportOfHearth'].get('codeCompliance', '')
            spec.support_of_hearth_photos = form_data['supportOfHearth'].get('photos', [])

        if 'requiredDamperSize' in form_data:
            spec.required_damper_size_condition = form_data['requiredDamperSize'].get('condition', '')
            spec.required_damper_size_comments = form_data['requiredDamperSize'].get('comments', '')
            spec.required_damper_size_code_compliance = form_data['requiredDamperSize'].get('codeCompliance', '')
            spec.required_damper_size_photos = form_data['requiredDamperSize'].get('photos', [])

        if 'slopeOfSmokeChamber' in form_data:
            spec.slope_of_smoke_chamber_condition = form_data['slopeOfSmokeChamber'].get('condition', '')
            spec.slope_of_smoke_chamber_comments = form_data['slopeOfSmokeChamber'].get('comments', '')
            spec.slope_of_smoke_chamber_code_compliance = form_data['slopeOfSmokeChamber'].get('codeCompliance', '')
            spec.slope_of_smoke_chamber_photos = form_data['slopeOfSmokeChamber'].get('photos', [])

        if 'wallThickness' in form_data:
            spec.wall_thickness_condition = form_data['wallThickness'].get('condition', '')
            spec.wall_thickness_comments = form_data['wallThickness'].get('comments', '')
            spec.wall_thickness_code_compliance = form_data['wallThickness'].get('codeCompliance', '')
            spec.wall_thickness_photos = form_data['wallThickness'].get('photos', [])

        if 'clearanceToFireplaceOpening' in form_data:
            spec.clearance_to_fireplace_opening_condition = form_data['clearanceToFireplaceOpening'].get('condition', '')
            spec.clearance_to_fireplace_opening_comments = form_data['clearanceToFireplaceOpening'].get('comments', '')
            spec.clearance_to_fireplace_opening_code_compliance = form_data['clearanceToFireplaceOpening'].get('codeCompliance', '')
            spec.clearance_to_fireplace_opening_photos = form_data['clearanceToFireplaceOpening'].get('photos', [])

        if 'metalExposedToInterior' in form_data:
            spec.metal_exposed_to_interior_condition = form_data['metalExposedToInterior'].get('condition', '')
            spec.metal_exposed_to_interior_comments = form_data['metalExposedToInterior'].get('comments', '')
            spec.metal_exposed_to_interior_code_compliance = form_data['metalExposedToInterior'].get('codeCompliance', '')
            spec.metal_exposed_to_interior_photos = form_data['metalExposedToInterior'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-hearth-construction/<int:inspection_id>', methods=['GET'])
def get_masonry_hearth_construction(inspection_id):
    """Get masonry hearth construction for an inspection."""
    try:
        spec = MasonryHearthConstruction.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry hearth construction not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-hearth-construction/<int:inspection_id>', methods=['PUT'])
def update_masonry_hearth_construction(inspection_id):
    """Update masonry hearth construction for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryHearthConstruction.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry hearth construction not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'supportOfHearth' in form_data:
            spec.support_of_hearth_condition = form_data['supportOfHearth'].get('condition', spec.support_of_hearth_condition)
            spec.support_of_hearth_comments = form_data['supportOfHearth'].get('comments', spec.support_of_hearth_comments)
            spec.support_of_hearth_code_compliance = form_data['supportOfHearth'].get('codeCompliance', spec.support_of_hearth_code_compliance)
            spec.support_of_hearth_photos = form_data['supportOfHearth'].get('photos', spec.support_of_hearth_photos)

        if 'requiredDamperSize' in form_data:
            spec.required_damper_size_condition = form_data['requiredDamperSize'].get('condition', spec.required_damper_size_condition)
            spec.required_damper_size_comments = form_data['requiredDamperSize'].get('comments', spec.required_damper_size_comments)
            spec.required_damper_size_code_compliance = form_data['requiredDamperSize'].get('codeCompliance', spec.required_damper_size_code_compliance)
            spec.required_damper_size_photos = form_data['requiredDamperSize'].get('photos', spec.required_damper_size_photos)

        if 'slopeOfSmokeChamber' in form_data:
            spec.slope_of_smoke_chamber_condition = form_data['slopeOfSmokeChamber'].get('condition', spec.slope_of_smoke_chamber_condition)
            spec.slope_of_smoke_chamber_comments = form_data['slopeOfSmokeChamber'].get('comments', spec.slope_of_smoke_chamber_comments)
            spec.slope_of_smoke_chamber_code_compliance = form_data['slopeOfSmokeChamber'].get('codeCompliance', spec.slope_of_smoke_chamber_code_compliance)
            spec.slope_of_smoke_chamber_photos = form_data['slopeOfSmokeChamber'].get('photos', spec.slope_of_smoke_chamber_photos)

        if 'wallThickness' in form_data:
            spec.wall_thickness_condition = form_data['wallThickness'].get('condition', spec.wall_thickness_condition)
            spec.wall_thickness_comments = form_data['wallThickness'].get('comments', spec.wall_thickness_comments)
            spec.wall_thickness_code_compliance = form_data['wallThickness'].get('codeCompliance', spec.wall_thickness_code_compliance)
            spec.wall_thickness_photos = form_data['wallThickness'].get('photos', spec.wall_thickness_photos)

        if 'clearanceToFireplaceOpening' in form_data:
            spec.clearance_to_fireplace_opening_condition = form_data['clearanceToFireplaceOpening'].get('condition', spec.clearance_to_fireplace_opening_condition)
            spec.clearance_to_fireplace_opening_comments = form_data['clearanceToFireplaceOpening'].get('comments', spec.clearance_to_fireplace_opening_comments)
            spec.clearance_to_fireplace_opening_code_compliance = form_data['clearanceToFireplaceOpening'].get('codeCompliance', spec.clearance_to_fireplace_opening_code_compliance)
            spec.clearance_to_fireplace_opening_photos = form_data['clearanceToFireplaceOpening'].get('photos', spec.clearance_to_fireplace_opening_photos)

        if 'metalExposedToInterior' in form_data:
            spec.metal_exposed_to_interior_condition = form_data['metalExposedToInterior'].get('condition', spec.metal_exposed_to_interior_condition)
            spec.metal_exposed_to_interior_comments = form_data['metalExposedToInterior'].get('comments', spec.metal_exposed_to_interior_comments)
            spec.metal_exposed_to_interior_code_compliance = form_data['metalExposedToInterior'].get('codeCompliance', spec.metal_exposed_to_interior_code_compliance)
            spec.metal_exposed_to_interior_photos = form_data['metalExposedToInterior'].get('photos', spec.metal_exposed_to_interior_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-hearth-construction/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_hearth_construction(inspection_id):
    """Delete masonry hearth construction for an inspection."""
    try:
        spec = MasonryHearthConstruction.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry hearth construction not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry hearth construction deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Fireplace Components routes
@main.route('/api/masonry-fireplace-components', methods=['POST'])
def create_masonry_fireplace_components():
    """Create masonry fireplace components for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry fireplace components already exist
        existing_spec = MasonryFireplaceComponents.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry fireplace components already exist for this inspection'}), 400

        # Create new masonry fireplace components
        spec = MasonryFireplaceComponents(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'obcWallThickness' in form_data:
            spec.obc_wall_thickness_condition = form_data['obcWallThickness'].get('condition', '')
            spec.obc_wall_thickness_comments = form_data['obcWallThickness'].get('comments', '')
            spec.obc_wall_thickness_code_compliance = form_data['obcWallThickness'].get('codeCompliance', '')
            spec.obc_wall_thickness_photos = form_data['obcWallThickness'].get('photos', [])

        if 'liningMaterials' in form_data:
            spec.lining_materials_condition = form_data['liningMaterials'].get('condition', '')
            spec.lining_materials_comments = form_data['liningMaterials'].get('comments', '')
            spec.lining_materials_code_compliance = form_data['liningMaterials'].get('codeCompliance', '')
            spec.lining_materials_photos = form_data['liningMaterials'].get('photos', [])

        if 'clayLiners' in form_data:
            spec.clay_liners_condition = form_data['clayLiners'].get('condition', '')
            spec.clay_liners_comments = form_data['clayLiners'].get('comments', '')
            spec.clay_liners_code_compliance = form_data['clayLiners'].get('codeCompliance', '')
            spec.clay_liners_photos = form_data['clayLiners'].get('photos', [])

        if 'firebrickLiners' in form_data:
            spec.firebrick_liners_condition = form_data['firebrickLiners'].get('condition', '')
            spec.firebrick_liners_comments = form_data['firebrickLiners'].get('comments', '')
            spec.firebrick_liners_code_compliance = form_data['firebrickLiners'].get('codeCompliance', '')
            spec.firebrick_liners_photos = form_data['firebrickLiners'].get('photos', [])

        if 'concreteLiners' in form_data:
            spec.concrete_liners_condition = form_data['concreteLiners'].get('condition', '')
            spec.concrete_liners_comments = form_data['concreteLiners'].get('comments', '')
            spec.concrete_liners_code_compliance = form_data['concreteLiners'].get('codeCompliance', '')
            spec.concrete_liners_photos = form_data['concreteLiners'].get('photos', [])

        if 'clearanceFromCombustibleMaterials' in form_data:
            spec.clearance_from_combustible_materials_condition = form_data['clearanceFromCombustibleMaterials'].get('condition', '')
            spec.clearance_from_combustible_materials_comments = form_data['clearanceFromCombustibleMaterials'].get('comments', '')
            spec.clearance_from_combustible_materials_code_compliance = form_data['clearanceFromCombustibleMaterials'].get('codeCompliance', '')
            spec.clearance_from_combustible_materials_photos = form_data['clearanceFromCombustibleMaterials'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-components/<int:inspection_id>', methods=['GET'])
def get_masonry_fireplace_components(inspection_id):
    """Get masonry fireplace components for an inspection."""
    try:
        spec = MasonryFireplaceComponents.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry fireplace components not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-components/<int:inspection_id>', methods=['PUT'])
def update_masonry_fireplace_components(inspection_id):
    """Update masonry fireplace components for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryFireplaceComponents.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry fireplace components not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'obcWallThickness' in form_data:
            spec.obc_wall_thickness_condition = form_data['obcWallThickness'].get('condition', spec.obc_wall_thickness_condition)
            spec.obc_wall_thickness_comments = form_data['obcWallThickness'].get('comments', spec.obc_wall_thickness_comments)
            spec.obc_wall_thickness_code_compliance = form_data['obcWallThickness'].get('codeCompliance', spec.obc_wall_thickness_code_compliance)
            spec.obc_wall_thickness_photos = form_data['obcWallThickness'].get('photos', spec.obc_wall_thickness_photos)

        if 'liningMaterials' in form_data:
            spec.lining_materials_condition = form_data['liningMaterials'].get('condition', spec.lining_materials_condition)
            spec.lining_materials_comments = form_data['liningMaterials'].get('comments', spec.lining_materials_comments)
            spec.lining_materials_code_compliance = form_data['liningMaterials'].get('codeCompliance', spec.lining_materials_code_compliance)
            spec.lining_materials_photos = form_data['liningMaterials'].get('photos', spec.lining_materials_photos)

        if 'clayLiners' in form_data:
            spec.clay_liners_condition = form_data['clayLiners'].get('condition', spec.clay_liners_condition)
            spec.clay_liners_comments = form_data['clayLiners'].get('comments', spec.clay_liners_comments)
            spec.clay_liners_code_compliance = form_data['clayLiners'].get('codeCompliance', spec.clay_liners_code_compliance)
            spec.clay_liners_photos = form_data['clayLiners'].get('photos', spec.clay_liners_photos)

        if 'firebrickLiners' in form_data:
            spec.firebrick_liners_condition = form_data['firebrickLiners'].get('condition', spec.firebrick_liners_condition)
            spec.firebrick_liners_comments = form_data['firebrickLiners'].get('comments', spec.firebrick_liners_comments)
            spec.firebrick_liners_code_compliance = form_data['firebrickLiners'].get('codeCompliance', spec.firebrick_liners_code_compliance)
            spec.firebrick_liners_photos = form_data['firebrickLiners'].get('photos', spec.firebrick_liners_photos)

        if 'concreteLiners' in form_data:
            spec.concrete_liners_condition = form_data['concreteLiners'].get('condition', spec.concrete_liners_condition)
            spec.concrete_liners_comments = form_data['concreteLiners'].get('comments', spec.concrete_liners_comments)
            spec.concrete_liners_code_compliance = form_data['concreteLiners'].get('codeCompliance', spec.concrete_liners_code_compliance)
            spec.concrete_liners_photos = form_data['concreteLiners'].get('photos', spec.concrete_liners_photos)

        if 'clearanceFromCombustibleMaterials' in form_data:
            spec.clearance_from_combustible_materials_condition = form_data['clearanceFromCombustibleMaterials'].get('condition', spec.clearance_from_combustible_materials_condition)
            spec.clearance_from_combustible_materials_comments = form_data['clearanceFromCombustibleMaterials'].get('comments', spec.clearance_from_combustible_materials_comments)
            spec.clearance_from_combustible_materials_code_compliance = form_data['clearanceFromCombustibleMaterials'].get('codeCompliance', spec.clearance_from_combustible_materials_code_compliance)
            spec.clearance_from_combustible_materials_photos = form_data['clearanceFromCombustibleMaterials'].get('photos', spec.clearance_from_combustible_materials_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-components/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_fireplace_components(inspection_id):
    """Delete masonry fireplace components for an inspection."""
    try:
        spec = MasonryFireplaceComponents.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry fireplace components not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry fireplace components deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Fireplace Clearances routes
@main.route('/api/masonry-fireplace-clearances', methods=['POST'])
def create_masonry_fireplace_clearances():
    """Create masonry fireplace clearances for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry fireplace clearances already exist
        existing_spec = MasonryFireplaceClearances.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry fireplace clearances already exist for this inspection'}), 400

        # Create new masonry fireplace clearances
        spec = MasonryFireplaceClearances(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'clearanceToCombustibleFraming1' in form_data:
            spec.clearance_to_combustible_framing_1_condition = form_data['clearanceToCombustibleFraming1'].get('condition', '')
            spec.clearance_to_combustible_framing_1_comments = form_data['clearanceToCombustibleFraming1'].get('comments', '')
            spec.clearance_to_combustible_framing_1_code_compliance = form_data['clearanceToCombustibleFraming1'].get('codeCompliance', '')
            spec.clearance_to_combustible_framing_1_photos = form_data['clearanceToCombustibleFraming1'].get('photos', [])

        if 'clearanceToCombustibleFraming2' in form_data:
            spec.clearance_to_combustible_framing_2_condition = form_data['clearanceToCombustibleFraming2'].get('condition', '')
            spec.clearance_to_combustible_framing_2_comments = form_data['clearanceToCombustibleFraming2'].get('comments', '')
            spec.clearance_to_combustible_framing_2_code_compliance = form_data['clearanceToCombustibleFraming2'].get('codeCompliance', '')
            spec.clearance_to_combustible_framing_2_photos = form_data['clearanceToCombustibleFraming2'].get('photos', [])

        if 'heatCirculatingDuctOutlets' in form_data:
            spec.heat_circulating_duct_outlets_condition = form_data['heatCirculatingDuctOutlets'].get('condition', '')
            spec.heat_circulating_duct_outlets_comments = form_data['heatCirculatingDuctOutlets'].get('comments', '')
            spec.heat_circulating_duct_outlets_code_compliance = form_data['heatCirculatingDuctOutlets'].get('codeCompliance', '')
            spec.heat_circulating_duct_outlets_photos = form_data['heatCirculatingDuctOutlets'].get('photos', [])

        if 'cleanout' in form_data:
            spec.cleanout_condition = form_data['cleanout'].get('condition', '')
            spec.cleanout_comments = form_data['cleanout'].get('comments', '')
            spec.cleanout_code_compliance = form_data['cleanout'].get('codeCompliance', '')
            spec.cleanout_photos = form_data['cleanout'].get('photos', [])

        if 'clearanceFromCombustibleMaterials' in form_data:
            spec.clearance_from_combustible_materials_condition = form_data['clearanceFromCombustibleMaterials'].get('condition', '')
            spec.clearance_from_combustible_materials_comments = form_data['clearanceFromCombustibleMaterials'].get('comments', '')
            spec.clearance_from_combustible_materials_code_compliance = form_data['clearanceFromCombustibleMaterials'].get('codeCompliance', '')
            spec.clearance_from_combustible_materials_photos = form_data['clearanceFromCombustibleMaterials'].get('photos', [])

        if 'abcBcbcNbcWallThickness' in form_data:
            spec.abc_bcbc_nbc_wall_thickness_condition = form_data['abcBcbcNbcWallThickness'].get('condition', '')
            spec.abc_bcbc_nbc_wall_thickness_comments = form_data['abcBcbcNbcWallThickness'].get('comments', '')
            spec.abc_bcbc_nbc_wall_thickness_code_compliance = form_data['abcBcbcNbcWallThickness'].get('codeCompliance', '')
            spec.abc_bcbc_nbc_wall_thickness_photos = form_data['abcBcbcNbcWallThickness'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-clearances/<int:inspection_id>', methods=['GET'])
def get_masonry_fireplace_clearances(inspection_id):
    """Get masonry fireplace clearances for an inspection."""
    try:
        spec = MasonryFireplaceClearances.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry fireplace clearances not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-clearances/<int:inspection_id>', methods=['PUT'])
def update_masonry_fireplace_clearances(inspection_id):
    """Update masonry fireplace clearances for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryFireplaceClearances.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry fireplace clearances not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'clearanceToCombustibleFraming1' in form_data:
            spec.clearance_to_combustible_framing_1_condition = form_data['clearanceToCombustibleFraming1'].get('condition', spec.clearance_to_combustible_framing_1_condition)
            spec.clearance_to_combustible_framing_1_comments = form_data['clearanceToCombustibleFraming1'].get('comments', spec.clearance_to_combustible_framing_1_comments)
            spec.clearance_to_combustible_framing_1_code_compliance = form_data['clearanceToCombustibleFraming1'].get('codeCompliance', spec.clearance_to_combustible_framing_1_code_compliance)
            spec.clearance_to_combustible_framing_1_photos = form_data['clearanceToCombustibleFraming1'].get('photos', spec.clearance_to_combustible_framing_1_photos)

        if 'clearanceToCombustibleFraming2' in form_data:
            spec.clearance_to_combustible_framing_2_condition = form_data['clearanceToCombustibleFraming2'].get('condition', spec.clearance_to_combustible_framing_2_condition)
            spec.clearance_to_combustible_framing_2_comments = form_data['clearanceToCombustibleFraming2'].get('comments', spec.clearance_to_combustible_framing_2_comments)
            spec.clearance_to_combustible_framing_2_code_compliance = form_data['clearanceToCombustibleFraming2'].get('codeCompliance', spec.clearance_to_combustible_framing_2_code_compliance)
            spec.clearance_to_combustible_framing_2_photos = form_data['clearanceToCombustibleFraming2'].get('photos', spec.clearance_to_combustible_framing_2_photos)

        if 'heatCirculatingDuctOutlets' in form_data:
            spec.heat_circulating_duct_outlets_condition = form_data['heatCirculatingDuctOutlets'].get('condition', spec.heat_circulating_duct_outlets_condition)
            spec.heat_circulating_duct_outlets_comments = form_data['heatCirculatingDuctOutlets'].get('comments', spec.heat_circulating_duct_outlets_comments)
            spec.heat_circulating_duct_outlets_code_compliance = form_data['heatCirculatingDuctOutlets'].get('codeCompliance', spec.heat_circulating_duct_outlets_code_compliance)
            spec.heat_circulating_duct_outlets_photos = form_data['heatCirculatingDuctOutlets'].get('photos', spec.heat_circulating_duct_outlets_photos)

        if 'cleanout' in form_data:
            spec.cleanout_condition = form_data['cleanout'].get('condition', spec.cleanout_condition)
            spec.cleanout_comments = form_data['cleanout'].get('comments', spec.cleanout_comments)
            spec.cleanout_code_compliance = form_data['cleanout'].get('codeCompliance', spec.cleanout_code_compliance)
            spec.cleanout_photos = form_data['cleanout'].get('photos', spec.cleanout_photos)

        if 'clearanceFromCombustibleMaterials' in form_data:
            spec.clearance_from_combustible_materials_condition = form_data['clearanceFromCombustibleMaterials'].get('condition', spec.clearance_from_combustible_materials_condition)
            spec.clearance_from_combustible_materials_comments = form_data['clearanceFromCombustibleMaterials'].get('comments', spec.clearance_from_combustible_materials_comments)
            spec.clearance_from_combustible_materials_code_compliance = form_data['clearanceFromCombustibleMaterials'].get('codeCompliance', spec.clearance_from_combustible_materials_code_compliance)
            spec.clearance_from_combustible_materials_photos = form_data['clearanceFromCombustibleMaterials'].get('photos', spec.clearance_from_combustible_materials_photos)

        if 'abcBcbcNbcWallThickness' in form_data:
            spec.abc_bcbc_nbc_wall_thickness_condition = form_data['abcBcbcNbcWallThickness'].get('condition', spec.abc_bcbc_nbc_wall_thickness_condition)
            spec.abc_bcbc_nbc_wall_thickness_comments = form_data['abcBcbcNbcWallThickness'].get('comments', spec.abc_bcbc_nbc_wall_thickness_comments)
            spec.abc_bcbc_nbc_wall_thickness_code_compliance = form_data['abcBcbcNbcWallThickness'].get('codeCompliance', spec.abc_bcbc_nbc_wall_thickness_code_compliance)
            spec.abc_bcbc_nbc_wall_thickness_photos = form_data['abcBcbcNbcWallThickness'].get('photos', spec.abc_bcbc_nbc_wall_thickness_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-fireplace-clearances/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_fireplace_clearances(inspection_id):
    """Delete masonry fireplace clearances for an inspection."""
    try:
        spec = MasonryFireplaceClearances.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry fireplace clearances not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry fireplace clearances deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Chimney Liners Installation routes
@main.route('/api/masonry-chimney-liners-installation', methods=['POST'])
def create_masonry_chimney_liners_installation():
    """Create masonry chimney liners installation for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry chimney liners installation already exist
        existing_spec = MasonryChimneyLinersInstallation.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry chimney liners installation already exist for this inspection'}), 400

        # Create new masonry chimney liners installation
        spec = MasonryChimneyLinersInstallation(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'obcChimneyFluePipeWalls' in form_data:
            spec.obc_chimney_flue_pipe_walls_condition = form_data['obcChimneyFluePipeWalls'].get('condition', '')
            spec.obc_chimney_flue_pipe_walls_comments = form_data['obcChimneyFluePipeWalls'].get('comments', '')
            spec.obc_chimney_flue_pipe_walls_code_compliance = form_data['obcChimneyFluePipeWalls'].get('codeCompliance', '')
            spec.obc_chimney_flue_pipe_walls_photos = form_data['obcChimneyFluePipeWalls'].get('photos', [])

        if 'abcBcbcNbcChimneyFluePipeWalls' in form_data:
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_condition = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('condition', '')
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_comments = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('comments', '')
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_code_compliance = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('codeCompliance', '')
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_photos = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('photos', [])

        if 'ovalChimneyFlues' in form_data:
            spec.oval_chimney_flues_condition = form_data['ovalChimneyFlues'].get('condition', '')
            spec.oval_chimney_flues_comments = form_data['ovalChimneyFlues'].get('comments', '')
            spec.oval_chimney_flues_code_compliance = form_data['ovalChimneyFlues'].get('codeCompliance', '')
            spec.oval_chimney_flues_photos = form_data['ovalChimneyFlues'].get('photos', [])

        if 'abcBcbcNbcSeparationOfFlueLiners' in form_data:
            spec.abc_bcbc_nbc_separation_of_flue_liners_condition = form_data['abcBcbcNbcSeparationOfFlueLiners'].get('condition', '')
            spec.abc_bcbc_nbc_separation_of_flue_liners_comments = form_data['abcBcbcNbcSeparationOfFlueLiners'].get('comments', '')
            spec.abc_bcbc_nbc_separation_of_flue_liners_code_compliance = form_data['abcBcbcNbcSeparationOfFlueLiners'].get('codeCompliance', '')
            spec.abc_bcbc_nbc_separation_of_flue_liners_photos = form_data['abcBcbcNbcSeparationOfFlueLiners'].get('photos', [])

        if 'obcSeparationOfFlueLiners' in form_data:
            spec.obc_separation_of_flue_liners_condition = form_data['obcSeparationOfFlueLiners'].get('condition', '')
            spec.obc_separation_of_flue_liners_comments = form_data['obcSeparationOfFlueLiners'].get('comments', '')
            spec.obc_separation_of_flue_liners_code_compliance = form_data['obcSeparationOfFlueLiners'].get('codeCompliance', '')
            spec.obc_separation_of_flue_liners_photos = form_data['obcSeparationOfFlueLiners'].get('photos', [])

        if 'jointsInChimneyLiners' in form_data:
            spec.joints_in_chimney_liners_condition = form_data['jointsInChimneyLiners'].get('condition', '')
            spec.joints_in_chimney_liners_comments = form_data['jointsInChimneyLiners'].get('comments', '')
            spec.joints_in_chimney_liners_code_compliance = form_data['jointsInChimneyLiners'].get('codeCompliance', '')
            spec.joints_in_chimney_liners_photos = form_data['jointsInChimneyLiners'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-liners-installation/<int:inspection_id>', methods=['GET'])
def get_masonry_chimney_liners_installation(inspection_id):
    """Get masonry chimney liners installation for an inspection."""
    try:
        spec = MasonryChimneyLinersInstallation.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry chimney liners installation not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-liners-installation/<int:inspection_id>', methods=['PUT'])
def update_masonry_chimney_liners_installation(inspection_id):
    """Update masonry chimney liners installation for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryChimneyLinersInstallation.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry chimney liners installation not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'obcChimneyFluePipeWalls' in form_data:
            spec.obc_chimney_flue_pipe_walls_condition = form_data['obcChimneyFluePipeWalls'].get('condition', spec.obc_chimney_flue_pipe_walls_condition)
            spec.obc_chimney_flue_pipe_walls_comments = form_data['obcChimneyFluePipeWalls'].get('comments', spec.obc_chimney_flue_pipe_walls_comments)
            spec.obc_chimney_flue_pipe_walls_code_compliance = form_data['obcChimneyFluePipeWalls'].get('codeCompliance', spec.obc_chimney_flue_pipe_walls_code_compliance)
            spec.obc_chimney_flue_pipe_walls_photos = form_data['obcChimneyFluePipeWalls'].get('photos', spec.obc_chimney_flue_pipe_walls_photos)

        if 'abcBcbcNbcChimneyFluePipeWalls' in form_data:
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_condition = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('condition', spec.abc_bcbc_nbc_chimney_flue_pipe_walls_condition)
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_comments = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('comments', spec.abc_bcbc_nbc_chimney_flue_pipe_walls_comments)
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_code_compliance = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('codeCompliance', spec.abc_bcbc_nbc_chimney_flue_pipe_walls_code_compliance)
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_photos = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('photos', spec.abc_bcbc_nbc_chimney_flue_pipe_walls_photos)

        if 'ovalChimneyFlues' in form_data:
            spec.oval_chimney_flues_condition = form_data['ovalChimneyFlues'].get('condition', spec.oval_chimney_flues_condition)
            spec.oval_chimney_flues_comments = form_data['ovalChimneyFlues'].get('comments', spec.oval_chimney_flues_comments)
            spec.oval_chimney_flues_code_compliance = form_data['ovalChimneyFlues'].get('codeCompliance', spec.oval_chimney_flues_code_compliance)
            spec.oval_chimney_flues_photos = form_data['ovalChimneyFlues'].get('photos', spec.oval_chimney_flues_photos)

        if 'abcBcbcNbcSeparationOfFlueLiners' in form_data:
            spec.abc_bcbc_nbc_separation_of_flue_liners_condition = form_data['abcBcbcNbcSeparationOfFlueLiners'].get('condition', spec.abc_bcbc_nbc_separation_of_flue_liners_condition)
            spec.abc_bcbc_nbc_separation_of_flue_liners_comments = form_data['abcBcbcNbcSeparationOfFlueLiners'].get('comments', spec.abc_bcbc_nbc_separation_of_flue_liners_comments)
            spec.abc_bcbc_nbc_separation_of_flue_liners_code_compliance = form_data['abcBcbcNbcSeparationOfFlueLiners'].get('codeCompliance', spec.abc_bcbc_nbc_separation_of_flue_liners_code_compliance)
            spec.abc_bcbc_nbc_separation_of_flue_liners_photos = form_data['abcBcbcNbcSeparationOfFlueLiners'].get('photos', spec.abc_bcbc_nbc_separation_of_flue_liners_photos)

        if 'obcSeparationOfFlueLiners' in form_data:
            spec.obc_separation_of_flue_liners_condition = form_data['obcSeparationOfFlueLiners'].get('condition', spec.obc_separation_of_flue_liners_condition)
            spec.obc_separation_of_flue_liners_comments = form_data['obcSeparationOfFlueLiners'].get('comments', spec.obc_separation_of_flue_liners_comments)
            spec.obc_separation_of_flue_liners_code_compliance = form_data['obcSeparationOfFlueLiners'].get('codeCompliance', spec.obc_separation_of_flue_liners_code_compliance)
            spec.obc_separation_of_flue_liners_photos = form_data['obcSeparationOfFlueLiners'].get('photos', spec.obc_separation_of_flue_liners_photos)

        if 'jointsInChimneyLiners' in form_data:
            spec.joints_in_chimney_liners_condition = form_data['jointsInChimneyLiners'].get('condition', spec.joints_in_chimney_liners_condition)
            spec.joints_in_chimney_liners_comments = form_data['jointsInChimneyLiners'].get('comments', spec.joints_in_chimney_liners_comments)
            spec.joints_in_chimney_liners_code_compliance = form_data['jointsInChimneyLiners'].get('codeCompliance', spec.joints_in_chimney_liners_code_compliance)
            spec.joints_in_chimney_liners_photos = form_data['jointsInChimneyLiners'].get('photos', spec.joints_in_chimney_liners_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-liners-installation/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_chimney_liners_installation(inspection_id):
    """Delete masonry chimney liners installation for an inspection."""
    try:
        spec = MasonryChimneyLinersInstallation.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry chimney liners installation not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry chimney liners installation deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Chimney Construction Liners routes
@main.route('/api/wood-stove-masonry-chimney-construction-liners', methods=['POST'])
def create_wood_stove_masonry_chimney_construction_liners():
    """Create wood stove masonry chimney construction liners for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if wood stove masonry chimney construction liners already exist
        existing_spec = WoodStoveMasonryChimneyConstructionLiners.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry chimney construction liners already exist for this inspection'}), 400

        # Create new wood stove masonry chimney construction liners
        spec = WoodStoveMasonryChimneyConstructionLiners(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'abcBcbcNbcSeparationFlueLiners' in form_data:
            spec.abc_bcbc_nbc_separation_flue_liners_condition = form_data['abcBcbcNbcSeparationFlueLiners'].get('condition', '')
            spec.abc_bcbc_nbc_separation_flue_liners_comments = form_data['abcBcbcNbcSeparationFlueLiners'].get('comments', '')
            spec.abc_bcbc_nbc_separation_flue_liners_code_compliance = form_data['abcBcbcNbcSeparationFlueLiners'].get('codeCompliance', '')
            spec.abc_bcbc_nbc_separation_flue_liners_photos = form_data['abcBcbcNbcSeparationFlueLiners'].get('photos', [])

        if 'obcSeparationFlueLiners' in form_data:
            spec.obc_separation_flue_liners_condition = form_data['obcSeparationFlueLiners'].get('condition', '')
            spec.obc_separation_flue_liners_comments = form_data['obcSeparationFlueLiners'].get('comments', '')
            spec.obc_separation_flue_liners_code_compliance = form_data['obcSeparationFlueLiners'].get('codeCompliance', '')
            spec.obc_separation_flue_liners_photos = form_data['obcSeparationFlueLiners'].get('photos', [])

        if 'jointsInChimneyLiners1' in form_data:
            spec.joints_in_chimney_liners_1_condition = form_data['jointsInChimneyLiners1'].get('condition', '')
            spec.joints_in_chimney_liners_1_comments = form_data['jointsInChimneyLiners1'].get('comments', '')
            spec.joints_in_chimney_liners_1_code_compliance = form_data['jointsInChimneyLiners1'].get('codeCompliance', '')
            spec.joints_in_chimney_liners_1_photos = form_data['jointsInChimneyLiners1'].get('photos', [])

        if 'jointsInChimneyLiners2' in form_data:
            spec.joints_in_chimney_liners_2_condition = form_data['jointsInChimneyLiners2'].get('condition', '')
            spec.joints_in_chimney_liners_2_comments = form_data['jointsInChimneyLiners2'].get('comments', '')
            spec.joints_in_chimney_liners_2_code_compliance = form_data['jointsInChimneyLiners2'].get('codeCompliance', '')
            spec.joints_in_chimney_liners_2_photos = form_data['jointsInChimneyLiners2'].get('photos', [])

        if 'installationOfChimneyLiners' in form_data:
            spec.installation_of_chimney_liners_condition = form_data['installationOfChimneyLiners'].get('condition', '')
            spec.installation_of_chimney_liners_comments = form_data['installationOfChimneyLiners'].get('comments', '')
            spec.installation_of_chimney_liners_code_compliance = form_data['installationOfChimneyLiners'].get('codeCompliance', '')
            spec.installation_of_chimney_liners_photos = form_data['installationOfChimneyLiners'].get('photos', [])

        if 'spacesBetweenLinersSurroundingMasonry' in form_data:
            spec.spaces_between_liners_surrounding_masonry_condition = form_data['spacesBetweenLinersSurroundingMasonry'].get('condition', '')
            spec.spaces_between_liners_surrounding_masonry_comments = form_data['spacesBetweenLinersSurroundingMasonry'].get('comments', '')
            spec.spaces_between_liners_surrounding_masonry_code_compliance = form_data['spacesBetweenLinersSurroundingMasonry'].get('codeCompliance', '')
            spec.spaces_between_liners_surrounding_masonry_photos = form_data['spacesBetweenLinersSurroundingMasonry'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-construction-liners/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_chimney_construction_liners(inspection_id):
    """Get wood stove masonry chimney construction liners for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyConstructionLiners.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney construction liners not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-construction-liners/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_chimney_construction_liners(inspection_id):
    """Update wood stove masonry chimney construction liners for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyConstructionLiners.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney construction liners not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        if 'abcBcbcNbcSeparationFlueLiners' in form_data:
            spec.abc_bcbc_nbc_separation_flue_liners_condition = form_data['abcBcbcNbcSeparationFlueLiners'].get('condition', '')
            spec.abc_bcbc_nbc_separation_flue_liners_comments = form_data['abcBcbcNbcSeparationFlueLiners'].get('comments', '')
            spec.abc_bcbc_nbc_separation_flue_liners_code_compliance = form_data['abcBcbcNbcSeparationFlueLiners'].get('codeCompliance', '')
            spec.abc_bcbc_nbc_separation_flue_liners_photos = form_data['abcBcbcNbcSeparationFlueLiners'].get('photos', [])

        if 'obcSeparationFlueLiners' in form_data:
            spec.obc_separation_flue_liners_condition = form_data['obcSeparationFlueLiners'].get('condition', '')
            spec.obc_separation_flue_liners_comments = form_data['obcSeparationFlueLiners'].get('comments', '')
            spec.obc_separation_flue_liners_code_compliance = form_data['obcSeparationFlueLiners'].get('codeCompliance', '')
            spec.obc_separation_flue_liners_photos = form_data['obcSeparationFlueLiners'].get('photos', [])

        if 'jointsInChimneyLiners1' in form_data:
            spec.joints_in_chimney_liners_1_condition = form_data['jointsInChimneyLiners1'].get('condition', '')
            spec.joints_in_chimney_liners_1_comments = form_data['jointsInChimneyLiners1'].get('comments', '')
            spec.joints_in_chimney_liners_1_code_compliance = form_data['jointsInChimneyLiners1'].get('codeCompliance', '')
            spec.joints_in_chimney_liners_1_photos = form_data['jointsInChimneyLiners1'].get('photos', [])

        if 'jointsInChimneyLiners2' in form_data:
            spec.joints_in_chimney_liners_2_condition = form_data['jointsInChimneyLiners2'].get('condition', '')
            spec.joints_in_chimney_liners_2_comments = form_data['jointsInChimneyLiners2'].get('comments', '')
            spec.joints_in_chimney_liners_2_code_compliance = form_data['jointsInChimneyLiners2'].get('codeCompliance', '')
            spec.joints_in_chimney_liners_2_photos = form_data['jointsInChimneyLiners2'].get('photos', [])

        if 'installationOfChimneyLiners' in form_data:
            spec.installation_of_chimney_liners_condition = form_data['installationOfChimneyLiners'].get('condition', '')
            spec.installation_of_chimney_liners_comments = form_data['installationOfChimneyLiners'].get('comments', '')
            spec.installation_of_chimney_liners_code_compliance = form_data['installationOfChimneyLiners'].get('codeCompliance', '')
            spec.installation_of_chimney_liners_photos = form_data['installationOfChimneyLiners'].get('photos', [])

        if 'spacesBetweenLinersSurroundingMasonry' in form_data:
            spec.spaces_between_liners_surrounding_masonry_condition = form_data['spacesBetweenLinersSurroundingMasonry'].get('condition', '')
            spec.spaces_between_liners_surrounding_masonry_comments = form_data['spacesBetweenLinersSurroundingMasonry'].get('comments', '')
            spec.spaces_between_liners_surrounding_masonry_code_compliance = form_data['spacesBetweenLinersSurroundingMasonry'].get('codeCompliance', '')
            spec.spaces_between_liners_surrounding_masonry_photos = form_data['spacesBetweenLinersSurroundingMasonry'].get('photos', [])

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-construction-liners/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_chimney_construction_liners(inspection_id):
    """Delete wood stove masonry chimney construction liners for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyConstructionLiners.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney construction liners not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry chimney construction liners deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Chimney Construction routes
@main.route('/api/wood-stove-masonry-chimney-construction', methods=['POST'])
def create_wood_stove_masonry_chimney_construction():
    """Create wood stove masonry chimney construction for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if wood stove masonry chimney construction already exists
        existing_spec = WoodStoveMasonryChimneyConstruction.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry chimney construction already exists for this inspection'}), 400

        # Create new wood stove masonry chimney construction
        spec = WoodStoveMasonryChimneyConstruction(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'footings' in form_data:
            spec.footings_condition = form_data['footings'].get('condition', '')
            spec.footings_comments = form_data['footings'].get('comments', '')
            spec.footings_code_compliance = form_data['footings'].get('codeCompliance', '')
            spec.footings_photos = form_data['footings'].get('photos', [])

        if 'cleanout' in form_data:
            spec.cleanout_condition = form_data['cleanout'].get('condition', '')
            spec.cleanout_comments = form_data['cleanout'].get('comments', '')
            spec.cleanout_code_compliance = form_data['cleanout'].get('codeCompliance', '')
            spec.cleanout_photos = form_data['cleanout'].get('photos', [])

        if 'clearanceFromCombustibleMaterials' in form_data:
            spec.clearance_from_combustible_materials_condition = form_data['clearanceFromCombustibleMaterials'].get('condition', '')
            spec.clearance_from_combustible_materials_comments = form_data['clearanceFromCombustibleMaterials'].get('comments', '')
            spec.clearance_from_combustible_materials_code_compliance = form_data['clearanceFromCombustibleMaterials'].get('codeCompliance', '')
            spec.clearance_from_combustible_materials_photos = form_data['clearanceFromCombustibleMaterials'].get('photos', [])

        if 'abcBcbcNbcWallThickness' in form_data:
            spec.abc_bcbc_nbc_wall_thickness_condition = form_data['abcBcbcNbcWallThickness'].get('condition', '')
            spec.abc_bcbc_nbc_wall_thickness_comments = form_data['abcBcbcNbcWallThickness'].get('comments', '')
            spec.abc_bcbc_nbc_wall_thickness_code_compliance = form_data['abcBcbcNbcWallThickness'].get('codeCompliance', '')
            spec.abc_bcbc_nbc_wall_thickness_photos = form_data['abcBcbcNbcWallThickness'].get('photos', [])

        if 'obcWallThickness' in form_data:
            spec.obc_wall_thickness_condition = form_data['obcWallThickness'].get('condition', '')
            spec.obc_wall_thickness_comments = form_data['obcWallThickness'].get('comments', '')
            spec.obc_wall_thickness_code_compliance = form_data['obcWallThickness'].get('codeCompliance', '')
            spec.obc_wall_thickness_photos = form_data['obcWallThickness'].get('photos', [])

        if 'liningMaterials' in form_data:
            spec.lining_materials_condition = form_data['liningMaterials'].get('condition', '')
            spec.lining_materials_comments = form_data['liningMaterials'].get('comments', '')
            spec.lining_materials_code_compliance = form_data['liningMaterials'].get('codeCompliance', '')
            spec.lining_materials_photos = form_data['liningMaterials'].get('photos', [])

        if 'clayLiners' in form_data:
            spec.clay_liners_condition = form_data['clayLiners'].get('condition', '')
            spec.clay_liners_comments = form_data['clayLiners'].get('comments', '')
            spec.clay_liners_code_compliance = form_data['clayLiners'].get('codeCompliance', '')
            spec.clay_liners_photos = form_data['clayLiners'].get('photos', [])

        if 'firebrickLiners' in form_data:
            spec.firebrick_liners_condition = form_data['firebrickLiners'].get('condition', '')
            spec.firebrick_liners_comments = form_data['firebrickLiners'].get('comments', '')
            spec.firebrick_liners_code_compliance = form_data['firebrickLiners'].get('codeCompliance', '')
            spec.firebrick_liners_photos = form_data['firebrickLiners'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-construction/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_chimney_construction(inspection_id):
    """Get wood stove masonry chimney construction for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyConstruction.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney construction not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-construction/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_chimney_construction(inspection_id):
    """Update wood stove masonry chimney construction for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyConstruction.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney construction not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        if 'footings' in form_data:
            spec.footings_condition = form_data['footings'].get('condition', '')
            spec.footings_comments = form_data['footings'].get('comments', '')
            spec.footings_code_compliance = form_data['footings'].get('codeCompliance', '')
            spec.footings_photos = form_data['footings'].get('photos', [])

        if 'cleanout' in form_data:
            spec.cleanout_condition = form_data['cleanout'].get('condition', '')
            spec.cleanout_comments = form_data['cleanout'].get('comments', '')
            spec.cleanout_code_compliance = form_data['cleanout'].get('codeCompliance', '')
            spec.cleanout_photos = form_data['cleanout'].get('photos', [])

        if 'clearanceFromCombustibleMaterials' in form_data:
            spec.clearance_from_combustible_materials_condition = form_data['clearanceFromCombustibleMaterials'].get('condition', '')
            spec.clearance_from_combustible_materials_comments = form_data['clearanceFromCombustibleMaterials'].get('comments', '')
            spec.clearance_from_combustible_materials_code_compliance = form_data['clearanceFromCombustibleMaterials'].get('codeCompliance', '')
            spec.clearance_from_combustible_materials_photos = form_data['clearanceFromCombustibleMaterials'].get('photos', [])

        if 'abcBcbcNbcWallThickness' in form_data:
            spec.abc_bcbc_nbc_wall_thickness_condition = form_data['abcBcbcNbcWallThickness'].get('condition', '')
            spec.abc_bcbc_nbc_wall_thickness_comments = form_data['abcBcbcNbcWallThickness'].get('comments', '')
            spec.abc_bcbc_nbc_wall_thickness_code_compliance = form_data['abcBcbcNbcWallThickness'].get('codeCompliance', '')
            spec.abc_bcbc_nbc_wall_thickness_photos = form_data['abcBcbcNbcWallThickness'].get('photos', [])

        if 'obcWallThickness' in form_data:
            spec.obc_wall_thickness_condition = form_data['obcWallThickness'].get('condition', '')
            spec.obc_wall_thickness_comments = form_data['obcWallThickness'].get('comments', '')
            spec.obc_wall_thickness_code_compliance = form_data['obcWallThickness'].get('codeCompliance', '')
            spec.obc_wall_thickness_photos = form_data['obcWallThickness'].get('photos', [])

        if 'liningMaterials' in form_data:
            spec.lining_materials_condition = form_data['liningMaterials'].get('condition', '')
            spec.lining_materials_comments = form_data['liningMaterials'].get('comments', '')
            spec.lining_materials_code_compliance = form_data['liningMaterials'].get('codeCompliance', '')
            spec.lining_materials_photos = form_data['liningMaterials'].get('photos', [])

        if 'clayLiners' in form_data:
            spec.clay_liners_condition = form_data['clayLiners'].get('condition', '')
            spec.clay_liners_comments = form_data['clayLiners'].get('comments', '')
            spec.clay_liners_code_compliance = form_data['clayLiners'].get('codeCompliance', '')
            spec.clay_liners_photos = form_data['clayLiners'].get('photos', [])

        if 'firebrickLiners' in form_data:
            spec.firebrick_liners_condition = form_data['firebrickLiners'].get('condition', '')
            spec.firebrick_liners_comments = form_data['firebrickLiners'].get('comments', '')
            spec.firebrick_liners_code_compliance = form_data['firebrickLiners'].get('codeCompliance', '')
            spec.firebrick_liners_photos = form_data['firebrickLiners'].get('photos', [])

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-construction/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_chimney_construction(inspection_id):
    """Delete wood stove masonry chimney construction for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyConstruction.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney construction not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry chimney construction deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Chimney Liners Installation routes
@main.route('/api/wood-stove-masonry-chimney-liners-installation', methods=['POST'])
def create_wood_stove_masonry_chimney_liners_installation():
    """Create wood stove masonry chimney liners installation for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if wood stove masonry chimney liners installation already exists
        existing_spec = WoodStoveMasonryChimneyLinersInstallation.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry chimney liners installation already exists for this inspection'}), 400

        # Create new wood stove masonry chimney liners installation
        spec = WoodStoveMasonryChimneyLinersInstallation(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'mortarSolidFuel' in form_data:
            spec.mortar_solid_fuel_condition = form_data['mortarSolidFuel'].get('condition', '')
            spec.mortar_solid_fuel_comments = form_data['mortarSolidFuel'].get('comments', '')
            spec.mortar_solid_fuel_code_compliance = form_data['mortarSolidFuel'].get('codeCompliance', '')
            spec.mortar_solid_fuel_photos = form_data['mortarSolidFuel'].get('photos', [])

        if 'mortarOilGas' in form_data:
            spec.mortar_oil_gas_condition = form_data['mortarOilGas'].get('condition', '')
            spec.mortar_oil_gas_comments = form_data['mortarOilGas'].get('comments', '')
            spec.mortar_oil_gas_code_compliance = form_data['mortarOilGas'].get('codeCompliance', '')
            spec.mortar_oil_gas_photos = form_data['mortarOilGas'].get('photos', [])

        if 'extensionChimneyLiners' in form_data:
            spec.extension_chimney_liners_condition = form_data['extensionChimneyLiners'].get('condition', '')
            spec.extension_chimney_liners_comments = form_data['extensionChimneyLiners'].get('comments', '')
            spec.extension_chimney_liners_code_compliance = form_data['extensionChimneyLiners'].get('codeCompliance', '')
            spec.extension_chimney_liners_photos = form_data['extensionChimneyLiners'].get('photos', [])

        if 'wallThickness' in form_data:
            spec.wall_thickness_condition = form_data['wallThickness'].get('condition', '')
            spec.wall_thickness_comments = form_data['wallThickness'].get('comments', '')
            spec.wall_thickness_code_compliance = form_data['wallThickness'].get('codeCompliance', '')
            spec.wall_thickness_photos = form_data['wallThickness'].get('photos', [])

        if 'liningMaterials' in form_data:
            spec.lining_materials_condition = form_data['liningMaterials'].get('condition', '')
            spec.lining_materials_comments = form_data['liningMaterials'].get('comments', '')
            spec.lining_materials_code_compliance = form_data['liningMaterials'].get('codeCompliance', '')
            spec.lining_materials_photos = form_data['liningMaterials'].get('photos', [])

        if 'clayLiners' in form_data:
            spec.clay_liners_condition = form_data['clayLiners'].get('condition', '')
            spec.clay_liners_comments = form_data['clayLiners'].get('comments', '')
            spec.clay_liners_code_compliance = form_data['clayLiners'].get('codeCompliance', '')
            spec.clay_liners_photos = form_data['clayLiners'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-liners-installation/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_chimney_liners_installation(inspection_id):
    """Get wood stove masonry chimney liners installation for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyLinersInstallation.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney liners installation not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-liners-installation/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_chimney_liners_installation(inspection_id):
    """Update wood stove masonry chimney liners installation for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyLinersInstallation.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney liners installation not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        if 'mortarSolidFuel' in form_data:
            spec.mortar_solid_fuel_condition = form_data['mortarSolidFuel'].get('condition', '')
            spec.mortar_solid_fuel_comments = form_data['mortarSolidFuel'].get('comments', '')
            spec.mortar_solid_fuel_code_compliance = form_data['mortarSolidFuel'].get('codeCompliance', '')
            spec.mortar_solid_fuel_photos = form_data['mortarSolidFuel'].get('photos', [])

        if 'mortarOilGas' in form_data:
            spec.mortar_oil_gas_condition = form_data['mortarOilGas'].get('condition', '')
            spec.mortar_oil_gas_comments = form_data['mortarOilGas'].get('comments', '')
            spec.mortar_oil_gas_code_compliance = form_data['mortarOilGas'].get('codeCompliance', '')
            spec.mortar_oil_gas_photos = form_data['mortarOilGas'].get('photos', [])

        if 'extensionChimneyLiners' in form_data:
            spec.extension_chimney_liners_condition = form_data['extensionChimneyLiners'].get('condition', '')
            spec.extension_chimney_liners_comments = form_data['extensionChimneyLiners'].get('comments', '')
            spec.extension_chimney_liners_code_compliance = form_data['extensionChimneyLiners'].get('codeCompliance', '')
            spec.extension_chimney_liners_photos = form_data['extensionChimneyLiners'].get('photos', [])

        if 'wallThickness' in form_data:
            spec.wall_thickness_condition = form_data['wallThickness'].get('condition', '')
            spec.wall_thickness_comments = form_data['wallThickness'].get('comments', '')
            spec.wall_thickness_code_compliance = form_data['wallThickness'].get('codeCompliance', '')
            spec.wall_thickness_photos = form_data['wallThickness'].get('photos', [])

        if 'liningMaterials' in form_data:
            spec.lining_materials_condition = form_data['liningMaterials'].get('condition', '')
            spec.lining_materials_comments = form_data['liningMaterials'].get('comments', '')
            spec.lining_materials_code_compliance = form_data['liningMaterials'].get('codeCompliance', '')
            spec.lining_materials_photos = form_data['liningMaterials'].get('photos', [])

        if 'clayLiners' in form_data:
            spec.clay_liners_condition = form_data['clayLiners'].get('condition', '')
            spec.clay_liners_comments = form_data['clayLiners'].get('comments', '')
            spec.clay_liners_code_compliance = form_data['clayLiners'].get('codeCompliance', '')
            spec.clay_liners_photos = form_data['clayLiners'].get('photos', [])

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-liners-installation/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_chimney_liners_installation(inspection_id):
    """Delete wood stove masonry chimney liners installation for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyLinersInstallation.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney liners installation not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry chimney liners installation deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Chimney Liners routes
@main.route('/api/wood-stove-masonry-chimney-liners', methods=['POST'])
def create_wood_stove_masonry_chimney_liners():
    """Create wood stove masonry chimney liners for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if wood stove masonry chimney liners already exists
        existing_spec = WoodStoveMasonryChimneyLiners.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry chimney liners already exists for this inspection'}), 400

        # Create new wood stove masonry chimney liners
        spec = WoodStoveMasonryChimneyLiners(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'concreteLiners' in form_data:
            spec.concrete_liners_condition = form_data['concreteLiners'].get('condition', '')
            spec.concrete_liners_comments = form_data['concreteLiners'].get('comments', '')
            spec.concrete_liners_code_compliance = form_data['concreteLiners'].get('codeCompliance', '')
            spec.concrete_liners_photos = form_data['concreteLiners'].get('photos', [])

        if 'metalLiners' in form_data:
            spec.metal_liners_condition = form_data['metalLiners'].get('condition', '')
            spec.metal_liners_comments = form_data['metalLiners'].get('comments', '')
            spec.metal_liners_code_compliance = form_data['metalLiners'].get('codeCompliance', '')
            spec.metal_liners_photos = form_data['metalLiners'].get('photos', [])

        if 'obcChimneyFluePipeWalls' in form_data:
            spec.obc_chimney_flue_pipe_walls_condition = form_data['obcChimneyFluePipeWalls'].get('condition', '')
            spec.obc_chimney_flue_pipe_walls_comments = form_data['obcChimneyFluePipeWalls'].get('comments', '')
            spec.obc_chimney_flue_pipe_walls_code_compliance = form_data['obcChimneyFluePipeWalls'].get('codeCompliance', '')
            spec.obc_chimney_flue_pipe_walls_photos = form_data['obcChimneyFluePipeWalls'].get('photos', [])

        if 'abcBcbcNbcChimneyFluePipeWalls' in form_data:
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_condition = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('condition', '')
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_comments = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('comments', '')
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_code_compliance = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('codeCompliance', '')
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_photos = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('photos', [])

        if 'sizeOfChimneyFlues' in form_data:
            spec.size_of_chimney_flues_condition = form_data['sizeOfChimneyFlues'].get('condition', '')
            spec.size_of_chimney_flues_comments = form_data['sizeOfChimneyFlues'].get('comments', '')
            spec.size_of_chimney_flues_code_compliance = form_data['sizeOfChimneyFlues'].get('codeCompliance', '')
            spec.size_of_chimney_flues_photos = form_data['sizeOfChimneyFlues'].get('photos', [])

        if 'ovalChimneyFlues' in form_data:
            spec.oval_chimney_flues_condition = form_data['ovalChimneyFlues'].get('condition', '')
            spec.oval_chimney_flues_comments = form_data['ovalChimneyFlues'].get('comments', '')
            spec.oval_chimney_flues_code_compliance = form_data['ovalChimneyFlues'].get('codeCompliance', '')
            spec.oval_chimney_flues_photos = form_data['ovalChimneyFlues'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-liners/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_chimney_liners(inspection_id):
    """Get wood stove masonry chimney liners for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyLiners.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney liners not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-liners/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_chimney_liners(inspection_id):
    """Update wood stove masonry chimney liners for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyLiners.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney liners not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        if 'concreteLiners' in form_data:
            spec.concrete_liners_condition = form_data['concreteLiners'].get('condition', '')
            spec.concrete_liners_comments = form_data['concreteLiners'].get('comments', '')
            spec.concrete_liners_code_compliance = form_data['concreteLiners'].get('codeCompliance', '')
            spec.concrete_liners_photos = form_data['concreteLiners'].get('photos', [])

        if 'metalLiners' in form_data:
            spec.metal_liners_condition = form_data['metalLiners'].get('condition', '')
            spec.metal_liners_comments = form_data['metalLiners'].get('comments', '')
            spec.metal_liners_code_compliance = form_data['metalLiners'].get('codeCompliance', '')
            spec.metal_liners_photos = form_data['metalLiners'].get('photos', [])

        if 'obcChimneyFluePipeWalls' in form_data:
            spec.obc_chimney_flue_pipe_walls_condition = form_data['obcChimneyFluePipeWalls'].get('condition', '')
            spec.obc_chimney_flue_pipe_walls_comments = form_data['obcChimneyFluePipeWalls'].get('comments', '')
            spec.obc_chimney_flue_pipe_walls_code_compliance = form_data['obcChimneyFluePipeWalls'].get('codeCompliance', '')
            spec.obc_chimney_flue_pipe_walls_photos = form_data['obcChimneyFluePipeWalls'].get('photos', [])

        if 'abcBcbcNbcChimneyFluePipeWalls' in form_data:
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_condition = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('condition', '')
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_comments = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('comments', '')
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_code_compliance = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('codeCompliance', '')
            spec.abc_bcbc_nbc_chimney_flue_pipe_walls_photos = form_data['abcBcbcNbcChimneyFluePipeWalls'].get('photos', [])

        if 'sizeOfChimneyFlues' in form_data:
            spec.size_of_chimney_flues_condition = form_data['sizeOfChimneyFlues'].get('condition', '')
            spec.size_of_chimney_flues_comments = form_data['sizeOfChimneyFlues'].get('comments', '')
            spec.size_of_chimney_flues_code_compliance = form_data['sizeOfChimneyFlues'].get('codeCompliance', '')
            spec.size_of_chimney_flues_photos = form_data['sizeOfChimneyFlues'].get('photos', [])

        if 'ovalChimneyFlues' in form_data:
            spec.oval_chimney_flues_condition = form_data['ovalChimneyFlues'].get('condition', '')
            spec.oval_chimney_flues_comments = form_data['ovalChimneyFlues'].get('comments', '')
            spec.oval_chimney_flues_code_compliance = form_data['ovalChimneyFlues'].get('codeCompliance', '')
            spec.oval_chimney_flues_photos = form_data['ovalChimneyFlues'].get('photos', [])

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-liners/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_chimney_liners(inspection_id):
    """Delete wood stove masonry chimney liners for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyLiners.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney liners not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry chimney liners deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Chimney Saddles routes
@main.route('/api/wood-stove-masonry-chimney-saddles', methods=['POST'])
def create_wood_stove_masonry_chimney_saddles():
    """Create wood stove masonry chimney saddles for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if wood stove masonry chimney saddles already exists
        existing_spec = WoodStoveMasonryChimneySaddles.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry chimney saddles already exists for this inspection'}), 400

        # Create new wood stove masonry chimney saddles
        spec = WoodStoveMasonryChimneySaddles(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'chimneySaddles' in form_data:
            spec.chimney_saddles_condition = form_data['chimneySaddles'].get('condition', '')
            spec.chimney_saddles_comments = form_data['chimneySaddles'].get('comments', '')
            spec.chimney_saddles_code_compliance = form_data['chimneySaddles'].get('codeCompliance', '')
            spec.chimney_saddles_photos = form_data['chimneySaddles'].get('photos', [])

        if 'fireCodeChimneyFlues' in form_data:
            spec.fire_code_chimney_flues_condition = form_data['fireCodeChimneyFlues'].get('condition', '')
            spec.fire_code_chimney_flues_comments = form_data['fireCodeChimneyFlues'].get('comments', '')
            spec.fire_code_chimney_flues_code_compliance = form_data['fireCodeChimneyFlues'].get('codeCompliance', '')
            spec.fire_code_chimney_flues_photos = form_data['fireCodeChimneyFlues'].get('photos', [])

        if 'fireCodeCleaning' in form_data:
            spec.fire_code_cleaning_condition = form_data['fireCodeCleaning'].get('condition', '')
            spec.fire_code_cleaning_comments = form_data['fireCodeCleaning'].get('comments', '')
            spec.fire_code_cleaning_code_compliance = form_data['fireCodeCleaning'].get('codeCompliance', '')
            spec.fire_code_cleaning_photos = form_data['fireCodeCleaning'].get('photos', [])

        if 'fireCodeStructuralDeficiency' in form_data:
            spec.fire_code_structural_deficiency_condition = form_data['fireCodeStructuralDeficiency'].get('condition', '')
            spec.fire_code_structural_deficiency_comments = form_data['fireCodeStructuralDeficiency'].get('comments', '')
            spec.fire_code_structural_deficiency_code_compliance = form_data['fireCodeStructuralDeficiency'].get('codeCompliance', '')
            spec.fire_code_structural_deficiency_photos = form_data['fireCodeStructuralDeficiency'].get('photos', [])

        if 'fireCodeAbandonedOpenings' in form_data:
            spec.fire_code_abandoned_openings_condition = form_data['fireCodeAbandonedOpenings'].get('condition', '')
            spec.fire_code_abandoned_openings_comments = form_data['fireCodeAbandonedOpenings'].get('comments', '')
            spec.fire_code_abandoned_openings_code_compliance = form_data['fireCodeAbandonedOpenings'].get('codeCompliance', '')
            spec.fire_code_abandoned_openings_photos = form_data['fireCodeAbandonedOpenings'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-saddles/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_chimney_saddles(inspection_id):
    """Get wood stove masonry chimney saddles for an inspection."""
    try:
        spec = WoodStoveMasonryChimneySaddles.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney saddles not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-saddles/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_chimney_saddles(inspection_id):
    """Update wood stove masonry chimney saddles for an inspection."""
    try:
        spec = WoodStoveMasonryChimneySaddles.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney saddles not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        if 'chimneySaddles' in form_data:
            spec.chimney_saddles_condition = form_data['chimneySaddles'].get('condition', '')
            spec.chimney_saddles_comments = form_data['chimneySaddles'].get('comments', '')
            spec.chimney_saddles_code_compliance = form_data['chimneySaddles'].get('codeCompliance', '')
            spec.chimney_saddles_photos = form_data['chimneySaddles'].get('photos', [])

        if 'fireCodeChimneyFlues' in form_data:
            spec.fire_code_chimney_flues_condition = form_data['fireCodeChimneyFlues'].get('condition', '')
            spec.fire_code_chimney_flues_comments = form_data['fireCodeChimneyFlues'].get('comments', '')
            spec.fire_code_chimney_flues_code_compliance = form_data['fireCodeChimneyFlues'].get('codeCompliance', '')
            spec.fire_code_chimney_flues_photos = form_data['fireCodeChimneyFlues'].get('photos', [])

        if 'fireCodeCleaning' in form_data:
            spec.fire_code_cleaning_condition = form_data['fireCodeCleaning'].get('condition', '')
            spec.fire_code_cleaning_comments = form_data['fireCodeCleaning'].get('comments', '')
            spec.fire_code_cleaning_code_compliance = form_data['fireCodeCleaning'].get('codeCompliance', '')
            spec.fire_code_cleaning_photos = form_data['fireCodeCleaning'].get('photos', [])

        if 'fireCodeStructuralDeficiency' in form_data:
            spec.fire_code_structural_deficiency_condition = form_data['fireCodeStructuralDeficiency'].get('condition', '')
            spec.fire_code_structural_deficiency_comments = form_data['fireCodeStructuralDeficiency'].get('comments', '')
            spec.fire_code_structural_deficiency_code_compliance = form_data['fireCodeStructuralDeficiency'].get('codeCompliance', '')
            spec.fire_code_structural_deficiency_photos = form_data['fireCodeStructuralDeficiency'].get('photos', [])

        if 'fireCodeAbandonedOpenings' in form_data:
            spec.fire_code_abandoned_openings_condition = form_data['fireCodeAbandonedOpenings'].get('condition', '')
            spec.fire_code_abandoned_openings_comments = form_data['fireCodeAbandonedOpenings'].get('comments', '')
            spec.fire_code_abandoned_openings_code_compliance = form_data['fireCodeAbandonedOpenings'].get('codeCompliance', '')
            spec.fire_code_abandoned_openings_photos = form_data['fireCodeAbandonedOpenings'].get('photos', [])

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-saddles/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_chimney_saddles(inspection_id):
    """Delete wood stove masonry chimney saddles for an inspection."""
    try:
        spec = WoodStoveMasonryChimneySaddles.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney saddles not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry chimney saddles deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Chimney Specifications routes
@main.route('/api/wood-stove-masonry-chimney-specifications', methods=['POST'])
def create_wood_stove_masonry_chimney_specifications():
    """Create wood stove masonry chimney specifications for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if wood stove masonry chimney specifications already exists
        existing_spec = WoodStoveMasonryChimneySpecifications.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry chimney specifications already exists for this inspection'}), 400

        # Create new wood stove masonry chimney specifications
        spec = WoodStoveMasonryChimneySpecifications(inspection_id=inspection_id)

        # Handle formData fields
        form_data = data.get('formData', {})

        if 'inspectionDiscussed' in form_data:
            spec.inspection_discussed = form_data['inspectionDiscussed']
        if 'buildingPermitsAvailable' in form_data:
            spec.building_permits_available = form_data['buildingPermitsAvailable']
        if 'timeOfDay' in form_data:
            spec.time_of_day = form_data['timeOfDay']
        if 'weatherConditions' in form_data:
            spec.weather_conditions = form_data['weatherConditions']
        if 'roofingTypeMaterial' in form_data:
            spec.roofing_type_material = form_data['roofingTypeMaterial']
        if 'roofAccessed' in form_data:
            spec.roof_accessed = form_data['roofAccessed']
        if 'atticAccessed' in form_data:
            spec.attic_accessed = form_data['atticAccessed']
        if 'chimneyFireplaceConstructedWithBuilding' in form_data:
            spec.chimney_fireplace_constructed_with_building = form_data['chimneyFireplaceConstructedWithBuilding']
        if 'approximateAge' in form_data:
            spec.approximate_age = form_data['approximateAge']
        if 'chimneyFireplaceShell' in form_data:
            spec.chimney_fireplace_shell = form_data['chimneyFireplaceShell']
        if 'rainCap' in form_data:
            spec.rain_cap = form_data['rainCap']
        if 'chimneyLocation' in form_data:
            spec.chimney_location = form_data['chimneyLocation']
        if 'heightFromFireboxFloor' in form_data:
            spec.height_from_firebox_floor = form_data['heightFromFireboxFloor']
        if 'flueSize' in form_data:
            spec.flue_size = form_data['flueSize']
        if 'sizeOfFlue' in form_data:
            spec.size_of_flue = form_data['sizeOfFlue']
        if 'materialOfFlue' in form_data:
            spec.material_of_flue = form_data['materialOfFlue']
        if 'chimneyLinedWith' in form_data:
            spec.chimney_lined_with = form_data['chimneyLinedWith']
        if 'chimneyInstalledBy' in form_data:
            spec.chimney_installed_by = form_data['chimneyInstalledBy']
        if 'chimneyInstalledByUnknown' in form_data:
            spec.chimney_installed_by_unknown = form_data['chimneyInstalledByUnknown']
        if 'chimneyDate' in form_data:
            spec.chimney_date = form_data['chimneyDate']
        if 'fireplaceLocation' in form_data:
            spec.fireplace_location = form_data['fireplaceLocation']
        if 'installedIn' in form_data:
            spec.installed_in = form_data['installedIn']
        if 'fireplaceLocation2' in form_data:
            spec.fireplace_location2 = form_data['fireplaceLocation2']
        if 'othersSpecify' in form_data:
            spec.others_specify = form_data['othersSpecify']
        if 'fireplaceInstalledBy' in form_data:
            spec.fireplace_installed_by = form_data['fireplaceInstalledBy']
        if 'fireplaceInstalledByUnknown' in form_data:
            spec.fireplace_installed_by_unknown = form_data['fireplaceInstalledByUnknown']
        if 'fireplaceDate' in form_data:
            spec.fireplace_date = form_data['fireplaceDate']
        if 'fireplaceLocation3' in form_data:
            spec.fireplace_location3 = form_data['fireplaceLocation3']
        if 'unitShareVentingSystem' in form_data:
            spec.unit_share_venting_system = form_data['unitShareVentingSystem']
        if 'commentsConditionOfChimney' in form_data:
            spec.comments_condition_of_chimney = form_data['commentsConditionOfChimney']
        if 'suitable' in form_data:
            spec.suitable = form_data['suitable']

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-specifications/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_chimney_specifications(inspection_id):
    """Get wood stove masonry chimney specifications for an inspection."""
    try:
        spec = WoodStoveMasonryChimneySpecifications.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney specifications not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-specifications/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_chimney_specifications(inspection_id):
    """Update wood stove masonry chimney specifications for an inspection."""
    try:
        spec = WoodStoveMasonryChimneySpecifications.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney specifications not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        if 'inspectionDiscussed' in form_data:
            spec.inspection_discussed = form_data['inspectionDiscussed']
        if 'buildingPermitsAvailable' in form_data:
            spec.building_permits_available = form_data['buildingPermitsAvailable']
        if 'timeOfDay' in form_data:
            spec.time_of_day = form_data['timeOfDay']
        if 'weatherConditions' in form_data:
            spec.weather_conditions = form_data['weatherConditions']
        if 'roofingTypeMaterial' in form_data:
            spec.roofing_type_material = form_data['roofingTypeMaterial']
        if 'roofAccessed' in form_data:
            spec.roof_accessed = form_data['roofAccessed']
        if 'atticAccessed' in form_data:
            spec.attic_accessed = form_data['atticAccessed']
        if 'chimneyFireplaceConstructedWithBuilding' in form_data:
            spec.chimney_fireplace_constructed_with_building = form_data['chimneyFireplaceConstructedWithBuilding']
        if 'approximateAge' in form_data:
            spec.approximate_age = form_data['approximateAge']
        if 'chimneyFireplaceShell' in form_data:
            spec.chimney_fireplace_shell = form_data['chimneyFireplaceShell']
        if 'rainCap' in form_data:
            spec.rain_cap = form_data['rainCap']
        if 'chimneyLocation' in form_data:
            spec.chimney_location = form_data['chimneyLocation']
        if 'heightFromFireboxFloor' in form_data:
            spec.height_from_firebox_floor = form_data['heightFromFireboxFloor']
        if 'flueSize' in form_data:
            spec.flue_size = form_data['flueSize']
        if 'sizeOfFlue' in form_data:
            spec.size_of_flue = form_data['sizeOfFlue']
        if 'materialOfFlue' in form_data:
            spec.material_of_flue = form_data['materialOfFlue']
        if 'chimneyLinedWith' in form_data:
            spec.chimney_lined_with = form_data['chimneyLinedWith']
        if 'chimneyInstalledBy' in form_data:
            spec.chimney_installed_by = form_data['chimneyInstalledBy']
        if 'chimneyInstalledByUnknown' in form_data:
            spec.chimney_installed_by_unknown = form_data['chimneyInstalledByUnknown']
        if 'chimneyDate' in form_data:
            spec.chimney_date = form_data['chimneyDate']
        if 'fireplaceLocation' in form_data:
            spec.fireplace_location = form_data['fireplaceLocation']
        if 'installedIn' in form_data:
            spec.installed_in = form_data['installedIn']
        if 'fireplaceLocation2' in form_data:
            spec.fireplace_location2 = form_data['fireplaceLocation2']
        if 'othersSpecify' in form_data:
            spec.others_specify = form_data['othersSpecify']
        if 'fireplaceInstalledBy' in form_data:
            spec.fireplace_installed_by = form_data['fireplaceInstalledBy']
        if 'fireplaceInstalledByUnknown' in form_data:
            spec.fireplace_installed_by_unknown = form_data['fireplaceInstalledByUnknown']
        if 'fireplaceDate' in form_data:
            spec.fireplace_date = form_data['fireplaceDate']
        if 'fireplaceLocation3' in form_data:
            spec.fireplace_location3 = form_data['fireplaceLocation3']
        if 'unitShareVentingSystem' in form_data:
            spec.unit_share_venting_system = form_data['unitShareVentingSystem']
        if 'commentsConditionOfChimney' in form_data:
            spec.comments_condition_of_chimney = form_data['commentsConditionOfChimney']
        if 'suitable' in form_data:
            spec.suitable = form_data['suitable']

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-specifications/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_chimney_specifications(inspection_id):
    """Delete wood stove masonry chimney specifications for an inspection."""
    try:
        spec = WoodStoveMasonryChimneySpecifications.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney specifications not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry chimney specifications deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Chimney Stability Caps routes
@main.route('/api/wood-stove-masonry-chimney-stability-caps', methods=['POST'])
def create_wood_stove_masonry_chimney_stability_caps():
    """Create wood stove masonry chimney stability caps for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if wood stove masonry chimney stability caps already exists
        existing_spec = WoodStoveMasonryChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry chimney stability caps already exists for this inspection'}), 400

        # Create new wood stove masonry chimney stability caps
        spec = WoodStoveMasonryChimneyStabilityCaps(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'heightOfChimneyFlues' in form_data:
            spec.height_of_chimney_flues_condition = form_data['heightOfChimneyFlues'].get('condition', '')
            spec.height_of_chimney_flues_comments = form_data['heightOfChimneyFlues'].get('comments', '')
            spec.height_of_chimney_flues_code_compliance = form_data['heightOfChimneyFlues'].get('codeCompliance', '')
            spec.height_of_chimney_flues_photos = form_data['heightOfChimneyFlues'].get('photos', [])
            spec.height_of_chimney_flues_required_height = form_data['heightOfChimneyFlues'].get('requiredHeight', '')
            spec.height_of_chimney_flues_present_value_height = form_data['heightOfChimneyFlues'].get('presentValueHeight', '')
            spec.height_of_chimney_flues_required_vertical = form_data['heightOfChimneyFlues'].get('requiredVertical', '')
            spec.height_of_chimney_flues_present_value_vertical = form_data['heightOfChimneyFlues'].get('presentValueVertical', '')

        if 'lateralStability' in form_data:
            spec.lateral_stability_condition = form_data['lateralStability'].get('condition', '')
            spec.lateral_stability_comments = form_data['lateralStability'].get('comments', '')
            spec.lateral_stability_code_compliance = form_data['lateralStability'].get('codeCompliance', '')
            spec.lateral_stability_photos = form_data['lateralStability'].get('photos', [])

        if 'chimneyCaps1' in form_data:
            spec.chimney_caps_1_condition = form_data['chimneyCaps1'].get('condition', '')
            spec.chimney_caps_1_comments = form_data['chimneyCaps1'].get('comments', '')
            spec.chimney_caps_1_code_compliance = form_data['chimneyCaps1'].get('codeCompliance', '')
            spec.chimney_caps_1_photos = form_data['chimneyCaps1'].get('photos', [])

        if 'chimneyCaps2' in form_data:
            spec.chimney_caps_2_condition = form_data['chimneyCaps2'].get('condition', '')
            spec.chimney_caps_2_comments = form_data['chimneyCaps2'].get('comments', '')
            spec.chimney_caps_2_code_compliance = form_data['chimneyCaps2'].get('codeCompliance', '')
            spec.chimney_caps_2_photos = form_data['chimneyCaps2'].get('photos', [])

        if 'chimneyCaps3' in form_data:
            spec.chimney_caps_3_condition = form_data['chimneyCaps3'].get('condition', '')
            spec.chimney_caps_3_comments = form_data['chimneyCaps3'].get('comments', '')
            spec.chimney_caps_3_code_compliance = form_data['chimneyCaps3'].get('codeCompliance', '')
            spec.chimney_caps_3_photos = form_data['chimneyCaps3'].get('photos', [])

        if 'chimneyCaps4' in form_data:
            spec.chimney_caps_4_condition = form_data['chimneyCaps4'].get('condition', '')
            spec.chimney_caps_4_comments = form_data['chimneyCaps4'].get('comments', '')
            spec.chimney_caps_4_code_compliance = form_data['chimneyCaps4'].get('codeCompliance', '')
            spec.chimney_caps_4_photos = form_data['chimneyCaps4'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-stability-caps/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_chimney_stability_caps(inspection_id):
    """Get wood stove masonry chimney stability caps for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney stability caps not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-stability-caps/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_chimney_stability_caps(inspection_id):
    """Update wood stove masonry chimney stability caps for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney stability caps not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        if 'heightOfChimneyFlues' in form_data:
            spec.height_of_chimney_flues_condition = form_data['heightOfChimneyFlues'].get('condition', '')
            spec.height_of_chimney_flues_comments = form_data['heightOfChimneyFlues'].get('comments', '')
            spec.height_of_chimney_flues_code_compliance = form_data['heightOfChimneyFlues'].get('codeCompliance', '')
            spec.height_of_chimney_flues_photos = form_data['heightOfChimneyFlues'].get('photos', [])
            spec.height_of_chimney_flues_required_height = form_data['heightOfChimneyFlues'].get('requiredHeight', '')
            spec.height_of_chimney_flues_present_value_height = form_data['heightOfChimneyFlues'].get('presentValueHeight', '')
            spec.height_of_chimney_flues_required_vertical = form_data['heightOfChimneyFlues'].get('requiredVertical', '')
            spec.height_of_chimney_flues_present_value_vertical = form_data['heightOfChimneyFlues'].get('presentValueVertical', '')

        if 'lateralStability' in form_data:
            spec.lateral_stability_condition = form_data['lateralStability'].get('condition', '')
            spec.lateral_stability_comments = form_data['lateralStability'].get('comments', '')
            spec.lateral_stability_code_compliance = form_data['lateralStability'].get('codeCompliance', '')
            spec.lateral_stability_photos = form_data['lateralStability'].get('photos', [])

        if 'chimneyCaps1' in form_data:
            spec.chimney_caps_1_condition = form_data['chimneyCaps1'].get('condition', '')
            spec.chimney_caps_1_comments = form_data['chimneyCaps1'].get('comments', '')
            spec.chimney_caps_1_code_compliance = form_data['chimneyCaps1'].get('codeCompliance', '')
            spec.chimney_caps_1_photos = form_data['chimneyCaps1'].get('photos', [])

        if 'chimneyCaps2' in form_data:
            spec.chimney_caps_2_condition = form_data['chimneyCaps2'].get('condition', '')
            spec.chimney_caps_2_comments = form_data['chimneyCaps2'].get('comments', '')
            spec.chimney_caps_2_code_compliance = form_data['chimneyCaps2'].get('codeCompliance', '')
            spec.chimney_caps_2_photos = form_data['chimneyCaps2'].get('photos', [])

        if 'chimneyCaps3' in form_data:
            spec.chimney_caps_3_condition = form_data['chimneyCaps3'].get('condition', '')
            spec.chimney_caps_3_comments = form_data['chimneyCaps3'].get('comments', '')
            spec.chimney_caps_3_code_compliance = form_data['chimneyCaps3'].get('codeCompliance', '')
            spec.chimney_caps_3_photos = form_data['chimneyCaps3'].get('photos', [])

        if 'chimneyCaps4' in form_data:
            spec.chimney_caps_4_condition = form_data['chimneyCaps4'].get('condition', '')
            spec.chimney_caps_4_comments = form_data['chimneyCaps4'].get('comments', '')
            spec.chimney_caps_4_code_compliance = form_data['chimneyCaps4'].get('codeCompliance', '')
            spec.chimney_caps_4_photos = form_data['chimneyCaps4'].get('photos', [])

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-stability-caps/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_chimney_stability_caps(inspection_id):
    """Delete wood stove masonry chimney stability caps for an inspection."""
    try:
        spec = WoodStoveMasonryChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney stability caps not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry chimney stability caps deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Chimney Supports routes
@main.route('/api/wood-stove-masonry-chimney-supports', methods=['POST'])
def create_wood_stove_masonry_chimney_supports():
    """Create wood stove masonry chimney supports for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'Inspection ID is required'}), 400

        # Check if record already exists
        existing_spec = WoodStoveMasonryChimneySupports.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry chimney supports already exists for this inspection'}), 409

        spec = WoodStoveMasonryChimneySupports(inspection_id=inspection_id)

        # Map formData to model fields
        form_data = data.get('formData', {})
        if 'flashing' in form_data:
            flashing = form_data['flashing']
            spec.flashing_condition = flashing.get('condition', '')
            spec.flashing_comments = flashing.get('comments', '')
            spec.flashing_code_compliance = flashing.get('codeCompliance', '')
            spec.flashing_photos = flashing.get('photos', [])

        if 'clearanceCombustibleMaterials' in form_data:
            clearance = form_data['clearanceCombustibleMaterials']
            spec.clearance_combustible_materials_condition = clearance.get('condition', '')
            spec.clearance_combustible_materials_comments = clearance.get('comments', '')
            spec.clearance_combustible_materials_code_compliance = clearance.get('codeCompliance', '')
            spec.clearance_combustible_materials_photos = clearance.get('photos', [])

        if 'clearanceCombustibleMaterials3' in form_data:
            clearance3 = form_data['clearanceCombustibleMaterials3']
            spec.clearance_combustible_materials_3_condition = clearance3.get('condition', '')
            spec.clearance_combustible_materials_3_comments = clearance3.get('comments', '')
            spec.clearance_combustible_materials_3_code_compliance = clearance3.get('codeCompliance', '')
            spec.clearance_combustible_materials_3_photos = clearance3.get('photos', [])

        if 'sealingSpaces' in form_data:
            sealing = form_data['sealingSpaces']
            spec.sealing_spaces_condition = sealing.get('condition', '')
            spec.sealing_spaces_comments = sealing.get('comments', '')
            spec.sealing_spaces_code_compliance = sealing.get('codeCompliance', '')
            spec.sealing_spaces_photos = sealing.get('photos', [])

        if 'supportJoistsBeams' in form_data:
            support = form_data['supportJoistsBeams']
            spec.support_joists_beams_condition = support.get('condition', '')
            spec.support_joists_beams_comments = support.get('comments', '')
            spec.support_joists_beams_code_compliance = support.get('codeCompliance', '')
            spec.support_joists_beams_photos = support.get('photos', [])

        if 'inclinedChimneyFlues' in form_data:
            inclined = form_data['inclinedChimneyFlues']
            spec.inclined_chimney_flues_condition = inclined.get('condition', '')
            spec.inclined_chimney_flues_comments = inclined.get('comments', '')
            spec.inclined_chimney_flues_code_compliance = inclined.get('codeCompliance', '')
            spec.inclined_chimney_flues_photos = inclined.get('photos', [])

        if 'intersectionShingleRoofs' in form_data:
            intersection = form_data['intersectionShingleRoofs']
            spec.intersection_shingle_roofs_condition = intersection.get('condition', '')
            spec.intersection_shingle_roofs_comments = intersection.get('comments', '')
            spec.intersection_shingle_roofs_code_compliance = intersection.get('codeCompliance', '')
            spec.intersection_shingle_roofs_photos = intersection.get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-supports/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_chimney_supports(inspection_id):
    """Get wood stove masonry chimney supports for an inspection."""
    try:
        spec = WoodStoveMasonryChimneySupports.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney supports not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-supports/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_chimney_supports(inspection_id):
    """Update wood stove masonry chimney supports for an inspection."""
    try:
        spec = WoodStoveMasonryChimneySupports.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney supports not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        # Update flashing section
        if 'flashing' in form_data:
            flashing = form_data['flashing']
            spec.flashing_condition = flashing.get('condition', spec.flashing_condition)
            spec.flashing_comments = flashing.get('comments', spec.flashing_comments)
            spec.flashing_code_compliance = flashing.get('codeCompliance', spec.flashing_code_compliance)
            spec.flashing_photos = flashing.get('photos', spec.flashing_photos)

        # Update clearanceCombustibleMaterials section
        if 'clearanceCombustibleMaterials' in form_data:
            clearance = form_data['clearanceCombustibleMaterials']
            spec.clearance_combustible_materials_condition = clearance.get('condition', spec.clearance_combustible_materials_condition)
            spec.clearance_combustible_materials_comments = clearance.get('comments', spec.clearance_combustible_materials_comments)
            spec.clearance_combustible_materials_code_compliance = clearance.get('codeCompliance', spec.clearance_combustible_materials_code_compliance)
            spec.clearance_combustible_materials_photos = clearance.get('photos', spec.clearance_combustible_materials_photos)

        # Update clearanceCombustibleMaterials3 section
        if 'clearanceCombustibleMaterials3' in form_data:
            clearance3 = form_data['clearanceCombustibleMaterials3']
            spec.clearance_combustible_materials_3_condition = clearance3.get('condition', spec.clearance_combustible_materials_3_condition)
            spec.clearance_combustible_materials_3_comments = clearance3.get('comments', spec.clearance_combustible_materials_3_comments)
            spec.clearance_combustible_materials_3_code_compliance = clearance3.get('codeCompliance', spec.clearance_combustible_materials_3_code_compliance)
            spec.clearance_combustible_materials_3_photos = clearance3.get('photos', spec.clearance_combustible_materials_3_photos)

        # Update sealingSpaces section
        if 'sealingSpaces' in form_data:
            sealing = form_data['sealingSpaces']
            spec.sealing_spaces_condition = sealing.get('condition', spec.sealing_spaces_condition)
            spec.sealing_spaces_comments = sealing.get('comments', spec.sealing_spaces_comments)
            spec.sealing_spaces_code_compliance = sealing.get('codeCompliance', spec.sealing_spaces_code_compliance)
            spec.sealing_spaces_photos = sealing.get('photos', spec.sealing_spaces_photos)

        # Update supportJoistsBeams section
        if 'supportJoistsBeams' in form_data:
            support = form_data['supportJoistsBeams']
            spec.support_joists_beams_condition = support.get('condition', spec.support_joists_beams_condition)
            spec.support_joists_beams_comments = support.get('comments', spec.support_joists_beams_comments)
            spec.support_joists_beams_code_compliance = support.get('codeCompliance', spec.support_joists_beams_code_compliance)
            spec.support_joists_beams_photos = support.get('photos', spec.support_joists_beams_photos)

        # Update inclinedChimneyFlues section
        if 'inclinedChimneyFlues' in form_data:
            inclined = form_data['inclinedChimneyFlues']
            spec.inclined_chimney_flues_condition = inclined.get('condition', spec.inclined_chimney_flues_condition)
            spec.inclined_chimney_flues_comments = inclined.get('comments', spec.inclined_chimney_flues_comments)
            spec.inclined_chimney_flues_code_compliance = inclined.get('codeCompliance', spec.inclined_chimney_flues_code_compliance)
            spec.inclined_chimney_flues_photos = inclined.get('photos', spec.inclined_chimney_flues_photos)

        # Update intersectionShingleRoofs section
        if 'intersectionShingleRoofs' in form_data:
            intersection = form_data['intersectionShingleRoofs']
            spec.intersection_shingle_roofs_condition = intersection.get('condition', spec.intersection_shingle_roofs_condition)
            spec.intersection_shingle_roofs_comments = intersection.get('comments', spec.intersection_shingle_roofs_comments)
            spec.intersection_shingle_roofs_code_compliance = intersection.get('codeCompliance', spec.intersection_shingle_roofs_code_compliance)
            spec.intersection_shingle_roofs_photos = intersection.get('photos', spec.intersection_shingle_roofs_photos)

        spec.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-chimney-supports/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_chimney_supports(inspection_id):
    """Delete wood stove masonry chimney supports for an inspection."""
    try:
        spec = WoodStoveMasonryChimneySupports.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry chimney supports not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry chimney supports deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Clearances & Shielding routes
@main.route('/api/wood-stove-masonry-clearances-shielding', methods=['POST'])
def create_wood_stove_masonry_clearances_shielding():
    """Create wood stove masonry clearances shielding for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'Inspection ID is required'}), 400

        # Check if record already exists
        existing_spec = WoodStoveMasonryClearancesShielding.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry clearances shielding already exists for this inspection'}), 409

        spec = WoodStoveMasonryClearancesShielding(inspection_id=inspection_id)

        # Map formData to model fields
        form_data = data.get('formData', {})
        if 'combustibleRightSideWall' in form_data:
            section = form_data['combustibleRightSideWall']
            spec.combustible_right_side_wall_required_value_uncertified = section.get('requiredValueUncertified', '36"/ 48"')
            spec.combustible_right_side_wall_required_value_certified = section.get('requiredValueCertified', '')
            spec.combustible_right_side_wall_present_value = section.get('presentValue', '')
            spec.combustible_right_side_wall_code_compliance = section.get('codeCompliance', '')
            spec.combustible_right_side_wall_photos = section.get('photos', [])

        if 'combustibleLeftSideWall' in form_data:
            section = form_data['combustibleLeftSideWall']
            spec.combustible_left_side_wall_required_value_uncertified = section.get('requiredValueUncertified', '36"/ 48"')
            spec.combustible_left_side_wall_required_value_certified = section.get('requiredValueCertified', '')
            spec.combustible_left_side_wall_present_value = section.get('presentValue', '')
            spec.combustible_left_side_wall_code_compliance = section.get('codeCompliance', '')
            spec.combustible_left_side_wall_photos = section.get('photos', [])

        if 'combustibleRearWall' in form_data:
            section = form_data['combustibleRearWall']
            spec.combustible_rear_wall_required_value_uncertified = section.get('requiredValueUncertified', '36"/ 48"')
            spec.combustible_rear_wall_required_value_certified = section.get('requiredValueCertified', '')
            spec.combustible_rear_wall_present_value = section.get('presentValue', '')
            spec.combustible_rear_wall_code_compliance = section.get('codeCompliance', '')
            spec.combustible_rear_wall_photos = section.get('photos', [])

        if 'combustibleCornerRightSide' in form_data:
            section = form_data['combustibleCornerRightSide']
            spec.combustible_corner_right_side_required_value_uncertified = section.get('requiredValueUncertified', '36"/ 48"')
            spec.combustible_corner_right_side_required_value_certified = section.get('requiredValueCertified', '')
            spec.combustible_corner_right_side_present_value = section.get('presentValue', '')
            spec.combustible_corner_right_side_code_compliance = section.get('codeCompliance', '')
            spec.combustible_corner_right_side_photos = section.get('photos', [])

        if 'combustibleCornerLeftSide' in form_data:
            section = form_data['combustibleCornerLeftSide']
            spec.combustible_corner_left_side_required_value_uncertified = section.get('requiredValueUncertified', '36"/ 48"')
            spec.combustible_corner_left_side_required_value_certified = section.get('requiredValueCertified', '')
            spec.combustible_corner_left_side_present_value = section.get('presentValue', '')
            spec.combustible_corner_left_side_code_compliance = section.get('codeCompliance', '')
            spec.combustible_corner_left_side_photos = section.get('photos', [])

        if 'topCeiling' in form_data:
            section = form_data['topCeiling']
            spec.top_ceiling_required_value_uncertified = section.get('requiredValueUncertified', '60"')
            spec.top_ceiling_required_value_certified = section.get('requiredValueCertified', '')
            spec.top_ceiling_present_value = section.get('presentValue', '')
            spec.top_ceiling_code_compliance = section.get('codeCompliance', '')
            spec.top_ceiling_photos = section.get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-clearances-shielding/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_clearances_shielding(inspection_id):
    """Get wood stove masonry clearances shielding for an inspection."""
    try:
        spec = WoodStoveMasonryClearancesShielding.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry clearances shielding not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-clearances-shielding/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_clearances_shielding(inspection_id):
    """Update wood stove masonry clearances shielding for an inspection."""
    try:
        spec = WoodStoveMasonryClearancesShielding.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry clearances shielding not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        # Update combustibleRightSideWall section
        if 'combustibleRightSideWall' in form_data:
            section = form_data['combustibleRightSideWall']
            spec.combustible_right_side_wall_required_value_uncertified = section.get('requiredValueUncertified', spec.combustible_right_side_wall_required_value_uncertified)
            spec.combustible_right_side_wall_required_value_certified = section.get('requiredValueCertified', spec.combustible_right_side_wall_required_value_certified)
            spec.combustible_right_side_wall_present_value = section.get('presentValue', spec.combustible_right_side_wall_present_value)
            spec.combustible_right_side_wall_code_compliance = section.get('codeCompliance', spec.combustible_right_side_wall_code_compliance)
            spec.combustible_right_side_wall_photos = section.get('photos', spec.combustible_right_side_wall_photos)

        # Update combustibleLeftSideWall section
        if 'combustibleLeftSideWall' in form_data:
            section = form_data['combustibleLeftSideWall']
            spec.combustible_left_side_wall_required_value_uncertified = section.get('requiredValueUncertified', spec.combustible_left_side_wall_required_value_uncertified)
            spec.combustible_left_side_wall_required_value_certified = section.get('requiredValueCertified', spec.combustible_left_side_wall_required_value_certified)
            spec.combustible_left_side_wall_present_value = section.get('presentValue', spec.combustible_left_side_wall_present_value)
            spec.combustible_left_side_wall_code_compliance = section.get('codeCompliance', spec.combustible_left_side_wall_code_compliance)
            spec.combustible_left_side_wall_photos = section.get('photos', spec.combustible_left_side_wall_photos)

        # Update combustibleRearWall section
        if 'combustibleRearWall' in form_data:
            section = form_data['combustibleRearWall']
            spec.combustible_rear_wall_required_value_uncertified = section.get('requiredValueUncertified', spec.combustible_rear_wall_required_value_uncertified)
            spec.combustible_rear_wall_required_value_certified = section.get('requiredValueCertified', spec.combustible_rear_wall_required_value_certified)
            spec.combustible_rear_wall_present_value = section.get('presentValue', spec.combustible_rear_wall_present_value)
            spec.combustible_rear_wall_code_compliance = section.get('codeCompliance', spec.combustible_rear_wall_code_compliance)
            spec.combustible_rear_wall_photos = section.get('photos', spec.combustible_rear_wall_photos)

        # Update combustibleCornerRightSide section
        if 'combustibleCornerRightSide' in form_data:
            section = form_data['combustibleCornerRightSide']
            spec.combustible_corner_right_side_required_value_uncertified = section.get('requiredValueUncertified', spec.combustible_corner_right_side_required_value_uncertified)
            spec.combustible_corner_right_side_required_value_certified = section.get('requiredValueCertified', spec.combustible_corner_right_side_required_value_certified)
            spec.combustible_corner_right_side_present_value = section.get('presentValue', spec.combustible_corner_right_side_present_value)
            spec.combustible_corner_right_side_code_compliance = section.get('codeCompliance', spec.combustible_corner_right_side_code_compliance)
            spec.combustible_corner_right_side_photos = section.get('photos', spec.combustible_corner_right_side_photos)

        # Update combustibleCornerLeftSide section
        if 'combustibleCornerLeftSide' in form_data:
            section = form_data['combustibleCornerLeftSide']
            spec.combustible_corner_left_side_required_value_uncertified = section.get('requiredValueUncertified', spec.combustible_corner_left_side_required_value_uncertified)
            spec.combustible_corner_left_side_required_value_certified = section.get('requiredValueCertified', spec.combustible_corner_left_side_required_value_certified)
            spec.combustible_corner_left_side_present_value = section.get('presentValue', spec.combustible_corner_left_side_present_value)
            spec.combustible_corner_left_side_code_compliance = section.get('codeCompliance', spec.combustible_corner_left_side_code_compliance)
            spec.combustible_corner_left_side_photos = section.get('photos', spec.combustible_corner_left_side_photos)

        # Update topCeiling section
        if 'topCeiling' in form_data:
            section = form_data['topCeiling']
            spec.top_ceiling_required_value_uncertified = section.get('requiredValueUncertified', spec.top_ceiling_required_value_uncertified)
            spec.top_ceiling_required_value_certified = section.get('requiredValueCertified', spec.top_ceiling_required_value_certified)
            spec.top_ceiling_present_value = section.get('presentValue', spec.top_ceiling_present_value)
            spec.top_ceiling_code_compliance = section.get('codeCompliance', spec.top_ceiling_code_compliance)
            spec.top_ceiling_photos = section.get('photos', spec.top_ceiling_photos)

        spec.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-clearances-shielding/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_clearances_shielding(inspection_id):
    """Delete wood stove masonry clearances shielding for an inspection."""
    try:
        spec = WoodStoveMasonryClearancesShielding.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry clearances shielding not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry clearances shielding deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Combustible Materials routes
@main.route('/api/wood-stove-masonry-combustible-materials', methods=['POST'])
def create_wood_stove_masonry_combustible_materials():
    """Create wood stove masonry combustible materials for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'Inspection ID is required'}), 400

        # Check if record already exists
        existing_spec = WoodStoveMasonryCombustibleMaterials.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry combustible materials already exists for this inspection'}), 409

        spec = WoodStoveMasonryCombustibleMaterials(inspection_id=inspection_id)

        # Map formData to model fields
        form_data = data.get('formData', {})
        if 'outdoorCombustionAir' in form_data:
            section = form_data['outdoorCombustionAir']
            spec.outdoor_combustion_air_required_value_uncertified = section.get('requiredValueUncertified', '')
            spec.outdoor_combustion_air_required_value_certified = section.get('requiredValueCertified', '')
            spec.outdoor_combustion_air_present_value = section.get('presentValue', '')
            spec.outdoor_combustion_air_code_compliance = section.get('codeCompliance', '')
            spec.outdoor_combustion_air_photos = section.get('photos', [])

        if 'coAlarmSameRoomBCBC' in form_data:
            section = form_data['coAlarmSameRoomBCBC']
            spec.co_alarm_same_room_bcbc_required_value = section.get('requiredValue', '9.32.4.2.3 (BCBC)')
            spec.co_alarm_same_room_bcbc_present_value = section.get('presentValue', '')
            spec.co_alarm_same_room_bcbc_code_compliance = section.get('codeCompliance', '')
            spec.co_alarm_same_room_bcbc_photos = section.get('photos', [])

        if 'coAlarmSameRoomABC' in form_data:
            section = form_data['coAlarmSameRoomABC']
            spec.co_alarm_same_room_abc_required_value = section.get('requiredValue', '9.32.3.9.3 (ABC)')
            spec.co_alarm_same_room_abc_present_value = section.get('presentValue', '')
            spec.co_alarm_same_room_abc_code_compliance = section.get('codeCompliance', '')
            spec.co_alarm_same_room_abc_photos = section.get('photos', [])

        if 'coAlarmPresent' in form_data:
            section = form_data['coAlarmPresent']
            spec.co_alarm_present_required_value = section.get('requiredValue', '9.33.4.2 (OBC)')
            spec.co_alarm_present_present_value = section.get('presentValue', '')
            spec.co_alarm_present_code_compliance = section.get('codeCompliance', '')
            spec.co_alarm_present_photos = section.get('photos', [])

        if 'fluePipeConnector' in form_data:
            section = form_data['fluePipeConnector']
            spec.flue_pipe_connector_type = section.get('type', '')
            spec.flue_pipe_connector_diameter = section.get('diameter', '')
            spec.flue_pipe_connector_manufacturer = section.get('manufacturer', '')
            spec.flue_pipe_connector_model = section.get('model', '')
            spec.flue_pipe_connector_listing_agency = section.get('listingAgency', '')
            spec.flue_pipe_connector_is_listing_agency_manually_available = section.get('isListingAgencyManuallyAvailable', '')

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-combustible-materials/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_combustible_materials(inspection_id):
    """Get wood stove masonry combustible materials for an inspection."""
    try:
        spec = WoodStoveMasonryCombustibleMaterials.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry combustible materials not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-combustible-materials/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_combustible_materials(inspection_id):
    """Update wood stove masonry combustible materials for an inspection."""
    try:
        spec = WoodStoveMasonryCombustibleMaterials.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry combustible materials not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        # Update outdoorCombustionAir section
        if 'outdoorCombustionAir' in form_data:
            section = form_data['outdoorCombustionAir']
            spec.outdoor_combustion_air_required_value_uncertified = section.get('requiredValueUncertified', spec.outdoor_combustion_air_required_value_uncertified)
            spec.outdoor_combustion_air_required_value_certified = section.get('requiredValueCertified', spec.outdoor_combustion_air_required_value_certified)
            spec.outdoor_combustion_air_present_value = section.get('presentValue', spec.outdoor_combustion_air_present_value)
            spec.outdoor_combustion_air_code_compliance = section.get('codeCompliance', spec.outdoor_combustion_air_code_compliance)
            spec.outdoor_combustion_air_photos = section.get('photos', spec.outdoor_combustion_air_photos)

        # Update coAlarmSameRoomBCBC section
        if 'coAlarmSameRoomBCBC' in form_data:
            section = form_data['coAlarmSameRoomBCBC']
            spec.co_alarm_same_room_bcbc_required_value = section.get('requiredValue', spec.co_alarm_same_room_bcbc_required_value)
            spec.co_alarm_same_room_bcbc_present_value = section.get('presentValue', spec.co_alarm_same_room_bcbc_present_value)
            spec.co_alarm_same_room_bcbc_code_compliance = section.get('codeCompliance', spec.co_alarm_same_room_bcbc_code_compliance)
            spec.co_alarm_same_room_bcbc_photos = section.get('photos', spec.co_alarm_same_room_bcbc_photos)

        # Update coAlarmSameRoomABC section
        if 'coAlarmSameRoomABC' in form_data:
            section = form_data['coAlarmSameRoomABC']
            spec.co_alarm_same_room_abc_required_value = section.get('requiredValue', spec.co_alarm_same_room_abc_required_value)
            spec.co_alarm_same_room_abc_present_value = section.get('presentValue', spec.co_alarm_same_room_abc_present_value)
            spec.co_alarm_same_room_abc_code_compliance = section.get('codeCompliance', spec.co_alarm_same_room_abc_code_compliance)
            spec.co_alarm_same_room_abc_photos = section.get('photos', spec.co_alarm_same_room_abc_photos)

        # Update coAlarmPresent section
        if 'coAlarmPresent' in form_data:
            section = form_data['coAlarmPresent']
            spec.co_alarm_present_required_value = section.get('requiredValue', spec.co_alarm_present_required_value)
            spec.co_alarm_present_present_value = section.get('presentValue', spec.co_alarm_present_present_value)
            spec.co_alarm_present_code_compliance = section.get('codeCompliance', spec.co_alarm_present_code_compliance)
            spec.co_alarm_present_photos = section.get('photos', spec.co_alarm_present_photos)

        # Update fluePipeConnector section
        if 'fluePipeConnector' in form_data:
            section = form_data['fluePipeConnector']
            spec.flue_pipe_connector_type = section.get('type', spec.flue_pipe_connector_type)
            spec.flue_pipe_connector_diameter = section.get('diameter', spec.flue_pipe_connector_diameter)
            spec.flue_pipe_connector_manufacturer = section.get('manufacturer', spec.flue_pipe_connector_manufacturer)
            spec.flue_pipe_connector_model = section.get('model', spec.flue_pipe_connector_model)
            spec.flue_pipe_connector_listing_agency = section.get('listingAgency', spec.flue_pipe_connector_listing_agency)
            spec.flue_pipe_connector_is_listing_agency_manually_available = section.get('isListingAgencyManuallyAvailable', spec.flue_pipe_connector_is_listing_agency_manually_available)

        spec.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-combustible-materials/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_combustible_materials(inspection_id):
    """Delete wood stove masonry combustible materials for an inspection."""
    try:
        spec = WoodStoveMasonryCombustibleMaterials.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry combustible materials not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry combustible materials deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Ember Pad & Floor Protection routes
@main.route('/api/wood-stove-masonry-ember-pad-floor-protection', methods=['POST'])
def create_wood_stove_masonry_ember_pad_floor_protection():
    """Create wood stove masonry ember pad floor protection for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'Inspection ID is required'}), 400

        # Check if record already exists
        existing_spec = WoodStoveMasonryEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry ember pad floor protection already exists for this inspection'}), 409

        spec = WoodStoveMasonryEmberPadFloorProtection(inspection_id=inspection_id)

        # Map formData to model fields
        form_data = data.get('formData', {})
        if 'emberPadFront' in form_data:
            section = form_data['emberPadFront']
            spec.ember_pad_front_required_value_uncertified = section.get('requiredValueUncertified', 'Minimum 18"')
            spec.ember_pad_front_required_value_certified = section.get('requiredValueCertified', '')
            spec.ember_pad_front_present_value = section.get('presentValue', '')
            spec.ember_pad_front_code_compliance = section.get('codeCompliance', '')
            spec.ember_pad_front_photos = section.get('photos', [])

        if 'emberPadRear' in form_data:
            section = form_data['emberPadRear']
            spec.ember_pad_rear_required_value_uncertified = section.get('requiredValueUncertified', 'Minimum 8"')
            spec.ember_pad_rear_required_value_certified = section.get('requiredValueCertified', '')
            spec.ember_pad_rear_present_value = section.get('presentValue', '')
            spec.ember_pad_rear_code_compliance = section.get('codeCompliance', '')
            spec.ember_pad_rear_photos = section.get('photos', [])

        if 'emberPadRightSide' in form_data:
            section = form_data['emberPadRightSide']
            spec.ember_pad_right_side_required_value_uncertified = section.get('requiredValueUncertified', 'Minimum 8"')
            spec.ember_pad_right_side_required_value_certified = section.get('requiredValueCertified', '')
            spec.ember_pad_right_side_present_value = section.get('presentValue', '')
            spec.ember_pad_right_side_code_compliance = section.get('codeCompliance', '')
            spec.ember_pad_right_side_photos = section.get('photos', [])

        if 'emberPadLeftSide' in form_data:
            section = form_data['emberPadLeftSide']
            spec.ember_pad_left_side_required_value_uncertified = section.get('requiredValueUncertified', 'Minimum 8"')
            spec.ember_pad_left_side_required_value_certified = section.get('requiredValueCertified', '')
            spec.ember_pad_left_side_present_value = section.get('presentValue', '')
            spec.ember_pad_left_side_code_compliance = section.get('codeCompliance', '')
            spec.ember_pad_left_side_photos = section.get('photos', [])

        if 'radiantHeatFloorProtectionUncertified' in form_data:
            section = form_data['radiantHeatFloorProtectionUncertified']
            spec.radiant_heat_floor_protection_uncertified_present_value = section.get('presentValue', '')
            spec.radiant_heat_floor_protection_uncertified_code_compliance = section.get('codeCompliance', '')
            spec.radiant_heat_floor_protection_uncertified_photos = section.get('photos', [])

        if 'radiantHeatFloorProtectionCertified' in form_data:
            section = form_data['radiantHeatFloorProtectionCertified']
            spec.radiant_heat_floor_protection_certified_required_value = section.get('requiredValue', '')
            spec.radiant_heat_floor_protection_certified_present_value = section.get('presentValue', '')
            spec.radiant_heat_floor_protection_certified_code_compliance = section.get('codeCompliance', '')
            spec.radiant_heat_floor_protection_certified_photos = section.get('photos', [])

        if 'hazardousLocation' in form_data:
            section = form_data['hazardousLocation']
            spec.hazardous_location_present_value = section.get('presentValue', '')
            spec.hazardous_location_code_compliance = section.get('codeCompliance', '')
            spec.hazardous_location_photos = section.get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-ember-pad-floor-protection/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_ember_pad_floor_protection(inspection_id):
    """Get wood stove masonry ember pad floor protection for an inspection."""
    try:
        spec = WoodStoveMasonryEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry ember pad floor protection not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-ember-pad-floor-protection/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_ember_pad_floor_protection(inspection_id):
    """Update wood stove masonry ember pad floor protection for an inspection."""
    try:
        spec = WoodStoveMasonryEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry ember pad floor protection not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        # Update emberPadFront section
        if 'emberPadFront' in form_data:
            section = form_data['emberPadFront']
            spec.ember_pad_front_required_value_uncertified = section.get('requiredValueUncertified', spec.ember_pad_front_required_value_uncertified)
            spec.ember_pad_front_required_value_certified = section.get('requiredValueCertified', spec.ember_pad_front_required_value_certified)
            spec.ember_pad_front_present_value = section.get('presentValue', spec.ember_pad_front_present_value)
            spec.ember_pad_front_code_compliance = section.get('codeCompliance', spec.ember_pad_front_code_compliance)
            spec.ember_pad_front_photos = section.get('photos', spec.ember_pad_front_photos)

        # Update emberPadRear section
        if 'emberPadRear' in form_data:
            section = form_data['emberPadRear']
            spec.ember_pad_rear_required_value_uncertified = section.get('requiredValueUncertified', spec.ember_pad_rear_required_value_uncertified)
            spec.ember_pad_rear_required_value_certified = section.get('requiredValueCertified', spec.ember_pad_rear_required_value_certified)
            spec.ember_pad_rear_present_value = section.get('presentValue', spec.ember_pad_rear_present_value)
            spec.ember_pad_rear_code_compliance = section.get('codeCompliance', spec.ember_pad_rear_code_compliance)
            spec.ember_pad_rear_photos = section.get('photos', spec.ember_pad_rear_photos)

        # Update emberPadRightSide section
        if 'emberPadRightSide' in form_data:
            section = form_data['emberPadRightSide']
            spec.ember_pad_right_side_required_value_uncertified = section.get('requiredValueUncertified', spec.ember_pad_right_side_required_value_uncertified)
            spec.ember_pad_right_side_required_value_certified = section.get('requiredValueCertified', spec.ember_pad_right_side_required_value_certified)
            spec.ember_pad_right_side_present_value = section.get('presentValue', spec.ember_pad_right_side_present_value)
            spec.ember_pad_right_side_code_compliance = section.get('codeCompliance', spec.ember_pad_right_side_code_compliance)
            spec.ember_pad_right_side_photos = section.get('photos', spec.ember_pad_right_side_photos)

        # Update emberPadLeftSide section
        if 'emberPadLeftSide' in form_data:
            section = form_data['emberPadLeftSide']
            spec.ember_pad_left_side_required_value_uncertified = section.get('requiredValueUncertified', spec.ember_pad_left_side_required_value_uncertified)
            spec.ember_pad_left_side_required_value_certified = section.get('requiredValueCertified', spec.ember_pad_left_side_required_value_certified)
            spec.ember_pad_left_side_present_value = section.get('presentValue', spec.ember_pad_left_side_present_value)
            spec.ember_pad_left_side_code_compliance = section.get('codeCompliance', spec.ember_pad_left_side_code_compliance)
            spec.ember_pad_left_side_photos = section.get('photos', spec.ember_pad_left_side_photos)

        # Update radiantHeatFloorProtectionUncertified section
        if 'radiantHeatFloorProtectionUncertified' in form_data:
            section = form_data['radiantHeatFloorProtectionUncertified']
            spec.radiant_heat_floor_protection_uncertified_present_value = section.get('presentValue', spec.radiant_heat_floor_protection_uncertified_present_value)
            spec.radiant_heat_floor_protection_uncertified_code_compliance = section.get('codeCompliance', spec.radiant_heat_floor_protection_uncertified_code_compliance)
            spec.radiant_heat_floor_protection_uncertified_photos = section.get('photos', spec.radiant_heat_floor_protection_uncertified_photos)

        # Update radiantHeatFloorProtectionCertified section
        if 'radiantHeatFloorProtectionCertified' in form_data:
            section = form_data['radiantHeatFloorProtectionCertified']
            spec.radiant_heat_floor_protection_certified_required_value = section.get('requiredValue', spec.radiant_heat_floor_protection_certified_required_value)
            spec.radiant_heat_floor_protection_certified_present_value = section.get('presentValue', spec.radiant_heat_floor_protection_certified_present_value)
            spec.radiant_heat_floor_protection_certified_code_compliance = section.get('codeCompliance', spec.radiant_heat_floor_protection_certified_code_compliance)
            spec.radiant_heat_floor_protection_certified_photos = section.get('photos', spec.radiant_heat_floor_protection_certified_photos)

        # Update hazardousLocation section
        if 'hazardousLocation' in form_data:
            section = form_data['hazardousLocation']
            spec.hazardous_location_present_value = section.get('presentValue', spec.hazardous_location_present_value)
            spec.hazardous_location_code_compliance = section.get('codeCompliance', spec.hazardous_location_code_compliance)
            spec.hazardous_location_photos = section.get('photos', spec.hazardous_location_photos)

        spec.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-ember-pad-floor-protection/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_ember_pad_floor_protection(inspection_id):
    """Delete wood stove masonry ember pad floor protection for an inspection."""
    try:
        spec = WoodStoveMasonryEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry ember pad floor protection not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry ember pad floor protection deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Fireplace Specifications routes
@main.route('/api/wood-stove-masonry-fireplace-specifications', methods=['POST'])
def create_wood_stove_masonry_fireplace_specifications():
    """Create wood stove masonry fireplace specifications for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'Inspection ID is required'}), 400

        # Check if record already exists
        existing_spec = WoodStoveMasonryFireplaceSpecifications.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry fireplace specifications already exists for this inspection'}), 409

        spec = WoodStoveMasonryFireplaceSpecifications(inspection_id=inspection_id)

        # Map formData to model fields
        form_data = data.get('formData', {})
        spec.fireplace_make_model_serial = form_data.get('fireplaceMakeModelSerial', '')
        spec.installation_manual_available = form_data.get('installationManualAvailable', '')
        spec.certification_standard = form_data.get('certificationStandard', '')
        spec.listing_agency = form_data.get('listingAgency', '')
        spec.appliance_type = form_data.get('applianceType', '')
        spec.flu_collar_size = form_data.get('fluCollarSize', '')
        spec.fan_blower_attached = form_data.get('fanBlowerAttached', '')
        spec.comments_condition_chimney = form_data.get('commentsConditionChimney', '')
        spec.suitable = form_data.get('suitable', '')
        spec.installed_in = form_data.get('installedIn', '')
        spec.other_installed_in = form_data.get('otherInstalledIn', '')
        spec.appliance_location = form_data.get('applianceLocation', '')
        spec.other_appliance_location = form_data.get('otherApplianceLocation', '')
        spec.appliance_installed_by = form_data.get('applianceInstalledBy', '')
        spec.appliance_installed_by_unknown = form_data.get('applianceInstalledByUnknown', False)
        spec.date_of_manufacture = form_data.get('dateOfManufacture', '')

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-fireplace-specifications/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_fireplace_specifications(inspection_id):
    """Get wood stove masonry fireplace specifications for an inspection."""
    try:
        spec = WoodStoveMasonryFireplaceSpecifications.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry fireplace specifications not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-fireplace-specifications/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_fireplace_specifications(inspection_id):
    """Update wood stove masonry fireplace specifications for an inspection."""
    try:
        spec = WoodStoveMasonryFireplaceSpecifications.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry fireplace specifications not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        # Update all fields
        spec.fireplace_make_model_serial = form_data.get('fireplaceMakeModelSerial', spec.fireplace_make_model_serial)
        spec.installation_manual_available = form_data.get('installationManualAvailable', spec.installation_manual_available)
        spec.certification_standard = form_data.get('certificationStandard', spec.certification_standard)
        spec.listing_agency = form_data.get('listingAgency', spec.listing_agency)
        spec.appliance_type = form_data.get('applianceType', spec.appliance_type)
        spec.flu_collar_size = form_data.get('fluCollarSize', spec.flu_collar_size)
        spec.fan_blower_attached = form_data.get('fanBlowerAttached', spec.fan_blower_attached)
        spec.comments_condition_chimney = form_data.get('commentsConditionChimney', spec.comments_condition_chimney)
        spec.suitable = form_data.get('suitable', spec.suitable)
        spec.installed_in = form_data.get('installedIn', spec.installed_in)
        spec.other_installed_in = form_data.get('otherInstalledIn', spec.other_installed_in)
        spec.appliance_location = form_data.get('applianceLocation', spec.appliance_location)
        spec.other_appliance_location = form_data.get('otherApplianceLocation', spec.other_appliance_location)
        spec.appliance_installed_by = form_data.get('applianceInstalledBy', spec.appliance_installed_by)
        spec.appliance_installed_by_unknown = form_data.get('applianceInstalledByUnknown', spec.appliance_installed_by_unknown)
        spec.date_of_manufacture = form_data.get('dateOfManufacture', spec.date_of_manufacture)

        spec.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-fireplace-specifications/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_fireplace_specifications(inspection_id):
    """Delete wood stove masonry fireplace specifications for an inspection."""
    try:
        spec = WoodStoveMasonryFireplaceSpecifications.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry fireplace specifications not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry fireplace specifications deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Flue Pipe Orientation & Joints I routes
@main.route('/api/wood-stove-masonry-flue-pipe-orientation-joints-1', methods=['POST'])
def create_wood_stove_masonry_flue_pipe_orientation_joints_1():
    """Create wood stove masonry flue pipe orientation joints 1 for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'Inspection ID is required'}), 400

        # Check if record already exists
        existing_spec = WoodStoveMasonryFluePipeOrientationJoints1.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry flue pipe orientation joints 1 already exists for this inspection'}), 409

        spec = WoodStoveMasonryFluePipeOrientationJoints1(inspection_id=inspection_id)

        # Map formData to model fields
        form_data = data.get('formData', {})
        if 'wallClearancesRightSide' in form_data:
            section = form_data['wallClearancesRightSide']
            spec.wall_clearances_right_side_required_value_uncertified = section.get('requiredValueUncertified', 'Unshielded 18"')
            spec.wall_clearances_right_side_required_value_certified = section.get('requiredValueCertified', 'Unshielded 9"')
            spec.wall_clearances_right_side_present_value = section.get('presentValue', '')
            spec.wall_clearances_right_side_code_compliance = section.get('codeCompliance', '')
            spec.wall_clearances_right_side_photos = section.get('photos', [])

        if 'wallClearancesLeftSide' in form_data:
            section = form_data['wallClearancesLeftSide']
            spec.wall_clearances_left_side_required_value_uncertified = section.get('requiredValueUncertified', 'Unshielded 18"')
            spec.wall_clearances_left_side_required_value_certified = section.get('requiredValueCertified', 'Unshielded 9"')
            spec.wall_clearances_left_side_present_value = section.get('presentValue', '')
            spec.wall_clearances_left_side_code_compliance = section.get('codeCompliance', '')
            spec.wall_clearances_left_side_photos = section.get('photos', [])

        if 'wallClearancesRearWall' in form_data:
            section = form_data['wallClearancesRearWall']
            spec.wall_clearances_rear_wall_required_value_uncertified = section.get('requiredValueUncertified', 'Unshielded 18"')
            spec.wall_clearances_rear_wall_required_value_certified = section.get('requiredValueCertified', 'Unshielded 9"')
            spec.wall_clearances_rear_wall_present_value = section.get('presentValue', '')
            spec.wall_clearances_rear_wall_code_compliance = section.get('codeCompliance', '')
            spec.wall_clearances_rear_wall_photos = section.get('photos', [])

        if 'clearancesHorizontalPipe' in form_data:
            section = form_data['clearancesHorizontalPipe']
            spec.clearances_horizontal_pipe_required_value_uncertified = section.get('requiredValueUncertified', 'Unshielded 18"')
            spec.clearances_horizontal_pipe_required_value_certified = section.get('requiredValueCertified', 'Unshielded 9"')
            spec.clearances_horizontal_pipe_present_value = section.get('presentValue', '')
            spec.clearances_horizontal_pipe_code_compliance = section.get('codeCompliance', '')
            spec.clearances_horizontal_pipe_photos = section.get('photos', [])

        if 'clearancesCeiling' in form_data:
            section = form_data['clearancesCeiling']
            spec.clearances_ceiling_required_value_uncertified = section.get('requiredValueUncertified', 'Unshielded 18"')
            spec.clearances_ceiling_required_value_certified = section.get('requiredValueCertified', 'Unshielded 9"')
            spec.clearances_ceiling_present_value = section.get('presentValue', '')
            spec.clearances_ceiling_code_compliance = section.get('codeCompliance', '')
            spec.clearances_ceiling_photos = section.get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipe-orientation-joints-1/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_flue_pipe_orientation_joints_1(inspection_id):
    """Get wood stove masonry flue pipe orientation joints 1 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipeOrientationJoints1.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipe orientation joints 1 not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipe-orientation-joints-1/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_flue_pipe_orientation_joints_1(inspection_id):
    """Update wood stove masonry flue pipe orientation joints 1 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipeOrientationJoints1.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipe orientation joints 1 not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        # Update wallClearancesRightSide section
        if 'wallClearancesRightSide' in form_data:
            section = form_data['wallClearancesRightSide']
            spec.wall_clearances_right_side_required_value_uncertified = section.get('requiredValueUncertified', spec.wall_clearances_right_side_required_value_uncertified)
            spec.wall_clearances_right_side_required_value_certified = section.get('requiredValueCertified', spec.wall_clearances_right_side_required_value_certified)
            spec.wall_clearances_right_side_present_value = section.get('presentValue', spec.wall_clearances_right_side_present_value)
            spec.wall_clearances_right_side_code_compliance = section.get('codeCompliance', spec.wall_clearances_right_side_code_compliance)
            spec.wall_clearances_right_side_photos = section.get('photos', spec.wall_clearances_right_side_photos)

        # Update wallClearancesLeftSide section
        if 'wallClearancesLeftSide' in form_data:
            section = form_data['wallClearancesLeftSide']
            spec.wall_clearances_left_side_required_value_uncertified = section.get('requiredValueUncertified', spec.wall_clearances_left_side_required_value_uncertified)
            spec.wall_clearances_left_side_required_value_certified = section.get('requiredValueCertified', spec.wall_clearances_left_side_required_value_certified)
            spec.wall_clearances_left_side_present_value = section.get('presentValue', spec.wall_clearances_left_side_present_value)
            spec.wall_clearances_left_side_code_compliance = section.get('codeCompliance', spec.wall_clearances_left_side_code_compliance)
            spec.wall_clearances_left_side_photos = section.get('photos', spec.wall_clearances_left_side_photos)

        # Update wallClearancesRearWall section
        if 'wallClearancesRearWall' in form_data:
            section = form_data['wallClearancesRearWall']
            spec.wall_clearances_rear_wall_required_value_uncertified = section.get('requiredValueUncertified', spec.wall_clearances_rear_wall_required_value_uncertified)
            spec.wall_clearances_rear_wall_required_value_certified = section.get('requiredValueCertified', spec.wall_clearances_rear_wall_required_value_certified)
            spec.wall_clearances_rear_wall_present_value = section.get('presentValue', spec.wall_clearances_rear_wall_present_value)
            spec.wall_clearances_rear_wall_code_compliance = section.get('codeCompliance', spec.wall_clearances_rear_wall_code_compliance)
            spec.wall_clearances_rear_wall_photos = section.get('photos', spec.wall_clearances_rear_wall_photos)

        # Update clearancesHorizontalPipe section
        if 'clearancesHorizontalPipe' in form_data:
            section = form_data['clearancesHorizontalPipe']
            spec.clearances_horizontal_pipe_required_value_uncertified = section.get('requiredValueUncertified', spec.clearances_horizontal_pipe_required_value_uncertified)
            spec.clearances_horizontal_pipe_required_value_certified = section.get('requiredValueCertified', spec.clearances_horizontal_pipe_required_value_certified)
            spec.clearances_horizontal_pipe_present_value = section.get('presentValue', spec.clearances_horizontal_pipe_present_value)
            spec.clearances_horizontal_pipe_code_compliance = section.get('codeCompliance', spec.clearances_horizontal_pipe_code_compliance)
            spec.clearances_horizontal_pipe_photos = section.get('photos', spec.clearances_horizontal_pipe_photos)

        # Update clearancesCeiling section
        if 'clearancesCeiling' in form_data:
            section = form_data['clearancesCeiling']
            spec.clearances_ceiling_required_value_uncertified = section.get('requiredValueUncertified', spec.clearances_ceiling_required_value_uncertified)
            spec.clearances_ceiling_required_value_certified = section.get('requiredValueCertified', spec.clearances_ceiling_required_value_certified)
            spec.clearances_ceiling_present_value = section.get('presentValue', spec.clearances_ceiling_present_value)
            spec.clearances_ceiling_code_compliance = section.get('codeCompliance', spec.clearances_ceiling_code_compliance)
            spec.clearances_ceiling_photos = section.get('photos', spec.clearances_ceiling_photos)

        spec.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipe-orientation-joints-1/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_flue_pipe_orientation_joints_1(inspection_id):
    """Delete wood stove masonry flue pipe orientation joints 1 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipeOrientationJoints1.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipe orientation joints 1 not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry flue pipe orientation joints 1 deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Flue Pipe Orientation & Joints II routes
@main.route('/api/wood-stove-masonry-flue-pipe-orientation-joints-2', methods=['POST'])
def create_wood_stove_masonry_flue_pipe_orientation_joints_2():
    """Create wood stove masonry flue pipe orientation joints 2 for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'Inspection ID is required'}), 400

        # Check if record already exists
        existing_spec = WoodStoveMasonryFluePipeOrientationJoints2.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry flue pipe orientation joints 2 already exists for this inspection'}), 409

        spec = WoodStoveMasonryFluePipeOrientationJoints2(inspection_id=inspection_id)

        # Map formData to model fields
        form_data = data.get('formData', {})
        if 'totalLength' in form_data:
            section = form_data['totalLength']
            spec.total_length_required_value = section.get('requiredValue', 'Maximum 10\'')
            spec.total_length_present_value = section.get('presentValue', '')
            spec.total_length_code_compliance = section.get('codeCompliance', '')
            spec.total_length_photos = section.get('photos', [])

        if 'elbowsMaximum' in form_data:
            section = form_data['elbowsMaximum']
            spec.elbows_maximum_required_value = section.get('requiredValue', '180°')
            spec.elbows_maximum_present_value = section.get('presentValue', '')
            spec.elbows_maximum_code_compliance = section.get('codeCompliance', '')
            spec.elbows_maximum_photos = section.get('photos', [])

        if 'fastening' in form_data:
            section = form_data['fastening']
            spec.fastening_required_value = section.get('requiredValue', '3 screws per joint')
            spec.fastening_present_value = section.get('presentValue', '')
            spec.fastening_code_compliance = section.get('codeCompliance', '')
            spec.fastening_photos = section.get('photos', [])

        if 'allowanceForExpansion' in form_data:
            section = form_data['allowanceForExpansion']
            spec.allowance_for_expansion_required_value = section.get('requiredValue', 'Elbow/ slip adjust')
            spec.allowance_for_expansion_present_value = section.get('presentValue', '')
            spec.allowance_for_expansion_code_compliance = section.get('codeCompliance', '')
            spec.allowance_for_expansion_photos = section.get('photos', [])

        if 'fluePipeOrientation' in form_data:
            section = form_data['fluePipeOrientation']
            spec.flue_pipe_orientation_required_value = section.get('requiredValue', 'Male end down')
            spec.flue_pipe_orientation_present_value = section.get('presentValue', '')
            spec.flue_pipe_orientation_code_compliance = section.get('codeCompliance', '')
            spec.flue_pipe_orientation_photos = section.get('photos', [])

        if 'jointOverlap' in form_data:
            section = form_data['jointOverlap']
            spec.joint_overlap_required_value = section.get('requiredValue', 'Min 30 mm (1-3/16")')
            spec.joint_overlap_present_value = section.get('presentValue', '')
            spec.joint_overlap_code_compliance = section.get('codeCompliance', '')
            spec.joint_overlap_photos = section.get('photos', [])

        if 'fluePipeSlope' in form_data:
            section = form_data['fluePipeSlope']
            spec.flue_pipe_slope_required_value = section.get('requiredValue', 'Min ¼" per foot')
            spec.flue_pipe_slope_present_value = section.get('presentValue', '')
            spec.flue_pipe_slope_code_compliance = section.get('codeCompliance', '')
            spec.flue_pipe_slope_photos = section.get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipe-orientation-joints-2/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_flue_pipe_orientation_joints_2(inspection_id):
    """Get wood stove masonry flue pipe orientation joints 2 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipeOrientationJoints2.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipe orientation joints 2 not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipe-orientation-joints-2/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_flue_pipe_orientation_joints_2(inspection_id):
    """Update wood stove masonry flue pipe orientation joints 2 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipeOrientationJoints2.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipe orientation joints 2 not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        # Update totalLength section
        if 'totalLength' in form_data:
            section = form_data['totalLength']
            spec.total_length_required_value = section.get('requiredValue', spec.total_length_required_value)
            spec.total_length_present_value = section.get('presentValue', spec.total_length_present_value)
            spec.total_length_code_compliance = section.get('codeCompliance', spec.total_length_code_compliance)
            spec.total_length_photos = section.get('photos', spec.total_length_photos)

        # Update elbowsMaximum section
        if 'elbowsMaximum' in form_data:
            section = form_data['elbowsMaximum']
            spec.elbows_maximum_required_value = section.get('requiredValue', spec.elbows_maximum_required_value)
            spec.elbows_maximum_present_value = section.get('presentValue', spec.elbows_maximum_present_value)
            spec.elbows_maximum_code_compliance = section.get('codeCompliance', spec.elbows_maximum_code_compliance)
            spec.elbows_maximum_photos = section.get('photos', spec.elbows_maximum_photos)

        # Update fastening section
        if 'fastening' in form_data:
            section = form_data['fastening']
            spec.fastening_required_value = section.get('requiredValue', spec.fastening_required_value)
            spec.fastening_present_value = section.get('presentValue', spec.fastening_present_value)
            spec.fastening_code_compliance = section.get('codeCompliance', spec.fastening_code_compliance)
            spec.fastening_photos = section.get('photos', spec.fastening_photos)

        # Update allowanceForExpansion section
        if 'allowanceForExpansion' in form_data:
            section = form_data['allowanceForExpansion']
            spec.allowance_for_expansion_required_value = section.get('requiredValue', spec.allowance_for_expansion_required_value)
            spec.allowance_for_expansion_present_value = section.get('presentValue', spec.allowance_for_expansion_present_value)
            spec.allowance_for_expansion_code_compliance = section.get('codeCompliance', spec.allowance_for_expansion_code_compliance)
            spec.allowance_for_expansion_photos = section.get('photos', spec.allowance_for_expansion_photos)

        # Update fluePipeOrientation section
        if 'fluePipeOrientation' in form_data:
            section = form_data['fluePipeOrientation']
            spec.flue_pipe_orientation_required_value = section.get('requiredValue', spec.flue_pipe_orientation_required_value)
            spec.flue_pipe_orientation_present_value = section.get('presentValue', spec.flue_pipe_orientation_present_value)
            spec.flue_pipe_orientation_code_compliance = section.get('codeCompliance', spec.flue_pipe_orientation_code_compliance)
            spec.flue_pipe_orientation_photos = section.get('photos', spec.flue_pipe_orientation_photos)

        # Update jointOverlap section
        if 'jointOverlap' in form_data:
            section = form_data['jointOverlap']
            spec.joint_overlap_required_value = section.get('requiredValue', spec.joint_overlap_required_value)
            spec.joint_overlap_present_value = section.get('presentValue', spec.joint_overlap_present_value)
            spec.joint_overlap_code_compliance = section.get('codeCompliance', spec.joint_overlap_code_compliance)
            spec.joint_overlap_photos = section.get('photos', spec.joint_overlap_photos)

        # Update fluePipeSlope section
        if 'fluePipeSlope' in form_data:
            section = form_data['fluePipeSlope']
            spec.flue_pipe_slope_required_value = section.get('requiredValue', spec.flue_pipe_slope_required_value)
            spec.flue_pipe_slope_present_value = section.get('presentValue', spec.flue_pipe_slope_present_value)
            spec.flue_pipe_slope_code_compliance = section.get('codeCompliance', spec.flue_pipe_slope_code_compliance)
            spec.flue_pipe_slope_photos = section.get('photos', spec.flue_pipe_slope_photos)

        spec.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipe-orientation-joints-2/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_flue_pipe_orientation_joints_2(inspection_id):
    """Delete wood stove masonry flue pipe orientation joints 2 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipeOrientationJoints2.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipe orientation joints 2 not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry flue pipe orientation joints 2 deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Flue Pipes & Connections I routes
@main.route('/api/wood-stove-masonry-flue-pipes-connections-1', methods=['POST'])
def create_wood_stove_masonry_flue_pipes_connections_1():
    """Create wood stove masonry flue pipes connections 1 for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'Inspection ID is required'}), 400

        # Check if record already exists
        existing_spec = WoodStoveMasonryFluePipesConnections1.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry flue pipes connections 1 already exists for this inspection'}), 409

        spec = WoodStoveMasonryFluePipesConnections1(inspection_id=inspection_id)

        # Map formData to model fields
        form_data = data.get('formData', {})
        if 'material' in form_data:
            section = form_data['material']
            spec.material_required_value = section.get('requiredValue', '')
            spec.material_present_value = section.get('presentValue', '')
            spec.material_code_compliance = section.get('codeCompliance', '')
            spec.material_photos = section.get('photos', [])

        if 'minimumThickness' in form_data:
            section = form_data['minimumThickness']
            spec.minimum_thickness_required_value = section.get('requiredValue', '')
            spec.minimum_thickness_present_value = section.get('presentValue', '')
            spec.minimum_thickness_code_compliance = section.get('codeCompliance', '')
            spec.minimum_thickness_photos = section.get('photos', [])

        if 'fluePipeCondition' in form_data:
            section = form_data['fluePipeCondition']
            spec.flue_pipe_condition_required_value = section.get('requiredValue', '')
            spec.flue_pipe_condition_present_value = section.get('presentValue', '')
            spec.flue_pipe_condition_code_compliance = section.get('codeCompliance', '')
            spec.flue_pipe_condition_photos = section.get('photos', [])

        if 'pipeShieldingPresent' in form_data:
            section = form_data['pipeShieldingPresent']
            spec.pipe_shielding_present_required_value = section.get('requiredValue', '')
            spec.pipe_shielding_present_present_value = section.get('presentValue', '')
            spec.pipe_shielding_present_code_compliance = section.get('codeCompliance', '')
            spec.pipe_shielding_present_photos = section.get('photos', [])

        if 'supportHorizontalPresent' in form_data:
            section = form_data['supportHorizontalPresent']
            spec.support_horizontal_present_required_value = section.get('requiredValue', '')
            spec.support_horizontal_present_present_value = section.get('presentValue', '')
            spec.support_horizontal_present_code_compliance = section.get('codeCompliance', '')
            spec.support_horizontal_present_photos = section.get('photos', [])

        if 'barometricDamperPresent' in form_data:
            section = form_data['barometricDamperPresent']
            spec.barometric_damper_present_description = section.get('description', 'CSA B365-17: 4.4.4')
            spec.barometric_damper_present_required_value = section.get('requiredValue', '')
            spec.barometric_damper_present_present_value = section.get('presentValue', '')
            spec.barometric_damper_present_code_compliance = section.get('codeCompliance', '')
            spec.barometric_damper_present_photos = section.get('photos', [])

        if 'flueMountedHeatReducersPresent' in form_data:
            section = form_data['flueMountedHeatReducersPresent']
            spec.flue_mounted_heat_reducers_present_description = section.get('description', 'CSA B365-17: 4.4.1')
            spec.flue_mounted_heat_reducers_present_required_value = section.get('requiredValue', '')
            spec.flue_mounted_heat_reducers_present_present_value = section.get('presentValue', '')
            spec.flue_mounted_heat_reducers_present_code_compliance = section.get('codeCompliance', '')
            spec.flue_mounted_heat_reducers_present_photos = section.get('photos', [])

        if 'fluePipeThroughFloorsCeilings' in form_data:
            section = form_data['fluePipeThroughFloorsCeilings']
            spec.flue_pipe_through_floors_ceilings_required_value = section.get('requiredValue', '')
            spec.flue_pipe_through_floors_ceilings_present_value = section.get('presentValue', '')
            spec.flue_pipe_through_floors_ceilings_code_compliance = section.get('codeCompliance', '')
            spec.flue_pipe_through_floors_ceilings_photos = section.get('photos', [])

        if 'connectionToFactoryBuiltChimney' in form_data:
            section = form_data['connectionToFactoryBuiltChimney']
            spec.connection_to_factory_built_chimney_required_value = section.get('requiredValue', '')
            spec.connection_to_factory_built_chimney_present_value = section.get('presentValue', '')
            spec.connection_to_factory_built_chimney_code_compliance = section.get('codeCompliance', '')
            spec.connection_to_factory_built_chimney_photos = section.get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipes-connections-1/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_flue_pipes_connections_1(inspection_id):
    """Get wood stove masonry flue pipes connections 1 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipesConnections1.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipes connections 1 not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipes-connections-1/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_flue_pipes_connections_1(inspection_id):
    """Update wood stove masonry flue pipes connections 1 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipesConnections1.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipes connections 1 not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        # Update material section
        if 'material' in form_data:
            section = form_data['material']
            spec.material_required_value = section.get('requiredValue', spec.material_required_value)
            spec.material_present_value = section.get('presentValue', spec.material_present_value)
            spec.material_code_compliance = section.get('codeCompliance', spec.material_code_compliance)
            spec.material_photos = section.get('photos', spec.material_photos)

        # Update minimumThickness section
        if 'minimumThickness' in form_data:
            section = form_data['minimumThickness']
            spec.minimum_thickness_required_value = section.get('requiredValue', spec.minimum_thickness_required_value)
            spec.minimum_thickness_present_value = section.get('presentValue', spec.minimum_thickness_present_value)
            spec.minimum_thickness_code_compliance = section.get('codeCompliance', spec.minimum_thickness_code_compliance)
            spec.minimum_thickness_photos = section.get('photos', spec.minimum_thickness_photos)

        # Update fluePipeCondition section
        if 'fluePipeCondition' in form_data:
            section = form_data['fluePipeCondition']
            spec.flue_pipe_condition_required_value = section.get('requiredValue', spec.flue_pipe_condition_required_value)
            spec.flue_pipe_condition_present_value = section.get('presentValue', spec.flue_pipe_condition_present_value)
            spec.flue_pipe_condition_code_compliance = section.get('codeCompliance', spec.flue_pipe_condition_code_compliance)
            spec.flue_pipe_condition_photos = section.get('photos', spec.flue_pipe_condition_photos)

        # Update pipeShieldingPresent section
        if 'pipeShieldingPresent' in form_data:
            section = form_data['pipeShieldingPresent']
            spec.pipe_shielding_present_required_value = section.get('requiredValue', spec.pipe_shielding_present_required_value)
            spec.pipe_shielding_present_present_value = section.get('presentValue', spec.pipe_shielding_present_present_value)
            spec.pipe_shielding_present_code_compliance = section.get('codeCompliance', spec.pipe_shielding_present_code_compliance)
            spec.pipe_shielding_present_photos = section.get('photos', spec.pipe_shielding_present_photos)

        # Update supportHorizontalPresent section
        if 'supportHorizontalPresent' in form_data:
            section = form_data['supportHorizontalPresent']
            spec.support_horizontal_present_required_value = section.get('requiredValue', spec.support_horizontal_present_required_value)
            spec.support_horizontal_present_present_value = section.get('presentValue', spec.support_horizontal_present_present_value)
            spec.support_horizontal_present_code_compliance = section.get('codeCompliance', spec.support_horizontal_present_code_compliance)
            spec.support_horizontal_present_photos = section.get('photos', spec.support_horizontal_present_photos)

        # Update barometricDamperPresent section
        if 'barometricDamperPresent' in form_data:
            section = form_data['barometricDamperPresent']
            spec.barometric_damper_present_description = section.get('description', spec.barometric_damper_present_description)
            spec.barometric_damper_present_required_value = section.get('requiredValue', spec.barometric_damper_present_required_value)
            spec.barometric_damper_present_present_value = section.get('presentValue', spec.barometric_damper_present_present_value)
            spec.barometric_damper_present_code_compliance = section.get('codeCompliance', spec.barometric_damper_present_code_compliance)
            spec.barometric_damper_present_photos = section.get('photos', spec.barometric_damper_present_photos)

        # Update flueMountedHeatReducersPresent section
        if 'flueMountedHeatReducersPresent' in form_data:
            section = form_data['flueMountedHeatReducersPresent']
            spec.flue_mounted_heat_reducers_present_description = section.get('description', spec.flue_mounted_heat_reducers_present_description)
            spec.flue_mounted_heat_reducers_present_required_value = section.get('requiredValue', spec.flue_mounted_heat_reducers_present_required_value)
            spec.flue_mounted_heat_reducers_present_present_value = section.get('presentValue', spec.flue_mounted_heat_reducers_present_present_value)
            spec.flue_mounted_heat_reducers_present_code_compliance = section.get('codeCompliance', spec.flue_mounted_heat_reducers_present_code_compliance)
            spec.flue_mounted_heat_reducers_present_photos = section.get('photos', spec.flue_mounted_heat_reducers_present_photos)

        # Update fluePipeThroughFloorsCeilings section
        if 'fluePipeThroughFloorsCeilings' in form_data:
            section = form_data['fluePipeThroughFloorsCeilings']
            spec.flue_pipe_through_floors_ceilings_required_value = section.get('requiredValue', spec.flue_pipe_through_floors_ceilings_required_value)
            spec.flue_pipe_through_floors_ceilings_present_value = section.get('presentValue', spec.flue_pipe_through_floors_ceilings_present_value)
            spec.flue_pipe_through_floors_ceilings_code_compliance = section.get('codeCompliance', spec.flue_pipe_through_floors_ceilings_code_compliance)
            spec.flue_pipe_through_floors_ceilings_photos = section.get('photos', spec.flue_pipe_through_floors_ceilings_photos)

        # Update connectionToFactoryBuiltChimney section
        if 'connectionToFactoryBuiltChimney' in form_data:
            section = form_data['connectionToFactoryBuiltChimney']
            spec.connection_to_factory_built_chimney_required_value = section.get('requiredValue', spec.connection_to_factory_built_chimney_required_value)
            spec.connection_to_factory_built_chimney_present_value = section.get('presentValue', spec.connection_to_factory_built_chimney_present_value)
            spec.connection_to_factory_built_chimney_code_compliance = section.get('codeCompliance', spec.connection_to_factory_built_chimney_code_compliance)
            spec.connection_to_factory_built_chimney_photos = section.get('photos', spec.connection_to_factory_built_chimney_photos)

        spec.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipes-connections-1/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_flue_pipes_connections_1(inspection_id):
    """Delete wood stove masonry flue pipes connections 1 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipesConnections1.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipes connections 1 not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry flue pipes connections 1 deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Flue Pipes & Connections II routes
@main.route('/api/wood-stove-masonry-flue-pipes-connections-2', methods=['POST'])
def create_wood_stove_masonry_flue_pipes_connections_2():
    """Create wood stove masonry flue pipes connections 2 for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'Inspection ID is required'}), 400

        # Check if record already exists
        existing_spec = WoodStoveMasonryFluePipesConnections2.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry flue pipes connections 2 already exists for this inspection'}), 409

        spec = WoodStoveMasonryFluePipesConnections2(inspection_id=inspection_id)

        # Map formData to model fields
        form_data = data.get('formData', {})
        if 'chimneyFlueLimitations1' in form_data:
            section = form_data['chimneyFlueLimitations1']
            spec.chimney_flue_limitations_1_title = section.get('title', 'Chimney Flue Limitations')
            spec.chimney_flue_limitations_1_code_reference = section.get('codeReference', '9.21.2.1.')
            spec.chimney_flue_limitations_1_description = section.get('description', '(1) A chimney flue that serves a fireplace or incinerator shall not serve any other appliance.')
            spec.chimney_flue_limitations_1_condition = section.get('condition', '')
            spec.chimney_flue_limitations_1_comments = section.get('comments', '')
            spec.chimney_flue_limitations_1_code_compliance = section.get('codeCompliance', '')
            spec.chimney_flue_limitations_1_photos = section.get('photos', [])

        if 'chimneyFlueLimitations2' in form_data:
            section = form_data['chimneyFlueLimitations2']
            spec.chimney_flue_limitations_2_title = section.get('title', 'Chimney Flue Limitations')
            spec.chimney_flue_limitations_2_code_reference = section.get('codeReference', '9.21.2.1.')
            spec.chimney_flue_limitations_2_description = section.get('description', '(2) A chimney flue that serves a solid-fuel-burning appliance shall not be connected to a natural-gas or propane-fired appliance unless the solid-fuel-burning appliance is certified for such installation and the installation of both appliances meets the requirements of the relevant standards referenced in Article 9.33.5.2. appliance.')
            spec.chimney_flue_limitations_2_condition = section.get('condition', '')
            spec.chimney_flue_limitations_2_comments = section.get('comments', '')
            spec.chimney_flue_limitations_2_code_compliance = section.get('codeCompliance', '')
            spec.chimney_flue_limitations_2_photos = section.get('photos', [])

        if 'connectionsMoreThanOneAppliance1' in form_data:
            section = form_data['connectionsMoreThanOneAppliance1']
            spec.connections_more_than_one_appliance_1_title = section.get('title', 'Connections of More Than One Appliance')
            spec.connections_more_than_one_appliance_1_code_reference = section.get('codeReference', '9.21.2.2.')
            spec.connections_more_than_one_appliance_1_description = section.get('description', '(1) Except as required by Article 9.21.2.1, where two or more fuel-burning appliances are connected to the same chimney flue, the connections shall be made as described in Sentences (2) to (4) and an adequate draft shall be provided for the connected appliances in conformance with the requirements of the relevant standards listed in Subsection 9.33.10.')
            spec.connections_more_than_one_appliance_1_condition = section.get('condition', '')
            spec.connections_more_than_one_appliance_1_comments = section.get('comments', '')
            spec.connections_more_than_one_appliance_1_code_compliance = section.get('codeCompliance', '')
            spec.connections_more_than_one_appliance_1_photos = section.get('photos', [])

        if 'connectionsMoreThanOneAppliance2' in form_data:
            section = form_data['connectionsMoreThanOneAppliance2']
            spec.connections_more_than_one_appliance_2_title = section.get('title', 'Connections of More Than One Appliance')
            spec.connections_more_than_one_appliance_2_code_reference = section.get('codeReference', '9.21.2.2.')
            spec.connections_more_than_one_appliance_2_description = section.get('description', '(2) Where 2 or more fuel-burning appliances are connected to the same chimney flue, the appliances shall be located on the same storey.')
            spec.connections_more_than_one_appliance_2_condition = section.get('condition', '')
            spec.connections_more_than_one_appliance_2_comments = section.get('comments', '')
            spec.connections_more_than_one_appliance_2_code_compliance = section.get('codeCompliance', '')
            spec.connections_more_than_one_appliance_2_photos = section.get('photos', [])

        if 'connectionsMoreThanOneAppliance3' in form_data:
            section = form_data['connectionsMoreThanOneAppliance3']
            spec.connections_more_than_one_appliance_3_title = section.get('title', 'Connections of More Than One Appliance')
            spec.connections_more_than_one_appliance_3_code_reference = section.get('codeReference', '9.21.2.2.')
            spec.connections_more_than_one_appliance_3_description = section.get('description', '(3) The connection referred to in Sentence (2) for a solid-fuel-burning appliance shall be made below connections for appliances burning other fuels.\n(a) conform to Table 9.23.6.2; and\n(b) have a bearing length not less than 90mm (3 1/2").')
            spec.connections_more_than_one_appliance_3_condition = section.get('condition', '')
            spec.connections_more_than_one_appliance_3_comments = section.get('comments', '')
            spec.connections_more_than_one_appliance_3_code_compliance = section.get('codeCompliance', '')
            spec.connections_more_than_one_appliance_3_photos = section.get('photos', [])

        if 'connectionsMoreThanOneAppliance4' in form_data:
            section = form_data['connectionsMoreThanOneAppliance4']
            spec.connections_more_than_one_appliance_4_title = section.get('title', 'Connections of More Than One Appliance')
            spec.connections_more_than_one_appliance_4_code_reference = section.get('codeReference', '9.21.2.2.')
            spec.connections_more_than_one_appliance_4_description = section.get('description', '(4) The connection referred to in Sentence (2) for a liquid-fuel-burning appliance shall be made below any connections for appliances burning natural gas or propane.\n(a) conform to Table 9.23.6.2; and\n(b) have a bearing length not less than 90mm (3 1/2").')
            spec.connections_more_than_one_appliance_4_condition = section.get('condition', '')
            spec.connections_more_than_one_appliance_4_comments = section.get('comments', '')
            spec.connections_more_than_one_appliance_4_code_compliance = section.get('codeCompliance', '')
            spec.connections_more_than_one_appliance_4_photos = section.get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipes-connections-2/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_flue_pipes_connections_2(inspection_id):
    """Get wood stove masonry flue pipes connections 2 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipesConnections2.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipes connections 2 not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipes-connections-2/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_flue_pipes_connections_2(inspection_id):
    """Update wood stove masonry flue pipes connections 2 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipesConnections2.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipes connections 2 not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        # Update chimneyFlueLimitations1 section
        if 'chimneyFlueLimitations1' in form_data:
            section = form_data['chimneyFlueLimitations1']
            spec.chimney_flue_limitations_1_title = section.get('title', spec.chimney_flue_limitations_1_title)
            spec.chimney_flue_limitations_1_code_reference = section.get('codeReference', spec.chimney_flue_limitations_1_code_reference)
            spec.chimney_flue_limitations_1_description = section.get('description', spec.chimney_flue_limitations_1_description)
            spec.chimney_flue_limitations_1_condition = section.get('condition', spec.chimney_flue_limitations_1_condition)
            spec.chimney_flue_limitations_1_comments = section.get('comments', spec.chimney_flue_limitations_1_comments)
            spec.chimney_flue_limitations_1_code_compliance = section.get('codeCompliance', spec.chimney_flue_limitations_1_code_compliance)
            spec.chimney_flue_limitations_1_photos = section.get('photos', spec.chimney_flue_limitations_1_photos)

        # Update chimneyFlueLimitations2 section
        if 'chimneyFlueLimitations2' in form_data:
            section = form_data['chimneyFlueLimitations2']
            spec.chimney_flue_limitations_2_title = section.get('title', spec.chimney_flue_limitations_2_title)
            spec.chimney_flue_limitations_2_code_reference = section.get('codeReference', spec.chimney_flue_limitations_2_code_reference)
            spec.chimney_flue_limitations_2_description = section.get('description', spec.chimney_flue_limitations_2_description)
            spec.chimney_flue_limitations_2_condition = section.get('condition', spec.chimney_flue_limitations_2_condition)
            spec.chimney_flue_limitations_2_comments = section.get('comments', spec.chimney_flue_limitations_2_comments)
            spec.chimney_flue_limitations_2_code_compliance = section.get('codeCompliance', spec.chimney_flue_limitations_2_code_compliance)
            spec.chimney_flue_limitations_2_photos = section.get('photos', spec.chimney_flue_limitations_2_photos)

        # Update connectionsMoreThanOneAppliance1 section
        if 'connectionsMoreThanOneAppliance1' in form_data:
            section = form_data['connectionsMoreThanOneAppliance1']
            spec.connections_more_than_one_appliance_1_title = section.get('title', spec.connections_more_than_one_appliance_1_title)
            spec.connections_more_than_one_appliance_1_code_reference = section.get('codeReference', spec.connections_more_than_one_appliance_1_code_reference)
            spec.connections_more_than_one_appliance_1_description = section.get('description', spec.connections_more_than_one_appliance_1_description)
            spec.connections_more_than_one_appliance_1_condition = section.get('condition', spec.connections_more_than_one_appliance_1_condition)
            spec.connections_more_than_one_appliance_1_comments = section.get('comments', spec.connections_more_than_one_appliance_1_comments)
            spec.connections_more_than_one_appliance_1_code_compliance = section.get('codeCompliance', spec.connections_more_than_one_appliance_1_code_compliance)
            spec.connections_more_than_one_appliance_1_photos = section.get('photos', spec.connections_more_than_one_appliance_1_photos)

        # Update connectionsMoreThanOneAppliance2 section
        if 'connectionsMoreThanOneAppliance2' in form_data:
            section = form_data['connectionsMoreThanOneAppliance2']
            spec.connections_more_than_one_appliance_2_title = section.get('title', spec.connections_more_than_one_appliance_2_title)
            spec.connections_more_than_one_appliance_2_code_reference = section.get('codeReference', spec.connections_more_than_one_appliance_2_code_reference)
            spec.connections_more_than_one_appliance_2_description = section.get('description', spec.connections_more_than_one_appliance_2_description)
            spec.connections_more_than_one_appliance_2_condition = section.get('condition', spec.connections_more_than_one_appliance_2_condition)
            spec.connections_more_than_one_appliance_2_comments = section.get('comments', spec.connections_more_than_one_appliance_2_comments)
            spec.connections_more_than_one_appliance_2_code_compliance = section.get('codeCompliance', spec.connections_more_than_one_appliance_2_code_compliance)
            spec.connections_more_than_one_appliance_2_photos = section.get('photos', spec.connections_more_than_one_appliance_2_photos)

        # Update connectionsMoreThanOneAppliance3 section
        if 'connectionsMoreThanOneAppliance3' in form_data:
            section = form_data['connectionsMoreThanOneAppliance3']
            spec.connections_more_than_one_appliance_3_title = section.get('title', spec.connections_more_than_one_appliance_3_title)
            spec.connections_more_than_one_appliance_3_code_reference = section.get('codeReference', spec.connections_more_than_one_appliance_3_code_reference)
            spec.connections_more_than_one_appliance_3_description = section.get('description', spec.connections_more_than_one_appliance_3_description)
            spec.connections_more_than_one_appliance_3_condition = section.get('condition', spec.connections_more_than_one_appliance_3_condition)
            spec.connections_more_than_one_appliance_3_comments = section.get('comments', spec.connections_more_than_one_appliance_3_comments)
            spec.connections_more_than_one_appliance_3_code_compliance = section.get('codeCompliance', spec.connections_more_than_one_appliance_3_code_compliance)
            spec.connections_more_than_one_appliance_3_photos = section.get('photos', spec.connections_more_than_one_appliance_3_photos)

        # Update connectionsMoreThanOneAppliance4 section
        if 'connectionsMoreThanOneAppliance4' in form_data:
            section = form_data['connectionsMoreThanOneAppliance4']
            spec.connections_more_than_one_appliance_4_title = section.get('title', spec.connections_more_than_one_appliance_4_title)
            spec.connections_more_than_one_appliance_4_code_reference = section.get('codeReference', spec.connections_more_than_one_appliance_4_code_reference)
            spec.connections_more_than_one_appliance_4_description = section.get('description', spec.connections_more_than_one_appliance_4_description)
            spec.connections_more_than_one_appliance_4_condition = section.get('condition', spec.connections_more_than_one_appliance_4_condition)
            spec.connections_more_than_one_appliance_4_comments = section.get('comments', spec.connections_more_than_one_appliance_4_comments)
            spec.connections_more_than_one_appliance_4_code_compliance = section.get('codeCompliance', spec.connections_more_than_one_appliance_4_code_compliance)
            spec.connections_more_than_one_appliance_4_photos = section.get('photos', spec.connections_more_than_one_appliance_4_photos)

        spec.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-flue-pipes-connections-2/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_flue_pipes_connections_2(inspection_id):
    """Delete wood stove masonry flue pipes connections 2 for an inspection."""
    try:
        spec = WoodStoveMasonryFluePipesConnections2.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry flue pipes connections 2 not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry flue pipes connections 2 deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Wood Stove Masonry Wall Shielding & Floor Protection routes
@main.route('/api/wood-stove-masonry-wall-shielding-floor-protection', methods=['POST'])
def create_wood_stove_masonry_wall_shielding_floor_protection():
    """Create wood stove masonry wall shielding floor protection for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')
        if not inspection_id:
            return jsonify({'error': 'Inspection ID is required'}), 400

        # Check if record already exists
        existing_spec = WoodStoveMasonryWallShieldingFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Wood stove masonry wall shielding floor protection already exists for this inspection'}), 409

        spec = WoodStoveMasonryWallShieldingFloorProtection(inspection_id=inspection_id)

        # Map formData to model fields
        form_data = data.get('formData', {})
        if 'shieldingCeiling' in form_data:
            section = form_data['shieldingCeiling']
            spec.shielding_ceiling_required_value_uncertified = section.get('requiredValueUncertified', '')
            spec.shielding_ceiling_required_value_certified = section.get('requiredValueCertified', '')
            spec.shielding_ceiling_present_value = section.get('presentValue', '')
            spec.shielding_ceiling_code_compliance = section.get('codeCompliance', '')
            spec.shielding_ceiling_photos = section.get('photos', [])

        if 'wallShieldingRear' in form_data:
            section = form_data['wallShieldingRear']
            spec.wall_shielding_rear_required_value_uncertified = section.get('requiredValueUncertified', '')
            spec.wall_shielding_rear_required_value_certified = section.get('requiredValueCertified', '')
            spec.wall_shielding_rear_present_value = section.get('presentValue', '')
            spec.wall_shielding_rear_code_compliance = section.get('codeCompliance', '')
            spec.wall_shielding_rear_photos = section.get('photos', [])

        if 'wallShieldingRightSide' in form_data:
            section = form_data['wallShieldingRightSide']
            spec.wall_shielding_right_side_required_value_uncertified = section.get('requiredValueUncertified', '')
            spec.wall_shielding_right_side_required_value_certified = section.get('requiredValueCertified', '')
            spec.wall_shielding_right_side_present_value = section.get('presentValue', '')
            spec.wall_shielding_right_side_code_compliance = section.get('codeCompliance', '')
            spec.wall_shielding_right_side_photos = section.get('photos', [])

        if 'wallShieldingLeftSide' in form_data:
            section = form_data['wallShieldingLeftSide']
            spec.wall_shielding_left_side_required_value_uncertified = section.get('requiredValueUncertified', '')
            spec.wall_shielding_left_side_required_value_certified = section.get('requiredValueCertified', '')
            spec.wall_shielding_left_side_present_value = section.get('presentValue', '')
            spec.wall_shielding_left_side_code_compliance = section.get('codeCompliance', '')
            spec.wall_shielding_left_side_photos = section.get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-wall-shielding-floor-protection/<int:inspection_id>', methods=['GET'])
def get_wood_stove_masonry_wall_shielding_floor_protection(inspection_id):
    """Get wood stove masonry wall shielding floor protection for an inspection."""
    try:
        spec = WoodStoveMasonryWallShieldingFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry wall shielding floor protection not found'}), 404

        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-wall-shielding-floor-protection/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_masonry_wall_shielding_floor_protection(inspection_id):
    """Update wood stove masonry wall shielding floor protection for an inspection."""
    try:
        spec = WoodStoveMasonryWallShieldingFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry wall shielding floor protection not found'}), 404

        data = request.get_json()
        form_data = data.get('formData', {})

        # Update shieldingCeiling section
        if 'shieldingCeiling' in form_data:
            section = form_data['shieldingCeiling']
            spec.shielding_ceiling_required_value_uncertified = section.get('requiredValueUncertified', spec.shielding_ceiling_required_value_uncertified)
            spec.shielding_ceiling_required_value_certified = section.get('requiredValueCertified', spec.shielding_ceiling_required_value_certified)
            spec.shielding_ceiling_present_value = section.get('presentValue', spec.shielding_ceiling_present_value)
            spec.shielding_ceiling_code_compliance = section.get('codeCompliance', spec.shielding_ceiling_code_compliance)
            spec.shielding_ceiling_photos = section.get('photos', spec.shielding_ceiling_photos)

        # Update wallShieldingRear section
        if 'wallShieldingRear' in form_data:
            section = form_data['wallShieldingRear']
            spec.wall_shielding_rear_required_value_uncertified = section.get('requiredValueUncertified', spec.wall_shielding_rear_required_value_uncertified)
            spec.wall_shielding_rear_required_value_certified = section.get('requiredValueCertified', spec.wall_shielding_rear_required_value_certified)
            spec.wall_shielding_rear_present_value = section.get('presentValue', spec.wall_shielding_rear_present_value)
            spec.wall_shielding_rear_code_compliance = section.get('codeCompliance', spec.wall_shielding_rear_code_compliance)
            spec.wall_shielding_rear_photos = section.get('photos', spec.wall_shielding_rear_photos)

        # Update wallShieldingRightSide section
        if 'wallShieldingRightSide' in form_data:
            section = form_data['wallShieldingRightSide']
            spec.wall_shielding_right_side_required_value_uncertified = section.get('requiredValueUncertified', spec.wall_shielding_right_side_required_value_uncertified)
            spec.wall_shielding_right_side_required_value_certified = section.get('requiredValueCertified', spec.wall_shielding_right_side_required_value_certified)
            spec.wall_shielding_right_side_present_value = section.get('presentValue', spec.wall_shielding_right_side_present_value)
            spec.wall_shielding_right_side_code_compliance = section.get('codeCompliance', spec.wall_shielding_right_side_code_compliance)
            spec.wall_shielding_right_side_photos = section.get('photos', spec.wall_shielding_right_side_photos)

        # Update wallShieldingLeftSide section
        if 'wallShieldingLeftSide' in form_data:
            section = form_data['wallShieldingLeftSide']
            spec.wall_shielding_left_side_required_value_uncertified = section.get('requiredValueUncertified', spec.wall_shielding_left_side_required_value_uncertified)
            spec.wall_shielding_left_side_required_value_certified = section.get('requiredValueCertified', spec.wall_shielding_left_side_required_value_certified)
            spec.wall_shielding_left_side_present_value = section.get('presentValue', spec.wall_shielding_left_side_present_value)
            spec.wall_shielding_left_side_code_compliance = section.get('codeCompliance', spec.wall_shielding_left_side_code_compliance)
            spec.wall_shielding_left_side_photos = section.get('photos', spec.wall_shielding_left_side_photos)

        spec.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/wood-stove-masonry-wall-shielding-floor-protection/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_masonry_wall_shielding_floor_protection(inspection_id):
    """Delete wood stove masonry wall shielding floor protection for an inspection."""
    try:
        spec = WoodStoveMasonryWallShieldingFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Wood stove masonry wall shielding floor protection not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Wood stove masonry wall shielding floor protection deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Joint Details routes
@main.route('/api/masonry-joint-details', methods=['POST'])
def create_masonry_joint_details():
    """Create masonry joint details for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry joint details already exist
        existing_spec = MasonryJointDetails.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry joint details already exist for this inspection'}), 400

        # Create new masonry joint details
        spec = MasonryJointDetails(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'jointsInChimneyLiners' in form_data:
            spec.joints_in_chimney_liners_condition = form_data['jointsInChimneyLiners'].get('condition', '')
            spec.joints_in_chimney_liners_comments = form_data['jointsInChimneyLiners'].get('comments', '')
            spec.joints_in_chimney_liners_code_compliance = form_data['jointsInChimneyLiners'].get('codeCompliance', '')
            spec.joints_in_chimney_liners_photos = form_data['jointsInChimneyLiners'].get('photos', [])

        if 'installationOfChimneyLiners' in form_data:
            spec.installation_of_chimney_liners_condition = form_data['installationOfChimneyLiners'].get('condition', '')
            spec.installation_of_chimney_liners_comments = form_data['installationOfChimneyLiners'].get('comments', '')
            spec.installation_of_chimney_liners_code_compliance = form_data['installationOfChimneyLiners'].get('codeCompliance', '')
            spec.installation_of_chimney_liners_photos = form_data['installationOfChimneyLiners'].get('photos', [])

        if 'spacesBetweenLinersAndSurroundingMasonry' in form_data:
            spec.spaces_between_liners_and_surrounding_masonry_condition = form_data['spacesBetweenLinersAndSurroundingMasonry'].get('condition', '')
            spec.spaces_between_liners_and_surrounding_masonry_comments = form_data['spacesBetweenLinersAndSurroundingMasonry'].get('comments', '')
            spec.spaces_between_liners_and_surrounding_masonry_code_compliance = form_data['spacesBetweenLinersAndSurroundingMasonry'].get('codeCompliance', '')
            spec.spaces_between_liners_and_surrounding_masonry_photos = form_data['spacesBetweenLinersAndSurroundingMasonry'].get('photos', [])

        if 'mortarForChimneyLiners' in form_data:
            spec.mortar_for_chimney_liners_condition = form_data['mortarForChimneyLiners'].get('condition', '')
            spec.mortar_for_chimney_liners_comments = form_data['mortarForChimneyLiners'].get('comments', '')
            spec.mortar_for_chimney_liners_code_compliance = form_data['mortarForChimneyLiners'].get('codeCompliance', '')
            spec.mortar_for_chimney_liners_photos = form_data['mortarForChimneyLiners'].get('photos', [])

        if 'extensionOfChimneyLiners' in form_data:
            spec.extension_of_chimney_liners_condition = form_data['extensionOfChimneyLiners'].get('condition', '')
            spec.extension_of_chimney_liners_comments = form_data['extensionOfChimneyLiners'].get('comments', '')
            spec.extension_of_chimney_liners_code_compliance = form_data['extensionOfChimneyLiners'].get('codeCompliance', '')
            spec.extension_of_chimney_liners_photos = form_data['extensionOfChimneyLiners'].get('photos', [])

        if 'heightOfChimneyFlues' in form_data:
            spec.height_of_chimney_flues_condition = form_data['heightOfChimneyFlues'].get('condition', '')
            spec.height_of_chimney_flues_comments = form_data['heightOfChimneyFlues'].get('comments', '')
            spec.height_of_chimney_flues_code_compliance = form_data['heightOfChimneyFlues'].get('codeCompliance', '')
            spec.height_of_chimney_flues_photos = form_data['heightOfChimneyFlues'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-joint-details/<int:inspection_id>', methods=['GET'])
def get_masonry_joint_details(inspection_id):
    """Get masonry joint details for an inspection."""
    try:
        spec = MasonryJointDetails.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry joint details not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-joint-details/<int:inspection_id>', methods=['PUT'])
def update_masonry_joint_details(inspection_id):
    """Update masonry joint details for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryJointDetails.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry joint details not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'jointsInChimneyLiners' in form_data:
            spec.joints_in_chimney_liners_condition = form_data['jointsInChimneyLiners'].get('condition', spec.joints_in_chimney_liners_condition)
            spec.joints_in_chimney_liners_comments = form_data['jointsInChimneyLiners'].get('comments', spec.joints_in_chimney_liners_comments)
            spec.joints_in_chimney_liners_code_compliance = form_data['jointsInChimneyLiners'].get('codeCompliance', spec.joints_in_chimney_liners_code_compliance)
            spec.joints_in_chimney_liners_photos = form_data['jointsInChimneyLiners'].get('photos', spec.joints_in_chimney_liners_photos)

        if 'installationOfChimneyLiners' in form_data:
            spec.installation_of_chimney_liners_condition = form_data['installationOfChimneyLiners'].get('condition', spec.installation_of_chimney_liners_condition)
            spec.installation_of_chimney_liners_comments = form_data['installationOfChimneyLiners'].get('comments', spec.installation_of_chimney_liners_comments)
            spec.installation_of_chimney_liners_code_compliance = form_data['installationOfChimneyLiners'].get('codeCompliance', spec.installation_of_chimney_liners_code_compliance)
            spec.installation_of_chimney_liners_photos = form_data['installationOfChimneyLiners'].get('photos', spec.installation_of_chimney_liners_photos)

        if 'spacesBetweenLinersAndSurroundingMasonry' in form_data:
            spec.spaces_between_liners_and_surrounding_masonry_condition = form_data['spacesBetweenLinersAndSurroundingMasonry'].get('condition', spec.spaces_between_liners_and_surrounding_masonry_condition)
            spec.spaces_between_liners_and_surrounding_masonry_comments = form_data['spacesBetweenLinersAndSurroundingMasonry'].get('comments', spec.spaces_between_liners_and_surrounding_masonry_comments)
            spec.spaces_between_liners_and_surrounding_masonry_code_compliance = form_data['spacesBetweenLinersAndSurroundingMasonry'].get('codeCompliance', spec.spaces_between_liners_and_surrounding_masonry_code_compliance)
            spec.spaces_between_liners_and_surrounding_masonry_photos = form_data['spacesBetweenLinersAndSurroundingMasonry'].get('photos', spec.spaces_between_liners_and_surrounding_masonry_photos)

        if 'mortarForChimneyLiners' in form_data:
            spec.mortar_for_chimney_liners_condition = form_data['mortarForChimneyLiners'].get('condition', spec.mortar_for_chimney_liners_condition)
            spec.mortar_for_chimney_liners_comments = form_data['mortarForChimneyLiners'].get('comments', spec.mortar_for_chimney_liners_comments)
            spec.mortar_for_chimney_liners_code_compliance = form_data['mortarForChimneyLiners'].get('codeCompliance', spec.mortar_for_chimney_liners_code_compliance)
            spec.mortar_for_chimney_liners_photos = form_data['mortarForChimneyLiners'].get('photos', spec.mortar_for_chimney_liners_photos)

        if 'extensionOfChimneyLiners' in form_data:
            spec.extension_of_chimney_liners_condition = form_data['extensionOfChimneyLiners'].get('condition', spec.extension_of_chimney_liners_condition)
            spec.extension_of_chimney_liners_comments = form_data['extensionOfChimneyLiners'].get('comments', spec.extension_of_chimney_liners_comments)
            spec.extension_of_chimney_liners_code_compliance = form_data['extensionOfChimneyLiners'].get('codeCompliance', spec.extension_of_chimney_liners_code_compliance)
            spec.extension_of_chimney_liners_photos = form_data['extensionOfChimneyLiners'].get('photos', spec.extension_of_chimney_liners_photos)

        if 'heightOfChimneyFlues' in form_data:
            spec.height_of_chimney_flues_condition = form_data['heightOfChimneyFlues'].get('condition', spec.height_of_chimney_flues_condition)
            spec.height_of_chimney_flues_comments = form_data['heightOfChimneyFlues'].get('comments', spec.height_of_chimney_flues_comments)
            spec.height_of_chimney_flues_code_compliance = form_data['heightOfChimneyFlues'].get('codeCompliance', spec.height_of_chimney_flues_code_compliance)
            spec.height_of_chimney_flues_photos = form_data['heightOfChimneyFlues'].get('photos', spec.height_of_chimney_flues_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-joint-details/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_joint_details(inspection_id):
    """Delete masonry joint details for an inspection."""
    try:
        spec = MasonryJointDetails.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry joint details not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry joint details deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Chimney Stability Caps routes
@main.route('/api/masonry-chimney-stability-caps', methods=['POST'])
def create_masonry_chimney_stability_caps():
    """Create masonry chimney stability caps for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry chimney stability caps already exist
        existing_spec = MasonryChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry chimney stability caps already exist for this inspection'}), 400

        # Create new masonry chimney stability caps
        spec = MasonryChimneyStabilityCaps(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'lateralStability1' in form_data:
            spec.lateral_stability_1_condition = form_data['lateralStability1'].get('condition', '')
            spec.lateral_stability_1_comments = form_data['lateralStability1'].get('comments', '')
            spec.lateral_stability_1_code_compliance = form_data['lateralStability1'].get('codeCompliance', '')
            spec.lateral_stability_1_photos = form_data['lateralStability1'].get('photos', [])

        if 'lateralStability2' in form_data:
            spec.lateral_stability_2_condition = form_data['lateralStability2'].get('condition', '')
            spec.lateral_stability_2_comments = form_data['lateralStability2'].get('comments', '')
            spec.lateral_stability_2_code_compliance = form_data['lateralStability2'].get('codeCompliance', '')
            spec.lateral_stability_2_photos = form_data['lateralStability2'].get('photos', [])

        if 'chimneyCaps1' in form_data:
            spec.chimney_caps_1_condition = form_data['chimneyCaps1'].get('condition', '')
            spec.chimney_caps_1_comments = form_data['chimneyCaps1'].get('comments', '')
            spec.chimney_caps_1_code_compliance = form_data['chimneyCaps1'].get('codeCompliance', '')
            spec.chimney_caps_1_photos = form_data['chimneyCaps1'].get('photos', [])

        if 'chimneyCaps2' in form_data:
            spec.chimney_caps_2_condition = form_data['chimneyCaps2'].get('condition', '')
            spec.chimney_caps_2_comments = form_data['chimneyCaps2'].get('comments', '')
            spec.chimney_caps_2_code_compliance = form_data['chimneyCaps2'].get('codeCompliance', '')
            spec.chimney_caps_2_photos = form_data['chimneyCaps2'].get('photos', [])

        if 'chimneyCaps3' in form_data:
            spec.chimney_caps_3_condition = form_data['chimneyCaps3'].get('condition', '')
            spec.chimney_caps_3_comments = form_data['chimneyCaps3'].get('comments', '')
            spec.chimney_caps_3_code_compliance = form_data['chimneyCaps3'].get('codeCompliance', '')
            spec.chimney_caps_3_photos = form_data['chimneyCaps3'].get('photos', [])

        if 'chimneyCaps4' in form_data:
            spec.chimney_caps_4_condition = form_data['chimneyCaps4'].get('condition', '')
            spec.chimney_caps_4_comments = form_data['chimneyCaps4'].get('comments', '')
            spec.chimney_caps_4_code_compliance = form_data['chimneyCaps4'].get('codeCompliance', '')
            spec.chimney_caps_4_photos = form_data['chimneyCaps4'].get('photos', [])

        if 'flashing' in form_data:
            spec.flashing_condition = form_data['flashing'].get('condition', '')
            spec.flashing_comments = form_data['flashing'].get('comments', '')
            spec.flashing_code_compliance = form_data['flashing'].get('codeCompliance', '')
            spec.flashing_photos = form_data['flashing'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-stability-caps/<int:inspection_id>', methods=['GET'])
def get_masonry_chimney_stability_caps(inspection_id):
    """Get masonry chimney stability caps for an inspection."""
    try:
        spec = MasonryChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry chimney stability caps not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-stability-caps/<int:inspection_id>', methods=['PUT'])
def update_masonry_chimney_stability_caps(inspection_id):
    """Update masonry chimney stability caps for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry chimney stability caps not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'lateralStability1' in form_data:
            spec.lateral_stability_1_condition = form_data['lateralStability1'].get('condition', spec.lateral_stability_1_condition)
            spec.lateral_stability_1_comments = form_data['lateralStability1'].get('comments', spec.lateral_stability_1_comments)
            spec.lateral_stability_1_code_compliance = form_data['lateralStability1'].get('codeCompliance', spec.lateral_stability_1_code_compliance)
            spec.lateral_stability_1_photos = form_data['lateralStability1'].get('photos', spec.lateral_stability_1_photos)

        if 'lateralStability2' in form_data:
            spec.lateral_stability_2_condition = form_data['lateralStability2'].get('condition', spec.lateral_stability_2_condition)
            spec.lateral_stability_2_comments = form_data['lateralStability2'].get('comments', spec.lateral_stability_2_comments)
            spec.lateral_stability_2_code_compliance = form_data['lateralStability2'].get('codeCompliance', spec.lateral_stability_2_code_compliance)
            spec.lateral_stability_2_photos = form_data['lateralStability2'].get('photos', spec.lateral_stability_2_photos)

        if 'chimneyCaps1' in form_data:
            spec.chimney_caps_1_condition = form_data['chimneyCaps1'].get('condition', spec.chimney_caps_1_condition)
            spec.chimney_caps_1_comments = form_data['chimneyCaps1'].get('comments', spec.chimney_caps_1_comments)
            spec.chimney_caps_1_code_compliance = form_data['chimneyCaps1'].get('codeCompliance', spec.chimney_caps_1_code_compliance)
            spec.chimney_caps_1_photos = form_data['chimneyCaps1'].get('photos', spec.chimney_caps_1_photos)

        if 'chimneyCaps2' in form_data:
            spec.chimney_caps_2_condition = form_data['chimneyCaps2'].get('condition', spec.chimney_caps_2_condition)
            spec.chimney_caps_2_comments = form_data['chimneyCaps2'].get('comments', spec.chimney_caps_2_comments)
            spec.chimney_caps_2_code_compliance = form_data['chimneyCaps2'].get('codeCompliance', spec.chimney_caps_2_code_compliance)
            spec.chimney_caps_2_photos = form_data['chimneyCaps2'].get('photos', spec.chimney_caps_2_photos)

        if 'chimneyCaps3' in form_data:
            spec.chimney_caps_3_condition = form_data['chimneyCaps3'].get('condition', spec.chimney_caps_3_condition)
            spec.chimney_caps_3_comments = form_data['chimneyCaps3'].get('comments', spec.chimney_caps_3_comments)
            spec.chimney_caps_3_code_compliance = form_data['chimneyCaps3'].get('codeCompliance', spec.chimney_caps_3_code_compliance)
            spec.chimney_caps_3_photos = form_data['chimneyCaps3'].get('photos', spec.chimney_caps_3_photos)

        if 'chimneyCaps4' in form_data:
            spec.chimney_caps_4_condition = form_data['chimneyCaps4'].get('condition', spec.chimney_caps_4_condition)
            spec.chimney_caps_4_comments = form_data['chimneyCaps4'].get('comments', spec.chimney_caps_4_comments)
            spec.chimney_caps_4_code_compliance = form_data['chimneyCaps4'].get('codeCompliance', spec.chimney_caps_4_code_compliance)
            spec.chimney_caps_4_photos = form_data['chimneyCaps4'].get('photos', spec.chimney_caps_4_photos)

        if 'flashing' in form_data:
            spec.flashing_condition = form_data['flashing'].get('condition', spec.flashing_condition)
            spec.flashing_comments = form_data['flashing'].get('comments', spec.flashing_comments)
            spec.flashing_code_compliance = form_data['flashing'].get('codeCompliance', spec.flashing_code_compliance)
            spec.flashing_photos = form_data['flashing'].get('photos', spec.flashing_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-stability-caps/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_chimney_stability_caps(inspection_id):
    """Delete masonry chimney stability caps for an inspection."""
    try:
        spec = MasonryChimneyStabilityCaps.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry chimney stability caps not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry chimney stability caps deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Clearances Supports routes
@main.route('/api/masonry-clearances-supports', methods=['POST'])
def create_masonry_clearances_supports():
    """Create masonry clearances supports for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry clearances supports already exist
        existing_spec = MasonryClearancesSupports.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry clearances supports already exist for this inspection'}), 400

        # Create new masonry clearances supports
        spec = MasonryClearancesSupports(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'clearanceCombustible1' in form_data:
            spec.clearance_combustible_1_condition = form_data['clearanceCombustible1'].get('condition', '')
            spec.clearance_combustible_1_comments = form_data['clearanceCombustible1'].get('comments', '')
            spec.clearance_combustible_1_code_compliance = form_data['clearanceCombustible1'].get('codeCompliance', '')
            spec.clearance_combustible_1_photos = form_data['clearanceCombustible1'].get('photos', [])

        if 'clearanceCombustible2' in form_data:
            spec.clearance_combustible_2_condition = form_data['clearanceCombustible2'].get('condition', '')
            spec.clearance_combustible_2_comments = form_data['clearanceCombustible2'].get('comments', '')
            spec.clearance_combustible_2_code_compliance = form_data['clearanceCombustible2'].get('codeCompliance', '')
            spec.clearance_combustible_2_photos = form_data['clearanceCombustible2'].get('photos', [])

        if 'sealingSpaces' in form_data:
            spec.sealing_spaces_condition = form_data['sealingSpaces'].get('condition', '')
            spec.sealing_spaces_comments = form_data['sealingSpaces'].get('comments', '')
            spec.sealing_spaces_code_compliance = form_data['sealingSpaces'].get('codeCompliance', '')
            spec.sealing_spaces_photos = form_data['sealingSpaces'].get('photos', [])

        if 'supportJoistsBeams' in form_data:
            spec.support_joists_beams_condition = form_data['supportJoistsBeams'].get('condition', '')
            spec.support_joists_beams_comments = form_data['supportJoistsBeams'].get('comments', '')
            spec.support_joists_beams_code_compliance = form_data['supportJoistsBeams'].get('codeCompliance', '')
            spec.support_joists_beams_photos = form_data['supportJoistsBeams'].get('photos', [])

        if 'inclinedChimneyFlues' in form_data:
            spec.inclined_chimney_flues_condition = form_data['inclinedChimneyFlues'].get('condition', '')
            spec.inclined_chimney_flues_comments = form_data['inclinedChimneyFlues'].get('comments', '')
            spec.inclined_chimney_flues_code_compliance = form_data['inclinedChimneyFlues'].get('codeCompliance', '')
            spec.inclined_chimney_flues_photos = form_data['inclinedChimneyFlues'].get('photos', [])

        if 'intersectionShingleRoofs' in form_data:
            spec.intersection_shingle_roofs_condition = form_data['intersectionShingleRoofs'].get('condition', '')
            spec.intersection_shingle_roofs_comments = form_data['intersectionShingleRoofs'].get('comments', '')
            spec.intersection_shingle_roofs_code_compliance = form_data['intersectionShingleRoofs'].get('codeCompliance', '')
            spec.intersection_shingle_roofs_photos = form_data['intersectionShingleRoofs'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-clearances-supports/<int:inspection_id>', methods=['GET'])
def get_masonry_clearances_supports(inspection_id):
    """Get masonry clearances supports for an inspection."""
    try:
        spec = MasonryClearancesSupports.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry clearances supports not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-clearances-supports/<int:inspection_id>', methods=['PUT'])
def update_masonry_clearances_supports(inspection_id):
    """Update masonry clearances supports for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryClearancesSupports.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry clearances supports not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'clearanceCombustible1' in form_data:
            spec.clearance_combustible_1_condition = form_data['clearanceCombustible1'].get('condition', spec.clearance_combustible_1_condition)
            spec.clearance_combustible_1_comments = form_data['clearanceCombustible1'].get('comments', spec.clearance_combustible_1_comments)
            spec.clearance_combustible_1_code_compliance = form_data['clearanceCombustible1'].get('codeCompliance', spec.clearance_combustible_1_code_compliance)
            spec.clearance_combustible_1_photos = form_data['clearanceCombustible1'].get('photos', spec.clearance_combustible_1_photos)

        if 'clearanceCombustible2' in form_data:
            spec.clearance_combustible_2_condition = form_data['clearanceCombustible2'].get('condition', spec.clearance_combustible_2_condition)
            spec.clearance_combustible_2_comments = form_data['clearanceCombustible2'].get('comments', spec.clearance_combustible_2_comments)
            spec.clearance_combustible_2_code_compliance = form_data['clearanceCombustible2'].get('codeCompliance', spec.clearance_combustible_2_code_compliance)
            spec.clearance_combustible_2_photos = form_data['clearanceCombustible2'].get('photos', spec.clearance_combustible_2_photos)

        if 'sealingSpaces' in form_data:
            spec.sealing_spaces_condition = form_data['sealingSpaces'].get('condition', spec.sealing_spaces_condition)
            spec.sealing_spaces_comments = form_data['sealingSpaces'].get('comments', spec.sealing_spaces_comments)
            spec.sealing_spaces_code_compliance = form_data['sealingSpaces'].get('codeCompliance', spec.sealing_spaces_code_compliance)
            spec.sealing_spaces_photos = form_data['sealingSpaces'].get('photos', spec.sealing_spaces_photos)

        if 'supportJoistsBeams' in form_data:
            spec.support_joists_beams_condition = form_data['supportJoistsBeams'].get('condition', spec.support_joists_beams_condition)
            spec.support_joists_beams_comments = form_data['supportJoistsBeams'].get('comments', spec.support_joists_beams_comments)
            spec.support_joists_beams_code_compliance = form_data['supportJoistsBeams'].get('codeCompliance', spec.support_joists_beams_code_compliance)
            spec.support_joists_beams_photos = form_data['supportJoistsBeams'].get('photos', spec.support_joists_beams_photos)

        if 'inclinedChimneyFlues' in form_data:
            spec.inclined_chimney_flues_condition = form_data['inclinedChimneyFlues'].get('condition', spec.inclined_chimney_flues_condition)
            spec.inclined_chimney_flues_comments = form_data['inclinedChimneyFlues'].get('comments', spec.inclined_chimney_flues_comments)
            spec.inclined_chimney_flues_code_compliance = form_data['inclinedChimneyFlues'].get('codeCompliance', spec.inclined_chimney_flues_code_compliance)
            spec.inclined_chimney_flues_photos = form_data['inclinedChimneyFlues'].get('photos', spec.inclined_chimney_flues_photos)

        if 'intersectionShingleRoofs' in form_data:
            spec.intersection_shingle_roofs_condition = form_data['intersectionShingleRoofs'].get('condition', spec.intersection_shingle_roofs_condition)
            spec.intersection_shingle_roofs_comments = form_data['intersectionShingleRoofs'].get('comments', spec.intersection_shingle_roofs_comments)
            spec.intersection_shingle_roofs_code_compliance = form_data['intersectionShingleRoofs'].get('codeCompliance', spec.intersection_shingle_roofs_code_compliance)
            spec.intersection_shingle_roofs_photos = form_data['intersectionShingleRoofs'].get('photos', spec.intersection_shingle_roofs_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-clearances-supports/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_clearances_supports(inspection_id):
    """Delete masonry clearances supports for an inspection."""
    try:
        spec = MasonryClearancesSupports.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry clearances supports not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry clearances supports deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry Chimney Saddles Fire Code routes
@main.route('/api/masonry-chimney-saddles-fire-code', methods=['POST'])
def create_masonry_chimney_saddles_fire_code():
    """Create masonry chimney saddles fire code for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry chimney saddles fire code already exist
        existing_spec = MasonryChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry chimney saddles fire code already exist for this inspection'}), 400

        # Create new masonry chimney saddles fire code
        spec = MasonryChimneySaddlesFireCode(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'chimneySaddles' in form_data:
            spec.chimney_saddles_condition = form_data['chimneySaddles'].get('condition', '')
            spec.chimney_saddles_comments = form_data['chimneySaddles'].get('comments', '')
            spec.chimney_saddles_code_compliance = form_data['chimneySaddles'].get('codeCompliance', '')
            spec.chimney_saddles_photos = form_data['chimneySaddles'].get('photos', [])

        if 'fireCodeInspection' in form_data:
            spec.fire_code_inspection_condition = form_data['fireCodeInspection'].get('condition', '')
            spec.fire_code_inspection_comments = form_data['fireCodeInspection'].get('comments', '')
            spec.fire_code_inspection_code_compliance = form_data['fireCodeInspection'].get('codeCompliance', '')
            spec.fire_code_inspection_photos = form_data['fireCodeInspection'].get('photos', [])

        if 'fireCodeCleaning' in form_data:
            spec.fire_code_cleaning_condition = form_data['fireCodeCleaning'].get('condition', '')
            spec.fire_code_cleaning_comments = form_data['fireCodeCleaning'].get('comments', '')
            spec.fire_code_cleaning_code_compliance = form_data['fireCodeCleaning'].get('codeCompliance', '')
            spec.fire_code_cleaning_photos = form_data['fireCodeCleaning'].get('photos', [])

        if 'fireCodeStructural' in form_data:
            spec.fire_code_structural_condition = form_data['fireCodeStructural'].get('condition', '')
            spec.fire_code_structural_comments = form_data['fireCodeStructural'].get('comments', '')
            spec.fire_code_structural_code_compliance = form_data['fireCodeStructural'].get('codeCompliance', '')
            spec.fire_code_structural_photos = form_data['fireCodeStructural'].get('photos', [])

        if 'fireCodeOpenings' in form_data:
            spec.fire_code_openings_condition = form_data['fireCodeOpenings'].get('condition', '')
            spec.fire_code_openings_comments = form_data['fireCodeOpenings'].get('comments', '')
            spec.fire_code_openings_code_compliance = form_data['fireCodeOpenings'].get('codeCompliance', '')
            spec.fire_code_openings_photos = form_data['fireCodeOpenings'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-saddles-fire-code/<int:inspection_id>', methods=['GET'])
def get_masonry_chimney_saddles_fire_code(inspection_id):
    """Get masonry chimney saddles fire code for an inspection."""
    try:
        spec = MasonryChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry chimney saddles fire code not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-saddles-fire-code/<int:inspection_id>', methods=['PUT'])
def update_masonry_chimney_saddles_fire_code(inspection_id):
    """Update masonry chimney saddles fire code for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry chimney saddles fire code not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'chimneySaddles' in form_data:
            spec.chimney_saddles_condition = form_data['chimneySaddles'].get('condition', spec.chimney_saddles_condition)
            spec.chimney_saddles_comments = form_data['chimneySaddles'].get('comments', spec.chimney_saddles_comments)
            spec.chimney_saddles_code_compliance = form_data['chimneySaddles'].get('codeCompliance', spec.chimney_saddles_code_compliance)
            spec.chimney_saddles_photos = form_data['chimneySaddles'].get('photos', spec.chimney_saddles_photos)

        if 'fireCodeInspection' in form_data:
            spec.fire_code_inspection_condition = form_data['fireCodeInspection'].get('condition', spec.fire_code_inspection_condition)
            spec.fire_code_inspection_comments = form_data['fireCodeInspection'].get('comments', spec.fire_code_inspection_comments)
            spec.fire_code_inspection_code_compliance = form_data['fireCodeInspection'].get('codeCompliance', spec.fire_code_inspection_code_compliance)
            spec.fire_code_inspection_photos = form_data['fireCodeInspection'].get('photos', spec.fire_code_inspection_photos)

        if 'fireCodeCleaning' in form_data:
            spec.fire_code_cleaning_condition = form_data['fireCodeCleaning'].get('condition', spec.fire_code_cleaning_condition)
            spec.fire_code_cleaning_comments = form_data['fireCodeCleaning'].get('comments', spec.fire_code_cleaning_comments)
            spec.fire_code_cleaning_code_compliance = form_data['fireCodeCleaning'].get('codeCompliance', spec.fire_code_cleaning_code_compliance)
            spec.fire_code_cleaning_photos = form_data['fireCodeCleaning'].get('photos', spec.fire_code_cleaning_photos)

        if 'fireCodeStructural' in form_data:
            spec.fire_code_structural_condition = form_data['fireCodeStructural'].get('condition', spec.fire_code_structural_condition)
            spec.fire_code_structural_comments = form_data['fireCodeStructural'].get('comments', spec.fire_code_structural_comments)
            spec.fire_code_structural_code_compliance = form_data['fireCodeStructural'].get('codeCompliance', spec.fire_code_structural_code_compliance)
            spec.fire_code_structural_photos = form_data['fireCodeStructural'].get('photos', spec.fire_code_structural_photos)

        if 'fireCodeOpenings' in form_data:
            spec.fire_code_openings_condition = form_data['fireCodeOpenings'].get('condition', spec.fire_code_openings_condition)
            spec.fire_code_openings_comments = form_data['fireCodeOpenings'].get('comments', spec.fire_code_openings_comments)
            spec.fire_code_openings_code_compliance = form_data['fireCodeOpenings'].get('codeCompliance', spec.fire_code_openings_code_compliance)
            spec.fire_code_openings_photos = form_data['fireCodeOpenings'].get('photos', spec.fire_code_openings_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-chimney-saddles-fire-code/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_chimney_saddles_fire_code(inspection_id):
    """Delete masonry chimney saddles fire code for an inspection."""
    try:
        spec = MasonryChimneySaddlesFireCode.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry chimney saddles fire code not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry chimney saddles fire code deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# NEW: Masonry CO Alarms routes
@main.route('/api/masonry-co-alarms', methods=['POST'])
def create_masonry_co_alarms():
    """Create masonry CO alarms for an inspection."""
    try:
        data = request.get_json()
        inspection_id = data.get('inspection_id')

        if not inspection_id:
            return jsonify({'error': 'inspection_id is required'}), 400

        # Check if inspection exists
        inspection = Inspection.query.get(inspection_id)
        if not inspection:
            return jsonify({'error': 'Inspection not found'}), 404

        # Check if masonry CO alarms already exist
        existing_spec = MasonryCOAlarms.query.filter_by(inspection_id=inspection_id).first()
        if existing_spec:
            return jsonify({'error': 'Masonry CO alarms already exist for this inspection'}), 400

        # Create new masonry CO alarms
        spec = MasonryCOAlarms(inspection_id=inspection_id)

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'question1' in form_data:
            spec.question1_required_value = form_data['question1'].get('requiredValue', '')
            spec.question1_present_value = form_data['question1'].get('presentValue', '')
            spec.question1_code_compliance = form_data['question1'].get('codeCompliance', '')
            spec.question1_photos = form_data['question1'].get('photos', [])

        if 'question2' in form_data:
            spec.question2_required_value = form_data['question2'].get('requiredValue', '')
            spec.question2_present_value = form_data['question2'].get('presentValue', '')
            spec.question2_code_compliance = form_data['question2'].get('codeCompliance', '')
            spec.question2_photos = form_data['question2'].get('photos', [])

        if 'question3' in form_data:
            spec.question3_required_value = form_data['question3'].get('requiredValue', '')
            spec.question3_present_value = form_data['question3'].get('presentValue', '')
            spec.question3_code_compliance = form_data['question3'].get('codeCompliance', '')
            spec.question3_photos = form_data['question3'].get('photos', [])

        db.session.add(spec)
        db.session.commit()
        return jsonify(spec.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-co-alarms/<int:inspection_id>', methods=['GET'])
def get_masonry_co_alarms(inspection_id):
    """Get masonry CO alarms for an inspection."""
    try:
        spec = MasonryCOAlarms.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry CO alarms not found'}), 404
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-co-alarms/<int:inspection_id>', methods=['PUT'])
def update_masonry_co_alarms(inspection_id):
    """Update masonry CO alarms for an inspection."""
    try:
        data = request.get_json()
        spec = MasonryCOAlarms.query.filter_by(inspection_id=inspection_id).first()

        if not spec:
            return jsonify({'error': 'Masonry CO alarms not found'}), 404

        # Handle formData sections
        form_data = data.get('formData', {})

        if 'question1' in form_data:
            spec.question1_required_value = form_data['question1'].get('requiredValue', spec.question1_required_value)
            spec.question1_present_value = form_data['question1'].get('presentValue', spec.question1_present_value)
            spec.question1_code_compliance = form_data['question1'].get('codeCompliance', spec.question1_code_compliance)
            spec.question1_photos = form_data['question1'].get('photos', spec.question1_photos)

        if 'question2' in form_data:
            spec.question2_required_value = form_data['question2'].get('requiredValue', spec.question2_required_value)
            spec.question2_present_value = form_data['question2'].get('presentValue', spec.question2_present_value)
            spec.question2_code_compliance = form_data['question2'].get('codeCompliance', spec.question2_code_compliance)
            spec.question2_photos = form_data['question2'].get('photos', spec.question2_photos)

        if 'question3' in form_data:
            spec.question3_required_value = form_data['question3'].get('requiredValue', spec.question3_required_value)
            spec.question3_present_value = form_data['question3'].get('presentValue', spec.question3_present_value)
            spec.question3_code_compliance = form_data['question3'].get('codeCompliance', spec.question3_code_compliance)
            spec.question3_photos = form_data['question3'].get('photos', spec.question3_photos)

        db.session.commit()
        return jsonify(spec.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@main.route('/api/masonry-co-alarms/<int:inspection_id>', methods=['DELETE'])
def delete_masonry_co_alarms(inspection_id):
    """Delete masonry CO alarms for an inspection."""
    try:
        spec = MasonryCOAlarms.query.filter_by(inspection_id=inspection_id).first()
        if not spec:
            return jsonify({'error': 'Masonry CO alarms not found'}), 404

        db.session.delete(spec)
        db.session.commit()
        return jsonify({'message': 'Masonry CO alarms deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Chimney Components Supports routes
@main.route('/api/wood-stove-manufactured/chimney-components-supports', methods=['POST'])
def create_wood_stove_manufactured_chimney_components_supports():
    """Create wood stove manufactured chimney components supports for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedChimneyComponentsSupports.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Wood stove manufactured chimney components supports already exists for this inspection'}), 400

        components = WoodStoveManufacturedChimneyComponentsSupports(
            inspection_id=inspection_id,
            firestopping_required=data.get('firestopping_required'),
            firestopping_present=data.get('firestopping_present'),
            firestopping_compliance=data.get('firestopping_compliance'),
            firestopping_photos=data.get('firestopping_photos', []),
            ceiling_support_required=data.get('ceiling_support_required'),
            ceiling_support_present=data.get('ceiling_support_present'),
            ceiling_support_compliance=data.get('ceiling_support_compliance'),
            ceiling_support_photos=data.get('ceiling_support_photos', []),
            minimum_vertical_extension_required_uncertified=data.get('minimum_vertical_extension_required_uncertified'),
            minimum_vertical_extension_required_certified=data.get('minimum_vertical_extension_required_certified'),
            minimum_vertical_extension_present=data.get('minimum_vertical_extension_present'),
            minimum_vertical_extension_compliance=data.get('minimum_vertical_extension_compliance'),
            minimum_vertical_extension_photos=data.get('minimum_vertical_extension_photos', []),
            attic_radiation_shield_required=data.get('attic_radiation_shield_required'),
            attic_radiation_shield_present=data.get('attic_radiation_shield_present'),
            attic_radiation_shield_compliance=data.get('attic_radiation_shield_compliance'),
            attic_radiation_shield_photos=data.get('attic_radiation_shield_photos', []),
            attic_radiation_shield_above_insulation_required=data.get('attic_radiation_shield_above_insulation_required'),
            attic_radiation_shield_above_insulation_present=data.get('attic_radiation_shield_above_insulation_present'),
            attic_radiation_shield_above_insulation_compliance=data.get('attic_radiation_shield_above_insulation_compliance'),
            attic_radiation_shield_above_insulation_photos=data.get('attic_radiation_shield_above_insulation_photos', []),
            other_radiation_shields_required=data.get('other_radiation_shields_required'),
            other_radiation_shields_present=data.get('other_radiation_shields_present'),
            other_radiation_shields_compliance=data.get('other_radiation_shields_compliance'),
            other_radiation_shields_photos=data.get('other_radiation_shields_photos', []),
            enclosed_through_living_space_required=data.get('enclosed_through_living_space_required'),
            enclosed_through_living_space_present=data.get('enclosed_through_living_space_present'),
            enclosed_through_living_space_compliance=data.get('enclosed_through_living_space_compliance'),
            enclosed_through_living_space_photos=data.get('enclosed_through_living_space_photos', []),
            roof_flashing_storm_collar_required=data.get('roof_flashing_storm_collar_required'),
            roof_flashing_storm_collar_present=data.get('roof_flashing_storm_collar_present'),
            roof_flashing_storm_collar_compliance=data.get('roof_flashing_storm_collar_compliance'),
            roof_flashing_storm_collar_photos=data.get('roof_flashing_storm_collar_photos', [])
        )

        db.session.add(components)
        db.session.commit()
        return jsonify({'data': components.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/chimney-components-supports/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_chimney_components_supports(inspection_id):
    """Get wood stove manufactured chimney components supports for an inspection"""
    try:
        components = WoodStoveManufacturedChimneyComponentsSupports.query.filter_by(inspection_id=inspection_id).first()
        if not components:
            return jsonify({'error': 'Wood stove manufactured chimney components supports not found'}), 404
        return jsonify({'data': components.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/chimney-components-supports/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_chimney_components_supports(inspection_id):
    """Update wood stove manufactured chimney components supports for an inspection"""
    data = request.get_json()
    try:
        components = WoodStoveManufacturedChimneyComponentsSupports.query.filter_by(inspection_id=inspection_id).first()
        if not components:
            return jsonify({'error': 'Wood stove manufactured chimney components supports not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(components, key):
                setattr(components, key, value)

        db.session.commit()
        return jsonify({'data': components.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/chimney-components-supports/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_chimney_components_supports(inspection_id):
    """Delete wood stove manufactured chimney components supports for an inspection"""
    try:
        components = WoodStoveManufacturedChimneyComponentsSupports.query.filter_by(inspection_id=inspection_id).first()
        if not components:
            return jsonify({'error': 'Wood stove manufactured chimney components supports not found'}), 404

        db.session.delete(components)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured chimney components supports deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Chimney Inspection routes
@main.route('/api/wood-stove-manufactured/chimney-inspection', methods=['POST'])
def create_wood_stove_manufactured_chimney_inspection():
    """Create wood stove manufactured chimney inspection for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    print(f"DEBUG: Creating wood stove manufactured chimney inspection for inspection_id {inspection_id}")
    print(f"DEBUG: Received data: {data}")

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedChimneyInspection.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            print(f"DEBUG: Wood stove manufactured chimney inspection already exists for inspection {inspection_id}")
            return jsonify({'error': 'Wood stove manufactured chimney inspection already exists for this inspection'}), 400

        inspection = WoodStoveManufacturedChimneyInspection(
            inspection_id=inspection_id,
            inspection_discussed=data.get('inspection_discussed'),
            building_permits_available=data.get('building_permits_available'),
            time_of_day=data.get('time_of_day'),
            weather_conditions=data.get('weather_conditions'),
            roofing_type_material=data.get('roofing_type_material'),
            roof_accessed=data.get('roof_accessed'),
            attic_accessed=data.get('attic_accessed'),
            chimney_make_model=data.get('chimney_make_model'),
            installation_manual_available=data.get('installation_manual_available'),
            listing_agency=data.get('listing_agency'),
            uti=data.get('uti'),
            uti_unknown=data.get('uti_unknown', False),
            certification_standard=data.get('certification_standard'),
            comments_condition_suitable=data.get('comments_condition_suitable'),
            installation=data.get('installation'),
            chimney_installed_by=data.get('chimney_installed_by'),
            chimney_installed_by_unknown=data.get('chimney_installed_by_unknown', False),
            date=data.get('date')
        )

        print(f"DEBUG: Created inspection object with values:")
        for col in inspection.__table__.columns:
            name = col.name
            if name not in ('id', 'inspection_id', 'created_at', 'updated_at'):
                val = getattr(inspection, name)
                print(f"DEBUG: {name} = {val}")

        db.session.add(inspection)
        db.session.commit()
        print(f"DEBUG: Successfully created wood stove manufactured chimney inspection")
        return jsonify({'data': inspection.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: Error creating wood stove manufactured chimney inspection: {e}")
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/chimney-inspection/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_chimney_inspection(inspection_id):
    """Get wood stove manufactured chimney inspection for an inspection"""
    try:
        inspection = WoodStoveManufacturedChimneyInspection.query.filter_by(inspection_id=inspection_id).first()
        if not inspection:
            return jsonify({'error': 'Wood stove manufactured chimney inspection not found'}), 404
        return jsonify({'data': inspection.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/chimney-inspection/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_chimney_inspection(inspection_id):
    """Update wood stove manufactured chimney inspection for an inspection"""
    data = request.get_json()
    try:
        inspection = WoodStoveManufacturedChimneyInspection.query.filter_by(inspection_id=inspection_id).first()
        if not inspection:
            return jsonify({'error': 'Wood stove manufactured chimney inspection not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(inspection, key):
                setattr(inspection, key, value)

        db.session.commit()
        return jsonify({'data': inspection.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/chimney-inspection/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_chimney_inspection(inspection_id):
    """Delete wood stove manufactured chimney inspection for an inspection"""
    try:
        inspection = WoodStoveManufacturedChimneyInspection.query.filter_by(inspection_id=inspection_id).first()
        if not inspection:
            return jsonify({'error': 'Wood stove manufactured chimney inspection not found'}), 404

        db.session.delete(inspection)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured chimney inspection deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Chimney Structure Clearances routes
@main.route('/api/wood-stove-manufactured/chimney-structure-clearances', methods=['POST'])
def create_wood_stove_manufactured_chimney_structure_clearances():
    """Create wood stove manufactured chimney structure clearances for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedChimneyStructureClearances.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Wood stove manufactured chimney structure clearances already exists for this inspection'}), 400

        clearances = WoodStoveManufacturedChimneyStructureClearances(
            inspection_id=inspection_id,
            rain_cap_required=data.get('rain_cap_required'),
            rain_cap_present=data.get('rain_cap_present'),
            rain_cap_compliance=data.get('rain_cap_compliance'),
            rain_cap_photos=data.get('rain_cap_photos', []),
            rain_cap_spark_arrestor_required=data.get('rain_cap_spark_arrestor_required'),
            rain_cap_spark_arrestor_present=data.get('rain_cap_spark_arrestor_present'),
            rain_cap_spark_arrestor_compliance=data.get('rain_cap_spark_arrestor_compliance'),
            rain_cap_spark_arrestor_photos=data.get('rain_cap_spark_arrestor_photos', []),
            roof_braces_required=data.get('roof_braces_required'),
            roof_braces_present=data.get('roof_braces_present'),
            roof_braces_compliance=data.get('roof_braces_compliance'),
            roof_braces_photos=data.get('roof_braces_photos', []),
            roof_brace_solidly_anchored_required=data.get('roof_brace_solidly_anchored_required'),
            roof_brace_solidly_anchored_present=data.get('roof_brace_solidly_anchored_present'),
            roof_brace_solidly_anchored_compliance=data.get('roof_brace_solidly_anchored_compliance'),
            roof_brace_solidly_anchored_photos=data.get('roof_brace_solidly_anchored_photos', []),
            height_above_roof_surface_required=data.get('height_above_roof_surface_required'),
            height_above_roof_surface_present=data.get('height_above_roof_surface_present'),
            height_above_roof_surface_compliance=data.get('height_above_roof_surface_compliance'),
            height_above_roof_surface_photos=data.get('height_above_roof_surface_photos', []),
            height_within_3m_required=data.get('height_within_3m_required'),
            height_within_3m_present=data.get('height_within_3m_present'),
            height_within_3m_compliance=data.get('height_within_3m_compliance'),
            height_within_3m_photos=data.get('height_within_3m_photos', []),
            chimney_height_above_chase_cap_required_uncertified=data.get('chimney_height_above_chase_cap_required_uncertified'),
            chimney_height_above_chase_cap_required_certified=data.get('chimney_height_above_chase_cap_required_certified'),
            chimney_height_above_chase_cap_present=data.get('chimney_height_above_chase_cap_present'),
            chimney_height_above_chase_cap_compliance=data.get('chimney_height_above_chase_cap_compliance'),
            chimney_height_above_chase_cap_photos=data.get('chimney_height_above_chase_cap_photos', []),
            chimney_clearance_to_combustibles_required_uncertified=data.get('chimney_clearance_to_combustibles_required_uncertified'),
            chimney_clearance_to_combustibles_required_certified=data.get('chimney_clearance_to_combustibles_required_certified'),
            chimney_clearance_to_combustibles_present=data.get('chimney_clearance_to_combustibles_present'),
            chimney_clearance_to_combustibles_compliance=data.get('chimney_clearance_to_combustibles_compliance'),
            chimney_clearance_to_combustibles_photos=data.get('chimney_clearance_to_combustibles_photos', []),
            other_areas_of_chimney_enclosed_or_hidden_required=data.get('other_areas_of_chimney_enclosed_or_hidden_required'),
            other_areas_of_chimney_enclosed_or_hidden_present=data.get('other_areas_of_chimney_enclosed_or_hidden_present'),
            other_areas_of_chimney_enclosed_or_hidden_compliance=data.get('other_areas_of_chimney_enclosed_or_hidden_compliance'),
            other_areas_of_chimney_enclosed_or_hidden_photos=data.get('other_areas_of_chimney_enclosed_or_hidden_photos', [])
        )

        db.session.add(clearances)
        db.session.commit()
        return jsonify({'data': clearances.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/chimney-structure-clearances/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_chimney_structure_clearances(inspection_id):
    """Get wood stove manufactured chimney structure clearances for an inspection"""
    try:
        clearances = WoodStoveManufacturedChimneyStructureClearances.query.filter_by(inspection_id=inspection_id).first()
        if not clearances:
            return jsonify({'error': 'Wood stove manufactured chimney structure clearances not found'}), 404
        return jsonify({'data': clearances.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/chimney-structure-clearances/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_chimney_structure_clearances(inspection_id):
    """Update wood stove manufactured chimney structure clearances for an inspection"""
    data = request.get_json()
    try:
        clearances = WoodStoveManufacturedChimneyStructureClearances.query.filter_by(inspection_id=inspection_id).first()
        if not clearances:
            return jsonify({'error': 'Wood stove manufactured chimney structure clearances not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(clearances, key):
                setattr(clearances, key, value)

        db.session.commit()
        return jsonify({'data': clearances.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/chimney-structure-clearances/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_chimney_structure_clearances(inspection_id):
    """Delete wood stove manufactured chimney structure clearances for an inspection"""
    try:
        clearances = WoodStoveManufacturedChimneyStructureClearances.query.filter_by(inspection_id=inspection_id).first()
        if not clearances:
            return jsonify({'error': 'Wood stove manufactured chimney structure clearances not found'}), 404

        db.session.delete(clearances)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured chimney structure clearances deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Clearances Shielding routes
@main.route('/api/wood-stove-manufactured/clearances-shielding', methods=['POST'])
def create_wood_stove_manufactured_clearances_shielding():
    """Create wood stove manufactured clearances shielding for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedClearancesShielding.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Wood stove manufactured clearances shielding already exists for this inspection'}), 400

        clearances_shielding = WoodStoveManufacturedClearancesShielding(
            inspection_id=inspection_id,
            combustible_right_side_wall_required=data.get('combustible_right_side_wall_required'),
            combustible_right_side_wall_present=data.get('combustible_right_side_wall_present'),
            combustible_right_side_wall_compliance=data.get('combustible_right_side_wall_compliance'),
            combustible_right_side_wall_photos=data.get('combustible_right_side_wall_photos', []),
            combustible_left_side_wall_required=data.get('combustible_left_side_wall_required'),
            combustible_left_side_wall_present=data.get('combustible_left_side_wall_present'),
            combustible_left_side_wall_compliance=data.get('combustible_left_side_wall_compliance'),
            combustible_left_side_wall_photos=data.get('combustible_left_side_wall_photos', []),
            combustible_rear_wall_required=data.get('combustible_rear_wall_required'),
            combustible_rear_wall_present=data.get('combustible_rear_wall_present'),
            combustible_rear_wall_compliance=data.get('combustible_rear_wall_compliance'),
            combustible_rear_wall_photos=data.get('combustible_rear_wall_photos', []),
            combustible_corner_right_side_required=data.get('combustible_corner_right_side_required'),
            combustible_corner_right_side_present=data.get('combustible_corner_right_side_present'),
            combustible_corner_right_side_compliance=data.get('combustible_corner_right_side_compliance'),
            combustible_corner_right_side_photos=data.get('combustible_corner_right_side_photos', []),
            combustible_corner_left_side_required=data.get('combustible_corner_left_side_required'),
            combustible_corner_left_side_present=data.get('combustible_corner_left_side_present'),
            combustible_corner_left_side_compliance=data.get('combustible_corner_left_side_compliance'),
            combustible_corner_left_side_photos=data.get('combustible_corner_left_side_photos', []),
            top_ceiling_required=data.get('top_ceiling_required'),
            top_ceiling_present=data.get('top_ceiling_present'),
            top_ceiling_compliance=data.get('top_ceiling_compliance'),
            top_ceiling_photos=data.get('top_ceiling_photos', []),
            shielding_ceiling_required=data.get('shielding_ceiling_required'),
            shielding_ceiling_present=data.get('shielding_ceiling_present'),
            shielding_ceiling_compliance=data.get('shielding_ceiling_compliance'),
            shielding_ceiling_photos=data.get('shielding_ceiling_photos', []),
            wall_shielding_rear_required=data.get('wall_shielding_rear_required'),
            wall_shielding_rear_present=data.get('wall_shielding_rear_present'),
            wall_shielding_rear_compliance=data.get('wall_shielding_rear_compliance'),
            wall_shielding_rear_photos=data.get('wall_shielding_rear_photos', []),
            wall_shielding_right_side_required=data.get('wall_shielding_right_side_required'),
            wall_shielding_right_side_present=data.get('wall_shielding_right_side_present'),
            wall_shielding_right_side_compliance=data.get('wall_shielding_right_side_compliance'),
            wall_shielding_right_side_photos=data.get('wall_shielding_right_side_photos', []),
            wall_shielding_left_side_required=data.get('wall_shielding_left_side_required'),
            wall_shielding_left_side_present=data.get('wall_shielding_left_side_present'),
            wall_shielding_left_side_compliance=data.get('wall_shielding_left_side_compliance'),
            wall_shielding_left_side_photos=data.get('wall_shielding_left_side_photos', [])
        )

        db.session.add(clearances_shielding)
        db.session.commit()
        return jsonify({'data': clearances_shielding.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/clearances-shielding/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_clearances_shielding(inspection_id):
    """Get wood stove manufactured clearances shielding for an inspection"""
    try:
        clearances_shielding = WoodStoveManufacturedClearancesShielding.query.filter_by(inspection_id=inspection_id).first()
        if not clearances_shielding:
            return jsonify({'error': 'Wood stove manufactured clearances shielding not found'}), 404
        return jsonify({'data': clearances_shielding.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/clearances-shielding/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_clearances_shielding(inspection_id):
    """Update wood stove manufactured clearances shielding for an inspection"""
    data = request.get_json()
    try:
        clearances_shielding = WoodStoveManufacturedClearancesShielding.query.filter_by(inspection_id=inspection_id).first()
        if not clearances_shielding:
            return jsonify({'error': 'Wood stove manufactured clearances shielding not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(clearances_shielding, key):
                setattr(clearances_shielding, key, value)

        db.session.commit()
        return jsonify({'data': clearances_shielding.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/clearances-shielding/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_clearances_shielding(inspection_id):
    """Delete wood stove manufactured clearances shielding for an inspection"""
    try:
        clearances_shielding = WoodStoveManufacturedClearancesShielding.query.filter_by(inspection_id=inspection_id).first()
        if not clearances_shielding:
            return jsonify({'error': 'Wood stove manufactured clearances shielding not found'}), 404

        db.session.delete(clearances_shielding)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured clearances shielding deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Combustion Air CO Alarm routes
@main.route('/api/wood-stove-manufactured/combustion-air-co-alarm', methods=['POST'])
def create_wood_stove_manufactured_combustion_air_co_alarm():
    """Create wood stove manufactured combustion air co alarm for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedCombustionAirCOAlarm.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Wood stove manufactured combustion air co alarm already exists for this inspection'}), 400

        combustion_air_co_alarm = WoodStoveManufacturedCombustionAirCOAlarm(
            inspection_id=inspection_id,
            outdoor_combustion_air_required_uncertified=data.get('outdoor_combustion_air_required_uncertified'),
            outdoor_combustion_air_required_certified=data.get('outdoor_combustion_air_required_certified'),
            outdoor_combustion_air_present=data.get('outdoor_combustion_air_present'),
            outdoor_combustion_air_compliance=data.get('outdoor_combustion_air_compliance'),
            outdoor_combustion_air_photos=data.get('outdoor_combustion_air_photos', []),
            co_alarm_solid_fuel_bcbc_required=data.get('co_alarm_solid_fuel_bcbc_required'),
            co_alarm_solid_fuel_bcbc_present=data.get('co_alarm_solid_fuel_bcbc_present'),
            co_alarm_solid_fuel_bcbc_compliance=data.get('co_alarm_solid_fuel_bcbc_compliance'),
            co_alarm_solid_fuel_bcbc_photos=data.get('co_alarm_solid_fuel_bcbc_photos', []),
            co_alarm_solid_fuel_abc_required=data.get('co_alarm_solid_fuel_abc_required'),
            co_alarm_solid_fuel_abc_present=data.get('co_alarm_solid_fuel_abc_present'),
            co_alarm_solid_fuel_abc_compliance=data.get('co_alarm_solid_fuel_abc_compliance'),
            co_alarm_solid_fuel_abc_photos=data.get('co_alarm_solid_fuel_abc_photos', []),
            co_alarm_present_required=data.get('co_alarm_present_required'),
            co_alarm_present_present=data.get('co_alarm_present_present'),
            co_alarm_present_compliance=data.get('co_alarm_present_compliance'),
            co_alarm_present_photos=data.get('co_alarm_present_photos', [])
        )

        db.session.add(combustion_air_co_alarm)
        db.session.commit()
        return jsonify({'data': combustion_air_co_alarm.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/combustion-air-co-alarm/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_combustion_air_co_alarm(inspection_id):
    """Get wood stove manufactured combustion air co alarm for an inspection"""
    try:
        combustion_air_co_alarm = WoodStoveManufacturedCombustionAirCOAlarm.query.filter_by(inspection_id=inspection_id).first()
        if not combustion_air_co_alarm:
            return jsonify({'error': 'Wood stove manufactured combustion air co alarm not found'}), 404
        return jsonify({'data': combustion_air_co_alarm.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/combustion-air-co-alarm/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_combustion_air_co_alarm(inspection_id):
    """Update wood stove manufactured combustion air co alarm for an inspection"""
    data = request.get_json()
    try:
        combustion_air_co_alarm = WoodStoveManufacturedCombustionAirCOAlarm.query.filter_by(inspection_id=inspection_id).first()
        if not combustion_air_co_alarm:
            return jsonify({'error': 'Wood stove manufactured combustion air co alarm not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(combustion_air_co_alarm, key):
                setattr(combustion_air_co_alarm, key, value)

        db.session.commit()
        return jsonify({'data': combustion_air_co_alarm.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/combustion-air-co-alarm/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_combustion_air_co_alarm(inspection_id):
    """Delete wood stove manufactured combustion air co alarm for an inspection"""
    try:
        combustion_air_co_alarm = WoodStoveManufacturedCombustionAirCOAlarm.query.filter_by(inspection_id=inspection_id).first()
        if not combustion_air_co_alarm:
            return jsonify({'error': 'Wood stove manufactured combustion air co alarm not found'}), 404

        db.session.delete(combustion_air_co_alarm)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured combustion air co alarm deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Ember Pad Floor Protection routes
@main.route('/api/wood-stove-manufactured/ember-pad-floor-protection', methods=['POST'])
def create_wood_stove_manufactured_ember_pad_floor_protection():
    """Create wood stove manufactured ember pad floor protection for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Wood stove manufactured ember pad floor protection already exists for this inspection'}), 400

        ember_pad_floor_protection = WoodStoveManufacturedEmberPadFloorProtection(
            inspection_id=inspection_id,
            ember_pad_front_description=data.get('ember_pad_front_description'),
            ember_pad_front_required_uncertified=data.get('ember_pad_front_required_uncertified'),
            ember_pad_front_required_certified=data.get('ember_pad_front_required_certified'),
            ember_pad_front_present=data.get('ember_pad_front_present'),
            ember_pad_front_compliance=data.get('ember_pad_front_compliance'),
            ember_pad_front_photos=data.get('ember_pad_front_photos', []),
            ember_pad_rear_required_uncertified=data.get('ember_pad_rear_required_uncertified'),
            ember_pad_rear_required_certified=data.get('ember_pad_rear_required_certified'),
            ember_pad_rear_present=data.get('ember_pad_rear_present'),
            ember_pad_rear_compliance=data.get('ember_pad_rear_compliance'),
            ember_pad_rear_photos=data.get('ember_pad_rear_photos', []),
            ember_pad_right_side_required_uncertified=data.get('ember_pad_right_side_required_uncertified'),
            ember_pad_right_side_required_certified=data.get('ember_pad_right_side_required_certified'),
            ember_pad_right_side_present=data.get('ember_pad_right_side_present'),
            ember_pad_right_side_compliance=data.get('ember_pad_right_side_compliance'),
            ember_pad_right_side_photos=data.get('ember_pad_right_side_photos', []),
            ember_pad_left_side_required_uncertified=data.get('ember_pad_left_side_required_uncertified'),
            ember_pad_left_side_required_certified=data.get('ember_pad_left_side_required_certified'),
            ember_pad_left_side_present=data.get('ember_pad_left_side_present'),
            ember_pad_left_side_compliance=data.get('ember_pad_left_side_compliance'),
            ember_pad_left_side_photos=data.get('ember_pad_left_side_photos', []),
            radiant_heat_floor_protection_uncertified_required=data.get('radiant_heat_floor_protection_uncertified_required'),
            radiant_heat_floor_protection_uncertified_present=data.get('radiant_heat_floor_protection_uncertified_present'),
            radiant_heat_floor_protection_uncertified_compliance=data.get('radiant_heat_floor_protection_uncertified_compliance'),
            radiant_heat_floor_protection_uncertified_photos=data.get('radiant_heat_floor_protection_uncertified_photos', []),
            radiant_heat_floor_protection_certified_required=data.get('radiant_heat_floor_protection_certified_required'),
            radiant_heat_floor_protection_certified_present=data.get('radiant_heat_floor_protection_certified_present'),
            radiant_heat_floor_protection_certified_compliance=data.get('radiant_heat_floor_protection_certified_compliance'),
            radiant_heat_floor_protection_certified_photos=data.get('radiant_heat_floor_protection_certified_photos', []),
            hazardous_location_required=data.get('hazardous_location_required'),
            hazardous_location_present=data.get('hazardous_location_present'),
            hazardous_location_compliance=data.get('hazardous_location_compliance'),
            hazardous_location_photos=data.get('hazardous_location_photos', [])
        )

        db.session.add(ember_pad_floor_protection)
        db.session.commit()
        return jsonify({'data': ember_pad_floor_protection.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/ember-pad-floor-protection/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_ember_pad_floor_protection(inspection_id):
    """Get wood stove manufactured ember pad floor protection for an inspection"""
    try:
        ember_pad_floor_protection = WoodStoveManufacturedEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not ember_pad_floor_protection:
            return jsonify({'error': 'Wood stove manufactured ember pad floor protection not found'}), 404
        return jsonify({'data': ember_pad_floor_protection.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/ember-pad-floor-protection/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_ember_pad_floor_protection(inspection_id):
    """Update wood stove manufactured ember pad floor protection for an inspection"""
    data = request.get_json()
    try:
        ember_pad_floor_protection = WoodStoveManufacturedEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not ember_pad_floor_protection:
            return jsonify({'error': 'Wood stove manufactured ember pad floor protection not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(ember_pad_floor_protection, key):
                setattr(ember_pad_floor_protection, key, value)

        db.session.commit()
        return jsonify({'data': ember_pad_floor_protection.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/ember-pad-floor-protection/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_ember_pad_floor_protection(inspection_id):
    """Delete wood stove manufactured ember pad floor protection for an inspection"""
    try:
        ember_pad_floor_protection = WoodStoveManufacturedEmberPadFloorProtection.query.filter_by(inspection_id=inspection_id).first()
        if not ember_pad_floor_protection:
            return jsonify({'error': 'Wood stove manufactured ember pad floor protection not found'}), 404

        db.session.delete(ember_pad_floor_protection)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured ember pad floor protection deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Fire Codes Compliance routes
@main.route('/api/wood-stove-manufactured/fire-codes-compliance', methods=['POST'])
def create_wood_stove_manufactured_fire_codes_compliance():
    """Create wood stove manufactured fire codes compliance for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedFireCodesCompliance.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Wood stove manufactured fire codes compliance already exists for this inspection'}), 400

        fire_codes_compliance = WoodStoveManufacturedFireCodesCompliance(
            inspection_id=inspection_id,
            rule1_condition=data.get('rule1_condition'),
            rule1_comments=data.get('rule1_comments'),
            rule1_compliance=data.get('rule1_compliance'),
            rule1_photos=data.get('rule1_photos', []),
            rule2_condition=data.get('rule2_condition'),
            rule2_comments=data.get('rule2_comments'),
            rule2_compliance=data.get('rule2_compliance'),
            rule2_photos=data.get('rule2_photos', []),
            rule3a_condition=data.get('rule3a_condition'),
            rule3a_comments=data.get('rule3a_comments'),
            rule3a_compliance=data.get('rule3a_compliance'),
            rule3a_photos=data.get('rule3a_photos', []),
            rule3b_condition=data.get('rule3b_condition'),
            rule3b_comments=data.get('rule3b_comments'),
            rule3b_compliance=data.get('rule3b_compliance'),
            rule3b_photos=data.get('rule3b_photos', [])
        )

        db.session.add(fire_codes_compliance)
        db.session.commit()
        return jsonify({'data': fire_codes_compliance.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/fire-codes-compliance/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_fire_codes_compliance(inspection_id):
    """Get wood stove manufactured fire codes compliance for an inspection"""
    try:
        fire_codes_compliance = WoodStoveManufacturedFireCodesCompliance.query.filter_by(inspection_id=inspection_id).first()
        if not fire_codes_compliance:
            return jsonify({'error': 'Wood stove manufactured fire codes compliance not found'}), 404
        return jsonify({'data': fire_codes_compliance.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/fire-codes-compliance/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_fire_codes_compliance(inspection_id):
    """Update wood stove manufactured fire codes compliance for an inspection"""
    data = request.get_json()
    try:
        fire_codes_compliance = WoodStoveManufacturedFireCodesCompliance.query.filter_by(inspection_id=inspection_id).first()
        if not fire_codes_compliance:
            return jsonify({'error': 'Wood stove manufactured fire codes compliance not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(fire_codes_compliance, key):
                setattr(fire_codes_compliance, key, value)

        db.session.commit()
        return jsonify({'data': fire_codes_compliance.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/fire-codes-compliance/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_fire_codes_compliance(inspection_id):
    """Delete wood stove manufactured fire codes compliance for an inspection"""
    try:
        fire_codes_compliance = WoodStoveManufacturedFireCodesCompliance.query.filter_by(inspection_id=inspection_id).first()
        if not fire_codes_compliance:
            return jsonify({'error': 'Wood stove manufactured fire codes compliance not found'}), 404

        db.session.delete(fire_codes_compliance)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured fire codes compliance deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Flue Pipe Chimney Connection routes
@main.route('/api/wood-stove-manufactured/flue-pipe-chimney-connection', methods=['POST'])
def create_wood_stove_manufactured_flue_pipe_chimney_connection():
    """Create wood stove manufactured flue pipe chimney connection for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedFluePipeChimneyConnection.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Wood stove manufactured flue pipe chimney connection already exists for this inspection'}), 400

        flue_pipe_chimney_connection = WoodStoveManufacturedFluePipeChimneyConnection(
            inspection_id=inspection_id,
            minimum_horizontal_extension_required=data.get('minimum_horizontal_extension_required'),
            minimum_horizontal_extension_present=data.get('minimum_horizontal_extension_present'),
            minimum_horizontal_extension_compliance=data.get('minimum_horizontal_extension_compliance'),
            minimum_horizontal_extension_photos=data.get('minimum_horizontal_extension_photos', []),
            maximum_horizontal_extension_required=data.get('maximum_horizontal_extension_required'),
            maximum_horizontal_extension_present=data.get('maximum_horizontal_extension_present'),
            maximum_horizontal_extension_compliance=data.get('maximum_horizontal_extension_compliance'),
            maximum_horizontal_extension_photos=data.get('maximum_horizontal_extension_photos', []),
            wall_radiation_shield_required=data.get('wall_radiation_shield_required'),
            wall_radiation_shield_present=data.get('wall_radiation_shield_present'),
            wall_radiation_shield_compliance=data.get('wall_radiation_shield_compliance'),
            wall_radiation_shield_photos=data.get('wall_radiation_shield_photos', []),
            base_tee_and_cap_required=data.get('base_tee_and_cap_required'),
            base_tee_and_cap_present=data.get('base_tee_and_cap_present'),
            base_tee_and_cap_compliance=data.get('base_tee_and_cap_compliance'),
            base_tee_and_cap_photos=data.get('base_tee_and_cap_photos', []),
            base_tee_support_required=data.get('base_tee_support_required'),
            base_tee_support_present=data.get('base_tee_support_present'),
            base_tee_support_compliance=data.get('base_tee_support_compliance'),
            base_tee_support_photos=data.get('base_tee_support_photos', []),
            wall_support_band_required=data.get('wall_support_band_required'),
            wall_support_band_present=data.get('wall_support_band_present'),
            wall_support_band_compliance=data.get('wall_support_band_compliance'),
            wall_support_band_photos=data.get('wall_support_band_photos', []),
            distance_between_supports_required=data.get('distance_between_supports_required'),
            distance_between_supports_present=data.get('distance_between_supports_present'),
            distance_between_supports_compliance=data.get('distance_between_supports_compliance'),
            distance_between_supports_photos=data.get('distance_between_supports_photos', []),
            chimney_offsets_required=data.get('chimney_offsets_required'),
            chimney_offsets_present=data.get('chimney_offsets_present'),
            chimney_offsets_compliance=data.get('chimney_offsets_compliance'),
            chimney_offsets_photos=data.get('chimney_offsets_photos', []),
            offset_support_required=data.get('offset_support_required'),
            offset_support_present=data.get('offset_support_present'),
            offset_support_compliance=data.get('offset_support_compliance'),
            offset_support_photos=data.get('offset_support_photos', [])
        )

        db.session.add(flue_pipe_chimney_connection)
        db.session.commit()
        return jsonify({'data': flue_pipe_chimney_connection.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-chimney-connection/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_flue_pipe_chimney_connection(inspection_id):
    """Get wood stove manufactured flue pipe chimney connection for an inspection"""
    try:
        flue_pipe_chimney_connection = WoodStoveManufacturedFluePipeChimneyConnection.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_chimney_connection:
            return jsonify({'error': 'Wood stove manufactured flue pipe chimney connection not found'}), 404
        return jsonify({'data': flue_pipe_chimney_connection.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-chimney-connection/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_flue_pipe_chimney_connection(inspection_id):
    """Update wood stove manufactured flue pipe chimney connection for an inspection"""
    data = request.get_json()
    try:
        flue_pipe_chimney_connection = WoodStoveManufacturedFluePipeChimneyConnection.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_chimney_connection:
            return jsonify({'error': 'Wood stove manufactured flue pipe chimney connection not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(flue_pipe_chimney_connection, key):
                setattr(flue_pipe_chimney_connection, key, value)

        db.session.commit()
        return jsonify({'data': flue_pipe_chimney_connection.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-chimney-connection/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_flue_pipe_chimney_connection(inspection_id):
    """Delete wood stove manufactured flue pipe chimney connection for an inspection"""
    try:
        flue_pipe_chimney_connection = WoodStoveManufacturedFluePipeChimneyConnection.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_chimney_connection:
            return jsonify({'error': 'Wood stove manufactured flue pipe chimney connection not found'}), 404

        db.session.delete(flue_pipe_chimney_connection)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured flue pipe chimney connection deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Flue Pipe Components routes
@main.route('/api/wood-stove-manufactured/flue-pipe-components', methods=['POST'])
def create_wood_stove_manufactured_flue_pipe_components():
    """Create wood stove manufactured flue pipe components for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedFluePipeComponents.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Wood stove manufactured flue pipe components already exists for this inspection'}), 400

        flue_pipe_components = WoodStoveManufacturedFluePipeComponents(
            inspection_id=inspection_id,
            material_required=data.get('material_required'),
            material_present=data.get('material_present'),
            material_compliance=data.get('material_compliance'),
            material_photos=data.get('material_photos', []),
            minimum_thickness_required_016=data.get('minimum_thickness_required_016'),
            minimum_thickness_required_024=data.get('minimum_thickness_required_024'),
            minimum_thickness_present=data.get('minimum_thickness_present'),
            minimum_thickness_compliance=data.get('minimum_thickness_compliance'),
            minimum_thickness_photos=data.get('minimum_thickness_photos', []),
            flue_pipe_condition_required=data.get('flue_pipe_condition_required'),
            flue_pipe_condition_present=data.get('flue_pipe_condition_present'),
            flue_pipe_condition_compliance=data.get('flue_pipe_condition_compliance'),
            flue_pipe_condition_photos=data.get('flue_pipe_condition_photos', []),
            flue_shielding_present_required=data.get('flue_shielding_present_required'),
            flue_shielding_present_present=data.get('flue_shielding_present_present'),
            flue_shielding_present_compliance=data.get('flue_shielding_present_compliance'),
            flue_shielding_present_photos=data.get('flue_shielding_present_photos', []),
            support_horizontal_present_required=data.get('support_horizontal_present_required'),
            support_horizontal_present_present=data.get('support_horizontal_present_present'),
            support_horizontal_present_compliance=data.get('support_horizontal_present_compliance'),
            support_horizontal_present_photos=data.get('support_horizontal_present_photos', []),
            barometric_damper_present_code_reference=data.get('barometric_damper_present_code_reference'),
            barometric_damper_present_required=data.get('barometric_damper_present_required'),
            barometric_damper_present_present=data.get('barometric_damper_present_present'),
            barometric_damper_present_compliance=data.get('barometric_damper_present_compliance'),
            barometric_damper_present_photos=data.get('barometric_damper_present_photos', []),
            flue_mounted_heat_reducers_present_code_reference=data.get('flue_mounted_heat_reducers_present_code_reference'),
            flue_mounted_heat_reducers_present_required=data.get('flue_mounted_heat_reducers_present_required'),
            flue_mounted_heat_reducers_present_present=data.get('flue_mounted_heat_reducers_present_present'),
            flue_mounted_heat_reducers_present_compliance=data.get('flue_mounted_heat_reducers_present_compliance'),
            flue_mounted_heat_reducers_present_photos=data.get('flue_mounted_heat_reducers_present_photos', []),
            flue_pipe_pass_through_floors_ceilings_required=data.get('flue_pipe_pass_through_floors_ceilings_required'),
            flue_pipe_pass_through_floors_ceilings_present=data.get('flue_pipe_pass_through_floors_ceilings_present'),
            flue_pipe_pass_through_floors_ceilings_compliance=data.get('flue_pipe_pass_through_floors_ceilings_compliance'),
            flue_pipe_pass_through_floors_ceilings_photos=data.get('flue_pipe_pass_through_floors_ceilings_photos', []),
            connection_to_factory_built_chimney_required=data.get('connection_to_factory_built_chimney_required'),
            connection_to_factory_built_chimney_present=data.get('connection_to_factory_built_chimney_present'),
            connection_to_factory_built_chimney_compliance=data.get('connection_to_factory_built_chimney_compliance'),
            connection_to_factory_built_chimney_photos=data.get('connection_to_factory_built_chimney_photos', [])
        )

        db.session.add(flue_pipe_components)
        db.session.commit()
        return jsonify({'data': flue_pipe_components.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-components/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_flue_pipe_components(inspection_id):
    """Get wood stove manufactured flue pipe components for an inspection"""
    try:
        flue_pipe_components = WoodStoveManufacturedFluePipeComponents.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_components:
            return jsonify({'error': 'Wood stove manufactured flue pipe components not found'}), 404
        return jsonify({'data': flue_pipe_components.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-components/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_flue_pipe_components(inspection_id):
    """Update wood stove manufactured flue pipe components for an inspection"""
    data = request.get_json()
    try:
        flue_pipe_components = WoodStoveManufacturedFluePipeComponents.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_components:
            return jsonify({'error': 'Wood stove manufactured flue pipe components not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(flue_pipe_components, key):
                setattr(flue_pipe_components, key, value)

        db.session.commit()
        return jsonify({'data': flue_pipe_components.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-components/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_flue_pipe_components(inspection_id):
    """Delete wood stove manufactured flue pipe components for an inspection"""
    try:
        flue_pipe_components = WoodStoveManufacturedFluePipeComponents.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_components:
            return jsonify({'error': 'Wood stove manufactured flue pipe components not found'}), 404

        db.session.delete(flue_pipe_components)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured flue pipe components deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Flue Pipe Info Clearances routes
@main.route('/api/wood-stove-manufactured/flue-pipe-info-clearances', methods=['POST'])
def create_wood_stove_manufactured_flue_pipe_info_clearances():
    """Create wood stove manufactured flue pipe info clearances for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedFluePipeInfoClearances.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Wood stove manufactured flue pipe info clearances already exists for this inspection'}), 400

        flue_pipe_info_clearances = WoodStoveManufacturedFluePipeInfoClearances(
            inspection_id=inspection_id,
            flue_pipe_connector_type=data.get('flue_pipe_connector_type'),
            flue_pipe_connector_diameter=data.get('flue_pipe_connector_diameter'),
            flue_pipe_connector_manufacturer=data.get('flue_pipe_connector_manufacturer'),
            flue_pipe_connector_model=data.get('flue_pipe_connector_model'),
            flue_pipe_connector_listing_agency=data.get('flue_pipe_connector_listing_agency'),
            flue_pipe_connector_is_listing_agency_manually_available=data.get('flue_pipe_connector_is_listing_agency_manually_available'),
            wall_clearances_right_side_required_uncertified=data.get('wall_clearances_right_side_required_uncertified'),
            wall_clearances_right_side_required_certified=data.get('wall_clearances_right_side_required_certified'),
            wall_clearances_right_side_present=data.get('wall_clearances_right_side_present'),
            wall_clearances_right_side_compliance=data.get('wall_clearances_right_side_compliance'),
            wall_clearances_right_side_photos=data.get('wall_clearances_right_side_photos', []),
            wall_clearances_left_side_required_uncertified=data.get('wall_clearances_left_side_required_uncertified'),
            wall_clearances_left_side_required_certified=data.get('wall_clearances_left_side_required_certified'),
            wall_clearances_left_side_present=data.get('wall_clearances_left_side_present'),
            wall_clearances_left_side_compliance=data.get('wall_clearances_left_side_compliance'),
            wall_clearances_left_side_photos=data.get('wall_clearances_left_side_photos', []),
            wall_clearances_rear_wall_required_uncertified=data.get('wall_clearances_rear_wall_required_uncertified'),
            wall_clearances_rear_wall_required_certified=data.get('wall_clearances_rear_wall_required_certified'),
            wall_clearances_rear_wall_present=data.get('wall_clearances_rear_wall_present'),
            wall_clearances_rear_wall_compliance=data.get('wall_clearances_rear_wall_compliance'),
            wall_clearances_rear_wall_photos=data.get('wall_clearances_rear_wall_photos', []),
            clearances_horizontal_pipe_required_uncertified=data.get('clearances_horizontal_pipe_required_uncertified'),
            clearances_horizontal_pipe_required_certified=data.get('clearances_horizontal_pipe_required_certified'),
            clearances_horizontal_pipe_present=data.get('clearances_horizontal_pipe_present'),
            clearances_horizontal_pipe_compliance=data.get('clearances_horizontal_pipe_compliance'),
            clearances_horizontal_pipe_photos=data.get('clearances_horizontal_pipe_photos', []),
            clearances_ceiling_required_uncertified=data.get('clearances_ceiling_required_uncertified'),
            clearances_ceiling_required_certified=data.get('clearances_ceiling_required_certified'),
            clearances_ceiling_present=data.get('clearances_ceiling_present'),
            clearances_ceiling_compliance=data.get('clearances_ceiling_compliance'),
            clearances_ceiling_photos=data.get('clearances_ceiling_photos', [])
        )

        db.session.add(flue_pipe_info_clearances)
        db.session.commit()
        return jsonify({'data': flue_pipe_info_clearances.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-info-clearances/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_flue_pipe_info_clearances(inspection_id):
    """Get wood stove manufactured flue pipe info clearances for an inspection"""
    try:
        flue_pipe_info_clearances = WoodStoveManufacturedFluePipeInfoClearances.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_info_clearances:
            return jsonify({'error': 'Wood stove manufactured flue pipe info clearances not found'}), 404
        return jsonify({'data': flue_pipe_info_clearances.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-info-clearances/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_flue_pipe_info_clearances(inspection_id):
    """Update wood stove manufactured flue pipe info clearances for an inspection"""
    data = request.get_json()
    try:
        flue_pipe_info_clearances = WoodStoveManufacturedFluePipeInfoClearances.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_info_clearances:
            return jsonify({'error': 'Wood stove manufactured flue pipe info clearances not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(flue_pipe_info_clearances, key):
                setattr(flue_pipe_info_clearances, key, value)

        db.session.commit()
        return jsonify({'data': flue_pipe_info_clearances.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-info-clearances/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_flue_pipe_info_clearances(inspection_id):
    """Delete wood stove manufactured flue pipe info clearances for an inspection"""
    try:
        flue_pipe_info_clearances = WoodStoveManufacturedFluePipeInfoClearances.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_info_clearances:
            return jsonify({'error': 'Wood stove manufactured flue pipe info clearances not found'}), 404

        db.session.delete(flue_pipe_info_clearances)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured flue pipe info clearances deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Wood Stove Manufactured Flue Pipe Orientation Joints routes
@main.route('/api/wood-stove-manufactured/flue-pipe-orientation-joints', methods=['POST'])
def create_wood_stove_manufactured_flue_pipe_orientation_joints():
    """Create wood stove manufactured flue pipe orientation joints for an inspection"""
    data = request.get_json()
    inspection_id = data.get('inspection_id')

    if not inspection_id:
        return jsonify({'error': 'inspection_id is required'}), 400

    try:
        # Check if already exists
        existing = WoodStoveManufacturedFluePipeOrientationJoints.query.filter_by(inspection_id=inspection_id).first()
        if existing:
            return jsonify({'error': 'Wood stove manufactured flue pipe orientation joints already exists for this inspection'}), 400

        flue_pipe_orientation_joints = WoodStoveManufacturedFluePipeOrientationJoints(
            inspection_id=inspection_id,
            total_length_required=data.get('total_length_required'),
            total_length_present=data.get('total_length_present'),
            total_length_compliance=data.get('total_length_compliance'),
            total_length_photos=data.get('total_length_photos', []),
            elbows_maximum_required=data.get('elbows_maximum_required'),
            elbows_maximum_present=data.get('elbows_maximum_present'),
            elbows_maximum_compliance=data.get('elbows_maximum_compliance'),
            elbows_maximum_photos=data.get('elbows_maximum_photos', []),
            fastening_required=data.get('fastening_required'),
            fastening_present=data.get('fastening_present'),
            fastening_compliance=data.get('fastening_compliance'),
            fastening_photos=data.get('fastening_photos', []),
            allowance_for_expansion_required=data.get('allowance_for_expansion_required'),
            allowance_for_expansion_present=data.get('allowance_for_expansion_present'),
            allowance_for_expansion_compliance=data.get('allowance_for_expansion_compliance'),
            allowance_for_expansion_photos=data.get('allowance_for_expansion_photos', []),
            flue_pipe_orientation_required=data.get('flue_pipe_orientation_required'),
            flue_pipe_orientation_present=data.get('flue_pipe_orientation_present'),
            flue_pipe_orientation_compliance=data.get('flue_pipe_orientation_compliance'),
            flue_pipe_orientation_photos=data.get('flue_pipe_orientation_photos', []),
            joint_overlap_required=data.get('joint_overlap_required'),
            joint_overlap_present=data.get('joint_overlap_present'),
            joint_overlap_compliance=data.get('joint_overlap_compliance'),
            joint_overlap_photos=data.get('joint_overlap_photos', []),
            flue_pipe_slope_required=data.get('flue_pipe_slope_required'),
            flue_pipe_slope_present=data.get('flue_pipe_slope_present'),
            flue_pipe_slope_compliance=data.get('flue_pipe_slope_compliance'),
            flue_pipe_slope_photos=data.get('flue_pipe_slope_photos', [])
        )

        db.session.add(flue_pipe_orientation_joints)
        db.session.commit()
        return jsonify({'data': flue_pipe_orientation_joints.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-orientation-joints/<int:inspection_id>', methods=['GET'])
def get_wood_stove_manufactured_flue_pipe_orientation_joints(inspection_id):
    """Get wood stove manufactured flue pipe orientation joints for an inspection"""
    try:
        flue_pipe_orientation_joints = WoodStoveManufacturedFluePipeOrientationJoints.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_orientation_joints:
            return jsonify({'error': 'Wood stove manufactured flue pipe orientation joints not found'}), 404
        return jsonify({'data': flue_pipe_orientation_joints.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-orientation-joints/<int:inspection_id>', methods=['PUT'])
def update_wood_stove_manufactured_flue_pipe_orientation_joints(inspection_id):
    """Update wood stove manufactured flue pipe orientation joints for an inspection"""
    data = request.get_json()
    try:
        flue_pipe_orientation_joints = WoodStoveManufacturedFluePipeOrientationJoints.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_orientation_joints:
            return jsonify({'error': 'Wood stove manufactured flue pipe orientation joints not found'}), 404

        # Update fields from data
        for key, value in data.items():
            if hasattr(flue_pipe_orientation_joints, key):
                setattr(flue_pipe_orientation_joints, key, value)

        db.session.commit()
        return jsonify({'data': flue_pipe_orientation_joints.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/wood-stove-manufactured/flue-pipe-orientation-joints/<int:inspection_id>', methods=['DELETE'])
def delete_wood_stove_manufactured_flue_pipe_orientation_joints(inspection_id):
    """Delete wood stove manufactured flue pipe orientation joints for an inspection"""
    try:
        flue_pipe_orientation_joints = WoodStoveManufacturedFluePipeOrientationJoints.query.filter_by(inspection_id=inspection_id).first()
        if not flue_pipe_orientation_joints:
            return jsonify({'error': 'Wood stove manufactured flue pipe orientation joints not found'}), 404

        db.session.delete(flue_pipe_orientation_joints)
        db.session.commit()
        return jsonify({'message': 'Wood stove manufactured flue pipe orientation joints deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
