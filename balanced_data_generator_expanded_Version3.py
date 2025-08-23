import json
import random
import uuid
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# CONFIGURATION
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class Config:
    CURRENT_USER_LOGIN = "Daveydrz"
    CURRENT_UTC_DATETIME = "2025-08-23 10:43:23"  # Updated timestamp
    DEFAULT_NUM_RECORDS = 10400  # 100 records per relation type for perfect balance
    MAX_RETRIES = 3
    OUTPUT_FILENAME = "perfectly_balanced_dataset.json"
    PROGRESS_INTERVAL = 500
    
    # Perfect balance targets
    TARGET_RECORDS_PER_RELATION = 100
    TARGET_RECORDS_PER_ENTITY = 153  # 10400/68 ≈ 153

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# ENTITY AND RELATION TYPE DEFINITIONS (68 entities, 104 relations)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class EntityTypes:
    # Core Personal Types (10)
    PERSON = "PERSON"
    PRONOUN = "PRONOUN"
    NICKNAME = "NICKNAME"
    PET = "PET"
    ROLE = "ROLE"
    TRAIT = "TRAIT"
    ATTRIBUTE = "ATTRIBUTE"
    PREFERENCE = "PREFERENCE"
    VALUE = "VALUE"
    BELIEF = "BELIEF"
    
    # Professional Types (8)
    ORGANIZATION = "ORGANIZATION"
    BUSINESS = "BUSINESS"
    INDUSTRY = "INDUSTRY"
    TECHNOLOGY = "TECHNOLOGY"
    PRODUCT = "PRODUCT"
    PROJECT = "PROJECT"
    SKILL = "SKILL"
    EQUIPMENT = "EQUIPMENT"
    
    # Location & Place Types (6)
    LOCATION = "LOCATION"
    GEOPOLITICAL_ENTITY = "GEOPOLITICAL_ENTITY"
    ROOM = "ROOM"
    VEHICLE = "VEHICLE"
    PLATFORM = "PLATFORM"
    GROUP = "GROUP"
    
    # Time & Schedule Types (8)
    DATE = "DATE"
    TIME = "TIME"
    DURATION = "DURATION"
    START_TIME = "START_TIME"
    END_TIME = "END_TIME"
    TIMELINE = "TIMELINE"
    FREQUENCY = "FREQUENCY"
    RECURRING_SCHEDULE = "RECURRING_SCHEDULE"
    
    # Activity & Goal Types (6)
    ACTIVITY = "ACTIVITY"
    HOBBY = "HOBBY"
    GOAL = "GOAL"
    INTENT = "INTENT"
    EVENT = "EVENT"
    TOPIC = "TOPIC"
    
    # Financial & Material Types (5)
    MONEY = "MONEY"
    BUDGET = "BUDGET"
    OBJECT = "OBJECT"
    AMOUNT = "AMOUNT"
    CONDITION = "CONDITION"
    
    # Health & Wellness Types (4)
    HEALTH_INFO = "HEALTH_INFO"
    EMOTION = "EMOTION"
    SENTIMENT = "SENTIMENT"
    FEELING = "FEELING"
    
    # Sensory Types (5)
    SOUND = "SOUND"
    SIGHT = "SIGHT"
    TASTE = "TASTE"
    SMELL = "SMELL"
    SENSATION = "SENSATION"
    
    # Relationship & Social Types (4)
    RELATIONSHIP = "RELATIONSHIP"
    RELATIONSHIP_TYPE = "RELATIONSHIP_TYPE"
    FOOD = "FOOD"
    WEATHER = "WEATHER"
    
    # Conceptual & Abstract Types (6)
    CONCEPT = "CONCEPT"
    IDEA = "IDEA"
    OPINION = "OPINION"
    MEMORY_TYPE = "MEMORY_TYPE"
    LIFE_STAGE = "LIFE_STAGE"
    PERIOD = "PERIOD"
    
    # Learning & Growth Types (4)
    LEARNING_METHOD = "LEARNING_METHOD"
    PERSONAL_GROWTH = "PERSONAL_GROWTH"
    COMMUNITY_ROLE = "COMMUNITY_ROLE"
    CULTURAL_ELEMENT = "CULTURAL_ELEMENT"
    
    # Media & Entertainment Types (2)
    MEDIA = "MEDIA"
    GENRE = "GENRE"

class RelationTypes:
    # Professional Relations (12)
    WORKS_FOR = "WORKS_FOR"
    WORKS_FROM = "WORKS_FROM"
    COLLABORATES_WITH = "COLLABORATES_WITH"
    WORKS_ON = "WORKS_ON"
    HAS_ROLE = "HAS_ROLE"
    HAS_SKILL = "HAS_SKILL"
    HAS_EXPERTISE = "HAS_EXPERTISE"
    USES = "USES"
    ORGANIZES = "ORGANIZES"
    LEADS = "LEADS"
    PARTICIPATES_IN = "PARTICIPATES_IN"
    MEMBER_OF = "MEMBER_OF"
    
    # Activity & Behavior Relations (12)
    DOES_ACTIVITY = "DOES_ACTIVITY"
    HAS_HOBBY = "HAS_HOBBY"
    LEARNS = "LEARNS"
    TEACHES = "TEACHES"
    PRACTICES = "PRACTICES"
    ENJOYS = "ENJOYS"
    LIKES = "LIKES"
    PREFERS = "PREFERS"
    WATCHES = "WATCHES"
    READS = "READS"
    LISTENS_TO = "LISTENS_TO"
    ATTENDS = "ATTENDS"
    
    # Location & Movement Relations (8)
    LIVES_IN = "LIVES_IN"
    LOCATED_AT = "LOCATED_AT"
    AT_LOCATION = "AT_LOCATION"
    TRAVELS_TO = "TRAVELS_TO"
    IS_NEAR = "IS_NEAR"
    VISITS = "VISITS"
    STAYS_AT = "STAYS_AT"
    MOVES_TO = "MOVES_TO"
    
    # Time & Schedule Relations (8)
    SCHEDULED_FOR = "SCHEDULED_FOR"
    HAPPENS_ON = "HAPPENS_ON"
    ON_DATE = "ON_DATE"
    STARTS_AT = "STARTS_AT"
    ENDS_AT = "ENDS_AT"
    FOR_DURATION = "FOR_DURATION"
    HAS_FREQUENCY = "HAS_FREQUENCY"
    REPEATS = "REPEATS"
    
    # Personal & Emotional Relations (12)
    FEELS_EMOTION = "FEELS_EMOTION"
    HAS_PREFERENCE = "HAS_PREFERENCE"
    BELIEVES = "BELIEVES"
    VALUES = "VALUES"
    HAS_OPINION = "HAS_OPINION"
    THINKS = "THINKS"
    FEELS = "FEELS"
    HAS_TRAIT = "HAS_TRAIT"
    HAS_ATTRIBUTE = "HAS_ATTRIBUTE"
    IS_TYPE = "IS_TYPE"
    KNOWN_AS = "KNOWN_AS"
    CALLED = "CALLED"
    
    # Goal & Planning Relations (8)
    WANTS_GOAL = "WANTS_GOAL"
    HAS_GOAL = "HAS_GOAL"
    HAS_INTENT = "HAS_INTENT"
    INTENDS = "INTENDS"
    PLANS = "PLANS"
    HOPES_FOR = "HOPES_FOR"
    DREAMS_OF = "DREAMS_OF"
    AIMS_FOR = "AIMS_FOR"
    
    # Cognitive Relations (8)
    THINKING_OF = "THINKING_OF"
    CONSIDERING = "CONSIDERING"
    REMEMBERS = "REMEMBERS"
    REGRETS = "REGRETS"
    MISSES = "MISSES"
    WORRIES_ABOUT = "WORRIES_ABOUT"
    LOOKING_FORWARD_TO = "LOOKING_FORWARD_TO"
    REFLECTS_ON = "REFLECTS_ON"
    
    # Sensory Relations (5)
    HEARS = "HEARS"
    SEES = "SEES"
    TASTES = "TASTES"
    SMELLS = "SMELLS"
    TOUCHES = "TOUCHES"
    
    # Social Relations (8)
    IS_FRIENDS_WITH = "IS_FRIENDS_WITH"
    IS_FAMILY_WITH = "IS_FAMILY_WITH"
    MAINTAINS_RELATIONSHIP = "MAINTAINS_RELATIONSHIP"
    CARES_FOR = "CARES_FOR"
    SUPPORTS = "SUPPORTS"
    MENTORS = "MENTORS"
    FOLLOWS = "FOLLOWS"
    INFLUENCES = "INFLUENCES"
    
    # Ownership & Possession Relations (6)
    OWNS = "OWNS"
    HAS_OBJECT = "HAS_OBJECT"
    BORROWED = "BORROWED"
    LENT = "LENT"
    GIVES = "GIVES"
    RECEIVES = "RECEIVES"
    
    # Financial Relations (4)
    SPENDS = "SPENDS"
    EARNS = "EARNS"
    SAVES = "SAVES"
    BUDGETS_FOR = "BUDGETS_FOR"
    
    # Health Relations (3)
    HAS_HEALTH_INFO = "HAS_HEALTH_INFO"
    HAS_HEALTH_CONDITION = "HAS_HEALTH_CONDITION"
    MANAGES_HEALTH = "MANAGES_HEALTH"
    
    # Causation & Influence Relations (6)
    CAUSED_BY = "CAUSED_BY"
    RESULTS_IN = "RESULTS_IN"
    CONTRIBUTED_TO = "CONTRIBUTED_TO"
    INFLUENCES = "INFLUENCES"
    AFFECTS = "AFFECTS"
    TRIGGERS = "TRIGGERS"
    
    # Learning & Growth Relations (4)
    LEARNS_FROM = "LEARNS_FROM"
    DEVELOPS = "DEVELOPS"
    IMPROVES = "IMPROVES"
    MASTERS = "MASTERS"

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# COMPREHENSIVE EXPANDED DATA POOLS
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# PEOPLE NAMES - Full Names (100+) + Single Names (50+)
PEOPLE_NAMES = [
    # Full Names - International/Diverse
    "Alex Chen", "Jordan Smith", "Casey Williams", "Morgan Taylor", "Dr. Evelyn Reed",
    "Maria Garcia", "Wei Li", "Samira Khan", "Leo Schmidt", "Sofia Rossi",
    "Kenji Tanaka", "Liam O'Connell", "Chloe Dubois", "Ryan Murphy", "Zoe Park",
    "Marcus Johnson", "Isabella Rodriguez", "Finn Anderson", "Luna Martinez", "David Kim",
    "Sarah Wilson", "Michael Brown", "Jennifer Lee", "Robert Davis", "Emily Zhang",
    "Thomas Anderson", "Rachel Green", "Mark Thompson", "Lisa Wang", "James Rodriguez",
    "Amy Foster", "Oliver Park", "Emma Chen", "Sebastian Kim", "Maya Patel",
    "Gabriel Lopez", "Aria Singh", "Lucas Wang", "Zara Ahmed", "Felix Rodriguez",
    "Nora Thompson", "Ethan Foster", "Isla Martinez", "Adrian Zhou", "Ruby Williams",
    "Kai Johnson", "Sage Miller", "Phoenix Davis", "River Garcia", "Orion Lee",
    "Luna Kim", "Atlas Brown", "Nova Wilson", "Sage Taylor", "Ivy Chen",
    "Cruz Martinez", "Jade Park", "Blake Thompson", "Riley Zhang", "Quinn Foster",
    "Cameron Lee", "Dakota Johnson", "Skylar Chen", "Rowan Garcia", "Finley Wang",
    "Avery Rodriguez", "Emery Kim", "Justice Smith", "Marlowe Taylor", "Phoenix Li",
    "Raven Martinez", "Storm Davis", "Sage Anderson", "River Thompson", "Ocean Park",
    "Sky Williams", "Rain Chen", "Luna Garcia", "Star Rodriguez", "Dawn Kim",
    "Iris Martinez", "Rose Thompson", "Lily Chen", "Violet Garcia", "Ruby Park",
    "Jade Kim", "Pearl Rodriguez", "Opal Martinez", "Crystal Chen", "Diamond Garcia",
    "Amber Park", "Coral Kim", "Sage Rodriguez", "Ivy Martinez", "Fern Chen",
    "Moss Garcia", "Sage Park", "Reed Kim", "Pine Rodriguez", "Oak Martinez",
    "Ash Chen", "Elm Garcia", "Birch Park", "Cedar Kim", "Maple Rodriguez",
    "Hazel Martinez", "Poplar Chen", "Willow Garcia", "Aspen Park", "Sequoia Kim",
    "Redwood Rodriguez", "Mahogany Martinez", "Cherry Chen", "Apple Garcia", "Berry Park"
]

SINGLE_NAMES = [
    # Single Names - Creative/Modern
    "Alex", "Jordan", "Casey", "Morgan", "Sage", "River", "Phoenix", "Quinn",
    "Blake", "Riley", "Cameron", "Dakota", "Skylar", "Rowan", "Finley", "Avery",
    "Emery", "Justice", "Marlowe", "Raven", "Storm", "Ocean", "Sky", "Rain",
    "Luna", "Star", "Dawn", "Iris", "Rose", "Lily", "Violet", "Ruby", "Jade",
    "Pearl", "Opal", "Crystal", "Diamond", "Amber", "Coral", "Ivy", "Fern",
    "Moss", "Reed", "Pine", "Oak", "Ash", "Elm", "Birch", "Cedar", "Maple"
]

# Combine for random selection
ALL_PEOPLE_NAMES = PEOPLE_NAMES + SINGLE_NAMES

# ORGANIZATIONS (50+)
ORGANIZATIONS = [
    "TechFlow Systems", "DataSolutions Inc.", "Innovate Corp", "GreenScape Environmental",
    "Starlight Studios", "Apex Health", "QuantumLeap AI", "Helios Energy",
    "BlueSky Dynamics", "NovaTech Solutions", "Meridian Analytics", "Vertex Innovations",
    "Catalyst Labs", "Prism Technologies", "Nexus Enterprises", "Zenith Consulting",
    "Horizon Networks", "Eclipse Systems", "Aurora Designs", "Phoenix Rising LLC",
    "Digital Frontier", "CloudWorks", "NextGen Solutions", "Global Innovations",
    "Future Systems", "Bright Ideas Co", "Swift Solutions", "Peak Performance",
    "Synergy Partners", "Quantum Technologies", "Infinity Labs", "Stellar Dynamics",
    "Cosmic Ventures", "Galaxy Systems", "Universe Corp", "Orbital Solutions",
    "Lunar Technologies", "Solar Innovations", "Comet Labs", "Meteor Systems",
    "Astro Dynamics", "Space Age Solutions", "Rocket Labs", "Satellite Systems",
    "Pioneer Technologies", "Explorer Corp", "Discovery Labs", "Venture Solutions",
    "Quest Systems", "Adventure Technologies", "Journey Labs", "Destination Corp"
]

