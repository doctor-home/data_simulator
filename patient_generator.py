import pandas as pd
import numpy as np
from faker import Faker
from faker.providers import phone_number, address, person, date_time
import datetime
import string
import random
from tqdm import tqdm

fake = Faker('en_UK')
fake.add_provider(person)
fake.add_provider(phone_number)
fake.add_provider(address)    
fake.add_provider(date_time)

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    """
    Creates a random lower case string
    """
    return ''.join(random.choice(chars) for _ in range(size))


# Create list of Health centers / hospitals
center_df = pd.DataFrame(columns=["center_name", "center_uuid"])
names = []
center_uuids = []

for i in range(10):
    names.append("center_{}".format(i))
    center_uuids.append(id_generator(size=10))

center_df["center_name"] = names
center_df["center_uuid"] = center_uuids

center_df.to_csv("data/df_centers.csv")


# Create list of Doctors:
physician_df = pd.DataFrame(columns = ["physician_name", "physician_uuid"])
physician_uuids = []
names = []

for _ in range(500):
    physician_uuids.append(id_generator(size=10))
    names.append("Dr. " + fake.first_name() + " " + fake.last_name())
    
physician_df["physician_name" ] = names
physician_df["physician_uuid" ] = physician_uuids

physician_df.to_csv("data/df_physicians.csv")


# Create unique list of patients
this_year = datetime.date.today().year

PRECONDITIONS = {"None" : 0.60, 
                 "Arthritis": 0.1, 
                 "Hypertension": 0.24, 
                 "Asthma": 0.05, 
                 "Cancer":0.01, }

FIX_COLUMN_NAMES = ["patient_uuid", 
                    "name", 
                    "surname", 
                    "phone", 
                    "city", 
                    "language",
                    "age", 
                    "preconditions", 
                    "fitness",
                    "smoker",
                    "physician_name", 
                    "physician_uuid",
                    "center_name",
                    "center_uuid"]

TIME_VARIABLE_COLUMNS = ["timestamp", 
                         "hearth_rate",
                         "oxigen_level",
                         "temperature",
                         "nr_days", 
                         "breathing_rate",
                         "label"]

fix_df = pd.DataFrame(columns=FIX_COLUMN_NAMES)


for _ in tqdm(range(10_000)):
    
    nr_physicians = np.random.choice([1,2,3], 1, p=[0.75,0.2,0.05])[0]
    nr_centers = np.random.choice([1,2], 1, p=[0.9,0.1])[0]
    
    physician = physician_df.sample(nr_physicians)
    center = center_df.sample(nr_centers)
    
    row = [id_generator(size=10), #uuid
                  fake.first_name(), #first na,me
                  fake.last_name(), #last name
                  fake.phone_number(), # phone
                  fake.city(), # city
                  np.random.choice(["English","German", "French", "Italian", "Dutch"], 1)[0], # language
                  this_year - fake.date_of_birth(tzinfo=None, minimum_age=10, maximum_age=105).year, #age
                  np.random.choice(list(PRECONDITIONS.keys()), 1, p=list(PRECONDITIONS.values()))[0], #precondition
                  np.random.randint(10), # fitness
                  bool(np.random.choice([0,1], 1,p=[0.85,0.15])[0]), # smoker
                  physician["physician_name"].values.tolist(), #physician name
                  physician["physician_uuid"].values.tolist(), #physician uuid
                  center["center_name"].values.tolist(), # center name
                  center["center_uuid"].values.tolist() # center uuid
                  ]
    
    
    fix_df.loc[len(fix_df)] = row
    
fix_df.to_csv("data/unique_patients.csv")