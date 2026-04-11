"""
Machine Learning models for fraud detection
"""
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (classification_report, confusion_matrix, 
                             roc_auc_score, roc_curve, accuracy_score,
                             precision_score, recall_score, f1_score)
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import plotly.graph_objects as go
import plotly.figure_factory as ff

@st.cache_resource
def train_fraud_detection_model(X, y, n_estimators=100, max_depth=20, 
                                min_samples_split=5, use_smote=True, 
                                class_weight='balanced'):
    """
    Train Random Forest classifier for fraud detection
    
    Args:
        X: Features dataframe
        y: Target variable
        n_estimators: Number of trees
        max_depth: Maximum depth of trees
        min_samples_split: Minimum samples to split node
        use_smote: Whether to apply SMOTE for class balancing
        class_weight: Class weight strategy
    
    Returns:
        model, scaler, X_test, y_test, training_time
    """
    import time
    start_time = time.time()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Apply SMOTE if requested
    if use_smote:
        smote = SMOTE(random_state=42)
        X_train_scaled, y_train = smote.fit_resample(X_train_scaled, y_train)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        class_weight=class_weight if not use_smote else None,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    training_time = time.time() - start_time
    
    return model, scaler, X_test_scaled, y_test, training_time

def evaluate_model(model, X_test, y_test):
    """
    Evaluate model performance
    
    Returns:
        Dictionary with all metrics
    """
    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba),
        'confusion_matrix': confusion_matrix(y_test, y_pred),
        'classification_report': classification_report(y_test, y_pred, output_dict=True)
    }
    
    return metrics, y_pred, y_pred_proba

def get_feature_importance(model, feature_names, top_n=15):
    """
    Get feature importance scores
    
    Returns:
        DataFrame with feature importance
    """
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).head(top_n)
    
    return importance_df

def plot_confusion_matrix(cm, labels=['Legitimate', 'Fraud']):
    """
    Create interactive confusion matrix heatmap
    """
    # Normalize confusion matrix
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    # Create annotations
    annotations = []
    for i in range(len(labels)):
        for j in range(len(labels)):
            annotations.append({
                'x': labels[j],
                'y': labels[i],
                'text': f'{cm[i, j]}<br>({cm_normalized[i, j]:.1%})',
                'showarrow': False,
                'font': {'size': 14, 'color': 'white' if cm_normalized[i, j] > 0.5 else 'black'}
            })
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=cm_normalized,
        x=labels,
        y=labels,
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title='Proportion')
    ))
    
    fig.update_layout(
        title='Confusion Matrix',
        xaxis_title='Predicted',
        yaxis_title='Actual',
        annotations=annotations,
        width=500,
        height=500
    )
    
    return fig

def plot_roc_curve(y_test, y_pred_proba):
    """
    Create ROC curve plot
    """
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    fig = go.Figure()
    
    # ROC curve
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode='lines',
        name=f'ROC Curve (AUC = {auc:.3f})',
        line=dict(color='#667eea', width=3)
    ))
    
    # Diagonal line
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        name='Random Classifier',
        line=dict(color='gray', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f'ROC Curve (AUC = {auc:.3f})',
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        width=700,
        height=500,
        showlegend=True
    )
    
    return fig

def plot_feature_importance(importance_df):
    """
    Create feature importance bar chart
    """
    fig = go.Figure(data=[
        go.Bar(
            x=importance_df['Importance'],
            y=importance_df['Feature'],
            orientation='h',
            marker=dict(
                color=importance_df['Importance'],
                colorscale='Viridis',
                showscale=True
            )
        )
    ])
    
    fig.update_layout(
        title='Top Feature Importance',
        xaxis_title='Importance Score',
        yaxis_title='Feature',
        height=500,
        width=700,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def predict_fraud(model, scaler, transaction_data):
    """
    Predict fraud probability for new transaction
    
    Args:
        model: Trained model
        scaler: Fitted scaler
        transaction_data: Dictionary or DataFrame with transaction features
    
    Returns:
        fraud_probability, prediction
    """
    # Convert to DataFrame if dict
    if isinstance(transaction_data, dict):
        transaction_data = pd.DataFrame([transaction_data])
    
    # Scale features
    transaction_scaled = scaler.transform(transaction_data)
    
    # Predict
    prediction = model.predict(transaction_scaled)[0]
    fraud_probability = model.predict_proba(transaction_scaled)[0, 1]
    
    return fraud_probability, prediction