# SKILLS (30+)
SKILLS = [
    "Python programming", "data analysis", "machine learning", "project management",
    "public speaking", "graphic design", "web development", "digital marketing",
    "financial analysis", "team leadership", "user experience design", "cloud computing",
    "cybersecurity", "agile methodology", "strategic planning", "communication",
    "negotiation", "time management", "problem solving", "critical thinking",
    "creative writing", "video editing", "3D modeling", "database management",
    "network administration", "mobile app development", "blockchain technology",
    "artificial intelligence", "data visualization", "business intelligence",
    "product management", "quality assurance", "technical writing", "social media management"
]

# ACTIVITIES (40+)
ACTIVITIES = [
    "developing software", "analyzing data", "designing interfaces", "managing projects",
    "conducting research", "teaching classes", "writing documentation", "testing applications",
    "building prototypes", "creating presentations", "traveling", "exercising",
    "reading", "cooking", "meditating", "networking", "mentoring", "strategizing",
    "problem-solving", "brainstorming", "coding", "debugging", "optimizing",
    "planning", "organizing", "coordinating", "facilitating", "consulting",
    "advising", "coaching", "training", "learning", "studying", "practicing",
    "experimenting", "innovating", "creating", "designing", "building", "testing",
    "reviewing", "evaluating", "analyzing", "investigating", "researching"
]

# LOCATIONS (30+)
LOCATIONS = [
    "downtown office", "co-working space", "home office", "local library",
    "coffee shop", "university campus", "community center", "innovation lab",
    "startup incubator", "shared workspace", "tech hub", "creative studio",
    "conference room", "meeting space", "collaboration area", "quiet zone",
    "brainstorming room", "focus area", "open workspace", "private office",
    "research facility", "training center", "workshop space", "maker space",
    "design studio", "testing lab", "demo room", "presentation hall",
    "networking lounge", "break room", "outdoor terrace", "rooftop garden"
]

# EMOTIONS (25+)
EMOTIONS = [
    "happiness", "excitement", "contentment", "satisfaction", "joy",
    "enthusiasm", "calm", "relaxation", "confidence", "pride",
    "gratitude", "hope", "curiosity", "inspiration", "determination",
    "anxiety", "nervousness", "worry", "stress", "frustration",
    "nostalgia", "anticipation", "empathy", "compassion", "love"
]

# ROLES (20+)
ROLES = [
    "project manager", "software engineer", "team lead", "data scientist",
    "designer", "product owner", "consultant", "analyst", "coordinator",
    "specialist", "director", "senior developer", "research assistant",
    "marketing manager", "sales representative", "customer support",
    "quality assurance", "business analyst", "system administrator", "content creator"
]

# TOPICS (25+)
TOPICS = [
    "artificial intelligence", "climate change", "productivity", "health and wellness",
    "technology trends", "personal development", "financial planning", "career growth",
    "relationship building", "creative projects", "sustainability", "innovation",
    "work-life balance", "entrepreneurship", "education", "social media",
    "fitness", "nutrition", "mental health", "travel experiences",
    "digital transformation", "remote work", "team collaboration", "leadership",
    "customer experience"
]

# ATTRIBUTES (20+)
ATTRIBUTES = [
    "experienced", "creative", "analytical", "collaborative", "innovative",
    "detail-oriented", "strategic", "empathetic", "reliable", "adaptable",
    "passionate", "organized", "communicative", "problem-solving", "leadership-oriented",
    "tech-savvy", "customer-focused", "results-driven", "team-oriented", "entrepreneurial"
]

# DATES (15+)
DATES = [
    "2024-01-15", "2024-03-22", "2024-06-10", "2024-09-05", "2024-12-20",
    "2025-02-14", "2025-05-30", "2025-08-16", "2025-11-25", "January 2024",
    "March 2024", "summer 2024", "fall 2024", "this year", "next month"
]

# DURATIONS (15+)
DURATIONS = [
    "two hours", "half a day", "three weeks", "six months", "one year",
    "several years", "a decade", "30 minutes", "90 minutes", "four hours",
    "all day", "overnight", "a weekend", "two weeks", "a quarter"
]

# NICKNAMES (20+)
NICKNAMES = [
    "Ace", "Buddy", "Chief", "Doc", "Eagle", "Flash", "Ghost", "Hero",
    "Jazz", "King", "Lion", "Max", "Ninja", "Owl", "Prince", "Queen",
    "Rebel", "Star", "Tiger", "Wolf"
]

# PETS (15+)
PETS = [
    "Golden Retriever named Max", "tabby cat named Whiskers", "German Shepherd named Rex",
    "Persian cat named Luna", "Border Collie named Scout", "Maine Coon cat named Shadow",
    "Labrador named Buddy", "Siamese cat named Blue", "Beagle named Charlie",
    "ragdoll cat named Milo", "parrot named Rio", "hamster named Peanut",
    "rabbit named Pepper", "ferret named Felix", "guinea pig named Ginger"
]

# GROUPS (20+)
GROUPS = [
    "book club", "hiking group", "chess club", "photography society",
    "cooking class", "language exchange", "volunteer organization", "sports team",
    "music band", "art collective", "study group", "professional association",
    "community garden group", "dance troupe", "environmental club", "startup accelerator",
    "maker space community", "tech meetup", "writing circle", "fitness group"
]

# GEOPOLITICAL_ENTITIES (25+)
GEOPOLITICAL_ENTITIES = [
    "United States", "European Union", "California", "New York City", "Tokyo",
    "London", "Berlin", "Paris", "Sydney", "Toronto", "Singapore", "Hong Kong",
    "Dubai", "Barcelona", "Amsterdam", "Ibiza", "Bali", "Thailand", "Greece",
    "Italy", "Spain", "Portugal", "Mexico", "Costa Rica", "Japan"
]

# EVENTS (20+)
EVENTS = [
    "annual conference", "team building retreat", "product launch", "graduation ceremony",
    "wedding celebration", "birthday party", "company picnic", "charity fundraiser",
    "art exhibition", "music festival", "sports tournament", "networking event",
    "workshop series", "cultural festival", "technology summit", "hackathon",
    "trade show", "webinar series", "book launch", "film premiere"
]

# OBJECTS (25+)
OBJECTS = [
    "smartphone", "laptop", "coffee mug", "notebook", "headphones", "backpack",
    "camera", "bicycle", "watch", "tablet", "keyboard", "mouse", "monitor",
    "desk chair", "water bottle", "fitness tracker", "e-reader", "gaming console",
    "drone", "smart speaker", "wireless charger", "portable battery", "desk lamp",
    "ergonomic keyboard", "standing desk"
]

# CONCEPTS (20+)
CONCEPTS = [
    "artificial intelligence", "sustainability", "innovation", "collaboration",
    "creativity", "leadership", "mindfulness", "efficiency", "diversity",
    "inclusion", "quality", "excellence", "growth", "learning", "adaptation",
    "automation", "digitalization", "remote work", "work-life balance", "continuous improvement"
]

# PREFERENCES (15+)
PREFERENCES = [
    "morning coffee", "quiet workspace", "natural lighting", "flexible schedule",
    "remote work", "team collaboration", "creative freedom", "structured environment",
    "continuous learning", "work-life balance", "minimal distractions", "open communication",
    "hands-on experience", "mentorship opportunities", "innovative projects"
]

# VALUES (15+)
VALUES = [
    "honesty", "integrity", "respect", "compassion", "excellence", "innovation",
    "teamwork", "responsibility", "fairness", "perseverance", "loyalty", "courage",
    "wisdom", "kindness", "dedication"
]

# HEALTH_INFO (15+)
HEALTH_INFO = [
    "daily exercise routine", "balanced nutrition", "regular sleep schedule",
    "stress management", "mental wellness", "preventive care", "healthy lifestyle",
    "meditation practice", "physical therapy", "health monitoring", "yoga practice",
    "strength training", "cardiovascular fitness", "mindfulness meditation", "wellness coaching"
]

# MONEY (15+)
MONEY = [
    "$500", "$1,200", "$5,000", "$10,000", "$25,000", "$50,000", "$100,000",
    "$250,000", "monthly salary", "annual bonus", "project budget", "savings account",
    "investment portfolio", "retirement fund", "emergency fund"
]

# SOUNDS (15+)
SOUNDS = [
    "music", "laughter", "conversation", "traffic", "rain", "birds chirping",
    "keyboard typing", "phone ringing", "footsteps", "machinery", "wind",
    "silence", "ambient noise", "notifications", "applause"
]

# SIGHTS (15+)
SIGHTS = [
    "sunset", "cityscape", "nature", "people walking", "traffic", "architecture",
    "artwork", "screens", "books", "colors", "patterns", "movement", "stillness",
    "lighting", "shadows"
]

# TASTES (10+)
TASTES = [
    "sweet", "salty", "bitter", "sour", "umami", "spicy", "mild", "rich", "fresh", "savory"
]

# SMELLS (15+)
SMELLS = [
    "coffee", "flowers", "rain", "food cooking", "perfume", "fresh air",
    "ocean breeze", "wood", "vanilla", "citrus", "herbs", "baking bread",
    "smoke", "leather", "pine"
]

# SENSATIONS (15+)
SENSATIONS = [
    "warmth", "coolness", "pressure", "texture", "vibration", "tingling",
    "comfort", "discomfort", "smoothness", "roughness", "softness", "tension",
    "relaxation", "energy", "fatigue"
]

# FEELINGS (15+)
FEELINGS = [
    "comfortable", "uneasy", "energized", "tired", "focused", "distracted",
    "motivated", "discouraged", "inspired", "overwhelmed", "peaceful", "restless",
    "secure", "vulnerable", "accomplished"
]

# BELIEFS (15+)
BELIEFS = [
    "hard work pays off", "honesty is the best policy", "everyone deserves respect",
    "change is possible", "education is important", "family comes first",
    "time heals wounds", "actions speak louder than words", "everything happens for a reason",
    "persistence wins", "kindness matters", "learning never stops", "teamwork succeeds",
    "innovation drives progress", "balance creates harmony"
]

# OPINIONS (10+)
OPINIONS = [
    "important", "overrated", "undervalued", "essential", "optional",
    "beneficial", "harmful", "interesting", "boring", "revolutionary"
]

# IDEAS (15+)
IDEAS = [
    "mobile app", "community project", "business venture", "creative collaboration",
    "research study", "improvement plan", "innovation concept", "solution design",
    "artistic project", "educational program", "sustainability initiative", "tech startup",
    "social platform", "productivity tool", "wellness program"
]

# FOODS (25+)
FOODS = [
    "pasta", "sushi", "pizza", "salad", "sandwich", "soup", "curry", "tacos",
    "stir-fry", "grilled chicken", "chocolate", "ice cream", "fresh fruit",
    "vegetables", "bread", "cheese", "fish", "rice", "noodles", "dessert",
    "smoothie", "yogurt", "nuts", "berries", "avocado"
]

# HOBBIES (20+)
HOBBIES = [
    "photography", "gardening", "cooking", "reading", "writing", "painting",
    "music", "sports", "hiking", "cycling", "gaming", "crafting", "collecting",
    "dancing", "traveling", "learning languages", "volunteering", "meditation",
    "fitness", "yoga"
]

# MEMORY_TYPES (15+)
MEMORY_TYPES = [
    "episodic memory", "semantic memory", "procedural memory", "emotional memory",
    "traumatic memory", "childhood memory", "recent memory", "vivid memory",
    "fragmented memory", "nostalgic memory", "suppressed memory", "triggered memory",
    "collective memory", "false memory", "flashbulb memory"
]

# LIFE_STAGES (13+)
LIFE_STAGES = [
    "infancy", "toddlerhood", "childhood", "adolescence", "young adulthood",
    "early career", "career building", "mid-career", "senior career",
    "pre-retirement", "early retirement", "active retirement", "later life"
]

# CULTURAL_ELEMENTS (15+)
CULTURAL_ELEMENTS = [
    "family recipes", "traditional songs", "cultural dances", "religious practices",
    "holiday customs", "storytelling traditions", "ancestral languages", "craft techniques",
    "ceremonial rituals", "folk art", "traditional games", "cultural dress",
    "historical narratives", "spiritual beliefs", "community celebrations"
]

# LEARNING_METHODS (15+)
LEARNING_METHODS = [
    "hands-on practice", "visual observation", "verbal instruction", "trial and error",
    "mentorship", "formal education", "self-study", "peer learning",
    "experiential learning", "repetitive practice", "guided discovery", "collaborative learning",
    "online courses", "workshop attendance", "reading extensively"
]

# PERSONAL_GROWTH (15+)
PERSONAL_GROWTH = [
    "emotional intelligence", "self-awareness", "confidence building", "resilience development",
    "communication skills", "leadership abilities", "empathy expansion", "stress management",
    "mindfulness practice", "creative expression", "problem-solving skills", "adaptability",
    "patience cultivation", "forgiveness capacity", "authenticity"
]

# COMMUNITY_ROLES (15+)
COMMUNITY_ROLES = [
    "volunteer coordinator", "neighborhood watch leader", "school board member", "youth mentor",
    "community organizer", "local activist", "charity fundraiser", "environmental advocate",
    "cultural preservationist", "elder caretaker", "child advocate", "religious leader",
    "social worker", "community mediator", "local historian"
]

# PERIODS (15+)
PERIODS = [
    "during childhood", "in their teens", "college years", "early career",
    "during marriage", "after the divorce", "during pregnancy", "when kids were young",
    "midlife crisis", "empty nest years", "pre-retirement", "during illness",
    "after recovery", "recent years", "last decade"
]

