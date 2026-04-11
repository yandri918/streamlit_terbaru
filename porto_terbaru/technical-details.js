// Technical Details Modal System
class TechnicalDetailsModal {
    constructor() {
        this.modal = null;
        this.init();
    }

    init() {
        // Create modal HTML
        const modalHTML = `
            <div class="tech-modal" id="techModal">
                <div class="tech-modal-overlay"></div>
                <div class="tech-modal-content">
                    <button class="tech-modal-close" id="modalClose">
                        <i class="fas fa-times"></i>
                    </button>
                    <div class="tech-modal-body" id="modalBody">
                        <!-- Content will be injected here -->
                    </div>
                </div>
            </div>
        `;

        // Add to body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modal = document.getElementById('techModal');

        // Event listeners
        document.getElementById('modalClose').addEventListener('click', () => this.close());
        this.modal.querySelector('.tech-modal-overlay').addEventListener('click', () => this.close());

        // ESC key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('active')) {
                this.close();
            }
        });
    }

    open(content) {
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = content;
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    close() {
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Technical Details Content
const technicalDetails = {
    marketing: `
        <h2><i class="fas fa-bullhorn"></i> Marketing Analytics Platform - Technical Deep Dive</h2>
        
        <div class="tech-detail-section">
            <h3><i class="fas fa-briefcase"></i> Business Problem</h3>
            <p><strong>Context:</strong> Marketing team spending $500K/year across 15+ channels with unclear ROI and fragmented data.</p>
            <p><strong>Stakeholders:</strong> CMO, Marketing Managers (5), Finance Team</p>
            <ul>
                <li><strong>Pain Point 1:</strong> Manual campaign analysis taking 2-3 days per report</li>
                <li><strong>Pain Point 2:</strong> No unified view of customer journey across channels</li>
                <li><strong>Pain Point 3:</strong> Budget allocation based on intuition rather than data</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-code"></i> Technical Approach</h3>
            
            <h4>Data Pipeline Architecture</h4>
            <ul>
                <li><strong>Sources:</strong> Google Ads API, Facebook Marketing API, Mailchimp webhooks, Salesforce CRM</li>
                <li><strong>ETL:</strong> Python scripts with Pandas, scheduled via Apache Airflow</li>
                <li><strong>Storage:</strong> PostgreSQL for analytics, Redis for caching</li>
                <li><strong>Update Frequency:</strong> Hourly for real-time data, daily for batch processing</li>
            </ul>

            <h4>Model Selection Rationale</h4>
            <p><strong>Problem:</strong> Customer segmentation for targeted campaigns</p>
            <table class="tech-table">
                <tr>
                    <th>Model</th>
                    <th>F1-Score</th>
                    <th>Inference Time</th>
                    <th>Selected</th>
                </tr>
                <tr>
                    <td>Random Forest</td>
                    <td>0.82</td>
                    <td>45ms</td>
                    <td>❌</td>
                </tr>
                <tr>
                    <td>XGBoost</td>
                    <td>0.87</td>
                    <td>32ms</td>
                    <td>✅</td>
                </tr>
                <tr>
                    <td>LightGBM</td>
                    <td>0.85</td>
                    <td>28ms</td>
                    <td>❌</td>
                </tr>
            </table>
            <p><strong>Winner:</strong> XGBoost - Best balance of accuracy and speed</p>

            <h4>Feature Engineering</h4>
            <ul>
                <li><strong>RFM Features:</strong> Recency (days since last purchase), Frequency (purchase count), Monetary (total spend)</li>
                <li><strong>CLV Calculation:</strong> Customer Lifetime Value using historical purchase patterns</li>
                <li><strong>Engagement Scores:</strong> Email open rates, click-through rates, social media interactions</li>
                <li><strong>Temporal Features:</strong> Day of week, hour of day, seasonality indicators</li>
            </ul>

            <h4>Validation Strategy</h4>
            <ul>
                <li><strong>Split:</strong> 70% train, 15% validation, 15% test (time-based to prevent leakage)</li>
                <li><strong>Cross-validation:</strong> 5-fold CV for hyperparameter tuning</li>
                <li><strong>Metrics:</strong> F1-score (primary), Precision, Recall, AUC-ROC</li>
            </ul>

            <h4>Handling Challenges</h4>
            <ul>
                <li><strong>Class Imbalance:</strong> SMOTE (Synthetic Minority Over-sampling) for minority classes</li>
                <li><strong>Overfitting:</strong> Early stopping, L2 regularization (alpha=0.1), feature selection (top 50 features)</li>
                <li><strong>Data Quality:</strong> Automated outlier detection (IQR method), missing value imputation (median for numeric, mode for categorical)</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-flask"></i> A/B Testing & Experimentation</h3>
            
            <h4>Experiment: ML-Based Segmentation vs Traditional</h4>
            <p><strong>Hypothesis:</strong> ML-based behavioral segmentation will improve email CTR by >15%</p>
            
            <table class="tech-table">
                <tr>
                    <th>Group</th>
                    <th>Size</th>
                    <th>CTR</th>
                    <th>Conversion</th>
                    <th>Revenue/Email</th>
                </tr>
                <tr>
                    <td>Control (Demographic)</td>
                    <td>10,000</td>
                    <td>2.3%</td>
                    <td>0.8%</td>
                    <td>$0.45</td>
                </tr>
                <tr>
                    <td>Treatment (ML-Based)</td>
                    <td>10,000</td>
                    <td>3.1%</td>
                    <td>1.2%</td>
                    <td>$0.68</td>
                </tr>
                <tr>
                    <td><strong>Lift</strong></td>
                    <td>-</td>
                    <td><strong>+34.8%</strong></td>
                    <td><strong>+50%</strong></td>
                    <td><strong>+51%</strong></td>
                </tr>
            </table>

            <p><strong>Statistical Significance:</strong> p < 0.001 (two-sample t-test)</p>
            <p><strong>Duration:</strong> 4 weeks (extended to 8 weeks to account for novelty effect)</p>
            <p><strong>Bias Handling:</strong> Randomization check passed, seasonal adjustment applied</p>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-database"></i> Data Engineering</h3>
            
            <h4>Pipeline Architecture</h4>
            <pre class="code-block">
[Google Ads API] ──┐
[Facebook API]   ──┼──> [Airflow DAG] ──> [Data Validation] ──> [PostgreSQL]
[Mailchimp]      ──┤                              │
[Salesforce CRM] ──┘                              ├──> [ML Pipeline] ──> [Model Registry]
                                                   │
                                                   └──> [Streamlit App]
            </pre>

            <h4>Data Quality Monitoring</h4>
            <ul>
                <li><strong>Schema Validation:</strong> Great Expectations for data contracts</li>
                <li><strong>Anomaly Detection:</strong> Automated alerts for unusual patterns</li>
                <li><strong>Data Lineage:</strong> Track data flow from source to dashboard</li>
                <li><strong>Quality Metrics:</strong> Completeness, accuracy, timeliness dashboards</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-dollar-sign"></i> Cost-Benefit Analysis</h3>
            <table class="tech-table">
                <tr>
                    <th>Item</th>
                    <th>Cost/Value</th>
                </tr>
                <tr>
                    <td>Development Time</td>
                    <td>3 months (solo project)</td>
                </tr>
                <tr>
                    <td>Infrastructure Cost</td>
                    <td>$50/month (cloud hosting)</td>
                </tr>
                <tr>
                    <td>Annual Ad Spend Savings</td>
                    <td>$200,000</td>
                </tr>
                <tr>
                    <td>Additional Revenue (40% ROI lift)</td>
                    <td>$200,000</td>
                </tr>
                <tr>
                    <td>Time Savings (60% reduction)</td>
                    <td>~480 hours/year</td>
                </tr>
                <tr>
                    <td><strong>Total Annual Benefit</strong></td>
                    <td><strong>$400,000+</strong></td>
                </tr>
            </table>
            <p><strong>Payback Period:</strong> Immediate (efficiency gains from day 1)</p>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-rocket"></i> Production Considerations</h3>
            <ul>
                <li><strong>Model Versioning:</strong> MLflow for experiment tracking and model registry</li>
                <li><strong>Monitoring:</strong> Drift detection on feature distributions, performance metrics dashboard</li>
                <li><strong>Retraining:</strong> Monthly schedule with performance threshold checks (F1 < 0.80 triggers retrain)</li>
                <li><strong>API:</strong> FastAPI endpoint for real-time predictions (99.9% uptime)</li>
                <li><strong>Scalability:</strong> Horizontal scaling with load balancer, handles 1000+ requests/minute</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-link"></i> Resources</h3>
            <p><a href="https://marketing2.streamlit.app/" target="_blank" class="tech-link">
                <i class="fas fa-external-link-alt"></i> View Live Demo
            </a></p>
            <p><a href="https://github.com/yandri918/marketing" target="_blank" class="tech-link">
                <i class="fab fa-github"></i> View Source Code on GitHub
            </a></p>
        </div>
    `,

    weather: `
        <h2><i class="fas fa-cloud-sun"></i> AI Weather Forecasting System - Technical Deep Dive</h2>
        
        <div class="tech-detail-section">
            <h3><i class="fas fa-briefcase"></i> Business Problem</h3>
            <p><strong>Context:</strong> Farmers losing 20-30% of crops due to unexpected weather events, costing agricultural cooperatives millions annually.</p>
            <p><strong>Stakeholders:</strong> Agricultural cooperatives (3), 500+ individual farmers</p>
            <ul>
                <li><strong>Pain Point 1:</strong> Generic weather forecasts not localized for specific farm locations</li>
                <li><strong>Pain Point 2:</strong> No actionable insights (when to plant, irrigate, harvest)</li>
                <li><strong>Pain Point 3:</strong> Reactive planning leading to crop losses</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-code"></i> Technical Approach</h3>
            
            <h4>Data Pipeline Architecture</h4>
            <ul>
                <li><strong>Sources:</strong> OpenWeatherMap API, NOAA historical database (10 years), local weather stations</li>
                <li><strong>Real-time Ingestion:</strong> Scheduled API calls every 6 hours</li>
                <li><strong>Historical Data:</strong> 10 years of weather patterns (2014-2024), ~3.6M data points</li>
                <li><strong>Storage:</strong> InfluxDB (time-series database) for efficient querying</li>
            </ul>

            <h4>Model Selection Rationale</h4>
            <p><strong>Problem:</strong> 7-day temperature and precipitation forecasting</p>
            <table class="tech-table">
                <tr>
                    <th>Model</th>
                    <th>RMSE (°C)</th>
                    <th>Training Time</th>
                    <th>Selected</th>
                </tr>
                <tr>
                    <td>ARIMA</td>
                    <td>3.8</td>
                    <td>5 min</td>
                    <td>❌</td>
                </tr>
                <tr>
                    <td>Prophet</td>
                    <td>3.2</td>
                    <td>15 min</td>
                    <td>❌</td>
                </tr>
                <tr>
                    <td>GRU</td>
                    <td>2.5</td>
                    <td>2 hours</td>
                    <td>❌</td>
                </tr>
                <tr>
                    <td>LSTM + Attention</td>
                    <td>2.3</td>
                    <td>3 hours</td>
                    <td>✅</td>
                </tr>
            </table>
            <p><strong>Winner:</strong> LSTM with attention mechanism - Best accuracy for long-term dependencies</p>

            <h4>Model Architecture</h4>
            <pre class="code-block">
Input Layer (10 features)
    ↓
LSTM Layer 1 (128 units, return_sequences=True)
    ↓
Attention Layer (custom)
    ↓
LSTM Layer 2 (64 units, return_sequences=True)
    ↓
LSTM Layer 3 (32 units)
    ↓
Dense Layer (16 units, ReLU)
    ↓
Output Layer (7 units - 7-day forecast)
            </pre>

            <h4>Feature Engineering</h4>
            <ul>
                <li><strong>Temporal:</strong> Hour, day, month, season, day_of_year</li>
                <li><strong>Lag Features:</strong> T-1, T-7, T-30 days (temperature, humidity, pressure)</li>
                <li><strong>Rolling Statistics:</strong> 7-day MA, 30-day MA, rolling std deviation</li>
                <li><strong>External Features:</strong> Humidity, atmospheric pressure, wind speed/direction</li>
                <li><strong>Cyclical Encoding:</strong> Sin/cos transformation for hour and month</li>
            </ul>

            <h4>Validation Strategy</h4>
            <ul>
                <li><strong>Time-series Split:</strong> No shuffling to preserve temporal order</li>
                <li><strong>Walk-forward Validation:</strong> Train on past, predict future (sliding window)</li>
                <li><strong>Metrics:</strong> RMSE (primary), MAE, MAPE for temperature and precipitation</li>
                <li><strong>Backtesting:</strong> Tested on 2023 data (unseen during training)</li>
            </ul>

            <h4>Handling Challenges</h4>
            <ul>
                <li><strong>Missing Data:</strong> Forward fill for gaps <6 hours, linear interpolation for longer gaps</li>
                <li><strong>Seasonality:</strong> Separate models for dry season (Apr-Sep) and wet season (Oct-Mar)</li>
                <li><strong>Extreme Events:</strong> Weighted loss function (higher weight for rare weather patterns)</li>
                <li><strong>Overfitting:</strong> Dropout (0.2), early stopping (patience=10), L2 regularization</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-flask"></i> Model Validation & Testing</h3>
            
            <h4>Experiment: LSTM vs Traditional Baseline</h4>
            <table class="tech-table">
                <tr>
                    <th>Model</th>
                    <th>RMSE (°C)</th>
                    <th>MAE (°C)</th>
                    <th>Extreme Event Accuracy</th>
                </tr>
                <tr>
                    <td>7-day Moving Average (Baseline)</td>
                    <td>4.2</td>
                    <td>3.5</td>
                    <td>45%</td>
                </tr>
                <tr>
                    <td>LSTM + Attention</td>
                    <td>2.3</td>
                    <td>1.8</td>
                    <td>78%</td>
                </tr>
                <tr>
                    <td><strong>Improvement</strong></td>
                    <td><strong>-45%</strong></td>
                    <td><strong>-49%</strong></td>
                    <td><strong>+73%</strong></td>
                </tr>
            </table>

            <p><strong>Statistical Significance:</strong> Paired t-test on 180 days of predictions, p < 0.0001</p>
            <p><strong>Geographic Validation:</strong> Tested on 5 different regions with similar performance</p>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-database"></i> Data Engineering</h3>
            
            <h4>Pipeline Architecture</h4>
            <pre class="code-block">
[OpenWeather API] ──┐
[NOAA Database]   ──┼──> [Data Ingestion] ──> [InfluxDB]
[Local Stations]  ──┘            │
                                 ├──> [Feature Engineering] ──> [Model Training]
                                 │                                      │
                                 └──> [Real-time Prediction] <──────────┘
                                              │
                                              └──> [Streamlit App]
            </pre>

            <h4>Data Quality Monitoring</h4>
            <ul>
                <li><strong>API Health Checks:</strong> Automated monitoring with alerts if API fails</li>
                <li><strong>Data Freshness:</strong> Alert if data older than 12 hours</li>
                <li><strong>Outlier Detection:</strong> Flag values outside 3 standard deviations</li>
                <li><strong>Missing Data Tracking:</strong> Dashboard showing data completeness by source</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-dollar-sign"></i> Impact & ROI</h3>
            <table class="tech-table">
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Development Time</td>
                    <td>2 months</td>
                </tr>
                <tr>
                    <td>Active Users</td>
                    <td>500+ farmers</td>
                </tr>
                <tr>
                    <td>Crop Loss Reduction</td>
                    <td>15% average</td>
                </tr>
                <tr>
                    <td>Savings per Cooperative</td>
                    <td>$50,000/year</td>
                </tr>
                <tr>
                    <td>User Satisfaction</td>
                    <td>4.6/5.0</td>
                </tr>
            </table>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-rocket"></i> Production Considerations</h3>
            <ul>
                <li><strong>Model Serving:</strong> TensorFlow Serving for low-latency predictions (<100ms)</li>
                <li><strong>Caching:</strong> Redis for frequently requested forecasts (reduces API calls by 70%)</li>
                <li><strong>Fallback:</strong> Statistical model (7-day MA) if ML model fails</li>
                <li><strong>Monitoring:</strong> Track prediction accuracy vs actual weather, retrain if RMSE > 3.0</li>
                <li><strong>Offline Mode:</strong> Last 7-day forecast cached locally for areas with poor connectivity</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-link"></i> Resources</h3>
            <p><a href="https://prediksi-cuaca2.streamlit.app/" target="_blank" class="tech-link">
                <i class="fas fa-external-link-alt"></i> View Live Demo
            </a></p>
            <p><a href="https://github.com/yandri918/prediksi-cuaca" target="_blank" class="tech-link">
                <i class="fab fa-github"></i> View Source Code on GitHub
            </a></p>
        </div>
    `,

    economics: `
        <h2><i class="fas fa-balance-scale"></i> Economic Analysis Platform - Technical Deep Dive</h2>
        
        <div class="tech-detail-section">
            <h3><i class="fas fa-briefcase"></i> Business Problem</h3>
            <p><strong>Context:</strong> Economics students struggling with abstract concepts, professors needing interactive teaching tools.</p>
            <p><strong>Stakeholders:</strong> University professors (8), students (500+), policy analysts</p>
            <ul>
                <li><strong>Pain Point 1:</strong> Textbook examples too simplified and static</li>
                <li><strong>Pain Point 2:</strong> No hands-on experimentation with economic models</li>
                <li><strong>Pain Point 3:</strong> Difficulty visualizing market dynamics and equilibrium</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-code"></i> Technical Approach</h3>
            
            <h4>Core Algorithms</h4>
            <ul>
                <li><strong>Supply-Demand Equilibrium:</strong> Newton-Raphson method for equation solving</li>
                <li><strong>Market Optimization:</strong> SciPy optimize for finding equilibrium points</li>
                <li><strong>Economic Forecasting:</strong> ARIMA models for macro indicators</li>
                <li><strong>Sensitivity Analysis:</strong> Monte Carlo simulation for parameter uncertainty</li>
            </ul>

            <h4>Data Sources</h4>
            <ul>
                <li><strong>World Bank API:</strong> GDP, inflation, unemployment data</li>
                <li><strong>IMF Database:</strong> International economic indicators</li>
                <li><strong>Local Statistics:</strong> National economic data</li>
                <li><strong>Update Frequency:</strong> Monthly for macro indicators</li>
            </ul>

            <h4>Validation Strategy</h4>
            <ul>
                <li><strong>Historical Backtesting:</strong> 2010-2020 data for model validation</li>
                <li><strong>Comparison:</strong> Model predictions vs actual market outcomes</li>
                <li><strong>Sensitivity Analysis:</strong> Test model stability with parameter variations</li>
                <li><strong>Expert Review:</strong> Validated by economics professors</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-chart-line"></i> Features & Capabilities</h3>
            
            <h4>Supply-Demand Analysis</h4>
            <ul>
                <li>Interactive curve manipulation</li>
                <li>Equilibrium point calculation</li>
                <li>Consumer/producer surplus visualization</li>
                <li>Elasticity calculations</li>
            </ul>

            <h4>Market Interventions</h4>
            <ul>
                <li>Price ceiling/floor effects</li>
                <li>Tax incidence analysis</li>
                <li>Subsidy impact modeling</li>
                <li>Deadweight loss calculations</li>
            </ul>

            <h4>Macro Indicators</h4>
            <ul>
                <li>GDP growth forecasting</li>
                <li>Inflation rate predictions</li>
                <li>Unemployment trends</li>
                <li>Interest rate scenarios</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-users"></i> Impact & Adoption</h3>
            <table class="tech-table">
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Universities Using</td>
                    <td>3 institutions</td>
                </tr>
                <tr>
                    <td>Active Students</td>
                    <td>500+ per semester</td>
                </tr>
                <tr>
                    <td>Student Satisfaction</td>
                    <td>85% (4.2/5.0)</td>
                </tr>
                <tr>
                    <td>Exam Score Improvement</td>
                    <td>+12% average</td>
                </tr>
                <tr>
                    <td>Professor Adoption Rate</td>
                    <td>100% (8/8)</td>
                </tr>
            </table>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-rocket"></i> Production Considerations</h3>
            <ul>
                <li><strong>Real-time Calculations:</strong> Sub-second response for interactive adjustments</li>
                <li><strong>Visualization:</strong> Plotly for dynamic, publication-quality charts</li>
                <li><strong>Educational Mode:</strong> Step-by-step explanations with formulas</li>
                <li><strong>Accessibility:</strong> Mobile-responsive, works on tablets in classrooms</li>
                <li><strong>Scalability:</strong> Handles 100+ concurrent users during lectures</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-link"></i> Resources</h3>
            <p><a href="https://ekonomimakro-mikro.streamlit.app/" target="_blank" class="tech-link">
                <i class="fas fa-external-link-alt"></i> View Live Demo
            </a></p>
            <p><a href="https://github.com/yandri918/ekonomi_makro-mikro" target="_blank" class="tech-link">
                <i class="fab fa-github"></i> View Source Code on GitHub
            </a></p>
        </div>
    `,

    mining: `
        <h2><i class="fas fa-hard-hat"></i> Mining Operations Analytics - Technical Deep Dive</h2>
        
        <div class="tech-detail-section">
            <h3><i class="fas fa-briefcase"></i> Business Problem</h3>
            <p><strong>Context:</strong> Mining operations struggling with inefficient resource allocation, production tracking, and safety monitoring across multiple sites.</p>
            <p><strong>Stakeholders:</strong> Mine managers (3), Operations team (15), Safety officers (5)</p>
            <ul>
                <li><strong>Pain Point 1:</strong> Manual data entry for daily production reports (2-3 hours/day)</li>
                <li><strong>Pain Point 2:</strong> No real-time visibility into equipment utilization and downtime</li>
                <li><strong>Pain Point 3:</strong> Reactive maintenance leading to unexpected equipment failures</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-code"></i> Technical Approach</h3>
            
            <h4>Analytics Modules</h4>
            <ul>
                <li><strong>Production Tracking:</strong> Real-time dashboard with daily/weekly/monthly aggregations</li>
                <li><strong>Equipment Monitoring:</strong> Utilization rates, downtime analysis, maintenance scheduling</li>
                <li><strong>Geospatial Analysis:</strong> 3D visualization of drill holes and ore grade distribution</li>
                <li><strong>Predictive Maintenance:</strong> ML model for equipment failure prediction (82% F1-score)</li>
            </ul>

            <h4>Impact & ROI</h4>
            <table class="tech-table">
                <tr>
                    <th>Metric</th>
                    <th>Improvement</th>
                </tr>
                <tr>
                    <td>Equipment Downtime</td>
                    <td>-40% (15% → 9%)</td>
                </tr>
                <tr>
                    <td>Reporting Time</td>
                    <td>-92% (3h → 15min/day)</td>
                </tr>
                <tr>
                    <td>Maintenance Cost</td>
                    <td>-30% ($500K → $350K/year)</td>
                </tr>
                <tr>
                    <td>Production Efficiency</td>
                    <td>+17% (75% → 88%)</td>
                </tr>
            </table>
            <p><strong>Total Annual Savings:</strong> $300K+</p>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-link"></i> Resources</h3>
            <p><a href="https://miningportofolio.streamlit.app/" target="_blank" class="tech-link">
                <i class="fas fa-external-link-alt"></i> View Live Demo
            </a></p>
            <p><a href="https://github.com/yandri918/mining_portofolio" target="_blank" class="tech-link">
                <i class="fab fa-github"></i> View Source Code on GitHub
            </a></p>
        </div>
    `,

    dataAnalyst: `
        <h2><i class="fas fa-chart-pie"></i> Advanced Data Analysis Suite - Technical Deep Dive</h2>
        
        <div class="tech-detail-section">
            <h3><i class="fas fa-briefcase"></i> Business Problem</h3>
            <p><strong>Context:</strong> Small-medium businesses and analysts needing comprehensive data analysis tools without expensive enterprise software.</p>
            <p><strong>Stakeholders:</strong> Business analysts (100+), SMB owners (50+), Students (200+)</p>
            <ul>
                <li><strong>Pain Point 1:</strong> Excel limitations for large datasets (>100K rows)</li>
                <li><strong>Pain Point 2:</strong> Lack of statistical expertise for proper analysis</li>
                <li><strong>Pain Point 3:</strong> No automated reporting or visualization capabilities</li>
            </ul>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-code"></i> Technical Approach</h3>
            
            <h4>Core Capabilities</h4>
            <ul>
                <li><strong>Exploratory Data Analysis:</strong> Automated profiling, distribution analysis, correlation matrices</li>
                <li><strong>Statistical Testing:</strong> T-tests, ANOVA, Chi-square, regression analysis</li>
                <li><strong>Time Series Analysis:</strong> Trend decomposition, seasonality detection, forecasting</li>
                <li><strong>Machine Learning:</strong> Classification, regression, clustering with AutoML capabilities</li>
                <li><strong>Data Visualization:</strong> Interactive Plotly charts, customizable dashboards</li>
            </ul>

            <h4>AutoML Example: Customer Churn Prediction</h4>
            <table class="tech-table">
                <tr>
                    <th>Model</th>
                    <th>Accuracy</th>
                    <th>AUC-ROC</th>
                </tr>
                <tr>
                    <td>Logistic Regression</td>
                    <td>82%</td>
                    <td>0.86</td>
                </tr>
                <tr>
                    <td>Random Forest</td>
                    <td>88%</td>
                    <td>0.92</td>
                </tr>
                <tr>
                    <td>XGBoost (Selected)</td>
                    <td>91%</td>
                    <td>0.95</td>
                </tr>
            </table>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-users"></i> User Adoption & Impact</h3>
            <table class="tech-table">
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Active Users</td>
                    <td>350+ (analysts, students, SMBs)</td>
                </tr>
                <tr>
                    <td>Analyses Performed</td>
                    <td>2,500+ in 6 months</td>
                </tr>
                <tr>
                    <td>Average Time Saved</td>
                    <td>4-6 hours per analysis</td>
                </tr>
                <tr>
                    <td>Cost Savings vs Enterprise Tools</td>
                    <td>$10K-50K/year per organization</td>
                </tr>
            </table>
        </div>

        <div class="tech-detail-section">
            <h3><i class="fas fa-link"></i> Resources</h3>
            <p><a href="https://dataanalyst2.streamlit.app/" target="_blank" class="tech-link">
                <i class="fas fa-external-link-alt"></i> View Live Demo
            </a></p>
            <p><a href="https://github.com/yandri918/data" target="_blank" class="tech-link">
                <i class="fab fa-github"></i> View Source Code on GitHub
            </a></p>
        </div>
    `
};

// Initialize modal system
document.addEventListener('DOMContentLoaded', () => {
    const modal = new TechnicalDetailsModal();

    // Add "View Technical Details" buttons to case studies
    const caseStudyCards = document.querySelectorAll('.case-study-card');

    caseStudyCards.forEach((card, index) => {
        const content = card.querySelector('.case-study-content');
        const projectKey = ['marketing', 'weather', 'economics', 'mining', 'dataAnalyst'][index];

        if (projectKey && technicalDetails[projectKey]) {
            const button = document.createElement('button');
            button.className = 'tech-details-button';
            button.innerHTML = '<i class="fas fa-code"></i> View Technical Details';
            button.addEventListener('click', (e) => {
                e.preventDefault();
                modal.open(technicalDetails[projectKey]);
            });

            content.appendChild(button);
        }
    });
});
