import os
import datetime
import uuid

import pandas as pd
import numpy as np
from faker import Faker
from faker.providers import phone_number, address, person, date_time
from tqdm import tqdm

fake = Faker('en_UK')
fake.add_provider(person)
fake.add_provider(phone_number)
fake.add_provider(address)    
fake.add_provider(date_time)


PRECONDITIONS = {
    "None": 0.60,
    "Arthritis": 0.1,
    "Hypertension": 0.24,
    "Asthma": 0.05,
    "Cancer": 0.01,
}

FIX_COLUMN_NAMES = [
    "patientID",
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
    "organizationID"
]


def _get_uuid():
    return str(uuid.uuid4())


def generate_centers(pfi_centers):
    """ Create list of Health centers / hospitals """
    center_df = pd.DataFrame(columns=["center_name", "center_uuid"])
    names = []
    center_uuids = []

    for i in range(10):
        names.append("center_{}".format(i))
        center_uuids.append(_get_uuid())

    center_df["center_name"] = names
    center_df["center_uuid"] = center_uuids

    center_df.to_csv(pfi_centers)


def generate_physicians(pfi_physicians):
    """ Create list of Doctors:"""
    physician_df = pd.DataFrame(columns = ["physician_name", "physician_uuid"])
    physician_uuids = []
    names = []

    for _ in range(500):
        physician_uuids.append(_get_uuid())
        names.append("Dr. " + fake.first_name() + " " + fake.last_name())

    physician_df["physician_name"] = names
    physician_df["physician_uuid"] = physician_uuids

    physician_df.to_csv(pfi_physicians)


def generate_patients(pfi_patients_list, pfi_physicians, pfi_centers, num_patients=5000):
    """Create unique list of patients"""
    assert os.path.exists(pfi_physicians)
    assert os.path.exists(pfi_centers)

    this_year = datetime.date.today().year
    physician_df = pd.read_csv(pfi_physicians)
    centers_df = pd.read_csv(pfi_centers)

    fix_df = pd.DataFrame(columns=FIX_COLUMN_NAMES)

    for _ in tqdm(range(num_patients)):

        nr_physicians = np.random.choice([1, 2, 3], 1, p=[0.75, 0.2, 0.05])[0]
        nr_centers = np.random.choice([1, 2], 1, p=[0.9, 0.1])[0]

        physician = physician_df.sample(nr_physicians)
        center = centers_df.sample(nr_centers)

        row = [
            _get_uuid(),
            fake.first_name(),
            fake.last_name(),
            fake.phone_number(),
            fake.city(),
            np.random.choice(["English", "German", "French", "Italian", "Dutch"], 1)[0],  # language
            this_year - fake.date_of_birth(tzinfo=None, minimum_age=10, maximum_age=105).year,  # age
            np.random.choice(list(PRECONDITIONS.keys()), 1, p=list(PRECONDITIONS.values()))[0],  # precondition
            np.random.randint(10),  # fitness
            bool(np.random.choice([0, 1], 1, p=[0.85, 0.15])[0]),  # smoker
            physician["physician_name"].values.tolist(),
            physician["physician_uuid"].values.tolist(),
            center["center_name"].values.tolist(),
            center["center_uuid"].values.tolist()
        ]

        fix_df.loc[len(fix_df)] = row

    fix_df.to_csv(pfi_patients_list)


def generate_data_for_each_patient(pfo_patients_data, pfi_patients_list):
    pass


if __name__ == "__main__":
    # pfi: path to file
    # pfo: path to folder
    root = os.path.dirname(os.path.dirname(__file__))
    data_folder = os.path.join(root, "data")

    if os.path.exists(data_folder):
        raise ValueError(
            f"Data folder {data_folder} already exist. Delete it and run again to re-create the data."
        )

    pfi_centers_ = os.path.join(data_folder)
    pfi_physicians_ = os.path.join(data_folder)
    pfi_patients_list_ = os.path.join(data_folder)

    print("Generating centers...")
    generate_centers(pfi_centers_)
    print("Generating physicians...")
    generate_physicians(pfi_physicians_)
    print("Generating patients list...")
    generate_patients(pfi_patients_list_, pfi_centers=pfi_centers_, pfi_physicians=pfi_physicians_)

    pfo_patients_data = os.path.join(data_folder, )

    print("Generating patients data...")
    generate_data_for_each_patient(pfo_patients_data, pfi_patients_list_)