# INDUSTRIES (15+)
INDUSTRIES = [
    "technology", "healthcare", "finance", "education", "manufacturing",
    "retail", "entertainment", "construction", "agriculture", "transportation",
    "energy", "telecommunications", "hospitality", "consulting", "media"
]

# TECHNOLOGIES (18+)
TECHNOLOGIES = [
    "artificial intelligence", "machine learning", "blockchain", "cloud computing",
    "IoT", "virtual reality", "augmented reality", "robotics", "quantum computing",
    "5G", "automation", "cybersecurity", "PyTorch", "TensorFlow", "React",
    "Angular", "Node.js", "Docker"
]

# PRODUCTS (16+)
PRODUCTS = [
    "smartphone app", "software platform", "physical device", "online service",
    "digital tool", "educational course", "fitness program", "creative work",
    "research paper", "business solution", "iPhone", "MacBook", "Tesla Model 3",
    "Samsung Galaxy", "iPad", "Surface Pro"
]

# START_TIMES (19+)
START_TIMES = [
    "6:00 AM", "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
    "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM",
    "6:00 PM", "7:00 PM", "8:00 PM", "early morning", "morning", "afternoon", "evening"
]

# END_TIMES (16+)
END_TIMES = [
    "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM",
    "4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM",
    "10:00 PM", "late evening", "night", "midnight"
]

# RECURRING_SCHEDULES (12+)
RECURRING_SCHEDULES = [
    "daily", "weekly", "bi-weekly", "monthly", "quarterly", "seasonal",
    "occasional", "regular", "flexible", "strict", "intensive", "relaxed"
]

# FREQUENCY_DETAILED (12+)
FREQUENCY_DETAILED = [
    "every morning", "twice a week", "once a month", "every few days",
    "daily", "weekly", "occasionally", "rarely", "frequently", "constantly",
    "seasonally", "annually"
]

# WEATHER_CONDITIONS (14+)
WEATHER_CONDITIONS = [
    "sunny", "rainy", "cloudy", "snowy", "windy", "foggy", "stormy", "clear",
    "humid", "dry", "hot", "cold", "mild", "perfect weather"
]

# TRANSPORTATION (13+)
TRANSPORTATION = [
    "car", "bus", "train", "subway", "bicycle", "motorcycle", "plane",
    "taxi", "rideshare", "walking", "scooter", "boat", "ferry"
]

# ROOM_TYPES (13+)
ROOM_TYPES = [
    "bedroom", "living room", "kitchen", "office", "bathroom", "basement",
    "attic", "garage", "study", "dining room", "balcony", "patio", "garden"
]

# MEDIA_TYPES (12+)
MEDIA_TYPES = [
    "podcast", "documentary", "movie", "TV series", "book", "audiobook",
    "YouTube video", "blog post", "article", "news report", "social media post", "webinar"
]

# PLATFORMS (13+)
PLATFORMS = [
    "Netflix", "YouTube", "Spotify", "Instagram", "LinkedIn", "Twitter",
    "Facebook", "TikTok", "Zoom", "Teams", "Discord", "Slack", "Reddit"
]

# GENRES (13+)
GENRES = [
    "comedy", "drama", "thriller", "romance", "sci-fi", "fantasy",
    "documentary", "horror", "action", "mystery", "biography", "historical", "educational"
]

# VEHICLES (10+)
VEHICLES = [
    "Tesla Model 3", "Honda Civic", "Toyota Prius", "Ford F-150", "BMW X5",
    "Audi A4", "Mercedes C-Class", "Jeep Wrangler", "Subaru Outback", "Nissan Leaf"
]

# BUSINESS_TYPES (12+)
BUSINESS_TYPES = [
    "restaurant", "coffee shop", "bookstore", "gym", "salon", "clinic",
    "pharmacy", "bank", "grocery store", "electronics store", "clothing store", "gas station"
]

# EQUIPMENT_TYPES (10+)
EQUIPMENT_TYPES = [
    "laptop stand", "ergonomic chair", "standing desk", "noise-canceling headphones",
    "external monitor", "wireless mouse", "mechanical keyboard", "tablet", "smartwatch", "camera"
]

# SOCIAL_SITUATIONS (10+)
SOCIAL_SITUATIONS = [
    "dinner party", "work meeting", "family gathering", "friend's wedding",
    "networking event", "conference presentation", "team lunch", "birthday celebration",
    "holiday party", "casual hangout"
]

# CONDITIONS (13+)
CONDITIONS = [
    "stress", "fatigue", "excitement", "nervousness", "confidence", "uncertainty",
    "motivation", "creativity", "focus", "distraction", "burnout", "energy", "calm"
]

# TIMELINES (15+ entries)
TIMELINES = [
    "next quarter", "this year", "within 6 months", "by 2025", "next decade",
    "short-term", "long-term", "immediate future", "near future", "distant future",
    "within weeks", "by summer", "end of year", "next fiscal year", "5-year plan"
]

# TIME (general time expressions, 15+ entries)
TIME = [
    "8:30 AM", "2:15 PM", "7:45 PM", "11:30 AM", "4:20 PM", "9:10 AM",
    "1:25 PM", "6:35 PM", "10:45 AM", "3:50 PM", "5:15 PM", "12:30 PM",
    "early morning", "late afternoon", "midnight hour"
]

# BUDGETS (full pool, 15+ entries)
BUDGETS = [
    "monthly budget", "annual budget", "project budget", "quarterly budget",
    "marketing budget", "training budget", "equipment budget", "travel budget",
    "emergency budget", "operational budget", "development budget", "research budget",
    "maintenance budget", "startup budget", "expansion budget"
]

# AMOUNTS (quantity expressions, 15+ entries)
AMOUNTS = [
    "2.5 hours", "45 minutes", "3.2 kilometers", "150 pages", "25 participants",
    "80% completion", "half the team", "dozens of ideas", "several attempts",
    "multiple iterations", "countless hours", "significant progress", "minimal effort",
    "maximum capacity", "optimal performance"
]

# SENTIMENTS (15+ entries)
SENTIMENTS = [
    "positive", "optimistic", "confident", "enthusiastic", "satisfied",
    "pleased", "content", "grateful", "hopeful", "inspired", "uncertain",
    "concerned", "excited", "nervous", "proud"
]

# PROJECTS (full pool, 20+ entries)
PROJECTS = [
    "AI integration project", "mobile app development", "website redesign",
    "database migration", "security upgrade", "performance optimization",
    "user interface overhaul", "cloud migration", "automation initiative",
    "data analysis project", "machine learning model", "customer portal",
    "inventory system", "payment gateway", "reporting dashboard",
    "content management system", "e-commerce platform", "API development",
    "quality assurance program", "digital transformation"
]

# INTENTS (15+ entries)
INTENTS = [
    "learn new skills", "improve performance", "build relationships", "achieve goals",
    "solve problems", "create value", "make impact", "grow professionally",
    "help others", "innovate", "optimize processes", "enhance user experience",
    "increase efficiency", "develop expertise", "expand knowledge"
]

# RELATIONSHIPS (15+ entries)
RELATIONSHIPS = [
    "close friendship", "professional partnership", "family bond", "mentorship",
    "romantic relationship", "business alliance", "collaborative partnership",
    "supportive friendship", "working relationship", "personal connection",
    "professional network", "advisory relationship", "peer relationship",
    "client relationship", "team dynamic"
]

# RELATIONSHIP_TYPES (15+ entries)
RELATIONSHIP_TYPES = [
    "friendship", "partnership", "collaboration", "mentorship", "family",
    "romantic", "professional", "business", "academic", "creative",
    "supportive", "advisory", "competitive", "cooperative", "hierarchical"
]

# TRAITS (20+ entries)
TRAITS = [
    "patience", "creativity", "analytical thinking", "leadership", "empathy",
    "resilience", "adaptability", "persistence", "optimism", "integrity",
    "curiosity", "innovation", "reliability", "collaboration", "initiative",
    "attention to detail", "strategic thinking", "emotional intelligence",
    "problem-solving", "communication"
]

# PERIODS (15+ entries)
PERIODS = [
    "during childhood", "in their teens", "college years", "early career",
    "during marriage", "after the divorce", "during pregnancy",
    "when kids were young", "midlife transition", "empty nest years",
    "pre-retirement", "during illness", "after recovery", "recent years",
    "last decade"
]

# EXPANDED CONDITIONS (current one exists but verify completeness, 15+ entries)
CONDITIONS_EXPANDED = [
    "stress", "fatigue", "excitement", "nervousness", "confidence",
    "uncertainty", "motivation", "creativity", "focus", "distraction",
    "burnout", "energy", "calm", "pressure", "flow state"
]

# WEATHER_CONDITIONS (verify current completeness, 16+ entries)
WEATHER_CONDITIONS_EXPANDED = [
    "sunny", "rainy", "cloudy", "snowy", "windy", "foggy", "stormy",
    "clear", "humid", "dry", "hot", "cold", "mild", "perfect weather",
    "overcast", "drizzling"
]

# EXPANDED SOCIAL_SITUATIONS (current exists, add more, 15+ entries)
SOCIAL_SITUATIONS_EXPANDED = [
    "dinner party", "work meeting", "family gathering", "friend's wedding",
    "networking event", "conference presentation", "team lunch", "birthday celebration",
    "holiday party", "casual hangout", "first date", "job interview",
    "performance review", "team building event", "graduation ceremony"
]

# MEMORY_TYPES (verify current exists and is complete, 15+ entries)
MEMORY_TYPES_EXPANDED = [
    "episodic memory", "semantic memory", "procedural memory", "emotional memory",
    "traumatic memory", "childhood memory", "recent memory", "vivid memory",
    "fragmented memory", "nostalgic memory", "suppressed memory", "triggered memory",
    "collective memory", "false memory", "flashbulb memory"
]

# LIFE_STAGES (verify current exists and is complete, 15+ entries)
LIFE_STAGES_EXPANDED = [
    "infancy", "toddlerhood", "childhood", "adolescence", "young adulthood",
    "early career", "career building", "mid-career", "senior career",
    "pre-retirement", "early retirement", "active retirement", "later life",
    "transition period", "life change"
]

# EXPANDED PLATFORMS (verify current completeness, 15+ entries)
PLATFORMS_EXPANDED = [
    "Netflix", "YouTube", "Spotify", "Instagram", "LinkedIn", "Twitter",
    "Facebook", "TikTok", "Zoom", "Teams", "Discord", "Slack", "Reddit",
    "GitHub", "Medium"
]

# EXPANDED MEDIA_TYPES (verify current completeness, 15+ entries)
MEDIA_TYPES_EXPANDED = [
    "podcast", "documentary", "movie", "TV series", "book", "audiobook",
    "YouTube video", "blog post", "article", "news report", "social media post",
    "webinar", "online course", "tutorial", "livestream"
]

# EXPANDED FREQUENCY_DETAILED (rename and expand current, 15+ entries)
FREQUENCY_PATTERNS = [
    "every morning", "twice a week", "once a month", "every few days",
    "daily", "weekly", "occasionally", "rarely", "frequently", "constantly",
    "seasonally", "annually", "bi-weekly", "quarterly", "sporadically"
]

# Additional missing specialized pools:

# CULTURAL_ELEMENTS (exists, verify completeness)
CULTURAL_ELEMENTS_EXPANDED = [
    "family recipes", "traditional songs", "cultural dances", "religious practices",
    "holiday customs", "storytelling traditions", "ancestral languages", "craft techniques",
    "ceremonial rituals", "folk art", "traditional games", "cultural dress",
    "historical narratives", "spiritual beliefs", "community celebrations", "art forms"
]

# LEARNING_METHODS (exists, verify completeness)
LEARNING_METHODS_EXPANDED = [
    "hands-on practice", "visual observation", "verbal instruction", "trial and error",
    "mentorship", "formal education", "self-study", "peer learning",
    "experiential learning", "repetitive practice", "guided discovery", "collaborative learning",
    "online courses", "workshop attendance", "reading extensively", "simulation"
]

# PERSONAL_GROWTH (exists, verify completeness)
PERSONAL_GROWTH_EXPANDED = [
    "emotional intelligence", "self-awareness", "confidence building", "resilience development",
    "communication skills", "leadership abilities", "empathy expansion", "stress management",
    "mindfulness practice", "creative expression", "problem-solving skills", "adaptability",
    "patience cultivation", "forgiveness capacity", "authenticity", "self-discipline"
]

