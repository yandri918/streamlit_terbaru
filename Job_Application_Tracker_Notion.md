# 💼 Job Application Tracker - Notion Database Template

**For AI Engineer / ML Engineer Positions**  
**Target: Global Companies (Remote/International)**

---

## 📊 Database Structure

Copy this template to create a Notion database for tracking your job applications.

---

## 🗂️ Database Properties (Columns)

### **1. Company Name** (Title)
- Type: Title
- Description: Company name

### **2. Position** (Text)
- Type: Text
- Description: Job title (e.g., "AI Engineer", "ML Engineer", "Senior AI Engineer")

### **3. Status** (Select)
- Type: Select
- Options:
  - 🎯 **Researching** (Gray)
  - 📝 **To Apply** (Blue)
  - ✉️ **Applied** (Yellow)
  - 📞 **Phone Screen** (Orange)
  - 💻 **Technical Interview** (Purple)
  - 🤝 **Final Interview** (Pink)
  - ✅ **Offer** (Green)
  - ❌ **Rejected** (Red)
  - 🔄 **On Hold** (Gray)

### **4. Priority** (Select)
- Type: Select
- Options:
  - 🔥 **High** (Red)
  - ⭐ **Medium** (Yellow)
  - 💡 **Low** (Blue)

### **5. Location** (Multi-select)
- Type: Multi-select
- Options:
  - 🌍 Remote (Global)
  - 🇺🇸 USA
  - 🇪🇺 Europe
  - 🇸🇬 Singapore
  - 🇯🇵 Japan
  - 🇦🇺 Australia
  - 🇨🇦 Canada
  - 🇬🇧 UK
  - 🇩🇪 Germany
  - 🇳🇱 Netherlands

### **6. Salary Range** (Text)
- Type: Text
- Format: "$120k-180k" or "€80k-120k"

### **7. Application Date** (Date)
- Type: Date
- Description: When you applied

### **8. Deadline** (Date)
- Type: Date
- Description: Application deadline (if any)

### **9. Next Action** (Text)
- Type: Text
- Description: What you need to do next

### **10. Next Action Date** (Date)
- Type: Date
- Description: When to do the next action

### **11. Job URL** (URL)
- Type: URL
- Description: Link to job posting

### **12. Company Website** (URL)
- Type: URL
- Description: Company website

### **13. Contact Person** (Text)
- Type: Text
- Description: Recruiter or hiring manager name

### **14. Contact Email** (Email)
- Type: Email
- Description: Contact email

### **15. LinkedIn** (URL)
- Type: URL
- Description: Contact's LinkedIn profile

### **16. Tech Stack** (Multi-select)
- Type: Multi-select
- Options:
  - Python
  - TensorFlow
  - PyTorch
  - scikit-learn
  - LLM
  - Computer Vision
  - NLP
  - AWS
  - GCP
  - Azure
  - Docker
  - Kubernetes
  - Streamlit
  - Flask
  - FastAPI

### **17. Company Type** (Select)
- Type: Select
- Options:
  - 🚀 Startup (Seed/Series A)
  - 📈 Scale-up (Series B-D)
  - 🏢 Enterprise
  - 🌟 FAANG/Big Tech
  - 🌱 AgriTech
  - 🌍 Climate Tech
  - 💰 FinTech
  - 🏥 HealthTech
  - 🛒 E-commerce

### **18. Interview Rounds** (Number)
- Type: Number
- Description: Total interview rounds

### **19. Current Round** (Number)
- Type: Number
- Description: Which round you're on

### **20. Notes** (Text - Long)
- Type: Text (Long)
- Description: Any additional notes

### **21. Referral** (Checkbox)
- Type: Checkbox
- Description: Did you get a referral?

### **22. Referral Source** (Text)
- Type: Text
- Description: Who referred you

### **23. Response Rate** (Formula)
- Type: Formula
- Formula: `if(prop("Status") == "Applied" or prop("Status") == "Phone Screen" or prop("Status") == "Technical Interview" or prop("Status") == "Final Interview" or prop("Status") == "Offer", "✅ Response", if(prop("Status") == "Rejected", "❌ No Response", "⏳ Pending"))`

### **24. Days Since Applied** (Formula)
- Type: Formula
- Formula: `dateBetween(now(), prop("Application Date"), "days")`

---

## 📋 Sample Entries

