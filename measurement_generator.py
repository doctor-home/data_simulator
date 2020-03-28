import pandas as pd
import numpy as np
from faker import Faker
from faker.providers import date_time
import datetime
import string
import random
from tqdm import tqdm

fake = Faker('en_UK')
fake.add_provider(date_time)


FIX_COLUMN_NAMES = ["patient_uuid", 
                    "name", 
                    "surname", 
                    "phone", 
                    "city", 
                    "age", 
                    "preconditions", 
                    "fitness",
                    "physician_name", 
                    "physician_uuid",
                    "center_name",
                    "center_uuid"]

TIME_VARIABLE_COLUMNS = ["timestamp",
                         "nr_days", 
                         "hearth_rate",
                         "oxigen_level",
                         "temperature",
                         "breathing_rate",
                         "label"]


unique_patients = pd.read_csv("data/unique_patients.csv")
unique_patients = unique_patients.set_index("Unnamed: 0")

# Fraction of all patients are the monitored patients
monitored_patients = unique_patients.sample(frac=0.2, random_state=42)

# helper functions:
def get_hearthrate(sick):
    """
    get the heartrate of the patient
    params:
        sick (bool): different values if patient is sick
    """
    
    # TODO
    return 1


def get_oxigen(sick):
    """
    get the oxigen of the patient
    params:
        sick (bool): different values if patient is sick
    """
    
    # TODO
    return 2


def get_temperature(sick):
    """
    get the temperature of the patient
    params:
        sick (bool): different values if patient is sick
    """
    
    # TODO
    return 3


def get_breathing(sick):
    """
    get the breathing of the patient
    params:
        sick (bool): different values if patient is sick
    """
    
    # TODO
    return 4

def get_breathing(sick):
    """
    get the breathing of the patient
    params:
        sick (bool): different values if patient is sick
    """
    
    pass


measurement_df = pd.DataFrame(columns = FIX_COLUMN_NAMES + TIME_VARIABLE_COLUMNS)

for _, row in tqdm(monitored_patients.iterrows()):
    fixed_values = row.values.tolist()
    
    # healthy or not:
    sick = bool(np.random.choice([0,1], 1,p=[0.8,0.2])[0])
    
    # Get the number of previous measurements
    nr_measurements = np.random.choice(list(range(1,16)), 1, 
                                       p=(np.array(list(range(15,0, -1))) / sum(list(range(1,16)))).tolist())[0]
    
    
    # Iterate through all the measurements
    for timestamp in fake.time_series(start_date='-{}d'.format(nr_measurements), end_date='now', precision=datetime.timedelta(days=1/3), distrib=None, tzinfo=None):
        new_values = fixed_values + [
            timestamp[0], # timestamp
            (datetime.date.today() - timestamp[0].date()).days, # days in under measurement
            get_hearthrate(sick),
            get_oxigen(sick),
            get_temperature(sick),
            get_breathing(sick)
        ]
        
        # Add to existing dataframe
        measurement_df.loc[len(measurement_df)] = new_values
    
    
    