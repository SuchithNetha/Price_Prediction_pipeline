"""
Streamlit Web App for House Price Prediction using MLflow
"""
import streamlit as st
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import os
import pickle

# Page config
st.set_page_config(
    page_title="🏠 House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Title
st.title("🏠 House Price Predictor")
st.markdown("Predict house prices using Machine Learning with MLflow")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This app predicts house prices using a trained Linear Regression model.
    
    **Model:** Linear Regression  
    **Framework:** Scikit-learn  
    **MLOps:** ZenML + MLflow
    **Model Tracking:** MLflow
    """)

# Initialize MLflow (Used primarily for historical context; local model.pkl is prioritized)
mlflow.set_tracking_uri("./mlruns") 

# Input form
st.header("📝 Enter House Details")

col1, col2 = st.columns(2)

with col1:
    lot_area = st.number_input("Lot Area (sq ft)", min_value=0, value=9600)
    gr_liv_area = st.number_input("Above Grade Living Area (sq ft)", min_value=0, value=1710)
    overall_qual = st.slider("Overall Quality (1-10)", 1, 10, 5)
    overall_cond = st.slider("Overall Condition (1-10)", 1, 10, 7)
    year_built = st.number_input("Year Built", min_value=1800, max_value=2024, value=1961)
    total_bsmt_sf = st.number_input("Total Basement Area (sq ft)", min_value=0, value=850)
    first_flr_sf = st.number_input("1st Floor Area (sq ft)", min_value=0, value=856)
    second_flr_sf = st.number_input("2nd Floor Area (sq ft)", min_value=0, value=854)

with col2:
    full_bath = st.number_input("Full Bathrooms", min_value=0, value=1)
    half_bath = st.number_input("Half Bathrooms", min_value=0, value=0)
    bedrooms = st.number_input("Bedrooms Above Grade", min_value=0, value=3)
    tot_rms_abv_grd = st.number_input("Total Rooms Above Grade", min_value=0, value=7)
    fireplaces = st.number_input("Fireplaces", min_value=0, value=2)
    garage_cars = st.number_input("Garage Cars", min_value=0, value=2)
    garage_area = st.number_input("Garage Area (sq ft)", min_value=0, value=500)
    year_remod = st.number_input("Year Remodeled", min_value=1800, max_value=2024, value=1961)

# Additional features
st.subheader("Additional Features")
col3, col4 = st.columns(2)

with col3:
    lot_frontage = st.number_input("Lot Frontage (ft)", min_value=0, value=80)
    mas_vnr_area = st.number_input("Masonry Veneer Area (sq ft)", min_value=0, value=0)
    bsmtfin_sf_1 = st.number_input("Basement Finished Area 1 (sq ft)", min_value=0, value=700)
    bsmtfin_sf_2 = st.number_input("Basement Finished Area 2 (sq ft)", min_value=0, value=0)

with col4:
    bsmt_unf_sf = st.number_input("Basement Unfinished Area (sq ft)", min_value=0, value=150)
    wood_deck_sf = st.number_input("Wood Deck Area (sq ft)", min_value=0, value=210)
    open_porch_sf = st.number_input("Open Porch Area (sq ft)", min_value=0, value=0)
    mo_sold = st.number_input("Month Sold", min_value=1, max_value=12, value=5)
    yr_sold = st.number_input("Year Sold", min_value=2000, max_value=2024, value=2010)

# Load model function
@st.cache_resource
def load_mlflow_model():
    """Load MLflow model with multiple fallback options"""
    # Using the local model.pkl file is the most robust method for hosted deployment
    run_id = "173084b4925743889a1348fd990f7dc5" 
    
    model_paths = [
        "model.pkl",                             # 1. LOCAL PICKLE FILE (Prioritized)
        f"runs:/{run_id}/model",                 # 2. MLflow runs URI (Fallback)
        f"mlruns/0/{run_id}/artifacts/model",    # 3. Local MLflow path (Fallback)
    ]
    
    for model_path in model_paths:
        try:
            if model_path.endswith('.pkl'):
                # Load from pickle
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                st.sidebar.success("✅ Model loaded from pickle file")
                return model
            else:
                # Load from MLflow (Only works if the tracking URI is accessible)
                model = mlflow.sklearn.load_model(model_path)
                st.sidebar.success(f"✅ Model loaded from MLflow: {model_path}")
                return model
        except Exception as e:
            continue
    
    return None

# --- START OF CORRECTED PREDICTION LOGIC (Ensures all features are present) ---

# Categorical Defaults (to satisfy the ColumnTransformer during inference)
categorical_defaults = {
    'MS Zoning': 'RL', 'Street': 'Pave', 'Alley': 'NA', 'Lot Shape': 'Reg', 
    'Land Contour': 'Lvl', 'Utilities': 'AllPub', 'Lot Config': 'Inside', 
    'Land Slope': 'Gtl', 'Neighborhood': 'NAmes', 'Condition 1': 'Norm', 
    'Condition 2': 'Norm', 'Bldg Type': '1Fam', 'House Style': '1Story', 
    'Roof Style': 'Gable', 'Roof Matl': 'CompShg', 'Exterior 1st': 'VinylSd', 
    'Exterior 2nd': 'VinylSd', 'Mas Vnr Type': 'None', 'Exter Qual': 'TA', 
    'Exter Cond': 'TA', 'Foundation': 'PConc', 'Bsmt Qual': 'TA', 
    'Bsmt Cond': 'TA', 'Bsmt Exposure': 'No', 'BsmtFin Type 1': 'GLQ', 
    'BsmtFin Type 2': 'Unf', 'Heating': 'GasA', 'Heating QC': 'Ex', 
    'Central Air': 'Y', 'Electrical': 'SBrkr', 'Kitchen Qual': 'TA', 
    'Functional': 'Typ', 'Fireplace Qu': 'NA', 'Garage Type': 'Attchd', 
    'Garage Finish': 'Unf', 'Garage Qual': 'TA', 'Garage Cond': 'TA', 
    'Paved Drive': 'Y', 'Pool QC': 'NA', 'Fence': 'NA', 'Misc Feature': 'NA', 
    'Sale Type': 'WD', 'Sale Condition': 'Normal',
}

# The complete list of columns the model expects, in the correct order.
expected_columns = [
    'Order', 'PID', 'MS SubClass', 'Lot Frontage', 'Lot Area', 'Overall Qual', 'Overall Cond', 
    'Year Built', 'Year Remod/Add', 'Mas Vnr Area', 'BsmtFin SF 1', 'BsmtFin SF 2', 
    'Bsmt Unf SF', 'Total Bsmt SF', '1st Flr SF', '2nd Flr SF', 'Low Qual Fin SF', 
    'Gr Liv Area', 'Bsmt Full Bath', 'Bsmt Half Bath', 'Full Bath', 'Half Bath', 
    'Bedroom AbvGr', 'Kitchen AbvGr', 'TotRms AbvGrd', 'Fireplaces', 'Garage Yr Blt', 
    'Garage Cars', 'Garage Area', 'Wood Deck SF', 'Open Porch SF', 'Enclosed Porch', 
    '3Ssn Porch', 'Screen Porch', 'Pool Area', 'Misc Val', 'Mo Sold', 'Yr Sold',
    'MS Zoning', 'Street', 'Alley', 'Lot Shape', 'Land Contour', 'Utilities', 'Lot Config', 
    'Land Slope', 'Neighborhood', 'Condition 1', 'Condition 2', 'Bldg Type', 'House Style', 
    'Roof Style', 'Roof Matl', 'Exterior 1st', 'Exterior 2nd', 'Mas Vnr Type', 'Exter Qual', 
    'Exter Cond', 'Foundation', 'Bsmt Qual', 'Bsmt Cond', 'Bsmt Exposure', 'BsmtFin Type 1', 
    'BsmtFin Type 2', 'Heating', 'Heating QC', 'Central Air', 'Electrical', 'Kitchen Qual', 
    'Functional', 'Fireplace Qu', 'Garage Type', 'Garage Finish', 'Garage Qual', 'Garage Cond', 
    'Paved Drive', 'Pool QC', 'Fence', 'Misc Feature', 'Sale Type', 'Sale Condition'
]

if st.button("🔮 Predict Price", type="primary"):
    try:
        # 1. Gather all inputs
        numerical_inputs = {
            "Order": 1, "PID": 5286, "MS SubClass": 20, "Low Qual Fin SF": 0, 
            "Bsmt Full Bath": 0, "Bsmt Half Bath": 0, "Kitchen AbvGr": 1, 
            "Enclosed Porch": 0, "3Ssn Porch": 0, "Screen Porch": 0, 
            "Pool Area": 0, "Misc Val": 0, "Lot Frontage": float(lot_frontage),
            "Lot Area": int(lot_area), "Overall Qual": int(overall_qual),
            "Overall Cond": int(overall_cond), "Year Built": int(year_built),
            "Year Remod/Add": int(year_remod), "Mas Vnr Area": float(mas_vnr_area),
            "BsmtFin SF 1": float(bsmtfin_sf_1), "BsmtFin SF 2": float(bsmtfin_sf_2),
            "Bsmt Unf SF": float(bsmt_unf_sf), "Total Bsmt SF": float(total_bsmt_sf),
            "1st Flr SF": int(first_flr_sf), "2nd Flr SF": int(second_flr_sf),
            "Gr Liv Area": float(gr_liv_area), "Full Bath": int(full_bath),
            "Half Bath": int(half_bath), "Bedroom AbvGr": int(bedrooms),
            "TotRms AbvGrd": int(tot_rms_abv_grd), "Fireplaces": int(fireplaces),
            "Garage Yr Blt": int(year_built), "Garage Cars": int(garage_cars),
            "Garage Area": float(garage_area), "Wood Deck SF": float(wood_deck_sf),
            "Open Porch SF": float(open_porch_sf), "Mo Sold": int(mo_sold),
            "Yr Sold": int(yr_sold),
        }

        # 2. Combine all data and create DataFrame
        final_input_data = {**numerical_inputs, **categorical_defaults}
        df = pd.DataFrame([final_input_data], columns=expected_columns)
        
        # Load model
        model = load_mlflow_model()
        
        if model is None:
            st.error("❌ Model not found. Deployment artifact 'model.pkl' is missing.")
        else:
            # 3. Make prediction (Output is a log-transformed value)
            prediction_log = model.predict(df)
            
            # 4. Apply Inverse Transformation (np.expm1 is the inverse of np.log1p)
            predicted_price_actual = np.expm1(prediction_log[0])
            
            # Display result
            st.success(f"## 🎯 Predicted House Price: ${predicted_price_actual:,.2f}")
            
            # Show MLflow info
            st.info("""
            **Model Information:**
            - **Framework:** MLflow + Scikit-learn
            - **Model Type:** Linear Regression
            - **Accuracy:** ~58% (R² Score)
            - **Note:** Actual price may vary based on market conditions
            """)
            
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")

# --- END OF CORRECTED PREDICTION LOGIC ---

# Footer
st.markdown("---")
st.markdown("""
**Built with:**
- 🐍 Python
- 🤖 Scikit-learn
- 📊 **MLflow** (Model Tracking & Serving)
- 🔄 ZenML
- 🎨 Streamlit
""")