### Entry 1: OpenAI
- **Company Name:** OpenAI
- **Position:** AI Engineer
- **Status:** Applied
- **Priority:** High
- **Location:** Remote (Global), USA
- **Salary Range:** $150k-200k
- **Application Date:** 2026-01-05
- **Next Action:** Follow up email
- **Next Action Date:** 2026-01-12
- **Job URL:** https://openai.com/careers
- **Tech Stack:** Python, PyTorch, LLM, NLP
- **Company Type:** Big Tech
- **Notes:** Applied through website. Mentioned AgriSensa project in cover letter.

### Entry 2: AgriTech Startup (Series B)
- **Company Name:** FarmWise
- **Position:** Senior ML Engineer
- **Status:** Phone Screen
- **Priority:** High
- **Location:** Remote (Global)
- **Salary Range:** $130k-170k
- **Application Date:** 2026-01-03
- **Next Action:** Prepare for technical interview
- **Next Action Date:** 2026-01-15
- **Tech Stack:** Python, TensorFlow, Computer Vision, AWS
- **Company Type:** AgriTech
- **Referral:** Yes
- **Referral Source:** LinkedIn connection (John Doe)
- **Notes:** Great culture fit. They loved AgriSensa project. Technical interview scheduled.

### Entry 3: Google DeepMind
- **Company Name:** Google DeepMind
- **Position:** Research Engineer
- **Status:** Researching
- **Priority:** High
- **Location:** UK, Remote
- **Salary Range:** £80k-120k
- **Next Action:** Prepare application materials
- **Next Action Date:** 2026-01-20
- **Job URL:** https://deepmind.google/careers
- **Tech Stack:** Python, TensorFlow, PyTorch, Deep Learning
- **Company Type:** FAANG/Big Tech
- **Notes:** Need to strengthen research portfolio. Consider publishing blog post first.

---

## 📊 Recommended Views

### View 1: **Active Applications**
- Filter: Status = "Applied" OR "Phone Screen" OR "Technical Interview" OR "Final Interview"
- Sort: Next Action Date (Ascending)
- Group by: Status

### View 2: **High Priority**
- Filter: Priority = "High" AND Status ≠ "Rejected" AND Status ≠ "Offer"
- Sort: Next Action Date (Ascending)

### View 3: **By Company Type**
- Group by: Company Type
- Sort: Priority (Descending)

### View 4: **By Location**
- Group by: Location
- Filter: Status ≠ "Rejected"

### View 5: **Timeline (Calendar)**
- View Type: Calendar
- Date Property: Application Date
- Show: All applications

### View 6: **Kanban Board**
- View Type: Board
- Group by: Status
- Sort: Priority (Descending)

### View 7: **Awaiting Response**
- Filter: Status = "Applied" AND Days Since Applied > 7
- Sort: Days Since Applied (Descending)

---

## 🎯 Weekly Review Template

Create a separate page for weekly reviews:

### **Week of [Date]**

**📊 Statistics:**
- Applications sent this week: __
- Responses received: __
- Interviews scheduled: __
- Offers received: __
- Rejections: __

**✅ Wins:**
- 

**📝 Learnings:**
- 

**🎯 Next Week Goals:**
- [ ] Apply to X companies
- [ ] Prepare for Y interviews
- [ ] Follow up with Z recruiters

**🔄 Action Items:**
- [ ] 
- [ ] 
- [ ] 

---

## 📧 Email Templates (Store in Notion)

### Template 1: Follow-up Email (After 1 Week)
```
Subject: Following Up - [Position] Application

Hi [Recruiter Name],

I hope this email finds you well. I wanted to follow up on my application for the [Position] role at [Company], which I submitted on [Date].

I'm very excited about the opportunity to contribute to [Company]'s mission, particularly [specific aspect of company/role]. My experience building AgriSensa (a production-grade multi-modal AI platform with 25+ modules and 99.5% uptime) has prepared me well for the challenges of this role.

I'd love to discuss how my background in [relevant skills] could add value to your team.

Thank you for your time and consideration.

Best regards,
Andriyanto
[LinkedIn] | [GitHub] | [Portfolio]
```