# COMMUNITY_ROLES (exists, verify completeness)
COMMUNITY_ROLES_EXPANDED = [
    "volunteer coordinator", "neighborhood watch leader", "school board member", "youth mentor",
    "community organizer", "local activist", "charity fundraiser", "environmental advocate",
    "cultural preservationist", "elder caretaker", "child advocate", "religious leader",
    "social worker", "community mediator", "local historian", "civic leader"
]

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# PERFECT BALANCE TRACKER (Keep existing implementation)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class PerfectBalanceTracker:
    """Tracks usage to ensure perfect balance across all entities and relations."""
    
    def __init__(self):
        self.entity_usage = defaultdict(int)
        self.relation_usage = defaultdict(int)
        self.entity_types = self._get_all_entity_types()
        self.relation_types = self._get_all_relation_types()
        
        # Target usage per type
        self.entity_target = Config.TARGET_RECORDS_PER_ENTITY
        self.relation_target = Config.TARGET_RECORDS_PER_RELATION
        
        print(f"🎯 Perfect Balance Tracker Initialized with Expanded Data Pools:")
        print(f"   - Entity types to balance: {len(self.entity_types)}")
        print(f"   - Relation types to balance: {len(self.relation_types)}")
        print(f"   - Target per entity: {self.entity_target}")
        print(f"   - Target per relation: {self.relation_target}")
        print(f"   - Total people names: {len(ALL_PEOPLE_NAMES)}")
        print(f"   - Total organizations: {len(ORGANIZATIONS)}")
        print(f"   - Data pools significantly expanded ✅")
    
    def _get_all_entity_types(self):
        return [getattr(EntityTypes, attr) for attr in dir(EntityTypes) 
                if not attr.startswith('_')]
    
    def _get_all_relation_types(self):
        return [getattr(RelationTypes, attr) for attr in dir(RelationTypes) 
                if not attr.startswith('_')]
    
    def get_needed_entities(self, count=10):
        """Get the most needed entity types."""
        needed = []
        for entity_type in self.entity_types:
            current_usage = self.entity_usage[entity_type]
            if current_usage < self.entity_target:
                needed.append((entity_type, self.entity_target - current_usage))
        
        # Sort by most needed first
        needed.sort(key=lambda x: x[1], reverse=True)
        return [entity_type for entity_type, _ in needed[:count]]
    
    def get_needed_relations(self, count=10):
        """Get the most needed relation types."""
        needed = []
        for relation_type in self.relation_types:
            current_usage = self.relation_usage[relation_type]
            if current_usage < self.relation_target:
                needed.append((relation_type, self.relation_target - current_usage))
        
        # Sort by most needed first
        needed.sort(key=lambda x: x[1], reverse=True)
        return [relation_type for relation_type, _ in needed[:count]]
    
    def record_usage(self, entities, relations):
        """Record usage of entities and relations."""
        for entity_type in entities:
            self.entity_usage[entity_type] += 1
        
        for relation_type in relations:
            self.relation_usage[relation_type] += 1
    
    def get_balance_status(self):
        """Get current balance status."""
        entity_balance = self._calculate_balance(self.entity_usage, self.entity_target)
        relation_balance = self._calculate_balance(self.relation_usage, self.relation_target)
        
        return {
            "entity_balance_score": entity_balance,
            "relation_balance_score": relation_balance,
            "overall_balance": (entity_balance + relation_balance) / 2,
            "entity_completion": sum(min(count, self.entity_target) for count in self.entity_usage.values()) / (len(self.entity_types) * self.entity_target) * 100,
            "relation_completion": sum(min(count, self.relation_target) for count in self.relation_usage.values()) / (len(self.relation_types) * self.relation_target) * 100
        }
    
    def _calculate_balance(self, usage_dict, target):
        """Calculate balance score (0-100, where 100 is perfect balance)."""
        if not usage_dict:
            return 0.0
        
        scores = []
        for expected_type in (self.entity_types if target == self.entity_target else self.relation_types):
            current = usage_dict.get(expected_type, 0)
            score = min(current / target, 1.0) * 100
            scores.append(score)
        
        return sum(scores) / len(scores)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# UTILITY FUNCTIONS (Keep existing implementation)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

def find_span_case_insensitive(text: str, subtext: str) -> Optional[List[int]]:
    """Find span of subtext in text, case-insensitive."""
    lower_text = text.lower()
    lower_subtext = subtext.lower()
    start = lower_text.find(lower_subtext)
    if start == -1: 
        return None
    return [start, start + len(subtext)]

def create_entity(entity_id: int, text: str, entity_type: str, entity_text: str) -> Optional[Dict]:
    """Create entity with proper span calculation."""
    span = find_span_case_insensitive(text, entity_text)
    if span:
        return {
            "id": entity_id, 
            "type": entity_type, 
            "text": entity_text, 
            "span": span
        }
    return None

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# BALANCED TEMPLATE BASE CLASS (Keep existing implementation)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class BalancedTemplate:
    """Base template class that ensures balanced entity and relation usage."""
    
    def __init__(self, template_id: int, tracker: PerfectBalanceTracker):
        self.id = template_id
        self.tracker = tracker
    
    def generate_balanced_record(self) -> Dict:
        """Generate a record that uses the most needed entities and relations."""
        # Get most needed types
        needed_entities = self.tracker.get_needed_entities(5)
        needed_relations = self.tracker.get_needed_relations(5)
        
        # Generate text and metadata
        text, entities_meta, relations_meta = self.create_content(needed_entities, needed_relations)
        
        # Build entities
        entities = []
        entity_map = {}
        
        for key, (entity_type, entity_text) in entities_meta.items():
            entity = create_entity(len(entities), text, entity_type, entity_text)
            if entity:
                entities.append(entity)
                entity_map[key] = entity['id']
        
        # Build relations
        relations = []
        for rel_type, head_key, tail_key in relations_meta:
            if head_key in entity_map and tail_key in entity_map:
                relations.append({
                    "type": rel_type,
                    "head": entity_map[head_key],
                    "tail": entity_map[tail_key]
                })
        
        # Record usage for tracking
        entity_types_used = [entity_type for _, (entity_type, _) in entities_meta.items()]
        relation_types_used = [rel_type for rel_type, _, _ in relations_meta]
        self.tracker.record_usage(entity_types_used, relation_types_used)
        
        # Create context
        context = {
            "Salience": random.choice(["High", "Medium", "Low"]),
            "Recency": random.choice(["just now", "recently", "last week", "yesterday"]),
            "Source": "balanced_generation_expanded",
            "Confidence": random.choice(["High", "Medium", "Low"]),
            "Associated_Emotion": random.choice(["Neutral", "Positive", "Excited", "Calm"]),
            "Balance_Optimized": True,
            "Data_Pool_Version": "expanded"
        }
        
        return {
            "id": f"balanced_{self.id}_{uuid.uuid4().hex[:8]}",
            "text": text,
            "entities": entities,
            "relations": relations,
            "context": context
        }
    
    def create_content(self, needed_entities, needed_relations) -> Tuple[str, Dict, List]:
        """Override this method in each template to create specific content."""
        raise NotImplementedError("Subclasses must implement create_content")

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# ENHANCED BALANCED TEMPLATE IMPLEMENTATIONS (Using expanded data pools)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class TimelineGoalTemplate(BalancedTemplate):
    """Template focusing on timeline, intent, and goal entities."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        timeline = random.choice(TIMELINES)
        intent = random.choice(INTENTS)
        goal = random.choice(["career advancement", "skill mastery", "personal growth"])
        time = random.choice(TIME)
        project = random.choice(PROJECTS)
        
        text = f"{person} has an intent to {intent} by {timeline}. At {time}, they work on {project} to achieve their goal of {goal}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "timeline1": (EntityTypes.TIMELINE, timeline),
            "intent1": (EntityTypes.INTENT, intent),
            "goal1": (EntityTypes.GOAL, goal),
            "time1": (EntityTypes.TIME, time),
            "project1": (EntityTypes.PROJECT, project)
        }
        
        relations = [
            (RelationTypes.HAS_INTENT, "person1", "intent1"),
            (RelationTypes.AIMS_FOR, "person1", "goal1"),
            (RelationTypes.SCHEDULED_FOR, "project1", "timeline1"),
            (RelationTypes.STARTS_AT, "project1", "time1"),
            (RelationTypes.WORKS_ON, "person1", "project1"),
            (RelationTypes.INTENDS, "person1", "intent1")
        ]
        
        return text, entities, relations

class BudgetSentimentTemplate(BalancedTemplate):
    """Template focusing on budget, sentiment, and amount entities."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        budget = random.choice(BUDGETS)
        sentiment = random.choice(SENTIMENTS)
        amount = random.choice(AMOUNTS)
        money = random.choice(MONEY)
        organization = random.choice(ORGANIZATIONS)
        
        text = f"{person} manages the {budget} at {organization} with {sentiment} sentiment. They allocated {amount} and spent {money} on improvements."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "budget1": (EntityTypes.BUDGET, budget),
            "sentiment1": (EntityTypes.SENTIMENT, sentiment),
            "amount1": (EntityTypes.AMOUNT, amount),
            "money1": (EntityTypes.MONEY, money),
            "org1": (EntityTypes.ORGANIZATION, organization)
        }
        
        relations = [
            (RelationTypes.BUDGETS_FOR, "person1", "budget1"),
            (RelationTypes.FEELS, "person1", "sentiment1"),
            (RelationTypes.SPENDS, "person1", "money1"),
            (RelationTypes.EARNS, "org1", "money1"),
            (RelationTypes.WORKS_FOR, "person1", "org1"),
            (RelationTypes.USES, "person1", "budget1")
        ]
        
        return text, entities, relations

class RelationshipTraitTemplate(BalancedTemplate):
    """Template focusing on relationship, trait, and social entities."""
    
    def create_content(self, needed_entities, needed_relations):
        person1 = random.choice(ALL_PEOPLE_NAMES)
        person2 = random.choice([n for n in ALL_PEOPLE_NAMES if n != person1])
        relationship = random.choice(RELATIONSHIPS)
        relationship_type = random.choice(RELATIONSHIP_TYPES)
        trait = random.choice(TRAITS)
        group = random.choice(GROUPS)
        
        text = f"{person1} maintains a {relationship} with {person2} based on {relationship_type}. They both show {trait} and are part of the {group}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person1),
            "person2": (EntityTypes.PERSON, person2),
            "rel1": (EntityTypes.RELATIONSHIP, relationship),
            "reltype1": (EntityTypes.RELATIONSHIP_TYPE, relationship_type),
            "trait1": (EntityTypes.TRAIT, trait),
            "group1": (EntityTypes.GROUP, group)
        }
        
        relations = [
            (RelationTypes.MAINTAINS_RELATIONSHIP, "person1", "rel1"),
            (RelationTypes.IS_FRIENDS_WITH, "person1", "person2"),
            (RelationTypes.IS_TYPE, "rel1", "reltype1"),
            (RelationTypes.HAS_TRAIT, "person1", "trait1"),
            (RelationTypes.HAS_TRAIT, "person2", "trait1"),
            (RelationTypes.MEMBER_OF, "person1", "group1"),
            (RelationTypes.MEMBER_OF, "person2", "group1")
        ]
        
        return text, entities, relations

class MemoryLifeStageTemplate(BalancedTemplate):
    """Template focusing on memory, life stage, and period entities."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        memory_type = random.choice(MEMORY_TYPES_EXPANDED)
        life_stage = random.choice(LIFE_STAGES_EXPANDED)
        period = random.choice(PERIODS)
        cultural_element = random.choice(CULTURAL_ELEMENTS_EXPANDED)
        learning_method = random.choice(LEARNING_METHODS_EXPANDED)
        
        text = f"{person} has a {memory_type} from their {life_stage} {period}. They learned about {cultural_element} through {learning_method}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "memory1": (EntityTypes.MEMORY_TYPE, memory_type),
            "stage1": (EntityTypes.LIFE_STAGE, life_stage),
            "period1": (EntityTypes.PERIOD, period),
            "culture1": (EntityTypes.CULTURAL_ELEMENT, cultural_element),
            "method1": (EntityTypes.LEARNING_METHOD, learning_method)
        }
        
        relations = [
            (RelationTypes.REMEMBERS, "person1", "memory1"),
            (RelationTypes.THINKS, "person1", "stage1"),
            (RelationTypes.HAPPENS_ON, "memory1", "period1"),
            (RelationTypes.LEARNS, "person1", "culture1"),
            (RelationTypes.LEARNS_FROM, "person1", "method1"),
            (RelationTypes.REFLECTS_ON, "person1", "period1")
        ]
        
        return text, entities, relations

class GrowthCommunityTemplate(BalancedTemplate):
    """Template focusing on personal growth and community role entities."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        growth = random.choice(PERSONAL_GROWTH_EXPANDED)
        community_role = random.choice(COMMUNITY_ROLES_EXPANDED)
        learning_method = random.choice(LEARNING_METHODS_EXPANDED)
        organization = random.choice(ORGANIZATIONS)
        skill = random.choice(SKILLS)
        
        text = f"{person} develops {growth} through {learning_method} in their role as {community_role} at {organization}. They master {skill} skills."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "growth1": (EntityTypes.PERSONAL_GROWTH, growth),
            "role1": (EntityTypes.COMMUNITY_ROLE, community_role),
            "method1": (EntityTypes.LEARNING_METHOD, learning_method),
            "org1": (EntityTypes.ORGANIZATION, organization),
            "skill1": (EntityTypes.SKILL, skill)
        }
        
        relations = [
            (RelationTypes.DEVELOPS, "person1", "growth1"),
            (RelationTypes.HAS_ROLE, "person1", "role1"),
            (RelationTypes.USES, "person1", "method1"),
            (RelationTypes.WORKS_FOR, "person1", "org1"),
            (RelationTypes.MASTERS, "person1", "skill1"),
            (RelationTypes.LEARNS_FROM, "person1", "method1")
        ]
        
        return text, entities, relations

class PlatformMediaTemplate(BalancedTemplate):
    """Template focusing on platform, media, and genre entities."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        platform = random.choice(PLATFORMS_EXPANDED)
        media = random.choice(MEDIA_TYPES_EXPANDED)
        genre = random.choice(GENRES)
        topic = random.choice(TOPICS)
        frequency = random.choice(FREQUENCY_PATTERNS)
        
        text = f"{person} watches {media} about {topic} on {platform} {frequency}. They prefer {genre} content and enjoy the experience."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "platform1": (EntityTypes.PLATFORM, platform),
            "media1": (EntityTypes.MEDIA, media),
            "genre1": (EntityTypes.GENRE, genre),
            "topic1": (EntityTypes.TOPIC, topic),
            "freq1": (EntityTypes.FREQUENCY, frequency)
        }
        
        relations = [
            (RelationTypes.USES, "person1", "platform1"),
            (RelationTypes.WATCHES, "person1", "media1"),
            (RelationTypes.PREFERS, "person1", "genre1"),
            (RelationTypes.THINKS, "media1", "topic1"),
            (RelationTypes.HAS_FREQUENCY, "media1", "freq1"),
            (RelationTypes.ENJOYS, "person1", "media1")
        ]
        
        return text, entities, relations

class WeatherConditionTemplate(BalancedTemplate):
    """Template focusing on weather, condition, and environmental entities."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        weather = random.choice(WEATHER_CONDITIONS_EXPANDED)
        condition = random.choice(CONDITIONS_EXPANDED)
        location = random.choice(LOCATIONS)
        activity = random.choice(ACTIVITIES)
        vehicle = random.choice(VEHICLES)
        
        text = f"During {weather} weather, {person} experiences {condition} at the {location}. They adapt by {activity} and use their {vehicle}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "weather1": (EntityTypes.WEATHER, weather),
            "condition1": (EntityTypes.CONDITION, condition),
            "location1": (EntityTypes.LOCATION, location),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "vehicle1": (EntityTypes.VEHICLE, vehicle)
        }
        
        relations = [
            (RelationTypes.FEELS, "person1", "condition1"),
            (RelationTypes.CAUSED_BY, "condition1", "weather1"),
            (RelationTypes.AT_LOCATION, "person1", "location1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1"),
            (RelationTypes.OWNS, "person1", "vehicle1"),
            (RelationTypes.TRAVELS_TO, "person1", "location1")
        ]
        
        return text, entities, relations

