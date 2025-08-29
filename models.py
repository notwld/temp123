from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clerk_user_id = db.Column(db.String(100), unique=True, nullable=True)  # Clerk user ID
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=True)  # Optional for OAuth users
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inspector = db.relationship('Inspector', backref='user', uselist=False, cascade='all, delete-orphan')
    company = db.relationship('Company', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'clerk_user_id': self.clerk_user_id,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Inspector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    wett_number = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Inspector {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'wett_number': self.wett_number,
            'province': self.province,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(200), nullable=True)
    company_email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    logo = db.Column(db.Text, nullable=True)  # Store base64 or URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Company {self.company_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'company_name': self.company_name,
            'address': self.address,
            'website': self.website,
            'company_email': self.company_email,
            'phone': self.phone,
            'logo': self.logo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Inspection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    form_type = db.Column(db.String(50), nullable=True)  # factory-built, fireplace-insert, masonry, pellet-insert, wood-stove-manufactured, wood-stove-masonry
    client_name = db.Column(db.String(100), nullable=True)
    client_address = db.Column(db.Text, nullable=True)
    inspection_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='draft')  # draft, completed, submitted
    form_data = db.Column(db.JSON, nullable=True)  # Store form data as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user_ref = db.relationship('User', backref='inspections')
    
    def __repr__(self):
        return f'<Inspection {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'form_type': self.form_type,
            'client_name': self.client_name,
            'client_address': self.client_address,
            'inspection_date': self.inspection_date.isoformat() if self.inspection_date else None,
            'status': self.status,
            'form_data': self.form_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ChimneySpecification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # Inspection details
    inspection_discussed = db.Column(db.String(10), nullable=True)  # yes/no
    building_permits = db.Column(db.String(10), nullable=True)  # yes/no
    time_of_day = db.Column(db.String(20), nullable=True)
    weather_conditions = db.Column(db.Text, nullable=True)
    roofing_type = db.Column(db.String(100), nullable=True)
    roof_accessed = db.Column(db.String(10), nullable=True)  # yes/no
    attic_accessed = db.Column(db.String(10), nullable=True)  # yes/no
    
    # Chimney details
    chimney_make_model = db.Column(db.String(200), nullable=True)
    chimney_listed = db.Column(db.String(20), nullable=True)  # yes/no/unknown
    flue_size = db.Column(db.String(50), nullable=True)
    installation_manual = db.Column(db.String(20), nullable=True)  # yes/no/original/web
    certification_standard = db.Column(db.JSON, nullable=True)  # Array of standards
    listing_agency = db.Column(db.JSON, nullable=True)  # Array of agencies
    comments = db.Column(db.Text, nullable=True)
    suitable = db.Column(db.String(10), nullable=True)  # yes/no
    installation = db.Column(db.String(20), nullable=True)  # inside/outside
    chimney_installed_by = db.Column(db.String(200), nullable=True)
    inspection_date = db.Column(db.String(50), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection_ref = db.relationship('Inspection', backref='chimney_specifications')
    
    def __repr__(self):
        return f'<ChimneySpecification {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'inspection_discussed': self.inspection_discussed,
            'building_permits': self.building_permits,
            'time_of_day': self.time_of_day,
            'weather_conditions': self.weather_conditions,
            'roofing_type': self.roofing_type,
            'roof_accessed': self.roof_accessed,
            'attic_accessed': self.attic_accessed,
            'chimney_make_model': self.chimney_make_model,
            'chimney_listed': self.chimney_listed,
            'flue_size': self.flue_size,
            'installation_manual': self.installation_manual,
            'certification_standard': self.certification_standard,
            'listing_agency': self.listing_agency,
            'comments': self.comments,
            'suitable': self.suitable,
            'installation': self.installation,
            'chimney_installed_by': self.chimney_installed_by,
            'inspection_date': self.inspection_date,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class FireplaceSpecification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # Fireplace details
    fireplace_model_serial = db.Column(db.String(200), nullable=True)
    installation_manual = db.Column(db.String(20), nullable=True)  # yes/no/original/web
    listing_agency = db.Column(db.JSON, nullable=True)  # Array of agencies
    certification_standard = db.Column(db.JSON, nullable=True)  # Array of standards
    fan_blower_attached = db.Column(db.String(10), nullable=True)  # yes/no
    comments = db.Column(db.Text, nullable=True)
    suitable = db.Column(db.String(10), nullable=True)  # yes/no
    mobile_home_approved = db.Column(db.String(10), nullable=True)  # yes/no/na
    installed_in = db.Column(db.String(50), nullable=True)  # residence/modular/mobile/alcove/other
    installed_in_other = db.Column(db.String(200), nullable=True)
    appliance_location = db.Column(db.String(50), nullable=True)  # basement/main/other
    appliance_location_other = db.Column(db.String(200), nullable=True)
    appliance_installed_by = db.Column(db.String(200), nullable=True)
    inspection_date = db.Column(db.String(50), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection_ref = db.relationship('Inspection', backref='fireplace_specifications')
    
    def __repr__(self):
        return f'<FireplaceSpecification {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'fireplace_model_serial': self.fireplace_model_serial,
            'installation_manual': self.installation_manual,
            'listing_agency': self.listing_agency,
            'certification_standard': self.certification_standard,
            'fan_blower_attached': self.fan_blower_attached,
            'comments': self.comments,
            'suitable': self.suitable,
            'mobile_home_approved': self.mobile_home_approved,
            'installed_in': self.installed_in,
            'installed_in_other': self.installed_in_other,
            'appliance_location': self.appliance_location,
            'appliance_location_other': self.appliance_location_other,
            'appliance_installed_by': self.appliance_installed_by,
            'inspection_date': self.inspection_date,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CombustibleMaterials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # Material Clearances section
    material_clearances_required = db.Column(db.String(100), nullable=True)
    material_clearances_present = db.Column(db.String(100), nullable=True)
    material_clearances_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    material_clearances_photos = db.Column(db.JSON, nullable=True)  # Array of photo URLs
    
    # Right Side Logs section
    right_side_logs_required = db.Column(db.String(100), nullable=True)
    right_side_logs_present = db.Column(db.String(100), nullable=True)
    right_side_logs_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    right_side_logs_photos = db.Column(db.JSON, nullable=True)  # Array of photo URLs
    
    # Left Side Logs section
    left_side_logs_required = db.Column(db.String(100), nullable=True)
    left_side_logs_present = db.Column(db.String(100), nullable=True)
    left_side_logs_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    left_side_logs_photos = db.Column(db.JSON, nullable=True)  # Array of photo URLs
    
    # Combustible Facing section
    combustible_facing_required = db.Column(db.String(100), nullable=True)
    combustible_facing_present = db.Column(db.String(100), nullable=True)
    combustible_facing_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    combustible_facing_photos = db.Column(db.JSON, nullable=True)  # Array of photo URLs
    
    # Combustible Side Wall section
    combustible_side_wall_required = db.Column(db.String(100), nullable=True)
    combustible_side_wall_present = db.Column(db.String(100), nullable=True)
    combustible_side_wall_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    combustible_side_wall_photos = db.Column(db.JSON, nullable=True)  # Array of photo URLs
    
    # Fireplace Beavers section
    fireplace_beaver_required = db.Column(db.String(100), nullable=True)
    fireplace_beaver_present = db.Column(db.String(100), nullable=True)
    fireplace_beaver_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    fireplace_beaver_photos = db.Column(db.JSON, nullable=True)  # Array of photo URLs
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection_ref = db.relationship('Inspection', backref='combustible_materials')
    
    def __repr__(self):
        return f'<CombustibleMaterials {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            # Material Clearances
            'material_clearances_required': self.material_clearances_required,
            'material_clearances_present': self.material_clearances_present,
            'material_clearances_compliance': self.material_clearances_compliance,
            'material_clearances_photos': self.material_clearances_photos,
            # Right Side Logs
            'right_side_logs_required': self.right_side_logs_required,
            'right_side_logs_present': self.right_side_logs_present,
            'right_side_logs_compliance': self.right_side_logs_compliance,
            'right_side_logs_photos': self.right_side_logs_photos,
            # Left Side Logs
            'left_side_logs_required': self.left_side_logs_required,
            'left_side_logs_present': self.left_side_logs_present,
            'left_side_logs_compliance': self.left_side_logs_compliance,
            'left_side_logs_photos': self.left_side_logs_photos,
            # Combustible Facing
            'combustible_facing_required': self.combustible_facing_required,
            'combustible_facing_present': self.combustible_facing_present,
            'combustible_facing_compliance': self.combustible_facing_compliance,
            'combustible_facing_photos': self.combustible_facing_photos,
            # Combustible Side Wall
            'combustible_side_wall_required': self.combustible_side_wall_required,
            'combustible_side_wall_present': self.combustible_side_wall_present,
            'combustible_side_wall_compliance': self.combustible_side_wall_compliance,
            'combustible_side_wall_photos': self.combustible_side_wall_photos,
            # Fireplace Beavers
            'fireplace_beaver_required': self.fireplace_beaver_required,
            'fireplace_beaver_present': self.fireplace_beaver_present,
            'fireplace_beaver_compliance': self.fireplace_beaver_compliance,
            'fireplace_beaver_photos': self.fireplace_beaver_photos,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class HearthFloorProtection(db.Model):
    __tablename__ = 'hearth_floor_protection'
    
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # Ember Strip (Section 7)
    ember_strip_required = db.Column(db.String(255))
    ember_strip_present = db.Column(db.String(255))
    ember_strip_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    ember_strip_photos = db.Column(db.JSON)
    
    # Hearth Extension Front (Section 8)
    hearth_extension_front_required = db.Column(db.String(255))
    hearth_extension_front_present = db.Column(db.String(255))
    hearth_extension_front_compliance = db.Column(db.String(10))
    hearth_extension_front_photos = db.Column(db.JSON)
    
    # Hearth Extension Right Side (Section 9)
    hearth_extension_right_required = db.Column(db.String(255))
    hearth_extension_right_present = db.Column(db.String(255))
    hearth_extension_right_compliance = db.Column(db.String(10))
    hearth_extension_right_photos = db.Column(db.JSON)
    
    # Hearth Extension Left Side (Section 10)
    hearth_extension_left_required = db.Column(db.String(255))
    hearth_extension_left_present = db.Column(db.String(255))
    hearth_extension_left_compliance = db.Column(db.String(10))
    hearth_extension_left_photos = db.Column(db.JSON)
    
    # Hearth Material (Section 11)
    hearth_material_required = db.Column(db.String(255))
    hearth_material_present = db.Column(db.String(255))
    hearth_material_compliance = db.Column(db.String(10))
    hearth_material_photos = db.Column(db.JSON)
    
    # Floor Radiation Protection (Section 12)
    floor_radiation_protection_required = db.Column(db.String(255))
    floor_radiation_protection_present = db.Column(db.String(255))
    floor_radiation_protection_compliance = db.Column(db.String(10))
    floor_radiation_protection_photos = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('hearth_floor_protection', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'emberStrip': {
                'requiredValue': self.ember_strip_required,
                'presentValue': self.ember_strip_present,
                'codeCompliance': self.ember_strip_compliance,
                'photos': self.ember_strip_photos or []
            },
            'hearthExtensionFront': {
                'requiredValue': self.hearth_extension_front_required,
                'presentValue': self.hearth_extension_front_present,
                'codeCompliance': self.hearth_extension_front_compliance,
                'photos': self.hearth_extension_front_photos or []
            },
            'hearthExtensionRightSide': {
                'requiredValue': self.hearth_extension_right_required,
                'presentValue': self.hearth_extension_right_present,
                'codeCompliance': self.hearth_extension_right_compliance,
                'photos': self.hearth_extension_right_photos or []
            },
            'hearthExtensionLeftSide': {
                'requiredValue': self.hearth_extension_left_required,
                'presentValue': self.hearth_extension_left_present,
                'codeCompliance': self.hearth_extension_left_compliance,
                'photos': self.hearth_extension_left_photos or []
            },
            'hearthMaterial': {
                'requiredValue': self.hearth_material_required,
                'presentValue': self.hearth_material_present,
                'codeCompliance': self.hearth_material_compliance,
                'photos': self.hearth_material_photos or []
            },
            'floorRadiationProtection': {
                'requiredValue': self.floor_radiation_protection_required,
                'presentValue': self.floor_radiation_protection_present,
                'codeCompliance': self.floor_radiation_protection_compliance,
                'photos': self.floor_radiation_protection_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class EnclosureVentilation(db.Model):
    __tablename__ = 'enclosure_ventilation'
    
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # Ceiling Height (Section 13)
    ceiling_height_required = db.Column(db.String(255))
    ceiling_height_present = db.Column(db.String(255))
    ceiling_height_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    ceiling_height_photos = db.Column(db.JSON)
    
    # Fireplace Enclosured (Section 14)
    fireplace_enclosured_required = db.Column(db.String(255))
    fireplace_enclosured_present = db.Column(db.String(255))
    fireplace_enclosured_compliance = db.Column(db.String(10))
    fireplace_enclosured_photos = db.Column(db.JSON)
    
    # Clearance Within Enclosure (Section 15)
    clearance_within_enclosure_required = db.Column(db.String(255))
    clearance_within_enclosure_present = db.Column(db.String(255))
    clearance_within_enclosure_compliance = db.Column(db.String(10))
    clearance_within_enclosure_photos = db.Column(db.JSON)
    
    # Gravity Vent Clearance (Section 16)
    gravity_vent_clearance_required = db.Column(db.String(255))
    gravity_vent_clearance_present = db.Column(db.String(255))
    gravity_vent_clearance_compliance = db.Column(db.String(10))
    gravity_vent_clearance_photos = db.Column(db.JSON)
    
    # Gravity Vent Grille Clearance (Section 17)
    gravity_vent_grille_clearance_required = db.Column(db.String(255))
    gravity_vent_grille_clearance_present = db.Column(db.String(255))
    gravity_vent_grille_clearance_compliance = db.Column(db.String(10))
    gravity_vent_grille_clearance_photos = db.Column(db.JSON)
    
    # Hearth Materials (Section 18)
    hearth_materials_required = db.Column(db.String(255))
    hearth_materials_present = db.Column(db.String(255))
    hearth_materials_compliance = db.Column(db.String(10))
    hearth_materials_photos = db.Column(db.JSON)
    
    # Central Heating Kit (Section 19)
    central_heating_kit_required = db.Column(db.String(255))
    central_heating_kit_present = db.Column(db.String(255))
    central_heating_kit_compliance = db.Column(db.String(10))
    central_heating_kit_photos = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('enclosure_ventilation', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'ceilingHeight': {
                'requiredValue': self.ceiling_height_required,
                'presentValue': self.ceiling_height_present,
                'codeCompliance': self.ceiling_height_compliance,
                'photos': self.ceiling_height_photos or []
            },
            'fireplaceEnclosured': {
                'requiredValue': self.fireplace_enclosured_required,
                'presentValue': self.fireplace_enclosured_present,
                'codeCompliance': self.fireplace_enclosured_compliance,
                'photos': self.fireplace_enclosured_photos or []
            },
            'clearanceWithinEnclosure': {
                'requiredValue': self.clearance_within_enclosure_required,
                'presentValue': self.clearance_within_enclosure_present,
                'codeCompliance': self.clearance_within_enclosure_compliance,
                'photos': self.clearance_within_enclosure_photos or []
            },
            'gravityVentClearance': {
                'requiredValue': self.gravity_vent_clearance_required,
                'presentValue': self.gravity_vent_clearance_present,
                'codeCompliance': self.gravity_vent_clearance_compliance,
                'photos': self.gravity_vent_clearance_photos or []
            },
            'gravityVentGrilleClearance': {
                'requiredValue': self.gravity_vent_grille_clearance_required,
                'presentValue': self.gravity_vent_grille_clearance_present,
                'codeCompliance': self.gravity_vent_grille_clearance_compliance,
                'photos': self.gravity_vent_grille_clearance_photos or []
            },
            'hearthMaterials': {
                'requiredValue': self.hearth_materials_required,
                'presentValue': self.hearth_materials_present,
                'codeCompliance': self.hearth_materials_compliance,
                'photos': self.hearth_materials_photos or []
            },
            'centralHeatingKit': {
                'requiredValue': self.central_heating_kit_required,
                'presentValue': self.central_heating_kit_present,
                'codeCompliance': self.central_heating_kit_compliance,
                'photos': self.central_heating_kit_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class FireplaceSafetyFeatures(db.Model):
    __tablename__ = 'fireplace_safety_features'
    
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # Glass Doors (Section 19)
    glass_doors_required = db.Column(db.String(255))
    glass_doors_present = db.Column(db.String(255))
    glass_doors_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    glass_doors_photos = db.Column(db.JSON)
    
    # Fire Screen (Section 20)
    fire_screen_required = db.Column(db.String(255))
    fire_screen_present = db.Column(db.String(255))
    fire_screen_compliance = db.Column(db.String(10))
    fire_screen_photos = db.Column(db.JSON)
    
    # Chase Framing Size (Section 21)
    chase_framing_size_required = db.Column(db.String(255))
    chase_framing_size_present = db.Column(db.String(255))
    chase_framing_size_compliance = db.Column(db.String(10))
    chase_framing_size_photos = db.Column(db.JSON)
    
    # Chase Insulated (Section 22)
    chase_insulated_required = db.Column(db.String(255))
    chase_insulated_present = db.Column(db.String(255))
    chase_insulated_compliance = db.Column(db.String(10))
    chase_insulated_photos = db.Column(db.JSON)
    
    # Chase Clear of Debris (Section 23)
    chase_clear_of_debris_required = db.Column(db.String(255))
    chase_clear_of_debris_present = db.Column(db.String(255))
    chase_clear_of_debris_compliance = db.Column(db.String(10))
    chase_clear_of_debris_photos = db.Column(db.JSON)
    
    # Outdoor Combustion Air (Section 24)
    outdoor_combustion_air_required = db.Column(db.String(255))
    outdoor_combustion_air_present = db.Column(db.String(255))
    outdoor_combustion_air_compliance = db.Column(db.String(10))
    outdoor_combustion_air_photos = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_safety_features', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'glassDoors': {
                'requiredValue': self.glass_doors_required,
                'presentValue': self.glass_doors_present,
                'codeCompliance': self.glass_doors_compliance,
                'photos': self.glass_doors_photos or []
            },
            'fireScreen': {
                'requiredValue': self.fire_screen_required,
                'presentValue': self.fire_screen_present,
                'codeCompliance': self.fire_screen_compliance,
                'photos': self.fire_screen_photos or []
            },
            'chaseFramingSize': {
                'requiredValue': self.chase_framing_size_required,
                'presentValue': self.chase_framing_size_present,
                'codeCompliance': self.chase_framing_size_compliance,
                'photos': self.chase_framing_size_photos or []
            },
            'chaseInsulated': {
                'requiredValue': self.chase_insulated_required,
                'presentValue': self.chase_insulated_present,
                'codeCompliance': self.chase_insulated_compliance,
                'photos': self.chase_insulated_photos or []
            },
            'chaseClearOfDebris': {
                'requiredValue': self.chase_clear_of_debris_required,
                'presentValue': self.chase_clear_of_debris_present,
                'codeCompliance': self.chase_clear_of_debris_compliance,
                'photos': self.chase_clear_of_debris_photos or []
            },
            'outdoorCombustionAir': {
                'requiredValue': self.outdoor_combustion_air_required,
                'presentValue': self.outdoor_combustion_air_present,
                'codeCompliance': self.outdoor_combustion_air_compliance,
                'photos': self.outdoor_combustion_air_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ChimneySupportConnection(db.Model):
    __tablename__ = 'chimney_support_connection'
    
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # CO Alarm Sections
    co_alarm_same_room_bcbc_required = db.Column(db.String(255))
    co_alarm_same_room_bcbc_present = db.Column(db.String(255))
    co_alarm_same_room_bcbc_compliance = db.Column(db.String(10))
    co_alarm_same_room_bcbc_photos = db.Column(db.JSON)

    co_alarm_same_room_nbcabc_required = db.Column(db.String(255))
    co_alarm_same_room_nbcabc_present = db.Column(db.String(255))
    co_alarm_same_room_nbcabc_compliance = db.Column(db.String(10))
    co_alarm_same_room_nbcabc_photos = db.Column(db.JSON)

    co_alarm_present_obc_required = db.Column(db.String(255))
    co_alarm_present_obc_present = db.Column(db.String(255))
    co_alarm_present_obc_compliance = db.Column(db.String(10))
    co_alarm_present_obc_photos = db.Column(db.JSON)

    # Note fields
    clearance_requirements = db.Column(db.String(255))
    note_required_value = db.Column(db.String(255))
    note_present_value = db.Column(db.String(255))
    note_code_compliance = db.Column(db.String(10))

    fire_resistant_solid_chase_required = db.Column(db.String(255))
    fire_resistant_solid_chase_present = db.Column(db.String(255))
    fire_resistant_solid_chase_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    fire_resistant_solid_chase_photos = db.Column(db.JSON)
    
    # Properly Secured Chase (Section 26)
    properly_secured_chase_required = db.Column(db.String(255))
    properly_secured_chase_present = db.Column(db.String(255))
    properly_secured_chase_compliance = db.Column(db.String(10))
    properly_secured_chase_photos = db.Column(db.JSON)
    
    # Is Proper (Section 27)
    is_proper_required = db.Column(db.String(255))
    is_proper_present = db.Column(db.String(255))
    is_proper_compliance = db.Column(db.String(10))
    is_proper_photos = db.Column(db.JSON)
    
    # Fire Retardant Clearances (Section 28)
    fire_retardant_clearances_required = db.Column(db.String(255))
    fire_retardant_clearances_present = db.Column(db.String(255))
    fire_retardant_clearances_compliance = db.Column(db.String(10))
    fire_retardant_clearances_photos = db.Column(db.JSON)
    
    # Foundation Footing Connection (Section 29)
    foundation_footing_connection_required = db.Column(db.String(255))
    foundation_footing_connection_present = db.Column(db.String(255))
    foundation_footing_connection_compliance = db.Column(db.String(10))
    foundation_footing_connection_photos = db.Column(db.JSON)
    
    # Well Supported (Section 30)
    well_supported_required = db.Column(db.String(255))
    well_supported_present = db.Column(db.String(255))
    well_supported_compliance = db.Column(db.String(10))
    well_supported_photos = db.Column(db.JSON)
    
    # Windows Foundation Aesthetic (Section 31)
    windows_foundation_aesthetic_required = db.Column(db.String(255))
    windows_foundation_aesthetic_present = db.Column(db.String(255))
    windows_foundation_aesthetic_compliance = db.Column(db.String(10))
    windows_foundation_aesthetic_photos = db.Column(db.JSON)
    
    # Roof System (Section 32)
    roof_system_required = db.Column(db.String(255))
    roof_system_present = db.Column(db.String(255))
    roof_system_compliance = db.Column(db.String(10))
    roof_system_photos = db.Column(db.JSON)
    
    # Penetrating (Section 33)
    penetrating_required = db.Column(db.String(255))
    penetrating_present = db.Column(db.String(255))
    penetrating_compliance = db.Column(db.String(10))
    penetrating_photos = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('chimney_support_connection', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'coAlarmSameRoomBCBC': {
                'requiredValue': self.co_alarm_same_room_bcbc_required,
                'presentValue': self.co_alarm_same_room_bcbc_present,
                'codeCompliance': self.co_alarm_same_room_bcbc_compliance,
                'photos': self.co_alarm_same_room_bcbc_photos or []
            },
            'coAlarmSameRoomNBCABC': {
                'requiredValue': self.co_alarm_same_room_nbcabc_required,
                'presentValue': self.co_alarm_same_room_nbcabc_present,
                'codeCompliance': self.co_alarm_same_room_nbcabc_compliance,
                'photos': self.co_alarm_same_room_nbcabc_photos or []
            },
            'coAlarmPresentOBC': {
                'requiredValue': self.co_alarm_present_obc_required,
                'presentValue': self.co_alarm_present_obc_present,
                'codeCompliance': self.co_alarm_present_obc_compliance,
                'photos': self.co_alarm_present_obc_photos or []
            },
            'clearanceRequirements': self.clearance_requirements,
            'noteRequiredValue': self.note_required_value,
            'notePresentValue': self.note_present_value,
            'noteCodeCompliance': self.note_code_compliance,
            'fireResistantSolidChase': {
                'requiredValue': self.fire_resistant_solid_chase_required,
                'presentValue': self.fire_resistant_solid_chase_present,
                'codeCompliance': self.fire_resistant_solid_chase_compliance,
                'photos': self.fire_resistant_solid_chase_photos or []
            },
            'properlySecuredChase': {
                'requiredValue': self.properly_secured_chase_required,
                'presentValue': self.properly_secured_chase_present,
                'codeCompliance': self.properly_secured_chase_compliance,
                'photos': self.properly_secured_chase_photos or []
            },
            'isProper': {
                'requiredValue': self.is_proper_required,
                'presentValue': self.is_proper_present,
                'codeCompliance': self.is_proper_compliance,
                'photos': self.is_proper_photos or []
            },
            'fireRetardantClearances': {
                'requiredValue': self.fire_retardant_clearances_required,
                'presentValue': self.fire_retardant_clearances_present,
                'codeCompliance': self.fire_retardant_clearances_compliance,
                'photos': self.fire_retardant_clearances_photos or []
            },
            'foundationFootingConnection': {
                'requiredValue': self.foundation_footing_connection_required,
                'presentValue': self.foundation_footing_connection_present,
                'codeCompliance': self.foundation_footing_connection_compliance,
                'photos': self.foundation_footing_connection_photos or []
            },
            'wellSupported': {
                'requiredValue': self.well_supported_required,
                'presentValue': self.well_supported_present,
                'codeCompliance': self.well_supported_compliance,
                'photos': self.well_supported_photos or []
            },
            'windowsFoundationAesthetic': {
                'requiredValue': self.windows_foundation_aesthetic_required,
                'presentValue': self.windows_foundation_aesthetic_present,
                'codeCompliance': self.windows_foundation_aesthetic_compliance,
                'photos': self.windows_foundation_aesthetic_photos or []
            },
            'roofSystem': {
                'requiredValue': self.roof_system_required,
                'presentValue': self.roof_system_present,
                'codeCompliance': self.roof_system_compliance,
                'photos': self.roof_system_photos or []
            },
            'penetrating': {
                'requiredValue': self.penetrating_required,
                'presentValue': self.penetrating_present,
                'codeCompliance': self.penetrating_compliance,
                'photos': self.penetrating_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AtticRadiationProtection(db.Model):
    __tablename__ = 'attic_radiation_protection'
    
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # Wall Support Brand (Section 35)
    wall_support_brand_required = db.Column(db.String(255))
    wall_support_brand_present = db.Column(db.String(255))
    wall_support_brand_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    wall_support_brand_photos = db.Column(db.JSON)
    
    # Attic Radiation Shield (Section 36)
    attic_radiation_shield_required = db.Column(db.String(255))
    attic_radiation_shield_present = db.Column(db.String(255))
    attic_radiation_shield_compliance = db.Column(db.String(10))
    attic_radiation_shield_photos = db.Column(db.JSON)
    
    # Attic Shield Above Insulation (Section 37)
    attic_shield_above_insulation_required = db.Column(db.String(255))
    attic_shield_above_insulation_present = db.Column(db.String(255))
    attic_shield_above_insulation_compliance = db.Column(db.String(10))
    attic_shield_above_insulation_photos = db.Column(db.JSON)
    
    # Other Radiation Shields (Section 38)
    other_radiation_shields_required = db.Column(db.String(255))
    other_radiation_shields_present = db.Column(db.String(255))
    other_radiation_shields_compliance = db.Column(db.String(10))
    other_radiation_shields_photos = db.Column(db.JSON)
    
    # Enclosed Through Living Space (Section 39)
    enclosed_through_living_space_required = db.Column(db.String(255))
    enclosed_through_living_space_present = db.Column(db.String(255))
    enclosed_through_living_space_compliance = db.Column(db.String(10))
    enclosed_through_living_space_photos = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('attic_radiation_protection', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'wallSupportBrand': {
                'requiredValue': self.wall_support_brand_required,
                'presentValue': self.wall_support_brand_present,
                'codeCompliance': self.wall_support_brand_compliance,
                'photos': self.wall_support_brand_photos or []
            },
            'atticRadiationShield': {
                'requiredValue': self.attic_radiation_shield_required,
                'presentValue': self.attic_radiation_shield_present,
                'codeCompliance': self.attic_radiation_shield_compliance,
                'photos': self.attic_radiation_shield_photos or []
            },
            'atticShieldAboveInsulation': {
                'requiredValue': self.attic_shield_above_insulation_required,
                'presentValue': self.attic_shield_above_insulation_present,
                'codeCompliance': self.attic_shield_above_insulation_compliance,
                'photos': self.attic_shield_above_insulation_photos or []
            },
            'otherRadiationShields': {
                'requiredValue': self.other_radiation_shields_required,
                'presentValue': self.other_radiation_shields_present,
                'codeCompliance': self.other_radiation_shields_compliance,
                'photos': self.other_radiation_shields_photos or []
            },
            'enclosedThroughLivingSpace': {
                'requiredValue': self.enclosed_through_living_space_required,
                'presentValue': self.enclosed_through_living_space_present,
                'codeCompliance': self.enclosed_through_living_space_compliance,
                'photos': self.enclosed_through_living_space_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class RoofExteriorProtection(db.Model):
    __tablename__ = 'roof_exterior_protection'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Roof Flashing Storm Collar (Section 40)
    roof_flashing_storm_collar_required = db.Column(db.String(255))
    roof_flashing_storm_collar_present = db.Column(db.String(255))
    roof_flashing_storm_collar_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    roof_flashing_storm_collar_photos = db.Column(db.JSON)

    # Rain (Section 41)
    rain_required = db.Column(db.String(255))
    rain_present = db.Column(db.String(255))
    rain_compliance = db.Column(db.String(10))
    rain_photos = db.Column(db.JSON)

    # Rain Cap Spark Arrestor (Section 42)
    rain_cap_spark_arrestor_required = db.Column(db.String(255))
    rain_cap_spark_arrestor_present = db.Column(db.String(255))
    rain_cap_spark_arrestor_compliance = db.Column(db.String(10))
    rain_cap_spark_arrestor_photos = db.Column(db.JSON)

    # Roof Braces (Section 43)
    roof_braces_required = db.Column(db.String(255))
    roof_braces_present = db.Column(db.String(255))
    roof_braces_compliance = db.Column(db.String(10))
    roof_braces_photos = db.Column(db.JSON)

    # Roof Braces Solidly Anchored (Section 44)
    roof_braces_solidly_anchored_required = db.Column(db.String(255))
    roof_braces_solidly_anchored_present = db.Column(db.String(255))
    roof_braces_solidly_anchored_compliance = db.Column(db.String(10))
    roof_braces_solidly_anchored_photos = db.Column(db.JSON)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('roof_exterior_protection', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'roofFlashingStormCollar': {
                'requiredValue': self.roof_flashing_storm_collar_required,
                'presentValue': self.roof_flashing_storm_collar_present,
                'codeCompliance': self.roof_flashing_storm_collar_compliance,
                'photos': self.roof_flashing_storm_collar_photos or []
            },
            'rain': {
                'requiredValue': self.rain_required,
                'presentValue': self.rain_present,
                'codeCompliance': self.rain_compliance,
                'photos': self.rain_photos or []
            },
            'rainCapSparkArrestor': {
                'requiredValue': self.rain_cap_spark_arrestor_required,
                'presentValue': self.rain_cap_spark_arrestor_present,
                'codeCompliance': self.rain_cap_spark_arrestor_compliance,
                'photos': self.rain_cap_spark_arrestor_photos or []
            },
            'roofBraces': {
                'requiredValue': self.roof_braces_required,
                'presentValue': self.roof_braces_present,
                'codeCompliance': self.roof_braces_compliance,
                'photos': self.roof_braces_photos or []
            },
            'roofBracesSolidlyAnchored': {
                'requiredValue': self.roof_braces_solidly_anchored_required,
                'presentValue': self.roof_braces_solidly_anchored_present,
                'codeCompliance': self.roof_braces_solidly_anchored_compliance,
                'photos': self.roof_braces_solidly_anchored_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedChimneyComponentsSupports(db.Model):
    __tablename__ = 'wood_stove_manufactured_chimney_components_supports'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Firestopping section
    firestopping_required = db.Column(db.String(255))
    firestopping_present = db.Column(db.String(255))
    firestopping_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    firestopping_photos = db.Column(db.JSON)

    # Ceiling Support section
    ceiling_support_required = db.Column(db.String(255))  # 'flat' or 'cathedral'
    ceiling_support_present = db.Column(db.String(255))
    ceiling_support_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    ceiling_support_photos = db.Column(db.JSON)

    # Minimum Vertical Extension section
    minimum_vertical_extension_required_uncertified = db.Column(db.String(255))
    minimum_vertical_extension_required_certified = db.Column(db.String(255))
    minimum_vertical_extension_present = db.Column(db.String(255))
    minimum_vertical_extension_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    minimum_vertical_extension_photos = db.Column(db.JSON)

    # Attic Radiation Shield section
    attic_radiation_shield_required = db.Column(db.String(255))
    attic_radiation_shield_present = db.Column(db.String(255))
    attic_radiation_shield_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    attic_radiation_shield_photos = db.Column(db.JSON)

    # Attic Radiation Shield Above Insulation section
    attic_radiation_shield_above_insulation_required = db.Column(db.String(255))
    attic_radiation_shield_above_insulation_present = db.Column(db.String(255))
    attic_radiation_shield_above_insulation_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    attic_radiation_shield_above_insulation_photos = db.Column(db.JSON)

    # Other Radiation Shields section
    other_radiation_shields_required = db.Column(db.String(255))
    other_radiation_shields_present = db.Column(db.String(255))
    other_radiation_shields_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    other_radiation_shields_photos = db.Column(db.JSON)

    # Enclosed Through Living Space section
    enclosed_through_living_space_required = db.Column(db.String(255))
    enclosed_through_living_space_present = db.Column(db.String(255))
    enclosed_through_living_space_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    enclosed_through_living_space_photos = db.Column(db.JSON)

    # Roof Flashing Storm Collar section
    roof_flashing_storm_collar_required = db.Column(db.String(255))
    roof_flashing_storm_collar_present = db.Column(db.String(255))
    roof_flashing_storm_collar_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    roof_flashing_storm_collar_photos = db.Column(db.JSON)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_chimney_components_supports', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'firestopping': {
                'requiredValue': self.firestopping_required,
                'presentValue': self.firestopping_present,
                'codeCompliance': self.firestopping_compliance,
                'photos': self.firestopping_photos or []
            },
            'ceilingSupport': {
                'requiredValue': self.ceiling_support_required,
                'presentValue': self.ceiling_support_present,
                'codeCompliance': self.ceiling_support_compliance,
                'photos': self.ceiling_support_photos or []
            },
            'minimumVerticalExtension': {
                'requiredValueUncertified': self.minimum_vertical_extension_required_uncertified,
                'requiredValueCertified': self.minimum_vertical_extension_required_certified,
                'presentValue': self.minimum_vertical_extension_present,
                'codeCompliance': self.minimum_vertical_extension_compliance,
                'photos': self.minimum_vertical_extension_photos or []
            },
            'atticRadiationShield': {
                'requiredValue': self.attic_radiation_shield_required,
                'presentValue': self.attic_radiation_shield_present,
                'codeCompliance': self.attic_radiation_shield_compliance,
                'photos': self.attic_radiation_shield_photos or []
            },
            'atticRadiationShieldAboveInsulation': {
                'requiredValue': self.attic_radiation_shield_above_insulation_required,
                'presentValue': self.attic_radiation_shield_above_insulation_present,
                'codeCompliance': self.attic_radiation_shield_above_insulation_compliance,
                'photos': self.attic_radiation_shield_above_insulation_photos or []
            },
            'otherRadiationShields': {
                'requiredValue': self.other_radiation_shields_required,
                'presentValue': self.other_radiation_shields_present,
                'codeCompliance': self.other_radiation_shields_compliance,
                'photos': self.other_radiation_shields_photos or []
            },
            'enclosedThroughLivingSpace': {
                'requiredValue': self.enclosed_through_living_space_required,
                'presentValue': self.enclosed_through_living_space_present,
                'codeCompliance': self.enclosed_through_living_space_compliance,
                'photos': self.enclosed_through_living_space_photos or []
            },
            'roofFlashingStormCollar': {
                'requiredValue': self.roof_flashing_storm_collar_required,
                'presentValue': self.roof_flashing_storm_collar_present,
                'codeCompliance': self.roof_flashing_storm_collar_compliance,
                'photos': self.roof_flashing_storm_collar_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedChimneyInspection(db.Model):
    __tablename__ = 'wood_stove_manufactured_chimney_inspection'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Inspection details
    inspection_discussed = db.Column(db.String(10), nullable=True)  # yes/no
    building_permits_available = db.Column(db.String(10), nullable=True)  # yes/no
    time_of_day = db.Column(db.String(20), nullable=True)
    weather_conditions = db.Column(db.Text, nullable=True)
    roofing_type_material = db.Column(db.String(200), nullable=True)
    roof_accessed = db.Column(db.String(10), nullable=True)  # yes/no
    attic_accessed = db.Column(db.String(10), nullable=True)  # yes/no

    # Chimney details
    chimney_make_model = db.Column(db.String(200), nullable=True)
    installation_manual_available = db.Column(db.String(20), nullable=True)  # yes/no/original/web-download
    listing_agency = db.Column(db.String(20), nullable=True)  # ulc/csa/wh-etl/otl/other
    uti = db.Column(db.String(100), nullable=True)
    uti_unknown = db.Column(db.Boolean, default=False)
    certification_standard = db.Column(db.String(20), nullable=True)  # ulc-s604/ulc-s629/other/unknown

    # Assessment
    comments_condition_suitable = db.Column(db.String(10), nullable=True)  # yes/no
    installation = db.Column(db.String(20), nullable=True)  # inside/outside
    chimney_installed_by = db.Column(db.String(200), nullable=True)
    chimney_installed_by_unknown = db.Column(db.Boolean, default=False)
    date = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_chimney_inspection', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'inspectionDiscussed': self.inspection_discussed,
            'buildingPermitsAvailable': self.building_permits_available,
            'timeOfDay': self.time_of_day,
            'weatherConditions': self.weather_conditions,
            'roofingTypeMaterial': self.roofing_type_material,
            'roofAccessed': self.roof_accessed,
            'atticAccessed': self.attic_accessed,
            'chimneyMakeModel': self.chimney_make_model,
            'installationManualAvailable': self.installation_manual_available,
            'listingAgency': self.listing_agency,
            'uti': self.uti,
            'utiUnknown': self.uti_unknown,
            'certificationStandard': self.certification_standard,
            'commentsConditionSuitable': self.comments_condition_suitable,
            'installation': self.installation,
            'chimneyInstalledBy': self.chimney_installed_by,
            'chimneyInstalledByUnknown': self.chimney_installed_by_unknown,
            'date': self.date,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedChimneyStructureClearances(db.Model):
    __tablename__ = 'wood_stove_manufactured_chimney_structure_clearances'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Rain Cap section
    rain_cap_required = db.Column(db.String(10), nullable=True)  # yes/no
    rain_cap_present = db.Column(db.String(255), nullable=True)
    rain_cap_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    rain_cap_photos = db.Column(db.JSON, nullable=True)

    # Rain Cap Spark Arrestor section
    rain_cap_spark_arrestor_required = db.Column(db.String(10), nullable=True)  # yes/no
    rain_cap_spark_arrestor_present = db.Column(db.String(255), nullable=True)
    rain_cap_spark_arrestor_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    rain_cap_spark_arrestor_photos = db.Column(db.JSON, nullable=True)

    # Roof Braces section
    roof_braces_required = db.Column(db.String(10), nullable=True)  # yes/no
    roof_braces_present = db.Column(db.String(255), nullable=True)
    roof_braces_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    roof_braces_photos = db.Column(db.JSON, nullable=True)

    # Roof Brace Solidly Anchored section
    roof_brace_solidly_anchored_required = db.Column(db.String(10), nullable=True)  # yes/no
    roof_brace_solidly_anchored_present = db.Column(db.String(255), nullable=True)
    roof_brace_solidly_anchored_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    roof_brace_solidly_anchored_photos = db.Column(db.JSON, nullable=True)

    # Height Above Roof Surface section
    height_above_roof_surface_required = db.Column(db.String(10), nullable=True)  # yes/no
    height_above_roof_surface_present = db.Column(db.String(255), nullable=True)
    height_above_roof_surface_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    height_above_roof_surface_photos = db.Column(db.JSON, nullable=True)

    # Height Within 3m section
    height_within_3m_required = db.Column(db.String(10), nullable=True)  # yes/no
    height_within_3m_present = db.Column(db.String(255), nullable=True)
    height_within_3m_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    height_within_3m_photos = db.Column(db.JSON, nullable=True)

    # Chimney Height Above Chase Cap section
    chimney_height_above_chase_cap_required_uncertified = db.Column(db.String(255), nullable=True)
    chimney_height_above_chase_cap_required_certified = db.Column(db.String(255), nullable=True)
    chimney_height_above_chase_cap_present = db.Column(db.String(255), nullable=True)
    chimney_height_above_chase_cap_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    chimney_height_above_chase_cap_photos = db.Column(db.JSON, nullable=True)

    # Chimney Clearance To Combustibles section
    chimney_clearance_to_combustibles_required_uncertified = db.Column(db.String(255), nullable=True)
    chimney_clearance_to_combustibles_required_certified = db.Column(db.String(255), nullable=True)
    chimney_clearance_to_combustibles_present = db.Column(db.String(255), nullable=True)
    chimney_clearance_to_combustibles_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    chimney_clearance_to_combustibles_photos = db.Column(db.JSON, nullable=True)

    # Other Areas Of Chimney Enclosed Or Hidden section
    other_areas_of_chimney_enclosed_or_hidden_required = db.Column(db.String(10), nullable=True)  # yes/no
    other_areas_of_chimney_enclosed_or_hidden_present = db.Column(db.String(255), nullable=True)
    other_areas_of_chimney_enclosed_or_hidden_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    other_areas_of_chimney_enclosed_or_hidden_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_chimney_structure_clearances', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'rainCap': {
                'requiredValue': self.rain_cap_required,
                'presentValue': self.rain_cap_present,
                'codeCompliance': self.rain_cap_compliance,
                'photos': self.rain_cap_photos or []
            },
            'rainCapSparkArrestor': {
                'requiredValue': self.rain_cap_spark_arrestor_required,
                'presentValue': self.rain_cap_spark_arrestor_present,
                'codeCompliance': self.rain_cap_spark_arrestor_compliance,
                'photos': self.rain_cap_spark_arrestor_photos or []
            },
            'roofBraces': {
                'requiredValue': self.roof_braces_required,
                'presentValue': self.roof_braces_present,
                'codeCompliance': self.roof_braces_compliance,
                'photos': self.roof_braces_photos or []
            },
            'roofBraceSolidlyAnchored': {
                'requiredValue': self.roof_brace_solidly_anchored_required,
                'presentValue': self.roof_brace_solidly_anchored_present,
                'codeCompliance': self.roof_brace_solidly_anchored_compliance,
                'photos': self.roof_brace_solidly_anchored_photos or []
            },
            'heightAboveRoofSurface': {
                'requiredValue': self.height_above_roof_surface_required,
                'presentValue': self.height_above_roof_surface_present,
                'codeCompliance': self.height_above_roof_surface_compliance,
                'photos': self.height_above_roof_surface_photos or []
            },
            'heightWithin3m': {
                'requiredValue': self.height_within_3m_required,
                'presentValue': self.height_within_3m_present,
                'codeCompliance': self.height_within_3m_compliance,
                'photos': self.height_within_3m_photos or []
            },
            'chimneyHeightAboveChaseCap': {
                'requiredValueUncertified': self.chimney_height_above_chase_cap_required_uncertified,
                'requiredValueCertified': self.chimney_height_above_chase_cap_required_certified,
                'presentValue': self.chimney_height_above_chase_cap_present,
                'codeCompliance': self.chimney_height_above_chase_cap_compliance,
                'photos': self.chimney_height_above_chase_cap_photos or []
            },
            'chimneyClearanceToCombustibles': {
                'requiredValueUncertified': self.chimney_clearance_to_combustibles_required_uncertified,
                'requiredValueCertified': self.chimney_clearance_to_combustibles_required_certified,
                'presentValue': self.chimney_clearance_to_combustibles_present,
                'codeCompliance': self.chimney_clearance_to_combustibles_compliance,
                'photos': self.chimney_clearance_to_combustibles_photos or []
            },
            'otherAreasOfChimneyEnclosedOrHidden': {
                'requiredValue': self.other_areas_of_chimney_enclosed_or_hidden_required,
                'presentValue': self.other_areas_of_chimney_enclosed_or_hidden_present,
                'codeCompliance': self.other_areas_of_chimney_enclosed_or_hidden_compliance,
                'photos': self.other_areas_of_chimney_enclosed_or_hidden_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedClearancesShielding(db.Model):
    __tablename__ = 'wood_stove_manufactured_clearances_shielding'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Combustible Right Side Wall section
    combustible_right_side_wall_required = db.Column(db.String(255), nullable=True)
    combustible_right_side_wall_present = db.Column(db.String(255), nullable=True)
    combustible_right_side_wall_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    combustible_right_side_wall_photos = db.Column(db.JSON, nullable=True)

    # Combustible Left Side Wall section
    combustible_left_side_wall_required = db.Column(db.String(255), nullable=True)
    combustible_left_side_wall_present = db.Column(db.String(255), nullable=True)
    combustible_left_side_wall_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    combustible_left_side_wall_photos = db.Column(db.JSON, nullable=True)

    # Combustible Rear Wall section
    combustible_rear_wall_required = db.Column(db.String(255), nullable=True)
    combustible_rear_wall_present = db.Column(db.String(255), nullable=True)
    combustible_rear_wall_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    combustible_rear_wall_photos = db.Column(db.JSON, nullable=True)

    # Combustible Corner Right Side section
    combustible_corner_right_side_required = db.Column(db.String(255), nullable=True)
    combustible_corner_right_side_present = db.Column(db.String(255), nullable=True)
    combustible_corner_right_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    combustible_corner_right_side_photos = db.Column(db.JSON, nullable=True)

    # Combustible Corner Left Side section
    combustible_corner_left_side_required = db.Column(db.String(255), nullable=True)
    combustible_corner_left_side_present = db.Column(db.String(255), nullable=True)
    combustible_corner_left_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    combustible_corner_left_side_photos = db.Column(db.JSON, nullable=True)

    # Top Ceiling section
    top_ceiling_required = db.Column(db.String(255), nullable=True)
    top_ceiling_present = db.Column(db.String(255), nullable=True)
    top_ceiling_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    top_ceiling_photos = db.Column(db.JSON, nullable=True)

    # Shielding Ceiling section
    shielding_ceiling_required = db.Column(db.String(255), nullable=True)
    shielding_ceiling_present = db.Column(db.String(255), nullable=True)
    shielding_ceiling_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    shielding_ceiling_photos = db.Column(db.JSON, nullable=True)

    # Wall Shielding Rear section
    wall_shielding_rear_required = db.Column(db.String(255), nullable=True)
    wall_shielding_rear_present = db.Column(db.String(255), nullable=True)
    wall_shielding_rear_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_shielding_rear_photos = db.Column(db.JSON, nullable=True)

    # Wall Shielding Right Side section
    wall_shielding_right_side_required = db.Column(db.String(255), nullable=True)
    wall_shielding_right_side_present = db.Column(db.String(255), nullable=True)
    wall_shielding_right_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_shielding_right_side_photos = db.Column(db.JSON, nullable=True)

    # Wall Shielding Left Side section
    wall_shielding_left_side_required = db.Column(db.String(255), nullable=True)
    wall_shielding_left_side_present = db.Column(db.String(255), nullable=True)
    wall_shielding_left_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_shielding_left_side_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_clearances_shielding', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'combustibleRightSideWall': {
                'requiredValue': self.combustible_right_side_wall_required,
                'presentValue': self.combustible_right_side_wall_present,
                'codeCompliance': self.combustible_right_side_wall_compliance,
                'photos': self.combustible_right_side_wall_photos or []
            },
            'combustibleLeftSideWall': {
                'requiredValue': self.combustible_left_side_wall_required,
                'presentValue': self.combustible_left_side_wall_present,
                'codeCompliance': self.combustible_left_side_wall_compliance,
                'photos': self.combustible_left_side_wall_photos or []
            },
            'combustibleRearWall': {
                'requiredValue': self.combustible_rear_wall_required,
                'presentValue': self.combustible_rear_wall_present,
                'codeCompliance': self.combustible_rear_wall_compliance,
                'photos': self.combustible_rear_wall_photos or []
            },
            'combustibleCornerRightSide': {
                'requiredValue': self.combustible_corner_right_side_required,
                'presentValue': self.combustible_corner_right_side_present,
                'codeCompliance': self.combustible_corner_right_side_compliance,
                'photos': self.combustible_corner_right_side_photos or []
            },
            'combustibleCornerLeftSide': {
                'requiredValue': self.combustible_corner_left_side_required,
                'presentValue': self.combustible_corner_left_side_present,
                'codeCompliance': self.combustible_corner_left_side_compliance,
                'photos': self.combustible_corner_left_side_photos or []
            },
            'topCeiling': {
                'requiredValue': self.top_ceiling_required,
                'presentValue': self.top_ceiling_present,
                'codeCompliance': self.top_ceiling_compliance,
                'photos': self.top_ceiling_photos or []
            },
            'shieldingCeiling': {
                'requiredValue': self.shielding_ceiling_required,
                'presentValue': self.shielding_ceiling_present,
                'codeCompliance': self.shielding_ceiling_compliance,
                'photos': self.shielding_ceiling_photos or []
            },
            'wallShieldingRear': {
                'requiredValue': self.wall_shielding_rear_required,
                'presentValue': self.wall_shielding_rear_present,
                'codeCompliance': self.wall_shielding_rear_compliance,
                'photos': self.wall_shielding_rear_photos or []
            },
            'wallShieldingRightSide': {
                'requiredValue': self.wall_shielding_right_side_required,
                'presentValue': self.wall_shielding_right_side_present,
                'codeCompliance': self.wall_shielding_right_side_compliance,
                'photos': self.wall_shielding_right_side_photos or []
            },
            'wallShieldingLeftSide': {
                'requiredValue': self.wall_shielding_left_side_required,
                'presentValue': self.wall_shielding_left_side_present,
                'codeCompliance': self.wall_shielding_left_side_compliance,
                'photos': self.wall_shielding_left_side_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedCombustionAirCOAlarm(db.Model):
    __tablename__ = 'wood_stove_manufactured_combustion_air_co_alarm'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Outdoor Combustion Air section
    outdoor_combustion_air_required_uncertified = db.Column(db.String(10), nullable=True)  # yes/no
    outdoor_combustion_air_required_certified = db.Column(db.String(255), nullable=True)
    outdoor_combustion_air_present = db.Column(db.String(255), nullable=True)
    outdoor_combustion_air_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    outdoor_combustion_air_photos = db.Column(db.JSON, nullable=True)

    # CO Alarm Solid Fuel BCBC section
    co_alarm_solid_fuel_bcbc_required = db.Column(db.String(255), nullable=True)
    co_alarm_solid_fuel_bcbc_present = db.Column(db.String(10), nullable=True)  # yes/no
    co_alarm_solid_fuel_bcbc_compliance = db.Column(db.String(10), nullable=True)  # yes/no/na
    co_alarm_solid_fuel_bcbc_photos = db.Column(db.JSON, nullable=True)

    # CO Alarm Solid Fuel ABC section
    co_alarm_solid_fuel_abc_required = db.Column(db.String(255), nullable=True)
    co_alarm_solid_fuel_abc_present = db.Column(db.String(10), nullable=True)  # yes/no
    co_alarm_solid_fuel_abc_compliance = db.Column(db.String(10), nullable=True)  # yes/no/na
    co_alarm_solid_fuel_abc_photos = db.Column(db.JSON, nullable=True)

    # CO Alarm Present section
    co_alarm_present_required = db.Column(db.String(255), nullable=True)
    co_alarm_present_present = db.Column(db.String(10), nullable=True)  # yes/no
    co_alarm_present_compliance = db.Column(db.String(10), nullable=True)  # yes/no/na
    co_alarm_present_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_combustion_air_co_alarm', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'outdoorCombustionAir': {
                'requiredValueUncertified': self.outdoor_combustion_air_required_uncertified,
                'requiredValueCertified': self.outdoor_combustion_air_required_certified,
                'presentValue': self.outdoor_combustion_air_present,
                'codeCompliance': self.outdoor_combustion_air_compliance,
                'photos': self.outdoor_combustion_air_photos or []
            },
            'coAlarmSolidFuelBCBC': {
                'requiredValue': self.co_alarm_solid_fuel_bcbc_required,
                'presentValue': self.co_alarm_solid_fuel_bcbc_present,
                'codeCompliance': self.co_alarm_solid_fuel_bcbc_compliance,
                'photos': self.co_alarm_solid_fuel_bcbc_photos or []
            },
            'coAlarmSolidFuelABC': {
                'requiredValue': self.co_alarm_solid_fuel_abc_required,
                'presentValue': self.co_alarm_solid_fuel_abc_present,
                'codeCompliance': self.co_alarm_solid_fuel_abc_compliance,
                'photos': self.co_alarm_solid_fuel_abc_photos or []
            },
            'coAlarmPresent': {
                'requiredValue': self.co_alarm_present_required,
                'presentValue': self.co_alarm_present_present,
                'codeCompliance': self.co_alarm_present_compliance,
                'photos': self.co_alarm_present_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedEmberPadFloorProtection(db.Model):
    __tablename__ = 'wood_stove_manufactured_ember_pad_floor_protection'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Ember pad - front section
    ember_pad_front_description = db.Column(db.String(255), nullable=True)
    ember_pad_front_required_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_front_required_certified = db.Column(db.String(255), nullable=True)
    ember_pad_front_present = db.Column(db.String(255), nullable=True)
    ember_pad_front_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    ember_pad_front_photos = db.Column(db.JSON, nullable=True)

    # Ember pad - rear section
    ember_pad_rear_required_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_rear_required_certified = db.Column(db.String(255), nullable=True)
    ember_pad_rear_present = db.Column(db.String(255), nullable=True)
    ember_pad_rear_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    ember_pad_rear_photos = db.Column(db.JSON, nullable=True)

    # Ember pad - right side section
    ember_pad_right_side_required_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_right_side_required_certified = db.Column(db.String(255), nullable=True)
    ember_pad_right_side_present = db.Column(db.String(255), nullable=True)
    ember_pad_right_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    ember_pad_right_side_photos = db.Column(db.JSON, nullable=True)

    # Ember pad - left side section
    ember_pad_left_side_required_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_left_side_required_certified = db.Column(db.String(255), nullable=True)
    ember_pad_left_side_present = db.Column(db.String(255), nullable=True)
    ember_pad_left_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    ember_pad_left_side_photos = db.Column(db.JSON, nullable=True)

    # Radiant heat floor protection - uncertified section
    radiant_heat_floor_protection_uncertified_required = db.Column(db.String(255), nullable=True)
    radiant_heat_floor_protection_uncertified_present = db.Column(db.String(255), nullable=True)
    radiant_heat_floor_protection_uncertified_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    radiant_heat_floor_protection_uncertified_photos = db.Column(db.JSON, nullable=True)

    # Radiant heat floor protection - certified section
    radiant_heat_floor_protection_certified_required = db.Column(db.String(255), nullable=True)
    radiant_heat_floor_protection_certified_present = db.Column(db.String(255), nullable=True)
    radiant_heat_floor_protection_certified_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    radiant_heat_floor_protection_certified_photos = db.Column(db.JSON, nullable=True)

    # Hazardous location section
    hazardous_location_required = db.Column(db.String(255), nullable=True)
    hazardous_location_present = db.Column(db.String(255), nullable=True)
    hazardous_location_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    hazardous_location_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_ember_pad_floor_protection', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'emberPadFront': {
                'description': self.ember_pad_front_description,
                'requiredValueUncertified': self.ember_pad_front_required_uncertified,
                'requiredValueCertified': self.ember_pad_front_required_certified,
                'presentValue': self.ember_pad_front_present,
                'codeCompliance': self.ember_pad_front_compliance,
                'photos': self.ember_pad_front_photos or []
            },
            'emberPadRear': {
                'requiredValueUncertified': self.ember_pad_rear_required_uncertified,
                'requiredValueCertified': self.ember_pad_rear_required_certified,
                'presentValue': self.ember_pad_rear_present,
                'codeCompliance': self.ember_pad_rear_compliance,
                'photos': self.ember_pad_rear_photos or []
            },
            'emberPadRightSide': {
                'requiredValueUncertified': self.ember_pad_right_side_required_uncertified,
                'requiredValueCertified': self.ember_pad_right_side_required_certified,
                'presentValue': self.ember_pad_right_side_present,
                'codeCompliance': self.ember_pad_right_side_compliance,
                'photos': self.ember_pad_right_side_photos or []
            },
            'emberPadLeftSide': {
                'requiredValueUncertified': self.ember_pad_left_side_required_uncertified,
                'requiredValueCertified': self.ember_pad_left_side_required_certified,
                'presentValue': self.ember_pad_left_side_present,
                'codeCompliance': self.ember_pad_left_side_compliance,
                'photos': self.ember_pad_left_side_photos or []
            },
            'radiantHeatFloorProtectionUncertified': {
                'requiredValue': self.radiant_heat_floor_protection_uncertified_required,
                'presentValue': self.radiant_heat_floor_protection_uncertified_present,
                'codeCompliance': self.radiant_heat_floor_protection_uncertified_compliance,
                'photos': self.radiant_heat_floor_protection_uncertified_photos or []
            },
            'radiantHeatFloorProtectionCertified': {
                'requiredValue': self.radiant_heat_floor_protection_certified_required,
                'presentValue': self.radiant_heat_floor_protection_certified_present,
                'codeCompliance': self.radiant_heat_floor_protection_certified_compliance,
                'photos': self.radiant_heat_floor_protection_certified_photos or []
            },
            'hazardousLocation': {
                'requiredValue': self.hazardous_location_required,
                'presentValue': self.hazardous_location_present,
                'codeCompliance': self.hazardous_location_compliance,
                'photos': self.hazardous_location_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedFireCodesCompliance(db.Model):
    __tablename__ = 'wood_stove_manufactured_fire_codes_compliance'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Rule 1 section - Fire Code = 2.6.1.4. Chimneys, Flues and Flue Pipes (1)
    rule1_condition = db.Column(db.Text, nullable=True)
    rule1_comments = db.Column(db.Text, nullable=True)
    rule1_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    rule1_photos = db.Column(db.JSON, nullable=True)

    # Rule 2 section - Fire Code = 2.6.1.4 (2)
    rule2_condition = db.Column(db.Text, nullable=True)
    rule2_comments = db.Column(db.Text, nullable=True)
    rule2_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    rule2_photos = db.Column(db.JSON, nullable=True)

    # Rule 3a section - Fire Code = 2.6.1.4 (3)(a)
    rule3a_condition = db.Column(db.Text, nullable=True)
    rule3a_comments = db.Column(db.Text, nullable=True)
    rule3a_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    rule3a_photos = db.Column(db.JSON, nullable=True)

    # Rule 3b section - Fire Code = 2.6.1.4 (3)(b)
    rule3b_condition = db.Column(db.Text, nullable=True)
    rule3b_comments = db.Column(db.Text, nullable=True)
    rule3b_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    rule3b_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_fire_codes_compliance', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'rule1': {
                'condition': self.rule1_condition,
                'comments': self.rule1_comments,
                'codeCompliance': self.rule1_compliance,
                'photos': self.rule1_photos or []
            },
            'rule2': {
                'condition': self.rule2_condition,
                'comments': self.rule2_comments,
                'codeCompliance': self.rule2_compliance,
                'photos': self.rule2_photos or []
            },
            'rule3a': {
                'condition': self.rule3a_condition,
                'comments': self.rule3a_comments,
                'codeCompliance': self.rule3a_compliance,
                'photos': self.rule3a_photos or []
            },
            'rule3b': {
                'condition': self.rule3b_condition,
                'comments': self.rule3b_comments,
                'codeCompliance': self.rule3b_compliance,
                'photos': self.rule3b_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedFluePipeChimneyConnection(db.Model):
    __tablename__ = 'wood_stove_manufactured_flue_pipe_chimney_connection'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Minimum horizontal extension section
    minimum_horizontal_extension_required = db.Column(db.String(255), nullable=True)
    minimum_horizontal_extension_present = db.Column(db.String(255), nullable=True)
    minimum_horizontal_extension_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    minimum_horizontal_extension_photos = db.Column(db.JSON, nullable=True)

    # Maximum horizontal extension section
    maximum_horizontal_extension_required = db.Column(db.String(255), nullable=True)
    maximum_horizontal_extension_present = db.Column(db.String(255), nullable=True)
    maximum_horizontal_extension_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    maximum_horizontal_extension_photos = db.Column(db.JSON, nullable=True)

    # Wall radiation shield section
    wall_radiation_shield_required = db.Column(db.String(10), nullable=True)  # yes/no
    wall_radiation_shield_present = db.Column(db.String(255), nullable=True)
    wall_radiation_shield_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_radiation_shield_photos = db.Column(db.JSON, nullable=True)

    # Base tee and cap section
    base_tee_and_cap_required = db.Column(db.String(10), nullable=True)  # yes/no
    base_tee_and_cap_present = db.Column(db.String(255), nullable=True)
    base_tee_and_cap_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    base_tee_and_cap_photos = db.Column(db.JSON, nullable=True)

    # Base tee support section
    base_tee_support_required = db.Column(db.String(10), nullable=True)  # yes/no
    base_tee_support_present = db.Column(db.String(255), nullable=True)
    base_tee_support_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    base_tee_support_photos = db.Column(db.JSON, nullable=True)

    # Wall support band section
    wall_support_band_required = db.Column(db.String(10), nullable=True)  # yes/no
    wall_support_band_present = db.Column(db.String(255), nullable=True)
    wall_support_band_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_support_band_photos = db.Column(db.JSON, nullable=True)

    # Distance between supports section
    distance_between_supports_required = db.Column(db.String(10), nullable=True)  # yes/no
    distance_between_supports_present = db.Column(db.String(255), nullable=True)
    distance_between_supports_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    distance_between_supports_photos = db.Column(db.JSON, nullable=True)

    # Chimney offsets section
    chimney_offsets_required = db.Column(db.String(10), nullable=True)  # yes/no
    chimney_offsets_present = db.Column(db.String(255), nullable=True)
    chimney_offsets_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    chimney_offsets_photos = db.Column(db.JSON, nullable=True)

    # Offset support section
    offset_support_required = db.Column(db.String(10), nullable=True)  # yes/no
    offset_support_present = db.Column(db.String(255), nullable=True)
    offset_support_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    offset_support_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_flue_pipe_chimney_connection', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'minimumHorizontalExtension': {
                'requiredValue': self.minimum_horizontal_extension_required,
                'presentValue': self.minimum_horizontal_extension_present,
                'codeCompliance': self.minimum_horizontal_extension_compliance,
                'photos': self.minimum_horizontal_extension_photos or []
            },
            'maximumHorizontalExtension': {
                'requiredValue': self.maximum_horizontal_extension_required,
                'presentValue': self.maximum_horizontal_extension_present,
                'codeCompliance': self.maximum_horizontal_extension_compliance,
                'photos': self.maximum_horizontal_extension_photos or []
            },
            'wallRadiationShield': {
                'requiredValue': self.wall_radiation_shield_required,
                'presentValue': self.wall_radiation_shield_present,
                'codeCompliance': self.wall_radiation_shield_compliance,
                'photos': self.wall_radiation_shield_photos or []
            },
            'baseTeeAndCap': {
                'requiredValue': self.base_tee_and_cap_required,
                'presentValue': self.base_tee_and_cap_present,
                'codeCompliance': self.base_tee_and_cap_compliance,
                'photos': self.base_tee_and_cap_photos or []
            },
            'baseTeeSupport': {
                'requiredValue': self.base_tee_support_required,
                'presentValue': self.base_tee_support_present,
                'codeCompliance': self.base_tee_support_compliance,
                'photos': self.base_tee_support_photos or []
            },
            'wallSupportBand': {
                'requiredValue': self.wall_support_band_required,
                'presentValue': self.wall_support_band_present,
                'codeCompliance': self.wall_support_band_compliance,
                'photos': self.wall_support_band_photos or []
            },
            'distanceBetweenSupports': {
                'requiredValue': self.distance_between_supports_required,
                'presentValue': self.distance_between_supports_present,
                'codeCompliance': self.distance_between_supports_compliance,
                'photos': self.distance_between_supports_photos or []
            },
            'chimneyOffsets': {
                'requiredValue': self.chimney_offsets_required,
                'presentValue': self.chimney_offsets_present,
                'codeCompliance': self.chimney_offsets_compliance,
                'photos': self.chimney_offsets_photos or []
            },
            'offsetSupport': {
                'requiredValue': self.offset_support_required,
                'presentValue': self.offset_support_present,
                'codeCompliance': self.offset_support_compliance,
                'photos': self.offset_support_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedFluePipeComponents(db.Model):
    __tablename__ = 'wood_stove_manufactured_flue_pipe_components'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Material section
    material_required = db.Column(db.String(10), nullable=True)  # yes/no
    material_present = db.Column(db.String(255), nullable=True)
    material_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    material_photos = db.Column(db.JSON, nullable=True)

    # Minimum thickness section
    minimum_thickness_required_016 = db.Column(db.String(255), nullable=True)
    minimum_thickness_required_024 = db.Column(db.String(255), nullable=True)
    minimum_thickness_present = db.Column(db.String(255), nullable=True)
    minimum_thickness_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    minimum_thickness_photos = db.Column(db.JSON, nullable=True)

    # Flue pipe condition section
    flue_pipe_condition_required = db.Column(db.String(10), nullable=True)  # yes/no
    flue_pipe_condition_present = db.Column(db.String(255), nullable=True)
    flue_pipe_condition_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    flue_pipe_condition_photos = db.Column(db.JSON, nullable=True)

    # Flue shielding present section
    flue_shielding_present_required = db.Column(db.String(10), nullable=True)  # yes/no
    flue_shielding_present_present = db.Column(db.String(255), nullable=True)
    flue_shielding_present_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    flue_shielding_present_photos = db.Column(db.JSON, nullable=True)

    # Support: horizontal present section
    support_horizontal_present_required = db.Column(db.String(10), nullable=True)  # yes/no
    support_horizontal_present_present = db.Column(db.String(255), nullable=True)
    support_horizontal_present_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    support_horizontal_present_photos = db.Column(db.JSON, nullable=True)

    # Barometric damper present section
    barometric_damper_present_code_reference = db.Column(db.String(255), nullable=True)
    barometric_damper_present_required = db.Column(db.String(10), nullable=True)  # yes/no
    barometric_damper_present_present = db.Column(db.String(255), nullable=True)
    barometric_damper_present_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    barometric_damper_present_photos = db.Column(db.JSON, nullable=True)

    # Flue-mounted heat reducers present section
    flue_mounted_heat_reducers_present_code_reference = db.Column(db.String(255), nullable=True)
    flue_mounted_heat_reducers_present_required = db.Column(db.String(10), nullable=True)  # yes/no
    flue_mounted_heat_reducers_present_present = db.Column(db.String(255), nullable=True)
    flue_mounted_heat_reducers_present_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    flue_mounted_heat_reducers_present_photos = db.Column(db.JSON, nullable=True)

    # Flue pipe pass through floors ceilings section
    flue_pipe_pass_through_floors_ceilings_required = db.Column(db.String(10), nullable=True)  # yes/no
    flue_pipe_pass_through_floors_ceilings_present = db.Column(db.String(255), nullable=True)
    flue_pipe_pass_through_floors_ceilings_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    flue_pipe_pass_through_floors_ceilings_photos = db.Column(db.JSON, nullable=True)

    # Connection to factory built chimney section
    connection_to_factory_built_chimney_required = db.Column(db.String(10), nullable=True)  # yes/no
    connection_to_factory_built_chimney_present = db.Column(db.String(255), nullable=True)
    connection_to_factory_built_chimney_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    connection_to_factory_built_chimney_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_flue_pipe_components', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'material': {
                'requiredValue': self.material_required,
                'presentValue': self.material_present,
                'codeCompliance': self.material_compliance,
                'photos': self.material_photos or []
            },
            'minimumThickness': {
                'requiredValue016': self.minimum_thickness_required_016,
                'requiredValue024': self.minimum_thickness_required_024,
                'presentValue': self.minimum_thickness_present,
                'codeCompliance': self.minimum_thickness_compliance,
                'photos': self.minimum_thickness_photos or []
            },
            'fluePipeCondition': {
                'requiredValue': self.flue_pipe_condition_required,
                'presentValue': self.flue_pipe_condition_present,
                'codeCompliance': self.flue_pipe_condition_compliance,
                'photos': self.flue_pipe_condition_photos or []
            },
            'flueShieldingPresent': {
                'requiredValue': self.flue_shielding_present_required,
                'presentValue': self.flue_shielding_present_present,
                'codeCompliance': self.flue_shielding_present_compliance,
                'photos': self.flue_shielding_present_photos or []
            },
            'supportHorizontalPresent': {
                'requiredValue': self.support_horizontal_present_required,
                'presentValue': self.support_horizontal_present_present,
                'codeCompliance': self.support_horizontal_present_compliance,
                'photos': self.support_horizontal_present_photos or []
            },
            'barometricDamperPresent': {
                'codeReference': self.barometric_damper_present_code_reference,
                'requiredValue': self.barometric_damper_present_required,
                'presentValue': self.barometric_damper_present_present,
                'codeCompliance': self.barometric_damper_present_compliance,
                'photos': self.barometric_damper_present_photos or []
            },
            'flueMountedHeatReducersPresent': {
                'codeReference': self.flue_mounted_heat_reducers_present_code_reference,
                'requiredValue': self.flue_mounted_heat_reducers_present_required,
                'presentValue': self.flue_mounted_heat_reducers_present_present,
                'codeCompliance': self.flue_mounted_heat_reducers_present_compliance,
                'photos': self.flue_mounted_heat_reducers_present_photos or []
            },
            'fluePipePassThroughFloorsCeilings': {
                'requiredValue': self.flue_pipe_pass_through_floors_ceilings_required,
                'presentValue': self.flue_pipe_pass_through_floors_ceilings_present,
                'codeCompliance': self.flue_pipe_pass_through_floors_ceilings_compliance,
                'photos': self.flue_pipe_pass_through_floors_ceilings_photos or []
            },
            'connectionToFactoryBuiltChimney': {
                'requiredValue': self.connection_to_factory_built_chimney_required,
                'presentValue': self.connection_to_factory_built_chimney_present,
                'codeCompliance': self.connection_to_factory_built_chimney_compliance,
                'photos': self.connection_to_factory_built_chimney_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedFluePipeInfoClearances(db.Model):
    __tablename__ = 'wood_stove_manufactured_flue_pipe_info_clearances'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Flue pipe connector section
    flue_pipe_connector_type = db.Column(db.String(50), nullable=True)  # single-wall, double-wall, ulc-s641
    flue_pipe_connector_diameter = db.Column(db.String(255), nullable=True)
    flue_pipe_connector_manufacturer = db.Column(db.String(255), nullable=True)
    flue_pipe_connector_model = db.Column(db.String(255), nullable=True)
    flue_pipe_connector_listing_agency = db.Column(db.String(255), nullable=True)
    flue_pipe_connector_is_listing_agency_manually_available = db.Column(db.String(10), nullable=True)  # yes/no

    # Wall clearances right side section
    wall_clearances_right_side_required_uncertified = db.Column(db.String(255), nullable=True)
    wall_clearances_right_side_required_certified = db.Column(db.String(255), nullable=True)
    wall_clearances_right_side_present = db.Column(db.String(255), nullable=True)
    wall_clearances_right_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_clearances_right_side_photos = db.Column(db.JSON, nullable=True)

    # Wall clearances left side section
    wall_clearances_left_side_required_uncertified = db.Column(db.String(255), nullable=True)
    wall_clearances_left_side_required_certified = db.Column(db.String(255), nullable=True)
    wall_clearances_left_side_present = db.Column(db.String(255), nullable=True)
    wall_clearances_left_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_clearances_left_side_photos = db.Column(db.JSON, nullable=True)

    # Wall clearances rear wall section
    wall_clearances_rear_wall_required_uncertified = db.Column(db.String(255), nullable=True)
    wall_clearances_rear_wall_required_certified = db.Column(db.String(255), nullable=True)
    wall_clearances_rear_wall_present = db.Column(db.String(255), nullable=True)
    wall_clearances_rear_wall_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_clearances_rear_wall_photos = db.Column(db.JSON, nullable=True)

    # Clearances horizontal pipe section
    clearances_horizontal_pipe_required_uncertified = db.Column(db.String(255), nullable=True)
    clearances_horizontal_pipe_required_certified = db.Column(db.String(255), nullable=True)
    clearances_horizontal_pipe_present = db.Column(db.String(255), nullable=True)
    clearances_horizontal_pipe_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearances_horizontal_pipe_photos = db.Column(db.JSON, nullable=True)

    # Clearances ceiling section
    clearances_ceiling_required_uncertified = db.Column(db.String(255), nullable=True)
    clearances_ceiling_required_certified = db.Column(db.String(255), nullable=True)
    clearances_ceiling_present = db.Column(db.String(255), nullable=True)
    clearances_ceiling_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearances_ceiling_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_flue_pipe_info_clearances', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'fluePipeConnector': {
                'type': self.flue_pipe_connector_type,
                'diameter': self.flue_pipe_connector_diameter,
                'manufacturer': self.flue_pipe_connector_manufacturer,
                'model': self.flue_pipe_connector_model,
                'listingAgency': self.flue_pipe_connector_listing_agency,
                'isListingAgencyManuallyAvailable': self.flue_pipe_connector_is_listing_agency_manually_available
            },
            'wallClearancesRightSide': {
                'requiredValueUncertified': self.wall_clearances_right_side_required_uncertified,
                'requiredValueCertified': self.wall_clearances_right_side_required_certified,
                'presentValue': self.wall_clearances_right_side_present,
                'codeCompliance': self.wall_clearances_right_side_compliance,
                'photos': self.wall_clearances_right_side_photos or []
            },
            'wallClearancesLeftSide': {
                'requiredValueUncertified': self.wall_clearances_left_side_required_uncertified,
                'requiredValueCertified': self.wall_clearances_left_side_required_certified,
                'presentValue': self.wall_clearances_left_side_present,
                'codeCompliance': self.wall_clearances_left_side_compliance,
                'photos': self.wall_clearances_left_side_photos or []
            },
            'wallClearancesRearWall': {
                'requiredValueUncertified': self.wall_clearances_rear_wall_required_uncertified,
                'requiredValueCertified': self.wall_clearances_rear_wall_required_certified,
                'presentValue': self.wall_clearances_rear_wall_present,
                'codeCompliance': self.wall_clearances_rear_wall_compliance,
                'photos': self.wall_clearances_rear_wall_photos or []
            },
            'clearancesHorizontalPipe': {
                'requiredValueUncertified': self.clearances_horizontal_pipe_required_uncertified,
                'requiredValueCertified': self.clearances_horizontal_pipe_required_certified,
                'presentValue': self.clearances_horizontal_pipe_present,
                'codeCompliance': self.clearances_horizontal_pipe_compliance,
                'photos': self.clearances_horizontal_pipe_photos or []
            },
            'clearancesCeiling': {
                'requiredValueUncertified': self.clearances_ceiling_required_uncertified,
                'requiredValueCertified': self.clearances_ceiling_required_certified,
                'presentValue': self.clearances_ceiling_present,
                'codeCompliance': self.clearances_ceiling_compliance,
                'photos': self.clearances_ceiling_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WoodStoveManufacturedFluePipeOrientationJoints(db.Model):
    __tablename__ = 'wood_stove_manufactured_flue_pipe_orientation_joints'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Total length section
    total_length_required = db.Column(db.String(255), nullable=True)
    total_length_present = db.Column(db.String(255), nullable=True)
    total_length_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    total_length_photos = db.Column(db.JSON, nullable=True)

    # Elbows maximum section
    elbows_maximum_required = db.Column(db.String(255), nullable=True)
    elbows_maximum_present = db.Column(db.String(255), nullable=True)
    elbows_maximum_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    elbows_maximum_photos = db.Column(db.JSON, nullable=True)

    # Fastening section
    fastening_required = db.Column(db.String(255), nullable=True)
    fastening_present = db.Column(db.String(255), nullable=True)
    fastening_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    fastening_photos = db.Column(db.JSON, nullable=True)

    # Allowance for expansion section
    allowance_for_expansion_required = db.Column(db.String(255), nullable=True)
    allowance_for_expansion_present = db.Column(db.String(255), nullable=True)
    allowance_for_expansion_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    allowance_for_expansion_photos = db.Column(db.JSON, nullable=True)

    # Flue pipe orientation section
    flue_pipe_orientation_required = db.Column(db.String(255), nullable=True)
    flue_pipe_orientation_present = db.Column(db.String(255), nullable=True)
    flue_pipe_orientation_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    flue_pipe_orientation_photos = db.Column(db.JSON, nullable=True)

    # Joint overlap section
    joint_overlap_required = db.Column(db.String(255), nullable=True)
    joint_overlap_present = db.Column(db.String(255), nullable=True)
    joint_overlap_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    joint_overlap_photos = db.Column(db.JSON, nullable=True)

    # Flue pipe slope section
    flue_pipe_slope_required = db.Column(db.String(255), nullable=True)
    flue_pipe_slope_present = db.Column(db.String(255), nullable=True)
    flue_pipe_slope_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    flue_pipe_slope_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_manufactured_flue_pipe_orientation_joints', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'totalLength': {
                'requiredValue': self.total_length_required,
                'presentValue': self.total_length_present,
                'codeCompliance': self.total_length_compliance,
                'photos': self.total_length_photos or []
            },
            'elbowsMaximum': {
                'requiredValue': self.elbows_maximum_required,
                'presentValue': self.elbows_maximum_present,
                'codeCompliance': self.elbows_maximum_compliance,
                'photos': self.elbows_maximum_photos or []
            },
            'fastening': {
                'requiredValue': self.fastening_required,
                'presentValue': self.fastening_present,
                'codeCompliance': self.fastening_compliance,
                'photos': self.fastening_photos or []
            },
            'allowanceForExpansion': {
                'requiredValue': self.allowance_for_expansion_required,
                'presentValue': self.allowance_for_expansion_present,
                'codeCompliance': self.allowance_for_expansion_compliance,
                'photos': self.allowance_for_expansion_photos or []
            },
            'fluePipeOrientation': {
                'requiredValue': self.flue_pipe_orientation_required,
                'presentValue': self.flue_pipe_orientation_present,
                'codeCompliance': self.flue_pipe_orientation_compliance,
                'photos': self.flue_pipe_orientation_photos or []
            },
            'jointOverlap': {
                'requiredValue': self.joint_overlap_required,
                'presentValue': self.joint_overlap_present,
                'codeCompliance': self.joint_overlap_compliance,
                'photos': self.joint_overlap_photos or []
            },
            'fluePipeSlope': {
                'requiredValue': self.flue_pipe_slope_required,
                'presentValue': self.flue_pipe_slope_present,
                'codeCompliance': self.flue_pipe_slope_compliance,
                'photos': self.flue_pipe_slope_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ChimneyHeightClearance(db.Model):
    __tablename__ = 'chimney_height_clearance'
    
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # Height Above Roof Surface (Section 45)
    height_above_roof_surface_required = db.Column(db.String(255))
    height_above_roof_surface_present = db.Column(db.String(255))
    height_above_roof_surface_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    height_above_roof_surface_photos = db.Column(db.JSON)
    
    # Height Within 3m (Section 46)
    height_within_3m_required = db.Column(db.String(255))
    height_within_3m_present = db.Column(db.String(255))
    height_within_3m_compliance = db.Column(db.String(10))
    height_within_3m_photos = db.Column(db.JSON)
    
    # Cap Height Above Chase (Section 47)
    cap_height_above_chase_required = db.Column(db.String(255))
    cap_height_above_chase_present = db.Column(db.String(255))
    cap_height_above_chase_compliance = db.Column(db.String(10))
    cap_height_above_chase_photos = db.Column(db.JSON)
    
    # Chimney Clearance to Combustibles (Section 48)
    chimney_clearance_to_combustibles_required = db.Column(db.String(255))
    chimney_clearance_to_combustibles_present = db.Column(db.String(255))
    chimney_clearance_to_combustibles_compliance = db.Column(db.String(10))
    chimney_clearance_to_combustibles_photos = db.Column(db.JSON)
    
    # Within 3m Area Enclosed (Section 49)
    within_3m_area_enclosed_required = db.Column(db.String(255))
    within_3m_area_enclosed_present = db.Column(db.String(255))
    within_3m_area_enclosed_compliance = db.Column(db.String(10))
    within_3m_area_enclosed_photos = db.Column(db.JSON)
    

    # Final Note Section
    final_note_clearance_requirements = db.Column(db.String(255))
    final_note_required_value = db.Column(db.String(255))
    final_note_present_value = db.Column(db.String(255))
    final_note_code_compliance = db.Column(db.String(10))
    final_note_photos = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('chimney_height_clearance', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'heightAboveRoofSurface': {
                'requiredValue': self.height_above_roof_surface_required,
                'presentValue': self.height_above_roof_surface_present,
                'codeCompliance': self.height_above_roof_surface_compliance,
                'photos': self.height_above_roof_surface_photos or []
            },
            'heightWithin3m': {
                'requiredValue': self.height_within_3m_required,
                'presentValue': self.height_within_3m_present,
                'codeCompliance': self.height_within_3m_compliance,
                'photos': self.height_within_3m_photos or []
            },
            'capHeightAboveChase': {
                'requiredValue': self.cap_height_above_chase_required,
                'presentValue': self.cap_height_above_chase_present,
                'codeCompliance': self.cap_height_above_chase_compliance,
                'photos': self.cap_height_above_chase_photos or []
            },
            'chimneyClearanceToCombustibles': {
                'requiredValue': self.chimney_clearance_to_combustibles_required,
                'presentValue': self.chimney_clearance_to_combustibles_present,
                'codeCompliance': self.chimney_clearance_to_combustibles_compliance,
                'photos': self.chimney_clearance_to_combustibles_photos or []
            },
            'within3mAreaEnclosed': {
                'requiredValue': self.within_3m_area_enclosed_required,
                'presentValue': self.within_3m_area_enclosed_present,
                'codeCompliance': self.within_3m_area_enclosed_compliance,
                'photos': self.within_3m_area_enclosed_photos or []
            },
            'finalNote': {
                'clearanceRequirements': self.final_note_clearance_requirements,
                'requiredValue': self.final_note_required_value,
                'presentValue': self.final_note_present_value,
                'codeCompliance': self.final_note_code_compliance,
                'photos': self.final_note_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class FireCodesCompliance(db.Model):
    __tablename__ = 'fire_codes_compliance'
    
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # Fire Code 1 - Section 2.6.1.4 (1)
    fire_code_1_condition = db.Column(db.String(255))
    fire_code_1_comments = db.Column(db.Text)
    fire_code_1_compliance = db.Column(db.String(10))  # 'yes', 'no', 'ufi', 'na'
    fire_code_1_photos = db.Column(db.JSON)
    
    # Fire Code 2 - Section 2.6.1.4 (2)
    fire_code_2_condition = db.Column(db.String(255))
    fire_code_2_comments = db.Column(db.Text)
    fire_code_2_compliance = db.Column(db.String(10))
    fire_code_2_photos = db.Column(db.JSON)
    
    # Fire Code 3 - Section 2.6.1.4 (3)
    fire_code_3_condition = db.Column(db.String(255))
    fire_code_3_comments = db.Column(db.Text)
    fire_code_3_compliance = db.Column(db.String(10))
    fire_code_3_photos = db.Column(db.JSON)
    
    # Fire Code 4 - Section 2.6.1.4 (4)
    fire_code_4_condition = db.Column(db.String(255))
    fire_code_4_comments = db.Column(db.Text)
    fire_code_4_compliance = db.Column(db.String(10))
    fire_code_4_photos = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fire_codes_compliance', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'fireCode1': {
                'condition': self.fire_code_1_condition,
                'comments': self.fire_code_1_comments,
                'codeCompliance': self.fire_code_1_compliance,
                'photos': self.fire_code_1_photos or []
            },
            'fireCode2': {
                'condition': self.fire_code_2_condition,
                'comments': self.fire_code_2_comments,
                'codeCompliance': self.fire_code_2_compliance,
                'photos': self.fire_code_2_photos or []
            },
            'fireCode3': {
                'condition': self.fire_code_3_condition,
                'comments': self.fire_code_3_comments,
                'codeCompliance': self.fire_code_3_compliance,
                'photos': self.fire_code_3_photos or []
            },
            'fireCode4': {
                'condition': self.fire_code_4_condition,
                'comments': self.fire_code_4_comments,
                'codeCompliance': self.fire_code_4_compliance,
                'photos': self.fire_code_4_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ReportDetails(db.Model):
    __tablename__ = 'report_details'
    
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    
    # Photo information
    photos_taken = db.Column(db.String(10))  # 'yes', 'no'
    number_of_photos_taken = db.Column(db.String(50))
    number_of_photos_in_checklist = db.Column(db.String(50))
    number_of_photos_in_reports = db.Column(db.String(50))
    
    # Comments and observations
    comments_observations = db.Column(db.Text)
    
    # Customer signature and date
    customer_signature = db.Column(db.Text)  # Base64 encoded signature image
    customer_signature_date = db.Column(db.String(50))
    
    # Inspector signature and date
    inspector_signature = db.Column(db.Text)  # Base64 encoded signature image
    inspector_signature_date = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('report_details', uselist=False))
    
    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'photosTaken': self.photos_taken,
            'numberOfPhotosTaken': self.number_of_photos_taken,
            'numberOfPhotosInChecklist': self.number_of_photos_in_checklist,
            'numberOfPhotosInReports': self.number_of_photos_in_reports,
            'commentsObservations': self.comments_observations,
            'customerSignature': self.customer_signature,
            'customerSignatureDate': self.customer_signature_date,
            'inspectorSignature': self.inspector_signature,
            'inspectorSignatureDate': self.inspector_signature_date,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# ==========================================
# FIREPLACE-INSERT FORM MODELS
# ==========================================

class FireplaceInsertChimneySpecification(db.Model):
    __tablename__ = 'fireplace_insert_chimney_specifications'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Inspection details
    inspection_discussed = db.Column(db.String(10), nullable=True)  # yes/no
    building_permits = db.Column(db.String(10), nullable=True)  # yes/no
    time_of_day = db.Column(db.String(20), nullable=True)
    weather_conditions = db.Column(db.Text, nullable=True)
    roofing_type = db.Column(db.String(100), nullable=True)
    roof_accessed = db.Column(db.String(10), nullable=True)  # yes/no
    attic_accessed = db.Column(db.String(10), nullable=True)  # yes/no

    # Access & Construction details
    chimney_constructed_in_building = db.Column(db.String(20), nullable=True)  # yes/no/unknown
    approximate_age = db.Column(db.String(100), nullable=True)

    # Chimney/Fireplace Material details
    shell = db.Column(db.String(200), nullable=True)
    rain_cap = db.Column(db.String(50), nullable=True)  # yes/no/with-screening/without-screening
    number_of_flues = db.Column(db.String(50), nullable=True)
    size_of_flue = db.Column(db.String(100), nullable=True)
    material_of_flue = db.Column(db.String(100), nullable=True)
    chimney_location = db.Column(db.String(20), nullable=True)  # interior/exterior
    height_from_firebox_floor = db.Column(db.String(50), nullable=True)
    chimney_lined_with = db.Column(db.JSON, nullable=True)  # Array of lining materials

    # Fireplace Details
    fireplace_location = db.Column(db.String(20), nullable=True)  # interior/exterior
    installed_in = db.Column(db.JSON, nullable=True)  # Array of installation types
    fireplace_location_in_building = db.Column(db.JSON, nullable=True)  # Array of locations
    other_location = db.Column(db.String(200), nullable=True)

    # Fireplace Lining details
    fireplace_lined_with = db.Column(db.JSON, nullable=True)  # Array of lining materials
    fan_blower_attached = db.Column(db.String(10), nullable=True)  # yes/no

    # Venting System & Condition
    shares_venting_system = db.Column(db.String(10), nullable=True)  # yes/no

    # Original chimney details (keeping for compatibility)
    chimney_make_model = db.Column(db.String(200), nullable=True)
    chimney_listed = db.Column(db.String(20), nullable=True)  # yes/no/unknown
    flue_size = db.Column(db.String(50), nullable=True)
    installation_manual = db.Column(db.String(20), nullable=True)  # yes/no/original/web
    certification_standard = db.Column(db.JSON, nullable=True)  # Array of standards
    listing_agency = db.Column(db.JSON, nullable=True)  # Array of agencies
    comments = db.Column(db.Text, nullable=True)
    suitable = db.Column(db.String(10), nullable=True)  # yes/no
    installation = db.Column(db.String(20), nullable=True)  # inside/outside

    # Installer & Date details
    chimney_installed_by = db.Column(db.String(200), nullable=True)
    chimney_installation_date = db.Column(db.String(50), nullable=True)
    fireplace_installed_by = db.Column(db.String(200), nullable=True)
    fireplace_installation_date = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection_ref = db.relationship('Inspection', backref='fireplace_insert_chimney_specifications')

    def __repr__(self):
        return f'<FireplaceInsertChimneySpecification {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,

            # Inspection details
            'inspection_discussed': self.inspection_discussed,
            'building_permits': self.building_permits,
            'time_of_day': self.time_of_day,
            'weather_conditions': self.weather_conditions,
            'roofing_type': self.roofing_type,
            'roof_accessed': self.roof_accessed,
            'attic_accessed': self.attic_accessed,

            # Access & Construction
            'chimney_constructed_in_building': self.chimney_constructed_in_building,
            'approximate_age': self.approximate_age,

            # Chimney/Fireplace Material
            'shell': self.shell,
            'rain_cap': self.rain_cap,
            'number_of_flues': self.number_of_flues,
            'size_of_flue': self.size_of_flue,
            'material_of_flue': self.material_of_flue,
            'chimney_location': self.chimney_location,
            'height_from_firebox_floor': self.height_from_firebox_floor,
            'chimney_lined_with': self.chimney_lined_with,

            # Fireplace Details
            'fireplace_location': self.fireplace_location,
            'installed_in': self.installed_in,
            'fireplace_location_in_building': self.fireplace_location_in_building,
            'other_location': self.other_location,

            # Fireplace Lining
            'fireplace_lined_with': self.fireplace_lined_with,
            'fan_blower_attached': self.fan_blower_attached,

            # Venting System & Condition
            'shares_venting_system': self.shares_venting_system,

            # Original chimney details (keeping for compatibility)
            'chimney_make_model': self.chimney_make_model,
            'chimney_listed': self.chimney_listed,
            'flue_size': self.flue_size,
            'installation_manual': self.installation_manual,
            'certification_standard': self.certification_standard,
            'listing_agency': self.listing_agency,
            'comments': self.comments,
            'suitable': self.suitable,
            'installation': self.installation,

            # Installer & Date
            'chimney_installed_by': self.chimney_installed_by,
            'chimney_installation_date': self.chimney_installation_date,
            'fireplace_installed_by': self.fireplace_installed_by,
            'fireplace_installation_date': self.fireplace_installation_date,

            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertFireplaceSpecification(db.Model):
    __tablename__ = 'fireplace_insert_fireplace_specifications'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Fireplace details
    fireplace_model_serial = db.Column(db.String(200), nullable=True)

    # Installation Manual
    installation_manual = db.Column(db.String(20), nullable=True)  # yes/no/original/web-download

    # Certification & Listing
    listing_agency = db.Column(db.JSON, nullable=True)  # Array of agencies
    certification_standard = db.Column(db.JSON, nullable=True)  # Array of standards

    # Appliance Type
    appliance_type = db.Column(db.String(30), nullable=True)  # fireplace-insert/hearth-mounted-stove

    # Technical Details
    flue_collar_size = db.Column(db.String(100), nullable=True)
    fan_blower_attached = db.Column(db.String(10), nullable=True)  # yes/no

    # Condition Assessment
    condition_comments = db.Column(db.Text, nullable=True)
    suitable = db.Column(db.String(10), nullable=True)  # yes/no
    mobile_home_approved = db.Column(db.String(10), nullable=True)  # yes/no/na

    # Location & Installation
    installed_in = db.Column(db.JSON, nullable=True)  # Array of installation types
    appliance_location = db.Column(db.JSON, nullable=True)  # Array of locations
    other_installed_in = db.Column(db.String(200), nullable=True)
    other_appliance_location = db.Column(db.String(200), nullable=True)
    appliance_installed_by = db.Column(db.String(200), nullable=True)
    installation_date = db.Column(db.String(50), nullable=True)

    # Legacy fields (keeping for compatibility)
    comments = db.Column(db.Text, nullable=True)
    installed_in_other = db.Column(db.String(200), nullable=True)
    appliance_location_other = db.Column(db.String(200), nullable=True)
    inspection_date = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection_ref = db.relationship('Inspection', backref='fireplace_insert_fireplace_specifications')

    def __repr__(self):
        return f'<FireplaceInsertFireplaceSpecification {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,

            # Fireplace details
            'fireplace_model_serial': self.fireplace_model_serial,

            # Installation Manual
            'installation_manual': self.installation_manual,

            # Certification & Listing
            'listing_agency': self.listing_agency,
            'certification_standard': self.certification_standard,

            # Appliance Type
            'appliance_type': self.appliance_type,

            # Technical Details
            'flue_collar_size': self.flue_collar_size,
            'fan_blower_attached': self.fan_blower_attached,

            # Condition Assessment
            'condition_comments': self.condition_comments,
            'suitable': self.suitable,
            'mobile_home_approved': self.mobile_home_approved,

            # Location & Installation
            'installed_in': self.installed_in,
            'appliance_location': self.appliance_location,
            'other_installed_in': self.other_installed_in,
            'other_appliance_location': self.other_appliance_location,
            'appliance_installed_by': self.appliance_installed_by,
            'installation_date': self.installation_date,

            # Legacy fields (keeping for compatibility)
            'comments': self.comments,
            'installed_in_other': self.installed_in_other,
            'appliance_location_other': self.appliance_location_other,
            'inspection_date': self.inspection_date,

            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertMaterialsClearances(db.Model):
    __tablename__ = 'fireplace_insert_materials_clearances'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Combustible Mantle section
    combustible_mantle_required_uncertified = db.Column(db.String(255), nullable=True)
    combustible_mantle_required_certified = db.Column(db.String(255), nullable=True)
    combustible_mantle_present = db.Column(db.String(255), nullable=True)
    combustible_mantle_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    combustible_mantle_photos = db.Column(db.JSON, nullable=True)

    # Top Trim/Facing section
    top_trim_facing_required_uncertified = db.Column(db.String(255), nullable=True)
    top_trim_facing_required_certified = db.Column(db.String(255), nullable=True)
    top_trim_facing_present = db.Column(db.String(255), nullable=True)
    top_trim_facing_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    top_trim_facing_photos = db.Column(db.JSON, nullable=True)

    # Side Trim/Facing - Right Side section
    side_trim_facing_right_required_uncertified = db.Column(db.String(255), nullable=True)
    side_trim_facing_right_required_certified = db.Column(db.String(255), nullable=True)
    side_trim_facing_right_present = db.Column(db.String(255), nullable=True)
    side_trim_facing_right_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    side_trim_facing_right_photos = db.Column(db.JSON, nullable=True)

    # Side Trim/Facing - Left Side section
    side_trim_facing_left_required_uncertified = db.Column(db.String(255), nullable=True)
    side_trim_facing_left_required_certified = db.Column(db.String(255), nullable=True)
    side_trim_facing_left_present = db.Column(db.String(255), nullable=True)
    side_trim_facing_left_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    side_trim_facing_left_photos = db.Column(db.JSON, nullable=True)

    # Combustible Side Wall section
    combustible_side_wall_required_uncertified = db.Column(db.String(255), nullable=True)
    combustible_side_wall_required_certified = db.Column(db.String(255), nullable=True)
    combustible_side_wall_present = db.Column(db.String(255), nullable=True)
    combustible_side_wall_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    combustible_side_wall_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_materials_clearances', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertMaterialsClearances {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            # Combustible Mantle
            'combustibleMantle': {
                'id': 'combustible-mantle',
                'title': 'Combustible Mantle (height/depth)',
                'requiredUncertified': self.combustible_mantle_required_uncertified,
                'requiredCertified': self.combustible_mantle_required_certified,
                'presentValue': self.combustible_mantle_present,
                'codeCompliance': self.combustible_mantle_compliance,
                'photos': self.combustible_mantle_photos
            },
            # Top Trim/Facing
            'topTrimFacing': {
                'id': 'top-trim-facing',
                'title': 'Top Trim/Facing',
                'requiredUncertified': self.top_trim_facing_required_uncertified,
                'requiredCertified': self.top_trim_facing_required_certified,
                'presentValue': self.top_trim_facing_present,
                'codeCompliance': self.top_trim_facing_compliance,
                'photos': self.top_trim_facing_photos
            },
            # Side Trim/Facing - Right Side
            'sideTrimFacingRight': {
                'id': 'side-trim-facing-right',
                'title': 'Side Trim/Facing – Right Side',
                'requiredUncertified': self.side_trim_facing_right_required_uncertified,
                'requiredCertified': self.side_trim_facing_right_required_certified,
                'presentValue': self.side_trim_facing_right_present,
                'codeCompliance': self.side_trim_facing_right_compliance,
                'photos': self.side_trim_facing_right_photos
            },
            # Side Trim/Facing - Left Side
            'sideTrimFacingLeft': {
                'id': 'side-trim-facing-left',
                'title': 'Side Trim/Facing – Left Side',
                'requiredUncertified': self.side_trim_facing_left_required_uncertified,
                'requiredCertified': self.side_trim_facing_left_required_certified,
                'presentValue': self.side_trim_facing_left_present,
                'codeCompliance': self.side_trim_facing_left_compliance,
                'photos': self.side_trim_facing_left_photos
            },
            # Combustible Side Wall
            'combustibleSideWall': {
                'id': 'combustible-side-wall',
                'title': 'Combustible Side Wall',
                'requiredUncertified': self.combustible_side_wall_required_uncertified,
                'requiredCertified': self.combustible_side_wall_required_certified,
                'presentValue': self.combustible_side_wall_present,
                'codeCompliance': self.combustible_side_wall_compliance,
                'photos': self.combustible_side_wall_photos
            },
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertEmberPadFloorProtection(db.Model):
    __tablename__ = 'fireplace_insert_ember_pad_floor_protection'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Emberpad Material section
    emberpad_material_required_uncertified = db.Column(db.String(255), nullable=True)
    emberpad_material_required_certified = db.Column(db.String(255), nullable=True)
    emberpad_material_present = db.Column(db.String(255), nullable=True)
    emberpad_material_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    emberpad_material_photos = db.Column(db.JSON, nullable=True)

    # Emberpad - Front section
    emberpad_front_required_uncertified = db.Column(db.String(255), nullable=True)
    emberpad_front_required_certified = db.Column(db.String(255), nullable=True)
    emberpad_front_present = db.Column(db.String(255), nullable=True)
    emberpad_front_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    emberpad_front_photos = db.Column(db.JSON, nullable=True)

    # Emberpad - Right Side section
    emberpad_right_side_required_uncertified = db.Column(db.String(255), nullable=True)
    emberpad_right_side_required_certified = db.Column(db.String(255), nullable=True)
    emberpad_right_side_present = db.Column(db.String(255), nullable=True)
    emberpad_right_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    emberpad_right_side_photos = db.Column(db.JSON, nullable=True)

    # Emberpad - Left Side section
    emberpad_left_side_required_uncertified = db.Column(db.String(255), nullable=True)
    emberpad_left_side_required_certified = db.Column(db.String(255), nullable=True)
    emberpad_left_side_present = db.Column(db.String(255), nullable=True)
    emberpad_left_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    emberpad_left_side_photos = db.Column(db.JSON, nullable=True)

    # Floor Protection Material section
    floor_protection_material_required_uncertified = db.Column(db.String(255), nullable=True)
    floor_protection_material_required_certified = db.Column(db.String(255), nullable=True)
    floor_protection_material_present = db.Column(db.String(255), nullable=True)
    floor_protection_material_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    floor_protection_material_photos = db.Column(db.JSON, nullable=True)

    # Radiant Floor Protection section
    radiant_floor_protection_required = db.Column(db.String(255), nullable=True)
    radiant_floor_protection_present = db.Column(db.String(255), nullable=True)
    radiant_floor_protection_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    radiant_floor_protection_photos = db.Column(db.JSON, nullable=True)

    # Floor Protection - Front section
    floor_protection_front_required_uncertified = db.Column(db.String(255), nullable=True)
    floor_protection_front_required_certified = db.Column(db.String(255), nullable=True)
    floor_protection_front_present = db.Column(db.String(255), nullable=True)
    floor_protection_front_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    floor_protection_front_photos = db.Column(db.JSON, nullable=True)

    # Floor Protection - Right Side section
    floor_protection_right_side_required_uncertified = db.Column(db.String(255), nullable=True)
    floor_protection_right_side_required_certified = db.Column(db.String(255), nullable=True)
    floor_protection_right_side_present = db.Column(db.String(255), nullable=True)
    floor_protection_right_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    floor_protection_right_side_photos = db.Column(db.JSON, nullable=True)

    # Floor Protection - Left Side section
    floor_protection_left_side_required_uncertified = db.Column(db.String(255), nullable=True)
    floor_protection_left_side_required_certified = db.Column(db.String(255), nullable=True)
    floor_protection_left_side_present = db.Column(db.String(255), nullable=True)
    floor_protection_left_side_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    floor_protection_left_side_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_ember_pad_floor_protection', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertEmberPadFloorProtection {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            # Emberpad Material
            'emberpadMaterial': {
                'id': 'emberpad-material',
                'title': 'Emberpad Material',
                'requiredUncertified': self.emberpad_material_required_uncertified,
                'requiredCertified': self.emberpad_material_required_certified,
                'presentValue': self.emberpad_material_present,
                'codeCompliance': self.emberpad_material_compliance,
                'photos': self.emberpad_material_photos
            },
            # Emberpad - Front
            'emberpadFront': {
                'id': 'emberpad-front',
                'title': 'Emberpad – Front',
                'requiredUncertified': self.emberpad_front_required_uncertified,
                'requiredCertified': self.emberpad_front_required_certified,
                'presentValue': self.emberpad_front_present,
                'codeCompliance': self.emberpad_front_compliance,
                'photos': self.emberpad_front_photos
            },
            # Emberpad - Right Side
            'emberpadRightSide': {
                'id': 'emberpad-right-side',
                'title': 'Emberpad – Right Side',
                'requiredUncertified': self.emberpad_right_side_required_uncertified,
                'requiredCertified': self.emberpad_right_side_required_certified,
                'presentValue': self.emberpad_right_side_present,
                'codeCompliance': self.emberpad_right_side_compliance,
                'photos': self.emberpad_right_side_photos
            },
            # Emberpad - Left Side
            'emberpadLeftSide': {
                'id': 'emberpad-left-side',
                'title': 'Emberpad – Left Side',
                'requiredUncertified': self.emberpad_left_side_required_uncertified,
                'requiredCertified': self.emberpad_left_side_required_certified,
                'presentValue': self.emberpad_left_side_present,
                'codeCompliance': self.emberpad_left_side_compliance,
                'photos': self.emberpad_left_side_photos
            },
            # Floor Protection Material
            'floorProtectionMaterial': {
                'id': 'floor-protection-material',
                'title': 'Floor Protection Material',
                'requiredUncertified': self.floor_protection_material_required_uncertified,
                'requiredCertified': self.floor_protection_material_required_certified,
                'presentValue': self.floor_protection_material_present,
                'codeCompliance': self.floor_protection_material_compliance,
                'photos': self.floor_protection_material_photos
            },
            # Radiant Floor Protection
            'radiantFloorProtection': {
                'id': 'radiant-floor-protection',
                'title': 'Radiant Floor Protection',
                'requiredValue': self.radiant_floor_protection_required,
                'presentValue': self.radiant_floor_protection_present,
                'codeCompliance': self.radiant_floor_protection_compliance,
                'photos': self.radiant_floor_protection_photos
            },
            # Floor Protection - Front
            'floorProtectionFront': {
                'id': 'floor-protection-front',
                'title': 'Floor Protection – Front',
                'requiredUncertified': self.floor_protection_front_required_uncertified,
                'requiredCertified': self.floor_protection_front_required_certified,
                'presentValue': self.floor_protection_front_present,
                'codeCompliance': self.floor_protection_front_compliance,
                'photos': self.floor_protection_front_photos
            },
            # Floor Protection - Right Side
            'floorProtectionRightSide': {
                'id': 'floor-protection-right-side',
                'title': 'Floor Protection – Right Side',
                'requiredUncertified': self.floor_protection_right_side_required_uncertified,
                'requiredCertified': self.floor_protection_right_side_required_certified,
                'presentValue': self.floor_protection_right_side_present,
                'codeCompliance': self.floor_protection_right_side_compliance,
                'photos': self.floor_protection_right_side_photos
            },
            # Floor Protection - Left Side
            'floorProtectionLeftSide': {
                'id': 'floor-protection-left-side',
                'title': 'Floor Protection – Left Side',
                'requiredUncertified': self.floor_protection_left_side_required_uncertified,
                'requiredCertified': self.floor_protection_left_side_required_certified,
                'presentValue': self.floor_protection_left_side_present,
                'codeCompliance': self.floor_protection_left_side_compliance,
                'photos': self.floor_protection_left_side_photos
            },
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertChimneySupportConnection(db.Model):
    __tablename__ = 'fireplace_insert_chimney_support_connection'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Electrical Outlet / Wires in Firebox section
    electrical_outlet_wires_required_uncertified = db.Column(db.String(255), nullable=True)
    electrical_outlet_wires_required_certified = db.Column(db.String(255), nullable=True)
    electrical_outlet_wires_present = db.Column(db.String(255), nullable=True)
    electrical_outlet_wires_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    electrical_outlet_wires_photos = db.Column(db.JSON, nullable=True)

    # Fireplace Modification section
    fireplace_modification_required_uncertified = db.Column(db.String(255), nullable=True)
    fireplace_modification_required_certified = db.Column(db.String(255), nullable=True)
    fireplace_modification_present = db.Column(db.String(255), nullable=True)
    fireplace_modification_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    fireplace_modification_photos = db.Column(db.JSON, nullable=True)
    fireplace_modification_has_been_modified = db.Column(db.String(10), nullable=True)  # yes/no

    # CO Alarm in Same Room (Solid-Fuel-Burning Appliance) section
    co_alarm_solid_fuel_required = db.Column(db.String(255), nullable=True)
    co_alarm_solid_fuel_present = db.Column(db.String(255), nullable=True)
    co_alarm_solid_fuel_compliance = db.Column(db.String(10), nullable=True)  # yes/no/na
    co_alarm_solid_fuel_photos = db.Column(db.JSON, nullable=True)

    # CO Alarm in Same Room (Solid-Fuel-Burning – NBC/ABC) section
    co_alarm_solid_fuel_nbc_required = db.Column(db.String(255), nullable=True)
    co_alarm_solid_fuel_nbc_present = db.Column(db.String(255), nullable=True)
    co_alarm_solid_fuel_nbc_compliance = db.Column(db.String(10), nullable=True)  # yes/no/na
    co_alarm_solid_fuel_nbc_photos = db.Column(db.JSON, nullable=True)

    # General CO Alarm Presence section
    general_co_alarm_required = db.Column(db.String(255), nullable=True)
    general_co_alarm_present = db.Column(db.String(255), nullable=True)
    general_co_alarm_compliance = db.Column(db.String(10), nullable=True)  # yes/no/na
    general_co_alarm_photos = db.Column(db.JSON, nullable=True)

    # Notes / Responsibility Statement section
    notes_responsibility_required_uncertified = db.Column(db.String(255), nullable=True)
    notes_responsibility_required_certified = db.Column(db.String(255), nullable=True)
    notes_responsibility_present = db.Column(db.String(255), nullable=True)
    notes_responsibility_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    notes_responsibility_photos = db.Column(db.JSON, nullable=True)
    notes_responsibility_condition = db.Column(db.Text, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_chimney_support_connection', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertChimneySupportConnection {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            # Electrical Outlet / Wires in Firebox
            'electricalOutletWires': {
                'id': 'electrical-outlet-wires',
                'title': 'Electrical Outlet / Wires in Firebox',
                'requiredUncertified': self.electrical_outlet_wires_required_uncertified,
                'requiredCertified': self.electrical_outlet_wires_required_certified,
                'presentValue': self.electrical_outlet_wires_present == 'yes' if self.electrical_outlet_wires_present in ['yes', 'no'] else self.electrical_outlet_wires_present,
                'codeCompliance': self.electrical_outlet_wires_compliance,
                'photos': self.electrical_outlet_wires_photos
            },
            # Fireplace Modification
            'fireplaceModification': {
                'id': 'fireplace-modification',
                'title': 'Fireplace Modification',
                'requiredUncertified': self.fireplace_modification_required_uncertified,
                'requiredCertified': self.fireplace_modification_required_certified,
                'presentValue': self.fireplace_modification_present,
                'codeCompliance': self.fireplace_modification_compliance,
                'photos': self.fireplace_modification_photos,
                'hasFireplaceBeenModified': self.fireplace_modification_has_been_modified == 'yes'
            },
            # CO Alarm in Same Room (Solid-Fuel-Burning Appliance)
            'coAlarmSolidFuel': {
                'id': 'co-alarm-solid-fuel',
                'title': 'CO Alarm in Same Room (Solid-Fuel-Burning Appliance)',
                'requiredValue': self.co_alarm_solid_fuel_required,
                'presentValue': self.co_alarm_solid_fuel_present == 'yes' if self.co_alarm_solid_fuel_present in ['yes', 'no'] else self.co_alarm_solid_fuel_present,
                'codeCompliance': self.co_alarm_solid_fuel_compliance,
                'photos': self.co_alarm_solid_fuel_photos
            },
            # CO Alarm in Same Room (Solid-Fuel-Burning – NBC/ABC)
            'coAlarmSolidFuelNbc': {
                'id': 'co-alarm-solid-fuel-nbc',
                'title': 'CO Alarm in Same Room (Solid-Fuel-Burning – NBC/ABC)',
                'requiredValue': self.co_alarm_solid_fuel_nbc_required,
                'presentValue': self.co_alarm_solid_fuel_nbc_present == 'yes' if self.co_alarm_solid_fuel_nbc_present in ['yes', 'no'] else self.co_alarm_solid_fuel_nbc_present,
                'codeCompliance': self.co_alarm_solid_fuel_nbc_compliance,
                'photos': self.co_alarm_solid_fuel_nbc_photos
            },
            # General CO Alarm Presence
            'generalCoAlarm': {
                'id': 'general-co-alarm',
                'title': 'General CO Alarm Presence',
                'requiredValue': self.general_co_alarm_required,
                'presentValue': self.general_co_alarm_present == 'yes' if self.general_co_alarm_present in ['yes', 'no'] else self.general_co_alarm_present,
                'codeCompliance': self.general_co_alarm_compliance,
                'photos': self.general_co_alarm_photos
            },
            # Notes / Responsibility Statement
            'notesResponsibility': {
                'id': 'notes-responsibility',
                'title': 'Notes / Responsibility Statement',
                'requiredUncertified': self.notes_responsibility_required_uncertified,
                'requiredCertified': self.notes_responsibility_required_certified,
                'presentValue': self.notes_responsibility_present,
                'codeCompliance': self.notes_responsibility_compliance,
                'photos': self.notes_responsibility_photos,
                'condition': self.notes_responsibility_condition
            },
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertFireplaceSafetyFeatures(db.Model):
    __tablename__ = 'fireplace_insert_fireplace_safety_features'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Manufacturer & Model section
    manufacturer_model_manufacturer = db.Column(db.String(255), nullable=True)
    manufacturer_model_model = db.Column(db.String(255), nullable=True)
    manufacturer_model_listing_agency = db.Column(db.String(255), nullable=True)
    manufacturer_model_is_listing_agency_manual_available = db.Column(db.String(10), nullable=True)  # yes/no
    manufacturer_model_present_value = db.Column(db.String(255), nullable=True)
    manufacturer_model_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    manufacturer_model_photos = db.Column(db.JSON, nullable=True)

    # Certification section
    certification_certification_standard = db.Column(db.String(255), nullable=True)
    certification_listing_agency_certification = db.Column(db.String(255), nullable=True)
    certification_diameter = db.Column(db.String(255), nullable=True)
    certification_comments = db.Column(db.Text, nullable=True)
    certification_present_value = db.Column(db.String(255), nullable=True)
    certification_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    certification_photos = db.Column(db.JSON, nullable=True)

    # Liner from Top of Appliance to Top of Chimney section
    liner_from_appliance_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    liner_from_appliance_present_value = db.Column(db.String(255), nullable=True)
    liner_from_appliance_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    liner_from_appliance_photos = db.Column(db.JSON, nullable=True)

    # Connection to Stainless Steel Liner section
    connection_to_liner_required_uncertified = db.Column(db.String(255), nullable=True)
    connection_to_liner_required_certified = db.Column(db.String(255), nullable=True)
    connection_to_liner_present_value = db.Column(db.String(255), nullable=True)
    connection_to_liner_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    connection_to_liner_photos = db.Column(db.JSON, nullable=True)

    # Continuous Liner section
    continuous_liner_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    continuous_liner_present_value = db.Column(db.String(255), nullable=True)
    continuous_liner_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    continuous_liner_photos = db.Column(db.JSON, nullable=True)

    # Connectors section
    connectors_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    connectors_present_value = db.Column(db.String(255), nullable=True)
    connectors_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    connectors_photos = db.Column(db.JSON, nullable=True)

    # Liner Base Tee section
    liner_base_tee_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    liner_base_tee_present_value = db.Column(db.String(255), nullable=True)
    liner_base_tee_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    liner_base_tee_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_fireplace_safety_features', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertFireplaceSafetyFeatures {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,

            # Manufacturer & Model section
            'manufacturerModel': {
                'id': 'manufacturer-model',
                'title': 'Manufacturer & Model',
                'manufacturer': self.manufacturer_model_manufacturer,
                'model': self.manufacturer_model_model,
                'listingAgency': self.manufacturer_model_listing_agency,
                'isListingAgencyManualAvailable': self.manufacturer_model_is_listing_agency_manual_available == 'yes' if self.manufacturer_model_is_listing_agency_manual_available in ['yes', 'no'] else self.manufacturer_model_is_listing_agency_manual_available,
                'presentValue': self.manufacturer_model_present_value,
                'codeCompliance': self.manufacturer_model_code_compliance,
                'photos': self.manufacturer_model_photos or []
            },

            # Certification section
            'certification': {
                'id': 'certification',
                'title': 'Certification',
                'certificationStandard': self.certification_certification_standard,
                'listingAgencyCertification': self.certification_listing_agency_certification,
                'diameter': self.certification_diameter,
                'comments': self.certification_comments,
                'presentValue': self.certification_present_value,
                'codeCompliance': self.certification_code_compliance,
                'photos': self.certification_photos or []
            },

            # Liner from Top of Appliance to Top of Chimney section
            'linerFromAppliance': {
                'id': 'liner-from-appliance',
                'title': 'Liner from Top of Appliance to Top of Chimney',
                'requiredValue': self.liner_from_appliance_required_value == 'yes' if self.liner_from_appliance_required_value in ['yes', 'no'] else self.liner_from_appliance_required_value,
                'presentValue': self.liner_from_appliance_present_value,
                'codeCompliance': self.liner_from_appliance_code_compliance,
                'photos': self.liner_from_appliance_photos or []
            },

            # Connection to Stainless Steel Liner section
            'connectionToLiner': {
                'id': 'connection-to-liner',
                'title': 'Connection to Stainless Steel Liner',
                'requiredUncertified': self.connection_to_liner_required_uncertified,
                'requiredCertified': self.connection_to_liner_required_certified,
                'presentValue': self.connection_to_liner_present_value,
                'codeCompliance': self.connection_to_liner_code_compliance,
                'photos': self.connection_to_liner_photos or []
            },

            # Continuous Liner section
            'continuousLiner': {
                'id': 'continuous-liner',
                'title': 'Continuous Liner',
                'requiredValue': self.continuous_liner_required_value == 'yes' if self.continuous_liner_required_value in ['yes', 'no'] else self.continuous_liner_required_value,
                'presentValue': self.continuous_liner_present_value,
                'codeCompliance': self.continuous_liner_code_compliance,
                'photos': self.continuous_liner_photos or []
            },

            # Connectors section
            'connectors': {
                'id': 'connectors',
                'title': 'Connectors',
                'requiredValue': self.connectors_required_value == 'yes' if self.connectors_required_value in ['yes', 'no'] else self.connectors_required_value,
                'presentValue': self.connectors_present_value,
                'codeCompliance': self.connectors_code_compliance,
                'photos': self.connectors_photos or []
            },

            # Liner Base Tee section
            'linerBaseTee': {
                'id': 'liner-base-tee',
                'title': 'Liner Base Tee',
                'requiredValue': self.liner_base_tee_required_value == 'yes' if self.liner_base_tee_required_value in ['yes', 'no'] else self.liner_base_tee_required_value,
                'presentValue': self.liner_base_tee_present_value,
                'codeCompliance': self.liner_base_tee_code_compliance,
                'photos': self.liner_base_tee_photos or []
            },

            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertLinerApplianceChecks(db.Model):
    __tablename__ = 'fireplace_insert_liner_appliance_checks'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Liner Base Tee Support section
    liner_base_tee_support_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    liner_base_tee_support_present_value = db.Column(db.String(255), nullable=True)
    liner_base_tee_support_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    liner_base_tee_support_photos = db.Column(db.JSON, nullable=True)

    # Liner / Flashing / Storm Collar section
    liner_flashing_storm_collar_required_uncertified = db.Column(db.String(255), nullable=True)
    liner_flashing_storm_collar_required_certified = db.Column(db.String(255), nullable=True)
    liner_flashing_storm_collar_present_value = db.Column(db.String(255), nullable=True)
    liner_flashing_storm_collar_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    liner_flashing_storm_collar_photos = db.Column(db.JSON, nullable=True)

    # Insulated Liner section
    insulated_liner_required_uncertified = db.Column(db.String(255), nullable=True)
    insulated_liner_required_certified = db.Column(db.String(255), nullable=True)
    insulated_liner_present_value = db.Column(db.String(255), nullable=True)
    insulated_liner_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    insulated_liner_photos = db.Column(db.JSON, nullable=True)

    # Clearance / Requirements section
    clearance_requirements_enter_data = db.Column(db.Text, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_liner_appliance_checks', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertLinerApplianceChecks {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,

            # Liner Base Tee Support section
            'linerBaseTeeSupport': {
                'id': 'liner-base-tee-support',
                'title': 'Liner Base Tee Support',
                'requiredValue': self.liner_base_tee_support_required_value == 'yes' if self.liner_base_tee_support_required_value in ['yes', 'no'] else self.liner_base_tee_support_required_value,
                'presentValue': self.liner_base_tee_support_present_value,
                'codeCompliance': self.liner_base_tee_support_code_compliance,
                'photos': self.liner_base_tee_support_photos or []
            },

            # Liner / Flashing / Storm Collar section
            'linerFlashingStormCollar': {
                'id': 'liner-flashing-storm-collar',
                'title': 'Liner / Flashing / Storm Collar',
                'requiredUncertified': self.liner_flashing_storm_collar_required_uncertified,
                'requiredCertified': self.liner_flashing_storm_collar_required_certified,
                'presentValue': self.liner_flashing_storm_collar_present_value,
                'codeCompliance': self.liner_flashing_storm_collar_code_compliance,
                'photos': self.liner_flashing_storm_collar_photos or []
            },

            # Insulated Liner section
            'insulatedLiner': {
                'id': 'insulated-liner',
                'title': 'Insulated Liner',
                'requiredUncertified': self.insulated_liner_required_uncertified,
                'requiredCertified': self.insulated_liner_required_certified,
                'presentValue': self.insulated_liner_present_value,
                'codeCompliance': self.insulated_liner_code_compliance,
                'photos': self.insulated_liner_photos or []
            },

            # Clearance / Requirements section
            'clearanceRequirements': {
                'id': 'clearance-requirements',
                'title': 'Clearance / Requirements',
                'enterData': self.clearance_requirements_enter_data
            },

            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertApplianceMasonryChecks(db.Model):
    __tablename__ = 'fireplace_insert_appliance_masonry_checks'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Appliance Standard section
    appliance_standard_condition = db.Column(db.String(255), nullable=True)
    appliance_standard_comments = db.Column(db.Text, nullable=True)
    appliance_standard_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    appliance_standard_photos = db.Column(db.JSON, nullable=True)

    # Footings section
    footings_condition = db.Column(db.String(255), nullable=True)
    footings_comments = db.Column(db.Text, nullable=True)
    footings_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    footings_photos = db.Column(db.JSON, nullable=True)

    # Fireplace Chimneys section
    fireplace_chimneys_condition = db.Column(db.String(255), nullable=True)
    fireplace_chimneys_comments = db.Column(db.Text, nullable=True)
    fireplace_chimneys_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    fireplace_chimneys_photos = db.Column(db.JSON, nullable=True)
    fireplace_chimneys_height = db.Column(db.String(255), nullable=True)
    fireplace_chimneys_width = db.Column(db.String(255), nullable=True)
    fireplace_chimneys_total = db.Column(db.String(255), nullable=True)
    fireplace_chimneys_flues_required = db.Column(db.String(255), nullable=True)

    # ABC/BCBC/NBC Lintels or Arches section
    lintels_arches_condition = db.Column(db.String(255), nullable=True)
    lintels_arches_comments = db.Column(db.Text, nullable=True)
    lintels_arches_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    lintels_arches_photos = db.Column(db.JSON, nullable=True)

    # OBC Lintels or Arches section
    obc_lintels_arches_condition = db.Column(db.String(255), nullable=True)
    obc_lintels_arches_comments = db.Column(db.Text, nullable=True)
    obc_lintels_arches_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    obc_lintels_arches_photos = db.Column(db.JSON, nullable=True)

    # Corbelling section
    corbelling_condition = db.Column(db.String(255), nullable=True)
    corbelling_comments = db.Column(db.Text, nullable=True)
    corbelling_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    corbelling_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_appliance_masonry_checks', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertApplianceMasonryChecks {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,

            # Appliance Standard section
            'applianceStandard': {
                'id': 'appliance-standard',
                'title': 'Appliance Standard – 9.22.10.1',
                'description': 'Fireplace inserts and hearth-mounted stoves vented through the throat of a fireplace shall conform to ULC S628, Fireplace Inserts.',
                'condition': self.appliance_standard_condition,
                'comments': self.appliance_standard_comments,
                'codeCompliance': self.appliance_standard_code_compliance,
                'photos': self.appliance_standard_photos or []
            },

            # Footings section
            'footings': {
                'id': 'footings',
                'title': 'Footings – 9.21.3.1(1)',
                'description': 'Footings for masonry and concrete fireplaces shall conform to Section 9.15.',
                'condition': self.footings_condition,
                'comments': self.footings_comments,
                'codeCompliance': self.footings_code_compliance,
                'photos': self.footings_photos or []
            },

            # Fireplace Chimneys section
            'fireplaceChimneys': {
                'id': 'fireplace-chimneys',
                'title': 'Fireplace Chimneys – 9.21.2.5',
                'description': '(1) The face of a chimney flue serving a masonry fireplace shall conform to Table 9.21.4.2.(1) of Article 9.21.4.2.',
                'condition': self.fireplace_chimneys_condition,
                'comments': self.fireplace_chimneys_comments,
                'codeCompliance': self.fireplace_chimneys_code_compliance,
                'photos': self.fireplace_chimneys_photos or [],
                'height': self.fireplace_chimneys_height,
                'width': self.fireplace_chimneys_width,
                'total': self.fireplace_chimneys_total,
                'fluesRequired': self.fireplace_chimneys_flues_required
            },

            # ABC/BCBC/NBC Lintels or Arches section
            'lintelsArches': {
                'id': 'lintels-arches',
                'title': 'ABC/BCBC/NBC Lintels or Arches – 9.20.5.2',
                'description': '(2) Masonry over openings shall be supported by steel, reinforced concrete lintels or masonry arches designed to support the imposed loads.',
                'condition': self.lintels_arches_condition,
                'comments': self.lintels_arches_comments,
                'codeCompliance': self.lintels_arches_code_compliance,
                'photos': self.lintels_arches_photos or []
            },

            # OBC Lintels or Arches section
            'obcLintelsArches': {
                'id': 'obc-lintels-arches',
                'title': 'OBC 9.20.5.2.(5)A – Lintels or Arches',
                'description': '(1) Masonry over openings shall be supported by steel, reinforced concrete lintels or masonry arches designed to support the imposed loads.\n(2) Except as provided in Sentences (3.1 & 3.2), steel angle lintels supporting masonry veneer above openings shall conform to Table 9.20.5.2.B.\n(3.1) Steel angle lintels described in Sentences (2) shall have a bearing length not less than 90 mm (3½ in.).\n(3.2) Steel angle lintels described in Sentences (2) that exceed 3.0 m (9.8 ft) in length shall have a deflection of not more than 1/720 of the clear span.\n(4) Steel beams, masonry, concrete or steel reinforced concrete arches supporting masonry shall be provided with padstones or alternative protection from corrosion.',
                'condition': self.obc_lintels_arches_condition,
                'comments': self.obc_lintels_arches_comments,
                'codeCompliance': self.obc_lintels_arches_code_compliance,
                'photos': self.obc_lintels_arches_photos or []
            },

            # Corbelling section
            'corbelling': {
                'id': 'corbelling',
                'title': 'Corbelling – 9.20.21.1',
                'description': '(3.2) The unit referred to in Sentence (3) shall be of uniform size. The horizontal projection of any unit shall not exceed 25 mm (1 in.) and the total projection does not exceed one-third of the unit wall thickness.\n(4) As referenced in Table 9.20.5.2.B and where a bearing length is not less than 90 mm (3½ in.).',
                'condition': self.corbelling_condition,
                'comments': self.corbelling_comments,
                'codeCompliance': self.corbelling_code_compliance,
                'photos': self.corbelling_photos or []
            },

            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertCOAlarmsLiners(db.Model):
    __tablename__ = 'fireplace_insert_co_alarms_liners'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # ABC/BCBC/NBC Combustion Air section
    abc_combustion_air_condition = db.Column(db.String(255), nullable=True)
    abc_combustion_air_comments = db.Column(db.Text, nullable=True)
    abc_combustion_air_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    abc_combustion_air_photos = db.Column(db.JSON, nullable=True)

    # NBC/ABC – 9.33.5.5 Combustion Air section
    nbc_combustion_air_condition = db.Column(db.String(255), nullable=True)
    nbc_combustion_air_comments = db.Column(db.Text, nullable=True)
    nbc_combustion_air_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    nbc_combustion_air_photos = db.Column(db.JSON, nullable=True)

    # 5 – OBC – 9.22.1.4 Combustion Air section
    obc_combustion_air_condition = db.Column(db.String(255), nullable=True)
    obc_combustion_air_comments = db.Column(db.Text, nullable=True)
    obc_combustion_air_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    obc_combustion_air_photos = db.Column(db.JSON, nullable=True)

    # Brick or Steel Liners – 9.22.2.1 section
    brick_steel_liners_condition = db.Column(db.String(255), nullable=True)
    brick_steel_liners_comments = db.Column(db.Text, nullable=True)
    brick_steel_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    brick_steel_liners_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners – 9.22.2.2(1) section
    firebrick_liners_1_condition = db.Column(db.String(255), nullable=True)
    firebrick_liners_1_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    firebrick_liners_1_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners – 9.22.2.2(2) section
    firebrick_liners_2_condition = db.Column(db.String(255), nullable=True)
    firebrick_liners_2_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_2_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    firebrick_liners_2_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_co_alarms_liners', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertCOAlarmsLiners {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'abcCombustionAir': {
                'condition': self.abc_combustion_air_condition,
                'comments': self.abc_combustion_air_comments,
                'codeCompliance': self.abc_combustion_air_code_compliance,
                'photos': self.abc_combustion_air_photos or []
            },
            'nbcCombustionAir': {
                'condition': self.nbc_combustion_air_condition,
                'comments': self.nbc_combustion_air_comments,
                'codeCompliance': self.nbc_combustion_air_code_compliance,
                'photos': self.nbc_combustion_air_photos or []
            },
            'obcCombustionAir': {
                'condition': self.obc_combustion_air_condition,
                'comments': self.obc_combustion_air_comments,
                'codeCompliance': self.obc_combustion_air_code_compliance,
                'photos': self.obc_combustion_air_photos or []
            },
            'brickSteelLiners': {
                'condition': self.brick_steel_liners_condition,
                'comments': self.brick_steel_liners_comments,
                'codeCompliance': self.brick_steel_liners_code_compliance,
                'photos': self.brick_steel_liners_photos or []
            },
            'firebrickLiners1': {
                'condition': self.firebrick_liners_1_condition,
                'comments': self.firebrick_liners_1_comments,
                'codeCompliance': self.firebrick_liners_1_code_compliance,
                'photos': self.firebrick_liners_1_photos or []
            },
            'firebrickLiners2': {
                'condition': self.firebrick_liners_2_condition,
                'comments': self.firebrick_liners_2_comments,
                'codeCompliance': self.firebrick_liners_2_code_compliance,
                'photos': self.firebrick_liners_2_photos or []
            },
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertChimneyLinerJointsDetails(db.Model):
    __tablename__ = 'fireplace_insert_chimney_liner_joints_details'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Chimney Liner sections
    chimney_liner_condition_required = db.Column(db.String(255), nullable=True)
    chimney_liner_condition_present = db.Column(db.String(255), nullable=True)
    chimney_liner_condition_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    chimney_liner_condition_photos = db.Column(db.JSON, nullable=True)

    chimney_liner_installation_required = db.Column(db.String(255), nullable=True)
    chimney_liner_installation_present = db.Column(db.String(255), nullable=True)
    chimney_liner_installation_compliance = db.Column(db.String(10), nullable=True)
    chimney_liner_installation_photos = db.Column(db.JSON, nullable=True)

    # Joints sections
    joints_condition_required = db.Column(db.String(255), nullable=True)
    joints_condition_present = db.Column(db.String(255), nullable=True)
    joints_condition_compliance = db.Column(db.String(10), nullable=True)
    joints_condition_photos = db.Column(db.JSON, nullable=True)

    joints_seal_required = db.Column(db.String(255), nullable=True)
    joints_seal_present = db.Column(db.String(255), nullable=True)
    joints_seal_compliance = db.Column(db.String(10), nullable=True)
    joints_seal_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_chimney_liner_joints_details', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertChimneyLinerJointsDetails {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'chimneyLinerConditionRequired': self.chimney_liner_condition_required,
            'chimneyLinerConditionPresent': self.chimney_liner_condition_present,
            'chimneyLinerConditionCompliance': self.chimney_liner_condition_compliance,
            'chimneyLinerConditionPhotos': self.chimney_liner_condition_photos,
            'chimneyLinerInstallationRequired': self.chimney_liner_installation_required,
            'chimneyLinerInstallationPresent': self.chimney_liner_installation_present,
            'chimneyLinerInstallationCompliance': self.chimney_liner_installation_compliance,
            'chimneyLinerInstallationPhotos': self.chimney_liner_installation_photos,
            'jointsConditionRequired': self.joints_condition_required,
            'jointsConditionPresent': self.joints_condition_present,
            'jointsConditionCompliance': self.joints_condition_compliance,
            'jointsConditionPhotos': self.joints_condition_photos,
            'jointsSealRequired': self.joints_seal_required,
            'jointsSealPresent': self.joints_seal_present,
            'jointsSealCompliance': self.joints_seal_compliance,
            'jointsSealPhotos': self.joints_seal_photos,
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertHearthSupport(db.Model):
    __tablename__ = 'fireplace_insert_hearth_support'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Hearth Extension section
    hearth_extension_condition = db.Column(db.String(255), nullable=True)
    hearth_extension_comments = db.Column(db.Text, nullable=True)
    hearth_extension_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    hearth_extension_photos = db.Column(db.JSON, nullable=True)

    # Support of Hearth 1 section
    hearth_support_1_condition = db.Column(db.String(255), nullable=True)
    hearth_support_1_comments = db.Column(db.Text, nullable=True)
    hearth_support_1_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    hearth_support_1_photos = db.Column(db.JSON, nullable=True)

    # Support of Hearth 2 section
    hearth_support_2_condition = db.Column(db.String(255), nullable=True)
    hearth_support_2_comments = db.Column(db.Text, nullable=True)
    hearth_support_2_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    hearth_support_2_photos = db.Column(db.JSON, nullable=True)

    # Slope of Smoke Chamber section
    smoke_chamber_slope_condition = db.Column(db.String(255), nullable=True)
    smoke_chamber_slope_comments = db.Column(db.Text, nullable=True)
    smoke_chamber_slope_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    smoke_chamber_slope_photos = db.Column(db.JSON, nullable=True)

    # Wall Thickness section
    wall_thickness_condition = db.Column(db.String(255), nullable=True)
    wall_thickness_comments = db.Column(db.Text, nullable=True)
    wall_thickness_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    wall_thickness_photos = db.Column(db.JSON, nullable=True)

    # Clearance to Opening section
    clearance_to_opening_condition = db.Column(db.String(255), nullable=True)
    clearance_to_opening_comments = db.Column(db.Text, nullable=True)
    clearance_to_opening_compliance = db.Column(db.String(10), nullable=True)  # yes/no/ufi/na
    clearance_to_opening_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_hearth_support', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertHearthSupport {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'hearthExtension': {
                'condition': self.hearth_extension_condition,
                'comments': self.hearth_extension_comments,
                'codeCompliance': self.hearth_extension_compliance,
                'photos': self.hearth_extension_photos or []
            },
            'hearthSupport1': {
                'condition': self.hearth_support_1_condition,
                'comments': self.hearth_support_1_comments,
                'codeCompliance': self.hearth_support_1_compliance,
                'photos': self.hearth_support_1_photos or []
            },
            'hearthSupport2': {
                'condition': self.hearth_support_2_condition,
                'comments': self.hearth_support_2_comments,
                'codeCompliance': self.hearth_support_2_compliance,
                'photos': self.hearth_support_2_photos or []
            },
            'smokeChamberSlope': {
                'condition': self.smoke_chamber_slope_condition,
                'comments': self.smoke_chamber_slope_comments,
                'codeCompliance': self.smoke_chamber_slope_compliance,
                'photos': self.smoke_chamber_slope_photos or []
            },
            'wallThickness': {
                'condition': self.wall_thickness_condition,
                'comments': self.wall_thickness_comments,
                'codeCompliance': self.wall_thickness_compliance,
                'photos': self.wall_thickness_photos or []
            },
            'clearanceToOpening': {
                'condition': self.clearance_to_opening_condition,
                'comments': self.clearance_to_opening_comments,
                'codeCompliance': self.clearance_to_opening_compliance,
                'photos': self.clearance_to_opening_photos or []
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertClearances(db.Model):
    __tablename__ = 'fireplace_insert_clearances'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Metal Exposed to the Interior section
    metal_exposed_interior_condition = db.Column(db.String(255), nullable=True)
    metal_exposed_interior_comments = db.Column(db.Text, nullable=True)
    metal_exposed_interior_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    metal_exposed_interior_photos = db.Column(db.JSON, nullable=True)

    # Clearance to Combustible Framing (1) section
    clearance_combustible_framing_1_condition = db.Column(db.String(255), nullable=True)
    clearance_combustible_framing_1_comments = db.Column(db.Text, nullable=True)
    clearance_combustible_framing_1_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_combustible_framing_1_photos = db.Column(db.JSON, nullable=True)

    # Clearance to Combustible Framing (3) section
    clearance_combustible_framing_3_condition = db.Column(db.String(255), nullable=True)
    clearance_combustible_framing_3_comments = db.Column(db.Text, nullable=True)
    clearance_combustible_framing_3_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_combustible_framing_3_photos = db.Column(db.JSON, nullable=True)

    # Heat-Circulating Duct Outlets section
    heat_circulating_duct_outlets_condition = db.Column(db.String(255), nullable=True)
    heat_circulating_duct_outlets_comments = db.Column(db.Text, nullable=True)
    heat_circulating_duct_outlets_code_compliance = db.Column(db.String(10), nullable=True)
    heat_circulating_duct_outlets_photos = db.Column(db.JSON, nullable=True)

    # Fireplace Inserts Appliance Standard section
    fireplace_inserts_appliance_standard_condition = db.Column(db.String(255), nullable=True)
    fireplace_inserts_appliance_standard_comments = db.Column(db.Text, nullable=True)
    fireplace_inserts_appliance_standard_code_compliance = db.Column(db.String(10), nullable=True)
    fireplace_inserts_appliance_standard_photos = db.Column(db.JSON, nullable=True)

    # Fireplace Inserts Installation section
    fireplace_inserts_installation_condition = db.Column(db.String(255), nullable=True)
    fireplace_inserts_installation_comments = db.Column(db.Text, nullable=True)
    fireplace_inserts_installation_code_compliance = db.Column(db.String(10), nullable=True)
    fireplace_inserts_installation_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_clearances', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertClearances {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'metalExposedInterior': {
                'condition': self.metal_exposed_interior_condition,
                'comments': self.metal_exposed_interior_comments,
                'codeCompliance': self.metal_exposed_interior_code_compliance,
                'photos': self.metal_exposed_interior_photos or []
            },
            'clearanceCombustibleFraming1': {
                'condition': self.clearance_combustible_framing_1_condition,
                'comments': self.clearance_combustible_framing_1_comments,
                'codeCompliance': self.clearance_combustible_framing_1_code_compliance,
                'photos': self.clearance_combustible_framing_1_photos or []
            },
            'clearanceCombustibleFraming3': {
                'condition': self.clearance_combustible_framing_3_condition,
                'comments': self.clearance_combustible_framing_3_comments,
                'codeCompliance': self.clearance_combustible_framing_3_code_compliance,
                'photos': self.clearance_combustible_framing_3_photos or []
            },
            'heatCirculatingDuctOutlets': {
                'condition': self.heat_circulating_duct_outlets_condition,
                'comments': self.heat_circulating_duct_outlets_comments,
                'codeCompliance': self.heat_circulating_duct_outlets_code_compliance,
                'photos': self.heat_circulating_duct_outlets_photos or []
            },
            'fireplaceInsertsApplianceStandard': {
                'condition': self.fireplace_inserts_appliance_standard_condition,
                'comments': self.fireplace_inserts_appliance_standard_comments,
                'codeCompliance': self.fireplace_inserts_appliance_standard_code_compliance,
                'photos': self.fireplace_inserts_appliance_standard_photos or []
            },
            'fireplaceInsertsInstallation': {
                'condition': self.fireplace_inserts_installation_condition,
                'comments': self.fireplace_inserts_installation_comments,
                'codeCompliance': self.fireplace_inserts_installation_code_compliance,
                'photos': self.fireplace_inserts_installation_photos or []
            },
            'additional_notes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertClearancesLiners(db.Model):
    __tablename__ = 'fireplace_insert_clearances_liners'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # OBC Fireplace Inserts and Hearth-Mounted Stoves – Installation • 9.22.10.2 section
    obc_installation_condition = db.Column(db.String(255), nullable=True)
    obc_installation_comments = db.Column(db.Text, nullable=True)
    obc_installation_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    obc_installation_photos = db.Column(db.JSON, nullable=True)

    # NFC 2.6.1.5 Clearances section
    nfc_clearances_condition = db.Column(db.String(255), nullable=True)
    nfc_clearances_comments = db.Column(db.Text, nullable=True)
    nfc_clearances_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    nfc_clearances_photos = db.Column(db.JSON, nullable=True)

    # Clearance from Combustible Materials – 9.21.5.1(2) section
    clearance_combustible_materials_condition = db.Column(db.String(255), nullable=True)
    clearance_combustible_materials_comments = db.Column(db.Text, nullable=True)
    clearance_combustible_materials_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearance_combustible_materials_photos = db.Column(db.JSON, nullable=True)

    # Wall Thickness – 9.21.4.8(1) section
    wall_thickness_condition = db.Column(db.String(255), nullable=True)
    wall_thickness_comments = db.Column(db.Text, nullable=True)
    wall_thickness_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_thickness_photos = db.Column(db.JSON, nullable=True)

    # Lining Materials – 9.21.3.1(1) section
    lining_materials_condition = db.Column(db.String(255), nullable=True)
    lining_materials_comments = db.Column(db.Text, nullable=True)
    lining_materials_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    lining_materials_photos = db.Column(db.JSON, nullable=True)

    # Clay Liners – 9.21.3.3(1) section
    clay_liners_condition = db.Column(db.String(255), nullable=True)
    clay_liners_comments = db.Column(db.Text, nullable=True)
    clay_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clay_liners_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_clearances_liners', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertClearancesLiners {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'obcInstallation': {
                'id': 'obc-installation',
                'title': 'OBC Fireplace Inserts and Hearth-Mounted Stoves – Installation • 9.22.10.2',
                'description': '(2) Fireplace inserts and hearth-mounted stoves vented through the throat of a fireplace (described in Sentence (1)) may be installed in existing fireplaces only if a minimum thickness of 100 mm of solid masonry is provided between the smoke chamber and any adjoining combustible material, unless the insert is listed for lesser clearances.\n\n(3) A fireplace insert installed in a masonry fireplace shall have:\n\n(a) a listed chimney liner installed from the insert outlet to the top of the chimney, or\n\n(b) a direct connection to the chimney flue where no such liner is part of an insert conforming to Sentence 9.22.10.1(1).',
                'condition': self.obc_installation_condition or '',
                'comments': self.obc_installation_comments or '',
                'codeCompliance': self.obc_installation_code_compliance,
                'photos': self.obc_installation_photos or []
            },
            'nfcClearances': {
                'id': 'nfc-clearances',
                'title': 'NFC 2.6.1.5 Clearances',
                'description': 'Combustible materials shall not be located within the required clearance space surrounding chimneys, flue pipes or appliances, or adjacent to ash pit or cleanout doors.',
                'condition': self.nfc_clearances_condition or '',
                'comments': self.nfc_clearances_comments or '',
                'codeCompliance': self.nfc_clearances_code_compliance,
                'photos': self.nfc_clearances_photos or []
            },
            'clearanceCombustibleMaterials': {
                'id': 'clearance-combustible-materials',
                'title': 'Clearance from Combustible Materials – 9.21.5.1(2)',
                'description': 'A clearance of not less than 150 mm (6") shall be provided between a cleanout opening and combustible material.',
                'condition': self.clearance_combustible_materials_condition or '',
                'comments': self.clearance_combustible_materials_comments or '',
                'codeCompliance': self.clearance_combustible_materials_code_compliance,
                'photos': self.clearance_combustible_materials_photos or []
            },
            'wallThickness': {
                'id': 'wall-thickness',
                'title': 'Wall Thickness – 9.21.4.8(1)',
                'description': 'The walls of a masonry chimney shall be built of solid units not less than:\n\nNBC/ABC/BC/CC: 75 mm (3") thick, or\n\nOBC: 70 mm (2.75") thick.',
                'condition': self.wall_thickness_condition or '',
                'comments': self.wall_thickness_comments or '',
                'codeCompliance': self.wall_thickness_code_compliance,
                'photos': self.wall_thickness_photos or []
            },
            'liningMaterials': {
                'id': 'lining-materials',
                'title': 'Lining Materials – 9.21.3.1(1)',
                'description': 'Every masonry or concrete chimney shall have a lining of clay, concrete, firebrick, or metal.',
                'condition': self.lining_materials_condition or '',
                'comments': self.lining_materials_comments or '',
                'codeCompliance': self.lining_materials_code_compliance,
                'photos': self.lining_materials_photos or []
            },
            'clayLiners': {
                'id': 'clay-liners',
                'title': 'Clay Liners – 9.21.3.3(1)',
                'description': 'Clay liners shall conform to CAN/CSA-A324-M, Clay Flue Liners.',
                'condition': self.clay_liners_condition or '',
                'comments': self.clay_liners_comments or '',
                'codeCompliance': self.clay_liners_code_compliance,
                'photos': self.clay_liners_photos or []
            },
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertLinerDetails(db.Model):
    __tablename__ = 'fireplace_insert_liner_details'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Inclined Chimney Flues – 9.21.2.3 section
    inclined_chimney_flues_condition = db.Column(db.String(255), nullable=True)
    inclined_chimney_flues_comments = db.Column(db.Text, nullable=True)
    inclined_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    inclined_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners – 9.21.3.4(1) section
    firebrick_liners_condition = db.Column(db.String(255), nullable=True)
    firebrick_liners_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    firebrick_liners_photos = db.Column(db.JSON, nullable=True)

    # Concrete Liners – 9.21.3.5(1) section
    concrete_liners_condition = db.Column(db.String(255), nullable=True)
    concrete_liners_comments = db.Column(db.Text, nullable=True)
    concrete_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    concrete_liners_photos = db.Column(db.JSON, nullable=True)

    # Metal Liners – 9.21.3.6 section
    metal_liners_condition = db.Column(db.String(255), nullable=True)
    metal_liners_comments = db.Column(db.Text, nullable=True)
    metal_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    metal_liners_photos = db.Column(db.JSON, nullable=True)

    # Oval Chimney Flues – 9.21.2.6(1) section
    oval_chimney_flues_condition = db.Column(db.String(255), nullable=True)
    oval_chimney_flues_comments = db.Column(db.Text, nullable=True)
    oval_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    oval_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    # Separation of Flue Liners – 9.21.4.9 section
    separation_of_flue_liners_condition = db.Column(db.String(255), nullable=True)
    separation_of_flue_liners_comments = db.Column(db.Text, nullable=True)
    separation_of_flue_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    separation_of_flue_liners_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_liner_details', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertLinerDetails {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'inclinedChimneyFlues': {
                'id': 'inclined-chimney-flues',
                'title': 'Inclined Chimney Flues – 9.21.2.3',
                'description': 'Chimney flues shall not be inclined more than 45° to the vertical.',
                'condition': self.inclined_chimney_flues_condition or '',
                'comments': self.inclined_chimney_flues_comments or '',
                'codeCompliance': self.inclined_chimney_flues_code_compliance,
                'photos': self.inclined_chimney_flues_photos or []
            },
            'firebrickLiners': {
                'id': 'firebrick-liners',
                'title': 'Firebrick Liners – 9.21.3.4(1)',
                'description': 'Firebrick liners shall conform to ASTM C 27, Fireclay and High-Alumina Refractory Brick.\n\nAdditional Reference:\n9.21.3.4(2) Firebrick liners shall be laid with high-temperature cement mortar conforming to CAN/CGSB-10.3, Air-Setting Refractory Mortar.',
                'condition': self.firebrick_liners_condition or '',
                'comments': self.firebrick_liners_comments or '',
                'codeCompliance': self.firebrick_liners_code_compliance,
                'photos': self.firebrick_liners_photos or []
            },
            'concreteLiners': {
                'id': 'concrete-liners',
                'title': 'Concrete Liners – 9.21.3.5(1)',
                'description': 'Concrete flue liners shall conform to Clause 4.2.6.2 of CAN/CSA-A405-M, Design and Construction of Masonry Chimneys and Fireplaces.',
                'condition': self.concrete_liners_condition or '',
                'comments': self.concrete_liners_comments or '',
                'codeCompliance': self.concrete_liners_code_compliance,
                'photos': self.concrete_liners_photos or []
            },
            'metalLiners': {
                'id': 'metal-liners',
                'title': 'Metal Liners – 9.21.3.6',
                'description': 'Metal liners shall be constructed of not less than 0.3 mm thick stainless steel.\n\nMetal liners referred to in Sentence (1) shall only be used in chimneys serving gas- or oil-burning appliances.',
                'condition': self.metal_liners_condition or '',
                'comments': self.metal_liners_comments or '',
                'codeCompliance': self.metal_liners_code_compliance,
                'photos': self.metal_liners_photos or []
            },
            'ovalChimneyFlues': {
                'id': 'oval-chimney-flues',
                'title': 'Oval Chimney Flues – 9.21.2.6(1)',
                'description': 'The width of an oval chimney flue shall be not less than two-thirds its breadth.',
                'condition': self.oval_chimney_flues_condition or '',
                'comments': self.oval_chimney_flues_comments or '',
                'codeCompliance': self.oval_chimney_flues_code_compliance,
                'photos': self.oval_chimney_flues_photos or []
            },
            'separationOfFlueLiners': {
                'id': 'separation-of-flue-liners',
                'title': 'Separation of Flue Liners – 9.21.4.9',
                'description': 'Flue liners in the same chimney shall be separated by not less than:\n\n75 mm (3") of masonry or concrete (exclusive of liners where clay liners are used), or\n\n90 mm (3½") of firebrick where firebrick liners are used.\n\nFlue liners referred to in Sentence (1) shall be installed to prevent significant lateral movement.',
                'condition': self.separation_of_flue_liners_condition or '',
                'comments': self.separation_of_flue_liners_comments or '',
                'codeCompliance': self.separation_of_flue_liners_code_compliance,
                'photos': self.separation_of_flue_liners_photos or []
            },
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertJointsDetails(db.Model):
    __tablename__ = 'fireplace_insert_joints_details'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Joints in Chimney Liners – 9.21.3.2(1) section
    joints_sealing_condition = db.Column(db.String(255), nullable=True)
    joints_sealing_comments = db.Column(db.Text, nullable=True)
    joints_sealing_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    joints_sealing_photos = db.Column(db.JSON, nullable=True)

    # Joints in Chimney Liners – 9.21.3.2(2) section
    joints_flush_condition = db.Column(db.String(255), nullable=True)
    joints_flush_comments = db.Column(db.Text, nullable=True)
    joints_flush_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    joints_flush_photos = db.Column(db.JSON, nullable=True)

    # Installation of Chimney Liners – 9.21.3.7(1) section
    liner_installation_condition = db.Column(db.String(255), nullable=True)
    liner_installation_comments = db.Column(db.Text, nullable=True)
    liner_installation_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    liner_installation_photos = db.Column(db.JSON, nullable=True)

    # Spaces between Liners and Surrounding Masonry – 9.21.3.8(2) section
    liner_spaces_condition = db.Column(db.String(255), nullable=True)
    liner_spaces_comments = db.Column(db.Text, nullable=True)
    liner_spaces_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    liner_spaces_photos = db.Column(db.JSON, nullable=True)

    # Mortar for Chimney Liners – 9.21.3.9 section
    mortar_for_liners_condition = db.Column(db.String(255), nullable=True)
    mortar_for_liners_comments = db.Column(db.Text, nullable=True)
    mortar_for_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    mortar_for_liners_photos = db.Column(db.JSON, nullable=True)

    # Extension of Chimney Liners – 9.21.3.10 section
    liner_extension_condition = db.Column(db.String(255), nullable=True)
    liner_extension_comments = db.Column(db.Text, nullable=True)
    liner_extension_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    liner_extension_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_joints_details', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertJointsDetails {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'jointsSealing': {
                'id': 'joints-sealing',
                'title': 'Joints in Chimney Liners – 9.21.3.2(1)',
                'description': 'Joints at chimney liners shall be sealed to provide a barrier to the passage of flue gases and condensates into the cavity between the liner and the surrounding masonry.',
                'condition': self.joints_sealing_condition or '',
                'comments': self.joints_sealing_comments or '',
                'codeCompliance': self.joints_sealing_code_compliance,
                'photos': self.joints_sealing_photos or []
            },
            'jointsFlush': {
                'id': 'joints-flush',
                'title': 'Joints in Chimney Liners – 9.21.3.2(2)',
                'description': 'Joints of clay, concrete, or firebrick chimney liners shall be struck flush to provide a straight, smooth, aligned chimney flue.',
                'condition': self.joints_flush_condition or '',
                'comments': self.joints_flush_comments or '',
                'codeCompliance': self.joints_flush_code_compliance,
                'photos': self.joints_flush_photos or []
            },
            'linerInstallation': {
                'id': 'liner-installation',
                'title': 'Installation of Chimney Liners – 9.21.3.7(1)',
                'description': 'Chimney liners shall be installed when the surrounding masonry or concrete is placed.',
                'condition': self.liner_installation_condition or '',
                'comments': self.liner_installation_comments or '',
                'codeCompliance': self.liner_installation_code_compliance,
                'photos': self.liner_installation_photos or []
            },
            'linerSpaces': {
                'id': 'liner-spaces',
                'title': 'Spaces between Liners and Surrounding Masonry – 9.21.3.8(2)',
                'description': 'A space not less than 10 mm (⅜ in.) wide shall be left between a chimney liner and surrounding masonry. This space shall not be filled with mortar.',
                'condition': self.liner_spaces_condition or '',
                'comments': self.liner_spaces_comments or '',
                'codeCompliance': self.liner_spaces_code_compliance,
                'photos': self.liner_spaces_photos or []
            },
            'mortarForLiners': {
                'id': 'mortar-for-liners',
                'title': 'Mortar for Chimney Liners – 9.21.3.9',
                'description': 'Chimney liners used in chimneys for solid-fuel-burning appliances shall be laid in a full bed of:\n\nHigh temperature cement mortar conforming to CAN/CGSB-10.3, Air-Setting Refractory Mortar, or\n\nMortar consisting of 1 part Portland cement to 3 parts sand by volume.\n\nChimney liners used in chimneys for oil- or gas-burning appliances shall be laid in a full bed of mortar consisting of 1 part Portland cement to 3 parts sand by volume.',
                'condition': self.mortar_for_liners_condition or '',
                'comments': self.mortar_for_liners_comments or '',
                'codeCompliance': self.mortar_for_liners_code_compliance,
                'photos': self.mortar_for_liners_photos or []
            },
            'linerExtension': {
                'id': 'liner-extension',
                'title': 'Extension of Chimney Liners – 9.21.3.10',
                'description': 'Chimney liners shall extend from a point not less than 200 mm (8 in.) below the lowest flue pipe connection to a point not less than 50 mm (2 in.) or more than 100 mm (4 in.) above the chimney cap.',
                'condition': self.liner_extension_condition or '',
                'comments': self.liner_extension_comments or '',
                'codeCompliance': self.liner_extension_code_compliance,
                'photos': self.liner_extension_photos or []
            },
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertChimneyHeightClearance(db.Model):
    __tablename__ = 'fireplace_insert_chimney_height_clearance'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Height of Chimney Flues – 9.21.4.4 section
    chimney_flues_height_required_height = db.Column(db.String(255), nullable=True)
    chimney_flues_height_present_height = db.Column(db.String(255), nullable=True)
    chimney_flues_height_required_width = db.Column(db.String(255), nullable=True)
    chimney_flues_height_present_width = db.Column(db.String(255), nullable=True)
    chimney_flues_height_required_vertical = db.Column(db.String(255), nullable=True)
    chimney_flues_height_present_vertical = db.Column(db.String(255), nullable=True)
    chimney_flues_height_condition = db.Column(db.String(255), nullable=True)
    chimney_flues_height_comments = db.Column(db.Text, nullable=True)
    chimney_flues_height_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    chimney_flues_height_photos = db.Column(db.JSON, nullable=True)

    # Lateral Stability – 9.21.4.5 section
    lateral_stability_condition = db.Column(db.String(255), nullable=True)
    lateral_stability_comments = db.Column(db.Text, nullable=True)
    lateral_stability_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    lateral_stability_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps – 9.21.4.6(1) section
    chimney_caps_1_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_1_comments = db.Column(db.Text, nullable=True)
    chimney_caps_1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    chimney_caps_1_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps – 9.21.4.6(2) section
    chimney_caps_2_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_2_comments = db.Column(db.Text, nullable=True)
    chimney_caps_2_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    chimney_caps_2_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps – 9.21.4.6(3) section
    chimney_caps_3_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_3_comments = db.Column(db.Text, nullable=True)
    chimney_caps_3_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    chimney_caps_3_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_chimney_height_clearance', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertChimneyHeightClearance {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'chimneyFluesHeight': {
                'id': 'chimney-flues-height',
                'title': 'Height of Chimney Flues – 9.21.4.4',
                'description': 'A chimney flue shall extend not less than:\n\na) 900 mm (36 in.) above the highest point at which the chimney comes in contact with the roof, and\n\nb) 600 mm (24 in.) above the highest roof surface or structure within 3 m (10 ft) of the chimney.',
                'requiredHeight': self.chimney_flues_height_required_height or '',
                'presentHeight': self.chimney_flues_height_present_height or '',
                'requiredWidth': self.chimney_flues_height_required_width or '',
                'presentWidth': self.chimney_flues_height_present_width or '',
                'requiredVertical': self.chimney_flues_height_required_vertical or '',
                'presentVertical': self.chimney_flues_height_present_vertical or '',
                'condition': self.chimney_flues_height_condition or '',
                'comments': self.chimney_flues_height_comments or '',
                'codeCompliance': self.chimney_flues_height_code_compliance,
                'photos': self.chimney_flues_height_photos or []
            },
            'lateralStability': {
                'id': 'lateral-stability',
                'title': 'Lateral Stability – 9.21.4.5',
                'description': 'Except as provided in Sentence (2), chimneys shall be braced in accordance with Subsection 4.3.2. to provide lateral stability under wind loads.\n\nA chimney need not be laterally braced provided:\n\nno horizontal cross dimension is less than 400 mm (15¾ in.), and\n\nthe chimney extends not more than 3.6 m (12 ft) above the roof or the masonry wall of which it forms a part.',
                'condition': self.lateral_stability_condition or '',
                'comments': self.lateral_stability_comments or '',
                'codeCompliance': self.lateral_stability_code_compliance,
                'photos': self.lateral_stability_photos or []
            },
            'chimneyCaps1': {
                'id': 'chimney-caps-1',
                'title': 'Chimney Caps – 9.21.4.6(1)',
                'description': 'The top of a chimney shall have a waterproof cap of reinforced concrete, masonry, or metal.',
                'condition': self.chimney_caps_1_condition or '',
                'comments': self.chimney_caps_1_comments or '',
                'codeCompliance': self.chimney_caps_1_code_compliance,
                'photos': self.chimney_caps_1_photos or []
            },
            'chimneyCaps2': {
                'id': 'chimney-caps-2',
                'title': 'Chimney Caps – 9.21.4.6(2)',
                'description': 'The cap required in Sentence (1) shall slope from the lining and be provided with a drip not less than 25 mm (1 in.) from the chimney wall.',
                'condition': self.chimney_caps_2_condition or '',
                'comments': self.chimney_caps_2_comments or '',
                'codeCompliance': self.chimney_caps_2_code_compliance,
                'photos': self.chimney_caps_2_photos or []
            },
            'chimneyCaps3': {
                'id': 'chimney-caps-3',
                'title': 'Chimney Caps – 9.21.4.6(3)',
                'description': 'A jointed precast concrete or masonry chimney cap shall have flashing installed beneath the cap, extending from the liner to the drip edge.',
                'condition': self.chimney_caps_3_condition or '',
                'comments': self.chimney_caps_3_comments or '',
                'codeCompliance': self.chimney_caps_3_code_compliance,
                'photos': self.chimney_caps_3_photos or []
            },
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertChimneySupports(db.Model):
    __tablename__ = 'fireplace_insert_chimney_supports'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Flashing – 9.21.4.10 section
    flashing_condition = db.Column(db.String(255), nullable=True)
    flashing_comments = db.Column(db.Text, nullable=True)
    flashing_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    flashing_photos = db.Column(db.JSON, nullable=True)

    # Clearance from Combustible Materials – 9.21.5.1 section
    clearance_combustible_1_condition = db.Column(db.String(255), nullable=True)
    clearance_combustible_1_comments = db.Column(db.Text, nullable=True)
    clearance_combustible_1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearance_combustible_1_photos = db.Column(db.JSON, nullable=True)

    # Clearance from Combustible Materials – 9.21.5.1(3) section
    clearance_combustible_3_condition = db.Column(db.String(255), nullable=True)
    clearance_combustible_3_comments = db.Column(db.Text, nullable=True)
    clearance_combustible_3_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearance_combustible_3_photos = db.Column(db.JSON, nullable=True)

    # Sealing of Spaces – 9.21.5.2 section
    sealing_spaces_condition = db.Column(db.String(255), nullable=True)
    sealing_spaces_comments = db.Column(db.Text, nullable=True)
    sealing_spaces_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    sealing_spaces_photos = db.Column(db.JSON, nullable=True)

    # Support of Joists or Beams – 9.21.5.3 section
    support_joists_beams_condition = db.Column(db.String(255), nullable=True)
    support_joists_beams_comments = db.Column(db.Text, nullable=True)
    support_joists_beams_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    support_joists_beams_photos = db.Column(db.JSON, nullable=True)

    # Intersection of Shingle Roofs and Masonry – 9.26.4.4 section
    roof_masonry_intersection_condition = db.Column(db.String(255), nullable=True)
    roof_masonry_intersection_comments = db.Column(db.Text, nullable=True)
    roof_masonry_intersection_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    roof_masonry_intersection_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_chimney_supports', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertChimneySupports {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'flashing': {
                'id': 'flashing',
                'title': 'Flashing – 9.21.4.10',
                'description': 'Junctions with adjacent materials shall be adequately flashed to shed water.',
                'condition': self.flashing_condition or '',
                'comments': self.flashing_comments or '',
                'codeCompliance': self.flashing_code_compliance,
                'photos': self.flashing_photos or []
            },
            'clearanceCombustible1': {
                'id': 'clearance-combustible-1',
                'title': 'Clearance from Combustible Materials – 9.21.5.1',
                'description': 'The clearance between masonry or concrete chimneys and combustible framing shall be not less than:\n\n50 mm (2") for interior chimneys, and\n\n12 mm (1/2") for exterior chimneys.\n\nNote (A-9.21.5.1(1)): For purposes of this Sentence, an exterior chimney can be considered to be one which has at least one side exposed to the outside. Masonry chimneys located within the insulated envelope of a building, typically in the length of exterior walls, should be considered interior.',
                'condition': self.clearance_combustible_1_condition or '',
                'comments': self.clearance_combustible_1_comments or '',
                'codeCompliance': self.clearance_combustible_1_code_compliance,
                'photos': self.clearance_combustible_1_photos or []
            },
            'clearanceCombustible3': {
                'id': 'clearance-combustible-3',
                'title': 'Clearance from Combustible Materials – 9.21.5.1(3)',
                'description': 'Combustible flooring and subflooring shall have not less than a 12 mm (1/2") clearance from masonry or concrete chimneys.',
                'condition': self.clearance_combustible_3_condition or '',
                'comments': self.clearance_combustible_3_comments or '',
                'codeCompliance': self.clearance_combustible_3_code_compliance,
                'photos': self.clearance_combustible_3_photos or []
            },
            'sealingSpaces': {
                'id': 'sealing-spaces',
                'title': 'Sealing of Spaces – 9.21.5.2',
                'description': 'All spaces between masonry or concrete chimneys and combustible framing shall be sealed top or bottom with noncombustible material.',
                'condition': self.sealing_spaces_condition or '',
                'comments': self.sealing_spaces_comments or '',
                'codeCompliance': self.sealing_spaces_code_compliance,
                'photos': self.sealing_spaces_photos or []
            },
            'supportJoistsBeams': {
                'id': 'support-joists-beams',
                'title': 'Support of Joists or Beams – 9.21.5.3',
                'description': 'Joists or beams may be supported on masonry walls which enclose chimney flues provided the combustible members are separated from the flue not less than 200 mm (8") of solid masonry.',
                'condition': self.support_joists_beams_condition or '',
                'comments': self.support_joists_beams_comments or '',
                'codeCompliance': self.support_joists_beams_code_compliance,
                'photos': self.support_joists_beams_photos or []
            },
            'roofMasonryIntersection': {
                'id': 'roof-masonry-intersection',
                'title': 'Intersection of Shingle Roofs and Masonry – 9.26.4.4',
                'description': 'The intersection of shingle roofs and masonry walls or chimneys shall be protected with flashing.\n\nCounter flashing required in Sentence (1) shall be embedded not less than 25 mm (1") in the masonry and extend not less than 150 mm (6") down the masonry and lap base flashing not less than 100 mm (4").\n\nFlashing along the slope of a roof described in Sentence (1) shall be stepped not less than 75 mm (3") with each step held in the joint between flashing and counter flashing.\n\nWhere the roof described in Sentence (1) slopes downward from the masonry, flashing shall extend up the roof slope to a point equal in height to the flashing on the masonry, but not less than 1.5 times the shingle exposure.',
                'condition': self.roof_masonry_intersection_condition or '',
                'comments': self.roof_masonry_intersection_comments or '',
                'codeCompliance': self.roof_masonry_intersection_code_compliance,
                'photos': self.roof_masonry_intersection_photos or []
            },
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FireplaceInsertChimneySaddlesFireCode(db.Model):
    __tablename__ = 'fireplace_insert_chimney_saddles_fire_code'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Chimney Saddles – 9.26.4.8 section
    chimney_saddles_condition = db.Column(db.String(255), nullable=True)
    chimney_saddles_comments = db.Column(db.Text, nullable=True)
    chimney_saddles_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    chimney_saddles_photos = db.Column(db.JSON, nullable=True)

    # Fire Code – 2.6.1.4 (1) section
    fire_code_inspection_condition = db.Column(db.String(255), nullable=True)
    fire_code_inspection_comments = db.Column(db.Text, nullable=True)
    fire_code_inspection_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    fire_code_inspection_photos = db.Column(db.JSON, nullable=True)

    # Fire Code – 2.6.1.4 (2) section
    fire_code_cleaning_condition = db.Column(db.String(255), nullable=True)
    fire_code_cleaning_comments = db.Column(db.Text, nullable=True)
    fire_code_cleaning_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    fire_code_cleaning_photos = db.Column(db.JSON, nullable=True)

    # Fire Code – 2.6.1.4 (3a) section
    fire_code_structural_deficiency_condition = db.Column(db.String(255), nullable=True)
    fire_code_structural_deficiency_comments = db.Column(db.Text, nullable=True)
    fire_code_structural_deficiency_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    fire_code_structural_deficiency_photos = db.Column(db.JSON, nullable=True)

    # Fire Code – 2.6.1.4 (3b) section
    fire_code_abandoned_openings_condition = db.Column(db.String(255), nullable=True)
    fire_code_abandoned_openings_comments = db.Column(db.Text, nullable=True)
    fire_code_abandoned_openings_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    fire_code_abandoned_openings_photos = db.Column(db.JSON, nullable=True)

    additional_notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('fireplace_insert_chimney_saddles_fire_code', uselist=False))

    def __repr__(self):
        return f'<FireplaceInsertChimneySaddlesFireCode {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'chimneySaddles': {
                'id': 'chimney-saddles',
                'title': 'Chimney Saddles – 9.26.4.8',
                'description': 'Except as otherwise permitted in Sentence (5), chimney saddles shall be installed where the upper side of a chimney on a sloping roof is more than 750 mm (30") wide.\n\nA chimney saddle need not be installed if the intersection between the chimney and roof is protected by sheet metal flashing that:\n\nExtends up the chimney to a height equal to at least one-sixth the width of the chimney (but not less than 150 mm (6")), and\n\nUp the roof slope to a point equal in height to the flashing on the chimney (but not less than 1.5 times the shingle exposure).',
                'condition': self.chimney_saddles_condition or '',
                'comments': self.chimney_saddles_comments or '',
                'codeCompliance': self.chimney_saddles_code_compliance,
                'photos': self.chimney_saddles_photos or []
            },
            'fireCodeInspection': {
                'id': 'fire-code-inspection',
                'title': 'Fire Code – 2.6.1.4 (1)',
                'description': 'Every chimney, flue, and flue pipe shall be inspected to identify any dangerous condition:\na) at intervals not greater than 12 months,\nb) at the time of addition of any appliance, and\nc) after any chimney fire.',
                'condition': self.fire_code_inspection_condition or '',
                'comments': self.fire_code_inspection_comments or '',
                'codeCompliance': self.fire_code_inspection_code_compliance,
                'photos': self.fire_code_inspection_photos or []
            },
            'fireCodeCleaning': {
                'id': 'fire-code-cleaning',
                'title': 'Fire Code – 2.6.1.4 (2)',
                'description': 'Chimneys, flues, and flue pipes shall be cleaned as often as necessary to keep them free from dangerous accumulations of combustible deposits.\n\nAppendix A – A.2.6.1.4 (2):\n\nThe presence in a chimney of soot or creosote in excess of 3 mm thick indicates the need for immediate cleaning.\n\nMay require modification of burning procedures.\n\nCalls for more frequent inspections.',
                'condition': self.fire_code_cleaning_condition or '',
                'comments': self.fire_code_cleaning_comments or '',
                'codeCompliance': self.fire_code_cleaning_code_compliance,
                'photos': self.fire_code_cleaning_photos or []
            },
            'fireCodeStructuralDeficiency': {
                'id': 'fire-code-structural-deficiency',
                'title': 'Fire Code – 2.6.1.4 (3a)',
                'description': 'A chimney, flue, or flue pipe shall be replaced or repaired to eliminate any structural deficiency or decay.\n\nAppendix A – A.2.6.1.4 (3a):\nStructural deficiencies include:\n\nAbsence of a liner or inadequate design of supports/ties.\n\nInstances of decay such as cracking, settling, crumbling mortar, distortion, advanced corrosion, separation of sections, or loose/broken supports.',
                'condition': self.fire_code_structural_deficiency_condition or '',
                'comments': self.fire_code_structural_deficiency_comments or '',
                'codeCompliance': self.fire_code_structural_deficiency_code_compliance,
                'photos': self.fire_code_structural_deficiency_photos or []
            },
            'fireCodeAbandonedOpenings': {
                'id': 'fire-code-abandoned-openings',
                'title': 'Fire Code – 2.6.1.4 (3b)',
                'description': 'A chimney, flue, or flue pipe shall be replaced or repaired to eliminate all abandoned or unused openings that are not effectively sealed in a manner that would prevent the passage of fire or smoke.',
                'condition': self.fire_code_abandoned_openings_condition or '',
                'comments': self.fire_code_abandoned_openings_comments or '',
                'codeCompliance': self.fire_code_abandoned_openings_code_compliance,
                'photos': self.fire_code_abandoned_openings_photos or []
            },
            'additionalNotes': self.additional_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryChimneySpecification(db.Model):
    __tablename__ = 'masonry_chimney_specifications'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Chimney construction details
    chimney_constructed_in_building = db.Column(db.String(20), nullable=True)  # yes/no/unknown
    approximate_age = db.Column(db.String(100), nullable=True)

    # Shell details
    shell = db.Column(db.String(50), nullable=True)  # brick/block/stone/others

    # Rain cap details
    rain_cap = db.Column(db.String(30), nullable=True)  # yes/no/with-screening/without-screening

    # Flue details
    number_of_flues = db.Column(db.String(50), nullable=True)
    size_of_flue = db.Column(db.String(100), nullable=True)
    material_of_flue = db.Column(db.String(100), nullable=True)

    # Location details
    chimney_location = db.Column(db.String(20), nullable=True)  # interior/exterior
    height_from_firebox_floor = db.Column(db.String(50), nullable=True)

    # Lining details
    chimney_lined_with = db.Column(db.String(50), nullable=True)  # clay-tile/pumice/stainless-steel-flex/stainless-steel-rigid/no-liner/insulated/uti

    # Installation details
    chimney_installed_by = db.Column(db.String(200), nullable=True)
    is_unknown_installer = db.Column(db.Boolean, default=False)
    installation_date = db.Column(db.String(50), nullable=True)

    # Assessment details
    comments = db.Column(db.Text, nullable=True)
    suitable = db.Column(db.String(30), nullable=True)  # yes/no

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_chimney_specifications', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'chimneyConstructedInBuilding': self.chimney_constructed_in_building or '',
            'approximateAge': self.approximate_age or '',
            'shell': self.shell or '',
            'rainCap': self.rain_cap or '',
            'numberOfFlues': self.number_of_flues or '',
            'sizeOfFlue': self.size_of_flue or '',
            'materialOfFlue': self.material_of_flue or '',
            'chimneyLocation': self.chimney_location or '',
            'heightFromFireboxFloor': self.height_from_firebox_floor or '',
            'chimneyLinedWith': self.chimney_lined_with or '',
            'chimneyInstalledBy': self.chimney_installed_by or '',
            'isUnknownInstaller': self.is_unknown_installer,
            'date': self.installation_date or '',
            'comments': self.comments or '',
            'suitable': self.suitable or '',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryFireplaceSpecification(db.Model):
    __tablename__ = 'masonry_fireplace_specifications'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Inspection details
    inspection_discussed = db.Column(db.String(10), nullable=True)  # yes/no
    building_permits_available = db.Column(db.String(10), nullable=True)  # yes/no
    time_of_day = db.Column(db.String(20), nullable=True)
    weather_conditions = db.Column(db.Text, nullable=True)
    roofing_type = db.Column(db.String(100), nullable=True)
    roof_accessed = db.Column(db.String(10), nullable=True)  # yes/no
    attic_accessed = db.Column(db.String(10), nullable=True)  # yes/no

    # Fireplace construction details
    fireplace_constructed_in_building = db.Column(db.String(20), nullable=True)  # yes/no/unknown
    approximate_age = db.Column(db.String(100), nullable=True)

    # Fireplace details
    fireplace_location = db.Column(db.String(20), nullable=True)  # interior/exterior
    fireplace_type = db.Column(db.String(30), nullable=True)  # firebrick-lined/steel-lined/steel-liner-assemblies
    certification_standard = db.Column(db.String(30), nullable=True)  # ulc-s639/uncertified
    listing_agency = db.Column(db.String(30), nullable=True)  # ulc/csa/wh-etl
    fireplace_location_in_building = db.Column(db.String(50), nullable=True)  # basement/main-floor/other
    other_location = db.Column(db.String(200), nullable=True)

    # Technical details
    fan_blower_attached = db.Column(db.String(10), nullable=True)  # yes/no
    installed_in = db.Column(db.String(50), nullable=True)  # residence-part-9/modular-home-a277/mobile/home-manufactured-z240/alcove/garage/other

    # Installation details
    fireplace_installed_by = db.Column(db.String(200), nullable=True)
    is_unknown_installer = db.Column(db.Boolean, default=False)
    installation_date = db.Column(db.String(50), nullable=True)

    # Assessment details
    comments = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_fireplace_specifications', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'inspectionDiscussed': self.inspection_discussed or '',
            'buildingPermitsAvailable': self.building_permits_available or '',
            'timeOfDay': self.time_of_day or '',
            'weatherConditions': self.weather_conditions or '',
            'roofingType': self.roofing_type or '',
            'roofAccessed': self.roof_accessed or '',
            'atticAccessed': self.attic_accessed or '',
            'fireplaceConstructedInBuilding': self.fireplace_constructed_in_building or '',
            'approximateAge': self.approximate_age or '',
            'fireplaceLocation': self.fireplace_location or '',
            'fireplaceType': self.fireplace_type or '',
            'certificationStandard': self.certification_standard or '',
            'listingAgency': self.listing_agency or '',
            'fireplaceLocation2': self.fireplace_location_in_building or '',
            'otherLocation': self.other_location or '',
            'fanBlowerAttached': self.fan_blower_attached or '',
            'installedIn': self.installed_in or '',
            'fireplaceInstalledBy': self.fireplace_installed_by or '',
            'isUnknownInstaller': self.is_unknown_installer,
            'date': self.installation_date or '',
            'comments': self.comments or '',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryFireplaceConstructionDetails(db.Model):
    __tablename__ = 'masonry_fireplace_construction_details'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Measurements
    height = db.Column(db.String(50), nullable=True)
    width = db.Column(db.String(50), nullable=True)
    total = db.Column(db.String(50), nullable=True)

    # Fireplace Chimneys section
    fireplace_chimneys_condition = db.Column(db.String(255), nullable=True)
    fireplace_chimneys_comments = db.Column(db.Text, nullable=True)
    fireplace_chimneys_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    fireplace_chimneys_photos = db.Column(db.JSON, nullable=True)

    # Lintels Arches section
    lintels_arches_condition = db.Column(db.String(255), nullable=True)
    lintels_arches_comments = db.Column(db.Text, nullable=True)
    lintels_arches_code_compliance = db.Column(db.String(10), nullable=True)
    lintels_arches_photos = db.Column(db.JSON, nullable=True)

    # OBC Lintels Arches section
    obc_lintels_arches_condition = db.Column(db.String(255), nullable=True)
    obc_lintels_arches_comments = db.Column(db.Text, nullable=True)
    obc_lintels_arches_code_compliance = db.Column(db.String(10), nullable=True)
    obc_lintels_arches_photos = db.Column(db.JSON, nullable=True)

    # Corbelling section
    corbelling_condition = db.Column(db.String(255), nullable=True)
    corbelling_comments = db.Column(db.Text, nullable=True)
    corbelling_code_compliance = db.Column(db.String(10), nullable=True)
    corbelling_photos = db.Column(db.JSON, nullable=True)

    # Combustion Air section
    combustion_air_condition = db.Column(db.String(255), nullable=True)
    combustion_air_comments = db.Column(db.Text, nullable=True)
    combustion_air_code_compliance = db.Column(db.String(10), nullable=True)
    combustion_air_photos = db.Column(db.JSON, nullable=True)

    # NBC Combustion Air section
    nbc_combustion_air_condition = db.Column(db.String(255), nullable=True)
    nbc_combustion_air_comments = db.Column(db.Text, nullable=True)
    nbc_combustion_air_code_compliance = db.Column(db.String(10), nullable=True)
    nbc_combustion_air_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_fireplace_construction_details', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'height': self.height or '',
            'width': self.width or '',
            'total': self.total or '',
            'formData': {
                'fireplaceChimneys': {
                    'condition': self.fireplace_chimneys_condition or '',
                    'comments': self.fireplace_chimneys_comments or '',
                    'codeCompliance': self.fireplace_chimneys_code_compliance or '',
                    'photos': self.fireplace_chimneys_photos or []
                },
                'lintelsArches': {
                    'condition': self.lintels_arches_condition or '',
                    'comments': self.lintels_arches_comments or '',
                    'codeCompliance': self.lintels_arches_code_compliance or '',
                    'photos': self.lintels_arches_photos or []
                },
                'obcLintelsArches': {
                    'condition': self.obc_lintels_arches_condition or '',
                    'comments': self.obc_lintels_arches_comments or '',
                    'codeCompliance': self.obc_lintels_arches_code_compliance or '',
                    'photos': self.obc_lintels_arches_photos or []
                },
                'corbelling': {
                    'condition': self.corbelling_condition or '',
                    'comments': self.corbelling_comments or '',
                    'codeCompliance': self.corbelling_code_compliance or '',
                    'photos': self.corbelling_photos or []
                },
                'combustionAir': {
                    'condition': self.combustion_air_condition or '',
                    'comments': self.combustion_air_comments or '',
                    'codeCompliance': self.combustion_air_code_compliance or '',
                    'photos': self.combustion_air_photos or []
                },
                'nbcCombustionAir': {
                    'condition': self.nbc_combustion_air_condition or '',
                    'comments': self.nbc_combustion_air_comments or '',
                    'codeCompliance': self.nbc_combustion_air_code_compliance or '',
                    'photos': self.nbc_combustion_air_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryCombustionAirRequirements(db.Model):
    __tablename__ = 'masonry_combustion_air_requirements'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # OBC Combustion Air section
    obc_combustion_air_condition = db.Column(db.String(255), nullable=True)
    obc_combustion_air_comments = db.Column(db.Text, nullable=True)
    obc_combustion_air_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    obc_combustion_air_photos = db.Column(db.JSON, nullable=True)

    # Brick or Steel Liners section
    brick_steel_liners_condition = db.Column(db.String(255), nullable=True)
    brick_steel_liners_comments = db.Column(db.Text, nullable=True)
    brick_steel_liners_code_compliance = db.Column(db.String(10), nullable=True)
    brick_steel_liners_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners 1 section
    firebrick_liners_1_condition = db.Column(db.String(255), nullable=True)
    firebrick_liners_1_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_1_code_compliance = db.Column(db.String(10), nullable=True)
    firebrick_liners_1_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners 2 section
    firebrick_liners_2_condition = db.Column(db.String(255), nullable=True)
    firebrick_liners_2_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_2_code_compliance = db.Column(db.String(10), nullable=True)
    firebrick_liners_2_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners 3 section
    firebrick_liners_3_condition = db.Column(db.String(255), nullable=True)
    firebrick_liners_3_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_3_code_compliance = db.Column(db.String(10), nullable=True)
    firebrick_liners_3_photos = db.Column(db.JSON, nullable=True)

    # Steel Liners section
    steel_liners_condition = db.Column(db.String(255), nullable=True)
    steel_liners_comments = db.Column(db.Text, nullable=True)
    steel_liners_code_compliance = db.Column(db.String(10), nullable=True)
    steel_liners_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_combustion_air_requirements', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'obcCombustionAir': {
                    'condition': self.obc_combustion_air_condition or '',
                    'comments': self.obc_combustion_air_comments or '',
                    'codeCompliance': self.obc_combustion_air_code_compliance or '',
                    'photos': self.obc_combustion_air_photos or []
                },
                'brickSteelLiners': {
                    'condition': self.brick_steel_liners_condition or '',
                    'comments': self.brick_steel_liners_comments or '',
                    'codeCompliance': self.brick_steel_liners_code_compliance or '',
                    'photos': self.brick_steel_liners_photos or []
                },
                'firebrickLiners1': {
                    'condition': self.firebrick_liners_1_condition or '',
                    'comments': self.firebrick_liners_1_comments or '',
                    'codeCompliance': self.firebrick_liners_1_code_compliance or '',
                    'photos': self.firebrick_liners_1_photos or []
                },
                'firebrickLiners2': {
                    'condition': self.firebrick_liners_2_condition or '',
                    'comments': self.firebrick_liners_2_comments or '',
                    'codeCompliance': self.firebrick_liners_2_code_compliance or '',
                    'photos': self.firebrick_liners_2_photos or []
                },
                'firebrickLiners3': {
                    'condition': self.firebrick_liners_3_condition or '',
                    'comments': self.firebrick_liners_3_comments or '',
                    'codeCompliance': self.firebrick_liners_3_code_compliance or '',
                    'photos': self.firebrick_liners_3_photos or []
                },
                'steelLiners': {
                    'condition': self.steel_liners_condition or '',
                    'comments': self.steel_liners_comments or '',
                    'codeCompliance': self.steel_liners_code_compliance or '',
                    'photos': self.steel_liners_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryChimneyStructure(db.Model):
    __tablename__ = 'masonry_chimney_structure'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Thickness of Walls 1 section
    thickness_walls_1_condition = db.Column(db.String(255), nullable=True)
    thickness_walls_1_comments = db.Column(db.Text, nullable=True)
    thickness_walls_1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    thickness_walls_1_photos = db.Column(db.JSON, nullable=True)

    # Thickness of Walls 2 section
    thickness_walls_2_condition = db.Column(db.String(255), nullable=True)
    thickness_walls_2_comments = db.Column(db.Text, nullable=True)
    thickness_walls_2_code_compliance = db.Column(db.String(10), nullable=True)
    thickness_walls_2_photos = db.Column(db.JSON, nullable=True)

    # Fire Chamber Dimensions section
    fire_chamber_dimensions_condition = db.Column(db.String(255), nullable=True)
    fire_chamber_dimensions_comments = db.Column(db.Text, nullable=True)
    fire_chamber_dimensions_code_compliance = db.Column(db.String(10), nullable=True)
    fire_chamber_dimensions_photos = db.Column(db.JSON, nullable=True)

    # Hearth Extension 1 section
    hearth_extension_1_condition = db.Column(db.String(255), nullable=True)
    hearth_extension_1_comments = db.Column(db.Text, nullable=True)
    hearth_extension_1_code_compliance = db.Column(db.String(10), nullable=True)
    hearth_extension_1_photos = db.Column(db.JSON, nullable=True)

    # Hearth Extension 2 section
    hearth_extension_2_condition = db.Column(db.String(255), nullable=True)
    hearth_extension_2_comments = db.Column(db.Text, nullable=True)
    hearth_extension_2_code_compliance = db.Column(db.String(10), nullable=True)
    hearth_extension_2_photos = db.Column(db.JSON, nullable=True)

    # Support of Hearth section
    support_of_hearth_condition = db.Column(db.String(255), nullable=True)
    support_of_hearth_comments = db.Column(db.Text, nullable=True)
    support_of_hearth_code_compliance = db.Column(db.String(10), nullable=True)
    support_of_hearth_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_chimney_structure', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'thicknessWalls1': {
                    'condition': self.thickness_walls_1_condition or '',
                    'comments': self.thickness_walls_1_comments or '',
                    'codeCompliance': self.thickness_walls_1_code_compliance or '',
                    'photos': self.thickness_walls_1_photos or []
                },
                'thicknessWalls2': {
                    'condition': self.thickness_walls_2_condition or '',
                    'comments': self.thickness_walls_2_comments or '',
                    'codeCompliance': self.thickness_walls_2_code_compliance or '',
                    'photos': self.thickness_walls_2_photos or []
                },
                'fireChamberDimensions': {
                    'condition': self.fire_chamber_dimensions_condition or '',
                    'comments': self.fire_chamber_dimensions_comments or '',
                    'codeCompliance': self.fire_chamber_dimensions_code_compliance or '',
                    'photos': self.fire_chamber_dimensions_photos or []
                },
                'hearthExtension1': {
                    'condition': self.hearth_extension_1_condition or '',
                    'comments': self.hearth_extension_1_comments or '',
                    'codeCompliance': self.hearth_extension_1_code_compliance or '',
                    'photos': self.hearth_extension_1_photos or []
                },
                'hearthExtension2': {
                    'condition': self.hearth_extension_2_condition or '',
                    'comments': self.hearth_extension_2_comments or '',
                    'codeCompliance': self.hearth_extension_2_code_compliance or '',
                    'photos': self.hearth_extension_2_photos or []
                },
                'supportOfHearth': {
                    'condition': self.support_of_hearth_condition or '',
                    'comments': self.support_of_hearth_comments or '',
                    'codeCompliance': self.support_of_hearth_code_compliance or '',
                    'photos': self.support_of_hearth_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryHearthConstruction(db.Model):
    __tablename__ = 'masonry_hearth_construction'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Support of Hearth section
    support_of_hearth_condition = db.Column(db.String(255), nullable=True)
    support_of_hearth_comments = db.Column(db.Text, nullable=True)
    support_of_hearth_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    support_of_hearth_photos = db.Column(db.JSON, nullable=True)

    # Required Damper Size section
    required_damper_size_condition = db.Column(db.String(255), nullable=True)
    required_damper_size_comments = db.Column(db.Text, nullable=True)
    required_damper_size_code_compliance = db.Column(db.String(10), nullable=True)
    required_damper_size_photos = db.Column(db.JSON, nullable=True)

    # Slope of Smoke Chamber section
    slope_of_smoke_chamber_condition = db.Column(db.String(255), nullable=True)
    slope_of_smoke_chamber_comments = db.Column(db.Text, nullable=True)
    slope_of_smoke_chamber_code_compliance = db.Column(db.String(10), nullable=True)
    slope_of_smoke_chamber_photos = db.Column(db.JSON, nullable=True)

    # Wall Thickness section
    wall_thickness_condition = db.Column(db.String(255), nullable=True)
    wall_thickness_comments = db.Column(db.Text, nullable=True)
    wall_thickness_code_compliance = db.Column(db.String(10), nullable=True)
    wall_thickness_photos = db.Column(db.JSON, nullable=True)

    # Clearance to Fireplace Opening section
    clearance_to_fireplace_opening_condition = db.Column(db.String(255), nullable=True)
    clearance_to_fireplace_opening_comments = db.Column(db.Text, nullable=True)
    clearance_to_fireplace_opening_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_to_fireplace_opening_photos = db.Column(db.JSON, nullable=True)

    # Metal Exposed to the Interior section
    metal_exposed_to_interior_condition = db.Column(db.String(255), nullable=True)
    metal_exposed_to_interior_comments = db.Column(db.Text, nullable=True)
    metal_exposed_to_interior_code_compliance = db.Column(db.String(10), nullable=True)
    metal_exposed_to_interior_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_hearth_construction', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'supportOfHearth': {
                    'condition': self.support_of_hearth_condition or '',
                    'comments': self.support_of_hearth_comments or '',
                    'codeCompliance': self.support_of_hearth_code_compliance or '',
                    'photos': self.support_of_hearth_photos or []
                },
                'requiredDamperSize': {
                    'condition': self.required_damper_size_condition or '',
                    'comments': self.required_damper_size_comments or '',
                    'codeCompliance': self.required_damper_size_code_compliance or '',
                    'photos': self.required_damper_size_photos or []
                },
                'slopeOfSmokeChamber': {
                    'condition': self.slope_of_smoke_chamber_condition or '',
                    'comments': self.slope_of_smoke_chamber_comments or '',
                    'codeCompliance': self.slope_of_smoke_chamber_code_compliance or '',
                    'photos': self.slope_of_smoke_chamber_photos or []
                },
                'wallThickness': {
                    'condition': self.wall_thickness_condition or '',
                    'comments': self.wall_thickness_comments or '',
                    'codeCompliance': self.wall_thickness_code_compliance or '',
                    'photos': self.wall_thickness_photos or []
                },
                'clearanceToFireplaceOpening': {
                    'condition': self.clearance_to_fireplace_opening_condition or '',
                    'comments': self.clearance_to_fireplace_opening_comments or '',
                    'codeCompliance': self.clearance_to_fireplace_opening_code_compliance or '',
                    'photos': self.clearance_to_fireplace_opening_photos or []
                },
                'metalExposedToInterior': {
                    'condition': self.metal_exposed_to_interior_condition or '',
                    'comments': self.metal_exposed_to_interior_comments or '',
                    'codeCompliance': self.metal_exposed_to_interior_code_compliance or '',
                    'photos': self.metal_exposed_to_interior_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryFireplaceComponents(db.Model):
    __tablename__ = 'masonry_fireplace_components'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # OBC Wall Thickness section
    obc_wall_thickness_condition = db.Column(db.String(255), nullable=True)
    obc_wall_thickness_comments = db.Column(db.Text, nullable=True)
    obc_wall_thickness_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    obc_wall_thickness_photos = db.Column(db.JSON, nullable=True)

    # Lining Materials section
    lining_materials_condition = db.Column(db.String(255), nullable=True)
    lining_materials_comments = db.Column(db.Text, nullable=True)
    lining_materials_code_compliance = db.Column(db.String(10), nullable=True)
    lining_materials_photos = db.Column(db.JSON, nullable=True)

    # Clay Liners section
    clay_liners_condition = db.Column(db.String(255), nullable=True)
    clay_liners_comments = db.Column(db.Text, nullable=True)
    clay_liners_code_compliance = db.Column(db.String(10), nullable=True)
    clay_liners_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners section
    firebrick_liners_condition = db.Column(db.String(255), nullable=True)
    firebrick_liners_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_code_compliance = db.Column(db.String(10), nullable=True)
    firebrick_liners_photos = db.Column(db.JSON, nullable=True)

    # Concrete Liners section
    concrete_liners_condition = db.Column(db.String(255), nullable=True)
    concrete_liners_comments = db.Column(db.Text, nullable=True)
    concrete_liners_code_compliance = db.Column(db.String(10), nullable=True)
    concrete_liners_photos = db.Column(db.JSON, nullable=True)

    # Clearance from Combustible Materials section
    clearance_from_combustible_materials_condition = db.Column(db.String(255), nullable=True)
    clearance_from_combustible_materials_comments = db.Column(db.Text, nullable=True)
    clearance_from_combustible_materials_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_from_combustible_materials_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_fireplace_components', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'obcWallThickness': {
                    'condition': self.obc_wall_thickness_condition or '',
                    'comments': self.obc_wall_thickness_comments or '',
                    'codeCompliance': self.obc_wall_thickness_code_compliance or '',
                    'photos': self.obc_wall_thickness_photos or []
                },
                'liningMaterials': {
                    'condition': self.lining_materials_condition or '',
                    'comments': self.lining_materials_comments or '',
                    'codeCompliance': self.lining_materials_code_compliance or '',
                    'photos': self.lining_materials_photos or []
                },
                'clayLiners': {
                    'condition': self.clay_liners_condition or '',
                    'comments': self.clay_liners_comments or '',
                    'codeCompliance': self.clay_liners_code_compliance or '',
                    'photos': self.clay_liners_photos or []
                },
                'firebrickLiners': {
                    'condition': self.firebrick_liners_condition or '',
                    'comments': self.firebrick_liners_comments or '',
                    'codeCompliance': self.firebrick_liners_code_compliance or '',
                    'photos': self.firebrick_liners_photos or []
                },
                'concreteLiners': {
                    'condition': self.concrete_liners_condition or '',
                    'comments': self.concrete_liners_comments or '',
                    'codeCompliance': self.concrete_liners_code_compliance or '',
                    'photos': self.concrete_liners_photos or []
                },
                'clearanceFromCombustibleMaterials': {
                    'condition': self.clearance_from_combustible_materials_condition or '',
                    'comments': self.clearance_from_combustible_materials_comments or '',
                    'codeCompliance': self.clearance_from_combustible_materials_code_compliance or '',
                    'photos': self.clearance_from_combustible_materials_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryFireplaceClearances(db.Model):
    __tablename__ = 'masonry_fireplace_clearances'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Clearance to Combustible Framing 1 section
    clearance_to_combustible_framing_1_condition = db.Column(db.String(255), nullable=True)
    clearance_to_combustible_framing_1_comments = db.Column(db.Text, nullable=True)
    clearance_to_combustible_framing_1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearance_to_combustible_framing_1_photos = db.Column(db.JSON, nullable=True)

    # Clearance to Combustible Framing 2 section
    clearance_to_combustible_framing_2_condition = db.Column(db.String(255), nullable=True)
    clearance_to_combustible_framing_2_comments = db.Column(db.Text, nullable=True)
    clearance_to_combustible_framing_2_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_to_combustible_framing_2_photos = db.Column(db.JSON, nullable=True)

    # Heat-Circulating Duct Outlets section
    heat_circulating_duct_outlets_condition = db.Column(db.String(255), nullable=True)
    heat_circulating_duct_outlets_comments = db.Column(db.Text, nullable=True)
    heat_circulating_duct_outlets_code_compliance = db.Column(db.String(10), nullable=True)
    heat_circulating_duct_outlets_photos = db.Column(db.JSON, nullable=True)

    # Cleanout section
    cleanout_condition = db.Column(db.String(255), nullable=True)
    cleanout_comments = db.Column(db.Text, nullable=True)
    cleanout_code_compliance = db.Column(db.String(10), nullable=True)
    cleanout_photos = db.Column(db.JSON, nullable=True)

    # Clearance from Combustible Materials section
    clearance_from_combustible_materials_condition = db.Column(db.String(255), nullable=True)
    clearance_from_combustible_materials_comments = db.Column(db.Text, nullable=True)
    clearance_from_combustible_materials_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_from_combustible_materials_photos = db.Column(db.JSON, nullable=True)

    # ABC/BCBC/NBC Wall Thickness section
    abc_bcbc_nbc_wall_thickness_condition = db.Column(db.String(255), nullable=True)
    abc_bcbc_nbc_wall_thickness_comments = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_wall_thickness_code_compliance = db.Column(db.String(10), nullable=True)
    abc_bcbc_nbc_wall_thickness_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_fireplace_clearances', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'clearanceToCombustibleFraming1': {
                    'condition': self.clearance_to_combustible_framing_1_condition or '',
                    'comments': self.clearance_to_combustible_framing_1_comments or '',
                    'codeCompliance': self.clearance_to_combustible_framing_1_code_compliance or '',
                    'photos': self.clearance_to_combustible_framing_1_photos or []
                },
                'clearanceToCombustibleFraming2': {
                    'condition': self.clearance_to_combustible_framing_2_condition or '',
                    'comments': self.clearance_to_combustible_framing_2_comments or '',
                    'codeCompliance': self.clearance_to_combustible_framing_2_code_compliance or '',
                    'photos': self.clearance_to_combustible_framing_2_photos or []
                },
                'heatCirculatingDuctOutlets': {
                    'condition': self.heat_circulating_duct_outlets_condition or '',
                    'comments': self.heat_circulating_duct_outlets_comments or '',
                    'codeCompliance': self.heat_circulating_duct_outlets_code_compliance or '',
                    'photos': self.heat_circulating_duct_outlets_photos or []
                },
                'cleanout': {
                    'condition': self.cleanout_condition or '',
                    'comments': self.cleanout_comments or '',
                    'codeCompliance': self.cleanout_code_compliance or '',
                    'photos': self.cleanout_photos or []
                },
                'clearanceFromCombustibleMaterials': {
                    'condition': self.clearance_from_combustible_materials_condition or '',
                    'comments': self.clearance_from_combustible_materials_comments or '',
                    'codeCompliance': self.clearance_from_combustible_materials_code_compliance or '',
                    'photos': self.clearance_from_combustible_materials_photos or []
                },
                'abcBcbcNbcWallThickness': {
                    'condition': self.abc_bcbc_nbc_wall_thickness_condition or '',
                    'comments': self.abc_bcbc_nbc_wall_thickness_comments or '',
                    'codeCompliance': self.abc_bcbc_nbc_wall_thickness_code_compliance or '',
                    'photos': self.abc_bcbc_nbc_wall_thickness_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryChimneyLinersInstallation(db.Model):
    __tablename__ = 'masonry_chimney_liners_installation'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # OBC Chimney Flue Pipe Walls section
    obc_chimney_flue_pipe_walls_condition = db.Column(db.String(255), nullable=True)
    obc_chimney_flue_pipe_walls_comments = db.Column(db.Text, nullable=True)
    obc_chimney_flue_pipe_walls_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    obc_chimney_flue_pipe_walls_photos = db.Column(db.JSON, nullable=True)

    # ABC/BCBC/NBC Chimney Flue Pipe Walls section
    abc_bcbc_nbc_chimney_flue_pipe_walls_condition = db.Column(db.String(255), nullable=True)
    abc_bcbc_nbc_chimney_flue_pipe_walls_comments = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_chimney_flue_pipe_walls_code_compliance = db.Column(db.String(10), nullable=True)
    abc_bcbc_nbc_chimney_flue_pipe_walls_photos = db.Column(db.JSON, nullable=True)

    # Oval Chimney Flues section
    oval_chimney_flues_condition = db.Column(db.String(255), nullable=True)
    oval_chimney_flues_comments = db.Column(db.Text, nullable=True)
    oval_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)
    oval_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    # ABC/BCBC/NBC Separation of Flue Liners section
    abc_bcbc_nbc_separation_of_flue_liners_condition = db.Column(db.String(255), nullable=True)
    abc_bcbc_nbc_separation_of_flue_liners_comments = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_separation_of_flue_liners_code_compliance = db.Column(db.String(10), nullable=True)
    abc_bcbc_nbc_separation_of_flue_liners_photos = db.Column(db.JSON, nullable=True)

    # OBC Separation of Flue Liners section
    obc_separation_of_flue_liners_condition = db.Column(db.String(255), nullable=True)
    obc_separation_of_flue_liners_comments = db.Column(db.Text, nullable=True)
    obc_separation_of_flue_liners_code_compliance = db.Column(db.String(10), nullable=True)
    obc_separation_of_flue_liners_photos = db.Column(db.JSON, nullable=True)

    # Joints in Chimney Liners section
    joints_in_chimney_liners_condition = db.Column(db.String(255), nullable=True)
    joints_in_chimney_liners_comments = db.Column(db.Text, nullable=True)
    joints_in_chimney_liners_code_compliance = db.Column(db.String(10), nullable=True)
    joints_in_chimney_liners_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_chimney_liners_installation', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'obcChimneyFluePipeWalls': {
                    'condition': self.obc_chimney_flue_pipe_walls_condition or '',
                    'comments': self.obc_chimney_flue_pipe_walls_comments or '',
                    'codeCompliance': self.obc_chimney_flue_pipe_walls_code_compliance or '',
                    'photos': self.obc_chimney_flue_pipe_walls_photos or []
                },
                'abcBcbcNbcChimneyFluePipeWalls': {
                    'condition': self.abc_bcbc_nbc_chimney_flue_pipe_walls_condition or '',
                    'comments': self.abc_bcbc_nbc_chimney_flue_pipe_walls_comments or '',
                    'codeCompliance': self.abc_bcbc_nbc_chimney_flue_pipe_walls_code_compliance or '',
                    'photos': self.abc_bcbc_nbc_chimney_flue_pipe_walls_photos or []
                },
                'ovalChimneyFlues': {
                    'condition': self.oval_chimney_flues_condition or '',
                    'comments': self.oval_chimney_flues_comments or '',
                    'codeCompliance': self.oval_chimney_flues_code_compliance or '',
                    'photos': self.oval_chimney_flues_photos or []
                },
                'abcBcbcNbcSeparationOfFlueLiners': {
                    'condition': self.abc_bcbc_nbc_separation_of_flue_liners_condition or '',
                    'comments': self.abc_bcbc_nbc_separation_of_flue_liners_comments or '',
                    'codeCompliance': self.abc_bcbc_nbc_separation_of_flue_liners_code_compliance or '',
                    'photos': self.abc_bcbc_nbc_separation_of_flue_liners_photos or []
                },
                'obcSeparationOfFlueLiners': {
                    'condition': self.obc_separation_of_flue_liners_condition or '',
                    'comments': self.obc_separation_of_flue_liners_comments or '',
                    'codeCompliance': self.obc_separation_of_flue_liners_code_compliance or '',
                    'photos': self.obc_separation_of_flue_liners_photos or []
                },
                'jointsInChimneyLiners': {
                    'condition': self.joints_in_chimney_liners_condition or '',
                    'comments': self.joints_in_chimney_liners_comments or '',
                    'codeCompliance': self.joints_in_chimney_liners_code_compliance or '',
                    'photos': self.joints_in_chimney_liners_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class WoodStoveMasonryChimneyConstructionLiners(db.Model):
    __tablename__ = 'wood_stove_masonry_chimney_construction_liners'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # ABC/BCBC/NBC Separation of Flue Liners section
    abc_bcbc_nbc_separation_flue_liners_condition = db.Column(db.String(255), nullable=True)
    abc_bcbc_nbc_separation_flue_liners_comments = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_separation_flue_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    abc_bcbc_nbc_separation_flue_liners_photos = db.Column(db.JSON, nullable=True)

    # OBC Separation of Flue Liners section
    obc_separation_flue_liners_condition = db.Column(db.String(255), nullable=True)
    obc_separation_flue_liners_comments = db.Column(db.Text, nullable=True)
    obc_separation_flue_liners_code_compliance = db.Column(db.String(10), nullable=True)
    obc_separation_flue_liners_photos = db.Column(db.JSON, nullable=True)

    # Joints in Chimney Liners 1 section
    joints_in_chimney_liners_1_condition = db.Column(db.String(255), nullable=True)
    joints_in_chimney_liners_1_comments = db.Column(db.Text, nullable=True)
    joints_in_chimney_liners_1_code_compliance = db.Column(db.String(10), nullable=True)
    joints_in_chimney_liners_1_photos = db.Column(db.JSON, nullable=True)

    # Joints in Chimney Liners 2 section
    joints_in_chimney_liners_2_condition = db.Column(db.String(255), nullable=True)
    joints_in_chimney_liners_2_comments = db.Column(db.Text, nullable=True)
    joints_in_chimney_liners_2_code_compliance = db.Column(db.String(10), nullable=True)
    joints_in_chimney_liners_2_photos = db.Column(db.JSON, nullable=True)

    # Installation of Chimney Liners section
    installation_of_chimney_liners_condition = db.Column(db.String(255), nullable=True)
    installation_of_chimney_liners_comments = db.Column(db.Text, nullable=True)
    installation_of_chimney_liners_code_compliance = db.Column(db.String(10), nullable=True)
    installation_of_chimney_liners_photos = db.Column(db.JSON, nullable=True)

    # Spaces between Liners and Surrounding Masonry section
    spaces_between_liners_surrounding_masonry_condition = db.Column(db.String(255), nullable=True)
    spaces_between_liners_surrounding_masonry_comments = db.Column(db.Text, nullable=True)
    spaces_between_liners_surrounding_masonry_code_compliance = db.Column(db.String(10), nullable=True)
    spaces_between_liners_surrounding_masonry_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_chimney_construction_liners', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'abcBcbcNbcSeparationFlueLiners': {
                    'condition': self.abc_bcbc_nbc_separation_flue_liners_condition or '',
                    'comments': self.abc_bcbc_nbc_separation_flue_liners_comments or '',
                    'codeCompliance': self.abc_bcbc_nbc_separation_flue_liners_code_compliance or '',
                    'photos': self.abc_bcbc_nbc_separation_flue_liners_photos or []
                },
                'obcSeparationFlueLiners': {
                    'condition': self.obc_separation_flue_liners_condition or '',
                    'comments': self.obc_separation_flue_liners_comments or '',
                    'codeCompliance': self.obc_separation_flue_liners_code_compliance or '',
                    'photos': self.obc_separation_flue_liners_photos or []
                },
                'jointsInChimneyLiners1': {
                    'condition': self.joints_in_chimney_liners_1_condition or '',
                    'comments': self.joints_in_chimney_liners_1_comments or '',
                    'codeCompliance': self.joints_in_chimney_liners_1_code_compliance or '',
                    'photos': self.joints_in_chimney_liners_1_photos or []
                },
                'jointsInChimneyLiners2': {
                    'condition': self.joints_in_chimney_liners_2_condition or '',
                    'comments': self.joints_in_chimney_liners_2_comments or '',
                    'codeCompliance': self.joints_in_chimney_liners_2_code_compliance or '',
                    'photos': self.joints_in_chimney_liners_2_photos or []
                },
                'installationOfChimneyLiners': {
                    'condition': self.installation_of_chimney_liners_condition or '',
                    'comments': self.installation_of_chimney_liners_comments or '',
                    'codeCompliance': self.installation_of_chimney_liners_code_compliance or '',
                    'photos': self.installation_of_chimney_liners_photos or []
                },
                'spacesBetweenLinersSurroundingMasonry': {
                    'condition': self.spaces_between_liners_surrounding_masonry_condition or '',
                    'comments': self.spaces_between_liners_surrounding_masonry_comments or '',
                    'codeCompliance': self.spaces_between_liners_surrounding_masonry_code_compliance or '',
                    'photos': self.spaces_between_liners_surrounding_masonry_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class WoodStoveMasonryChimneyConstruction(db.Model):
    __tablename__ = 'wood_stove_masonry_chimney_construction'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Footings section
    footings_condition = db.Column(db.String(255), nullable=True)
    footings_comments = db.Column(db.Text, nullable=True)
    footings_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    footings_photos = db.Column(db.JSON, nullable=True)

    # Cleanout section
    cleanout_condition = db.Column(db.String(255), nullable=True)
    cleanout_comments = db.Column(db.Text, nullable=True)
    cleanout_code_compliance = db.Column(db.String(10), nullable=True)
    cleanout_photos = db.Column(db.JSON, nullable=True)

    # Clearance from Combustible Materials section
    clearance_from_combustible_materials_condition = db.Column(db.String(255), nullable=True)
    clearance_from_combustible_materials_comments = db.Column(db.Text, nullable=True)
    clearance_from_combustible_materials_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_from_combustible_materials_photos = db.Column(db.JSON, nullable=True)

    # ABC/BCBC/NBC Wall Thickness section
    abc_bcbc_nbc_wall_thickness_condition = db.Column(db.String(255), nullable=True)
    abc_bcbc_nbc_wall_thickness_comments = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_wall_thickness_code_compliance = db.Column(db.String(10), nullable=True)
    abc_bcbc_nbc_wall_thickness_photos = db.Column(db.JSON, nullable=True)

    # OBC Wall Thickness section
    obc_wall_thickness_condition = db.Column(db.String(255), nullable=True)
    obc_wall_thickness_comments = db.Column(db.Text, nullable=True)
    obc_wall_thickness_code_compliance = db.Column(db.String(10), nullable=True)
    obc_wall_thickness_photos = db.Column(db.JSON, nullable=True)

    # Lining Materials section
    lining_materials_condition = db.Column(db.String(255), nullable=True)
    lining_materials_comments = db.Column(db.Text, nullable=True)
    lining_materials_code_compliance = db.Column(db.String(10), nullable=True)
    lining_materials_photos = db.Column(db.JSON, nullable=True)

    # Clay Liners section
    clay_liners_condition = db.Column(db.String(255), nullable=True)
    clay_liners_comments = db.Column(db.Text, nullable=True)
    clay_liners_code_compliance = db.Column(db.String(10), nullable=True)
    clay_liners_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners section
    firebrick_liners_condition = db.Column(db.String(255), nullable=True)
    firebrick_liners_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_code_compliance = db.Column(db.String(10), nullable=True)
    firebrick_liners_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_chimney_construction', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'footings': {
                    'condition': self.footings_condition or '',
                    'comments': self.footings_comments or '',
                    'codeCompliance': self.footings_code_compliance or '',
                    'photos': self.footings_photos or []
                },
                'cleanout': {
                    'condition': self.cleanout_condition or '',
                    'comments': self.cleanout_comments or '',
                    'codeCompliance': self.cleanout_code_compliance or '',
                    'photos': self.cleanout_photos or []
                },
                'clearanceFromCombustibleMaterials': {
                    'condition': self.clearance_from_combustible_materials_condition or '',
                    'comments': self.clearance_from_combustible_materials_comments or '',
                    'codeCompliance': self.clearance_from_combustible_materials_code_compliance or '',
                    'photos': self.clearance_from_combustible_materials_photos or []
                },
                'abcBcbcNbcWallThickness': {
                    'condition': self.abc_bcbc_nbc_wall_thickness_condition or '',
                    'comments': self.abc_bcbc_nbc_wall_thickness_comments or '',
                    'codeCompliance': self.abc_bcbc_nbc_wall_thickness_code_compliance or '',
                    'photos': self.abc_bcbc_nbc_wall_thickness_photos or []
                },
                'obcWallThickness': {
                    'condition': self.obc_wall_thickness_condition or '',
                    'comments': self.obc_wall_thickness_comments or '',
                    'codeCompliance': self.obc_wall_thickness_code_compliance or '',
                    'photos': self.obc_wall_thickness_photos or []
                },
                'liningMaterials': {
                    'condition': self.lining_materials_condition or '',
                    'comments': self.lining_materials_comments or '',
                    'codeCompliance': self.lining_materials_code_compliance or '',
                    'photos': self.lining_materials_photos or []
                },
                'clayLiners': {
                    'condition': self.clay_liners_condition or '',
                    'comments': self.clay_liners_comments or '',
                    'codeCompliance': self.clay_liners_code_compliance or '',
                    'photos': self.clay_liners_photos or []
                },
                'firebrickLiners': {
                    'condition': self.firebrick_liners_condition or '',
                    'comments': self.firebrick_liners_comments or '',
                    'codeCompliance': self.firebrick_liners_code_compliance or '',
                    'photos': self.firebrick_liners_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class WoodStoveMasonryChimneyLinersInstallation(db.Model):
    __tablename__ = 'wood_stove_masonry_chimney_liners_installation'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Mortar for Solid Fuel section
    mortar_solid_fuel_condition = db.Column(db.String(255), nullable=True)
    mortar_solid_fuel_comments = db.Column(db.Text, nullable=True)
    mortar_solid_fuel_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    mortar_solid_fuel_photos = db.Column(db.JSON, nullable=True)

    # Mortar for Oil/Gas section
    mortar_oil_gas_condition = db.Column(db.String(255), nullable=True)
    mortar_oil_gas_comments = db.Column(db.Text, nullable=True)
    mortar_oil_gas_code_compliance = db.Column(db.String(10), nullable=True)
    mortar_oil_gas_photos = db.Column(db.JSON, nullable=True)

    # Extension of Chimney Liners section
    extension_chimney_liners_condition = db.Column(db.String(255), nullable=True)
    extension_chimney_liners_comments = db.Column(db.Text, nullable=True)
    extension_chimney_liners_code_compliance = db.Column(db.String(10), nullable=True)
    extension_chimney_liners_photos = db.Column(db.JSON, nullable=True)

    # Wall Thickness section
    wall_thickness_condition = db.Column(db.String(255), nullable=True)
    wall_thickness_comments = db.Column(db.Text, nullable=True)
    wall_thickness_code_compliance = db.Column(db.String(10), nullable=True)
    wall_thickness_photos = db.Column(db.JSON, nullable=True)

    # Lining Materials section
    lining_materials_condition = db.Column(db.String(255), nullable=True)
    lining_materials_comments = db.Column(db.Text, nullable=True)
    lining_materials_code_compliance = db.Column(db.String(10), nullable=True)
    lining_materials_photos = db.Column(db.JSON, nullable=True)

    # Clay Liners section
    clay_liners_condition = db.Column(db.String(255), nullable=True)
    clay_liners_comments = db.Column(db.Text, nullable=True)
    clay_liners_code_compliance = db.Column(db.String(10), nullable=True)
    clay_liners_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_chimney_liners_installation', uselist=False))


class WoodStoveMasonryChimneyLiners(db.Model):
    __tablename__ = 'wood_stove_masonry_chimney_liners'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Concrete Liners section
    concrete_liners_condition = db.Column(db.String(255), nullable=True)
    concrete_liners_comments = db.Column(db.Text, nullable=True)
    concrete_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    concrete_liners_photos = db.Column(db.JSON, nullable=True)

    # Metal Liners section
    metal_liners_condition = db.Column(db.String(255), nullable=True)
    metal_liners_comments = db.Column(db.Text, nullable=True)
    metal_liners_code_compliance = db.Column(db.String(10), nullable=True)
    metal_liners_photos = db.Column(db.JSON, nullable=True)

    # OBC Chimney Flue Pipe Walls section
    obc_chimney_flue_pipe_walls_condition = db.Column(db.String(255), nullable=True)
    obc_chimney_flue_pipe_walls_comments = db.Column(db.Text, nullable=True)
    obc_chimney_flue_pipe_walls_code_compliance = db.Column(db.String(10), nullable=True)
    obc_chimney_flue_pipe_walls_photos = db.Column(db.JSON, nullable=True)

    # ABC/BCBC/NBC Chimney Flue Pipe Walls section
    abc_bcbc_nbc_chimney_flue_pipe_walls_condition = db.Column(db.String(255), nullable=True)
    abc_bcbc_nbc_chimney_flue_pipe_walls_comments = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_chimney_flue_pipe_walls_code_compliance = db.Column(db.String(10), nullable=True)
    abc_bcbc_nbc_chimney_flue_pipe_walls_photos = db.Column(db.JSON, nullable=True)

    # Size of Chimney Flues section
    size_of_chimney_flues_condition = db.Column(db.String(255), nullable=True)
    size_of_chimney_flues_comments = db.Column(db.Text, nullable=True)
    size_of_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)
    size_of_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    # Oval Chimney Flues section
    oval_chimney_flues_condition = db.Column(db.String(255), nullable=True)
    oval_chimney_flues_comments = db.Column(db.Text, nullable=True)
    oval_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)
    oval_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_chimney_liners', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'concreteLiners': {
                    'title': 'Concrete Liners',
                    'codeReference': '9.21.3.5.',
                    'description': '(1) Concrete flue liners shall conform to Clause 4.2.6.4 of CAN/CSA-A405-M-87, "Design and Construction of Masonry Chimneys and Fireplaces."',
                    'condition': self.concrete_liners_condition or '',
                    'comments': self.concrete_liners_comments or '',
                    'codeCompliance': self.concrete_liners_code_compliance or '',
                    'photos': self.concrete_liners_photos or []
                },
                'metalLiners': {
                    'title': 'Metal Liners',
                    'codeReference': '9.21.3.6.',
                    'description': '(1) Metal liners shall be constructed of not less than 0.3 mm thick stainless steel, (2) Metal liners referred to in Sentence (1) shall only be used in chimneys serving gas- or oil-burning appliances.',
                    'condition': self.metal_liners_condition or '',
                    'comments': self.metal_liners_comments or '',
                    'codeCompliance': self.metal_liners_code_compliance or '',
                    'photos': self.metal_liners_photos or []
                },
                'obcChimneyFluePipeWalls': {
                    'title': 'OBC 9.21.1.4. Chimney or Flue pipe walls',
                    'codeReference': '9.21.1.4.',
                    'description': '(1) The walls of any chimney or flue pipe shall be constructed to be smoke- and flame-tight.',
                    'condition': self.obc_chimney_flue_pipe_walls_condition or '',
                    'comments': self.obc_chimney_flue_pipe_walls_comments or '',
                    'codeCompliance': self.obc_chimney_flue_pipe_walls_code_compliance or '',
                    'photos': self.obc_chimney_flue_pipe_walls_photos or []
                },
                'abcBcbcNbcChimneyFluePipeWalls': {
                    'title': 'ABC/BCBC/NBC 9.21.1.2. Chimney or Flue pipe walls',
                    'codeReference': '9.21.1.2.',
                    'description': '(1) The walls of any chimney or flue pipe shall be constructed to be smoke- and flame-tight.',
                    'condition': self.abc_bcbc_nbc_chimney_flue_pipe_walls_condition or '',
                    'comments': self.abc_bcbc_nbc_chimney_flue_pipe_walls_comments or '',
                    'codeCompliance': self.abc_bcbc_nbc_chimney_flue_pipe_walls_code_compliance or '',
                    'photos': self.abc_bcbc_nbc_chimney_flue_pipe_walls_photos or []
                },
                'sizeOfChimneyFlues': {
                    'title': 'Size of Chimney Flues',
                    'codeReference': '9.21.2.4',
                    'description': '(1) Except for chimneys serving fireplaces, the size of a chimney flue shall conform to the requirements of the appliance installation standards referenced in Sentences 9.33.5.2.(1) and 9.33.5.3.(1)',
                    'condition': self.size_of_chimney_flues_condition or '',
                    'comments': self.size_of_chimney_flues_comments or '',
                    'codeCompliance': self.size_of_chimney_flues_code_compliance or '',
                    'photos': self.size_of_chimney_flues_photos or []
                },
                'ovalChimneyFlues': {
                    'title': 'Oval Chimney Flues',
                    'codeReference': '9.21.2.6.',
                    'description': '(1) The width of an oval chimney flue shall be not less than two-thirds its breadth.',
                    'condition': self.oval_chimney_flues_condition or '',
                    'comments': self.oval_chimney_flues_comments or '',
                    'codeCompliance': self.oval_chimney_flues_code_compliance or '',
                    'photos': self.oval_chimney_flues_photos or []
                }
            }
        }


class WoodStoveMasonryChimneySaddles(db.Model):
    __tablename__ = 'wood_stove_masonry_chimney_saddles'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Chimney Saddles section
    chimney_saddles_condition = db.Column(db.String(255), nullable=True)
    chimney_saddles_comments = db.Column(db.Text, nullable=True)
    chimney_saddles_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    chimney_saddles_photos = db.Column(db.JSON, nullable=True)

    # Fire Code Chimney Flues section
    fire_code_chimney_flues_condition = db.Column(db.String(255), nullable=True)
    fire_code_chimney_flues_comments = db.Column(db.Text, nullable=True)
    fire_code_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    # Fire Code Cleaning section
    fire_code_cleaning_condition = db.Column(db.String(255), nullable=True)
    fire_code_cleaning_comments = db.Column(db.Text, nullable=True)
    fire_code_cleaning_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_cleaning_photos = db.Column(db.JSON, nullable=True)

    # Fire Code Structural Deficiency section
    fire_code_structural_deficiency_condition = db.Column(db.String(255), nullable=True)
    fire_code_structural_deficiency_comments = db.Column(db.Text, nullable=True)
    fire_code_structural_deficiency_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_structural_deficiency_photos = db.Column(db.JSON, nullable=True)

    # Fire Code Abandoned Openings section
    fire_code_abandoned_openings_condition = db.Column(db.String(255), nullable=True)
    fire_code_abandoned_openings_comments = db.Column(db.Text, nullable=True)
    fire_code_abandoned_openings_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_abandoned_openings_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_chimney_saddles', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'chimneySaddles': {
                    'title': 'Chimney Saddles',
                    'codeReference': '9.26.4.8',
                    'description': 'Except as otherwise permitted in Sentence (5), chimney saddles shall be installed where the upper side of a chimney on a sloping roof is more than 750 mm (30") wide.\n\nA chimney saddle need not be installed if the intersection between the chimney and roof is protected by sheet metal flashing that extends up the chimney to a height equal to at least one sixth the width of the chimney, but not less than 150 mm (6"), and up the roof slope to a point equal in height to the flashing on the chimney, but not less than 1.5 times the shingle exposure.',
                    'condition': self.chimney_saddles_condition or '',
                    'comments': self.chimney_saddles_comments or '',
                    'codeCompliance': self.chimney_saddles_code_compliance or '',
                    'photos': self.chimney_saddles_photos or []
                },
                'fireCodeChimneyFlues': {
                    'title': 'Fire Code – Chimneys, Flues and Flue Pipes',
                    'codeReference': '2.6.1.4',
                    'description': 'Every chimney, flue and flue pipe shall be inspected to identify any dangerous condition:\n\nat intervals not greater than 12 months,\n\nat the time of addition of any appliance, and\n\nafter any chimney fire.',
                    'condition': self.fire_code_chimney_flues_condition or '',
                    'comments': self.fire_code_chimney_flues_comments or '',
                    'codeCompliance': self.fire_code_chimney_flues_code_compliance or '',
                    'photos': self.fire_code_chimney_flues_photos or []
                },
                'fireCodeCleaning': {
                    'title': 'Fire Code',
                    'codeReference': '2.6.1.4(2)',
                    'description': 'Chimneys, flues and flue pipes shall be cleaned as often as necessary to keep them free from dangerous accumulations of combustible deposits.\n\nAppendix A – A.2.6.1.4(2):\nThe presence in a chimney of deposits of soot or creosote in excess of 3 mm thick will indicate the need for immediate cleaning, possible modification of burning procedures, and more frequent inspections.',
                    'condition': self.fire_code_cleaning_condition or '',
                    'comments': self.fire_code_cleaning_comments or '',
                    'codeCompliance': self.fire_code_cleaning_code_compliance or '',
                    'photos': self.fire_code_cleaning_photos or []
                },
                'fireCodeStructuralDeficiency': {
                    'title': 'Fire Code – Structural Deficiency or Decay',
                    'codeReference': '2.6.1.4(3a)',
                    'description': 'A chimney, flue, or flue pipe shall be replaced or repaired to eliminate any structural deficiency or decay.\n\nAppendix A – A.2.6.1.4(3a):\nStructural deficiencies are deviations from required construction, such as the absence of a liner or inadequate design of supports or ties. Instances of decay are cracking, settling, crumbling mortar, distortion, advanced corrosion, separation of sections, or loose or broken supports.',
                    'condition': self.fire_code_structural_deficiency_condition or '',
                    'comments': self.fire_code_structural_deficiency_comments or '',
                    'codeCompliance': self.fire_code_structural_deficiency_code_compliance or '',
                    'photos': self.fire_code_structural_deficiency_photos or []
                },
                'fireCodeAbandonedOpenings': {
                    'title': 'Fire Code – Abandoned or Unused Openings',
                    'codeReference': '2.6.1.4(3b)',
                    'description': 'A chimney, flue, or flue pipe shall be replaced or repaired to eliminate all abandoned or unused openings that are not effectively sealed in a manner that would prevent the passage of fire or smoke.',
                    'condition': self.fire_code_abandoned_openings_condition or '',
                    'comments': self.fire_code_abandoned_openings_comments or '',
                    'codeCompliance': self.fire_code_abandoned_openings_code_compliance or '',
                    'photos': self.fire_code_abandoned_openings_photos or []
                }
            }
        }


class WoodStoveMasonryChimneySpecifications(db.Model):
    __tablename__ = 'wood_stove_masonry_chimney_specifications'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Inspection details
    inspection_discussed = db.Column(db.String(10), nullable=True)  # yes/no
    building_permits_available = db.Column(db.String(10), nullable=True)  # yes/no
    time_of_day = db.Column(db.String(20), nullable=True)
    weather_conditions = db.Column(db.String(255), nullable=True)
    roofing_type_material = db.Column(db.String(255), nullable=True)
    roof_accessed = db.Column(db.String(10), nullable=True)  # yes/no
    attic_accessed = db.Column(db.String(10), nullable=True)  # yes/no

    # Chimney construction details
    chimney_fireplace_constructed_with_building = db.Column(db.String(10), nullable=True)  # yes/no/unknown
    approximate_age = db.Column(db.String(100), nullable=True)
    chimney_fireplace_shell = db.Column(db.String(50), nullable=True)  # brick/block/stone/others
    rain_cap = db.Column(db.String(20), nullable=True)  # yes/no/with-screening/without-screening
    chimney_location = db.Column(db.String(20), nullable=True)  # interior/exterior
    height_from_firebox_floor = db.Column(db.String(100), nullable=True)
    flue_size = db.Column(db.String(100), nullable=True)
    size_of_flue = db.Column(db.String(100), nullable=True)
    material_of_flue = db.Column(db.String(255), nullable=True)
    chimney_lined_with = db.Column(db.String(50), nullable=True)  # clay-tile/pumice/stainless-steel-flex/stainless-steel-rigid/no-liner/insulated/uti

    # Installation details
    chimney_installed_by = db.Column(db.String(255), nullable=True)
    chimney_installed_by_unknown = db.Column(db.Boolean, default=False)
    chimney_date = db.Column(db.String(20), nullable=True)

    # Fireplace details
    fireplace_location = db.Column(db.String(20), nullable=True)  # interior/exterior
    installed_in = db.Column(db.String(50), nullable=True)  # residence-part9/modular-home-a277/mobile-home-manufactured-z240/alcove/garage/other
    fireplace_location2 = db.Column(db.String(20), nullable=True)  # basement/main-floor/other-specify
    others_specify = db.Column(db.String(255), nullable=True)
    fireplace_installed_by = db.Column(db.String(255), nullable=True)
    fireplace_installed_by_unknown = db.Column(db.Boolean, default=False)
    fireplace_date = db.Column(db.String(20), nullable=True)
    fireplace_location3 = db.Column(db.String(20), nullable=True)  # interior/exterior

    # System details
    unit_share_venting_system = db.Column(db.String(10), nullable=True)  # yes/no

    # Comments and assessment
    comments_condition_of_chimney = db.Column(db.Text, nullable=True)
    suitable = db.Column(db.String(15), nullable=True)  # yes/no-see-notes

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_chimney_specifications', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'inspectionDiscussed': self.inspection_discussed or '',
                'buildingPermitsAvailable': self.building_permits_available or '',
                'timeOfDay': self.time_of_day or '',
                'weatherConditions': self.weather_conditions or '',
                'roofingTypeMaterial': self.roofing_type_material or '',
                'roofAccessed': self.roof_accessed or '',
                'atticAccessed': self.attic_accessed or '',
                'chimneyFireplaceConstructedWithBuilding': self.chimney_fireplace_constructed_with_building or '',
                'approximateAge': self.approximate_age or '',
                'chimneyFireplaceShell': self.chimney_fireplace_shell or '',
                'rainCap': self.rain_cap or '',
                'chimneyLocation': self.chimney_location or '',
                'heightFromFireboxFloor': self.height_from_firebox_floor or '',
                'flueSize': self.flue_size or '',
                'sizeOfFlue': self.size_of_flue or '',
                'materialOfFlue': self.material_of_flue or '',
                'chimneyLinedWith': self.chimney_lined_with or '',
                'chimneyInstalledBy': self.chimney_installed_by or '',
                'chimneyInstalledByUnknown': self.chimney_installed_by_unknown or False,
                'chimneyDate': self.chimney_date or '',
                'fireplaceLocation': self.fireplace_location or '',
                'installedIn': self.installed_in or '',
                'fireplaceLocation2': self.fireplace_location2 or '',
                'othersSpecify': self.others_specify or '',
                'fireplaceInstalledBy': self.fireplace_installed_by or '',
                'fireplaceInstalledByUnknown': self.fireplace_installed_by_unknown or False,
                'fireplaceDate': self.fireplace_date or '',
                'fireplaceLocation3': self.fireplace_location3 or '',
                'unitShareVentingSystem': self.unit_share_venting_system or '',
                'commentsConditionOfChimney': self.comments_condition_of_chimney or '',
                'suitable': self.suitable or ''
            }
        }


class WoodStoveMasonryChimneyStabilityCaps(db.Model):
    __tablename__ = 'wood_stove_masonry_chimney_stability_caps'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Height of Chimney Flues section
    height_of_chimney_flues_condition = db.Column(db.String(255), nullable=True)
    height_of_chimney_flues_comments = db.Column(db.Text, nullable=True)
    height_of_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    height_of_chimney_flues_photos = db.Column(db.JSON, nullable=True)
    height_of_chimney_flues_required_height = db.Column(db.String(100), nullable=True)
    height_of_chimney_flues_present_value_height = db.Column(db.String(100), nullable=True)
    height_of_chimney_flues_required_vertical = db.Column(db.String(100), nullable=True)
    height_of_chimney_flues_present_value_vertical = db.Column(db.String(100), nullable=True)

    # Lateral Stability section
    lateral_stability_condition = db.Column(db.String(255), nullable=True)
    lateral_stability_comments = db.Column(db.Text, nullable=True)
    lateral_stability_code_compliance = db.Column(db.String(10), nullable=True)
    lateral_stability_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 1 section
    chimney_caps_1_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_1_comments = db.Column(db.Text, nullable=True)
    chimney_caps_1_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_1_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 2 section
    chimney_caps_2_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_2_comments = db.Column(db.Text, nullable=True)
    chimney_caps_2_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_2_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 3 section
    chimney_caps_3_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_3_comments = db.Column(db.Text, nullable=True)
    chimney_caps_3_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_3_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 4 section
    chimney_caps_4_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_4_comments = db.Column(db.Text, nullable=True)
    chimney_caps_4_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_4_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_chimney_stability_caps', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'heightOfChimneyFlues': {
                    'title': 'Height of Chimney Flues',
                    'codeReference': '9.21.4.4',
                    'description': '(1) A chimney flue shall extend not less than 900 mm (36") above the highest point at which the chimney comes in contact with the roof and at least 600 mm (24") above the highest roof surface or structure within 3 m (10\') of the chimney.',
                    'condition': self.height_of_chimney_flues_condition or '',
                    'comments': self.height_of_chimney_flues_comments or '',
                    'codeCompliance': self.height_of_chimney_flues_code_compliance or '',
                    'photos': self.height_of_chimney_flues_photos or [],
                    'requiredHeight': self.height_of_chimney_flues_required_height or '',
                    'presentValueHeight': self.height_of_chimney_flues_present_value_height or '',
                    'requiredVertical': self.height_of_chimney_flues_required_vertical or '',
                    'presentValueVertical': self.height_of_chimney_flues_present_value_vertical or ''
                },
                'lateralStability': {
                    'title': 'Lateral Stability',
                    'codeReference': '9.21.4.5',
                    'description': '(1) Except as provided in Sentence (2), chimneys shall be braced in accordance with Sentence A-9.21.4.10 to provide lateral stability under wind loads.\n\n(2) A chimney need not be laterally braced provided:\n\na) unsupported height difference is less than 600 mm (24"), or\n\nb) the chimney extends not more than 3 m (10\') above the roof surface or beyond a wall of which it forms a part.',
                    'condition': self.lateral_stability_condition or '',
                    'comments': self.lateral_stability_comments or '',
                    'codeCompliance': self.lateral_stability_code_compliance or '',
                    'photos': self.lateral_stability_photos or []
                },
                'chimneyCaps1': {
                    'title': 'Chimney Caps',
                    'codeReference': '9.21.4.6(1)',
                    'description': 'The top of a chimney shall have a waterproof cap of reinforced concrete, masonry or metal.',
                    'condition': self.chimney_caps_1_condition or '',
                    'comments': self.chimney_caps_1_comments or '',
                    'codeCompliance': self.chimney_caps_1_code_compliance or '',
                    'photos': self.chimney_caps_1_photos or []
                },
                'chimneyCaps2': {
                    'title': 'Chimney Caps',
                    'codeReference': '9.21.4.6(2)',
                    'description': 'The cap required in Sentence (1) shall slope from the lining and be provided with a drip edge not less than 25 mm (1") from the chimney wall.',
                    'condition': self.chimney_caps_2_condition or '',
                    'comments': self.chimney_caps_2_comments or '',
                    'codeCompliance': self.chimney_caps_2_code_compliance or '',
                    'photos': self.chimney_caps_2_photos or []
                },
                'chimneyCaps3': {
                    'title': 'Chimney Caps',
                    'codeReference': '9.21.4.6(3)',
                    'description': 'Cast-in-place concrete caps shall be separated from the chimney liner by a bond break and be sealed at that location.',
                    'condition': self.chimney_caps_3_condition or '',
                    'comments': self.chimney_caps_3_comments or '',
                    'codeCompliance': self.chimney_caps_3_code_compliance or '',
                    'photos': self.chimney_caps_3_photos or []
                },
                'chimneyCaps4': {
                    'title': 'Chimney Caps',
                    'codeReference': '9.21.4.6(4)',
                    'description': 'Jointed precast concrete or masonry chimney caps shall have flashing installed beneath the cap, extending from the liner to the drip edge.',
                    'condition': self.chimney_caps_4_condition or '',
                    'comments': self.chimney_caps_4_comments or '',
                    'codeCompliance': self.chimney_caps_4_code_compliance or '',
                    'photos': self.chimney_caps_4_photos or []
                }
            }
        }


class WoodStoveMasonryChimneySupports(db.Model):
    __tablename__ = 'wood_stove_masonry_chimney_supports'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Flashing section
    flashing_condition = db.Column(db.String(255), nullable=True)
    flashing_comments = db.Column(db.Text, nullable=True)
    flashing_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    flashing_photos = db.Column(db.JSON, nullable=True)

    # Clearance Combustible Materials section
    clearance_combustible_materials_condition = db.Column(db.String(255), nullable=True)
    clearance_combustible_materials_comments = db.Column(db.Text, nullable=True)
    clearance_combustible_materials_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_combustible_materials_photos = db.Column(db.JSON, nullable=True)

    # Clearance Combustible Materials 3 section
    clearance_combustible_materials_3_condition = db.Column(db.String(255), nullable=True)
    clearance_combustible_materials_3_comments = db.Column(db.Text, nullable=True)
    clearance_combustible_materials_3_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_combustible_materials_3_photos = db.Column(db.JSON, nullable=True)

    # Sealing Spaces section
    sealing_spaces_condition = db.Column(db.String(255), nullable=True)
    sealing_spaces_comments = db.Column(db.Text, nullable=True)
    sealing_spaces_code_compliance = db.Column(db.String(10), nullable=True)
    sealing_spaces_photos = db.Column(db.JSON, nullable=True)

    # Support Joists Beams section
    support_joists_beams_condition = db.Column(db.String(255), nullable=True)
    support_joists_beams_comments = db.Column(db.Text, nullable=True)
    support_joists_beams_code_compliance = db.Column(db.String(10), nullable=True)
    support_joists_beams_photos = db.Column(db.JSON, nullable=True)

    # Inclined Chimney Flues section
    inclined_chimney_flues_condition = db.Column(db.String(255), nullable=True)
    inclined_chimney_flues_comments = db.Column(db.Text, nullable=True)
    inclined_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)
    inclined_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    # Intersection Shingle Roofs section
    intersection_shingle_roofs_condition = db.Column(db.String(255), nullable=True)
    intersection_shingle_roofs_comments = db.Column(db.Text, nullable=True)
    intersection_shingle_roofs_code_compliance = db.Column(db.String(10), nullable=True)
    intersection_shingle_roofs_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_chimney_supports', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'flashing': {
                    'title': 'Flashing',
                    'codeReference': '9.21.4.10',
                    'description': 'Junctions with adjacent materials shall be adequately flashed to shed water.',
                    'condition': self.flashing_condition or '',
                    'comments': self.flashing_comments or '',
                    'codeCompliance': self.flashing_code_compliance or '',
                    'photos': self.flashing_photos or []
                },
                'clearanceCombustibleMaterials': {
                    'title': 'Clearance from Combustible Materials',
                    'codeReference': '9.21.5.1',
                    'description': 'The clearance between masonry or concrete chimneys and combustible framing shall not be less than 50 mm (2") for interior chimneys, and 12 mm (1/2") for exterior chimneys.\n\nNOTE: A-9.21.5.1(1) Clearance from Combustible Materials\nFor purposes of this Sentence, an exterior chimney shall be considered to be one which has at least one side exposed to the outdoors (excluding the outside wall of the building having masonry veneer). All other chimneys shall be considered to be interior.',
                    'condition': self.clearance_combustible_materials_condition or '',
                    'comments': self.clearance_combustible_materials_comments or '',
                    'codeCompliance': self.clearance_combustible_materials_code_compliance or '',
                    'photos': self.clearance_combustible_materials_photos or []
                },
                'clearanceCombustibleMaterials3': {
                    'title': 'Clearance from Combustible Materials',
                    'codeReference': '9.21.5.1(3)',
                    'description': 'Combustible flooring and subflooring shall have not less than a 12 mm (1/2") clearance from masonry or concrete chimneys.',
                    'condition': self.clearance_combustible_materials_3_condition or '',
                    'comments': self.clearance_combustible_materials_3_comments or '',
                    'codeCompliance': self.clearance_combustible_materials_3_code_compliance or '',
                    'photos': self.clearance_combustible_materials_3_photos or []
                },
                'sealingSpaces': {
                    'title': 'Sealing of Spaces',
                    'codeReference': '9.21.5.2',
                    'description': 'All spaces between masonry or concrete chimneys and combustible framing shall be sealed top or bottom with noncombustible material.',
                    'condition': self.sealing_spaces_condition or '',
                    'comments': self.sealing_spaces_comments or '',
                    'codeCompliance': self.sealing_spaces_code_compliance or '',
                    'photos': self.sealing_spaces_photos or []
                },
                'supportJoistsBeams': {
                    'title': 'Support of Joists & Beams',
                    'codeReference': '9.21.5.3',
                    'description': 'Joists or beams may be supported on masonry walls which enclose chimney flues provided the combustible members are separated from the flue by not less than 200 mm (7 ⅞") of solid masonry.',
                    'condition': self.support_joists_beams_condition or '',
                    'comments': self.support_joists_beams_comments or '',
                    'codeCompliance': self.support_joists_beams_code_compliance or '',
                    'photos': self.support_joists_beams_photos or []
                },
                'inclinedChimneyFlues': {
                    'title': 'Inclined Chimney Flues',
                    'codeReference': '9.21.3',
                    'description': '(1) Chimney flues shall not be inclined more than 30° from the vertical.',
                    'condition': self.inclined_chimney_flues_condition or '',
                    'comments': self.inclined_chimney_flues_comments or '',
                    'codeCompliance': self.inclined_chimney_flues_code_compliance or '',
                    'photos': self.inclined_chimney_flues_photos or []
                },
                'intersectionShingleRoofs': {
                    'title': 'Intersection of Shingle Roofs and Masonry',
                    'codeReference': '9.26.4.4',
                    'description': 'The intersection of shingled roofs and masonry walls or chimneys shall be protected with flashing.\n\nCounter flashing required in Sentence (1) shall be embedded not less than 25 mm (1") in the masonry wall and extend not less than 75 mm (3") down the masonry and lap the base flashing not less than 100 mm (4").\n\nFlashing along the slopes of a roof described in Sentence (1) shall be stepped so that there is not less than a 75 mm (3") head lap in the base flashing and counter flashing.\n\nWhere the roof described in Sentence (1) abuts against the masonry, flashing shall extend up the roof not less than 125 mm (5") and up to a point equal in height to the flashing on the masonry, but not less than 1.5 times the shingle exposure.',
                    'condition': self.intersection_shingle_roofs_condition or '',
                    'comments': self.intersection_shingle_roofs_comments or '',
                    'codeCompliance': self.intersection_shingle_roofs_code_compliance or '',
                    'photos': self.intersection_shingle_roofs_photos or []
                }
            }
        }


class WoodStoveMasonryClearancesShielding(db.Model):
    __tablename__ = 'wood_stove_masonry_clearances_shielding'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Combustible right side wall section
    combustible_right_side_wall_required_value_uncertified = db.Column(db.String(255), nullable=True)
    combustible_right_side_wall_required_value_certified = db.Column(db.String(255), nullable=True)
    combustible_right_side_wall_present_value = db.Column(db.String(255), nullable=True)
    combustible_right_side_wall_code_compliance = db.Column(db.String(10), nullable=True)
    combustible_right_side_wall_photos = db.Column(db.JSON, nullable=True)

    # Combustible left side wall section
    combustible_left_side_wall_required_value_uncertified = db.Column(db.String(255), nullable=True)
    combustible_left_side_wall_required_value_certified = db.Column(db.String(255), nullable=True)
    combustible_left_side_wall_present_value = db.Column(db.String(255), nullable=True)
    combustible_left_side_wall_code_compliance = db.Column(db.String(10), nullable=True)
    combustible_left_side_wall_photos = db.Column(db.JSON, nullable=True)

    # Combustible rear wall section
    combustible_rear_wall_required_value_uncertified = db.Column(db.String(255), nullable=True)
    combustible_rear_wall_required_value_certified = db.Column(db.String(255), nullable=True)
    combustible_rear_wall_present_value = db.Column(db.String(255), nullable=True)
    combustible_rear_wall_code_compliance = db.Column(db.String(10), nullable=True)
    combustible_rear_wall_photos = db.Column(db.JSON, nullable=True)

    # Combustible corner right side section
    combustible_corner_right_side_required_value_uncertified = db.Column(db.String(255), nullable=True)
    combustible_corner_right_side_required_value_certified = db.Column(db.String(255), nullable=True)
    combustible_corner_right_side_present_value = db.Column(db.String(255), nullable=True)
    combustible_corner_right_side_code_compliance = db.Column(db.String(10), nullable=True)
    combustible_corner_right_side_photos = db.Column(db.JSON, nullable=True)

    # Combustible corner left side section
    combustible_corner_left_side_required_value_uncertified = db.Column(db.String(255), nullable=True)
    combustible_corner_left_side_required_value_certified = db.Column(db.String(255), nullable=True)
    combustible_corner_left_side_present_value = db.Column(db.String(255), nullable=True)
    combustible_corner_left_side_code_compliance = db.Column(db.String(10), nullable=True)
    combustible_corner_left_side_photos = db.Column(db.JSON, nullable=True)

    # Top ceiling section
    top_ceiling_required_value_uncertified = db.Column(db.String(255), nullable=True)
    top_ceiling_required_value_certified = db.Column(db.String(255), nullable=True)
    top_ceiling_present_value = db.Column(db.String(255), nullable=True)
    top_ceiling_code_compliance = db.Column(db.String(10), nullable=True)
    top_ceiling_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_clearances_shielding', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'combustibleRightSideWall': {
                    'title': 'Combustible right side wall',
                    'requiredValueUncertified': self.combustible_right_side_wall_required_value_uncertified or '36"/ 48"',
                    'requiredValueCertified': self.combustible_right_side_wall_required_value_certified or '',
                    'presentValue': self.combustible_right_side_wall_present_value or '',
                    'codeCompliance': self.combustible_right_side_wall_code_compliance or '',
                    'photos': self.combustible_right_side_wall_photos or []
                },
                'combustibleLeftSideWall': {
                    'title': 'Combustible left side wall',
                    'requiredValueUncertified': self.combustible_left_side_wall_required_value_uncertified or '36"/ 48"',
                    'requiredValueCertified': self.combustible_left_side_wall_required_value_certified or '',
                    'presentValue': self.combustible_left_side_wall_present_value or '',
                    'codeCompliance': self.combustible_left_side_wall_code_compliance or '',
                    'photos': self.combustible_left_side_wall_photos or []
                },
                'combustibleRearWall': {
                    'title': 'Combustible rear wall',
                    'requiredValueUncertified': self.combustible_rear_wall_required_value_uncertified or '36"/ 48"',
                    'requiredValueCertified': self.combustible_rear_wall_required_value_certified or '',
                    'presentValue': self.combustible_rear_wall_present_value or '',
                    'codeCompliance': self.combustible_rear_wall_code_compliance or '',
                    'photos': self.combustible_rear_wall_photos or []
                },
                'combustibleCornerRightSide': {
                    'title': 'Combustible corner - right side (45 degrees)',
                    'requiredValueUncertified': self.combustible_corner_right_side_required_value_uncertified or '36"/ 48"',
                    'requiredValueCertified': self.combustible_corner_right_side_required_value_certified or '',
                    'presentValue': self.combustible_corner_right_side_present_value or '',
                    'codeCompliance': self.combustible_corner_right_side_code_compliance or '',
                    'photos': self.combustible_corner_right_side_photos or []
                },
                'combustibleCornerLeftSide': {
                    'title': 'Combustible corner - left side (45 degrees)',
                    'requiredValueUncertified': self.combustible_corner_left_side_required_value_uncertified or '36"/ 48"',
                    'requiredValueCertified': self.combustible_corner_left_side_required_value_certified or '',
                    'presentValue': self.combustible_corner_left_side_present_value or '',
                    'codeCompliance': self.combustible_corner_left_side_code_compliance or '',
                    'photos': self.combustible_corner_left_side_photos or []
                },
                'topCeiling': {
                    'title': 'Top/ceiling',
                    'requiredValueUncertified': self.top_ceiling_required_value_uncertified or '60"',
                    'requiredValueCertified': self.top_ceiling_required_value_certified or '',
                    'presentValue': self.top_ceiling_present_value or '',
                    'codeCompliance': self.top_ceiling_code_compliance or '',
                    'photos': self.top_ceiling_photos or []
                }
            }
        }


class WoodStoveMasonryCombustibleMaterials(db.Model):
    __tablename__ = 'wood_stove_masonry_combustible_materials'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Outdoor combustion air section
    outdoor_combustion_air_required_value_uncertified = db.Column(db.String(10), nullable=True)
    outdoor_combustion_air_required_value_certified = db.Column(db.String(255), nullable=True)
    outdoor_combustion_air_present_value = db.Column(db.String(255), nullable=True)
    outdoor_combustion_air_code_compliance = db.Column(db.String(10), nullable=True)
    outdoor_combustion_air_photos = db.Column(db.JSON, nullable=True)

    # CO alarm same room BCBC section
    co_alarm_same_room_bcbc_required_value = db.Column(db.String(255), nullable=True)
    co_alarm_same_room_bcbc_present_value = db.Column(db.String(10), nullable=True)
    co_alarm_same_room_bcbc_code_compliance = db.Column(db.String(10), nullable=True)
    co_alarm_same_room_bcbc_photos = db.Column(db.JSON, nullable=True)

    # CO alarm same room ABC section
    co_alarm_same_room_abc_required_value = db.Column(db.String(255), nullable=True)
    co_alarm_same_room_abc_present_value = db.Column(db.String(10), nullable=True)
    co_alarm_same_room_abc_code_compliance = db.Column(db.String(10), nullable=True)
    co_alarm_same_room_abc_photos = db.Column(db.JSON, nullable=True)

    # CO alarm present section
    co_alarm_present_required_value = db.Column(db.String(255), nullable=True)
    co_alarm_present_present_value = db.Column(db.String(10), nullable=True)
    co_alarm_present_code_compliance = db.Column(db.String(10), nullable=True)
    co_alarm_present_photos = db.Column(db.JSON, nullable=True)

    # Flue pipe connector section
    flue_pipe_connector_type = db.Column(db.String(50), nullable=True)
    flue_pipe_connector_diameter = db.Column(db.String(255), nullable=True)
    flue_pipe_connector_manufacturer = db.Column(db.String(255), nullable=True)
    flue_pipe_connector_model = db.Column(db.String(255), nullable=True)
    flue_pipe_connector_listing_agency = db.Column(db.String(255), nullable=True)
    flue_pipe_connector_is_listing_agency_manually_available = db.Column(db.String(10), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_combustible_materials', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'outdoorCombustionAir': {
                    'title': 'Outdoor combustion air',
                    'requiredValueUncertified': self.outdoor_combustion_air_required_value_uncertified or '',
                    'requiredValueCertified': self.outdoor_combustion_air_required_value_certified or '',
                    'presentValue': self.outdoor_combustion_air_present_value or '',
                    'codeCompliance': self.outdoor_combustion_air_code_compliance or '',
                    'photos': self.outdoor_combustion_air_photos or []
                },
                'coAlarmSameRoomBCBC': {
                    'title': 'Is CO alarm present in same room with solid-fuel-burning appliance?',
                    'requiredValue': self.co_alarm_same_room_bcbc_required_value or '9.32.4.2.3 (BCBC)',
                    'presentValue': self.co_alarm_same_room_bcbc_present_value or '',
                    'codeCompliance': self.co_alarm_same_room_bcbc_code_compliance or '',
                    'photos': self.co_alarm_same_room_bcbc_photos or []
                },
                'coAlarmSameRoomABC': {
                    'title': 'Is CO alarm present in same room with solid-fuel-burning appliance?',
                    'requiredValue': self.co_alarm_same_room_abc_required_value or '9.32.3.9.3 (ABC)',
                    'presentValue': self.co_alarm_same_room_abc_present_value or '',
                    'codeCompliance': self.co_alarm_same_room_abc_code_compliance or '',
                    'photos': self.co_alarm_same_room_abc_photos or []
                },
                'coAlarmPresent': {
                    'title': 'Is CO alarm present?',
                    'requiredValue': self.co_alarm_present_required_value or '9.33.4.2 (OBC)',
                    'presentValue': self.co_alarm_present_present_value or '',
                    'codeCompliance': self.co_alarm_present_code_compliance or '',
                    'photos': self.co_alarm_present_photos or []
                },
                'fluePipeConnector': {
                    'title': 'Flue Pipe/ Connector',
                    'type': self.flue_pipe_connector_type or '',
                    'diameter': self.flue_pipe_connector_diameter or '',
                    'manufacturer': self.flue_pipe_connector_manufacturer or '',
                    'model': self.flue_pipe_connector_model or '',
                    'listingAgency': self.flue_pipe_connector_listing_agency or '',
                    'isListingAgencyManuallyAvailable': self.flue_pipe_connector_is_listing_agency_manually_available or ''
                }
            }
        }


class WoodStoveMasonryEmberPadFloorProtection(db.Model):
    __tablename__ = 'wood_stove_masonry_ember_pad_floor_protection'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Ember pad front section
    ember_pad_front_required_value_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_front_required_value_certified = db.Column(db.String(255), nullable=True)
    ember_pad_front_present_value = db.Column(db.String(255), nullable=True)
    ember_pad_front_code_compliance = db.Column(db.String(10), nullable=True)
    ember_pad_front_photos = db.Column(db.JSON, nullable=True)

    # Ember pad rear section
    ember_pad_rear_required_value_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_rear_required_value_certified = db.Column(db.String(255), nullable=True)
    ember_pad_rear_present_value = db.Column(db.String(255), nullable=True)
    ember_pad_rear_code_compliance = db.Column(db.String(10), nullable=True)
    ember_pad_rear_photos = db.Column(db.JSON, nullable=True)

    # Ember pad right side section
    ember_pad_right_side_required_value_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_right_side_required_value_certified = db.Column(db.String(255), nullable=True)
    ember_pad_right_side_present_value = db.Column(db.String(255), nullable=True)
    ember_pad_right_side_code_compliance = db.Column(db.String(10), nullable=True)
    ember_pad_right_side_photos = db.Column(db.JSON, nullable=True)

    # Ember pad left side section
    ember_pad_left_side_required_value_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_left_side_required_value_certified = db.Column(db.String(255), nullable=True)
    ember_pad_left_side_present_value = db.Column(db.String(255), nullable=True)
    ember_pad_left_side_code_compliance = db.Column(db.String(10), nullable=True)
    ember_pad_left_side_photos = db.Column(db.JSON, nullable=True)

    # Radiant heat floor protection uncertified section
    radiant_heat_floor_protection_uncertified_present_value = db.Column(db.String(255), nullable=True)
    radiant_heat_floor_protection_uncertified_code_compliance = db.Column(db.String(10), nullable=True)
    radiant_heat_floor_protection_uncertified_photos = db.Column(db.JSON, nullable=True)

    # Radiant heat floor protection certified section
    radiant_heat_floor_protection_certified_required_value = db.Column(db.String(255), nullable=True)
    radiant_heat_floor_protection_certified_present_value = db.Column(db.String(255), nullable=True)
    radiant_heat_floor_protection_certified_code_compliance = db.Column(db.String(10), nullable=True)
    radiant_heat_floor_protection_certified_photos = db.Column(db.JSON, nullable=True)

    # Hazardous location section
    hazardous_location_present_value = db.Column(db.String(255), nullable=True)
    hazardous_location_code_compliance = db.Column(db.String(10), nullable=True)
    hazardous_location_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_ember_pad_floor_protection', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'emberPadFront': {
                    'title': 'Ember pad - front',
                    'requiredValueUncertified': self.ember_pad_front_required_value_uncertified or 'Minimum 18"',
                    'requiredValueCertified': self.ember_pad_front_required_value_certified or '',
                    'presentValue': self.ember_pad_front_present_value or '',
                    'codeCompliance': self.ember_pad_front_code_compliance or '',
                    'photos': self.ember_pad_front_photos or []
                },
                'emberPadRear': {
                    'title': 'Ember pad - rear',
                    'requiredValueUncertified': self.ember_pad_rear_required_value_uncertified or 'Minimum 8"',
                    'requiredValueCertified': self.ember_pad_rear_required_value_certified or '',
                    'presentValue': self.ember_pad_rear_present_value or '',
                    'codeCompliance': self.ember_pad_rear_code_compliance or '',
                    'photos': self.ember_pad_rear_photos or []
                },
                'emberPadRightSide': {
                    'title': 'Ember pad - right side',
                    'requiredValueUncertified': self.ember_pad_right_side_required_value_uncertified or 'Minimum 8"',
                    'requiredValueCertified': self.ember_pad_right_side_required_value_certified or '',
                    'presentValue': self.ember_pad_right_side_present_value or '',
                    'codeCompliance': self.ember_pad_right_side_code_compliance or '',
                    'photos': self.ember_pad_right_side_photos or []
                },
                'emberPadLeftSide': {
                    'title': 'Ember pad - left side',
                    'requiredValueUncertified': self.ember_pad_left_side_required_value_uncertified or 'Minimum 8"',
                    'requiredValueCertified': self.ember_pad_left_side_required_value_certified or '',
                    'presentValue': self.ember_pad_left_side_present_value or '',
                    'codeCompliance': self.ember_pad_left_side_code_compliance or '',
                    'photos': self.ember_pad_left_side_photos or []
                },
                'radiantHeatFloorProtectionUncertified': {
                    'title': 'Radiant heat floor protection material - uncertified appliance',
                    'presentValue': self.radiant_heat_floor_protection_uncertified_present_value or '',
                    'codeCompliance': self.radiant_heat_floor_protection_uncertified_code_compliance or '',
                    'photos': self.radiant_heat_floor_protection_uncertified_photos or []
                },
                'radiantHeatFloorProtectionCertified': {
                    'title': 'Radiant heat floor protection material - certified appliance',
                    'requiredValue': self.radiant_heat_floor_protection_certified_required_value or '',
                    'presentValue': self.radiant_heat_floor_protection_certified_present_value or '',
                    'codeCompliance': self.radiant_heat_floor_protection_certified_code_compliance or '',
                    'photos': self.radiant_heat_floor_protection_certified_photos or []
                },
                'hazardousLocation': {
                    'title': 'Hazardous location',
                    'presentValue': self.hazardous_location_present_value or '',
                    'codeCompliance': self.hazardous_location_code_compliance or '',
                    'photos': self.hazardous_location_photos or []
                }
            }
        }


class WoodStoveMasonryFireplaceSpecifications(db.Model):
    __tablename__ = 'wood_stove_masonry_fireplace_specifications'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Basic fireplace information
    fireplace_make_model_serial = db.Column(db.String(255), nullable=True)
    installation_manual_available = db.Column(db.String(20), nullable=True)
    certification_standard = db.Column(db.String(20), nullable=True)
    listing_agency = db.Column(db.String(20), nullable=True)
    appliance_type = db.Column(db.String(30), nullable=True)
    flu_collar_size = db.Column(db.String(255), nullable=True)
    fan_blower_attached = db.Column(db.String(10), nullable=True)
    comments_condition_chimney = db.Column(db.Text, nullable=True)

    # Suitability and installation
    suitable = db.Column(db.String(15), nullable=True)
    installed_in = db.Column(db.String(30), nullable=True)
    other_installed_in = db.Column(db.String(255), nullable=True)
    appliance_location = db.Column(db.String(20), nullable=True)
    other_appliance_location = db.Column(db.String(255), nullable=True)
    appliance_installed_by = db.Column(db.String(255), nullable=True)
    appliance_installed_by_unknown = db.Column(db.Boolean, nullable=True)
    date_of_manufacture = db.Column(db.String(20), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_fireplace_specifications', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'fireplaceMakeModelSerial': self.fireplace_make_model_serial or '',
                'installationManualAvailable': self.installation_manual_available or '',
                'certificationStandard': self.certification_standard or '',
                'listingAgency': self.listing_agency or '',
                'applianceType': self.appliance_type or '',
                'fluCollarSize': self.flu_collar_size or '',
                'fanBlowerAttached': self.fan_blower_attached or '',
                'commentsConditionChimney': self.comments_condition_chimney or '',
                'suitable': self.suitable or '',
                'installedIn': self.installed_in or '',
                'otherInstalledIn': self.other_installed_in or '',
                'applianceLocation': self.appliance_location or '',
                'otherApplianceLocation': self.other_appliance_location or '',
                'applianceInstalledBy': self.appliance_installed_by or '',
                'applianceInstalledByUnknown': self.appliance_installed_by_unknown or False,
                'dateOfManufacture': self.date_of_manufacture or ''
            }
        }


class WoodStoveMasonryFluePipeOrientationJoints1(db.Model):
    __tablename__ = 'wood_stove_masonry_flue_pipe_orientation_joints_1'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Wall clearances right side section
    wall_clearances_right_side_required_value_uncertified = db.Column(db.String(255), nullable=True)
    wall_clearances_right_side_required_value_certified = db.Column(db.String(255), nullable=True)
    wall_clearances_right_side_present_value = db.Column(db.String(255), nullable=True)
    wall_clearances_right_side_code_compliance = db.Column(db.String(10), nullable=True)
    wall_clearances_right_side_photos = db.Column(db.JSON, nullable=True)

    # Wall clearances left side section
    wall_clearances_left_side_required_value_uncertified = db.Column(db.String(255), nullable=True)
    wall_clearances_left_side_required_value_certified = db.Column(db.String(255), nullable=True)
    wall_clearances_left_side_present_value = db.Column(db.String(255), nullable=True)
    wall_clearances_left_side_code_compliance = db.Column(db.String(10), nullable=True)
    wall_clearances_left_side_photos = db.Column(db.JSON, nullable=True)

    # Wall clearances rear wall section
    wall_clearances_rear_wall_required_value_uncertified = db.Column(db.String(255), nullable=True)
    wall_clearances_rear_wall_required_value_certified = db.Column(db.String(255), nullable=True)
    wall_clearances_rear_wall_present_value = db.Column(db.String(255), nullable=True)
    wall_clearances_rear_wall_code_compliance = db.Column(db.String(10), nullable=True)
    wall_clearances_rear_wall_photos = db.Column(db.JSON, nullable=True)

    # Clearances horizontal pipe section
    clearances_horizontal_pipe_required_value_uncertified = db.Column(db.String(255), nullable=True)
    clearances_horizontal_pipe_required_value_certified = db.Column(db.String(255), nullable=True)
    clearances_horizontal_pipe_present_value = db.Column(db.String(255), nullable=True)
    clearances_horizontal_pipe_code_compliance = db.Column(db.String(10), nullable=True)
    clearances_horizontal_pipe_photos = db.Column(db.JSON, nullable=True)

    # Clearances ceiling section
    clearances_ceiling_required_value_uncertified = db.Column(db.String(255), nullable=True)
    clearances_ceiling_required_value_certified = db.Column(db.String(255), nullable=True)
    clearances_ceiling_present_value = db.Column(db.String(255), nullable=True)
    clearances_ceiling_code_compliance = db.Column(db.String(10), nullable=True)
    clearances_ceiling_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_flue_pipe_orientation_joints_1', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'wallClearancesRightSide': {
                    'title': 'Wall clearances - right side',
                    'requiredValueUncertified': self.wall_clearances_right_side_required_value_uncertified or 'Unshielded 18"',
                    'requiredValueCertified': self.wall_clearances_right_side_required_value_certified or 'Unshielded 9"',
                    'presentValue': self.wall_clearances_right_side_present_value or '',
                    'codeCompliance': self.wall_clearances_right_side_code_compliance or '',
                    'photos': self.wall_clearances_right_side_photos or []
                },
                'wallClearancesLeftSide': {
                    'title': 'Wall clearances - left side',
                    'requiredValueUncertified': self.wall_clearances_left_side_required_value_uncertified or 'Unshielded 18"',
                    'requiredValueCertified': self.wall_clearances_left_side_required_value_certified or 'Unshielded 9"',
                    'presentValue': self.wall_clearances_left_side_present_value or '',
                    'codeCompliance': self.wall_clearances_left_side_code_compliance or '',
                    'photos': self.wall_clearances_left_side_photos or []
                },
                'wallClearancesRearWall': {
                    'title': 'Wall clearances - rear wall',
                    'requiredValueUncertified': self.wall_clearances_rear_wall_required_value_uncertified or 'Unshielded 18"',
                    'requiredValueCertified': self.wall_clearances_rear_wall_required_value_certified or 'Unshielded 9"',
                    'presentValue': self.wall_clearances_rear_wall_present_value or '',
                    'codeCompliance': self.wall_clearances_rear_wall_code_compliance or '',
                    'photos': self.wall_clearances_rear_wall_photos or []
                },
                'clearancesHorizontalPipe': {
                    'title': '(a) Clearances - horizontal pipe',
                    'requiredValueUncertified': self.clearances_horizontal_pipe_required_value_uncertified or 'Unshielded 18"',
                    'requiredValueCertified': self.clearances_horizontal_pipe_required_value_certified or 'Unshielded 9"',
                    'presentValue': self.clearances_horizontal_pipe_present_value or '',
                    'codeCompliance': self.clearances_horizontal_pipe_code_compliance or '',
                    'photos': self.clearances_horizontal_pipe_photos or []
                },
                'clearancesCeiling': {
                    'title': '(b) Clearances - ceiling',
                    'requiredValueUncertified': self.clearances_ceiling_required_value_uncertified or 'Unshielded 18"',
                    'requiredValueCertified': self.clearances_ceiling_required_value_certified or 'Unshielded 9"',
                    'presentValue': self.clearances_ceiling_present_value or '',
                    'codeCompliance': self.clearances_ceiling_code_compliance or '',
                    'photos': self.clearances_ceiling_photos or []
                }
            }
        }


class WoodStoveMasonryFluePipeOrientationJoints2(db.Model):
    __tablename__ = 'wood_stove_masonry_flue_pipe_orientation_joints_2'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Total length section
    total_length_required_value = db.Column(db.String(255), nullable=True)
    total_length_present_value = db.Column(db.String(255), nullable=True)
    total_length_code_compliance = db.Column(db.String(10), nullable=True)
    total_length_photos = db.Column(db.JSON, nullable=True)

    # Elbows maximum section
    elbows_maximum_required_value = db.Column(db.String(255), nullable=True)
    elbows_maximum_present_value = db.Column(db.String(255), nullable=True)
    elbows_maximum_code_compliance = db.Column(db.String(10), nullable=True)
    elbows_maximum_photos = db.Column(db.JSON, nullable=True)

    # Fastening section
    fastening_required_value = db.Column(db.String(255), nullable=True)
    fastening_present_value = db.Column(db.String(255), nullable=True)
    fastening_code_compliance = db.Column(db.String(10), nullable=True)
    fastening_photos = db.Column(db.JSON, nullable=True)

    # Allowance for expansion section
    allowance_for_expansion_required_value = db.Column(db.String(255), nullable=True)
    allowance_for_expansion_present_value = db.Column(db.String(255), nullable=True)
    allowance_for_expansion_code_compliance = db.Column(db.String(10), nullable=True)
    allowance_for_expansion_photos = db.Column(db.JSON, nullable=True)

    # Flue pipe orientation section
    flue_pipe_orientation_required_value = db.Column(db.String(255), nullable=True)
    flue_pipe_orientation_present_value = db.Column(db.String(255), nullable=True)
    flue_pipe_orientation_code_compliance = db.Column(db.String(10), nullable=True)
    flue_pipe_orientation_photos = db.Column(db.JSON, nullable=True)

    # Joint overlap section
    joint_overlap_required_value = db.Column(db.String(255), nullable=True)
    joint_overlap_present_value = db.Column(db.String(255), nullable=True)
    joint_overlap_code_compliance = db.Column(db.String(10), nullable=True)
    joint_overlap_photos = db.Column(db.JSON, nullable=True)

    # Flue pipe slope section
    flue_pipe_slope_required_value = db.Column(db.String(255), nullable=True)
    flue_pipe_slope_present_value = db.Column(db.String(255), nullable=True)
    flue_pipe_slope_code_compliance = db.Column(db.String(10), nullable=True)
    flue_pipe_slope_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_flue_pipe_orientation_joints_2', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'totalLength': {
                    'title': 'Total length',
                    'requiredValue': self.total_length_required_value or 'Maximum 10\'',
                    'presentValue': self.total_length_present_value or '',
                    'codeCompliance': self.total_length_code_compliance or '',
                    'photos': self.total_length_photos or []
                },
                'elbowsMaximum': {
                    'title': 'Elbows Maximum',
                    'requiredValue': self.elbows_maximum_required_value or '180°',
                    'presentValue': self.elbows_maximum_present_value or '',
                    'codeCompliance': self.elbows_maximum_code_compliance or '',
                    'photos': self.elbows_maximum_photos or []
                },
                'fastening': {
                    'title': 'Fastening',
                    'requiredValue': self.fastening_required_value or '3 screws per joint',
                    'presentValue': self.fastening_present_value or '',
                    'codeCompliance': self.fastening_code_compliance or '',
                    'photos': self.fastening_photos or []
                },
                'allowanceForExpansion': {
                    'title': 'Allowance for expansion',
                    'requiredValue': self.allowance_for_expansion_required_value or 'Elbow/ slip adjust',
                    'presentValue': self.allowance_for_expansion_present_value or '',
                    'codeCompliance': self.allowance_for_expansion_code_compliance or '',
                    'photos': self.allowance_for_expansion_photos or []
                },
                'fluePipeOrientation': {
                    'title': 'Flue pipe orientation',
                    'requiredValue': self.flue_pipe_orientation_required_value or 'Male end down',
                    'presentValue': self.flue_pipe_orientation_present_value or '',
                    'codeCompliance': self.flue_pipe_orientation_code_compliance or '',
                    'photos': self.flue_pipe_orientation_photos or []
                },
                'jointOverlap': {
                    'title': 'Joint overlap',
                    'requiredValue': self.joint_overlap_required_value or 'Min 30 mm (1-3/16")',
                    'presentValue': self.joint_overlap_present_value or '',
                    'codeCompliance': self.joint_overlap_code_compliance or '',
                    'photos': self.joint_overlap_photos or []
                },
                'fluePipeSlope': {
                    'title': 'Flue pipe slope',
                    'requiredValue': self.flue_pipe_slope_required_value or 'Min ¼" per foot',
                    'presentValue': self.flue_pipe_slope_present_value or '',
                    'codeCompliance': self.flue_pipe_slope_code_compliance or '',
                    'photos': self.flue_pipe_slope_photos or []
                }
            }
        }


class WoodStoveMasonryFluePipesConnections1(db.Model):
    __tablename__ = 'wood_stove_masonry_flue_pipes_connections_1'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Material section
    material_required_value = db.Column(db.String(255), nullable=True)
    material_present_value = db.Column(db.String(255), nullable=True)
    material_code_compliance = db.Column(db.String(10), nullable=True)
    material_photos = db.Column(db.JSON, nullable=True)

    # Minimum thickness section
    minimum_thickness_required_value = db.Column(db.String(255), nullable=True)
    minimum_thickness_present_value = db.Column(db.String(255), nullable=True)
    minimum_thickness_code_compliance = db.Column(db.String(10), nullable=True)
    minimum_thickness_photos = db.Column(db.JSON, nullable=True)

    # Flue pipe condition section
    flue_pipe_condition_required_value = db.Column(db.String(255), nullable=True)
    flue_pipe_condition_present_value = db.Column(db.String(255), nullable=True)
    flue_pipe_condition_code_compliance = db.Column(db.String(10), nullable=True)
    flue_pipe_condition_photos = db.Column(db.JSON, nullable=True)

    # Pipe shielding present section
    pipe_shielding_present_required_value = db.Column(db.String(255), nullable=True)
    pipe_shielding_present_present_value = db.Column(db.String(255), nullable=True)
    pipe_shielding_present_code_compliance = db.Column(db.String(10), nullable=True)
    pipe_shielding_present_photos = db.Column(db.JSON, nullable=True)

    # Support horizontal present section
    support_horizontal_present_required_value = db.Column(db.String(255), nullable=True)
    support_horizontal_present_present_value = db.Column(db.String(255), nullable=True)
    support_horizontal_present_code_compliance = db.Column(db.String(10), nullable=True)
    support_horizontal_present_photos = db.Column(db.JSON, nullable=True)

    # Barometric damper present section
    barometric_damper_present_description = db.Column(db.String(255), nullable=True)
    barometric_damper_present_required_value = db.Column(db.String(255), nullable=True)
    barometric_damper_present_present_value = db.Column(db.String(255), nullable=True)
    barometric_damper_present_code_compliance = db.Column(db.String(10), nullable=True)
    barometric_damper_present_photos = db.Column(db.JSON, nullable=True)

    # Flue mounted heat reducers present section
    flue_mounted_heat_reducers_present_description = db.Column(db.String(255), nullable=True)
    flue_mounted_heat_reducers_present_required_value = db.Column(db.String(255), nullable=True)
    flue_mounted_heat_reducers_present_present_value = db.Column(db.String(255), nullable=True)
    flue_mounted_heat_reducers_present_code_compliance = db.Column(db.String(10), nullable=True)
    flue_mounted_heat_reducers_present_photos = db.Column(db.JSON, nullable=True)

    # Flue pipe through floors ceilings section
    flue_pipe_through_floors_ceilings_required_value = db.Column(db.String(255), nullable=True)
    flue_pipe_through_floors_ceilings_present_value = db.Column(db.String(255), nullable=True)
    flue_pipe_through_floors_ceilings_code_compliance = db.Column(db.String(10), nullable=True)
    flue_pipe_through_floors_ceilings_photos = db.Column(db.JSON, nullable=True)

    # Connection to factory built chimney section
    connection_to_factory_built_chimney_required_value = db.Column(db.String(255), nullable=True)
    connection_to_factory_built_chimney_present_value = db.Column(db.String(255), nullable=True)
    connection_to_factory_built_chimney_code_compliance = db.Column(db.String(10), nullable=True)
    connection_to_factory_built_chimney_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_flue_pipes_connections_1', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'material': {
                    'title': 'Material - steel or other noncombustible material with a melting point of not less than 1100 °C (2000 °F)',
                    'requiredValue': self.material_required_value or '',
                    'presentValue': self.material_present_value or '',
                    'codeCompliance': self.material_code_compliance or '',
                    'photos': self.material_photos or []
                },
                'minimumThickness': {
                    'title': 'Minimum thickness of flue a pipe',
                    'requiredValue': self.minimum_thickness_required_value or '',
                    'presentValue': self.minimum_thickness_present_value or '',
                    'codeCompliance': self.minimum_thickness_code_compliance or '',
                    'photos': self.minimum_thickness_photos or []
                },
                'fluePipeCondition': {
                    'title': 'Flue pipe condition',
                    'requiredValue': self.flue_pipe_condition_required_value or '',
                    'presentValue': self.flue_pipe_condition_present_value or '',
                    'codeCompliance': self.flue_pipe_condition_code_compliance or '',
                    'photos': self.flue_pipe_condition_photos or []
                },
                'pipeShieldingPresent': {
                    'title': 'Pipe shielding present',
                    'requiredValue': self.pipe_shielding_present_required_value or '',
                    'presentValue': self.pipe_shielding_present_present_value or '',
                    'codeCompliance': self.pipe_shielding_present_code_compliance or '',
                    'photos': self.pipe_shielding_present_photos or []
                },
                'supportHorizontalPresent': {
                    'title': 'Support: horizontal present',
                    'requiredValue': self.support_horizontal_present_required_value or '',
                    'presentValue': self.support_horizontal_present_present_value or '',
                    'codeCompliance': self.support_horizontal_present_code_compliance or '',
                    'photos': self.support_horizontal_present_photos or []
                },
                'barometricDamperPresent': {
                    'title': 'Barometric damper present',
                    'description': self.barometric_damper_present_description or 'CSA B365-17: 4.4.4',
                    'requiredValue': self.barometric_damper_present_required_value or '',
                    'presentValue': self.barometric_damper_present_present_value or '',
                    'codeCompliance': self.barometric_damper_present_code_compliance or '',
                    'photos': self.barometric_damper_present_photos or []
                },
                'flueMountedHeatReducersPresent': {
                    'title': 'Flue-mounted heat reducers present',
                    'description': self.flue_mounted_heat_reducers_present_description or 'CSA B365-17: 4.4.1',
                    'requiredValue': self.flue_mounted_heat_reducers_present_required_value or '',
                    'presentValue': self.flue_mounted_heat_reducers_present_present_value or '',
                    'codeCompliance': self.flue_mounted_heat_reducers_present_code_compliance or '',
                    'photos': self.flue_mounted_heat_reducers_present_photos or []
                },
                'fluePipeThroughFloorsCeilings': {
                    'title': 'Does the flue pipe pass through floors or ceilings?',
                    'requiredValue': self.flue_pipe_through_floors_ceilings_required_value or '',
                    'presentValue': self.flue_pipe_through_floors_ceilings_present_value or '',
                    'codeCompliance': self.flue_pipe_through_floors_ceilings_code_compliance or '',
                    'photos': self.flue_pipe_through_floors_ceilings_photos or []
                },
                'connectionToFactoryBuiltChimney': {
                    'title': 'Connection to factory-built chimney - Mfg. instructions',
                    'requiredValue': self.connection_to_factory_built_chimney_required_value or '',
                    'presentValue': self.connection_to_factory_built_chimney_present_value or '',
                    'codeCompliance': self.connection_to_factory_built_chimney_code_compliance or '',
                    'photos': self.connection_to_factory_built_chimney_photos or []
                }
            }
        }


class WoodStoveMasonryFluePipesConnections2(db.Model):
    __tablename__ = 'wood_stove_masonry_flue_pipes_connections_2'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Chimney flue limitations 1 section
    chimney_flue_limitations_1_title = db.Column(db.String(255), nullable=True)
    chimney_flue_limitations_1_code_reference = db.Column(db.String(255), nullable=True)
    chimney_flue_limitations_1_description = db.Column(db.Text, nullable=True)
    chimney_flue_limitations_1_condition = db.Column(db.Text, nullable=True)
    chimney_flue_limitations_1_comments = db.Column(db.Text, nullable=True)
    chimney_flue_limitations_1_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_flue_limitations_1_photos = db.Column(db.JSON, nullable=True)

    # Chimney flue limitations 2 section
    chimney_flue_limitations_2_title = db.Column(db.String(255), nullable=True)
    chimney_flue_limitations_2_code_reference = db.Column(db.String(255), nullable=True)
    chimney_flue_limitations_2_description = db.Column(db.Text, nullable=True)
    chimney_flue_limitations_2_condition = db.Column(db.Text, nullable=True)
    chimney_flue_limitations_2_comments = db.Column(db.Text, nullable=True)
    chimney_flue_limitations_2_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_flue_limitations_2_photos = db.Column(db.JSON, nullable=True)

    # Connections more than one appliance 1 section
    connections_more_than_one_appliance_1_title = db.Column(db.String(255), nullable=True)
    connections_more_than_one_appliance_1_code_reference = db.Column(db.String(255), nullable=True)
    connections_more_than_one_appliance_1_description = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_1_condition = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_1_comments = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_1_code_compliance = db.Column(db.String(10), nullable=True)
    connections_more_than_one_appliance_1_photos = db.Column(db.JSON, nullable=True)

    # Connections more than one appliance 2 section
    connections_more_than_one_appliance_2_title = db.Column(db.String(255), nullable=True)
    connections_more_than_one_appliance_2_code_reference = db.Column(db.String(255), nullable=True)
    connections_more_than_one_appliance_2_description = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_2_condition = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_2_comments = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_2_code_compliance = db.Column(db.String(10), nullable=True)
    connections_more_than_one_appliance_2_photos = db.Column(db.JSON, nullable=True)

    # Connections more than one appliance 3 section
    connections_more_than_one_appliance_3_title = db.Column(db.String(255), nullable=True)
    connections_more_than_one_appliance_3_code_reference = db.Column(db.String(255), nullable=True)
    connections_more_than_one_appliance_3_description = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_3_condition = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_3_comments = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_3_code_compliance = db.Column(db.String(10), nullable=True)
    connections_more_than_one_appliance_3_photos = db.Column(db.JSON, nullable=True)

    # Connections more than one appliance 4 section
    connections_more_than_one_appliance_4_title = db.Column(db.String(255), nullable=True)
    connections_more_than_one_appliance_4_code_reference = db.Column(db.String(255), nullable=True)
    connections_more_than_one_appliance_4_description = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_4_condition = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_4_comments = db.Column(db.Text, nullable=True)
    connections_more_than_one_appliance_4_code_compliance = db.Column(db.String(10), nullable=True)
    connections_more_than_one_appliance_4_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_flue_pipes_connections_2', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'chimneyFlueLimitations1': {
                    'title': self.chimney_flue_limitations_1_title or 'Chimney Flue Limitations',
                    'codeReference': self.chimney_flue_limitations_1_code_reference or '9.21.2.1.',
                    'description': self.chimney_flue_limitations_1_description or '(1) A chimney flue that serves a fireplace or incinerator shall not serve any other appliance.',
                    'condition': self.chimney_flue_limitations_1_condition or '',
                    'comments': self.chimney_flue_limitations_1_comments or '',
                    'codeCompliance': self.chimney_flue_limitations_1_code_compliance or '',
                    'photos': self.chimney_flue_limitations_1_photos or []
                },
                'chimneyFlueLimitations2': {
                    'title': self.chimney_flue_limitations_2_title or 'Chimney Flue Limitations',
                    'codeReference': self.chimney_flue_limitations_2_code_reference or '9.21.2.1.',
                    'description': self.chimney_flue_limitations_2_description or '(2) A chimney flue that serves a solid-fuel-burning appliance shall not be connected to a natural-gas or propane-fired appliance unless the solid-fuel-burning appliance is certified for such installation and the installation of both appliances meets the requirements of the relevant standards referenced in Article 9.33.5.2. appliance.',
                    'condition': self.chimney_flue_limitations_2_condition or '',
                    'comments': self.chimney_flue_limitations_2_comments or '',
                    'codeCompliance': self.chimney_flue_limitations_2_code_compliance or '',
                    'photos': self.chimney_flue_limitations_2_photos or []
                },
                'connectionsMoreThanOneAppliance1': {
                    'title': self.connections_more_than_one_appliance_1_title or 'Connections of More Than One Appliance',
                    'codeReference': self.connections_more_than_one_appliance_1_code_reference or '9.21.2.2.',
                    'description': self.connections_more_than_one_appliance_1_description or '(1) Except as required by Article 9.21.2.1, where two or more fuel-burning appliances are connected to the same chimney flue, the connections shall be made as described in Sentences (2) to (4) and an adequate draft shall be provided for the connected appliances in conformance with the requirements of the relevant standards listed in Subsection 9.33.10.',
                    'condition': self.connections_more_than_one_appliance_1_condition or '',
                    'comments': self.connections_more_than_one_appliance_1_comments or '',
                    'codeCompliance': self.connections_more_than_one_appliance_1_code_compliance or '',
                    'photos': self.connections_more_than_one_appliance_1_photos or []
                },
                'connectionsMoreThanOneAppliance2': {
                    'title': self.connections_more_than_one_appliance_2_title or 'Connections of More Than One Appliance',
                    'codeReference': self.connections_more_than_one_appliance_2_code_reference or '9.21.2.2.',
                    'description': self.connections_more_than_one_appliance_2_description or '(2) Where 2 or more fuel-burning appliances are connected to the same chimney flue, the appliances shall be located on the same storey.',
                    'condition': self.connections_more_than_one_appliance_2_condition or '',
                    'comments': self.connections_more_than_one_appliance_2_comments or '',
                    'codeCompliance': self.connections_more_than_one_appliance_2_code_compliance or '',
                    'photos': self.connections_more_than_one_appliance_2_photos or []
                },
                'connectionsMoreThanOneAppliance3': {
                    'title': self.connections_more_than_one_appliance_3_title or 'Connections of More Than One Appliance',
                    'codeReference': self.connections_more_than_one_appliance_3_code_reference or '9.21.2.2.',
                    'description': self.connections_more_than_one_appliance_3_description or '(3) The connection referred to in Sentence (2) for a solid-fuel-burning appliance shall be made below connections for appliances burning other fuels.\n(a) conform to Table 9.23.6.2; and\n(b) have a bearing length not less than 90mm (3 1/2").',
                    'condition': self.connections_more_than_one_appliance_3_condition or '',
                    'comments': self.connections_more_than_one_appliance_3_comments or '',
                    'codeCompliance': self.connections_more_than_one_appliance_3_code_compliance or '',
                    'photos': self.connections_more_than_one_appliance_3_photos or []
                },
                'connectionsMoreThanOneAppliance4': {
                    'title': self.connections_more_than_one_appliance_4_title or 'Connections of More Than One Appliance',
                    'codeReference': self.connections_more_than_one_appliance_4_code_reference or '9.21.2.2.',
                    'description': self.connections_more_than_one_appliance_4_description or '(4) The connection referred to in Sentence (2) for a liquid-fuel-burning appliance shall be made below any connections for appliances burning natural gas or propane.\n(a) conform to Table 9.23.6.2; and\n(b) have a bearing length not less than 90mm (3 1/2").',
                    'condition': self.connections_more_than_one_appliance_4_condition or '',
                    'comments': self.connections_more_than_one_appliance_4_comments or '',
                    'codeCompliance': self.connections_more_than_one_appliance_4_code_compliance or '',
                    'photos': self.connections_more_than_one_appliance_4_photos or []
                }
            }
        }


class WoodStoveMasonryWallShieldingFloorProtection(db.Model):
    __tablename__ = 'wood_stove_masonry_wall_shielding_floor_protection'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Shielding ceiling section
    shielding_ceiling_required_value_uncertified = db.Column(db.String(255), nullable=True)
    shielding_ceiling_required_value_certified = db.Column(db.String(255), nullable=True)
    shielding_ceiling_present_value = db.Column(db.String(255), nullable=True)
    shielding_ceiling_code_compliance = db.Column(db.String(10), nullable=True)
    shielding_ceiling_photos = db.Column(db.JSON, nullable=True)

    # Wall shielding rear section
    wall_shielding_rear_required_value_uncertified = db.Column(db.String(255), nullable=True)
    wall_shielding_rear_required_value_certified = db.Column(db.String(255), nullable=True)
    wall_shielding_rear_present_value = db.Column(db.String(255), nullable=True)
    wall_shielding_rear_code_compliance = db.Column(db.String(10), nullable=True)
    wall_shielding_rear_photos = db.Column(db.JSON, nullable=True)

    # Wall shielding right side section
    wall_shielding_right_side_required_value_uncertified = db.Column(db.String(255), nullable=True)
    wall_shielding_right_side_required_value_certified = db.Column(db.String(255), nullable=True)
    wall_shielding_right_side_present_value = db.Column(db.String(255), nullable=True)
    wall_shielding_right_side_code_compliance = db.Column(db.String(10), nullable=True)
    wall_shielding_right_side_photos = db.Column(db.JSON, nullable=True)

    # Wall shielding left side section
    wall_shielding_left_side_required_value_uncertified = db.Column(db.String(255), nullable=True)
    wall_shielding_left_side_required_value_certified = db.Column(db.String(255), nullable=True)
    wall_shielding_left_side_present_value = db.Column(db.String(255), nullable=True)
    wall_shielding_left_side_code_compliance = db.Column(db.String(10), nullable=True)
    wall_shielding_left_side_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('wood_stove_masonry_wall_shielding_floor_protection', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'shieldingCeiling': {
                    'title': 'Shielding ceiling',
                    'requiredValueUncertified': self.shielding_ceiling_required_value_uncertified or '',
                    'requiredValueCertified': self.shielding_ceiling_required_value_certified or '',
                    'presentValue': self.shielding_ceiling_present_value or '',
                    'codeCompliance': self.shielding_ceiling_code_compliance or '',
                    'photos': self.shielding_ceiling_photos or []
                },
                'wallShieldingRear': {
                    'title': 'Wall shielding - rear',
                    'requiredValueUncertified': self.wall_shielding_rear_required_value_uncertified or '',
                    'requiredValueCertified': self.wall_shielding_rear_required_value_certified or '',
                    'presentValue': self.wall_shielding_rear_present_value or '',
                    'codeCompliance': self.wall_shielding_rear_code_compliance or '',
                    'photos': self.wall_shielding_rear_photos or []
                },
                'wallShieldingRightSide': {
                    'title': 'Wall shielding - right side',
                    'requiredValueUncertified': self.wall_shielding_right_side_required_value_uncertified or '',
                    'requiredValueCertified': self.wall_shielding_right_side_required_value_certified or '',
                    'presentValue': self.wall_shielding_right_side_present_value or '',
                    'codeCompliance': self.wall_shielding_right_side_code_compliance or '',
                    'photos': self.wall_shielding_right_side_photos or []
                },
                'wallShieldingLeftSide': {
                    'title': 'Wall shielding - left side',
                    'requiredValueUncertified': self.wall_shielding_left_side_required_value_uncertified or '',
                    'requiredValueCertified': self.wall_shielding_left_side_required_value_certified or '',
                    'presentValue': self.wall_shielding_left_side_present_value or '',
                    'codeCompliance': self.wall_shielding_left_side_code_compliance or '',
                    'photos': self.wall_shielding_left_side_photos or []
                }
            }
        }


class MasonryJointDetails(db.Model):
    __tablename__ = 'masonry_joint_details'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Joints in Chimney Liners section
    joints_in_chimney_liners_condition = db.Column(db.String(255), nullable=True)
    joints_in_chimney_liners_comments = db.Column(db.Text, nullable=True)
    joints_in_chimney_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    joints_in_chimney_liners_photos = db.Column(db.JSON, nullable=True)

    # Installation of Chimney Liners section
    installation_of_chimney_liners_condition = db.Column(db.String(255), nullable=True)
    installation_of_chimney_liners_comments = db.Column(db.Text, nullable=True)
    installation_of_chimney_liners_code_compliance = db.Column(db.String(10), nullable=True)
    installation_of_chimney_liners_photos = db.Column(db.JSON, nullable=True)

    # Spaces between Liners and Surrounding Masonry section
    spaces_between_liners_and_surrounding_masonry_condition = db.Column(db.String(255), nullable=True)
    spaces_between_liners_and_surrounding_masonry_comments = db.Column(db.Text, nullable=True)
    spaces_between_liners_and_surrounding_masonry_code_compliance = db.Column(db.String(10), nullable=True)
    spaces_between_liners_and_surrounding_masonry_photos = db.Column(db.JSON, nullable=True)

    # Mortar for Chimney Liners section
    mortar_for_chimney_liners_condition = db.Column(db.String(255), nullable=True)
    mortar_for_chimney_liners_comments = db.Column(db.Text, nullable=True)
    mortar_for_chimney_liners_code_compliance = db.Column(db.String(10), nullable=True)
    mortar_for_chimney_liners_photos = db.Column(db.JSON, nullable=True)

    # Extension of Chimney Liners section
    extension_of_chimney_liners_condition = db.Column(db.String(255), nullable=True)
    extension_of_chimney_liners_comments = db.Column(db.Text, nullable=True)
    extension_of_chimney_liners_code_compliance = db.Column(db.String(10), nullable=True)
    extension_of_chimney_liners_photos = db.Column(db.JSON, nullable=True)

    # Height of Chimney Flues section
    height_of_chimney_flues_condition = db.Column(db.String(255), nullable=True)
    height_of_chimney_flues_comments = db.Column(db.Text, nullable=True)
    height_of_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)
    height_of_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_joint_details', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'jointsInChimneyLiners': {
                    'condition': self.joints_in_chimney_liners_condition or '',
                    'comments': self.joints_in_chimney_liners_comments or '',
                    'codeCompliance': self.joints_in_chimney_liners_code_compliance or '',
                    'photos': self.joints_in_chimney_liners_photos or []
                },
                'installationOfChimneyLiners': {
                    'condition': self.installation_of_chimney_liners_condition or '',
                    'comments': self.installation_of_chimney_liners_comments or '',
                    'codeCompliance': self.installation_of_chimney_liners_code_compliance or '',
                    'photos': self.installation_of_chimney_liners_photos or []
                },
                'spacesBetweenLinersAndSurroundingMasonry': {
                    'condition': self.spaces_between_liners_and_surrounding_masonry_condition or '',
                    'comments': self.spaces_between_liners_and_surrounding_masonry_comments or '',
                    'codeCompliance': self.spaces_between_liners_and_surrounding_masonry_code_compliance or '',
                    'photos': self.spaces_between_liners_and_surrounding_masonry_photos or []
                },
                'mortarForChimneyLiners': {
                    'condition': self.mortar_for_chimney_liners_condition or '',
                    'comments': self.mortar_for_chimney_liners_comments or '',
                    'codeCompliance': self.mortar_for_chimney_liners_code_compliance or '',
                    'photos': self.mortar_for_chimney_liners_photos or []
                },
                'extensionOfChimneyLiners': {
                    'condition': self.extension_of_chimney_liners_condition or '',
                    'comments': self.extension_of_chimney_liners_comments or '',
                    'codeCompliance': self.extension_of_chimney_liners_code_compliance or '',
                    'photos': self.extension_of_chimney_liners_photos or []
                },
                'heightOfChimneyFlues': {
                    'condition': self.height_of_chimney_flues_condition or '',
                    'comments': self.height_of_chimney_flues_comments or '',
                    'codeCompliance': self.height_of_chimney_flues_code_compliance or '',
                    'photos': self.height_of_chimney_flues_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryChimneyStabilityCaps(db.Model):
    __tablename__ = 'masonry_chimney_stability_caps'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Lateral Stability 1 section
    lateral_stability_1_condition = db.Column(db.String(255), nullable=True)
    lateral_stability_1_comments = db.Column(db.Text, nullable=True)
    lateral_stability_1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    lateral_stability_1_photos = db.Column(db.JSON, nullable=True)

    # Lateral Stability 2 section
    lateral_stability_2_condition = db.Column(db.String(255), nullable=True)
    lateral_stability_2_comments = db.Column(db.Text, nullable=True)
    lateral_stability_2_code_compliance = db.Column(db.String(10), nullable=True)
    lateral_stability_2_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 1 section
    chimney_caps_1_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_1_comments = db.Column(db.Text, nullable=True)
    chimney_caps_1_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_1_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 2 section
    chimney_caps_2_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_2_comments = db.Column(db.Text, nullable=True)
    chimney_caps_2_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_2_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 3 section
    chimney_caps_3_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_3_comments = db.Column(db.Text, nullable=True)
    chimney_caps_3_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_3_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 4 section
    chimney_caps_4_condition = db.Column(db.String(255), nullable=True)
    chimney_caps_4_comments = db.Column(db.Text, nullable=True)
    chimney_caps_4_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_4_photos = db.Column(db.JSON, nullable=True)

    # Flashing section
    flashing_condition = db.Column(db.String(255), nullable=True)
    flashing_comments = db.Column(db.Text, nullable=True)
    flashing_code_compliance = db.Column(db.String(10), nullable=True)
    flashing_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_chimney_stability_caps', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'lateralStability1': {
                    'condition': self.lateral_stability_1_condition or '',
                    'comments': self.lateral_stability_1_comments or '',
                    'codeCompliance': self.lateral_stability_1_code_compliance or '',
                    'photos': self.lateral_stability_1_photos or []
                },
                'lateralStability2': {
                    'condition': self.lateral_stability_2_condition or '',
                    'comments': self.lateral_stability_2_comments or '',
                    'codeCompliance': self.lateral_stability_2_code_compliance or '',
                    'photos': self.lateral_stability_2_photos or []
                },
                'chimneyCaps1': {
                    'condition': self.chimney_caps_1_condition or '',
                    'comments': self.chimney_caps_1_comments or '',
                    'codeCompliance': self.chimney_caps_1_code_compliance or '',
                    'photos': self.chimney_caps_1_photos or []
                },
                'chimneyCaps2': {
                    'condition': self.chimney_caps_2_condition or '',
                    'comments': self.chimney_caps_2_comments or '',
                    'codeCompliance': self.chimney_caps_2_code_compliance or '',
                    'photos': self.chimney_caps_2_photos or []
                },
                'chimneyCaps3': {
                    'condition': self.chimney_caps_3_condition or '',
                    'comments': self.chimney_caps_3_comments or '',
                    'codeCompliance': self.chimney_caps_3_code_compliance or '',
                    'photos': self.chimney_caps_3_photos or []
                },
                'chimneyCaps4': {
                    'condition': self.chimney_caps_4_condition or '',
                    'comments': self.chimney_caps_4_comments or '',
                    'codeCompliance': self.chimney_caps_4_code_compliance or '',
                    'photos': self.chimney_caps_4_photos or []
                },
                'flashing': {
                    'condition': self.flashing_condition or '',
                    'comments': self.flashing_comments or '',
                    'codeCompliance': self.flashing_code_compliance or '',
                    'photos': self.flashing_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryClearancesSupports(db.Model):
    __tablename__ = 'masonry_clearances_supports'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Clearance from Combustible Materials 1 section
    clearance_combustible_1_condition = db.Column(db.String(255), nullable=True)
    clearance_combustible_1_comments = db.Column(db.Text, nullable=True)
    clearance_combustible_1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearance_combustible_1_photos = db.Column(db.JSON, nullable=True)

    # Clearance from Combustible Materials 2 section
    clearance_combustible_2_condition = db.Column(db.String(255), nullable=True)
    clearance_combustible_2_comments = db.Column(db.Text, nullable=True)
    clearance_combustible_2_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_combustible_2_photos = db.Column(db.JSON, nullable=True)

    # Sealing of Spaces section
    sealing_spaces_condition = db.Column(db.String(255), nullable=True)
    sealing_spaces_comments = db.Column(db.Text, nullable=True)
    sealing_spaces_code_compliance = db.Column(db.String(10), nullable=True)
    sealing_spaces_photos = db.Column(db.JSON, nullable=True)

    # Support of Joists or Beams section
    support_joists_beams_condition = db.Column(db.String(255), nullable=True)
    support_joists_beams_comments = db.Column(db.Text, nullable=True)
    support_joists_beams_code_compliance = db.Column(db.String(10), nullable=True)
    support_joists_beams_photos = db.Column(db.JSON, nullable=True)

    # Inclined Chimney Flues section
    inclined_chimney_flues_condition = db.Column(db.String(255), nullable=True)
    inclined_chimney_flues_comments = db.Column(db.Text, nullable=True)
    inclined_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)
    inclined_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    # Intersection of Shingle Roofs and Masonry section
    intersection_shingle_roofs_condition = db.Column(db.String(255), nullable=True)
    intersection_shingle_roofs_comments = db.Column(db.Text, nullable=True)
    intersection_shingle_roofs_code_compliance = db.Column(db.String(10), nullable=True)
    intersection_shingle_roofs_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_clearances_supports', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'clearanceCombustible1': {
                    'condition': self.clearance_combustible_1_condition or '',
                    'comments': self.clearance_combustible_1_comments or '',
                    'codeCompliance': self.clearance_combustible_1_code_compliance or '',
                    'photos': self.clearance_combustible_1_photos or []
                },
                'clearanceCombustible2': {
                    'condition': self.clearance_combustible_2_condition or '',
                    'comments': self.clearance_combustible_2_comments or '',
                    'codeCompliance': self.clearance_combustible_2_code_compliance or '',
                    'photos': self.clearance_combustible_2_photos or []
                },
                'sealingSpaces': {
                    'condition': self.sealing_spaces_condition or '',
                    'comments': self.sealing_spaces_comments or '',
                    'codeCompliance': self.sealing_spaces_code_compliance or '',
                    'photos': self.sealing_spaces_photos or []
                },
                'supportJoistsBeams': {
                    'condition': self.support_joists_beams_condition or '',
                    'comments': self.support_joists_beams_comments or '',
                    'codeCompliance': self.support_joists_beams_code_compliance or '',
                    'photos': self.support_joists_beams_photos or []
                },
                'inclinedChimneyFlues': {
                    'condition': self.inclined_chimney_flues_condition or '',
                    'comments': self.inclined_chimney_flues_comments or '',
                    'codeCompliance': self.inclined_chimney_flues_code_compliance or '',
                    'photos': self.inclined_chimney_flues_photos or []
                },
                'intersectionShingleRoofs': {
                    'condition': self.intersection_shingle_roofs_condition or '',
                    'comments': self.intersection_shingle_roofs_comments or '',
                    'codeCompliance': self.intersection_shingle_roofs_code_compliance or '',
                    'photos': self.intersection_shingle_roofs_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryChimneySaddlesFireCode(db.Model):
    __tablename__ = 'masonry_chimney_saddles_fire_code'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Chimney Saddles section
    chimney_saddles_condition = db.Column(db.String(255), nullable=True)
    chimney_saddles_comments = db.Column(db.Text, nullable=True)
    chimney_saddles_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    chimney_saddles_photos = db.Column(db.JSON, nullable=True)

    # Fire Code Inspection section
    fire_code_inspection_condition = db.Column(db.String(255), nullable=True)
    fire_code_inspection_comments = db.Column(db.Text, nullable=True)
    fire_code_inspection_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_inspection_photos = db.Column(db.JSON, nullable=True)

    # Fire Code Cleaning section
    fire_code_cleaning_condition = db.Column(db.String(255), nullable=True)
    fire_code_cleaning_comments = db.Column(db.Text, nullable=True)
    fire_code_cleaning_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_cleaning_photos = db.Column(db.JSON, nullable=True)

    # Fire Code Structural section
    fire_code_structural_condition = db.Column(db.String(255), nullable=True)
    fire_code_structural_comments = db.Column(db.Text, nullable=True)
    fire_code_structural_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_structural_photos = db.Column(db.JSON, nullable=True)

    # Fire Code Openings section
    fire_code_openings_condition = db.Column(db.String(255), nullable=True)
    fire_code_openings_comments = db.Column(db.Text, nullable=True)
    fire_code_openings_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_openings_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_chimney_saddles_fire_code', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'chimneySaddles': {
                    'condition': self.chimney_saddles_condition or '',
                    'comments': self.chimney_saddles_comments or '',
                    'codeCompliance': self.chimney_saddles_code_compliance or '',
                    'photos': self.chimney_saddles_photos or []
                },
                'fireCodeInspection': {
                    'condition': self.fire_code_inspection_condition or '',
                    'comments': self.fire_code_inspection_comments or '',
                    'codeCompliance': self.fire_code_inspection_code_compliance or '',
                    'photos': self.fire_code_inspection_photos or []
                },
                'fireCodeCleaning': {
                    'condition': self.fire_code_cleaning_condition or '',
                    'comments': self.fire_code_cleaning_comments or '',
                    'codeCompliance': self.fire_code_cleaning_code_compliance or '',
                    'photos': self.fire_code_cleaning_photos or []
                },
                'fireCodeStructural': {
                    'condition': self.fire_code_structural_condition or '',
                    'comments': self.fire_code_structural_comments or '',
                    'codeCompliance': self.fire_code_structural_code_compliance or '',
                    'photos': self.fire_code_structural_photos or []
                },
                'fireCodeOpenings': {
                    'condition': self.fire_code_openings_condition or '',
                    'comments': self.fire_code_openings_comments or '',
                    'codeCompliance': self.fire_code_openings_code_compliance or '',
                    'photos': self.fire_code_openings_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MasonryCOAlarms(db.Model):
    __tablename__ = 'masonry_co_alarms'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Question 1: BCBC CO Alarm section
    question1_required_value = db.Column(db.String(255), nullable=True)
    question1_present_value = db.Column(db.String(10), nullable=True)  # yes/no
    question1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/na
    question1_photos = db.Column(db.JSON, nullable=True)

    # Question 2: NBC/ABC CO Alarm section
    question2_required_value = db.Column(db.String(255), nullable=True)
    question2_present_value = db.Column(db.String(10), nullable=True)  # yes/no
    question2_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/na
    question2_photos = db.Column(db.JSON, nullable=True)

    # Question 3: OBC CO Alarm section
    question3_required_value = db.Column(db.String(255), nullable=True)
    question3_present_value = db.Column(db.String(10), nullable=True)  # yes/no
    question3_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/na
    question3_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('masonry_co_alarms', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'question1': {
                    'requiredValue': self.question1_required_value or '',
                    'presentValue': self.question1_present_value or '',
                    'codeCompliance': self.question1_code_compliance or '',
                    'photos': self.question1_photos or []
                },
                'question2': {
                    'requiredValue': self.question2_required_value or '',
                    'presentValue': self.question2_present_value or '',
                    'codeCompliance': self.question2_code_compliance or '',
                    'photos': self.question2_photos or []
                },
                'question3': {
                    'requiredValue': self.question3_required_value or '',
                    'presentValue': self.question3_present_value or '',
                    'codeCompliance': self.question3_code_compliance or '',
                    'photos': self.question3_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertChimneyLiners(db.Model):
    __tablename__ = 'pellet_insert_chimney_liners'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Lining Materials section
    lining_materials_condition = db.Column(db.Text, nullable=True)
    lining_materials_comments = db.Column(db.Text, nullable=True)
    lining_materials_code_compliance = db.Column(db.String(10), nullable=True)
    lining_materials_photos = db.Column(db.JSON, nullable=True)

    # Clay Liners section
    clay_liners_condition = db.Column(db.Text, nullable=True)
    clay_liners_comments = db.Column(db.Text, nullable=True)
    clay_liners_code_compliance = db.Column(db.String(10), nullable=True)
    clay_liners_photos = db.Column(db.JSON, nullable=True)

    # Inclined Chimney Flues section
    inclined_chimney_flues_condition = db.Column(db.Text, nullable=True)
    inclined_chimney_flues_comments = db.Column(db.Text, nullable=True)
    inclined_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)
    inclined_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners section
    firebrick_liners_condition = db.Column(db.Text, nullable=True)
    firebrick_liners_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_code_compliance = db.Column(db.String(10), nullable=True)
    firebrick_liners_photos = db.Column(db.JSON, nullable=True)

    # Concrete Liners section
    concrete_liners_condition = db.Column(db.Text, nullable=True)
    concrete_liners_comments = db.Column(db.Text, nullable=True)
    concrete_liners_code_compliance = db.Column(db.String(10), nullable=True)
    concrete_liners_photos = db.Column(db.JSON, nullable=True)

    # Metal Liners section
    metal_liners_condition = db.Column(db.Text, nullable=True)
    metal_liners_comments = db.Column(db.Text, nullable=True)
    metal_liners_code_compliance = db.Column(db.String(10), nullable=True)
    metal_liners_photos = db.Column(db.JSON, nullable=True)

    # Oval Chimney Flues section
    oval_chimney_flues_condition = db.Column(db.Text, nullable=True)
    oval_chimney_flues_comments = db.Column(db.Text, nullable=True)
    oval_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)
    oval_chimney_flues_photos = db.Column(db.JSON, nullable=True)

    # Separation of Flue Liners section
    separation_of_flue_liners_condition = db.Column(db.Text, nullable=True)
    separation_of_flue_liners_comments = db.Column(db.Text, nullable=True)
    separation_of_flue_liners_code_compliance = db.Column(db.String(10), nullable=True)
    separation_of_flue_liners_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_chimney_liners', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'liningMaterials': {
                    'condition': self.lining_materials_condition or '',
                    'comments': self.lining_materials_comments or '',
                    'codeCompliance': self.lining_materials_code_compliance or '',
                    'photos': self.lining_materials_photos or []
                },
                'clayLiners': {
                    'condition': self.clay_liners_condition or '',
                    'comments': self.clay_liners_comments or '',
                    'codeCompliance': self.clay_liners_code_compliance or '',
                    'photos': self.clay_liners_photos or []
                },
                'inclinedChimneyFlues': {
                    'condition': self.inclined_chimney_flues_condition or '',
                    'comments': self.inclined_chimney_flues_comments or '',
                    'codeCompliance': self.inclined_chimney_flues_code_compliance or '',
                    'photos': self.inclined_chimney_flues_photos or []
                },
                'firebrickLiners': {
                    'condition': self.firebrick_liners_condition or '',
                    'comments': self.firebrick_liners_comments or '',
                    'codeCompliance': self.firebrick_liners_code_compliance or '',
                    'photos': self.firebrick_liners_photos or []
                },
                'concreteLiners': {
                    'condition': self.concrete_liners_condition or '',
                    'comments': self.concrete_liners_comments or '',
                    'codeCompliance': self.concrete_liners_code_compliance or '',
                    'photos': self.concrete_liners_photos or []
                },
                'metalLiners': {
                    'condition': self.metal_liners_condition or '',
                    'comments': self.metal_liners_comments or '',
                    'codeCompliance': self.metal_liners_code_compliance or '',
                    'photos': self.metal_liners_photos or []
                },
                'ovalChimneyFlues': {
                    'condition': self.oval_chimney_flues_condition or '',
                    'comments': self.oval_chimney_flues_comments or '',
                    'codeCompliance': self.oval_chimney_flues_code_compliance or '',
                    'photos': self.oval_chimney_flues_photos or []
                },
                'separationOfFlueLiners': {
                    'condition': self.separation_of_flue_liners_condition or '',
                    'comments': self.separation_of_flue_liners_comments or '',
                    'codeCompliance': self.separation_of_flue_liners_code_compliance or '',
                    'photos': self.separation_of_flue_liners_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertChimneySaddlesFireCode(db.Model):
    __tablename__ = 'pellet_insert_chimney_saddles_fire_code'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Chimney Saddles section
    chimney_saddles_condition = db.Column(db.Text, nullable=True)
    chimney_saddles_comments = db.Column(db.Text, nullable=True)
    chimney_saddles_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_saddles_photos = db.Column(db.JSON, nullable=True)

    # Fire Code 1 section
    fire_code_1_condition = db.Column(db.Text, nullable=True)
    fire_code_1_comments = db.Column(db.Text, nullable=True)
    fire_code_1_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_1_photos = db.Column(db.JSON, nullable=True)

    # Fire Code 2 section
    fire_code_2_condition = db.Column(db.Text, nullable=True)
    fire_code_2_comments = db.Column(db.Text, nullable=True)
    fire_code_2_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_2_photos = db.Column(db.JSON, nullable=True)

    # Fire Code 3 section
    fire_code_3_condition = db.Column(db.Text, nullable=True)
    fire_code_3_comments = db.Column(db.Text, nullable=True)
    fire_code_3_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_3_photos = db.Column(db.JSON, nullable=True)

    # Fire Code 4 section
    fire_code_4_condition = db.Column(db.Text, nullable=True)
    fire_code_4_comments = db.Column(db.Text, nullable=True)
    fire_code_4_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_4_photos = db.Column(db.JSON, nullable=True)

    # Fire Code 5 section
    fire_code_5_condition = db.Column(db.Text, nullable=True)
    fire_code_5_comments = db.Column(db.Text, nullable=True)
    fire_code_5_code_compliance = db.Column(db.String(10), nullable=True)
    fire_code_5_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_chimney_saddles_fire_code', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'chimneySaddles': {
                    'condition': self.chimney_saddles_condition or '',
                    'comments': self.chimney_saddles_comments or '',
                    'codeCompliance': self.chimney_saddles_code_compliance or '',
                    'photos': self.chimney_saddles_photos or []
                },
                'fireCode1': {
                    'condition': self.fire_code_1_condition or '',
                    'comments': self.fire_code_1_comments or '',
                    'codeCompliance': self.fire_code_1_code_compliance or '',
                    'photos': self.fire_code_1_photos or []
                },
                'fireCode2': {
                    'condition': self.fire_code_2_condition or '',
                    'comments': self.fire_code_2_comments or '',
                    'codeCompliance': self.fire_code_2_code_compliance or '',
                    'photos': self.fire_code_2_photos or []
                },
                'fireCode3': {
                    'condition': self.fire_code_3_condition or '',
                    'comments': self.fire_code_3_comments or '',
                    'codeCompliance': self.fire_code_3_code_compliance or '',
                    'photos': self.fire_code_3_photos or []
                },
                'fireCode4': {
                    'condition': self.fire_code_4_condition or '',
                    'comments': self.fire_code_4_comments or '',
                    'codeCompliance': self.fire_code_4_code_compliance or '',
                    'photos': self.fire_code_4_photos or []
                },
                'fireCode5': {
                    'condition': self.fire_code_5_condition or '',
                    'comments': self.fire_code_5_comments or '',
                    'codeCompliance': self.fire_code_5_code_compliance or '',
                    'photos': self.fire_code_5_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertChimneySpecification(db.Model):
    __tablename__ = 'pellet_insert_chimney_specifications'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Inspection details
    inspection_discussed = db.Column(db.String(10), nullable=True)  # yes/no
    building_permits_available = db.Column(db.String(10), nullable=True)  # yes/no
    time_of_day = db.Column(db.String(20), nullable=True)
    weather_conditions = db.Column(db.Text, nullable=True)
    roofing_type_material = db.Column(db.String(200), nullable=True)
    roof_accessed = db.Column(db.String(10), nullable=True)  # yes/no
    attic_accessed = db.Column(db.String(10), nullable=True)  # yes/no

    # Construction details
    chimney_constructed_with_building = db.Column(db.String(20), nullable=True)  # yes/no/unknown
    approximate_age = db.Column(db.String(100), nullable=True)
    chimney_shell = db.Column(db.String(50), nullable=True)  # brick/block/stone/others
    rain_cap = db.Column(db.String(30), nullable=True)  # yes/no/with-screening/without-screening
    chimney_location = db.Column(db.String(20), nullable=True)  # interior/exterior
    height_from_firebox_floor = db.Column(db.String(50), nullable=True)
    flue_size = db.Column(db.String(50), nullable=True)
    size_of_flue = db.Column(db.String(100), nullable=True)
    material_of_flue = db.Column(db.String(100), nullable=True)
    chimney_lined_with = db.Column(db.String(50), nullable=True)  # clay-tile/pumice/stainless-steel-flex/stainless-steel-rigid/no-liner/insulated/uti

    # Installation details
    chimney_installed_by = db.Column(db.String(200), nullable=True)
    chimney_installed_by_unknown = db.Column(db.Boolean, default=False)
    chimney_installation_date = db.Column(db.String(50), nullable=True)

    # Fireplace details
    fireplace_location = db.Column(db.String(20), nullable=True)  # interior/exterior
    installed_in = db.Column(db.String(50), nullable=True)  # residence/modular-home/mobile/home-manufactured/alcove/garage/other
    fireplace_location_building = db.Column(db.String(50), nullable=True)  # basement/main-floor/other
    other_location_specify = db.Column(db.String(200), nullable=True)
    fireplace_installed_by = db.Column(db.String(200), nullable=True)
    fireplace_installed_by_unknown = db.Column(db.Boolean, default=False)
    fireplace_installation_date = db.Column(db.String(50), nullable=True)
    fireplace_location_final = db.Column(db.String(20), nullable=True)  # interior/exterior
    shares_venting_system = db.Column(db.String(10), nullable=True)  # yes/no

    # Assessment details
    comments_condition = db.Column(db.Text, nullable=True)
    suitable = db.Column(db.String(10), nullable=True)  # yes/no

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_chimney_specifications', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'inspectionDiscussed': self.inspection_discussed or '',
                'buildingPermitsAvailable': self.building_permits_available or '',
                'timeOfDay': self.time_of_day or '',
                'weatherConditions': self.weather_conditions or '',
                'roofingTypeMaterial': self.roofing_type_material or '',
                'roofAccessed': self.roof_accessed or '',
                'atticAccessed': self.attic_accessed or '',
                'chimneyConstructedWithBuilding': self.chimney_constructed_with_building or '',
                'approximateAge': self.approximate_age or '',
                'chimneyShell': self.chimney_shell or '',
                'rainCap': self.rain_cap or '',
                'chimneyLocation': self.chimney_location or '',
                'heightFromFireboxFloor': self.height_from_firebox_floor or '',
                'flueSize': self.flue_size or '',
                'sizeOfFlue': self.size_of_flue or '',
                'materialOfFlue': self.material_of_flue or '',
                'chimneyLinedWith': self.chimney_lined_with or '',
                'chimneyInstalledBy': self.chimney_installed_by or '',
                'chimneyInstalledByUnknown': self.chimney_installed_by_unknown or False,
                'date': self.chimney_installation_date or '',
                'fireplaceLocation': self.fireplace_location or '',
                'installedIn': self.installed_in or '',
                'fireplaceLocation2': self.fireplace_location_building or '',
                'othersSpecify': self.other_location_specify or '',
                'fireplaceInstalledBy': self.fireplace_installed_by or '',
                'fireplaceInstalledByUnknown': self.fireplace_installed_by_unknown or False,
                'date2': self.fireplace_installation_date or '',
                'fireplaceLocation3': self.fireplace_location_final or '',
                'sharesVentingSystem': self.shares_venting_system or '',
                'commentsCondition': self.comments_condition or '',
                'suitable': self.suitable or ''
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertChimneyStabilityCaps(db.Model):
    __tablename__ = 'pellet_insert_chimney_stability_caps'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Height of Chimney Flues section
    height_of_chimney_flues_condition = db.Column(db.Text, nullable=True)
    height_of_chimney_flues_comments = db.Column(db.Text, nullable=True)
    height_of_chimney_flues_code_compliance = db.Column(db.String(10), nullable=True)
    height_of_chimney_flues_photos = db.Column(db.JSON, nullable=True)
    height_of_chimney_flues_required_height = db.Column(db.String(100), nullable=True)
    height_of_chimney_flues_present_height = db.Column(db.String(100), nullable=True)
    height_of_chimney_flues_required_width = db.Column(db.String(100), nullable=True)
    height_of_chimney_flues_present_width = db.Column(db.String(100), nullable=True)
    height_of_chimney_flues_required_vertical = db.Column(db.String(100), nullable=True)
    height_of_chimney_flues_present_vertical = db.Column(db.String(100), nullable=True)

    # Lateral Stability section
    lateral_stability_condition = db.Column(db.Text, nullable=True)
    lateral_stability_comments = db.Column(db.Text, nullable=True)
    lateral_stability_code_compliance = db.Column(db.String(10), nullable=True)
    lateral_stability_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 1 section
    chimney_caps_1_condition = db.Column(db.Text, nullable=True)
    chimney_caps_1_comments = db.Column(db.Text, nullable=True)
    chimney_caps_1_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_1_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 2 section
    chimney_caps_2_condition = db.Column(db.Text, nullable=True)
    chimney_caps_2_comments = db.Column(db.Text, nullable=True)
    chimney_caps_2_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_2_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 3 section
    chimney_caps_3_condition = db.Column(db.Text, nullable=True)
    chimney_caps_3_comments = db.Column(db.Text, nullable=True)
    chimney_caps_3_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_3_photos = db.Column(db.JSON, nullable=True)

    # Chimney Caps 4 section
    chimney_caps_4_condition = db.Column(db.Text, nullable=True)
    chimney_caps_4_comments = db.Column(db.Text, nullable=True)
    chimney_caps_4_code_compliance = db.Column(db.String(10), nullable=True)
    chimney_caps_4_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_chimney_stability_caps', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'heightOfChimneyFlues': {
                    'condition': self.height_of_chimney_flues_condition or '',
                    'comments': self.height_of_chimney_flues_comments or '',
                    'codeCompliance': self.height_of_chimney_flues_code_compliance or '',
                    'photos': self.height_of_chimney_flues_photos or [],
                    'requiredHeight': self.height_of_chimney_flues_required_height or '',
                    'presentHeight': self.height_of_chimney_flues_present_height or '',
                    'requiredWidth': self.height_of_chimney_flues_required_width or '',
                    'presentWidth': self.height_of_chimney_flues_present_width or '',
                    'requiredVertical': self.height_of_chimney_flues_required_vertical or '',
                    'presentVertical': self.height_of_chimney_flues_present_vertical or ''
                },
                'lateralStability': {
                    'condition': self.lateral_stability_condition or '',
                    'comments': self.lateral_stability_comments or '',
                    'codeCompliance': self.lateral_stability_code_compliance or '',
                    'photos': self.lateral_stability_photos or []
                },
                'chimneyCaps1': {
                    'condition': self.chimney_caps_1_condition or '',
                    'comments': self.chimney_caps_1_comments or '',
                    'codeCompliance': self.chimney_caps_1_code_compliance or '',
                    'photos': self.chimney_caps_1_photos or []
                },
                'chimneyCaps2': {
                    'condition': self.chimney_caps_2_condition or '',
                    'comments': self.chimney_caps_2_comments or '',
                    'codeCompliance': self.chimney_caps_2_code_compliance or '',
                    'photos': self.chimney_caps_2_photos or []
                },
                'chimneyCaps3': {
                    'condition': self.chimney_caps_3_condition or '',
                    'comments': self.chimney_caps_3_comments or '',
                    'codeCompliance': self.chimney_caps_3_code_compliance or '',
                    'photos': self.chimney_caps_3_photos or []
                },
                'chimneyCaps4': {
                    'condition': self.chimney_caps_4_condition or '',
                    'comments': self.chimney_caps_4_comments or '',
                    'codeCompliance': self.chimney_caps_4_code_compliance or '',
                    'photos': self.chimney_caps_4_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertChimneySupportConnection(db.Model):
    __tablename__ = 'pellet_insert_chimney_support_connection'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Electrical Outlet section
    electrical_outlet_required_value_uncertified = db.Column(db.String(255), nullable=True)
    electrical_outlet_required_value_certified = db.Column(db.String(255), nullable=True)
    electrical_outlet_present_value = db.Column(db.String(10), nullable=True)  # yes/no
    electrical_outlet_code_compliance = db.Column(db.String(10), nullable=True)
    electrical_outlet_photos = db.Column(db.JSON, nullable=True)

    # Fireplace Modified section
    fireplace_modified_required_value_uncertified = db.Column(db.String(255), nullable=True)
    fireplace_modified_required_value_certified = db.Column(db.String(255), nullable=True)
    fireplace_modified_present_value = db.Column(db.String(10), nullable=True)  # yes/no
    fireplace_modified_code_compliance = db.Column(db.String(10), nullable=True)
    fireplace_modified_photos = db.Column(db.JSON, nullable=True)

    # CO Alarm BCBC section
    co_alarm_bcbc_required_value = db.Column(db.String(255), nullable=True)
    co_alarm_bcbc_present_value = db.Column(db.String(10), nullable=True)  # yes/no
    co_alarm_bcbc_code_compliance = db.Column(db.String(10), nullable=True)
    co_alarm_bcbc_photos = db.Column(db.JSON, nullable=True)

    # CO Alarm NBC section
    co_alarm_nbc_required_value = db.Column(db.String(255), nullable=True)
    co_alarm_nbc_present_value = db.Column(db.String(10), nullable=True)  # yes/no
    co_alarm_nbc_code_compliance = db.Column(db.String(10), nullable=True)
    co_alarm_nbc_photos = db.Column(db.JSON, nullable=True)

    # CO Alarm OBC section
    co_alarm_obc_required_value = db.Column(db.String(255), nullable=True)
    co_alarm_obc_present_value = db.Column(db.String(10), nullable=True)  # yes/no
    co_alarm_obc_code_compliance = db.Column(db.String(10), nullable=True)
    co_alarm_obc_photos = db.Column(db.JSON, nullable=True)

    # Condition section
    condition_required_value_uncertified = db.Column(db.String(255), nullable=True)
    condition_required_value_certified = db.Column(db.String(255), nullable=True)
    condition_present_value = db.Column(db.Text, nullable=True)
    condition_code_compliance = db.Column(db.String(10), nullable=True)
    condition_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_chimney_support_connection', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'electricalOutlet': {
                    'requiredValueUncertified': self.electrical_outlet_required_value_uncertified or '',
                    'requiredValueCertified': self.electrical_outlet_required_value_certified or '',
                    'presentValue': self.electrical_outlet_present_value or '',
                    'codeCompliance': self.electrical_outlet_code_compliance or '',
                    'photos': self.electrical_outlet_photos or []
                },
                'fireplaceModified': {
                    'requiredValueUncertified': self.fireplace_modified_required_value_uncertified or '',
                    'requiredValueCertified': self.fireplace_modified_required_value_certified or '',
                    'presentValue': self.fireplace_modified_present_value or '',
                    'codeCompliance': self.fireplace_modified_code_compliance or '',
                    'photos': self.fireplace_modified_photos or []
                },
                'coAlarmBCBC': {
                    'requiredValue': self.co_alarm_bcbc_required_value or '',
                    'presentValue': self.co_alarm_bcbc_present_value or '',
                    'codeCompliance': self.co_alarm_bcbc_code_compliance or '',
                    'photos': self.co_alarm_bcbc_photos or []
                },
                'coAlarmNBC': {
                    'requiredValue': self.co_alarm_nbc_required_value or '',
                    'presentValue': self.co_alarm_nbc_present_value or '',
                    'codeCompliance': self.co_alarm_nbc_code_compliance or '',
                    'photos': self.co_alarm_nbc_photos or []
                },
                'coAlarmOBC': {
                    'requiredValue': self.co_alarm_obc_required_value or '',
                    'presentValue': self.co_alarm_obc_present_value or '',
                    'codeCompliance': self.co_alarm_obc_code_compliance or '',
                    'photos': self.co_alarm_obc_photos or []
                },
                'condition': {
                    'requiredValueUncertified': self.condition_required_value_uncertified or '',
                    'requiredValueCertified': self.condition_required_value_certified or '',
                    'presentValue': self.condition_present_value or '',
                    'codeCompliance': self.condition_code_compliance or '',
                    'photos': self.condition_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertChimneySupports(db.Model):
    __tablename__ = 'pellet_insert_chimney_supports'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Flashing section
    flashing_condition = db.Column(db.Text, nullable=True)
    flashing_comments = db.Column(db.Text, nullable=True)
    flashing_code_compliance = db.Column(db.String(10), nullable=True)
    flashing_photos = db.Column(db.JSON, nullable=True)

    # Clearance from Combustible Materials 1 section
    clearance_from_combustible_materials_1_condition = db.Column(db.Text, nullable=True)
    clearance_from_combustible_materials_1_comments = db.Column(db.Text, nullable=True)
    clearance_from_combustible_materials_1_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_from_combustible_materials_1_photos = db.Column(db.JSON, nullable=True)

    # Clearance from Combustible Materials 2 section
    clearance_from_combustible_materials_2_condition = db.Column(db.Text, nullable=True)
    clearance_from_combustible_materials_2_comments = db.Column(db.Text, nullable=True)
    clearance_from_combustible_materials_2_code_compliance = db.Column(db.String(10), nullable=True)
    clearance_from_combustible_materials_2_photos = db.Column(db.JSON, nullable=True)

    # Sealing of Spaces section
    sealing_of_spaces_condition = db.Column(db.Text, nullable=True)
    sealing_of_spaces_comments = db.Column(db.Text, nullable=True)
    sealing_of_spaces_code_compliance = db.Column(db.String(10), nullable=True)
    sealing_of_spaces_photos = db.Column(db.JSON, nullable=True)

    # Support of Joists or Beams section
    support_of_joists_or_beams_condition = db.Column(db.Text, nullable=True)
    support_of_joists_or_beams_comments = db.Column(db.Text, nullable=True)
    support_of_joists_or_beams_code_compliance = db.Column(db.String(10), nullable=True)
    support_of_joists_or_beams_photos = db.Column(db.JSON, nullable=True)

    # Intersection of Shingle Roofs and Masonry section
    intersection_of_shingle_roofs_and_masonry_condition = db.Column(db.Text, nullable=True)
    intersection_of_shingle_roofs_and_masonry_comments = db.Column(db.Text, nullable=True)
    intersection_of_shingle_roofs_and_masonry_code_compliance = db.Column(db.String(10), nullable=True)
    intersection_of_shingle_roofs_and_masonry_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_chimney_supports', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'flashing': {
                    'condition': self.flashing_condition or '',
                    'comments': self.flashing_comments or '',
                    'codeCompliance': self.flashing_code_compliance or '',
                    'photos': self.flashing_photos or []
                },
                'clearanceFromCombustibleMaterials1': {
                    'condition': self.clearance_from_combustible_materials_1_condition or '',
                    'comments': self.clearance_from_combustible_materials_1_comments or '',
                    'codeCompliance': self.clearance_from_combustible_materials_1_code_compliance or '',
                    'photos': self.clearance_from_combustible_materials_1_photos or []
                },
                'clearanceFromCombustibleMaterials2': {
                    'condition': self.clearance_from_combustible_materials_2_condition or '',
                    'comments': self.clearance_from_combustible_materials_2_comments or '',
                    'codeCompliance': self.clearance_from_combustible_materials_2_code_compliance or '',
                    'photos': self.clearance_from_combustible_materials_2_photos or []
                },
                'sealingOfSpaces': {
                    'condition': self.sealing_of_spaces_condition or '',
                    'comments': self.sealing_of_spaces_comments or '',
                    'codeCompliance': self.sealing_of_spaces_code_compliance or '',
                    'photos': self.sealing_of_spaces_photos or []
                },
                'supportOfJoistsOrBeams': {
                    'condition': self.support_of_joists_or_beams_condition or '',
                    'comments': self.support_of_joists_or_beams_comments or '',
                    'codeCompliance': self.support_of_joists_or_beams_code_compliance or '',
                    'photos': self.support_of_joists_or_beams_photos or []
                },
                'intersectionOfShingleRoofsAndMasonry': {
                    'condition': self.intersection_of_shingle_roofs_and_masonry_condition or '',
                    'comments': self.intersection_of_shingle_roofs_and_masonry_comments or '',
                    'codeCompliance': self.intersection_of_shingle_roofs_and_masonry_code_compliance or '',
                    'photos': self.intersection_of_shingle_roofs_and_masonry_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertCOAlarmsLiners(db.Model):
    __tablename__ = 'pellet_insert_co_alarms_liners'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # ABC/BCBC/NBC Combustion Air section
    abc_bcbc_nbc_combustion_air_condition = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_combustion_air_comments = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_combustion_air_code_compliance = db.Column(db.String(10), nullable=True)
    abc_bcbc_nbc_combustion_air_photos = db.Column(db.JSON, nullable=True)

    # NBC/ABC Combustion Air section
    nbc_abc_combustion_air_condition = db.Column(db.Text, nullable=True)
    nbc_abc_combustion_air_comments = db.Column(db.Text, nullable=True)
    nbc_abc_combustion_air_code_compliance = db.Column(db.String(10), nullable=True)
    nbc_abc_combustion_air_photos = db.Column(db.JSON, nullable=True)

    # S - OBC Combustion Air section
    s_obc_combustion_air_condition = db.Column(db.Text, nullable=True)
    s_obc_combustion_air_comments = db.Column(db.Text, nullable=True)
    s_obc_combustion_air_code_compliance = db.Column(db.String(10), nullable=True)
    s_obc_combustion_air_photos = db.Column(db.JSON, nullable=True)

    # Brick or Steel Liners section
    brick_or_steel_liners_condition = db.Column(db.Text, nullable=True)
    brick_or_steel_liners_comments = db.Column(db.Text, nullable=True)
    brick_or_steel_liners_code_compliance = db.Column(db.String(10), nullable=True)
    brick_or_steel_liners_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners 1 section
    firebrick_liners_1_condition = db.Column(db.Text, nullable=True)
    firebrick_liners_1_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_1_code_compliance = db.Column(db.String(10), nullable=True)
    firebrick_liners_1_photos = db.Column(db.JSON, nullable=True)

    # Firebrick Liners 2 section
    firebrick_liners_2_condition = db.Column(db.Text, nullable=True)
    firebrick_liners_2_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_2_code_compliance = db.Column(db.String(10), nullable=True)
    firebrick_liners_2_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_co_alarms_liners', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'abcBcbcNbcCombustionAir': {
                    'condition': self.abc_bcbc_nbc_combustion_air_condition or '',
                    'comments': self.abc_bcbc_nbc_combustion_air_comments or '',
                    'codeCompliance': self.abc_bcbc_nbc_combustion_air_code_compliance or '',
                    'photos': self.abc_bcbc_nbc_combustion_air_photos or []
                },
                'nbcAbcCombustionAir': {
                    'condition': self.nbc_abc_combustion_air_condition or '',
                    'comments': self.nbc_abc_combustion_air_comments or '',
                    'codeCompliance': self.nbc_abc_combustion_air_code_compliance or '',
                    'photos': self.nbc_abc_combustion_air_photos or []
                },
                'sObcCombustionAir': {
                    'condition': self.s_obc_combustion_air_condition or '',
                    'comments': self.s_obc_combustion_air_comments or '',
                    'codeCompliance': self.s_obc_combustion_air_code_compliance or '',
                    'photos': self.s_obc_combustion_air_photos or []
                },
                'brickOrSteelLiners': {
                    'condition': self.brick_or_steel_liners_condition or '',
                    'comments': self.brick_or_steel_liners_comments or '',
                    'codeCompliance': self.brick_or_steel_liners_code_compliance or '',
                    'photos': self.brick_or_steel_liners_photos or []
                },
                'firebrickLiners1': {
                    'condition': self.firebrick_liners_1_condition or '',
                    'comments': self.firebrick_liners_1_comments or '',
                    'codeCompliance': self.firebrick_liners_1_code_compliance or '',
                    'photos': self.firebrick_liners_1_photos or []
                },
                'firebrickLiners2': {
                    'condition': self.firebrick_liners_2_condition or '',
                    'comments': self.firebrick_liners_2_comments or '',
                    'codeCompliance': self.firebrick_liners_2_code_compliance or '',
                    'photos': self.firebrick_liners_2_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertEmberPadFloorProtection(db.Model):
    __tablename__ = 'pellet_insert_ember_pad_floor_protection'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Ember pad - front section
    ember_pad_front_required_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_front_required_certified = db.Column(db.String(255), nullable=True)
    ember_pad_front_present_value = db.Column(db.String(255), nullable=True)
    ember_pad_front_code_compliance = db.Column(db.String(10), nullable=True)
    ember_pad_front_photos = db.Column(db.JSON, nullable=True)

    # Ember pad - right side section
    ember_pad_right_side_required_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_right_side_required_certified = db.Column(db.String(255), nullable=True)
    ember_pad_right_side_present_value = db.Column(db.String(255), nullable=True)
    ember_pad_right_side_code_compliance = db.Column(db.String(10), nullable=True)
    ember_pad_right_side_photos = db.Column(db.JSON, nullable=True)

    # Ember pad - left side section
    ember_pad_left_side_required_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_left_side_required_certified = db.Column(db.String(255), nullable=True)
    ember_pad_left_side_present_value = db.Column(db.String(255), nullable=True)
    ember_pad_left_side_code_compliance = db.Column(db.String(10), nullable=True)
    ember_pad_left_side_photos = db.Column(db.JSON, nullable=True)

    # Floor protection material section
    floor_protection_material_required_uncertified = db.Column(db.String(255), nullable=True)
    floor_protection_material_required_certified = db.Column(db.String(255), nullable=True)
    floor_protection_material_present_value = db.Column(db.String(255), nullable=True)
    floor_protection_material_code_compliance = db.Column(db.String(10), nullable=True)
    floor_protection_material_photos = db.Column(db.JSON, nullable=True)

    # Radiant floor protection section
    radiant_floor_protection_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    radiant_floor_protection_present_value = db.Column(db.String(255), nullable=True)
    radiant_floor_protection_code_compliance = db.Column(db.String(10), nullable=True)
    radiant_floor_protection_photos = db.Column(db.JSON, nullable=True)

    # Floor protection - front section
    floor_protection_front_required_uncertified = db.Column(db.String(255), nullable=True)
    floor_protection_front_required_certified = db.Column(db.String(255), nullable=True)
    floor_protection_front_present_value = db.Column(db.String(255), nullable=True)
    floor_protection_front_code_compliance = db.Column(db.String(10), nullable=True)
    floor_protection_front_photos = db.Column(db.JSON, nullable=True)

    # Floor protection - right side section
    floor_protection_right_side_required_uncertified = db.Column(db.String(255), nullable=True)
    floor_protection_right_side_required_certified = db.Column(db.String(255), nullable=True)
    floor_protection_right_side_present_value = db.Column(db.String(255), nullable=True)
    floor_protection_right_side_code_compliance = db.Column(db.String(10), nullable=True)
    floor_protection_right_side_photos = db.Column(db.JSON, nullable=True)

    # Floor protection - left side section
    floor_protection_left_side_required_uncertified = db.Column(db.String(255), nullable=True)
    floor_protection_left_side_required_certified = db.Column(db.String(255), nullable=True)
    floor_protection_left_side_present_value = db.Column(db.String(255), nullable=True)
    floor_protection_left_side_code_compliance = db.Column(db.String(10), nullable=True)
    floor_protection_left_side_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_ember_pad_floor_protection', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'emberPadFront': {
                    'requiredValueUncertified': self.ember_pad_front_required_uncertified or '',
                    'requiredValueCertified': self.ember_pad_front_required_certified or '',
                    'presentValue': self.ember_pad_front_present_value or '',
                    'codeCompliance': self.ember_pad_front_code_compliance or '',
                    'photos': self.ember_pad_front_photos or []
                },
                'emberPadRightSide': {
                    'requiredValueUncertified': self.ember_pad_right_side_required_uncertified or '',
                    'requiredValueCertified': self.ember_pad_right_side_required_certified or '',
                    'presentValue': self.ember_pad_right_side_present_value or '',
                    'codeCompliance': self.ember_pad_right_side_code_compliance or '',
                    'photos': self.ember_pad_right_side_photos or []
                },
                'emberPadLeftSide': {
                    'requiredValueUncertified': self.ember_pad_left_side_required_uncertified or '',
                    'requiredValueCertified': self.ember_pad_left_side_required_certified or '',
                    'presentValue': self.ember_pad_left_side_present_value or '',
                    'codeCompliance': self.ember_pad_left_side_code_compliance or '',
                    'photos': self.ember_pad_left_side_photos or []
                },
                'floorProtectionMaterial': {
                    'requiredValueUncertified': self.floor_protection_material_required_uncertified or '',
                    'requiredValueCertified': self.floor_protection_material_required_certified or '',
                    'presentValue': self.floor_protection_material_present_value or '',
                    'codeCompliance': self.floor_protection_material_code_compliance or '',
                    'photos': self.floor_protection_material_photos or []
                },
                'radiantFloorProtection': {
                    'requiredValue': self.radiant_floor_protection_required_value or '',
                    'presentValue': self.radiant_floor_protection_present_value or '',
                    'codeCompliance': self.radiant_floor_protection_code_compliance or '',
                    'photos': self.radiant_floor_protection_photos or []
                },
                'floorProtectionFront': {
                    'requiredValueUncertified': self.floor_protection_front_required_uncertified or '',
                    'requiredValueCertified': self.floor_protection_front_required_certified or '',
                    'presentValue': self.floor_protection_front_present_value or '',
                    'codeCompliance': self.floor_protection_front_code_compliance or '',
                    'photos': self.floor_protection_front_photos or []
                },
                'floorProtectionRightSide': {
                    'requiredValueUncertified': self.floor_protection_right_side_required_uncertified or '',
                    'requiredValueCertified': self.floor_protection_right_side_required_certified or '',
                    'presentValue': self.floor_protection_right_side_present_value or '',
                    'codeCompliance': self.floor_protection_right_side_code_compliance or '',
                    'photos': self.floor_protection_right_side_photos or []
                },
                'floorProtectionLeftSide': {
                    'requiredValueUncertified': self.floor_protection_left_side_required_uncertified or '',
                    'requiredValueCertified': self.floor_protection_left_side_required_certified or '',
                    'presentValue': self.floor_protection_left_side_present_value or '',
                    'codeCompliance': self.floor_protection_left_side_code_compliance or '',
                    'photos': self.floor_protection_left_side_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertFireplaceSafetyFeatures(db.Model):
    __tablename__ = 'pellet_insert_fireplace_safety_features'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Basic Info section
    basic_info_manufacturer = db.Column(db.String(255), nullable=True)
    basic_info_model = db.Column(db.String(255), nullable=True)
    basic_info_listing_agency = db.Column(db.String(255), nullable=True)
    basic_info_is_listing_agency_manually_available = db.Column(db.String(10), nullable=True)  # yes/no
    basic_info_certification_standard = db.Column(db.String(20), nullable=True)  # ulc-s635/640/609
    basic_info_listing_agency_type = db.Column(db.String(20), nullable=True)  # ulc/csa/wh-etl/otl/unknown
    basic_info_diameter = db.Column(db.String(255), nullable=True)
    basic_info_comments = db.Column(db.Text, nullable=True)

    # Liner from top of appliance to top of chimney section
    liner_from_top_to_top_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    liner_from_top_to_top_present_value = db.Column(db.String(255), nullable=True)
    liner_from_top_to_top_code_compliance = db.Column(db.String(10), nullable=True)
    liner_from_top_to_top_photos = db.Column(db.JSON, nullable=True)

    # Connection to stainless steel Liner/vent section
    connection_to_stainless_steel_required_value = db.Column(db.String(255), nullable=True)
    connection_to_stainless_steel_comments = db.Column(db.Text, nullable=True)
    connection_to_stainless_steel_code_compliance = db.Column(db.String(10), nullable=True)
    connection_to_stainless_steel_photos = db.Column(db.JSON, nullable=True)

    # Continuous liner section
    continuous_liner_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    continuous_liner_present_value = db.Column(db.String(255), nullable=True)
    continuous_liner_code_compliance = db.Column(db.String(10), nullable=True)
    continuous_liner_photos = db.Column(db.JSON, nullable=True)

    # Total length EVL section
    total_length_evl_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    total_length_evl_present_value = db.Column(db.String(255), nullable=True)
    total_length_evl_code_compliance = db.Column(db.String(10), nullable=True)
    total_length_evl_photos = db.Column(db.JSON, nullable=True)

    # Liner/vent base tee section
    liner_vent_base_tee_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    liner_vent_base_tee_present_value = db.Column(db.String(255), nullable=True)
    liner_vent_base_tee_code_compliance = db.Column(db.String(10), nullable=True)
    liner_vent_base_tee_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_fireplace_safety_features', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'basicInfo': {
                    'manufacturer': self.basic_info_manufacturer or '',
                    'model': self.basic_info_model or '',
                    'listingAgency': self.basic_info_listing_agency or '',
                    'isListingAgencyManuallyAvailable': self.basic_info_is_listing_agency_manually_available or '',
                    'certificationStandard': self.basic_info_certification_standard or '',
                    'listingAgencyType': self.basic_info_listing_agency_type or '',
                    'diameter': self.basic_info_diameter or '',
                    'comments': self.basic_info_comments or ''
                },
                'linerFromTopToTop': {
                    'requiredValue': self.liner_from_top_to_top_required_value or '',
                    'presentValue': self.liner_from_top_to_top_present_value or '',
                    'codeCompliance': self.liner_from_top_to_top_code_compliance or '',
                    'photos': self.liner_from_top_to_top_photos or []
                },
                'connectionToStainlessSteel': {
                    'requiredValue': self.connection_to_stainless_steel_required_value or '',
                    'comments': self.connection_to_stainless_steel_comments or '',
                    'codeCompliance': self.connection_to_stainless_steel_code_compliance or '',
                    'photos': self.connection_to_stainless_steel_photos or []
                },
                'continuousLiner': {
                    'requiredValue': self.continuous_liner_required_value or '',
                    'presentValue': self.continuous_liner_present_value or '',
                    'codeCompliance': self.continuous_liner_code_compliance or '',
                    'photos': self.continuous_liner_photos or []
                },
                'totalLengthEVL': {
                    'requiredValue': self.total_length_evl_required_value or '',
                    'presentValue': self.total_length_evl_present_value or '',
                    'codeCompliance': self.total_length_evl_code_compliance or '',
                    'photos': self.total_length_evl_photos or []
                },
                'linerVentBaseTee': {
                    'requiredValue': self.liner_vent_base_tee_required_value or '',
                    'presentValue': self.liner_vent_base_tee_present_value or '',
                    'codeCompliance': self.liner_vent_base_tee_code_compliance or '',
                    'photos': self.liner_vent_base_tee_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertFireplaceSpecifications(db.Model):
    __tablename__ = 'pellet_insert_fireplace_specifications'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Basic fireplace information
    fireplace_make_model_serial = db.Column(db.String(255), nullable=True)

    # Installation manual
    installation_manual_available = db.Column(db.String(20), nullable=True)  # yes/no/original/web-download

    # Certification and listing
    certification_standard = db.Column(db.String(20), nullable=True)  # astem-e1509/ulc-s628/epa/csa-b415/uncertified/unknown
    listing_agency = db.Column(db.String(20), nullable=True)  # ulc/csa/wh-etl/otl/other

    # Technical specifications
    appliance_type = db.Column(db.String(30), nullable=True)  # fireplace-insert/hearth-mounted-stove
    flu_collar_size = db.Column(db.String(100), nullable=True)
    fan_blower_attached = db.Column(db.String(10), nullable=True)  # yes/no

    # Condition assessment
    comments_condition = db.Column(db.Text, nullable=True)
    suitable = db.Column(db.String(10), nullable=True)  # yes/no

    # Installation location
    installed_in = db.Column(db.String(20), nullable=True)  # residence/modular-home/mobile-home/alcove-garage/other
    specify_installed_in = db.Column(db.String(255), nullable=True)
    appliance_location = db.Column(db.String(20), nullable=True)  # basement/main-floor/other
    specify_appliance_location = db.Column(db.String(255), nullable=True)

    # Installation details
    appliance_installed_by = db.Column(db.String(255), nullable=True)
    appliance_installed_by_unknown = db.Column(db.Boolean, default=False)

    # Additional comments
    comments = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_fireplace_specifications', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'fireplaceMakeModelSerial': self.fireplace_make_model_serial or '',
                'installationManualAvailable': self.installation_manual_available or '',
                'certificationStandard': self.certification_standard or '',
                'listingAgency': self.listing_agency or '',
                'applianceType': self.appliance_type or '',
                'fluCollarSize': self.flu_collar_size or '',
                'fanBlowerAttached': self.fan_blower_attached or '',
                'commentsCondition': self.comments_condition or '',
                'suitable': self.suitable or '',
                'installedIn': self.installed_in or '',
                'specifyInstalledIn': self.specify_installed_in or '',
                'applianceLocation': self.appliance_location or '',
                'specifyApplianceLocation': self.specify_appliance_location or '',
                'applianceInstalledBy': self.appliance_installed_by or '',
                'applianceInstalledByUnknown': self.appliance_installed_by_unknown or False,
                'comments': self.comments or ''
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertLinerApplianceChecks1(db.Model):
    __tablename__ = 'pellet_insert_liner_appliance_checks_1'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Liner/vent base tee support section
    liner_vent_base_tee_support_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    liner_vent_base_tee_support_present_value = db.Column(db.String(255), nullable=True)
    liner_vent_base_tee_support_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    liner_vent_base_tee_support_photos = db.Column(db.JSON, nullable=True)

    # Liner/vent/flashing/storm collar section
    liner_vent_flashing_storm_collar_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    liner_vent_flashing_storm_collar_present_value = db.Column(db.String(255), nullable=True)
    liner_vent_flashing_storm_collar_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    liner_vent_flashing_storm_collar_photos = db.Column(db.JSON, nullable=True)

    # Insulated liner section
    insulated_liner_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    insulated_liner_present_value = db.Column(db.String(255), nullable=True)
    insulated_liner_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    insulated_liner_photos = db.Column(db.JSON, nullable=True)

    # Appliance Vent adaptor section
    appliance_vent_adaptor_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    appliance_vent_adaptor_present_value = db.Column(db.String(255), nullable=True)
    appliance_vent_adaptor_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    appliance_vent_adaptor_photos = db.Column(db.JSON, nullable=True)

    # Vent sealing section
    vent_sealing_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    vent_sealing_present_value = db.Column(db.String(255), nullable=True)
    vent_sealing_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    vent_sealing_photos = db.Column(db.JSON, nullable=True)

    # Liner/vent condition - Acceptable? section
    liner_vent_condition_acceptable_required_value = db.Column(db.String(10), nullable=True)  # yes/no
    liner_vent_condition_acceptable_present_value = db.Column(db.String(255), nullable=True)
    liner_vent_condition_acceptable_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    liner_vent_condition_acceptable_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_liner_appliance_checks_1', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'linerVentBaseTeeSupport': {
                    'requiredValue': self.liner_vent_base_tee_support_required_value or '',
                    'presentValue': self.liner_vent_base_tee_support_present_value or '',
                    'codeCompliance': self.liner_vent_base_tee_support_code_compliance or '',
                    'photos': self.liner_vent_base_tee_support_photos or []
                },
                'linerVentFlashingStormCollar': {
                    'requiredValue': self.liner_vent_flashing_storm_collar_required_value or '',
                    'presentValue': self.liner_vent_flashing_storm_collar_present_value or '',
                    'codeCompliance': self.liner_vent_flashing_storm_collar_code_compliance or '',
                    'photos': self.liner_vent_flashing_storm_collar_photos or []
                },
                'insulatedLiner': {
                    'requiredValue': self.insulated_liner_required_value or '',
                    'presentValue': self.insulated_liner_present_value or '',
                    'codeCompliance': self.insulated_liner_code_compliance or '',
                    'photos': self.insulated_liner_photos or []
                },
                'applianceVentAdaptor': {
                    'requiredValue': self.appliance_vent_adaptor_required_value or '',
                    'presentValue': self.appliance_vent_adaptor_present_value or '',
                    'codeCompliance': self.appliance_vent_adaptor_code_compliance or '',
                    'photos': self.appliance_vent_adaptor_photos or []
                },
                'ventSealing': {
                    'requiredValue': self.vent_sealing_required_value or '',
                    'presentValue': self.vent_sealing_present_value or '',
                    'codeCompliance': self.vent_sealing_code_compliance or '',
                    'photos': self.vent_sealing_photos or []
                },
                'linerVentConditionAcceptable': {
                    'requiredValue': self.liner_vent_condition_acceptable_required_value or '',
                    'presentValue': self.liner_vent_condition_acceptable_present_value or '',
                    'codeCompliance': self.liner_vent_condition_acceptable_code_compliance or '',
                    'photos': self.liner_vent_condition_acceptable_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertLinerApplianceChecks2(db.Model):
    __tablename__ = 'pellet_insert_liner_appliance_checks_2'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Appliance Standard section
    appliance_standard_condition = db.Column(db.Text, nullable=True)
    appliance_standard_comments = db.Column(db.Text, nullable=True)
    appliance_standard_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    appliance_standard_photos = db.Column(db.JSON, nullable=True)

    # Footings section
    footings_condition = db.Column(db.Text, nullable=True)
    footings_comments = db.Column(db.Text, nullable=True)
    footings_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    footings_photos = db.Column(db.JSON, nullable=True)

    # Fireplace Chimneys section
    fireplace_chimneys_condition = db.Column(db.Text, nullable=True)
    fireplace_chimneys_comments = db.Column(db.Text, nullable=True)
    fireplace_chimneys_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    fireplace_chimneys_photos = db.Column(db.JSON, nullable=True)
    fireplace_chimneys_fireball_opening_height = db.Column(db.String(100), nullable=True)
    fireplace_chimneys_fireball_opening_width = db.Column(db.String(100), nullable=True)
    fireplace_chimneys_fireball_opening_total = db.Column(db.String(100), nullable=True)
    fireplace_chimneys_flue_size_required = db.Column(db.String(100), nullable=True)

    # ABC/BCBC/NBC Lintels section
    abc_bcbc_nbc_lintels_condition = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_lintels_comments = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_lintels_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    abc_bcbc_nbc_lintels_photos = db.Column(db.JSON, nullable=True)

    # OBC Lintels section
    obc_lintels_condition = db.Column(db.Text, nullable=True)
    obc_lintels_comments = db.Column(db.Text, nullable=True)
    obc_lintels_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    obc_lintels_photos = db.Column(db.JSON, nullable=True)

    # Corbelling section
    corbelling_condition = db.Column(db.Text, nullable=True)
    corbelling_comments = db.Column(db.Text, nullable=True)
    corbelling_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    corbelling_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_liner_appliance_checks_2', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'applianceStandard': {
                    'condition': self.appliance_standard_condition or '',
                    'comments': self.appliance_standard_comments or '',
                    'codeCompliance': self.appliance_standard_code_compliance or '',
                    'photos': self.appliance_standard_photos or []
                },
                'footings': {
                    'condition': self.footings_condition or '',
                    'comments': self.footings_comments or '',
                    'codeCompliance': self.footings_code_compliance or '',
                    'photos': self.footings_photos or []
                },
                'fireplaceChimneys': {
                    'condition': self.fireplace_chimneys_condition or '',
                    'comments': self.fireplace_chimneys_comments or '',
                    'codeCompliance': self.fireplace_chimneys_code_compliance or '',
                    'photos': self.fireplace_chimneys_photos or [],
                    'fireballOpeningHeight': self.fireplace_chimneys_fireball_opening_height or '',
                    'fireballOpeningWidth': self.fireplace_chimneys_fireball_opening_width or '',
                    'fireballOpeningTotal': self.fireplace_chimneys_fireball_opening_total or '',
                    'flueSizeRequired': self.fireplace_chimneys_flue_size_required or ''
                },
                'abcBcbcNbcLintels': {
                    'condition': self.abc_bcbc_nbc_lintels_condition or '',
                    'comments': self.abc_bcbc_nbc_lintels_comments or '',
                    'codeCompliance': self.abc_bcbc_nbc_lintels_code_compliance or '',
                    'photos': self.abc_bcbc_nbc_lintels_photos or []
                },
                'obcLintels': {
                    'condition': self.obc_lintels_condition or '',
                    'comments': self.obc_lintels_comments or '',
                    'codeCompliance': self.obc_lintels_code_compliance or '',
                    'photos': self.obc_lintels_photos or []
                },
                'corbelling': {
                    'condition': self.corbelling_condition or '',
                    'comments': self.corbelling_comments or '',
                    'codeCompliance': self.corbelling_code_compliance or '',
                    'photos': self.corbelling_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertLinerVentComponents(db.Model):
    __tablename__ = 'pellet_insert_liner_vent_components'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Firebrick Liners section
    firebrick_liners_condition = db.Column(db.Text, nullable=True)
    firebrick_liners_comments = db.Column(db.Text, nullable=True)
    firebrick_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    firebrick_liners_photos = db.Column(db.JSON, nullable=True)

    # Steel Liners section
    steel_liners_condition = db.Column(db.Text, nullable=True)
    steel_liners_comments = db.Column(db.Text, nullable=True)
    steel_liners_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    steel_liners_photos = db.Column(db.JSON, nullable=True)

    # Thickness of Walls 1 section
    thickness_of_walls_1_condition = db.Column(db.Text, nullable=True)
    thickness_of_walls_1_comments = db.Column(db.Text, nullable=True)
    thickness_of_walls_1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    thickness_of_walls_1_photos = db.Column(db.JSON, nullable=True)

    # Thickness of Walls 2 section
    thickness_of_walls_2_condition = db.Column(db.Text, nullable=True)
    thickness_of_walls_2_comments = db.Column(db.Text, nullable=True)
    thickness_of_walls_2_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    thickness_of_walls_2_photos = db.Column(db.JSON, nullable=True)

    # Fire Chamber Dimensions section
    fire_chamber_dimensions_condition = db.Column(db.Text, nullable=True)
    fire_chamber_dimensions_comments = db.Column(db.Text, nullable=True)
    fire_chamber_dimensions_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    fire_chamber_dimensions_photos = db.Column(db.JSON, nullable=True)

    # Hearth Extension section
    hearth_extension_condition = db.Column(db.Text, nullable=True)
    hearth_extension_comments = db.Column(db.Text, nullable=True)
    hearth_extension_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    hearth_extension_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_liner_vent_components', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'firebrickLiners': {
                    'condition': self.firebrick_liners_condition or '',
                    'comments': self.firebrick_liners_comments or '',
                    'codeCompliance': self.firebrick_liners_code_compliance or '',
                    'photos': self.firebrick_liners_photos or []
                },
                'steelLiners': {
                    'condition': self.steel_liners_condition or '',
                    'comments': self.steel_liners_comments or '',
                    'codeCompliance': self.steel_liners_code_compliance or '',
                    'photos': self.steel_liners_photos or []
                },
                'thicknessOfWalls1': {
                    'condition': self.thickness_of_walls_1_condition or '',
                    'comments': self.thickness_of_walls_1_comments or '',
                    'codeCompliance': self.thickness_of_walls_1_code_compliance or '',
                    'photos': self.thickness_of_walls_1_photos or []
                },
                'thicknessOfWalls2': {
                    'condition': self.thickness_of_walls_2_condition or '',
                    'comments': self.thickness_of_walls_2_comments or '',
                    'codeCompliance': self.thickness_of_walls_2_code_compliance or '',
                    'photos': self.thickness_of_walls_2_photos or []
                },
                'fireChamberDimensions': {
                    'condition': self.fire_chamber_dimensions_condition or '',
                    'comments': self.fire_chamber_dimensions_comments or '',
                    'codeCompliance': self.fire_chamber_dimensions_code_compliance or '',
                    'photos': self.fire_chamber_dimensions_photos or []
                },
                'hearthExtension': {
                    'condition': self.hearth_extension_condition or '',
                    'comments': self.hearth_extension_comments or '',
                    'codeCompliance': self.hearth_extension_code_compliance or '',
                    'photos': self.hearth_extension_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertMasonryFireplaceConstruction1(db.Model):
    __tablename__ = 'pellet_insert_masonry_fireplace_construction_1'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Hearth Extension section
    hearth_extension_condition = db.Column(db.Text, nullable=True)
    hearth_extension_comments = db.Column(db.Text, nullable=True)
    hearth_extension_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    hearth_extension_photos = db.Column(db.JSON, nullable=True)

    # Support of Hearth 1 section
    support_of_hearth_1_condition = db.Column(db.Text, nullable=True)
    support_of_hearth_1_comments = db.Column(db.Text, nullable=True)
    support_of_hearth_1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    support_of_hearth_1_photos = db.Column(db.JSON, nullable=True)

    # Support of Hearth 2 section
    support_of_hearth_2_condition = db.Column(db.Text, nullable=True)
    support_of_hearth_2_comments = db.Column(db.Text, nullable=True)
    support_of_hearth_2_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    support_of_hearth_2_photos = db.Column(db.JSON, nullable=True)

    # Slope of Smoke Chamber section
    slope_of_smoke_chamber_condition = db.Column(db.Text, nullable=True)
    slope_of_smoke_chamber_comments = db.Column(db.Text, nullable=True)
    slope_of_smoke_chamber_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    slope_of_smoke_chamber_photos = db.Column(db.JSON, nullable=True)

    # Wall Thickness section
    wall_thickness_condition = db.Column(db.Text, nullable=True)
    wall_thickness_comments = db.Column(db.Text, nullable=True)
    wall_thickness_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_thickness_photos = db.Column(db.JSON, nullable=True)

    # Clearance to Fireplace Opening section
    clearance_to_fireplace_opening_condition = db.Column(db.Text, nullable=True)
    clearance_to_fireplace_opening_comments = db.Column(db.Text, nullable=True)
    clearance_to_fireplace_opening_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearance_to_fireplace_opening_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_masonry_fireplace_construction_1', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'hearthExtension': {
                    'condition': self.hearth_extension_condition or '',
                    'comments': self.hearth_extension_comments or '',
                    'codeCompliance': self.hearth_extension_code_compliance or '',
                    'photos': self.hearth_extension_photos or []
                },
                'supportOfHearth1': {
                    'condition': self.support_of_hearth_1_condition or '',
                    'comments': self.support_of_hearth_1_comments or '',
                    'codeCompliance': self.support_of_hearth_1_code_compliance or '',
                    'photos': self.support_of_hearth_1_photos or []
                },
                'supportOfHearth2': {
                    'condition': self.support_of_hearth_2_condition or '',
                    'comments': self.support_of_hearth_2_comments or '',
                    'codeCompliance': self.support_of_hearth_2_code_compliance or '',
                    'photos': self.support_of_hearth_2_photos or []
                },
                'slopeOfSmokeChamber': {
                    'condition': self.slope_of_smoke_chamber_condition or '',
                    'comments': self.slope_of_smoke_chamber_comments or '',
                    'codeCompliance': self.slope_of_smoke_chamber_code_compliance or '',
                    'photos': self.slope_of_smoke_chamber_photos or []
                },
                'wallThickness': {
                    'condition': self.wall_thickness_condition or '',
                    'comments': self.wall_thickness_comments or '',
                    'codeCompliance': self.wall_thickness_code_compliance or '',
                    'photos': self.wall_thickness_photos or []
                },
                'clearanceToFireplaceOpening': {
                    'condition': self.clearance_to_fireplace_opening_condition or '',
                    'comments': self.clearance_to_fireplace_opening_comments or '',
                    'codeCompliance': self.clearance_to_fireplace_opening_code_compliance or '',
                    'photos': self.clearance_to_fireplace_opening_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertMasonryFireplaceConstruction2(db.Model):
    __tablename__ = 'pellet_insert_masonry_fireplace_construction_2'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Material located in the interior section
    material_located_in_interior_condition = db.Column(db.Text, nullable=True)
    material_located_in_interior_comments = db.Column(db.Text, nullable=True)
    material_located_in_interior_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    material_located_in_interior_photos = db.Column(db.JSON, nullable=True)

    # Clearance to Combustible Framing 1 section
    clearance_to_combustible_framing_1_condition = db.Column(db.Text, nullable=True)
    clearance_to_combustible_framing_1_comments = db.Column(db.Text, nullable=True)
    clearance_to_combustible_framing_1_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearance_to_combustible_framing_1_photos = db.Column(db.JSON, nullable=True)

    # Clearance to Combustible Framing 2 section
    clearance_to_combustible_framing_2_condition = db.Column(db.Text, nullable=True)
    clearance_to_combustible_framing_2_comments = db.Column(db.Text, nullable=True)
    clearance_to_combustible_framing_2_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearance_to_combustible_framing_2_photos = db.Column(db.JSON, nullable=True)

    # Heat-Circulating Duct Outlets section
    heat_circulating_duct_outlets_condition = db.Column(db.Text, nullable=True)
    heat_circulating_duct_outlets_comments = db.Column(db.Text, nullable=True)
    heat_circulating_duct_outlets_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    heat_circulating_duct_outlets_photos = db.Column(db.JSON, nullable=True)

    # ABC/BCBC/NBC Fireplace Inserts section
    abc_bcbc_nbc_fireplace_inserts_condition = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_fireplace_inserts_comments = db.Column(db.Text, nullable=True)
    abc_bcbc_nbc_fireplace_inserts_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    abc_bcbc_nbc_fireplace_inserts_photos = db.Column(db.JSON, nullable=True)

    # OBC Fireplace Inserts section
    obc_fireplace_inserts_condition = db.Column(db.Text, nullable=True)
    obc_fireplace_inserts_comments = db.Column(db.Text, nullable=True)
    obc_fireplace_inserts_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    obc_fireplace_inserts_photos = db.Column(db.JSON, nullable=True)

    # Cleanout section
    cleanout_condition = db.Column(db.Text, nullable=True)
    cleanout_comments = db.Column(db.Text, nullable=True)
    cleanout_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    cleanout_photos = db.Column(db.JSON, nullable=True)

    # Clearance from Combustible Materials section
    clearance_from_combustible_materials_condition = db.Column(db.Text, nullable=True)
    clearance_from_combustible_materials_comments = db.Column(db.Text, nullable=True)
    clearance_from_combustible_materials_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    clearance_from_combustible_materials_photos = db.Column(db.JSON, nullable=True)

    # Wall Thickness section
    wall_thickness_condition = db.Column(db.Text, nullable=True)
    wall_thickness_comments = db.Column(db.Text, nullable=True)
    wall_thickness_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    wall_thickness_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_masonry_fireplace_construction_2', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'materialLocatedInInterior': {
                    'condition': self.material_located_in_interior_condition or '',
                    'comments': self.material_located_in_interior_comments or '',
                    'codeCompliance': self.material_located_in_interior_code_compliance or '',
                    'photos': self.material_located_in_interior_photos or []
                },
                'clearanceToCombustibleFraming1': {
                    'condition': self.clearance_to_combustible_framing_1_condition or '',
                    'comments': self.clearance_to_combustible_framing_1_comments or '',
                    'codeCompliance': self.clearance_to_combustible_framing_1_code_compliance or '',
                    'photos': self.clearance_to_combustible_framing_1_photos or []
                },
                'clearanceToCombustibleFraming2': {
                    'condition': self.clearance_to_combustible_framing_2_condition or '',
                    'comments': self.clearance_to_combustible_framing_2_comments or '',
                    'codeCompliance': self.clearance_to_combustible_framing_2_code_compliance or '',
                    'photos': self.clearance_to_combustible_framing_2_photos or []
                },
                'heatCirculatingDuctOutlets': {
                    'condition': self.heat_circulating_duct_outlets_condition or '',
                    'comments': self.heat_circulating_duct_outlets_comments or '',
                    'codeCompliance': self.heat_circulating_duct_outlets_code_compliance or '',
                    'photos': self.heat_circulating_duct_outlets_photos or []
                },
                'abcBcbcNbcFireplaceInserts': {
                    'condition': self.abc_bcbc_nbc_fireplace_inserts_condition or '',
                    'comments': self.abc_bcbc_nbc_fireplace_inserts_comments or '',
                    'codeCompliance': self.abc_bcbc_nbc_fireplace_inserts_code_compliance or '',
                    'photos': self.abc_bcbc_nbc_fireplace_inserts_photos or []
                },
                'obcFireplaceInserts': {
                    'condition': self.obc_fireplace_inserts_condition or '',
                    'comments': self.obc_fireplace_inserts_comments or '',
                    'codeCompliance': self.obc_fireplace_inserts_code_compliance or '',
                    'photos': self.obc_fireplace_inserts_photos or []
                },
                'cleanout': {
                    'condition': self.cleanout_condition or '',
                    'comments': self.cleanout_comments or '',
                    'codeCompliance': self.cleanout_code_compliance or '',
                    'photos': self.cleanout_photos or []
                },
                'clearanceFromCombustibleMaterials': {
                    'condition': self.clearance_from_combustible_materials_condition or '',
                    'comments': self.clearance_from_combustible_materials_comments or '',
                    'codeCompliance': self.clearance_from_combustible_materials_code_compliance or '',
                    'photos': self.clearance_from_combustible_materials_photos or []
                },
                'wallThickness': {
                    'condition': self.wall_thickness_condition or '',
                    'comments': self.wall_thickness_comments or '',
                    'codeCompliance': self.wall_thickness_code_compliance or '',
                    'photos': self.wall_thickness_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertMaterialsClearances(db.Model):
    __tablename__ = 'pellet_insert_materials_clearances'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Combustible Mantle section
    combustible_mantle_required_value_uncertified = db.Column(db.String(255), nullable=True)
    combustible_mantle_required_value_certified = db.Column(db.String(255), nullable=True)
    combustible_mantle_present_value = db.Column(db.String(255), nullable=True)
    combustible_mantle_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    combustible_mantle_photos = db.Column(db.JSON, nullable=True)

    # Top Trim Facing section
    top_trim_facing_required_value_uncertified = db.Column(db.String(255), nullable=True)
    top_trim_facing_required_value_certified = db.Column(db.String(255), nullable=True)
    top_trim_facing_present_value = db.Column(db.String(255), nullable=True)
    top_trim_facing_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    top_trim_facing_photos = db.Column(db.JSON, nullable=True)

    # Side Trim Facing Right section
    side_trim_facing_right_required_value_uncertified = db.Column(db.String(255), nullable=True)
    side_trim_facing_right_required_value_certified = db.Column(db.String(255), nullable=True)
    side_trim_facing_right_present_value = db.Column(db.String(255), nullable=True)
    side_trim_facing_right_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    side_trim_facing_right_photos = db.Column(db.JSON, nullable=True)

    # Side Trim Facing Left section
    side_trim_facing_left_required_value_uncertified = db.Column(db.String(255), nullable=True)
    side_trim_facing_left_required_value_certified = db.Column(db.String(255), nullable=True)
    side_trim_facing_left_present_value = db.Column(db.String(255), nullable=True)
    side_trim_facing_left_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    side_trim_facing_left_photos = db.Column(db.JSON, nullable=True)

    # Combustible Side Wall section
    combustible_side_wall_required_value_uncertified = db.Column(db.String(255), nullable=True)
    combustible_side_wall_required_value_certified = db.Column(db.String(255), nullable=True)
    combustible_side_wall_present_value = db.Column(db.String(255), nullable=True)
    combustible_side_wall_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    combustible_side_wall_photos = db.Column(db.JSON, nullable=True)

    # Ember Pad Material section
    ember_pad_material_required_value_uncertified = db.Column(db.String(255), nullable=True)
    ember_pad_material_required_value_certified = db.Column(db.String(255), nullable=True)
    ember_pad_material_present_value = db.Column(db.String(255), nullable=True)
    ember_pad_material_code_compliance = db.Column(db.String(10), nullable=True)  # yes/no/uti/na
    ember_pad_material_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_materials_clearances', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'combustibleMantle': {
                    'requiredValueUncertified': self.combustible_mantle_required_value_uncertified or '',
                    'requiredValueCertified': self.combustible_mantle_required_value_certified or '',
                    'presentValue': self.combustible_mantle_present_value or '',
                    'codeCompliance': self.combustible_mantle_code_compliance or '',
                    'photos': self.combustible_mantle_photos or []
                },
                'topTrimFacing': {
                    'requiredValueUncertified': self.top_trim_facing_required_value_uncertified or '',
                    'requiredValueCertified': self.top_trim_facing_required_value_certified or '',
                    'presentValue': self.top_trim_facing_present_value or '',
                    'codeCompliance': self.top_trim_facing_code_compliance or '',
                    'photos': self.top_trim_facing_photos or []
                },
                'sideTrimFacingRight': {
                    'requiredValueUncertified': self.side_trim_facing_right_required_value_uncertified or '',
                    'requiredValueCertified': self.side_trim_facing_right_required_value_certified or '',
                    'presentValue': self.side_trim_facing_right_present_value or '',
                    'codeCompliance': self.side_trim_facing_right_code_compliance or '',
                    'photos': self.side_trim_facing_right_photos or []
                },
                'sideTrimFacingLeft': {
                    'requiredValueUncertified': self.side_trim_facing_left_required_value_uncertified or '',
                    'requiredValueCertified': self.side_trim_facing_left_required_value_certified or '',
                    'presentValue': self.side_trim_facing_left_present_value or '',
                    'codeCompliance': self.side_trim_facing_left_code_compliance or '',
                    'photos': self.side_trim_facing_left_photos or []
                },
                'combustibleSideWall': {
                    'requiredValueUncertified': self.combustible_side_wall_required_value_uncertified or '',
                    'requiredValueCertified': self.combustible_side_wall_required_value_certified or '',
                    'presentValue': self.combustible_side_wall_present_value or '',
                    'codeCompliance': self.combustible_side_wall_code_compliance or '',
                    'photos': self.combustible_side_wall_photos or []
                },
                'emberPadMaterial': {
                    'requiredValueUncertified': self.ember_pad_material_required_value_uncertified or '',
                    'requiredValueCertified': self.ember_pad_material_required_value_certified or '',
                    'presentValue': self.ember_pad_material_present_value or '',
                    'codeCompliance': self.ember_pad_material_code_compliance or '',
                    'photos': self.ember_pad_material_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PelletInsertChimneyJointsLinerDetails(db.Model):
    __tablename__ = 'pellet_insert_chimney_joints_liner_details'

    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)

    # Joints in Chimney Liners 1 section
    joints_in_chimney_liners_1_condition = db.Column(db.Text, nullable=True)
    joints_in_chimney_liners_1_comments = db.Column(db.Text, nullable=True)
    joints_in_chimney_liners_1_code_compliance = db.Column(db.String(10), nullable=True)
    joints_in_chimney_liners_1_photos = db.Column(db.JSON, nullable=True)

    # Joints in Chimney Liners 2 section
    joints_in_chimney_liners_2_condition = db.Column(db.Text, nullable=True)
    joints_in_chimney_liners_2_comments = db.Column(db.Text, nullable=True)
    joints_in_chimney_liners_2_code_compliance = db.Column(db.String(10), nullable=True)
    joints_in_chimney_liners_2_photos = db.Column(db.JSON, nullable=True)

    # Installation of Chimney Liners section
    installation_of_chimney_liners_condition = db.Column(db.Text, nullable=True)
    installation_of_chimney_liners_comments = db.Column(db.Text, nullable=True)
    installation_of_chimney_liners_code_compliance = db.Column(db.String(10), nullable=True)
    installation_of_chimney_liners_photos = db.Column(db.JSON, nullable=True)

    # Spaces between Liners and Surrounding Masonry section
    spaces_between_liners_and_surrounding_masonry_condition = db.Column(db.Text, nullable=True)
    spaces_between_liners_and_surrounding_masonry_comments = db.Column(db.Text, nullable=True)
    spaces_between_liners_and_surrounding_masonry_code_compliance = db.Column(db.String(10), nullable=True)
    spaces_between_liners_and_surrounding_masonry_photos = db.Column(db.JSON, nullable=True)

    # Mortar for Chimney Liners section
    mortar_for_chimney_liners_condition = db.Column(db.Text, nullable=True)
    mortar_for_chimney_liners_comments = db.Column(db.Text, nullable=True)
    mortar_for_chimney_liners_code_compliance = db.Column(db.String(10), nullable=True)
    mortar_for_chimney_liners_photos = db.Column(db.JSON, nullable=True)

    # Extension of Chimney Liners section
    extension_of_chimney_liners_condition = db.Column(db.Text, nullable=True)
    extension_of_chimney_liners_comments = db.Column(db.Text, nullable=True)
    extension_of_chimney_liners_code_compliance = db.Column(db.String(10), nullable=True)
    extension_of_chimney_liners_photos = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    inspection = db.relationship('Inspection', backref=db.backref('pellet_insert_chimney_joints_liner_details', uselist=False))

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'formData': {
                'jointsInChimneyLiners1': {
                    'condition': self.joints_in_chimney_liners_1_condition or '',
                    'comments': self.joints_in_chimney_liners_1_comments or '',
                    'codeCompliance': self.joints_in_chimney_liners_1_code_compliance or '',
                    'photos': self.joints_in_chimney_liners_1_photos or []
                },
                'jointsInChimneyLiners2': {
                    'condition': self.joints_in_chimney_liners_2_condition or '',
                    'comments': self.joints_in_chimney_liners_2_comments or '',
                    'codeCompliance': self.joints_in_chimney_liners_2_code_compliance or '',
                    'photos': self.joints_in_chimney_liners_2_photos or []
                },
                'installationOfChimneyLiners': {
                    'condition': self.installation_of_chimney_liners_condition or '',
                    'comments': self.installation_of_chimney_liners_comments or '',
                    'codeCompliance': self.installation_of_chimney_liners_code_compliance or '',
                    'photos': self.installation_of_chimney_liners_photos or []
                },
                'spacesBetweenLinersAndSurroundingMasonry': {
                    'condition': self.spaces_between_liners_and_surrounding_masonry_condition or '',
                    'comments': self.spaces_between_liners_and_surrounding_masonry_comments or '',
                    'codeCompliance': self.spaces_between_liners_and_surrounding_masonry_code_compliance or '',
                    'photos': self.spaces_between_liners_and_surrounding_masonry_photos or []
                },
                'mortarForChimneyLiners': {
                    'condition': self.mortar_for_chimney_liners_condition or '',
                    'comments': self.mortar_for_chimney_liners_comments or '',
                    'codeCompliance': self.mortar_for_chimney_liners_code_compliance or '',
                    'photos': self.mortar_for_chimney_liners_photos or []
                },
                'extensionOfChimneyLiners': {
                    'condition': self.extension_of_chimney_liners_condition or '',
                    'comments': self.extension_of_chimney_liners_comments or '',
                    'codeCompliance': self.extension_of_chimney_liners_code_compliance or '',
                    'photos': self.extension_of_chimney_liners_photos or []
                }
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
