import pandas as pd
import numpy as np
from faker import Faker
from faker.providers import phone_number, address, person, date_time
import datetime
import random
import string

fake = Faker('de_DE')
fake.add_provider(person)
fake.add_provider(phone_number)
fake.add_provider(address)    
fake.add_provider(date_time)

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

FIX_COLUMN_NAMES = ["patient_uuid", 
                    "name", 
                    "surname", 
                    "phone", 
                    "city", 
                    "country", 
                    "age", 
                    "preconditions", 
                    "fitness",
                    "physician", 
                    "physician_uuid",
                    "center"
                    "center_uuid"]

TIME_VARIABLE_COLUMNS = ["timestamp", 
                         "hearth_rate",
                         "oxigen_level",
                         "temperature",
                         "nr_days", 
                         "breathing_rate",
                         "label"]

fix_df = pd.DataFrame(columns=FIX_COLUMN_NAMES)

names = []
surnames = []
patient_uuids = []
phones = []
cities = []
countries = []
ages = []
fitness = []


for _ in range(10_000):
    names.append(fake.first_name())
    surnames.append(fake.last_name())
    patient_uuids.append(id_generator(size=10))
    phones.append(fake.phone_number())
    cities.append(fake.city())
    countries.append(fake.country())
    ages.append(datetime.date.today().year - fake.date_of_birth(tzinfo=None, minimum_age=10, maximum_age=105).year)
    fitness.append(np.random.randint(10))
    
fix_df["name" ] = names
fix_df["surname" ] = surnames
fix_df["patient_uuid" ] = patient_uuids
fix_df["phone" ] = phones
fix_df["city" ] = cities
fix_df["country" ] = countries
fix_df["age" ] = ages
fix_df["fitness" ] = fitness