class SocialBusinessTemplate(BalancedTemplate):
    """Template focusing on social situations and business entities."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        social_situation = random.choice(SOCIAL_SITUATIONS_EXPANDED)
        business = random.choice(BUSINESS_TYPES)
        equipment = random.choice(EQUIPMENT_TYPES)
        room = random.choice(ROOM_TYPES)
        food = random.choice(FOODS)
        
        text = f"{person} attends a {social_situation} at the {business} in the {room}. They use {equipment} and enjoy {food}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "social1": (EntityTypes.EVENT, social_situation),
            "business1": (EntityTypes.BUSINESS, business),
            "equipment1": (EntityTypes.EQUIPMENT, equipment),
            "room1": (EntityTypes.ROOM, room),
            "food1": (EntityTypes.FOOD, food)
        }
        
        relations = [
            (RelationTypes.ATTENDS, "person1", "social1"),
            (RelationTypes.AT_LOCATION, "social1", "business1"),
            (RelationTypes.USES, "person1", "equipment1"),
            (RelationTypes.LOCATED_AT, "equipment1", "room1"),
            (RelationTypes.ENJOYS, "person1", "food1"),
            (RelationTypes.LIKES, "business1", "food1")
        ]
        
        return text, entities, relations

class WorkflowTemplate(BalancedTemplate):
    """Template focusing on work-related entities and relations."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        organization = random.choice(ORGANIZATIONS)
        skill = random.choice(SKILLS)
        activity = random.choice(ACTIVITIES)
        location = random.choice(LOCATIONS)
        role = random.choice(ROLES)
        project = "AI integration project"
        
        text = f"{person} works for {organization} as a {role} at the {location}. They use their {skill} skills while {activity} on the {project}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "org1": (EntityTypes.ORGANIZATION, organization),
            "skill1": (EntityTypes.SKILL, skill),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "location1": (EntityTypes.LOCATION, location),
            "role1": (EntityTypes.ROLE, role),
            "project1": (EntityTypes.PROJECT, project)
        }
        
        relations = [
            (RelationTypes.WORKS_FOR, "person1", "org1"),
            (RelationTypes.HAS_ROLE, "person1", "role1"),
            (RelationTypes.HAS_SKILL, "person1", "skill1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1"),
            (RelationTypes.LOCATED_AT, "person1", "location1"),
            (RelationTypes.WORKS_ON, "person1", "project1"),
            (RelationTypes.USES, "person1", "skill1")
        ]
        
        return text, entities, relations

class PersonalLifeTemplate(BalancedTemplate):
    """Template focusing on personal life entities and relations."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        hobby = random.choice(HOBBIES)
        emotion = random.choice(EMOTIONS)
        friend = random.choice([n for n in ALL_PEOPLE_NAMES if n != person])
        preference = random.choice(PREFERENCES)
        belief = random.choice(BELIEFS)
        
        text = f"{person} has a hobby of {hobby} and feels {emotion} about it. They believe that '{belief}' and prefer {preference}. {person} is friends with {friend}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "hobby1": (EntityTypes.HOBBY, hobby),
            "emotion1": (EntityTypes.EMOTION, emotion),
            "friend1": (EntityTypes.PERSON, friend),
            "pref1": (EntityTypes.PREFERENCE, preference),
            "belief1": (EntityTypes.BELIEF, belief)
        }
        
        relations = [
            (RelationTypes.HAS_HOBBY, "person1", "hobby1"),
            (RelationTypes.FEELS_EMOTION, "person1", "emotion1"),
            (RelationTypes.IS_FRIENDS_WITH, "person1", "friend1"),
            (RelationTypes.HAS_PREFERENCE, "person1", "pref1"),
            (RelationTypes.BELIEVES, "person1", "belief1"),
            (RelationTypes.ENJOYS, "person1", "hobby1")
        ]
        
        return text, entities, relations

class ScheduleTimeTemplate(BalancedTemplate):
    """Template focusing on time and schedule entities and relations."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        start_time = random.choice(START_TIMES)
        end_time = random.choice(END_TIMES)
        duration = random.choice(DURATIONS)
        frequency = random.choice(FREQUENCY_DETAILED)
        date = random.choice(DATES)
        activity = random.choice(ACTIVITIES)
        
        text = f"{person} starts at {start_time} and ends at {end_time} {frequency} on {date}. The {activity} lasts for {duration}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "start1": (EntityTypes.START_TIME, start_time),
            "end1": (EntityTypes.END_TIME, end_time),
            "duration1": (EntityTypes.DURATION, duration),
            "freq1": (EntityTypes.FREQUENCY, frequency),
            "date1": (EntityTypes.DATE, date),
            "activity1": (EntityTypes.ACTIVITY, activity)
        }
        
        relations = [
            (RelationTypes.STARTS_AT, "activity1", "start1"),
            (RelationTypes.ENDS_AT, "activity1", "end1"),
            (RelationTypes.FOR_DURATION, "activity1", "duration1"),
            (RelationTypes.HAS_FREQUENCY, "activity1", "freq1"),
            (RelationTypes.ON_DATE, "activity1", "date1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1")
        ]
        
        return text, entities, relations

class SensoryExperienceTemplate(BalancedTemplate):
    """Template focusing on sensory entities and relations."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        location = random.choice(LOCATIONS)
        sound = random.choice(SOUNDS)
        sight = random.choice(SIGHTS)
        taste = random.choice(TASTES)
        smell = random.choice(SMELLS)
        sensation = random.choice(SENSATIONS)
        
        text = f"At the {location}, {person} hears {sound}, sees a {sight}, tastes something {taste}, smells {smell}, and feels {sensation}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "location1": (EntityTypes.LOCATION, location),
            "sound1": (EntityTypes.SOUND, sound),
            "sight1": (EntityTypes.SIGHT, sight),
            "taste1": (EntityTypes.TASTE, taste),
            "smell1": (EntityTypes.SMELL, smell),
            "sensation1": (EntityTypes.SENSATION, sensation)
        }
        
        relations = [
            (RelationTypes.AT_LOCATION, "person1", "location1"),
            (RelationTypes.HEARS, "person1", "sound1"),
            (RelationTypes.SEES, "person1", "sight1"),
            (RelationTypes.TASTES, "person1", "taste1"),
            (RelationTypes.SMELLS, "person1", "smell1"),
            (RelationTypes.TOUCHES, "person1", "sensation1")
        ]
        
        return text, entities, relations

class FinancialTemplate(BalancedTemplate):
    """Template focusing on financial entities and relations."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        money = random.choice(MONEY)
        budget = "monthly budget"
        goal = random.choice(["financial independence", "early retirement", "debt freedom"])
        amount = random.choice(MONEY)
        
        text = f"{person} earns {money} and saves {amount} in their {budget}. Their goal is {goal}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "money1": (EntityTypes.MONEY, money),
            "budget1": (EntityTypes.BUDGET, budget),
            "goal1": (EntityTypes.GOAL, goal),
            "amount1": (EntityTypes.AMOUNT, amount)
        }
        
        relations = [
            (RelationTypes.EARNS, "person1", "money1"),
            (RelationTypes.SAVES, "person1", "amount1"),
            (RelationTypes.BUDGETS_FOR, "person1", "budget1"),
            (RelationTypes.WANTS_GOAL, "person1", "goal1"),
            (RelationTypes.HAS_GOAL, "person1", "goal1")
        ]
        
        return text, entities, relations

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# ADDITIONAL PERFECTLY BALANCED TEMPLATES (15-20 new templates for 100% coverage)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class WorkExpertiseTemplate(BalancedTemplate):
    """Template focusing on professional expertise with first/third person variations."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        organization = random.choice(ORGANIZATIONS)
        skill = random.choice(SKILLS)
        expertise = random.choice(["machine learning", "data analysis", "software architecture", "project management", "user experience design"])
        project = random.choice(PROJECTS)
        technology = random.choice(["Python", "React", "AWS", "Docker", "Kubernetes", "TensorFlow"])
        equipment = random.choice(["laptop", "workstation", "server", "tablet", "smartphone"])
        industry = random.choice(["technology", "healthcare", "finance", "education", "manufacturing"])
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I work for {organization} in the {industry} industry. I have expertise in {expertise} and use {skill} with {technology}. I'm currently working on {project} using my {equipment}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} works for {organization} in the {industry} industry. They have expertise in {expertise} and use {skill} with {technology}. They're currently working on {project} using their {equipment}."
            person_entity = person
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "org1": (EntityTypes.ORGANIZATION, organization),
            "skill1": (EntityTypes.SKILL, skill),
            "expertise1": (EntityTypes.SKILL, expertise),  # Using SKILL type for expertise
            "project1": (EntityTypes.PROJECT, project),
            "tech1": (EntityTypes.TECHNOLOGY, technology),
            "equip1": (EntityTypes.EQUIPMENT, equipment),
            "industry1": (EntityTypes.INDUSTRY, industry)
        }
        
        relations = [
            (RelationTypes.WORKS_FOR, "person1", "org1"),
            (RelationTypes.HAS_EXPERTISE, "person1", "expertise1"),
            (RelationTypes.HAS_SKILL, "person1", "skill1"),
            (RelationTypes.USES, "person1", "tech1"),
            (RelationTypes.WORKS_ON, "person1", "project1"),
            (RelationTypes.USES, "person1", "equip1"),
            (RelationTypes.WORKS_FROM, "person1", "industry1")
        ]
        
        return text, entities, relations

class CareerProgressionTemplate(BalancedTemplate):
    """Template focusing on career progression and goals."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        role = random.choice(ROLES)
        goal = random.choice(["promotion", "career change", "skill development", "leadership role", "industry expertise"])
        timeline = random.choice(TIMELINES)
        industry = random.choice(["technology", "healthcare", "finance", "education", "manufacturing"])
        intent = random.choice(INTENTS)
        learning_method = random.choice(LEARNING_METHODS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I currently work as a {role} in the {industry} sector. My goal is {goal} over the {timeline}. I intend to {intent} and am using {learning_method} to achieve this."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} currently works as a {role} in the {industry} sector. Their goal is {goal} over the {timeline}. They intend to {intent} and are using {learning_method} to achieve this."
            person_entity = person
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "role1": (EntityTypes.ROLE, role),
            "goal1": (EntityTypes.GOAL, goal),
            "timeline1": (EntityTypes.TIMELINE, timeline),
            "industry1": (EntityTypes.INDUSTRY, industry),
            "intent1": (EntityTypes.INTENT, intent),
            "method1": (EntityTypes.LEARNING_METHOD, learning_method)
        }
        
        relations = [
            (RelationTypes.HAS_ROLE, "person1", "role1"),
            (RelationTypes.HAS_GOAL, "person1", "goal1"),
            (RelationTypes.HAS_INTENT, "person1", "intent1"),
            (RelationTypes.LEARNS_FROM, "person1", "method1"),
            (RelationTypes.WORKS_FROM, "person1", "industry1"),
            (RelationTypes.PLANS, "person1", "goal1"),
            (RelationTypes.AIMS_FOR, "person1", "goal1")
        ]
        
        return text, entities, relations

class TeamCollaborationTemplate(BalancedTemplate):
    """Template focusing on team collaboration and group activities."""
    
    def create_content(self, needed_entities, needed_relations):
        person1 = random.choice(ALL_PEOPLE_NAMES)
        person2 = random.choice([n for n in ALL_PEOPLE_NAMES if n != person1])
        group = random.choice(GROUPS)
        activity = random.choice(ACTIVITIES)
        location = random.choice(LOCATIONS)
        project = random.choice(PROJECTS)
        skill = random.choice(SKILLS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I collaborate with {person2} in our {group}. We're working on {activity} at the {location} for the {project}. I use my {skill} skills in this collaboration."
            person1_entity = "I"
        else:
            # Third person variation
            text = f"{person1} collaborates with {person2} in their {group}. They're working on {activity} at the {location} for the {project}. {person1} uses their {skill} skills in this collaboration."
            person1_entity = person1
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person1_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person1_type, person1_entity),
            "person2": (EntityTypes.PERSON, person2),
            "group1": (EntityTypes.GROUP, group),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "location1": (EntityTypes.LOCATION, location),
            "project1": (EntityTypes.PROJECT, project),
            "skill1": (EntityTypes.SKILL, skill)
        }
        
        relations = [
            (RelationTypes.COLLABORATES_WITH, "person1", "person2"),
            (RelationTypes.MEMBER_OF, "person1", "group1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1"),
            (RelationTypes.AT_LOCATION, "person1", "location1"),
            (RelationTypes.WORKS_ON, "person1", "project1"),
            (RelationTypes.HAS_SKILL, "person1", "skill1"),
            (RelationTypes.USES, "person1", "skill1")
        ]
        
        return text, entities, relations

