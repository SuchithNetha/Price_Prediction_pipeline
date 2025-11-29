"""
Export MLflow model to a pickle file for deployment
"""
import mlflow
import mlflow.sklearn
import pickle
import os

# --- Configuration (Based on your system's ZenML path) ---

# !!! CRITICAL FIX: REPLACE THIS WITH YOUR ABSOLUTE ZENML PATH !!!
# This path must be exact. I am using the path identified in previous attempts.
ZENML_TRACKING_URI = 'file:C:\\Users\\suchi\\AppData\\Roaming\\zenml\\local_stores\\7f120baa-71f3-4e9f-a2e6-7301bc1845a2\\mlruns'

# CRITICAL FIX: The Run ID from your successful training run
RUN_ID = "173084b4925743889a1348fd990f7dc5" 
# The RUN_ID in your original script ("37fd669970544f8ca4bbc9dc7f821cf6") 
# might be incorrect if you switched models. Use the one you confirmed was successful.

# --- Script Logic ---

# Set MLflow tracking URI to the ZenML store
mlflow.set_tracking_uri(ZENML_TRACKING_URI)

# The correct MLflow URI format for loading artifacts
MODEL_URI = f"runs:/{RUN_ID}/model"
output_path = "model.pkl"

model = None
try:
    print(f"Trying to load model from: {MODEL_URI} at tracking URI: {ZENML_TRACKING_URI}")
    
    # Load the model directly using the runs URI
    model = mlflow.sklearn.load_model(MODEL_URI)
    
    print(f"✅ Successfully loaded model from MLflow.")
    
    # Save as pickle file
    with open(output_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"✅ Model successfully saved to: {output_path}")
    if os.path.exists(output_path):
        print(f"✅ File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
        print("\n*** The Streamlit app can now load 'model.pkl' and will work. ***")

except Exception as e:
    print(f"❌ FAILED TO LOAD MODEL. Error: {e}")
    print("\n💡 Action Required: Double-check the ZENML_TRACKING_URI and RUN_ID variables above.")