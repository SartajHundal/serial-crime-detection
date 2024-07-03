import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the Data Vault Model Structure
class Hub:
    def __init__(self, name):
        self.name = name
        self.data = []

class Link:
    def __init__(self, name):
        self.name = name
        self.data = []

class Satellite:
    def __init__(self, name):
        self.name = name
        self.data = []

# Function to load and transform data
def load_and_transform_data(serial_killer_file, simulated_file):
    # Simulate loading data from CSV files
    serial_killer_df = pd.read_csv(serial_killer_file)
    simulated_df = pd.read_csv(simulated_file)
    
    # Transform data into Data Vault structure
    hub_patient = Hub('Patient')
    hub_call = Hub('Call')
    link_patient_call = Link('PatientCallLink')
    satellite_patient_attribute = Satellite('PatientAttribute')
    satellite_call_detail = Satellite('CallDetail')
    
    # Example transformation logic
    for _, row in serial_killer_df.iterrows():
        patient_id = f'PATIENT_{row["PatientID"].zfill(5)}'  # Generating unique Patient ID
        call_id = f'CALL_{row["CallID"].zfill(5)}'  # Generating unique Call ID
        
        hub_patient.data.append({
            'id': patient_id,
            'name': row['PatientName']
        })
        
        hub_call.data.append({
            'id': call_id,
            'name': row['CallDescription']
        })
        
        link_patient_call.data.append({
            'source_hub_id': patient_id,
            'target_hub_id': call_id
        })
        
        satellite_patient_attribute.data.append({
            'patient_id': patient_id,
            'attribute_name': row['PatientAttribute']
        })
        
        satellite_call_detail.data.append({
            'call_id': call_id,
            'detail': row['CallDetail']
        })
    
    return hub_patient, hub_call, link_patient_call, satellite_patient_attribute, satellite_call_detail

# Function to visualize the data
def visualize_data(satellite_data):
    # Example visualization: Count of calls by detail
    sns.countplot(x='detail', data=satellite_data)
    plt.title('Count of Calls by Detail')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main Execution Flow
if __name__ == "__main__":
    # Load and transform data
    hub_patient, hub_call, link_patient_call, satellite_patient_attribute, satellite_call_detail = load_and_transform_data(
        'serial_killers_with_patient_calls.csv',
        'simulated_data.csv'
    )
    
    # Proceed to visualize the data
    visualize_data(satellite_call_detail.data)