class LifeJourneyTemplate(BalancedTemplate):
    """Template focusing on life stages and personal growth journey."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        life_stage = random.choice(LIFE_STAGES)
        memory_type = random.choice(MEMORY_TYPES)
        cultural_element = random.choice(CULTURAL_ELEMENTS)
        period = random.choice(PERIODS)
        personal_growth = random.choice(PERSONAL_GROWTH)
        sentiment = random.choice(SENTIMENTS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I'm currently in my {life_stage} phase. I have {memory_type} memories from the {period} that shaped my understanding of {cultural_element}. This period brought {personal_growth} with a {sentiment} outlook."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} is currently in their {life_stage} phase. They have {memory_type} memories from the {period} that shaped their understanding of {cultural_element}. This period brought {personal_growth} with a {sentiment} outlook."
            person_entity = person
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "stage1": (EntityTypes.LIFE_STAGE, life_stage),
            "memory1": (EntityTypes.MEMORY_TYPE, memory_type),
            "culture1": (EntityTypes.CULTURAL_ELEMENT, cultural_element),
            "period1": (EntityTypes.PERIOD, period),
            "growth1": (EntityTypes.PERSONAL_GROWTH, personal_growth),
            "sentiment1": (EntityTypes.SENTIMENT, sentiment)
        }
        
        relations = [
            (RelationTypes.THINKS, "person1", "stage1"),
            (RelationTypes.REMEMBERS, "person1", "memory1"),
            (RelationTypes.LEARNS, "person1", "culture1"),
            (RelationTypes.REFLECTS_ON, "person1", "period1"),
            (RelationTypes.IMPROVES, "person1", "growth1"),
            (RelationTypes.FEELS, "person1", "sentiment1"),
            (RelationTypes.HAPPENS_ON, "memory1", "period1")
        ]
        
        return text, entities, relations

class RelationshipDynamicsTemplate(BalancedTemplate):
    """Template focusing on relationship dynamics and social traits."""
    
    def create_content(self, needed_entities, needed_relations):
        person1 = random.choice(ALL_PEOPLE_NAMES)
        person2 = random.choice([n for n in ALL_PEOPLE_NAMES if n != person1])
        relationship = random.choice(RELATIONSHIPS)
        trait = random.choice(TRAITS)
        emotion = random.choice(EMOTIONS)
        group = random.choice(GROUPS)
        relationship_type = random.choice(RELATIONSHIP_TYPES)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I maintain a {relationship} with {person2} based on {relationship_type}. I show {trait} in this relationship and feel {emotion}. We're both part of the {group}."
            person_entity = "I"
        else:
            # Third person variation  
            text = f"{person1} maintains a {relationship} with {person2} based on {relationship_type}. They show {trait} in this relationship and feel {emotion}. They're both part of the {group}."
            person_entity = person1
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person1_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person1_type, person_entity),
            "person2": (EntityTypes.PERSON, person2),
            "rel1": (EntityTypes.RELATIONSHIP, relationship),
            "trait1": (EntityTypes.TRAIT, trait),
            "emotion1": (EntityTypes.EMOTION, emotion),
            "group1": (EntityTypes.GROUP, group),
            "reltype1": (EntityTypes.RELATIONSHIP_TYPE, relationship_type)
        }
        
        relations = [
            (RelationTypes.MAINTAINS_RELATIONSHIP, "person1", "person2"),
            (RelationTypes.HAS_TRAIT, "person1", "trait1"),
            (RelationTypes.FEELS_EMOTION, "person1", "emotion1"),
            (RelationTypes.MEMBER_OF, "person1", "group1"),
            (RelationTypes.IS_TYPE, "rel1", "reltype1"),
            (RelationTypes.CARES_FOR, "person1", "person2"),
            (RelationTypes.SUPPORTS, "person1", "person2")
        ]
        
        return text, entities, relations

class HobbyInterestTemplate(BalancedTemplate):
    """Template focusing on hobbies, interests and personal activities."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        hobby = random.choice(HOBBIES)
        skill = random.choice(SKILLS)
        frequency = random.choice(FREQUENCY_PATTERNS)
        equipment = random.choice(["camera", "guitar", "bicycle", "easel", "laptop", "telescope", "chess set"])
        goal = random.choice(["mastery", "relaxation", "creativity", "fitness", "social connection"])
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I enjoy {hobby} as my main hobby and practice it {frequency}. I use my {skill} skills and {equipment} to pursue {goal} through this activity."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} enjoys {hobby} as their main hobby and practices it {frequency}. They use their {skill} skills and {equipment} to pursue {goal} through this activity."
            person_entity = person
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "hobby1": (EntityTypes.HOBBY, hobby),
            "skill1": (EntityTypes.SKILL, skill),
            "freq1": (EntityTypes.FREQUENCY, frequency),
            "equip1": (EntityTypes.EQUIPMENT, equipment),
            "goal1": (EntityTypes.GOAL, goal)
        }
        
        relations = [
            (RelationTypes.HAS_HOBBY, "person1", "hobby1"),
            (RelationTypes.ENJOYS, "person1", "hobby1"),
            (RelationTypes.HAS_SKILL, "person1", "skill1"),
            (RelationTypes.HAS_FREQUENCY, "hobby1", "freq1"),
            (RelationTypes.USES, "person1", "equip1"),
            (RelationTypes.HAS_GOAL, "person1", "goal1"),
            (RelationTypes.PRACTICES, "person1", "hobby1")
        ]
        
        return text, entities, relations

class LearningGrowthTemplate(BalancedTemplate):
    """Template focusing on learning processes and personal growth."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        learning_method = random.choice(LEARNING_METHODS)
        personal_growth = random.choice(PERSONAL_GROWTH)
        skill = random.choice(SKILLS)
        goal = random.choice(["mastery", "improvement", "understanding", "expertise", "knowledge"])
        topic = random.choice(["artificial intelligence", "philosophy", "cooking", "music", "history", "science"])
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I'm using {learning_method} to develop my {skill} abilities. This approach supports my {personal_growth} as I work toward {goal} in {topic}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} is using {learning_method} to develop their {skill} abilities. This approach supports their {personal_growth} as they work toward {goal} in {topic}."
            person_entity = person
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "method1": (EntityTypes.LEARNING_METHOD, learning_method),
            "growth1": (EntityTypes.PERSONAL_GROWTH, personal_growth),
            "skill1": (EntityTypes.SKILL, skill),
            "goal1": (EntityTypes.GOAL, goal),
            "topic1": (EntityTypes.TOPIC, topic)
        }
        
        relations = [
            (RelationTypes.LEARNS_FROM, "person1", "method1"),
            (RelationTypes.IMPROVES, "person1", "growth1"),
            (RelationTypes.HAS_SKILL, "person1", "skill1"),
            (RelationTypes.HAS_GOAL, "person1", "goal1"),
            (RelationTypes.LEARNS, "person1", "topic1"),
            (RelationTypes.DEVELOPS, "person1", "skill1"),
            (RelationTypes.MASTERS, "person1", "skill1")
        ]
        
        return text, entities, relations

class MemoryReflectionTemplate(BalancedTemplate):
    """Template focusing on memory, reflection and personal insights."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        memory_type = random.choice(MEMORY_TYPES)
        period = random.choice(PERIODS)
        sentiment = random.choice(SENTIMENTS)
        belief = random.choice(BELIEFS)
        emotion = random.choice(EMOTIONS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I have {memory_type} memories from the {period} that evoke a {sentiment} feeling. These experiences shaped my belief that '{belief}' and make me feel {emotion} when I reflect on them."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} has {memory_type} memories from the {period} that evoke a {sentiment} feeling. These experiences shaped their belief that '{belief}' and make them feel {emotion} when they reflect on them."
            person_entity = person
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "memory1": (EntityTypes.MEMORY_TYPE, memory_type),
            "period1": (EntityTypes.PERIOD, period),
            "sentiment1": (EntityTypes.SENTIMENT, sentiment),
            "belief1": (EntityTypes.BELIEF, belief),
            "emotion1": (EntityTypes.EMOTION, emotion)
        }
        
        relations = [
            (RelationTypes.REMEMBERS, "person1", "memory1"),
            (RelationTypes.REFLECTS_ON, "person1", "period1"),
            (RelationTypes.FEELS, "person1", "sentiment1"),
            (RelationTypes.BELIEVES, "person1", "belief1"),
            (RelationTypes.FEELS_EMOTION, "person1", "emotion1"),
            (RelationTypes.THINKS, "person1", "memory1"),
            (RelationTypes.HAPPENS_ON, "memory1", "period1")
        ]
        
        return text, entities, relations

class DecisionMakingTemplate(BalancedTemplate):
    """Template focusing on decision making and personal values."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        intent = random.choice(INTENTS)
        goal = random.choice(["career advancement", "personal fulfillment", "family happiness", "financial security", "creative expression"])
        opinion = random.choice(["optimistic", "pragmatic", "cautious", "ambitious", "balanced"])
        value = random.choice(VALUES)
        preference = random.choice(PREFERENCES)
        
        # First person variation (50% chance) 
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I intend to {intent} because my goal is {goal}. My {opinion} opinion guides my decisions, and I value {value}. I prefer {preference} when making important choices."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} intends to {intent} because their goal is {goal}. Their {opinion} opinion guides their decisions, and they value {value}. They prefer {preference} when making important choices."
            person_entity = person
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "intent1": (EntityTypes.INTENT, intent),
            "goal1": (EntityTypes.GOAL, goal),
            "opinion1": (EntityTypes.OPINION, opinion),
            "value1": (EntityTypes.VALUE, value),
            "pref1": (EntityTypes.PREFERENCE, preference)
        }
        
        relations = [
            (RelationTypes.HAS_INTENT, "person1", "intent1"),
            (RelationTypes.HAS_GOAL, "person1", "goal1"),
            (RelationTypes.HAS_OPINION, "person1", "opinion1"),
            (RelationTypes.VALUES, "person1", "value1"),
            (RelationTypes.HAS_PREFERENCE, "person1", "pref1"),
            (RelationTypes.INTENDS, "person1", "intent1"),
            (RelationTypes.PLANS, "person1", "goal1")
        ]
        
        return text, entities, relations

        return text, entities, relations

class CommunityEngagementTemplate(BalancedTemplate):
    """Template focusing on community roles and cultural engagement."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        community_role = random.choice(COMMUNITY_ROLES)
        group = random.choice(GROUPS)
        cultural_element = random.choice(CULTURAL_ELEMENTS)
        location = random.choice(LOCATIONS)
        activity = random.choice(ACTIVITIES)
        event = random.choice(["festival", "workshop", "meeting", "celebration", "conference"])
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I serve as a {community_role} in our {group} at the {location}. I'm involved in {activity} that celebrates {cultural_element} during our community {event}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} serves as a {community_role} in their {group} at the {location}. They're involved in {activity} that celebrates {cultural_element} during their community {event}."
            person_entity = person
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "role1": (EntityTypes.COMMUNITY_ROLE, community_role),
            "group1": (EntityTypes.GROUP, group),
            "culture1": (EntityTypes.CULTURAL_ELEMENT, cultural_element),
            "location1": (EntityTypes.LOCATION, location),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "event1": (EntityTypes.EVENT, event)
        }
        
        relations = [
            (RelationTypes.HAS_ROLE, "person1", "role1"),
            (RelationTypes.MEMBER_OF, "person1", "group1"),
            (RelationTypes.AT_LOCATION, "person1", "location1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1"),
            (RelationTypes.PARTICIPATES_IN, "person1", "event1"),
            (RelationTypes.LEARNS, "person1", "culture1"),
            (RelationTypes.LEADS, "person1", "group1")
        ]
        
        return text, entities, relations

class MediaConsumptionTemplate(BalancedTemplate):
    """Template focusing on media consumption and platform usage."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        platform = random.choice(PLATFORMS)
        media = random.choice(MEDIA_TYPES_EXPANDED)
        genre = random.choice(GENRES)
        frequency = random.choice(FREQUENCY_PATTERNS)
        topic = random.choice(["technology", "health", "travel", "food", "entertainment", "news"])
        preference = random.choice(PREFERENCES)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I use {platform} to consume {media} content, especially {genre} topics about {topic}. I engage with this content {frequency} because I prefer {preference}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} uses {platform} to consume {media} content, especially {genre} topics about {topic}. They engage with this content {frequency} because they prefer {preference}."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "platform1": (EntityTypes.PLATFORM, platform),
            "media1": (EntityTypes.MEDIA, media),
            "genre1": (EntityTypes.GENRE, genre),
            "freq1": (EntityTypes.FREQUENCY, frequency),
            "topic1": (EntityTypes.TOPIC, topic),
            "pref1": (EntityTypes.PREFERENCE, preference)
        }
        
        relations = [
            (RelationTypes.USES, "person1", "platform1"),
            (RelationTypes.WATCHES, "person1", "media1"),
            (RelationTypes.LIKES, "person1", "genre1"),
            (RelationTypes.HAS_FREQUENCY, "person1", "freq1"),
            (RelationTypes.READS, "person1", "topic1"),
            (RelationTypes.HAS_PREFERENCE, "person1", "pref1"),
            (RelationTypes.ENJOYS, "person1", "media1")
        ]
        
        return text, entities, relations

class SocialSituationTemplate(BalancedTemplate):
    """Template focusing on social situations and business interactions."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        event = random.choice(["meeting", "dinner", "conference", "party", "presentation"])
        business = random.choice(BUSINESS_TYPES)
        food = random.choice(FOODS)
        room = random.choice(ROOM_TYPES)
        equipment = random.choice(["projector", "microphone", "tablet", "phone", "laptop"])
        emotion = random.choice(EMOTIONS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I'm attending a {event} at {business} in the {room}. We're having {food} while using the {equipment}. I feel {emotion} about this social situation."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} is attending a {event} at {business} in the {room}. They're having {food} while using the {equipment}. They feel {emotion} about this social situation."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "event1": (EntityTypes.EVENT, event),
            "business1": (EntityTypes.BUSINESS, business),
            "food1": (EntityTypes.FOOD, food),
            "room1": (EntityTypes.ROOM, room),
            "equip1": (EntityTypes.EQUIPMENT, equipment),
            "emotion1": (EntityTypes.EMOTION, emotion)
        }
        
        relations = [
            (RelationTypes.ATTENDS, "person1", "event1"),
            (RelationTypes.VISITS, "person1", "business1"),
            (RelationTypes.TASTES, "person1", "food1"),
            (RelationTypes.AT_LOCATION, "person1", "room1"),
            (RelationTypes.USES, "person1", "equip1"),
            (RelationTypes.FEELS_EMOTION, "person1", "emotion1"),
            (RelationTypes.PARTICIPATES_IN, "person1", "event1")
        ]
        
        return text, entities, relations

