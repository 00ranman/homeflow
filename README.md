# HomeFlow - Complete Household Coordination System

A comprehensive physics-based household management platform that integrates seamlessly with the Extropy unified ecosystem, transforming how families coordinate daily life through measurable value creation.

## Ecosystem Integration

> **Ecosystem Note:** This is the standalone Python service. The deployed TypeScript equivalent lives in the [extropy-engine](https://github.com/00ranman/extropy-engine) monorepo at `packages/homeflow` (port 4015).
>
> See [ECOSYSTEM_MAP.md](https://github.com/00ranman/extropy-engine/blob/main/ECOSYSTEM_MAP.md) for the full repository mapping.


## 🏠 Vision

HomeFlow revolutionizes household management by bringing physics-based coordination to family life:

- **Complete Inventory Tracking**: From toilet paper to q-tips, track everything
- **Intelligent Meal Planning**: AI-powered nutrition optimization for families
- **Skill-Based Chore Management**: Tasks matched to capabilities and development goals
- **Camera-Based Monitoring**: Privacy-preserving visual tracking with Coral dev boards
- **Physics-Based XP Rewards**: Measurable value creation for household contributions
- **Unified Ecosystem Integration**: Seamless connection with SignalFlow and LevelUp Academy

## ⚛️ Physics-Based Household Coordination

### Core XP Formulas

HomeFlow calculates entropy reduction for different household activities:

#### Chore Completion XP
```
Chore_XP = base_entropy × difficulty × skill_bonus × quality × efficiency × consistency × family_impact
```

#### Inventory Management XP
```
Inventory_XP = base_entropy × organization_score × accuracy × automation_bonus × cost_optimization × waste_reduction
```

#### Meal Preparation XP
```
Meal_XP = base_entropy × nutrition_score × complexity × satisfaction × waste_reduction × time_efficiency × cost_effectiveness
```

#### Health Optimization XP
```
Health_XP = base_entropy × dietary_improvement × exercise_integration × wellness_score × long_term_impact
```

### Causal Closure Speeds by Domain

- **Chore Completion**: c_L = 10⁵ (behavioral domain)
- **Inventory Management**: c_L = 10⁴ (economic/organizational domain)
- **Meal Preparation**: c_L = 10⁶ (cognitive domain - planning and creativity)
- **Health Optimization**: c_L = 10³ (social domain - family wellbeing)
- **Automation Setup**: c_L = 10² (technical domain - long-term efficiency)

## 🏗️ System Architecture

### Core Services

```
HomeFlow Ecosystem (Port 3005)
├── Unified Integration
│   ├── Authentication Service (Port 3002)
│   ├── XP Ledger Service (Port 3001)
│   └── API Gateway (Port 3000)
├── Platform Integration
│   ├── SignalFlow Tasks (Port 3003)
│   └── LevelUp Academy Skills (Port 3004)
├── Household Management
│   ├── Complete Inventory System
│   ├── Intelligent Meal Planning
│   ├── Comprehensive Chore Management
│   └── Family Health Optimization
└── Smart Monitoring
    ├── Coral Device Integration
    ├── Camera-Based Tracking
    └── Consumption Forecasting
```

### Database Schema

```sql
-- Complete household inventory
household_inventory        -- All items from food to toiletries
consumption_patterns      -- Usage tracking and predictions
purchase_history          -- Cost analysis and vendor tracking

-- Comprehensive task management
household_tasks           -- All possible household tasks
task_assignments         -- Current and scheduled assignments
task_completions        -- XP-eligible completion tracking
skill_task_mapping      -- Required skills per task type

-- Family capabilities
family_skills           -- LevelUp Academy skill integration
family_health_profiles  -- Individual health and nutrition data

-- Camera integration
coral_devices          -- Visual monitoring device network
detection_events       -- Item recognition and activity tracking
inventory_updates      -- Automated inventory adjustments

-- Smart scheduling
planned_events         -- Calendar integration for consumption
consumption_forecasts  -- Predictive usage modeling
automated_orders      -- Smart shopping and reordering
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- SQLite database
- Access to Extropy unified services
- Optional: Coral dev boards for visual monitoring

### Installation

1. **Setup HomeFlow System**
```bash
cd /Users/randallgossett/homeflow

# Install dependencies
pip install aiohttp aiohttp-cors sqlite3 asyncio

# Start the service
python homeflow_service.py
```

2. **Test the Integration**
```bash
# Run the unified integration test
python unified_integration.py
```

3. **Setup Coral Devices (Optional)**
```bash
# Test camera integration
python coral_integration.py
```

### Authentication

Connect to the unified ecosystem:

```python
# Authenticate with xpengine.org account
success = await initialize_integration("family@xpengine.org", password="your_password")

# Or use existing token
success = await initialize_integration("family@xpengine.org", token="existing_token")
```

## 📊 Complete Household Features

### 1. Universal Inventory Management

Track **everything** in your household:

#### Categories Covered
- **Food & Beverages**: Fresh, pantry, frozen items
- **Personal Care**: Toiletries, hygiene products, medications
- **Cleaning Supplies**: Detergents, tools, paper products
- **Household Items**: Batteries, light bulbs, office supplies
- **Maintenance**: Tools, hardware, seasonal items

#### Smart Features
- **Barcode Scanning**: Easy item addition and tracking
- **Automatic Reorder Alerts**: Never run out of essentials
- **Consumption Prediction**: AI-powered usage forecasting
- **Cost Optimization**: Budget tracking and vendor comparison
- **Expiration Monitoring**: Reduce waste with smart alerts

```python
# Add inventory item with complete tracking
item_data = {
    "name": "Toilet Paper",
    "category": "Personal Care",
    "quantity": 12,
    "unit": "rolls",
    "location": "Bathroom Closet",
    "reorder_level": 4,
    "brand": "Charmin",
    "cost": 15.99,
    "barcode": "123456789"
}

await add_inventory_item(item_data)
```

### 2. Intelligent Meal Planning & Nutrition

Building upon the existing meal planner with advanced health optimization:

#### Enhanced Features
- **Family Health Profiles**: Individual dietary needs and restrictions
- **AI Nutritionist**: Automated meal suggestions based on health goals
- **Inventory Integration**: Meal planning using available ingredients
- **Preparation Skill Matching**: Recipes matched to family cooking abilities
- **Cost-Conscious Planning**: Budget-aware meal optimization

#### Nutrition Analysis
- **Real-time Nutritional Tracking**: Macros, vitamins, minerals
- **Family Member Customization**: Age and activity-based requirements
- **Health Goal Integration**: Weight management, fitness, medical needs
- **Meal Prep Optimization**: Time and nutrition efficiency

```python
# Track meal preparation with XP rewards
meal_data = {
    "meal_name": "Healthy Family Dinner",
    "nutrition_score": 0.92,
    "complexity": 1.8,
    "family_satisfaction": 0.95,
    "waste_reduction": 1.2,
    "time_efficiency": 1.1,
    "cost_effectiveness": 1.05
}

xp_id = await track_meal_preparation(meal_data)
```

### 3. Comprehensive Chore Management

Skill-based task distribution with progressive development:

#### Task Categories
- **Daily Tasks**: Dishwashing, tidying, basic cleaning
- **Weekly Tasks**: Vacuuming, bathroom cleaning, laundry
- **Monthly Tasks**: Deep cleaning, organization, maintenance
- **Seasonal Tasks**: Yard work, holiday preparation, storage

#### Skill Integration
- **LevelUp Academy Sync**: Import skill levels from educational platform
- **Progressive Development**: Tasks that build capabilities over time
- **Age-Appropriate Assignment**: Safe and suitable task matching
- **Skill Gap Analysis**: Identify learning opportunities

#### Smart Assignment
- **Availability Matching**: Calendar integration for optimal scheduling
- **Load Balancing**: Fair distribution across family members
- **Emergency Redistribution**: Automatic reassignment when needed
- **Performance Tracking**: Quality scores and improvement metrics

```python
# Complete chore with skill development tracking
chore_data = {
    "task_id": "clean_kitchen",
    "name": "Deep Clean Kitchen",
    "category": "Kitchen",
    "difficulty": 2.2,
    "quality_score": 0.9,
    "estimated_time": 45,
    "actual_time": 38,
    "skill_gap": 0.3,  # Learning new techniques
    "family_impact": 1.4,
    "consistency_score": 1.2
}

xp_id = await track_chore_completion(chore_data)
```

### 4. Camera-Based Visual Monitoring

Privacy-preserving Coral dev board integration:

#### Monitoring Capabilities
- **Inventory Quantity Tracking**: Visual detection of item levels
- **Quality Assessment**: Freshness and condition monitoring
- **Activity Pattern Recognition**: Household behavior insights
- **Automated Inventory Updates**: Real-time stock level adjustments

#### Privacy Features
- **On-Device Processing**: No cloud image transmission
- **Configurable Zones**: Control what areas are monitored
- **Privacy Mode**: Temporary monitoring suspension
- **Data Retention Control**: Automatic deletion of old data

```python
# Register Coral device for kitchen monitoring
device_data = {
    "device_name": "Kitchen Monitor",
    "location": "Kitchen",
    "capabilities": ["inventory_tracking", "quantity_estimation"],
    "detection_zones": [
        {"name": "Pantry", "x": 0, "y": 0, "width": 100, "height": 100},
        {"name": "Refrigerator", "x": 100, "y": 0, "width": 100, "height": 100}
    ]
}

device_id = await register_coral_device(device_data)
```

### 5. Health & Wellness Optimization

Family-wide health coordination:

#### Health Tracking
- **Individual Profiles**: Age, activity level, health goals
- **Dietary Management**: Restrictions, allergies, preferences
- **Nutrition Goals**: Macro and micronutrient targeting
- **Activity Integration**: Exercise and lifestyle coordination

#### Wellness Features
- **Meal Health Scoring**: Nutritional quality assessment
- **Family Wellness Dashboard**: Collective health metrics
- **Health Goal Tracking**: Progress toward individual objectives
- **Medical Condition Support**: Specialized dietary management

```python
# Track health optimization activity
health_data = {
    "activity_type": "family_nutrition_planning",
    "description": "Planned week of heart-healthy meals",
    "dietary_improvement": 1.3,
    "exercise_integration": 1.1,
    "family_wellness_score": 0.88,
    "long_term_impact": 1.4
}

xp_id = await track_health_optimization(health_data)
```

## 🔌 API Endpoints

### Authentication & Status
```
POST /api/auth/login             # Authenticate with unified system
GET  /api/auth/status            # Check authentication status
GET  /api/health                 # Service health check
```

### Complete Inventory Management
```
GET  /api/inventory              # Get household inventory
POST /api/inventory/add          # Add inventory item
PUT  /api/inventory/{item_id}    # Update inventory item
DELETE /api/inventory/{item_id}  # Remove inventory item
GET  /api/inventory/low-stock    # Get items needing reorder
POST /api/inventory/barcode-scan # Process barcode scan
```

### Advanced Meal Planning
```
GET  /api/meals/plans            # Get meal plans
POST /api/meals/plan             # Create meal plan
GET  /api/meals/nutrition-analysis # Nutritional analysis
POST /api/meals/prep-session     # Track meal preparation
GET  /api/meals/suggestions      # AI meal suggestions
```

### Comprehensive Chore Management
```
GET  /api/chores                 # Get household tasks
POST /api/chores/assign          # Assign task to family member
POST /api/chores/complete        # Complete task with XP tracking
GET  /api/chores/assignments     # Get current assignments
POST /api/chores/create-signalflow # Create SignalFlow task
```

### Family Skills & Capabilities
```
GET  /api/family/skills          # Get family skill levels
POST /api/family/skills/update   # Update skill progression
GET  /api/family/skill-recommendations # Get skill development suggestions
```

### Camera & Device Integration
```
GET  /api/devices                # Get Coral devices
POST /api/devices/register       # Register new device
GET  /api/devices/{id}/status    # Get device status
POST /api/devices/detection-event # Process detection event
```

### Consumption & Forecasting
```
GET  /api/consumption/patterns   # Get usage patterns
POST /api/consumption/forecast   # Create consumption forecast
GET  /api/consumption/calendar-events # Get planned events
POST /api/consumption/event      # Add calendar event
```

### Shopping & Ordering
```
GET  /api/shopping/list          # Generate shopping list
POST /api/shopping/order         # Create automated order
GET  /api/shopping/orders        # Get order history
```

### Health & Nutrition
```
GET  /api/health/profiles        # Get family health profiles
POST /api/health/profile         # Update health profile
GET  /api/health/recommendations # Get health suggestions
POST /api/health/track-activity  # Track health activity
```

### Analytics & Dashboard
```
GET  /api/analytics/dashboard    # Household dashboard
GET  /api/analytics/xp-summary   # XP earnings summary
GET  /api/analytics/efficiency   # Efficiency metrics
```

### XP Tracking
```
POST /api/xp/track              # Manual XP tracking
GET  /api/xp/leaderboard        # Family XP leaderboard
```

### Real-time Updates
```
WS   /ws/{user_id}              # WebSocket for live updates
```

## 🌐 Unified Ecosystem Integration

### SignalFlow Task Distribution

Automatic task creation and management:

```python
# Create household task in SignalFlow
task_data = {
    "name": "Weekly Bathroom Cleaning",
    "description": "Deep clean all bathrooms",
    "difficulty": 2.5,
    "assigned_to": "family_member_id",
    "due_date": "2024-01-15T10:00:00Z",
    "priority": "normal",
    "xp_base_reward": 25.0
}

signalflow_task_id = await create_household_task_in_signalflow(task_data)
```

### LevelUp Academy Skill Sync

Import and track skill development:

- **Skill Level Import**: Automatic sync of capabilities from educational platform
- **Task-Skill Matching**: Assignments based on current skill levels
- **Progressive Development**: Tasks that challenge and build abilities
- **Achievement Integration**: Household tasks contributing to learning goals

### XP Ledger Integration

Physics-based value measurement:

- **Automatic XP Tracking**: All household activities generate XP transactions
- **Cross-Platform XP**: Household contributions count toward unified totals
- **XP Economy**: Household XP represents verified entropy reduction
- **Family Leaderboards**: Healthy competition and recognition

## 📱 Real-time Updates

### WebSocket Integration

Live household coordination:

```javascript
// Connect to HomeFlow updates
const ws = new WebSocket('ws://localhost:3005/ws/USER_ID');

// Handle household events
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  switch(message.type) {
    case 'household_update':
      updateHouseholdDashboard(message.update);
      break;
    case 'inventory_alert':
      showLowStockAlert(message.items);
      break;
    case 'task_assigned':
      notifyTaskAssignment(message.task);
      break;
    case 'xp_earned':
      celebrateXPGain(message.xp_amount);
      break;
  }
};
```

### Update Types

- **Inventory Changes**: Stock level updates, reorder alerts
- **Task Updates**: Assignments, completions, redistributions
- **XP Notifications**: Real-time value creation tracking
- **Health Insights**: Nutrition goals, wellness achievements
- **Device Status**: Camera events, detection alerts

## 🔧 Configuration

### Environment Variables

```bash
# Service configuration
HOMEFLOW_PORT=3005
DEBUG=false

# Integration endpoints
AUTH_SERVICE_URL=http://localhost:3002
XP_LEDGER_URL=http://localhost:3001
GATEWAY_URL=http://localhost:3000
SIGNALFLOW_URL=http://localhost:3003
LEVELUP_URL=http://localhost:3004

# Camera integration
CORAL_DEVICES_ENABLED=true
PRIVACY_MODE_DEFAULT=false
DATA_RETENTION_DAYS=7
```

### Household Settings

```python
# Customize XP calculation parameters
XP_SETTINGS = {
    "chore_base_entropy": 12.0,
    "inventory_base_entropy": 8.0,
    "meal_base_entropy": 10.0,
    "health_base_entropy": 15.0,
    "skill_development_bonus": 0.5,
    "family_impact_multiplier": 1.2
}

# Privacy controls
PRIVACY_SETTINGS = {
    "camera_zones_required": True,
    "data_retention_days": 7,
    "automatic_deletion": True,
    "person_detection_enabled": False,  # For activity patterns only
    "image_storage": False  # Only metadata stored
}
```

## 🧪 Testing the System

### Complete Integration Test

```bash
# Run comprehensive HomeFlow test
python homeflow_service.py --test-mode
```

### Manual Testing

```python
import asyncio
from unified_integration import *

async def test_homeflow():
    # Authenticate
    await initialize_integration("family@xpengine.org", token="demo-token")
    
    # Test inventory management
    inventory_data = {
        "action": "weekly_inventory_update",
        "organization_score": 0.92,
        "accuracy_score": 0.95,
        "automation_level": 0.4,
        "cost_optimization": 1.1,
        "waste_reduction": 1.3
    }
    
    xp_id = await track_inventory_management(inventory_data)
    print(f"Inventory XP: {xp_id}")
    
    # Test chore completion
    chore_data = {
        "task_name": "Deep Clean Bathrooms",
        "difficulty": 2.5,
        "quality_score": 0.88,
        "family_impact": 1.3,
        "skill_development": 0.2
    }
    
    chore_xp = await track_chore_completion(chore_data)
    print(f"Chore XP: {chore_xp}")

asyncio.run(test_homeflow())
```

## 📊 Analytics & Insights

### Household Dashboard Metrics

- **Inventory Health**: Stock levels, expiration alerts, cost trends
- **Task Efficiency**: Completion rates, quality scores, time trends
- **Family XP Leaderboard**: Individual contributions and growth
- **Health Progress**: Nutrition goals, wellness improvements
- **System Optimization**: Automation levels, efficiency gains

### Predictive Analytics

- **Consumption Forecasting**: Usage patterns and reorder predictions
- **Seasonal Planning**: Holiday preparation and seasonal adjustments
- **Health Trend Analysis**: Long-term family wellness patterns
- **Cost Optimization**: Budget efficiency and vendor recommendations

## 🔮 Advanced Features

### AI-Powered Household Intelligence

- **Smart Scheduling**: Optimal task timing based on family patterns
- **Predictive Maintenance**: Proactive household care recommendations
- **Health Optimization**: Automated nutrition and wellness suggestions
- **Energy Efficiency**: Consumption pattern optimization

### Future Enhancements

- **Voice Control**: Hands-free household management
- **Mobile App**: On-the-go family coordination
- **IoT Integration**: Smart device ecosystem connection
- **Blockchain XP**: Decentralized value verification

## 📞 Support & Resources

- **Service Health**: `/api/health` for system status
- **API Documentation**: Interactive docs at `/api/docs`
- **WebSocket Testing**: `/ws/test` for connection verification
- **Family Dashboard**: Real-time household insights

## 📄 License

Proprietary - Extropy Technologies LLC

---

**🏠 HomeFlow - Physics-Based Household Coordination**

*Transforming family life through measurable value creation and intelligent automation*

### Key Benefits

✅ **Complete Household Tracking** - From toilet paper to q-tips  
✅ **Intelligent Meal Planning** - AI-powered nutrition optimization  
✅ **Skill-Based Chore Management** - Progressive family development  
✅ **Camera-Based Monitoring** - Privacy-preserving visual tracking  
✅ **Physics-Based XP Rewards** - Measurable household contributions  
✅ **Unified Ecosystem Integration** - Seamless family coordination  

**Transform your household into a physics-based coordination system where every contribution creates measurable value for the family.**
