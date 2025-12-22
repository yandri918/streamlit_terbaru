import sys
import os

# Add app to path
sys.path.append(os.getcwd())

try:
    from app.services.research_service import ResearchService
    print("Successfully imported ResearchService")
except ImportError as e:
    print(f"Failed to import ResearchService: {e}")
    sys.exit(1)

# Sample Data
data = {
    "treatment_names": ["P0", "P1", "P2"],
    "replications": 3,
    "parameters": {
        "Tinggi Tanaman": [
            [10, 12, 11], # Data for P0
            [15, 16, 14], # Data for P1
            [20, 22, 21]  # Data for P2
        ]
    }
}

print("Running analysis...")
try:
    results = ResearchService.analyze_ral(data)
    print("Analysis successful!")
    print(results)
except Exception as e:
    print("Analysis failed!")
    import traceback
    traceback.print_exc()