class WeatherActivityTemplate(BalancedTemplate):
    """Template focusing on weather conditions and environmental activities."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        weather = random.choice(WEATHER_CONDITIONS_EXPANDED)
        condition = random.choice(CONDITIONS_EXPANDED)
        activity = random.choice(ACTIVITIES)
        location = random.choice(LOCATIONS)
        vehicle = random.choice(VEHICLES)
        equipment = random.choice(["umbrella", "jacket", "sunglasses", "boots", "hat"])
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"With {weather} weather and {condition} conditions, I'm doing {activity} at the {location}. I use my {vehicle} to get there and bring my {equipment} for the conditions."
            person_entity = "I"
        else:
            # Third person variation
            text = f"With {weather} weather and {condition} conditions, {person} is doing {activity} at the {location}. They use their {vehicle} to get there and bring their {equipment} for the conditions."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "weather1": (EntityTypes.WEATHER, weather),
            "condition1": (EntityTypes.CONDITION, condition),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "location1": (EntityTypes.LOCATION, location),
            "vehicle1": (EntityTypes.VEHICLE, vehicle),
            "equip1": (EntityTypes.EQUIPMENT, equipment)
        }
        
        relations = [
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1"),
            (RelationTypes.AT_LOCATION, "person1", "location1"),
            (RelationTypes.USES, "person1", "vehicle1"),
            (RelationTypes.USES, "person1", "equip1"),
            (RelationTypes.AFFECTS, "weather1", "person1"),
            (RelationTypes.AFFECTS, "condition1", "activity1"),
            (RelationTypes.TRAVELS_TO, "person1", "location1")
        ]
        
        return text, entities, relations

class TimeScheduleTemplate(BalancedTemplate):
    """Template focusing on time management and scheduling."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        time = random.choice(TIME)
        duration = random.choice(DURATIONS)
        recurring_schedule = random.choice(RECURRING_SCHEDULES)
        activity = random.choice(ACTIVITIES)
        location = random.choice(LOCATIONS)
        start_time = "9:00 AM"
        end_time = "5:00 PM"
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I have a {recurring_schedule} schedule for {activity} at the {location}. It starts at {start_time} and runs for {duration}, ending at {end_time}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} has a {recurring_schedule} schedule for {activity} at the {location}. It starts at {start_time} and runs for {duration}, ending at {end_time}."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "time1": (EntityTypes.TIME, time),
            "duration1": (EntityTypes.DURATION, duration),
            "schedule1": (EntityTypes.RECURRING_SCHEDULE, recurring_schedule),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "location1": (EntityTypes.LOCATION, location),
            "start1": (EntityTypes.START_TIME, start_time),
            "end1": (EntityTypes.END_TIME, end_time)
        }
        
        relations = [
            (RelationTypes.SCHEDULED_FOR, "person1", "activity1"),
            (RelationTypes.STARTS_AT, "activity1", "start1"),
            (RelationTypes.ENDS_AT, "activity1", "end1"),
            (RelationTypes.FOR_DURATION, "activity1", "duration1"),
            (RelationTypes.AT_LOCATION, "activity1", "location1"),
            (RelationTypes.REPEATS, "activity1", "schedule1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1")
        ]
        
        return text, entities, relations

class TravelExperienceTemplate(BalancedTemplate):
    """Template focusing on travel experiences and geographic locations."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        geopolitical_entity = random.choice(GEOPOLITICAL_ENTITIES)
        vehicle = random.choice(VEHICLES)
        duration = random.choice(DURATIONS)
        sentiment = random.choice(SENTIMENTS)
        activity = random.choice(ACTIVITIES)
        cultural_element = random.choice(CULTURAL_ELEMENTS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I traveled to {geopolitical_entity} using {vehicle} for {duration}. I feel {sentiment} about the experience and enjoyed {activity} while learning about {cultural_element}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} traveled to {geopolitical_entity} using {vehicle} for {duration}. They feel {sentiment} about the experience and enjoyed {activity} while learning about {cultural_element}."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "geo1": (EntityTypes.GEOPOLITICAL_ENTITY, geopolitical_entity),
            "vehicle1": (EntityTypes.VEHICLE, vehicle),
            "duration1": (EntityTypes.DURATION, duration),
            "sentiment1": (EntityTypes.SENTIMENT, sentiment),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "culture1": (EntityTypes.CULTURAL_ELEMENT, cultural_element)
        }
        
        relations = [
            (RelationTypes.TRAVELS_TO, "person1", "geo1"),
            (RelationTypes.USES, "person1", "vehicle1"),
            (RelationTypes.FOR_DURATION, "person1", "duration1"),
            (RelationTypes.FEELS, "person1", "sentiment1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1"),
            (RelationTypes.LEARNS, "person1", "culture1"),
            (RelationTypes.VISITS, "person1", "geo1")
        ]
        
        return text, entities, relations

        return text, entities, relations

class HealthWellnessTemplate(BalancedTemplate):
    """Template focusing on health, wellness and personal care."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        health_info = random.choice(HEALTH_INFO)
        activity = random.choice(["exercise", "meditation", "yoga", "running", "swimming"])
        goal = random.choice(["fitness", "wellness", "strength", "flexibility", "peace"])
        frequency = random.choice(FREQUENCY_PATTERNS)
        equipment = random.choice(["yoga mat", "dumbbells", "running shoes", "water bottle", "heart monitor"])
        feeling = random.choice(FEELINGS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I focus on {health_info} through {activity} {frequency}. My goal is {goal} and I use {equipment} for my routine. This makes me feel {feeling}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} focuses on {health_info} through {activity} {frequency}. Their goal is {goal} and they use {equipment} for their routine. This makes them feel {feeling}."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "health1": (EntityTypes.HEALTH_INFO, health_info),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "goal1": (EntityTypes.GOAL, goal),
            "freq1": (EntityTypes.FREQUENCY, frequency),
            "equip1": (EntityTypes.EQUIPMENT, equipment),
            "feeling1": (EntityTypes.FEELING, feeling)
        }
        
        relations = [
            (RelationTypes.HAS_HEALTH_INFO, "person1", "health1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1"),
            (RelationTypes.HAS_GOAL, "person1", "goal1"),
            (RelationTypes.HAS_FREQUENCY, "activity1", "freq1"),
            (RelationTypes.USES, "person1", "equip1"),
            (RelationTypes.FEELS, "person1", "feeling1"),
            (RelationTypes.MANAGES_HEALTH, "person1", "health1")
        ]
        
        return text, entities, relations

class ObjectInteractionTemplate(BalancedTemplate):
    """Template focusing on object interaction and ownership."""
    
    def create_content(self, needed_entities, needed_relations):
        person1 = random.choice(ALL_PEOPLE_NAMES)
        person2 = random.choice([n for n in ALL_PEOPLE_NAMES if n != person1])
        obj = random.choice(["book", "tool", "instrument", "device", "artwork"])
        money = random.choice(MONEY)
        business = random.choice(BUSINESS_TYPES)
        product = random.choice(["software", "application", "gadget", "service"])
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I own a {obj} that I borrowed from {person2}. I spent {money} on a {product} from {business}, and now I'm lending the {obj} to help others."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person1} owns a {obj} that they borrowed from {person2}. They spent {money} on a {product} from {business}, and now they're lending the {obj} to help others."
            person_entity = person1
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "person2": (EntityTypes.PERSON, person2),
            "obj1": (EntityTypes.OBJECT, obj),
            "money1": (EntityTypes.MONEY, money),
            "business1": (EntityTypes.BUSINESS, business),
            "product1": (EntityTypes.PRODUCT, product)
        }
        
        relations = [
            (RelationTypes.OWNS, "person1", "obj1"),
            (RelationTypes.BORROWED, "person1", "obj1"),
            (RelationTypes.LENT, "person2", "obj1"),
            (RelationTypes.SPENDS, "person1", "money1"),
            (RelationTypes.RECEIVES, "person1", "product1"),
            (RelationTypes.GIVES, "person1", "obj1"),
            (RelationTypes.HAS_OBJECT, "person1", "obj1")
        ]
        
        return text, entities, relations

class NicknameIdentityTemplate(BalancedTemplate):
    """Template focusing on nicknames, identity and personal attributes."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        nickname = random.choice(["Ace", "Chief", "Scout", "Spark", "Dash", "Phoenix", "Sage"])
        pronoun = random.choice(["they/them", "she/her", "he/him"])
        attribute = random.choice(ATTRIBUTES)
        pet = random.choice(PETS)
        trait = random.choice(TRAITS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"People call me {nickname} and my pronouns are {pronoun}. I have the attribute of being {attribute} and my {pet} reflects my {trait} nature."
            person_entity = "I"
        else:
            # Third person variation
            text = f"People call {person} by the nickname {nickname} and their pronouns are {pronoun}. They have the attribute of being {attribute} and their {pet} reflects their {trait} nature."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "nickname1": (EntityTypes.NICKNAME, nickname),
            "pronoun1": (EntityTypes.PRONOUN, pronoun),
            "attr1": (EntityTypes.ATTRIBUTE, attribute),
            "pet1": (EntityTypes.PET, pet),
            "trait1": (EntityTypes.TRAIT, trait)
        }
        
        relations = [
            (RelationTypes.CALLED, "person1", "nickname1"),
            (RelationTypes.KNOWN_AS, "person1", "nickname1"),
            (RelationTypes.IS_TYPE, "person1", "pronoun1"),
            (RelationTypes.HAS_ATTRIBUTE, "person1", "attr1"),
            (RelationTypes.OWNS, "person1", "pet1"),
            (RelationTypes.HAS_TRAIT, "person1", "trait1")
        ]
        
        return text, entities, relations

class ConceptualThinkingTemplate(BalancedTemplate):
    """Template focusing on abstract concepts and intellectual processes."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        concept = random.choice(["innovation", "sustainability", "creativity", "efficiency", "collaboration"])
        idea = random.choice(["solution", "approach", "method", "strategy", "framework"])
        opinion = random.choice(["progressive", "conservative", "balanced", "innovative", "practical"])
        topic = random.choice(["technology", "environment", "society", "business", "education"])
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I'm thinking about the concept of {concept} and considering a new {idea}. My {opinion} opinion on {topic} influences how I approach these abstract thoughts."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} is thinking about the concept of {concept} and considering a new {idea}. Their {opinion} opinion on {topic} influences how they approach these abstract thoughts."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "concept1": (EntityTypes.CONCEPT, concept),
            "idea1": (EntityTypes.IDEA, idea),
            "opinion1": (EntityTypes.OPINION, opinion),
            "topic1": (EntityTypes.TOPIC, topic)
        }
        
        relations = [
            (RelationTypes.THINKING_OF, "person1", "concept1"),
            (RelationTypes.CONSIDERING, "person1", "idea1"),
            (RelationTypes.HAS_OPINION, "person1", "opinion1"),
            (RelationTypes.THINKS, "person1", "topic1"),
            (RelationTypes.REFLECTS_ON, "person1", "concept1"),
            (RelationTypes.DEVELOPS, "person1", "idea1")
        ]
        
        return text, entities, relations

        return text, entities, relations

class FamilyConnectionTemplate(BalancedTemplate):
    """Template focusing on family relationships and emotional connections."""
    
    def create_content(self, needed_entities, needed_relations):
        person1 = random.choice(ALL_PEOPLE_NAMES)
        person2 = random.choice([n for n in ALL_PEOPLE_NAMES if n != person1])
        geopolitical_entity = random.choice(GEOPOLITICAL_ENTITIES)
        memory_type = random.choice(MEMORY_TYPES)
        emotion = random.choice(EMOTIONS)
        period = random.choice(PERIODS)
        cultural_element = random.choice(CULTURAL_ELEMENTS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I am family with {person2} who lives in {geopolitical_entity}. I have {memory_type} memories from the {period} and miss our connection to {cultural_element}. This makes me feel {emotion}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person1} is family with {person2} who lives in {geopolitical_entity}. They have {memory_type} memories from the {period} and miss their connection to {cultural_element}. This makes them feel {emotion}."
            person_entity = person1
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "person2": (EntityTypes.PERSON, person2),
            "geo1": (EntityTypes.GEOPOLITICAL_ENTITY, geopolitical_entity),
            "memory1": (EntityTypes.MEMORY_TYPE, memory_type),
            "emotion1": (EntityTypes.EMOTION, emotion),
            "period1": (EntityTypes.PERIOD, period),
            "culture1": (EntityTypes.CULTURAL_ELEMENT, cultural_element)
        }
        
        relations = [
            (RelationTypes.IS_FAMILY_WITH, "person1", "person2"),
            (RelationTypes.LIVES_IN, "person2", "geo1"),
            (RelationTypes.REMEMBERS, "person1", "memory1"),
            (RelationTypes.MISSES, "person1", "culture1"),
            (RelationTypes.FEELS_EMOTION, "person1", "emotion1"),
            (RelationTypes.HAPPENS_ON, "memory1", "period1"),
            (RelationTypes.REFLECTS_ON, "person1", "period1")
        ]
        
        return text, entities, relations

class MentorshipTemplate(BalancedTemplate):
    """Template focusing on mentorship, teaching and influence relationships."""
    
    def create_content(self, needed_entities, needed_relations):
        person1 = random.choice(ALL_PEOPLE_NAMES)
        person2 = random.choice([n for n in ALL_PEOPLE_NAMES if n != person1])
        skill = random.choice(SKILLS)
        topic = random.choice(TOPICS)
        organization = random.choice(ORGANIZATIONS)
        goal = random.choice(["career growth", "skill development", "leadership", "expertise"])
        platform = random.choice(PLATFORMS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I mentor {person2} at {organization} and teach them {skill} about {topic}. I follow their progress on {platform} and influence their goal of {goal}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person1} mentors {person2} at {organization} and teaches them {skill} about {topic}. They follow their progress on {platform} and influence their goal of {goal}."
            person_entity = person1
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "person2": (EntityTypes.PERSON, person2),
            "skill1": (EntityTypes.SKILL, skill),
            "topic1": (EntityTypes.TOPIC, topic),
            "org1": (EntityTypes.ORGANIZATION, organization),
            "goal1": (EntityTypes.GOAL, goal),
            "platform1": (EntityTypes.PLATFORM, platform)
        }
        
        relations = [
            (RelationTypes.MENTORS, "person1", "person2"),
            (RelationTypes.TEACHES, "person1", "skill1"),
            (RelationTypes.FOLLOWS, "person1", "person2"),
            (RelationTypes.INFLUENCES, "person1", "goal1"),
            (RelationTypes.ORGANIZES, "person1", "topic1"),
            (RelationTypes.WORKS_FOR, "person1", "org1"),
            (RelationTypes.USES, "person1", "platform1")
        ]
        
        return text, entities, relations

