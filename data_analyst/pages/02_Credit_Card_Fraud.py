"""
Credit Card Fraud Detection Analysis
Comprehensive analysis of credit card fraud patterns with ML insights
"""
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.data_loader import load_credit_card_data, preprocess_fraud_data
from utils.chart_builder import (create_bar_chart, create_histogram, 
                                  create_scatter_plot, create_boxplot,
                                  COLOR_SCHEME)
from utils.metrics import calculate_fraud_metrics, calculate_correlation_matrix

# Page configuration
st.set_page_config(
    page_title="Credit Card Fraud Detection",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .fraud-metric {
        background: linear-gradient(135deg, #f56565 0%, #c53030 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .legit-metric {
        background: linear-gradient(135deg, #48bb78 0%, #2f855a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .warning-box {
        background: #fff5f5;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #f56565;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #ebf8ff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #4299e1;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔍 Credit Card Fraud Detection Analysis")
st.markdown("**Analisis pola fraud pada transaksi kartu kredit menggunakan teknik Machine Learning**")

# Load and preprocess data
with st.spinner("Loading credit card data..."):
    # Load sample data for performance
    sample_size = st.sidebar.slider("Sample Size", 10000, 100000, 50000, 10000)
    df = load_credit_card_data(sample_size=sample_size)

if df is not None:
    df = preprocess_fraud_data(df)
    
    # Sidebar info
    st.sidebar.markdown("### 📊 Dataset Information")
    st.sidebar.markdown(f"**Total Transactions:** {len(df):,}")
    st.sidebar.markdown(f"**Features:** {len(df.columns)}")
    st.sidebar.markdown(f"**Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **Note:** Dataset contains PCA-transformed features (V1-V28) 
    to protect sensitive information.
    """)
    
    # Calculate metrics
    metrics = calculate_fraud_metrics(df)
    
    # Key Metrics Dashboard
    st.markdown("## 📊 Fraud Detection Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="fraud-metric">
            <div class="metric-label">Fraudulent Transactions</div>
            <div class="metric-value">{metrics['fraud_count']:,}</div>
            <div class="metric-label">{metrics['fraud_percentage']:.3f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="legit-metric">
            <div class="metric-label">Legitimate Transactions</div>
            <div class="metric-value">{metrics['legitimate_count']:,}</div>
            <div class="metric-label">{100 - metrics['fraud_percentage']:.3f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="fraud-metric">
            <div class="metric-label">Avg Fraud Amount</div>
            <div class="metric-value">${metrics['avg_fraud_amount']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="legit-metric">
            <div class="metric-label">Avg Legit Amount</div>
            <div class="metric-value">${metrics['avg_legitimate_amount']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Class imbalance warning
    st.markdown(f"""
    <div class="warning-box">
        <strong>⚠️ Class Imbalance Detected:</strong> 
        The dataset is highly imbalanced with a ratio of {metrics['class_imbalance_ratio']:.0f}:1 
        (legitimate to fraud). This is typical in fraud detection scenarios and requires 
        special handling techniques like SMOTE, class weighting, or anomaly detection.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main visualizations
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Distribution Analysis",
        "💰 Amount Analysis",
        "⏰ Time Patterns",
        "🔗 Feature Correlation",
        "📈 PCA Visualization",
        "🤖 ML Model"
    ])
    
    with tab1:
        st.markdown("### Class Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Class distribution bar chart
            class_dist = df['Class'].value_counts().reset_index()
            class_dist.columns = ['Class', 'Count']
            class_dist['Class'] = class_dist['Class'].map({0: 'Legitimate', 1: 'Fraud'})
            
            class_chart = alt.Chart(class_dist).mark_bar().encode(
                x=alt.X('Class:N', title='Transaction Type'),
                y=alt.Y('Count:Q', title='Number of Transactions'),
                color=alt.Color('Class:N', 
                              scale=alt.Scale(domain=['Legitimate', 'Fraud'],
                                            range=[COLOR_SCHEME['success'], COLOR_SCHEME['danger']]),
                              legend=None),
                tooltip=['Class', 'Count']
            ).properties(
                width=400,
                height=400,
                title='Transaction Class Distribution'
            )
            
            st.altair_chart(class_chart, use_container_width=True)
        
        with col2:
            # Pie chart representation
            st.markdown("#### Percentage Breakdown")
            
            fraud_pct = metrics['fraud_percentage']
            legit_pct = 100 - fraud_pct
            
            st.markdown(f"""
            **Legitimate Transactions:** {legit_pct:.3f}%  
            **Fraudulent Transactions:** {fraud_pct:.3f}%
            
            ---
            
            **Total Transactions:** {metrics['total_transactions']:,}  
            **Fraud Count:** {metrics['fraud_count']:,}  
            **Legitimate Count:** {metrics['legitimate_count']:,}
            """)
            
            st.markdown(f"""
            <div class="info-box">
                <strong>💡 Insight:</strong> 
                Only {fraud_pct:.3f}% of transactions are fraudulent, 
                making this a highly imbalanced classification problem. 
                Traditional accuracy metrics would be misleading here.
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Transaction Amount Analysis")
        
        # Amount distribution by class
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Fraud Transactions Amount")
            fraud_data = df[df['Class'] == 1]
            
            if len(fraud_data) > 0:
                fraud_hist = create_histogram(
                    fraud_data,
                    column='Amount',
                    bins=30,
                    title="Distribution of Fraud Transaction Amounts",
                    width=450,
                    height=350
                )
                st.altair_chart(fraud_hist, use_container_width=True)
                
                st.metric("Max Fraud Amount", f"${metrics['max_fraud_amount']:.2f}")
        
        with col2:
            st.markdown("#### Legitimate Transactions Amount")
            legit_data = df[df['Class'] == 0].sample(min(5000, len(df[df['Class'] == 0])))
            
            legit_hist = create_histogram(
                legit_data,
                column='Amount',
                bins=30,
                title="Distribution of Legitimate Transaction Amounts (Sample)",
                width=450,
                height=350
            )
            st.altair_chart(legit_hist, use_container_width=True)
        
        # Box plot comparison
        st.markdown("#### Amount Comparison by Class")
        
        # Sample data for better visualization
        sample_df = pd.concat([
            df[df['Class'] == 1],  # All fraud
            df[df['Class'] == 0].sample(min(5000, len(df[df['Class'] == 0])))  # Sample legitimate
        ])
        sample_df['Class_Label'] = sample_df['Class'].map({0: 'Legitimate', 1: 'Fraud'})
        
        box_chart = create_boxplot(
            sample_df,
            x='Class_Label',
            y='Amount',
            title="Transaction Amount Distribution by Class",
            width=800,
            height=400
        )
        
        st.altair_chart(box_chart, use_container_width=True)
    
    with tab3:
        st.markdown("### Time-based Patterns")
        
        # Fraud by hour
        if 'Hour' in df.columns:
            fraud_by_hour = df.groupby(['Hour', 'Class']).size().reset_index(name='Count')
            fraud_by_hour['Class_Label'] = fraud_by_hour['Class'].map({0: 'Legitimate', 1: 'Fraud'})
            
            hour_chart = alt.Chart(fraud_by_hour).mark_bar().encode(
                x=alt.X('Hour:O', title='Hour of Day'),
                y=alt.Y('Count:Q', title='Number of Transactions'),
                color=alt.Color('Class_Label:N',
                              scale=alt.Scale(domain=['Legitimate', 'Fraud'],
                                            range=[COLOR_SCHEME['success'], COLOR_SCHEME['danger']]),
                              title='Transaction Type'),
                tooltip=['Hour', 'Class_Label', 'Count']
            ).properties(
                width=800,
                height=400,
                title='Transaction Distribution by Hour of Day'
            ).interactive()
            
            st.altair_chart(hour_chart, use_container_width=True)
            
            # Fraud percentage by hour
            fraud_pct_hour = df.groupby('Hour')['Class'].agg(['sum', 'count']).reset_index()
            fraud_pct_hour['Fraud_Percentage'] = (fraud_pct_hour['sum'] / fraud_pct_hour['count'] * 100)
            
            pct_chart = alt.Chart(fraud_pct_hour).mark_line(
                point=True,
                strokeWidth=3
            ).encode(
                x=alt.X('Hour:O', title='Hour of Day'),
                y=alt.Y('Fraud_Percentage:Q', title='Fraud Percentage (%)'),
                color=alt.value(COLOR_SCHEME['danger']),
                tooltip=['Hour', 'Fraud_Percentage']
            ).properties(
                width=800,
                height=300,
                title='Fraud Percentage by Hour'
            ).interactive()
            
            st.altair_chart(pct_chart, use_container_width=True)
    
    with tab4:
        st.markdown("### Feature Correlation Analysis")
        
        # Select top features for correlation
        feature_cols = [col for col in df.columns if col.startswith('V')][:10] + ['Amount']
        
        if len(feature_cols) > 0:
            corr_matrix = calculate_correlation_matrix(df, feature_cols)
            
            # Prepare data for heatmap
            corr_data = corr_matrix.stack().reset_index()
            corr_data.columns = ['Feature1', 'Feature2', 'Correlation']
            
            heatmap = alt.Chart(corr_data).mark_rect().encode(
                x=alt.X('Feature1:O', title=''),
                y=alt.Y('Feature2:O', title=''),
                color=alt.Color('Correlation:Q',
                              scale=alt.Scale(scheme='redblue', domain=[-1, 1]),
                              title='Correlation'),
                tooltip=['Feature1', 'Feature2', alt.Tooltip('Correlation:Q', format='.3f')]
            ).properties(
                width=600,
                height=600,
                title='Feature Correlation Matrix (Top 10 Features + Amount)'
            )
            
            st.altair_chart(heatmap, use_container_width=True)
            
            st.markdown("""
            <div class="info-box">
                <strong>💡 Note:</strong> 
                Features V1-V28 are PCA-transformed components. 
                Strong correlations might indicate redundant information.
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### PCA Feature Visualization")
        
        st.markdown("""
        The dataset uses PCA (Principal Component Analysis) to protect sensitive information. 
        Let's visualize the first two principal components.
        """)
        
        # Sample for visualization
        viz_sample = pd.concat([
            df[df['Class'] == 1],  # All fraud
            df[df['Class'] == 0].sample(min(2000, len(df[df['Class'] == 0])))  # Sample legitimate
        ])
        viz_sample['Class_Label'] = viz_sample['Class'].map({0: 'Legitimate', 1: 'Fraud'})
        
        # V1 vs V2 scatter plot
        scatter = create_scatter_plot(
            viz_sample,
            x='V1',
            y='V2',
            color=alt.Color('Class_Label:N',
                          scale=alt.Scale(domain=['Legitimate', 'Fraud'],
                                        range=[COLOR_SCHEME['success'], COLOR_SCHEME['danger']]),
                          title='Transaction Type'),
            title="PCA Components V1 vs V2",
            width=800,
            height=500
        )
        
        st.altair_chart(scatter, use_container_width=True)
        
        # Feature importance visualization (based on correlation with Class)
        st.markdown("#### Feature Correlation with Fraud")
        
        feature_cols = [col for col in df.columns if col.startswith('V')]
        correlations = []
        
        for col in feature_cols[:15]:  # Top 15 features
            corr = df[col].corr(df['Class'])
            correlations.append({'Feature': col, 'Correlation': abs(corr)})
        
        corr_df = pd.DataFrame(correlations).sort_values('Correlation', ascending=False)
        
        corr_chart = alt.Chart(corr_df).mark_bar().encode(
            x=alt.X('Correlation:Q', title='Absolute Correlation with Fraud'),
            y=alt.Y('Feature:N', sort='-x', title='Feature'),
            color=alt.value(COLOR_SCHEME['primary']),
            tooltip=['Feature', alt.Tooltip('Correlation:Q', format='.4f')]
        ).properties(
            width=700,
            height=400,
            title='Top 15 Features Correlated with Fraud'
        )
        
        st.altair_chart(corr_chart, use_container_width=True)
    
    with tab6:
        st.markdown("### 🤖 Machine Learning Fraud Detection Model")
        
        st.markdown("""
        Train a Random Forest classifier to detect fraudulent transactions. 
        Adjust the parameters in the sidebar to see how they affect model performance.
        """)
        
        # Import ML utilities
        from utils.ml_models import (train_fraud_detection_model, evaluate_model,
                                    get_feature_importance, plot_confusion_matrix,
                                    plot_roc_curve, plot_feature_importance)
        
        # Sidebar parameters
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🎛️ Model Parameters")
        
        n_estimators = st.sidebar.slider("Number of Trees", 10, 500, 100, 10)
        max_depth = st.sidebar.slider("Max Depth", 5, 50, 20, 5)
        min_samples_split = st.sidebar.slider("Min Samples Split", 2, 20, 5, 1)
        use_smote = st.sidebar.checkbox("Use SMOTE (Balance Classes)", value=True)
        
        # Train button
        if st.sidebar.button("🚀 Train Model", type="primary"):
            with st.spinner("Training model... This may take a moment."):
                # Prepare features
                feature_cols = [col for col in df.columns if col.startswith('V')] + ['Amount']
                X = df[feature_cols]
                y = df['Class']
                
                # Train model
                model, scaler, X_test, y_test, training_time = train_fraud_detection_model(
                    X, y,
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    min_samples_split=min_samples_split,
                    use_smote=use_smote
                )
                
                # Store in session state
                st.session_state['fraud_model'] = model
                st.session_state['fraud_scaler'] = scaler
                st.session_state['X_test'] = X_test
                st.session_state['y_test'] = y_test
                st.session_state['feature_cols'] = feature_cols
                st.session_state['training_time'] = training_time
                
                st.success(f"✅ Model trained successfully in {training_time:.2f} seconds!")
        
        # Display results if model exists
        if 'fraud_model' in st.session_state:
            model = st.session_state['fraud_model']
            scaler = st.session_state['fraud_scaler']
            X_test = st.session_state['X_test']
            y_test = st.session_state['y_test']
            feature_cols = st.session_state['feature_cols']
            
            # Evaluate model
            metrics, y_pred, y_pred_proba = evaluate_model(model, X_test, y_test)
            
            # Metrics Dashboard
            st.markdown("#### 📊 Model Performance Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Accuracy", f"{metrics['accuracy']:.4f}")
            with col2:
                st.metric("Precision", f"{metrics['precision']:.4f}")
            with col3:
                st.metric("Recall", f"{metrics['recall']:.4f}")
            with col4:
                st.metric("F1-Score", f"{metrics['f1']:.4f}")
            
            st.metric("ROC-AUC Score", f"{metrics['roc_auc']:.4f}", 
                     help="Area Under the ROC Curve - measures model's ability to distinguish between classes")
            
            # Visualizations
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ROC Curve")
                roc_fig = plot_roc_curve(y_test, y_pred_proba)
                st.plotly_chart(roc_fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Confusion Matrix")
                cm_fig = plot_confusion_matrix(metrics['confusion_matrix'])
                st.plotly_chart(cm_fig, use_container_width=True)
            
            # Feature Importance
            st.markdown("---")
            st.markdown("#### 🎯 Feature Importance")
            
            importance_df = get_feature_importance(model, feature_cols, top_n=15)
            importance_fig = plot_feature_importance(importance_df)
            st.plotly_chart(importance_fig, use_container_width=True)
            
            st.markdown("""
            <div class="info-box">
                <strong>💡 Interpretation:</strong> 
                Features with higher importance scores have more influence on the model's predictions.
                These are the key indicators the model uses to detect fraud.
            </div>
            """, unsafe_allow_html=True)
            
            # Classification Report
            st.markdown("---")
            st.markdown("#### 📋 Detailed Classification Report")
            
            report_df = pd.DataFrame(metrics['classification_report']).transpose()
            st.dataframe(report_df.style.format("{:.4f}"), use_container_width=True)
            
            # Prediction Interface
            st.markdown("---")
            st.markdown("#### 🔮 Test Prediction")
            
            st.markdown("Enter transaction details to predict fraud probability:")
            
            with st.expander("Enter Transaction Features"):
                pred_cols = st.columns(3)
                
                # Create input fields for key features
                transaction_input = {}
                
                # Amount
                with pred_cols[0]:
                    transaction_input['Amount'] = st.number_input("Amount ($)", 
                                                                  min_value=0.0, 
                                                                  max_value=10000.0, 
                                                                  value=100.0)
                
                # V1-V28 features (show first few)
                for i, col in enumerate([f'V{j}' for j in range(1, 29)]):
                    col_idx = i % 3
                    with pred_cols[col_idx]:
                        transaction_input[col] = st.number_input(f"{col}", 
                                                                 value=0.0, 
                                                                 format="%.4f",
                                                                 key=f"input_{col}")
                
                if st.button("🔍 Predict Fraud Probability"):
                    from utils.ml_models import predict_fraud
                    
                    fraud_prob, prediction = predict_fraud(model, scaler, transaction_input)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if prediction == 1:
                            st.markdown(f"""
                            <div class="fraud-metric">
                                <div class="metric-label">Prediction</div>
                                <div class="metric-value">⚠️ FRAUD</div>
                                <div class="metric-label">Probability: {fraud_prob:.2%}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="legit-metric">
                                <div class="metric-label">Prediction</div>
                                <div class="metric-value">✅ LEGITIMATE</div>
                                <div class="metric-label">Fraud Probability: {fraud_prob:.2%}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col2:
                        # Probability gauge
                        st.markdown(f"""
                        **Fraud Probability:** {fraud_prob:.2%}
                        
                        **Confidence:** {"High" if abs(fraud_prob - 0.5) > 0.3 else "Medium" if abs(fraud_prob - 0.5) > 0.1 else "Low"}
                        
                        **Recommendation:** {"Block transaction and investigate" if fraud_prob > 0.7 else "Flag for review" if fraud_prob > 0.3 else "Approve transaction"}
                        """)
        
        else:
            st.info("👆 Click 'Train Model' in the sidebar to start training the fraud detection model.")
            
            st.markdown("""
            <div class="info-box">
                <strong>ℹ️ About the Model:</strong><br>
                This Random Forest classifier uses ensemble learning to detect fraudulent transactions.
                
                <br><br><strong>Key Features:</strong>
                <ul>
                    <li><strong>SMOTE:</strong> Handles class imbalance by oversampling minority class</li>
                    <li><strong>Random Forest:</strong> Ensemble of decision trees for robust predictions</li>
                    <li><strong>Feature Scaling:</strong> Standardizes features for better performance</li>
                    <li><strong>Cross-validation:</strong> Ensures model generalizes well</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Data preview
    st.markdown("---")
    st.markdown("### 📋 Data Preview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Fraudulent Transactions Sample")
        fraud_sample = df[df['Class'] == 1].head(10)
        st.dataframe(fraud_sample[['Time', 'Amount', 'Class']], use_container_width=True)
    
    with col2:
        st.markdown("#### Legitimate Transactions Sample")
        legit_sample = df[df['Class'] == 0].head(10)
        st.dataframe(legit_sample[['Time', 'Amount', 'Class']], use_container_width=True)

else:
    st.error("❌ Failed to load credit card data. Please check the data file.")
    st.info("💡 Make sure 'creditcard.csv' is in the data folder or parent directory.")
