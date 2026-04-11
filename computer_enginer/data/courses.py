"""
Course Database for UTel University - Computer Engineering Program
All courses organized by category with complete metadata
"""

COURSES = {
    # ==================== PROGRAMMING COURSES ====================
    "CE101": {
        "name": "Structured Programming",
        "credits": 4,
        "category": "Programming",
        "semester": 1,
        "prerequisites": [],
        "description": "Introduction to programming fundamentals using structured programming paradigm. Covers variables, control structures, functions, and basic algorithms.",
        "learning_outcomes": [
            "Understand basic programming concepts and logic",
            "Write well-structured programs using functions",
            "Implement basic algorithms and data manipulation",
            "Debug and test programs effectively"
        ],
        "concentrations": ["IT", "Finance", "Management"],
        "difficulty": 2,
        "hours_per_week": 6,
        "type": "Core"
    },
    
    "CE201": {
        "name": "Object Oriented Programming",
        "credits": 4,
        "category": "Programming",
        "semester": 3,
        "prerequisites": ["CE101"],
        "description": "Advanced programming using OOP principles. Covers classes, objects, inheritance, polymorphism, and design patterns.",
        "learning_outcomes": [
            "Master OOP concepts and principles",
            "Design and implement class hierarchies",
            "Apply design patterns to solve problems",
            "Develop maintainable and scalable code"
        ],
        "concentrations": ["IT", "Finance", "Management"],
        "difficulty": 4,
        "hours_per_week": 7,
        "type": "Core"
    },
    
    "CE202": {
        "name": "Assembly Language",
        "credits": 3,
        "category": "Programming",
        "semester": 3,
        "prerequisites": ["CE101", "CE103"],
        "description": "Low-level programming using assembly language. Understanding computer architecture at the instruction level.",
        "learning_outcomes": [
            "Understand machine-level instructions",
            "Write efficient assembly code",
            "Optimize code for performance",
            "Interface with hardware directly"
        ],
        "concentrations": ["IT"],
        "difficulty": 5,
        "hours_per_week": 6,
        "type": "Core"
    },
    
    "CE401": {
        "name": "Web Development",
        "credits": 4,
        "category": "Programming",
        "semester": 6,
        "prerequisites": ["CE201", "CE304"],
        "description": "Modern web development using HTML, CSS, JavaScript, and frameworks. Full-stack development concepts.",
        "learning_outcomes": [
            "Build responsive web applications",
            "Implement RESTful APIs",
            "Use modern web frameworks",
            "Deploy web applications to cloud"
        ],
        "concentrations": ["IT", "Management"],
        "difficulty": 4,
        "hours_per_week": 8,
        "type": "Elective"
    },
    
    # ==================== MATHEMATICS COURSES ====================
    "MA101": {
        "name": "Differential and Integral Calculus",
        "credits": 4,
        "category": "Mathematics",
        "semester": 1,
        "prerequisites": [],
        "description": "Fundamental calculus concepts including limits, derivatives, and integrals with applications.",
        "learning_outcomes": [
            "Compute derivatives and integrals",
            "Solve optimization problems",
            "Apply calculus to real-world scenarios",
            "Understand limits and continuity"
        ],
        "concentrations": ["IT", "Finance", "Management"],
        "difficulty": 5,
        "hours_per_week": 6,
        "type": "Core"
    },
    
    "MA102": {
        "name": "Linear Algebra",
        "credits": 3,
        "category": "Mathematics",
        "semester": 2,
        "prerequisites": [],
        "description": "Vectors, matrices, linear transformations, eigenvalues, and applications in computer graphics and ML.",
        "learning_outcomes": [
            "Perform matrix operations",
            "Solve systems of linear equations",
            "Understand vector spaces",
            "Apply to computer graphics and AI"
        ],
        "concentrations": ["IT", "Finance"],
        "difficulty": 4,
        "hours_per_week": 5,
        "type": "Core"
    },
    
    "MA201": {
        "name": "Statistics and Probability",
        "credits": 3,
        "category": "Mathematics",
        "semester": 3,
        "prerequisites": ["MA101"],
        "description": "Statistical analysis, probability theory, distributions, and hypothesis testing for data science.",
        "learning_outcomes": [
            "Analyze data statistically",
            "Calculate probabilities",
            "Perform hypothesis testing",
            "Apply to machine learning"
        ],
        "concentrations": ["IT", "Finance", "Management"],
        "difficulty": 4,
        "hours_per_week": 5,
        "type": "Core"
    },
    
    "MA301": {
        "name": "Higher Algebra",
        "credits": 3,
        "category": "Mathematics",
        "semester": 5,
        "prerequisites": ["MA102"],
        "description": "Advanced algebraic structures including groups, rings, and fields with applications to cryptography.",
        "learning_outcomes": [
            "Understand abstract algebra concepts",
            "Work with algebraic structures",
            "Apply to cryptography",
            "Solve complex mathematical problems"
        ],
        "concentrations": ["IT"],
        "difficulty": 6,
        "hours_per_week": 5,
        "type": "Elective"
    },
    
    # ==================== COMPUTER SYSTEMS ====================
    "CE103": {
        "name": "Computer Architecture",
        "credits": 4,
        "category": "Systems",
        "semester": 2,
        "prerequisites": [],
        "description": "Computer organization, CPU design, memory hierarchy, I/O systems, and performance optimization.",
        "learning_outcomes": [
            "Understand computer organization",
            "Analyze CPU performance",
            "Design memory systems",
            "Optimize system performance"
        ],
        "concentrations": ["IT"],
        "difficulty": 5,
        "hours_per_week": 6,
        "type": "Core"
    },
    
    "CE203": {
        "name": "Operating Systems",
        "credits": 4,
        "category": "Systems",
        "semester": 4,
        "prerequisites": ["CE103", "CE201"],
        "description": "OS concepts including processes, threads, memory management, file systems, and concurrency.",
        "learning_outcomes": [
            "Understand OS architecture",
            "Implement process scheduling",
            "Manage memory efficiently",
            "Handle concurrency and synchronization"
        ],
        "concentrations": ["IT"],
        "difficulty": 6,
        "hours_per_week": 7,
        "type": "Core"
    },
    
    "CE301": {
        "name": "Computer Networks",
        "credits": 4,
        "category": "Systems",
        "semester": 5,
        "prerequisites": ["CE203"],
        "description": "Network protocols, TCP/IP, routing, network security, and distributed systems.",
        "learning_outcomes": [
            "Understand network protocols",
            "Configure network devices",
            "Implement network security",
            "Design distributed systems"
        ],
        "concentrations": ["IT", "Management"],
        "difficulty": 5,
        "hours_per_week": 7,
        "type": "Core"
    },
    
    "CE302": {
        "name": "Digital Systems and Peripherals",
        "credits": 3,
        "category": "Systems",
        "semester": 4,
        "prerequisites": ["CE103"],
        "description": "Digital logic design, combinational and sequential circuits, and peripheral interfacing.",
        "learning_outcomes": [
            "Design digital circuits",
            "Implement logic gates",
            "Interface with peripherals",
            "Optimize digital systems"
        ],
        "concentrations": ["IT"],
        "difficulty": 4,
        "hours_per_week": 6,
        "type": "Core"
    },
    
    # ==================== DATA & ALGORITHMS ====================
    "CE204": {
        "name": "Algorithms and Data Structures",
        "credits": 4,
        "category": "Algorithms",
        "semester": 4,
        "prerequisites": ["CE101", "MA101"],
        "description": "Algorithm design and analysis, data structures, complexity theory, and optimization techniques.",
        "learning_outcomes": [
            "Implement advanced data structures",
            "Analyze algorithm complexity",
            "Design efficient algorithms",
            "Solve computational problems"
        ],
        "concentrations": ["IT", "Finance"],
        "difficulty": 6,
        "hours_per_week": 8,
        "type": "Core"
    },
    
    "CE304": {
        "name": "Databases",
        "credits": 4,
        "category": "Data",
        "semester": 5,
        "prerequisites": ["CE201", "CE204"],
        "description": "Database design, SQL, normalization, transactions, and NoSQL databases.",
        "learning_outcomes": [
            "Design relational databases",
            "Write complex SQL queries",
            "Optimize database performance",
            "Work with NoSQL databases"
        ],
        "concentrations": ["IT", "Finance", "Management"],
        "difficulty": 4,
        "hours_per_week": 7,
        "type": "Core"
    },
    
    # ==================== AI & ADVANCED ====================
    "CE402": {
        "name": "Artificial Intelligence",
        "credits": 4,
        "category": "AI/ML",
        "semester": 7,
        "prerequisites": ["CE204", "MA201"],
        "description": "AI fundamentals, search algorithms, machine learning, neural networks, and applications.",
        "learning_outcomes": [
            "Implement AI algorithms",
            "Build machine learning models",
            "Apply neural networks",
            "Solve AI problems"
        ],
        "concentrations": ["IT"],
        "difficulty": 7,
        "hours_per_week": 8,
        "type": "Elective"
    },
    
    # ==================== SOFTWARE ENGINEERING ====================
    "CE303": {
        "name": "Systems Analysis and Design",
        "credits": 3,
        "category": "Software Engineering",
        "semester": 5,
        "prerequisites": ["CE201"],
        "description": "Software development lifecycle, requirements analysis, system design, and UML modeling.",
        "learning_outcomes": [
            "Analyze system requirements",
            "Design software architecture",
            "Create UML diagrams",
            "Manage software projects"
        ],
        "concentrations": ["IT", "Management"],
        "difficulty": 4,
        "hours_per_week": 6,
        "type": "Core"
    },
    
    # ==================== ELECTRONICS & PHYSICS ====================
    "EE101": {
        "name": "Electronics",
        "credits": 4,
        "category": "Electronics",
        "semester": 2,
        "prerequisites": [],
        "description": "Basic electronics, circuits, components, analog and digital electronics fundamentals.",
        "learning_outcomes": [
            "Understand electronic components",
            "Analyze circuits",
            "Design basic electronic systems",
            "Interface hardware with software"
        ],
        "concentrations": ["IT"],
        "difficulty": 4,
        "hours_per_week": 6,
        "type": "Core"
    },
    
    "PH101": {
        "name": "Physics",
        "credits": 3,
        "category": "Science",
        "semester": 1,
        "prerequisites": [],
        "description": "Fundamental physics concepts including mechanics, electricity, magnetism, and waves.",
        "learning_outcomes": [
            "Understand physical principles",
            "Apply physics to engineering",
            "Solve physics problems",
            "Conduct experiments"
        ],
        "concentrations": ["IT", "Finance", "Management"],
        "difficulty": 4,
        "hours_per_week": 5,
        "type": "Core"
    },
    
    # ==================== BUSINESS & MANAGEMENT ====================
    "BU201": {
        "name": "Structure of the Processing Industry",
        "credits": 3,
        "category": "Business",
        "semester": 4,
        "prerequisites": [],
        "description": "Understanding industrial processes, manufacturing systems, and business operations.",
        "learning_outcomes": [
            "Understand industrial processes",
            "Analyze business operations",
            "Optimize production systems",
            "Apply IT to business"
        ],
        "concentrations": ["Management", "Finance"],
        "difficulty": 3,
        "hours_per_week": 4,
        "type": "Elective"
    },
    
    "SD101": {
        "name": "Sustainable Development",
        "credits": 2,
        "category": "General",
        "semester": 6,
        "prerequisites": [],
        "description": "Sustainability principles, environmental impact, and responsible technology development.",
        "learning_outcomes": [
            "Understand sustainability concepts",
            "Assess environmental impact",
            "Design sustainable systems",
            "Apply ethical principles"
        ],
        "concentrations": ["IT", "Finance", "Management"],
        "difficulty": 2,
        "hours_per_week": 3,
        "type": "General Education"
    },
    
    # ==================== CONCENTRATION COURSES ====================
    "FI301": {
        "name": "Concentration - Finance",
        "credits": 3,
        "category": "Concentration",
        "semester": 6,
        "prerequisites": ["MA201"],
        "description": "Financial systems, fintech applications, algorithmic trading, and financial data analysis.",
        "learning_outcomes": [
            "Understand financial systems",
            "Develop fintech applications",
            "Analyze financial data",
            "Implement trading algorithms"
        ],
        "concentrations": ["Finance"],
        "difficulty": 5,
        "hours_per_week": 6,
        "type": "Concentration"
    },
    
    "IT301": {
        "name": "Concentration - Information Technology",
        "credits": 3,
        "category": "Concentration",
        "semester": 6,
        "prerequisites": ["CE301"],
        "description": "Advanced IT topics including cloud computing, cybersecurity, and enterprise systems.",
        "learning_outcomes": [
            "Master cloud technologies",
            "Implement security measures",
            "Manage IT infrastructure",
            "Design enterprise solutions"
        ],
        "concentrations": ["IT"],
        "difficulty": 5,
        "hours_per_week": 6,
        "type": "Concentration"
    },
    
    "MG301": {
        "name": "Concentration - Management",
        "credits": 3,
        "category": "Concentration",
        "semester": 6,
        "prerequisites": ["CE303"],
        "description": "IT project management, agile methodologies, team leadership, and business strategy.",
        "learning_outcomes": [
            "Manage IT projects",
            "Apply agile methodologies",
            "Lead technical teams",
            "Align IT with business goals"
        ],
        "concentrations": ["Management"],
        "difficulty": 4,
        "hours_per_week": 5,
        "type": "Concentration"
    }
}

# Category colors for visualization
CATEGORY_COLORS = {
    "Programming": "#3b82f6",
    "Mathematics": "#8b5cf6",
    "Systems": "#10b981",
    "Algorithms": "#f59e0b",
    "Data": "#06b6d4",
    "AI/ML": "#ec4899",
    "Software Engineering": "#14b8a6",
    "Electronics": "#f97316",
    "Science": "#6366f1",
    "Business": "#eab308",
    "General": "#94a3b8",
    "Concentration": "#a855f7"
}

# Difficulty levels
DIFFICULTY_LEVELS = {
    1: "Very Easy",
    2: "Easy",
    3: "Moderate",
    4: "Challenging",
    5: "Difficult",
    6: "Very Difficult",
    7: "Expert"
}