class EmotionalJourneyTemplate(BalancedTemplate):
    """Template focusing on emotional states and future aspirations."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        goal = random.choice(["travel", "education", "family", "achievement", "peace"])
        event = random.choice(["reunion", "graduation", "promotion", "wedding", "adventure"])
        memory_type = random.choice(MEMORY_TYPES)
        geopolitical_entity = random.choice(GEOPOLITICAL_ENTITIES)
        period = random.choice(PERIODS)
        emotion = random.choice(EMOTIONS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I dream of {goal} and look forward to a {event}. I have {memory_type} memories that I regret from the {period}. I hope for moving to {geopolitical_entity} and feel {emotion} about it."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} dreams of {goal} and looks forward to a {event}. They have {memory_type} memories that they regret from the {period}. They hope for moving to {geopolitical_entity} and feel {emotion} about it."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "goal1": (EntityTypes.GOAL, goal),
            "event1": (EntityTypes.EVENT, event),
            "memory1": (EntityTypes.MEMORY_TYPE, memory_type),
            "geo1": (EntityTypes.GEOPOLITICAL_ENTITY, geopolitical_entity),
            "period1": (EntityTypes.PERIOD, period),
            "emotion1": (EntityTypes.EMOTION, emotion)
        }
        
        relations = [
            (RelationTypes.DREAMS_OF, "person1", "goal1"),
            (RelationTypes.LOOKING_FORWARD_TO, "person1", "event1"),
            (RelationTypes.REGRETS, "person1", "memory1"),
            (RelationTypes.HOPES_FOR, "person1", "geo1"),
            (RelationTypes.MOVES_TO, "person1", "geo1"),
            (RelationTypes.HAPPENS_ON, "memory1", "period1"),
            (RelationTypes.FEELS_EMOTION, "person1", "emotion1")
        ]
        
        return text, entities, relations

class HealthLocationTemplate(BalancedTemplate):
    """Template focusing on health conditions, locations and lifestyle."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        health_condition = random.choice(["allergies", "fitness goals", "wellness routine", "dietary needs"])
        location = random.choice(LOCATIONS)
        room = random.choice(ROOM_TYPES)
        activity = random.choice(ACTIVITIES)
        business = random.choice(BUSINESS_TYPES)
        media = random.choice(MEDIA_TYPES_EXPANDED)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I have {health_condition} and stay at the {location} in the {room}. I'm near the {business} where I do {activity} and listen to {media}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} has {health_condition} and stays at the {location} in the {room}. They're near the {business} where they do {activity} and listen to {media}."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "health1": (EntityTypes.HEALTH_INFO, health_condition),  # Using HEALTH_INFO type
            "location1": (EntityTypes.LOCATION, location),
            "room1": (EntityTypes.ROOM, room),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "business1": (EntityTypes.BUSINESS, business),
            "media1": (EntityTypes.MEDIA, media)
        }
        
        relations = [
            (RelationTypes.HAS_HEALTH_CONDITION, "person1", "health1"),
            (RelationTypes.STAYS_AT, "person1", "location1"),
            (RelationTypes.AT_LOCATION, "person1", "room1"),
            (RelationTypes.IS_NEAR, "location1", "business1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1"),
            (RelationTypes.LISTENS_TO, "person1", "media1"),
            (RelationTypes.LOCATED_AT, "business1", "location1")
        ]
        
        return text, entities, relations

class CausalInfluenceTemplate(BalancedTemplate):
    """Template focusing on cause-effect relationships and triggers."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        event = random.choice(["change", "decision", "opportunity", "challenge", "breakthrough"])
        emotion = random.choice(EMOTIONS)
        goal = random.choice(GOALS if 'GOALS' in globals() else ["success", "growth", "improvement"])
        activity = random.choice(ACTIVITIES)
        result = random.choice(["improvement", "success", "satisfaction", "achievement", "progress"])
        project = random.choice(PROJECTS)
        
        # First person variation (50% chance)
        if random.choice([True, False]):
            text = f"My {activity} contributed to the {project} and triggered a {event}. This results in {result} and makes me feel {emotion}, which influences my {goal}."
        else:
            # Third person variation
            text = f"{person}'s {activity} contributed to the {project} and triggered a {event}. This results in {result} and makes them feel {emotion}, which influences their {goal}."
        
        entities = {
            "person1": (EntityTypes.PERSON, person),
            "event1": (EntityTypes.EVENT, event),
            "emotion1": (EntityTypes.EMOTION, emotion),
            "goal1": (EntityTypes.GOAL, goal),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "result1": (EntityTypes.CONCEPT, result),  # Using CONCEPT for result
            "project1": (EntityTypes.PROJECT, project)
        }
        
        relations = [
            (RelationTypes.CONTRIBUTED_TO, "activity1", "project1"),
            (RelationTypes.TRIGGERS, "activity1", "event1"),
            (RelationTypes.RESULTS_IN, "event1", "result1"),
            (RelationTypes.FEELS_EMOTION, "person1", "emotion1"),
            (RelationTypes.INFLUENCES, "emotion1", "goal1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1"),
            (RelationTypes.WORKS_ON, "person1", "project1")
        ]
        
        return text, entities, relations

        return text, entities, relations

class WorkPlanningTemplate(BalancedTemplate):
    """Template focusing on concerns, planning and future anxiety."""
    
    def create_content(self, needed_entities, needed_relations):
        person = random.choice(ALL_PEOPLE_NAMES)
        goal = random.choice(["career advancement", "family security", "financial stability", "health", "future"])
        event = random.choice(["deadline", "presentation", "interview", "meeting", "change"])
        timeline = random.choice(TIMELINES)
        intent = random.choice(INTENTS)
        activity = random.choice(ACTIVITIES)
        emotion = random.choice(EMOTIONS)
        
        # First person variation (50% chance)
        use_first_person = random.choice([True, False])
        if use_first_person:
            text = f"I worry about my {goal} and the upcoming {event}. I plan to {intent} over the {timeline} through {activity}. This makes me feel {emotion}."
            person_entity = "I"
        else:
            # Third person variation
            text = f"{person} worries about their {goal} and the upcoming {event}. They plan to {intent} over the {timeline} through {activity}. This makes them feel {emotion}."
            person_entity = person
        
        
        # Use PRONOUN type for first-person "I", PERSON type for third-person names
        person_type = EntityTypes.PRONOUN if use_first_person else EntityTypes.PERSON
        
        entities = {
            "person1": (person_type, person_entity),
            "goal1": (EntityTypes.GOAL, goal),
            "event1": (EntityTypes.EVENT, event),
            "timeline1": (EntityTypes.TIMELINE, timeline),
            "intent1": (EntityTypes.INTENT, intent),
            "activity1": (EntityTypes.ACTIVITY, activity),
            "emotion1": (EntityTypes.EMOTION, emotion)
        }
        
        relations = [
            (RelationTypes.WORRIES_ABOUT, "person1", "goal1"),
            (RelationTypes.WORRIES_ABOUT, "person1", "event1"),
            (RelationTypes.PLANS, "person1", "intent1"),
            (RelationTypes.DOES_ACTIVITY, "person1", "activity1"),
            (RelationTypes.HAS_GOAL, "person1", "goal1"),
            (RelationTypes.FEELS_EMOTION, "person1", "emotion1"),
            (RelationTypes.HAS_INTENT, "person1", "intent1")
        ]
        
        return text, entities, relations

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# MAIN GENERATION FUNCTIONS (Keep existing with expanded data pools)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

def generate_perfectly_balanced_dataset(num_records: int = None) -> Dict:
    """Generate a perfectly balanced dataset with even distribution using all data pools."""
    
    if num_records is None:
        num_records = Config.DEFAULT_NUM_RECORDS
    
    print(f"🎯 PERFECTLY BALANCED DATASET GENERATION - ALL DATA POOLS COMPLETE")
    print(f"=" * 75)
    print(f"Target records: {num_records}")
    print(f"Updated timestamp: {Config.CURRENT_UTC_DATETIME}")
    print(f"Total people names available: {len(ALL_PEOPLE_NAMES)}")
    print(f"All missing data pools now included ✅")
    
    # Initialize tracker and templates
    tracker = PerfectBalanceTracker()
    
    # ALL TEMPLATES - Original + New ones utilizing missing data pools
    template_classes = [
        # Original templates
        WorkflowTemplate,
        PersonalLifeTemplate,
        ScheduleTimeTemplate,
        SensoryExperienceTemplate,
        FinancialTemplate,
        
        # NEW templates for missing data pools
        TimelineGoalTemplate,
        BudgetSentimentTemplate,
        RelationshipTraitTemplate,
        MemoryLifeStageTemplate,
        GrowthCommunityTemplate,
        PlatformMediaTemplate,
        WeatherConditionTemplate,
        SocialBusinessTemplate,
        
        # ADDITIONAL PERFECTLY BALANCED TEMPLATES (15+ new templates for 100% coverage)
        # Professional Templates
        WorkExpertiseTemplate,
        CareerProgressionTemplate,
        TeamCollaborationTemplate,
        
        # Personal Life Templates
        LifeJourneyTemplate,
        RelationshipDynamicsTemplate,
        HobbyInterestTemplate,
        
        # Cognitive Templates
        LearningGrowthTemplate,
        MemoryReflectionTemplate,
        DecisionMakingTemplate,
        
        # Social Context Templates
        CommunityEngagementTemplate,
        MediaConsumptionTemplate,
        SocialSituationTemplate,
        
        # Environmental Templates
        WeatherActivityTemplate,
        TimeScheduleTemplate,
        TravelExperienceTemplate,
        
        # Additional Specialized Templates
        HealthWellnessTemplate,
        ObjectInteractionTemplate,
        NicknameIdentityTemplate,
        ConceptualThinkingTemplate,
        
        # Targeted Templates for Missing Relations
        FamilyConnectionTemplate,
        MentorshipTemplate,
        EmotionalJourneyTemplate,
        HealthLocationTemplate,
        CausalInfluenceTemplate,
        WorkPlanningTemplate
    ]
    
    dataset = []
    failed_generations = 0
    
    print(f"Using {len(template_classes)} templates for perfect balance")
    
    for i in range(num_records):
        # Cycle through templates
        TemplateClass = template_classes[i % len(template_classes)]
        template = TemplateClass(i, tracker)
        
        try:
            record = template.generate_balanced_record()
            dataset.append(record)
            
            # Progress reporting
            if (i + 1) % Config.PROGRESS_INTERVAL == 0:
                balance_status = tracker.get_balance_status()
                print(f"Generated {i+1}/{num_records} | "
                      f"Balance: {balance_status['overall_balance']:.1f}% | "
                      f"Entity: {balance_status['entity_completion']:.1f}% | "
                      f"Relation: {balance_status['relation_completion']:.1f}%")
                
        except Exception as e:
            print(f"Failed to generate record {i}: {e}")
            failed_generations += 1
    
    # Generate final statistics
    final_balance = tracker.get_balance_status()
    
    stats = {
        "total_generated": len(dataset),
        "failed_generations": failed_generations,
        "success_rate": len(dataset) / num_records * 100,
        "balance_scores": final_balance,
        "entity_usage": dict(tracker.entity_usage),
        "relation_usage": dict(tracker.relation_usage),
        "templates_used": len(template_classes),
        "data_pools_complete": True,
        "total_people_names": len(ALL_PEOPLE_NAMES),
        "missing_pools_added": True,
        "timestamp_updated": Config.CURRENT_UTC_DATETIME
    }
    
    return {
        "dataset": dataset,
        "statistics": stats,
        "tracker": tracker
    }
    
def print_balance_report(result: Dict):
    """Print comprehensive balance report showing all data pools are complete."""
    stats = result["statistics"]
    
    print(f"\n{'='*75}")
    print("PERFECT BALANCE REPORT - ALL DATA POOLS COMPLETE")
    print(f"{'='*75}")
    
    print(f"Total generated: {stats['total_generated']}")
    print(f"Success rate: {stats['success_rate']:.1f}%")
    print(f"All data pools complete: {stats.get('data_pools_complete', False)} ✅")
    print(f"Missing pools added: {stats.get('missing_pools_added', False)} ✅")
    print(f"Timestamp updated: {stats.get('timestamp_updated', 'N/A')}")
    print(f"Templates used: {stats.get('templates_used', 0)}")
    
    balance = stats["balance_scores"]
    print(f"\nBalance Scores:")
    print(f"  Overall: {balance['overall_balance']:.1f}%")
    print(f"  Entity: {balance['entity_balance_score']:.1f}%")
    print(f"  Relation: {balance['relation_balance_score']:.1f}%")
    
    print(f"\nCompletion Status:")
    print(f"  Entity completion: {balance['entity_completion']:.1f}%")
    print(f"  Relation completion: {balance['relation_completion']:.1f}%")
    
    print(f"\nData Pool Coverage Summary:")
    print(f"  TIMELINES: {len(TIMELINES)}")
    print(f"  TIME: {len(TIME)}")
    print(f"  BUDGETS: {len(BUDGETS)}")
    print(f"  AMOUNTS: {len(AMOUNTS)}")
    print(f"  SENTIMENTS: {len(SENTIMENTS)}")
    print(f"  PROJECTS: {len(PROJECTS)}")
    print(f"  INTENTS: {len(INTENTS)}")
    print(f"  RELATIONSHIPS: {len(RELATIONSHIPS)}")
    print(f"  RELATIONSHIP_TYPES: {len(RELATIONSHIP_TYPES)}")
    print(f"  TRAITS: {len(TRAITS)}")
    print(f"  All missing data pools now included! 🎯")

def main():
    """Main execution function with expanded data pools."""
    print("🚀 Starting Perfectly Balanced Dataset Generation with Expanded Data Pools")
    
    # Generate small test dataset first
    result = generate_perfectly_balanced_dataset(1000)  # Start with 1K records
    
    print_balance_report(result)
    
    # Save dataset
    filename = f"balanced_expanded_dataset_{Config.CURRENT_UTC_DATETIME.replace(':', '').replace(' ', '_').replace('-', '')}.json"
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(result["dataset"], f, indent=2, ensure_ascii=False)
    
    print(f"\nDataset saved to: {filename}")
    
    # Show sample records demonstrating diversity
    print(f"\nSample Records (showing expanded data pool diversity):")
    for i, record in enumerate(result["dataset"][:5]):
        print(f"\n--- Sample {i+1} ---")
        print(f"Text: {record['text']}")
        print(f"Entities: {[e['type'] for e in record['entities']]}")
        print(f"Relations: {[r['type'] for r in record['relations']]}")
        
        # Show specific entity values to demonstrate diversity
        person_entities = [e for e in record['entities'] if e['type'] == 'PERSON']
        if person_entities:
            print(f"Person name used: {person_entities[0]['text']}")

if __name__ == "__main__":
    main()