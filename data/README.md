# 📊 Data Analyst Portfolio

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Transforming Data into Actionable Insights**

A comprehensive portfolio showcasing professional data analysis projects with interactive visualizations, statistical analysis, and machine learning applications.

🔗 **Live Demo:** [View Portfolio](https://your-streamlit-app.streamlit.app)

---

## 🎯 Featured Projects

### 1. 📈 Stock Price Analysis
Comprehensive stock market analysis with interactive visualizations and technical indicators.

**Features:**
- Candlestick charts with volume analysis
- Moving averages (SMA, EMA)
- Volatility analysis and risk metrics
- Price trend identification
- Interactive date range selection

**Technologies:** Python, Pandas, Altair, Statistical Analysis  
**Dataset:** 1,500+ data points from major stock exchanges

---

### 2. 🛡️ Credit Card Fraud Detection
Advanced fraud detection system using machine learning and anomaly detection techniques.

**Features:**
- PCA-based dimensionality reduction
- Anomaly detection algorithms
- Interactive scatter plots and heatmaps
- Fraud pattern visualization
- Model performance metrics

**Technologies:** Python, Scikit-learn, PCA, Altair  
**Dataset:** 284,000+ credit card transactions

---

### 3. 💰 Gold Price Analysis
Time series analysis and forecasting of gold prices for investment decision support.

**Features:**
- Historical price trend analysis
- Moving average crossover signals
- Volatility analysis
- Price prediction models
- Investment insights

**Technologies:** Python, Pandas, Time Series Analysis  
**Dataset:** Historical gold prices with multiple timeframes

---

### 4. 🗳️ Survey Sampling & Election Polling
Professional survey sampling calculator for election polling and public opinion research.

**Features:**
- **Sample Size Calculator:** Determine required respondents with finite population correction
- **Survey Results Analysis:** Confidence intervals and statistical significance testing
- **Margin of Error Calculator:** Calculate MoE with interactive visualizations
- **Educational Guide:** Comprehensive theory, best practices, and real-world examples

**Technologies:** Python, SciPy, Plotly, Statistical Inference  
**Use Cases:** Political polling, market research, academic surveys

**Key Capabilities:**
- Finite population correction (FPC)
- Confidence interval estimation (90%, 95%, 99%)
- Statistical significance testing (overlap detection)
- Sample size optimization (cost vs accuracy trade-off)
- Professional reporting standards

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yandri918/data.git
cd data
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run Home.py
```

4. **Open your browser:**
The app will automatically open at `http://localhost:8501`

---

## 📦 Dependencies

```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
altair>=5.0.0
plotly>=5.14.0
scipy>=1.10.0
scikit-learn>=1.3.0
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
data/
├── Home.py                      # Main landing page
├── pages/                       # Individual project pages
│   ├── 1_Stock_Analysis.py     # Stock price analysis
│   ├── 2_Credit_Fraud.py       # Fraud detection
│   ├── 3_Gold_Analysis.py      # Gold price analysis
│   └── 4_Survey_Sampling.py    # Survey sampling calculator
├── data/                        # Dataset files
│   └── *.csv                   # CSV data files
├── utils/                       # Utility functions
│   ├── data_loader.py          # Data loading utilities
│   ├── visualizations.py       # Visualization helpers
│   └── statistics.py           # Statistical functions
├── .streamlit/                  # Streamlit configuration
│   └── config.toml             # App configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🛠️ Technologies & Skills

### Programming Languages
- **Python** - Primary language for data analysis

### Data Analysis & Manipulation
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **SciPy** - Scientific computing and statistics

### Machine Learning
- **Scikit-learn** - ML algorithms and model evaluation
- **PCA** - Dimensionality reduction
- **Anomaly Detection** - Fraud detection algorithms

### Data Visualization
- **Altair** - Declarative statistical visualizations
- **Plotly** - Interactive charts and graphs
- **Streamlit** - Web app framework

### Statistical Analysis
- **Hypothesis Testing** - Statistical inference
- **Confidence Intervals** - Uncertainty quantification
- **Time Series Analysis** - Trend and seasonality analysis
- **Survey Sampling** - Sample size and margin of error calculations

---

## 📊 Key Features

### Interactive Visualizations
- **Responsive charts** that adapt to user input
- **Hover tooltips** with detailed information
- **Zoom and pan** capabilities
- **Dynamic filtering** and date range selection

### Statistical Rigor
- **Confidence intervals** for all estimates
- **Statistical significance testing**
- **Proper error handling** and validation
- **Professional reporting standards**

### User Experience
- **Clean, modern UI** with glassmorphism design
- **Intuitive navigation** between projects
- **Responsive layout** for all screen sizes
- **Fast loading** with optimized data processing

### Educational Content
- **Detailed explanations** of methodologies
- **Best practices** and industry standards
- **Real-world examples** and case studies
- **Interactive learning** through calculators

---

## 🎓 Survey Sampling Module - Deep Dive

The Survey Sampling & Election Polling module is a professional-grade tool for survey methodology:

### Sample Size Calculator
**Formula:**
```
n = (Z² × p × (1-p)) / E²

Finite Population Correction:
n_adjusted = n / (1 + (n-1)/N)
```

**Example:**
- Population: 200,000,000 (Indonesia voters)
- Confidence Level: 95% (Z=1.96)
- Margin of Error: ±3%
- Expected Proportion: 50% (worst case)
- **Result: 1,067 respondents needed**

### Statistical Significance Testing
Automatically detects if differences between candidates are statistically significant:

```
Candidate A: 45% [42.2% - 47.8%]
Candidate B: 43% [40.3% - 45.7%]

CIs overlap → Not statistically significant
Decision: Too early to call a winner
```

### Best Practices Included
- **Sample sizes:** National (1,000-1,200), Regional (400-600), Local (300-400)
- **Sampling methods:** Random, Stratified, Cluster
- **Reporting standards:** Always include n, MoE, confidence level, date, methodology
- **Red flags:** Sample < 300, MoE > 5%, no methodology disclosed

---

## 📈 Use Cases

### For Researchers
- Calculate accurate sample sizes for studies
- Analyze survey results with confidence intervals
- Test statistical significance of findings
- Learn survey methodology best practices

### For Media & Journalists
- Report election polls responsibly
- Understand margin of error implications
- Identify reliable vs unreliable polls
- Avoid common polling mistakes

### For Political Campaigns
- Plan polling budgets efficiently
- Determine if leads are statistically significant
- Track trends over time
- Make data-driven strategy decisions

### For Students & Educators
- Learn survey sampling theory
- Practice with interactive calculators
- Study real-world examples
- Understand statistical inference

---

## 🔬 Technical Highlights

### Statistical Methods
- **Finite Population Correction** - Adjusts for small populations
- **Wald Method** - Confidence interval calculation
- **Normal Approximation** - Valid for n > 30
- **Z-scores** - 80%, 85%, 90%, 95%, 99% confidence levels

### Visualizations
- **Error bar charts** - Show confidence intervals visually
- **Interactive curves** - MoE vs sample size relationships
- **Comparison tables** - Cost-benefit analysis
- **Professional styling** - Publication-ready graphics

### Code Quality
- **Modular design** - Reusable functions
- **Input validation** - Prevent errors
- **Error handling** - Graceful degradation
- **Documentation** - Clear comments and docstrings

---

## 📚 References & Resources

### Academic
- Cochran, W.G. (1977). *Sampling Techniques*. Wiley.
- Lohr, S.L. (2019). *Sampling: Design and Analysis*. CRC Press.

### Industry Standards
- [Pew Research Center - Survey Methodology](https://www.pewresearch.org/methods/)
- [AAPOR - American Association for Public Opinion Research](https://www.aapor.org/)

### Technical Documentation
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [SciPy Stats Module](https://docs.scipy.org/doc/scipy/reference/stats.html)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Contribution Guidelines
- Follow PEP 8 style guide for Python code
- Add docstrings to all functions
- Include unit tests for new features
- Update README if adding new functionality

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Yandri**

- GitHub: [@yandri918](https://github.com/yandri918)
- Portfolio: [Data Analyst Portfolio](https://github.com/yandri918/data)

---

## 🙏 Acknowledgments

- **Streamlit** - For the amazing web app framework
- **Plotly** - For interactive visualization capabilities
- **SciPy** - For statistical computing tools
- **Open Source Community** - For inspiration and resources

---

## 📞 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/yandri918/data/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yandri918/data/discussions)
- **Email:** Contact via GitHub profile

---

## 🎯 Future Enhancements

### Planned Features
- [ ] Stratified sampling calculator
- [ ] Power analysis for hypothesis testing
- [ ] Weighting and post-stratification
- [ ] Non-response bias adjustment
- [ ] PDF report generation
- [ ] Excel export functionality
- [ ] API endpoints for programmatic access

### Additional Projects
- [ ] Customer segmentation analysis
- [ ] Sales forecasting dashboard
- [ ] A/B testing calculator
- [ ] Cohort analysis tool

---

## 📊 Project Statistics

- **Total Projects:** 4
- **Total Data Points:** 285,000+
- **Visualization Types:** 20+
- **Statistical Methods:** 15+
- **Lines of Code:** 2,500+

---

## 🌟 Star History

If you find this portfolio useful, please consider giving it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=yandri918/data&type=Date)](https://star-history.com/#yandri918/data&Date)

---

<div align="center">

**Built with ❤️ using Streamlit & Python**

© 2026 Data Analyst Portfolio | All Rights Reserved

</div>