### Template 2: Thank You Email (After Interview)
```
Subject: Thank You - [Position] Interview

Hi [Interviewer Name],

Thank you for taking the time to speak with me today about the [Position] role at [Company]. I really enjoyed learning about [specific topic discussed] and [team/project details].

Our conversation reinforced my enthusiasm for this opportunity. I'm particularly excited about [specific aspect], and I believe my experience with [relevant project/skill] would enable me to contribute meaningfully from day one.

Please don't hesitate to reach out if you need any additional information. I look forward to hearing about the next steps.

Best regards,
Andriyanto
```

### Template 3: Networking Message (LinkedIn)
```
Hi [Name],

I came across your profile while researching [Company] and was impressed by your work on [specific project/achievement].

I'm an AI Engineer with production experience in multi-modal AI systems (LLM + Computer Vision + Predictive ML). I recently built AgriSensa, an AI platform serving farmers with 25+ modules and 99.5% uptime.

I'm very interested in opportunities at [Company], particularly in [area]. Would you be open to a brief chat about your experience there?

Thank you for considering!

Best,
Andriyanto
[Portfolio Link]
```

---

## 📈 Metrics Dashboard

Create a separate page with these metrics:

### **Overall Statistics**
- Total Applications: [Formula: countall()]
- Active Applications: [Formula: count where Status = Active]
- Response Rate: [Formula: (Responses / Total) * 100]
- Interview Rate: [Formula: (Interviews / Total) * 100]
- Offer Rate: [Formula: (Offers / Total) * 100]

### **By Status**
- 📝 To Apply: [Count]
- ✉️ Applied: [Count]
- 📞 Phone Screen: [Count]
- 💻 Technical Interview: [Count]
- 🤝 Final Interview: [Count]
- ✅ Offer: [Count]
- ❌ Rejected: [Count]

### **By Company Type**
- Startups: [Count]
- Scale-ups: [Count]
- Enterprise: [Count]
- FAANG: [Count]
- AgriTech: [Count]

### **Average Timeline**
- Days to first response: [Average]
- Days to interview: [Average]
- Days to offer: [Average]

---

## 🎯 Best Practices

### **Daily:**
- [ ] Check for new job postings (30 min)
- [ ] Apply to 1-2 companies
- [ ] Follow up on pending applications
- [ ] Update database with any responses

### **Weekly:**
- [ ] Review all active applications
- [ ] Update next actions
- [ ] Prepare for upcoming interviews
- [ ] Network with 5-10 people on LinkedIn
- [ ] Write weekly review

### **Monthly:**
- [ ] Analyze metrics
- [ ] Adjust strategy based on data
- [ ] Update resume/portfolio if needed
- [ ] Reach out to recruiters

---

## 🔗 Related Pages (Create These in Notion)

1. **Interview Preparation**
   - Common questions & answers
   - Technical questions practice
   - System design templates
   - Behavioral questions (STAR method)

2. **Company Research**
   - Company profiles
   - Tech stack notes
   - Culture notes
   - Glassdoor reviews summary

3. **Networking Contacts**
   - Database of contacts
   - Conversation notes
   - Follow-up reminders

4. **Skills Development**
   - Courses to take
   - Certifications to get
   - Projects to build
   - Books to read

5. **Salary Negotiation**
   - Market research
   - Negotiation scripts
   - Offer comparison template

---

## 📱 Mobile App

Install Notion mobile app to:
- Update status on the go
- Check next actions
- Take notes during interviews
- Quick follow-ups

---

## 🎨 Customization Tips

1. **Add Icons:**
   - Use company logos as page icons
   - Add emojis to status options

2. **Add Relations:**
   - Link to Interview Prep pages
   - Link to Company Research pages
   - Link to Contact database

3. **Add Automations (if using Notion Pro):**
   - Auto-update "Days Since Applied"
   - Send reminders for follow-ups
   - Archive old rejections

4. **Color Coding:**
   - High priority = Red
   - Medium priority = Yellow
   - Low priority = Blue

---

## 📊 Success Metrics to Track

After 1 month:
- Applications sent: Target 20-30
- Response rate: Target 30-40%
- Interview rate: Target 10-20%
- Offer rate: Target 5-10%

After 3 months:
- Should have 2-3 offers
- Choose best fit
- Start new role!

---

**Good luck with your job search! 🚀**

---

## 🔖 Tags

`Job Search` `Career` `AI Engineer` `ML Engineer` `Application Tracking` `Notion Template` `Productivity` `Job Hunt` `Career Development`
