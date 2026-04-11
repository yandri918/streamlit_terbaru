
import json
import re
import os
import glob

def extract_course_data(filepath):
    filename = os.path.basename(filepath)
    # Parse filename like "1_📐_MA101_Calculus.py"
    # Or "10_📊_MA201_Statistics.py"
    
    # Updated regex to handle varying formats more robustly
    filename_match = re.match(r"(\d+)_([^_]+)_([^_]+)_(.+)\.py", filename)
    
    if not filename_match:
        print(f"Skipping {filename}: Does not match pattern")
        return None
        
    order_num, icon, course_id, course_name_raw = filename_match.groups()
    course_name = course_name_raw.replace("_", " ")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract Credits, Semester, Difficulty, Hours
    # st.metric("Credits", "4")
    credits = re.search(r'st\.metric\("Credits",\s*"([^"]+)"\)', content)
    semester = re.search(r'st\.metric\("Semester",\s*"([^"]+)"\)', content)
    difficulty = re.search(r'st\.metric\("Difficulty",\s*"([^"]+)"\)', content)
    hours = re.search(r'st\.metric\("Hours/Week",\s*"([^"]+)"\)', content)
    
    credits_val = credits.group(1) if credits else "3"
    semester_val = semester.group(1) if semester else "1"
    difficulty_val = difficulty.group(1) if difficulty else "N/A"
    hours_val = hours.group(1) if hours else "N/A"
    
    # Extract Syllabus / Description
    # Look for content in Tab 1 (Overview)
    # This is rough extraction
    desc_match = re.search(r'<div class="theory-box">\s*<h3>Course Description</h3>\s*<p>(.*?)</p>', content, re.DOTALL)
    description = desc_match.group(1).strip().replace("\n", " ") if desc_match else "No description available."
    
    # Extract topics
    topics = []
    topics_match = re.findall(r'- (.*?)$', content, re.MULTILINE)
    # Filter out empty or too short lines, take first 10
    topics = [t.strip() for t in topics_match if len(t) > 3][:10]

    return {
        "id": course_id,
        "name": course_name,
        "icon": icon,
        "credits": credits_val,
        "semester": semester_val,
        "difficulty": difficulty_val,
        "hours": hours_val,
        "description": description,
        "topics": topics,
        "filename": filename, # For reference
        "resources": [] # Placeholder
    }

def main():
    pages_dir = "c:/Users/yandr/OneDrive/Desktop/agrisensa-api/computer_enginer/pages"
    output_file = "c:/Users/yandr/OneDrive/Desktop/agrisensa-api/computer_enginer/data/curriculum.json"
    
    files = glob.glob(os.path.join(pages_dir, "*.py"))
    
    curriculum = {}
    
    for f in files:
        if "Semester" in f or "Course_Catalog" in f or "Roadmap" in f:
            continue
            
        data = extract_course_data(f)
        if data:
            sem_key = f"Semester {data['semester']}"
            if sem_key not in curriculum:
                curriculum[sem_key] = []
            curriculum[sem_key].append(data)
            
    # Sort by ID within semester
    for sem in curriculum:
        curriculum[sem].sort(key=lambda x: x['id'])
        
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(curriculum, f, indent=4, ensure_ascii=False)
        
    print(f"Generated curriculum.json with {sum(len(v) for v in curriculum.values())} courses")

if __name__ == "__main__":
    main()
