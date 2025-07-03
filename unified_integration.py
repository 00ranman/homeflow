#!/usr/bin/env python3
"""
HomeFlow Unified Integration
Complete household coordination system integrated with Extropy ecosystem
"""

import asyncio
import aiohttp
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import sqlite3
import hashlib
import math
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class HouseholdXPTransaction:
    user_id: str
    action_type: str
    description: str
    entropy_delta: float
    closure_speed: float
    domain: str
    metadata: Dict[str, Any]

class HomeFlowIntegration:
    def __init__(self):
        self.auth_service_url = os.getenv("AUTH_SERVICE_URL", "http://localhost:3002")
        self.xp_ledger_url = os.getenv("XP_LEDGER_URL", "http://localhost:3001")
        self.gateway_url = os.getenv("GATEWAY_URL", "http://localhost:3000")
        self.signalflow_url = os.getenv("SIGNALFLOW_URL", "http://localhost:3003")
        self.levelup_url = os.getenv("LEVELUP_URL", "http://localhost:3004")
        
        self.auth_token = None
        self.user_data = None
        self.session = None
        
        # Initialize comprehensive household database
        self.init_household_db()
    
    def init_household_db(self):
        """Initialize comprehensive household management database"""
        conn = sqlite3.connect('homeflow_complete.db')
        cursor = conn.cursor()
        
        # Complete household inventory (food + ALL items)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS household_inventory (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                location TEXT,
                expiration_date TEXT,
                reorder_level REAL,
                brand TEXT,
                cost REAL,
                barcode TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Consumption patterns and predictions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consumption_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                daily_rate REAL DEFAULT 0,
                weekly_rate REAL DEFAULT 0,
                monthly_rate REAL DEFAULT 0,
                seasonal_factors TEXT,
                family_member_usage TEXT,
                pattern_confidence REAL DEFAULT 0.5,
                last_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES household_inventory (id)
            )
        ''')
        
        # Purchase history and cost tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                purchase_date TIMESTAMP NOT NULL,
                quantity REAL NOT NULL,
                cost REAL,
                vendor TEXT,
                payment_method TEXT,
                notes TEXT,
                receipt_image TEXT,
                FOREIGN KEY (item_id) REFERENCES household_inventory (id)
            )
        ''')
        
        # Comprehensive household tasks system
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS household_tasks (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT,
                description TEXT,
                difficulty REAL DEFAULT 1.0,
                skill_requirements TEXT,
                time_estimate INTEGER,
                frequency_days INTEGER,
                seasonal_task BOOLEAN DEFAULT FALSE,
                assignable_to TEXT,
                tools_required TEXT,
                safety_level TEXT DEFAULT 'safe',
                xp_base_reward REAL DEFAULT 10.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Task assignments and scheduling
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_assignments (
                id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                assigned_to TEXT NOT NULL,
                assigned_by TEXT,
                due_date TIMESTAMP,
                priority TEXT DEFAULT 'normal',
                status TEXT DEFAULT 'pending',
                estimated_duration INTEGER,
                actual_duration INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES household_tasks (id)
            )
        ''')
        
        # Task completion tracking with XP
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_id TEXT NOT NULL,
                completed_by TEXT NOT NULL,
                completion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                quality_score REAL DEFAULT 0.8,
                difficulty_actual REAL,
                skill_used TEXT,
                tools_used TEXT,
                notes TEXT,
                photo_evidence TEXT,
                xp_earned REAL,
                xp_transaction_id TEXT,
                verified_by TEXT,
                FOREIGN KEY (assignment_id) REFERENCES task_assignments (id)
            )
        ''')
        
        # Family skills from LevelUp Academy integration
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS family_skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                skill_category TEXT NOT NULL,
                skill_name TEXT NOT NULL,
                skill_level REAL DEFAULT 0.0,
                confidence_level REAL DEFAULT 0.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                progression_rate REAL DEFAULT 0.0,
                levelup_sync_id TEXT,
                household_applications TEXT
            )
        ''')
        
        # Skill to task mapping
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skill_task_mapping (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_category TEXT NOT NULL,
                skill_name TEXT NOT NULL,
                task_id TEXT NOT NULL,
                required_level REAL DEFAULT 0.0,
                optimal_level REAL DEFAULT 1.0,
                skill_development_value REAL DEFAULT 0.1,
                FOREIGN KEY (task_id) REFERENCES household_tasks (id)
            )
        ''')
        
        # Coral device integration for camera tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coral_devices (
                id TEXT PRIMARY KEY,
                device_name TEXT NOT NULL,
                location TEXT NOT NULL,
                device_type TEXT DEFAULT 'camera',
                ip_address TEXT,
                capabilities TEXT,
                status TEXT DEFAULT 'offline',
                last_ping TIMESTAMP,
                privacy_mode BOOLEAN DEFAULT FALSE,
                detection_zones TEXT,
                setup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Visual detection events from cameras
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detection_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT NOT NULL,
                detected_items TEXT,
                confidence_scores TEXT,
                image_data TEXT,
                processed BOOLEAN DEFAULT FALSE,
                verified BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (device_id) REFERENCES coral_devices (id)
            )
        ''')
        
        # Inventory updates from visual detection
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT,
                change_type TEXT NOT NULL,
                quantity_change REAL,
                detected_by TEXT,
                detection_confidence REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                verified BOOLEAN DEFAULT FALSE,
                verified_by TEXT,
                verification_timestamp TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES household_inventory (id)
            )
        ''')
        
        # Calendar integration for planned events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS planned_events (
                id TEXT PRIMARY KEY,
                event_name TEXT NOT NULL,
                event_date TIMESTAMP NOT NULL,
                event_type TEXT DEFAULT 'general',
                guest_count INTEGER DEFAULT 0,
                special_requirements TEXT,
                meal_requirements TEXT,
                supply_requirements TEXT,
                notes TEXT,
                created_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Consumption forecasting
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consumption_forecasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT,
                event_id TEXT,
                forecast_date TIMESTAMP,
                predicted_usage REAL,
                confidence_level REAL,
                calculation_method TEXT,
                actual_usage REAL,
                accuracy_score REAL,
                FOREIGN KEY (item_id) REFERENCES household_inventory (id),
                FOREIGN KEY (event_id) REFERENCES planned_events (id)
            )
        ''')
        
        # Automated ordering system
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automated_orders (
                id TEXT PRIMARY KEY,
                vendor TEXT NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                items TEXT NOT NULL,
                total_cost REAL,
                delivery_date TIMESTAMP,
                status TEXT DEFAULT 'pending',
                tracking_number TEXT,
                notes TEXT,
                confirmation_data TEXT
            )
        ''')
        
        # Meal planning enhancement (build on existing)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enhanced_meals (
                id TEXT PRIMARY KEY,
                meal_name TEXT NOT NULL,
                meal_type TEXT,
                family_members TEXT,
                nutrition_goals TEXT,
                dietary_restrictions TEXT,
                preparation_time INTEGER,
                cooking_skill_required REAL DEFAULT 1.0,
                cost_estimate REAL,
                ingredients_needed TEXT,
                health_score REAL,
                family_rating REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Health and nutrition tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS family_health_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                age INTEGER,
                activity_level TEXT DEFAULT 'moderate',
                dietary_restrictions TEXT,
                health_goals TEXT,
                allergies TEXT,
                medical_conditions TEXT,
                nutrition_targets TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # XP transactions for household activities
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS household_xp_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                description TEXT NOT NULL,
                entropy_delta REAL NOT NULL,
                closure_speed REAL NOT NULL,
                domain TEXT NOT NULL,
                metadata TEXT NOT NULL,
                synced BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ledger_transaction_id TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Initialize with sample household data
        self.create_sample_household_data()
    
    def create_sample_household_data(self):
        """Create comprehensive sample household data"""
        conn = sqlite3.connect('homeflow_complete.db')
        cursor = conn.cursor()
        
        # Sample household inventory categories
        sample_inventory = [
            # Kitchen/Food items
            {"id": str(uuid.uuid4()), "name": "Milk", "category": "Dairy", "quantity": 2, "unit": "gallon", "location": "Refrigerator", "reorder_level": 0.5},
            {"id": str(uuid.uuid4()), "name": "Bread", "category": "Bakery", "quantity": 1, "unit": "loaf", "location": "Pantry", "reorder_level": 0.5},
            {"id": str(uuid.uuid4()), "name": "Eggs", "category": "Dairy", "quantity": 12, "unit": "count", "location": "Refrigerator", "reorder_level": 6},
            
            # Bathroom/Personal Care
            {"id": str(uuid.uuid4()), "name": "Toilet Paper", "category": "Personal Care", "quantity": 8, "unit": "rolls", "location": "Bathroom Closet", "reorder_level": 4},
            {"id": str(uuid.uuid4()), "name": "Toothpaste", "category": "Personal Care", "quantity": 2, "unit": "tube", "location": "Bathroom", "reorder_level": 1},
            {"id": str(uuid.uuid4()), "name": "Shampoo", "category": "Personal Care", "quantity": 1, "unit": "bottle", "location": "Shower", "reorder_level": 0.25},
            {"id": str(uuid.uuid4()), "name": "Q-tips", "category": "Personal Care", "quantity": 150, "unit": "count", "location": "Bathroom", "reorder_level": 50},
            
            # Cleaning Supplies
            {"id": str(uuid.uuid4()), "name": "Dish Soap", "category": "Cleaning", "quantity": 1, "unit": "bottle", "location": "Kitchen Sink", "reorder_level": 0.25},
            {"id": str(uuid.uuid4()), "name": "Laundry Detergent", "category": "Cleaning", "quantity": 1, "unit": "bottle", "location": "Laundry Room", "reorder_level": 0.2},
            {"id": str(uuid.uuid4()), "name": "Paper Towels", "category": "Cleaning", "quantity": 6, "unit": "rolls", "location": "Kitchen", "reorder_level": 2},
            {"id": str(uuid.uuid4()), "name": "All-Purpose Cleaner", "category": "Cleaning", "quantity": 1, "unit": "bottle", "location": "Cleaning Closet", "reorder_level": 0.25},
            
            # Miscellaneous
            {"id": str(uuid.uuid4()), "name": "Batteries AA", "category": "Electronics", "quantity": 8, "unit": "count", "location": "Utility Drawer", "reorder_level": 4},
            {"id": str(uuid.uuid4()), "name": "Light Bulbs", "category": "Home Maintenance", "quantity": 4, "unit": "count", "location": "Storage Closet", "reorder_level": 2},
        ]
        
        for item in sample_inventory:
            cursor.execute('''
                INSERT OR IGNORE INTO household_inventory 
                (id, name, category, quantity, unit, location, reorder_level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (item["id"], item["name"], item["category"], item["quantity"], 
                  item["unit"], item["location"], item["reorder_level"]))
        
        # Sample household tasks with difficulty and skill requirements
        sample_tasks = [
            # Kitchen tasks
            {"id": str(uuid.uuid4()), "name": "Load/Unload Dishwasher", "category": "Kitchen", "difficulty": 1.0, "time_estimate": 10, "frequency_days": 1, "skill_requirements": "organization,attention_to_detail", "assignable_to": "age_8+"},
            {"id": str(uuid.uuid4()), "name": "Wipe Down Counters", "category": "Kitchen", "difficulty": 1.2, "time_estimate": 5, "frequency_days": 1, "skill_requirements": "cleaning,attention_to_detail", "assignable_to": "age_6+"},
            {"id": str(uuid.uuid4()), "name": "Clean Stovetop", "category": "Kitchen", "difficulty": 2.0, "time_estimate": 15, "frequency_days": 3, "skill_requirements": "cleaning,safety_awareness", "assignable_to": "age_12+"},
            {"id": str(uuid.uuid4()), "name": "Deep Clean Refrigerator", "category": "Kitchen", "difficulty": 2.8, "time_estimate": 45, "frequency_days": 14, "skill_requirements": "organization,cleaning,time_management", "assignable_to": "age_14+"},
            
            # Bathroom tasks
            {"id": str(uuid.uuid4()), "name": "Clean Toilet", "category": "Bathroom", "difficulty": 2.2, "time_estimate": 10, "frequency_days": 3, "skill_requirements": "cleaning,hygiene_awareness", "assignable_to": "age_10+"},
            {"id": str(uuid.uuid4()), "name": "Clean Shower/Bathtub", "category": "Bathroom", "difficulty": 2.5, "time_estimate": 20, "frequency_days": 7, "skill_requirements": "cleaning,physical_strength", "assignable_to": "age_12+"},
            {"id": str(uuid.uuid4()), "name": "Mop Bathroom Floor", "category": "Bathroom", "difficulty": 1.8, "time_estimate": 8, "frequency_days": 3, "skill_requirements": "cleaning,coordination", "assignable_to": "age_8+"},
            
            # Living areas
            {"id": str(uuid.uuid4()), "name": "Vacuum Living Room", "category": "Living Areas", "difficulty": 1.5, "time_estimate": 15, "frequency_days": 3, "skill_requirements": "physical_activity,attention_to_detail", "assignable_to": "age_10+"},
            {"id": str(uuid.uuid4()), "name": "Dust Furniture", "category": "Living Areas", "difficulty": 1.3, "time_estimate": 12, "frequency_days": 7, "skill_requirements": "attention_to_detail,gentle_handling", "assignable_to": "age_8+"},
            {"id": str(uuid.uuid4()), "name": "Organize Books/Media", "category": "Living Areas", "difficulty": 1.0, "time_estimate": 10, "frequency_days": 7, "skill_requirements": "organization,categorization", "assignable_to": "age_6+"},
            
            # Laundry tasks
            {"id": str(uuid.uuid4()), "name": "Sort Laundry", "category": "Laundry", "difficulty": 1.2, "time_estimate": 8, "frequency_days": 2, "skill_requirements": "categorization,color_recognition", "assignable_to": "age_6+"},
            {"id": str(uuid.uuid4()), "name": "Load Washing Machine", "category": "Laundry", "difficulty": 1.8, "time_estimate": 5, "frequency_days": 2, "skill_requirements": "machine_operation,measurement", "assignable_to": "age_10+"},
            {"id": str(uuid.uuid4()), "name": "Fold and Put Away Clothes", "category": "Laundry", "difficulty": 1.5, "time_estimate": 20, "frequency_days": 2, "skill_requirements": "organization,fine_motor_skills", "assignable_to": "age_8+"},
            
            # Outdoor/Maintenance
            {"id": str(uuid.uuid4()), "name": "Take Out Trash", "category": "Maintenance", "difficulty": 1.0, "time_estimate": 5, "frequency_days": 2, "skill_requirements": "responsibility,physical_activity", "assignable_to": "age_8+"},
            {"id": str(uuid.uuid4()), "name": "Water Plants", "category": "Outdoor", "difficulty": 1.2, "time_estimate": 10, "frequency_days": 2, "skill_requirements": "plant_care,measurement", "assignable_to": "age_6+"},
            {"id": str(uuid.uuid4()), "name": "Mow Lawn", "category": "Outdoor", "difficulty": 3.0, "time_estimate": 45, "frequency_days": 7, "skill_requirements": "machine_operation,safety_awareness,physical_strength", "assignable_to": "age_16+"},
        ]
        
        for task in sample_tasks:
            cursor.execute('''
                INSERT OR IGNORE INTO household_tasks 
                (id, name, category, difficulty, time_estimate, frequency_days, skill_requirements, assignable_to)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (task["id"], task["name"], task["category"], task["difficulty"], 
                  task["time_estimate"], task["frequency_days"], task["skill_requirements"], task["assignable_to"]))
        
        conn.commit()
        conn.close()
    
    async def authenticate_user(self, email: str, password: str = None, token: str = None) -> bool:
        """Authenticate user with unified system"""
        try:
            async with aiohttp.ClientSession() as session:
                if token:
                    # Verify existing token
                    headers = {"Authorization": f"Bearer {token}"}
                    async with session.get(f"{self.auth_service_url}/api/users/me", headers=headers) as response:
                        if response.status == 200:
                            self.user_data = await response.json()
                            self.auth_token = token
                            await self.connect_platform()
                            return True
                else:
                    # Login with credentials
                    login_data = {"email": email, "password": password}
                    async with session.post(f"{self.auth_service_url}/api/auth/login", json=login_data) as response:
                        if response.status == 200:
                            result = await response.json()
                            self.auth_token = result["token"]
                            self.user_data = result["user"]
                            await self.connect_platform()
                            return True
                        
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            
        return False
    
    async def connect_platform(self) -> bool:
        """Connect HomeFlow to the unified platform"""
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            platform_data = {
                "platformUserId": self.user_data["userId"],
                "username": self.user_data.get("profile", {}).get("displayName", "HomeFlow User"),
                "credentials": {
                    "homeflow_version": "1.0",
                    "capabilities": [
                        "household_inventory", "meal_planning", "chore_management", 
                        "camera_integration", "skill_tracking", "health_optimization",
                        "automated_ordering", "consumption_prediction"
                    ]
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.auth_service_url}/api/platforms/connect/homeflow",
                    json=platform_data,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info("HomeFlow connected to unified platform")
                        return True
                        
        except Exception as e:
            logger.error(f"Platform connection failed: {e}")
            
        return False
    
    def calculate_household_entropy(self, activity_data: Dict[str, Any]) -> float:
        """Calculate entropy reduction for household activities"""
        
        activity_type = activity_data.get("activity_type", "general")
        
        if activity_type == "chore_completion":
            return self.calculate_chore_entropy(activity_data)
        elif activity_type == "inventory_management":
            return self.calculate_inventory_entropy(activity_data)
        elif activity_type == "meal_preparation":
            return self.calculate_meal_entropy(activity_data)
        elif activity_type == "health_optimization":
            return self.calculate_health_entropy(activity_data)
        else:
            return self.calculate_general_household_entropy(activity_data)
    
    def calculate_chore_entropy(self, chore_data: Dict[str, Any]) -> float:
        """Calculate entropy reduction for chore completion"""
        base_entropy = 12.0
        
        # Task difficulty multiplier
        difficulty = chore_data.get("difficulty", 1.0)
        
        # Skill gap bonus (learning new skills)
        skill_gap = chore_data.get("skill_gap", 0.0)
        skill_bonus = 1.0 + (skill_gap * 0.5)
        
        # Quality of completion
        quality_score = chore_data.get("quality_score", 0.8)
        
        # Time efficiency
        estimated_time = chore_data.get("estimated_time", 30)
        actual_time = chore_data.get("actual_time", 30)
        efficiency = min(2.0, estimated_time / actual_time) if actual_time > 0 else 1.0
        
        # Consistency bonus
        consistency = chore_data.get("consistency_score", 1.0)
        
        # Family impact (how much this helps the whole household)
        family_impact = chore_data.get("family_impact", 1.0)
        
        entropy_delta = (
            base_entropy * 
            difficulty * 
            skill_bonus * 
            quality_score * 
            efficiency * 
            consistency * 
            family_impact
        )
        
        return round(entropy_delta, 2)
    
    def calculate_inventory_entropy(self, inventory_data: Dict[str, Any]) -> float:
        """Calculate entropy reduction for inventory management"""
        base_entropy = 8.0
        
        # Organization level achieved
        organization_score = inventory_data.get("organization_score", 0.8)
        
        # Accuracy of tracking
        accuracy_score = inventory_data.get("accuracy_score", 0.9)
        
        # Automation level (manual vs automated tracking)
        automation_level = inventory_data.get("automation_level", 0.5)
        automation_bonus = 1.0 + (automation_level * 0.3)
        
        # Cost optimization achieved
        cost_optimization = inventory_data.get("cost_optimization", 1.0)
        
        # Waste reduction
        waste_reduction = inventory_data.get("waste_reduction", 1.0)
        
        entropy_delta = (
            base_entropy * 
            organization_score * 
            accuracy_score * 
            automation_bonus * 
            cost_optimization * 
            waste_reduction
        )
        
        return round(entropy_delta, 2)
    
    def calculate_meal_entropy(self, meal_data: Dict[str, Any]) -> float:
        """Calculate entropy reduction for meal preparation and planning"""
        base_entropy = 10.0
        
        # Nutrition optimization
        nutrition_score = meal_data.get("nutrition_score", 0.8)
        
        # Meal complexity and skill development
        complexity = meal_data.get("complexity", 1.0)
        
        # Family satisfaction
        satisfaction = meal_data.get("family_satisfaction", 0.8)
        
        # Waste reduction (using up ingredients)
        waste_reduction = meal_data.get("waste_reduction", 1.0)
        
        # Time efficiency
        time_efficiency = meal_data.get("time_efficiency", 1.0)
        
        # Cost effectiveness
        cost_effectiveness = meal_data.get("cost_effectiveness", 1.0)
        
        entropy_delta = (
            base_entropy * 
            nutrition_score * 
            complexity * 
            satisfaction * 
            waste_reduction * 
            time_efficiency * 
            cost_effectiveness
        )
        
        return round(entropy_delta, 2)
    
    def calculate_health_entropy(self, health_data: Dict[str, Any]) -> float:
        """Calculate entropy reduction for health and nutrition optimization"""
        base_entropy = 15.0
        
        # Dietary improvement
        dietary_improvement = health_data.get("dietary_improvement", 1.0)
        
        # Exercise integration
        exercise_integration = health_data.get("exercise_integration", 1.0)
        
        # Family wellness score
        wellness_score = health_data.get("family_wellness_score", 0.8)
        
        # Long-term health impact
        health_impact = health_data.get("long_term_impact", 1.0)
        
        entropy_delta = (
            base_entropy * 
            dietary_improvement * 
            exercise_integration * 
            wellness_score * 
            health_impact
        )
        
        return round(entropy_delta, 2)
    
    def calculate_general_household_entropy(self, activity_data: Dict[str, Any]) -> float:
        """Calculate entropy reduction for general household activities"""
        base_entropy = 5.0
        
        # General effort and impact
        effort_level = activity_data.get("effort_level", 1.0)
        household_impact = activity_data.get("household_impact", 1.0)
        quality = activity_data.get("quality", 0.8)
        
        entropy_delta = base_entropy * effort_level * household_impact * quality
        
        return round(entropy_delta, 2)
    
    async def track_household_activity(self, activity_data: Dict[str, Any]) -> Optional[str]:
        """Track household activity and award XP"""
        if not self.user_data:
            logger.error("User not authenticated")
            return None
        
        # Calculate entropy reduction
        entropy_delta = self.calculate_household_entropy(activity_data)
        
        # Determine causal closure speed based on activity type
        activity_type = activity_data.get("activity_type", "general")
        closure_speeds = {
            "chore_completion": 1e5,     # Behavioral domain
            "inventory_management": 1e4,  # Economic/organizational domain
            "meal_preparation": 1e6,     # Cognitive domain (planning and creativity)
            "health_optimization": 1e3,  # Social domain (family wellbeing)
            "automation_setup": 1e2,     # Technical domain (long-term efficiency)
            "general": 1e5
        }
        closure_speed = closure_speeds.get(activity_type, 1e5)
        
        # Create XP transaction
        transaction = HouseholdXPTransaction(
            user_id=self.user_data["userId"],
            action_type=f"household_{activity_type}",
            description=activity_data.get("description", f"Household activity: {activity_type}"),
            entropy_delta=entropy_delta,
            closure_speed=closure_speed,
            domain="household",
            metadata={
                **activity_data,
                "platform": "homeflow",
                "household_category": activity_data.get("category", "general")
            }
        )
        
        # Track XP transaction
        return await self.track_xp_transaction(transaction)
    
    async def track_xp_transaction(self, transaction: HouseholdXPTransaction) -> Optional[str]:
        """Track XP transaction locally and sync with ledger"""
        try:
            # Store locally first
            local_id = self.store_local_xp_transaction(transaction)
            
            # Sync with XP Ledger
            if self.auth_token:
                ledger_id = await self.sync_to_xp_ledger(transaction)
                if ledger_id:
                    self.update_transaction_sync_status(local_id, ledger_id)
                    return ledger_id
            
            return str(local_id)
            
        except Exception as e:
            logger.error(f"XP tracking failed: {e}")
            return None
    
    def store_local_xp_transaction(self, transaction: HouseholdXPTransaction) -> int:
        """Store XP transaction in local database"""
        conn = sqlite3.connect('homeflow_complete.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO household_xp_transactions 
            (user_id, action_type, description, entropy_delta, closure_speed, domain, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction.user_id,
            transaction.action_type,
            transaction.description,
            transaction.entropy_delta,
            transaction.closure_speed,
            transaction.domain,
            json.dumps(transaction.metadata)
        ))
        
        local_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return local_id
    
    async def sync_to_xp_ledger(self, transaction: HouseholdXPTransaction) -> Optional[str]:
        """Sync XP transaction to the central ledger"""
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            ledger_data = {
                "userId": transaction.user_id,
                "platform": "homeflow",
                "actionType": transaction.action_type,
                "actionDescription": transaction.description,
                "entropyDelta": transaction.entropy_delta,
                "causalClosureSpeed": transaction.closure_speed,
                "domain": transaction.domain,
                "validators": [
                    {
                        "type": "household_activity",
                        "validatorId": "homeflow_system",
                        "score": 0.92,
                        "timestamp": datetime.now().isoformat()
                    }
                ],
                "metadata": {
                    **transaction.metadata,
                    "source": "homeflow",
                    "integration_version": "1.0"
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.xp_ledger_url}/api/xp/transaction",
                    json=ledger_data,
                    headers=headers
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        return result["transaction"]["transactionId"]
                        
        except Exception as e:
            logger.error(f"XP Ledger sync failed: {e}")
            
        return None
    
    def update_transaction_sync_status(self, local_id: int, ledger_id: str):
        """Update local transaction with sync status"""
        conn = sqlite3.connect('homeflow_complete.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE household_xp_transactions 
            SET synced = TRUE, ledger_transaction_id = ?
            WHERE id = ?
        ''', (ledger_id, local_id))
        
        conn.commit()
        conn.close()
    
    async def create_signalflow_task(self, task_data: Dict[str, Any]) -> Optional[str]:
        """Create task in SignalFlow for household management"""
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            signalflow_task = {
                "task": task_data.get("name"),
                "description": task_data.get("description"),
                "priority": task_data.get("priority", "normal"),
                "assigned_to": task_data.get("assigned_to"),
                "due_date": task_data.get("due_date"),
                "category": "household",
                "metadata": {
                    "household_task_id": task_data.get("id"),
                    "difficulty": task_data.get("difficulty"),
                    "estimated_time": task_data.get("time_estimate"),
                    "skill_requirements": task_data.get("skill_requirements"),
                    "xp_reward": task_data.get("xp_base_reward")
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.signalflow_url}/api/tasks/create",
                    json=signalflow_task,
                    headers=headers
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        return result.get("task_id")
                        
        except Exception as e:
            logger.error(f"SignalFlow task creation failed: {e}")
            
        return None
    
    def get_household_analytics(self) -> Dict[str, Any]:
        """Get comprehensive household analytics"""
        conn = sqlite3.connect('homeflow_complete.db')
        cursor = conn.cursor()
        
        # Inventory analytics
        cursor.execute('''
            SELECT category, COUNT(*) as item_count, 
                   SUM(CASE WHEN quantity <= reorder_level THEN 1 ELSE 0 END) as low_stock_count
            FROM household_inventory
            GROUP BY category
        ''')
        inventory_stats = cursor.fetchall()
        
        # Task completion analytics
        cursor.execute('''
            SELECT category, COUNT(*) as total_tasks,
                   AVG(quality_score) as avg_quality,
                   SUM(xp_earned) as total_xp
            FROM household_tasks ht
            LEFT JOIN task_assignments ta ON ht.id = ta.task_id
            LEFT JOIN task_completions tc ON ta.id = tc.assignment_id
            GROUP BY category
        ''')
        task_stats = cursor.fetchall()
        
        # XP analytics
        cursor.execute('''
            SELECT action_type, COUNT(*) as transaction_count,
                   SUM(entropy_delta) as total_xp,
                   AVG(entropy_delta) as avg_xp
            FROM household_xp_transactions
            GROUP BY action_type
        ''')
        xp_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            "inventory_analytics": {
                "by_category": [
                    {
                        "category": row[0],
                        "item_count": row[1],
                        "low_stock_count": row[2]
                    }
                    for row in inventory_stats
                ]
            },
            "task_analytics": {
                "by_category": [
                    {
                        "category": row[0],
                        "total_tasks": row[1],
                        "avg_quality": row[2] or 0,
                        "total_xp": row[3] or 0
                    }
                    for row in task_stats
                ]
            },
            "xp_analytics": {
                "by_action_type": [
                    {
                        "action_type": row[0],
                        "transaction_count": row[1],
                        "total_xp": row[2],
                        "avg_xp": row[3]
                    }
                    for row in xp_stats
                ]
            }
        }

# Global integration instance
integration = HomeFlowIntegration()

# Integration functions for HomeFlow
async def initialize_integration(email: str, password: str = None, token: str = None) -> bool:
    """Initialize the unified integration"""
    return await integration.authenticate_user(email, password, token)

async def track_chore_completion(chore_data: Dict[str, Any]) -> Optional[str]:
    """Track chore completion XP"""
    activity_data = {
        **chore_data,
        "activity_type": "chore_completion"
    }
    return await integration.track_household_activity(activity_data)

async def track_inventory_management(inventory_data: Dict[str, Any]) -> Optional[str]:
    """Track inventory management XP"""
    activity_data = {
        **inventory_data,
        "activity_type": "inventory_management"
    }
    return await integration.track_household_activity(activity_data)

async def track_meal_preparation(meal_data: Dict[str, Any]) -> Optional[str]:
    """Track meal preparation XP"""
    activity_data = {
        **meal_data,
        "activity_type": "meal_preparation"
    }
    return await integration.track_household_activity(activity_data)

async def track_health_optimization(health_data: Dict[str, Any]) -> Optional[str]:
    """Track health optimization XP"""
    activity_data = {
        **health_data,
        "activity_type": "health_optimization"
    }
    return await integration.track_household_activity(activity_data)

async def create_household_task_in_signalflow(task_data: Dict[str, Any]) -> Optional[str]:
    """Create household task in SignalFlow"""
    return await integration.create_signalflow_task(task_data)

def get_integration_status() -> Dict[str, Any]:
    """Get integration status"""
    return {
        "authenticated": integration.auth_token is not None,
        "user": integration.user_data,
        "household_analytics": integration.get_household_analytics()
    }

if __name__ == "__main__":
    # Test the integration
    async def test_integration():
        # Test authentication
        success = await initialize_integration("family@xpengine.org", token="test-token")
        print(f"Authentication: {'Success' if success else 'Failed'}")
        
        if success:
            # Test chore completion tracking
            chore_data = {
                "task_id": "test-task-1",
                "name": "Clean Kitchen",
                "category": "Kitchen",
                "difficulty": 2.0,
                "quality_score": 0.9,
                "estimated_time": 30,
                "actual_time": 25,
                "skill_gap": 0.2,
                "family_impact": 1.2
            }
            
            xp_id = await track_chore_completion(chore_data)
            print(f"Chore Completion XP Transaction ID: {xp_id}")
            
            # Test inventory management
            inventory_data = {
                "action": "restock_pantry",
                "organization_score": 0.95,
                "accuracy_score": 0.9,
                "automation_level": 0.3,
                "cost_optimization": 1.1,
                "waste_reduction": 1.2
            }
            
            inventory_xp_id = await track_inventory_management(inventory_data)
            print(f"Inventory Management XP Transaction ID: {inventory_xp_id}")
            
            # Get analytics
            status = get_integration_status()
            print(f"Household Analytics: {status}")
    
    asyncio.run(test_integration())