"""
Concentration Data for UTel University - Computer Engineering Program
Three specialization tracks: Finance, IT, and Management
"""

CONCENTRATIONS = {
    "Finance": {
        "name": "Financial Technology & Computing",
        "description": "Combine computer engineering with financial systems, algorithmic trading, and fintech applications.",
        "required_courses": ["FI301", "MA201", "CE304", "CE402"],
        "elective_courses": ["CE401", "CE204"],
        "total_credits": 18,
        "skills": {
            "Programming": 70,
            "Mathematics": 90,
            "Business": 85,
            "Systems": 60,
            "AI/ML": 50,
            "Data Analysis": 95
        },
        "career_paths": [
            "Quantitative Analyst",
            "Financial Software Developer",
            "Algorithmic Trader",
            "Fintech Engineer",
            "Risk Management Analyst",
            "Data Scientist (Finance)"
        ],
        "average_salary": "$85,000 - $150,000",
        "job_growth": "15% (2024-2034)",
        "top_companies": ["Goldman Sachs", "JP Morgan", "Bloomberg", "Stripe", "PayPal"]
    },
    
    "IT": {
        "name": "Information Technology & Systems",
        "description": "Deep dive into IT infrastructure, cloud computing, cybersecurity, and enterprise systems.",
        "required_courses": ["IT301", "CE301", "CE203", "CE402"],
        "elective_courses": ["CE401", "CE302"],
        "total_credits": 18,
        "skills": {
            "Programming": 85,
            "Mathematics": 70,
            "Business": 50,
            "Systems": 95,
            "AI/ML": 75,
            "Data Analysis": 70
        },
        "career_paths": [
            "Cloud Architect",
            "DevOps Engineer",
            "Cybersecurity Specialist",
            "Network Engineer",
            "Systems Administrator",
            "AI/ML Engineer"
        ],
        "average_salary": "$90,000 - $160,000",
        "job_growth": "22% (2024-2034)",
        "top_companies": ["Google", "Microsoft", "Amazon", "Meta", "Netflix"]
    },
    
    "Management": {
        "name": "IT Project Management & Leadership",
        "description": "Combine technical skills with project management, team leadership, and business strategy.",
        "required_courses": ["MG301", "CE303", "BU201"],
        "elective_courses": ["CE401", "CE304"],
        "total_credits": 15,
        "skills": {
            "Programming": 65,
            "Mathematics": 60,
            "Business": 90,
            "Systems": 70,
            "AI/ML": 40,
            "Data Analysis": 65
        },
        "career_paths": [
            "IT Project Manager",
            "Product Manager",
            "Technical Lead",
            "Scrum Master",
            "Business Analyst",
            "CTO/VP Engineering"
        ],
        "average_salary": "$80,000 - $180,000",
        "job_growth": "18% (2024-2034)",
        "top_companies": ["Accenture", "Deloitte", "McKinsey", "IBM", "Salesforce"]
    }
}

# Skill categories for radar chart
SKILL_CATEGORIES = [
    "Programming",
    "Mathematics",
    "Business",
    "Systems",
    "AI/ML",
    "Data Analysis"
]

# Concentration comparison matrix
CONCENTRATION_COMPARISON = {
    "Technical Depth": {
        "Finance": 75,
        "IT": 95,
        "Management": 60
    },
    "Business Acumen": {
        "Finance": 85,
        "IT": 50,
        "Management": 90
    },
    "Math Intensity": {
        "Finance": 90,
        "IT": 70,
        "Management": 60
    },
    "Leadership Skills": {
        "Finance": 60,
        "IT": 65,
        "Management": 95
    },
    "Innovation Potential": {
        "Finance": 80,
        "IT": 90,
        "Management": 75
    }
}
