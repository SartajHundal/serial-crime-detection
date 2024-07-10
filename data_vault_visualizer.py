import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def load_and_transform_data(serial_killer_file, simulated_file):
    try:
        serial_killer_df = pd.read_csv(serial_killer_file)
        simulated_df = pd.read_csv(simulated_file)
    except FileNotFoundError:
        print("One or both CSV files not found.")
        return None
    
    hub_patient = Hub('Patient')
    hub_call = Hub('Call')
    link_patient_call = Link('PatientCallLink')
    satellite_patient_attribute = Satellite('PatientAttribute')
    satellite_call_detail = Satellite('CallDetail')
    
    for _, row in serial_killer_df.iterrows():
        patient_id = f'PATIENT_{row["PatientID"].zfill(5)}'
        call_id = f'CALL_{row["CallID"].zfill(5)}'
        
        hub_patient.data.append({'id': patient_id, 'name': row['PatientName']})
        hub_call.data.append({'id': call_id, 'name': row['CallDescription']})
        link_patient_call.data.append({'source_hub_id': patient_id, 'target_hub_id': call_id})
        satellite_patient_attribute.data.append({'patient_id': patient_id, 'attribute_name': row['PatientAttribute']})
        satellite_call_detail.data.append({'call_id': call_id, 'detail': row['CallDetail']})
    
    return hub_patient, hub_call, link_patient_call, satellite_patient_attribute, satellite_call_detail

def visualize_data(satellite_data):
    if not satellite_data:
        print("No data to visualize.")
        return
    
    sns.countplot(x='detail', data=pd.DataFrame(satellite_data))
    plt.title('Count of Calls by Detail')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        hub_patient, hub_call, link_patient_call, satellite_patient_attribute, satellite_call_detail = load_and_transform_data(
            'serial_killers_with_patient_calls.csv',
            'simulated_data.csv'
        )
        
        if hub_patient and hub_call and link_patient_call and satellite_patient_attribute and satellite_call_detail:
            visualize_data(satellite_call_detail.data)
        else:
            print("Data loading failed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
