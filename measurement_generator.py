import datetime

import pandas as pd
import numpy as np
from faker import Faker
from faker.providers import date_time
from tqdm import tqdm

fake = Faker('en_UK')
fake.add_provider(date_time)


FIX_COLUMN_NAMES = ["patientID", 
                    "name", 
                    "surname", 
                    "phone", 
                    "city", 
                    "language",
                    "age", 
                    "preconditions", 
                    "fitness",
                    "smoker",
                    "clinician", 
                    "clinicianID",
                    "organization",
                    "organizationID"]

TIME_VARIABLE_COLUMNS = ["timestamp",
                         "daysUnderInspection", 
                         "hearthBeat",
                         "oxygenation",
                         "temperature",
                         "breathingRate",
                         "patient"]


unique_patients = pd.read_csv("data/unique_patients.csv")
unique_patients = unique_patients.set_index("Unnamed: 0")

# Fraction of all patients are the monitored patients
monitored_patients = unique_patients.sample(frac=0.2, random_state=42)


# helper functions:
def get_hearthrate(is_sick):
    """
    get the heartrate of the patient
    params:
        patient (bool): different values if patient is patient
    """
    # A normal resting heart rate for adults ranges from 60 to 100 beats per minute
    if is_sick:
        high = bool(np.random.choice([0, 1], 1)[0])
        if high:
            return np.random.randint(100, high=160)
        else:
            return np.random.randint(30, high=60)
    
    else:
        return np.random.randint(60, high=100)


def get_oxigen(is_sick):
    """
    get the oxygen of the patient
    params:
        patient (bool): different values if patient is sick
    """
    if is_sick:
        return np.random.uniform(low=0.89, high=0.94, size=1)[0]
    
    else:
        mu, sigma = 0.97, 0.2  # mean and standard deviation
        rate = np.random.normal(mu, sigma, 1,)[0]
        return rate if rate < 0.995 else 0.995


def get_temperature(is_sick):
    """
    get the temperature of the patient
    params:
        patient (bool): different values if patient is patient
    """
    if is_sick:
        return np.random.uniform(low=37.5, high=42.0, size=1)[0]
    
    else:
        mu, sigma = 36.5, 0.5 # mean and standard deviation
        return np.random.normal(mu, sigma, 1)[0]


def get_breathing(is_sick: bool):
    """
    get the breathing of the patient
    params:
        patient (bool): different values if patient is patient
    """
    if is_sick:
        high = bool(np.random.choice([0,1], 1)[0])
        if high:
            return np.random.randint(26, high=50)
        else:
            return np.random.randint(3, high=12)
    
    else:
        return np.random.randint(12, high=25)


if __name__ == "__main__":
    measurements_df = pd.DataFrame(columns=FIX_COLUMN_NAMES + TIME_VARIABLE_COLUMNS)

    for _, row in tqdm(monitored_patients.iterrows()):
        fixed_values = row.values.tolist()

        # healthy or not:
        sick = bool(np.random.choice([0, 1], 1, p=[0.8, 0.2])[0])

        # Get the number of previous measurements
        nr_measurements = np.random.choice(
            list(range(1, 16)), 1,
            p=(np.array(list(range(15, 0, -1))) / sum(list(range(1, 16)))).tolist())[0]

        # Iterate through all the measurements
        for timestamp in fake.time_series(start_date='-{}d'.format(nr_measurements), end_date='now', precision=datetime.timedelta(days=1/3), distrib=None, tzinfo=None):
            new_values = fixed_values + [
                timestamp[0],  # timestamp
                (datetime.date.today() - timestamp[0].date()).days,  # days in under measurement
                get_hearthrate(sick),
                get_oxigen(sick),
                get_temperature(sick),
                get_breathing(sick),
                sick
            ]
            # Add to existing dataframe
            measurements_df.loc[len(measurements_df)] = new_values

    measurements_df.to_csv("data/measured_data.csv")
