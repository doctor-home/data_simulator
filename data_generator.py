import os
import datetime
import uuid

import pandas as pd
import numpy as np
from faker import Faker
from faker.providers import phone_number, address, person, date_time, lorem
from tqdm import tqdm

fake = Faker(["en_UK"])
fake.add_provider(person)
fake.add_provider(phone_number)
fake.add_provider(address)
fake.add_provider(date_time)
fake.add_provider(lorem)


NOW = datetime.datetime(2020, 3, 28, 17, 32, 8, 947063)

TRIAGE_LEVELS = [1, 2, 3, 4, 5]

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
    "organizationID",
    "under_observation"
]

TIME_VARIABLE_COLUMNS = [
    "timestamp",
    "heart_beat",
    "oxygenation",
    "temperature",
    "breathing_rate",
    "triage_level",
]


def _get_uuid():
    return str(uuid.uuid4())


def generate_centers(pfi_centers):
    """ Create list of Health centers / hospitals """
    center_df = pd.DataFrame(columns=["center_name", "center_uuid"])
    names = []
    center_uuids = []

    for i in tqdm(range(10)):
        names.append("center_{}".format(i))
        center_uuids.append(_get_uuid())

    center_df["center_name"] = names
    center_df["center_uuid"] = center_uuids

    center_df.to_csv(pfi_centers)


def generate_physicians(pfi_physicians, pfi_centers):
    """ Create list of Doctors:"""
    physician_df = pd.DataFrame(columns=["physician_name", "physician_uuid"])
    centers_df = pd.read_csv(pfi_centers)

    physician_uuids = []
    names = []
    usernames = []
    passwords = []
    center_names = []
    center_uuids = []

    for _ in tqdm(range(500)):
        physician_uuids.append(_get_uuid())
        first_name = fake.first_name()
        last_name = fake.last_name()

        names.append("Dr. " + first_name + " " + last_name)
        usernames.append((first_name + "_" + last_name).replace(" ", "").lower())
        passwords.append("_".join(fake.words(nb=3)))

        center = centers_df.sample(1)
        center_names.append(center["center_name"].values.tolist()[0])
        center_uuids.append(center["center_uuid"].values.tolist()[0])

    physician_df["physician_name"] = names
    physician_df["physician_uuid"] = physician_uuids
    physician_df["physician_username"] = usernames
    physician_df["physician_password"] = passwords
    physician_df["center_name"] = center_names
    physician_df["center_uuid"] = center_uuids

    physician_df.to_csv(pfi_physicians)


def generate_patients(
    pfi_patients_list, pfi_physicians, pfi_centers, num_patients=5000
):
    """Create unique list of patients"""
    assert os.path.exists(pfi_physicians), pfi_physicians
    assert os.path.exists(pfi_centers), pfi_centers

    this_year = datetime.date.today().year
    physician_df = pd.read_csv(pfi_physicians)

    fix_df = pd.DataFrame(columns=FIX_COLUMN_NAMES)

    for _ in tqdm(range(num_patients)):

        nr_physicians = np.random.choice([1, 2, 3], 1, p=[0.75, 0.2, 0.05])[0]

        physician = physician_df.sample(nr_physicians)

        row = [
            _get_uuid(),
            fake.first_name(),
            fake.last_name(),
            fake.phone_number(),
            fake.city(),
            np.random.choice(["English", "German", "French", "Italian", "Dutch"], 1)[
                0
            ],  # language
            this_year
            - fake.date_of_birth(
                tzinfo=None, minimum_age=10, maximum_age=105
            ).year,  # age
            np.random.choice(
                list(PRECONDITIONS.keys()), 1, p=list(PRECONDITIONS.values())
            )[
                0
            ],  # precondition
            np.random.randint(10),  # fitness
            bool(np.random.choice([0, 1], 1, p=[0.85, 0.15])[0]),  # smoker
            physician["physician_name"].values.tolist(),
            physician["physician_uuid"].values.tolist(),
            physician["center_name"].values.tolist(),
            physician["center_uuid"].values.tolist(),
            np.random.choice([True, False], p=[0.2, 0.8])  # under observation
        ]

        fix_df.loc[len(fix_df)] = row

    fix_df.to_csv(pfi_patients_list)


def generate_random_triage_levels_for_a_patient(age):
    """ Triage level is the label we want to infer. For the simulated data we are """

    def age_weights(p, num_vals, epsilon=0.08):
        n = num_vals + 1
        h = 1 / n
        if p <= 0.5:
            a, b, x = epsilon * (n - 1), 1 - h, p / 0.5
            pos_pivot = (b - a) * x + a
            h_bar = pos_pivot / (n - 2)
            intervals = [k * h_bar for k in range(n - 1)] + [1]

        else:
            a, b, x = h, 1 - epsilon * (n - 1), (p - 0.5) / 0.5
            pos_pivot = (b - a) * x + a
            h_bar = (1 - pos_pivot) / (n - 2)
            intervals = [0] + [1 - k * h_bar for k in range(n - 1)]
            intervals = sorted(intervals)

        return [intervals[j + 1] - intervals[j] for j in range(num_vals)][::-1]

    assert age <= 117, "A new Jiroemon Kimura found."

    normalized_age = int(age / 117)

    num_of_triage_level_variations = np.random.choice(
        [1, 2, 3, 4], p=[0.5, 0.3, 0.1, 0.1]
    )
    triage_levels = np.random.choice(
        TRIAGE_LEVELS,
        p=age_weights(normalized_age, len(TRIAGE_LEVELS)),
        size=num_of_triage_level_variations,
    )
    return triage_levels


def get_readouts(tl, ntp, get_one_readout):

    criteria = np.random.choice(["random", "triage_level"], p=[0.1, 0.9])
    if criteria == "random":
        severity = np.random.uniform(0, 1)
    else:  # triage level based criteria
        severity = tl / np.max(TRIAGE_LEVELS) + np.random.normal(scale=0.3)
        severity = np.clip(severity, a_min=0, a_max=1)

    return [get_one_readout(severity) for _ in range(ntp)]


def get_heart_beats(tl: int, ntp: int) -> list:
    """Triage level and number of time-points to random heart beats per min"""

    def get_one_readout(sev):
        if 0 < sev < 0.6:
            return np.random.randint(60, high=100)
        elif 0.6 <= sev < 0.8:
            return np.random.randint(100, high=140)
        else:
            return np.random.randint(140, high=150)

    return get_readouts(tl, ntp, get_one_readout)


def get_oxygenation(tl: int, ntp: int) -> list:
    """Triage level and number of time-points to random oxygenation in
    percentage oxygenated haemoglobin"""

    def get_one_readout(sev):
        if 0 < sev < 0.7:
            # Normal is between 90% and 100%
            return np.random.randint(90, high=100)
        elif 0.7 <= sev < 0.8:
            # mild hypoxia: 85% to 90%
            return np.random.randint(85, high=90)
        elif 0.8 <= sev < 0.95:
            # hypoxia: 80% to 85%
            return np.random.randint(80, high=85)
        else:
            # severe hypoxia: 75% to 80%
            return np.random.randint(75, high=80)

    return get_readouts(tl, ntp, get_one_readout)


def get_temperature(tl: int, ntp: int) -> list:
    """Triage level and number of time-points to temperature in Celsius"""

    def get_one_readout(sev):
        if 0 <= sev < 0.6:
            # normal
            return np.round(np.random.uniform(36.5, 37.5), decimals=1)
        elif 0.6 <= sev < 0.85:
            # medium
            return np.round(np.random.uniform(37.5, 39), decimals=1)
        else:
            # high
            return np.round(np.random.uniform(39, 41), decimals=1)

    return get_readouts(tl, ntp, get_one_readout)


def get_breathing_rate(tl: int, ntp: int) -> list:
    """Triage level and number of time-points to breathing rate per minute"""

    def get_one_readout(sev):

        if 0 <= sev < 0.7:
            # normal 12 to 20
            return np.random.randint(12, high=20)
        elif 0.7 <= sev < 0.85:
            # abnormal 20 to 25
            return np.random.randint(20, high=25)
        else:
            # abnormal 25 to 30
            return np.random.randint(25, high=30)

    return get_readouts(tl, ntp, get_one_readout)


def generate_historical_data(triage_levels: list) -> pd.DataFrame:

    nr_measurements = np.random.choice(
        list(range(3, 8)),
        1,
        p=(np.array(list(range(7, 2, -1))) / sum(list(range(3, 8)))).tolist(),
    )[0]

    timepoints = fake.time_series(
        start_date="-{}d".format(nr_measurements),
        end_date=NOW,
        precision=datetime.timedelta(days=1 / 3),
        distrib=None,
        tzinfo=None,
    )

    measurements_df = pd.DataFrame(columns=TIME_VARIABLE_COLUMNS)

    timepoints = list(timepoints)
    num_timepoints = len(timepoints)

    for triage_level in triage_levels:
        heart_beat = get_heart_beats(triage_level, num_timepoints)
        oxygenation = get_oxygenation(triage_level, num_timepoints)
        temperature = get_temperature(triage_level, num_timepoints)
        breathing_rate = get_breathing_rate(triage_level, num_timepoints)

        for tp_n, tp in enumerate(timepoints):
            data_at_tp = dict(
                timestamp=tp[0],
                heart_beat=heart_beat[tp_n],
                oxygenation=oxygenation[tp_n],
                temperature=temperature[tp_n],
                breathing_rate=breathing_rate[tp_n],
                triage_level=triage_level,
            )
            measurements_df = measurements_df.append(data_at_tp, ignore_index=True)

    return measurements_df


def generate_data_for_each_patient(pfi_measured_data, pfi_patients_list, single_file=True):
    """
    Get all the patients from pfi_patients_list and create their dummy history.
    All patients measurements in a single .csv file (>100k lines), to be grouped by patient id.
    """
    assert os.path.exists(pfi_patients_list), pfi_patients_list

    df_patients = pd.read_csv(pfi_patients_list, index_col=0)

    df_measurements = pd.DataFrame(columns=["patientID"] + TIME_VARIABLE_COLUMNS)

    for patient_uuid, patient_age in tqdm(
        zip(df_patients["patientID"], df_patients["age"])
    ):
        triage_levels = generate_random_triage_levels_for_a_patient(patient_age)
        historical_data_df = generate_historical_data(triage_levels)
        historical_data_df["patientID"] = [
            patient_uuid for _ in range(len(historical_data_df))
        ]
        df_measurements = pd.concat([df_measurements, historical_data_df])

    df_measurements = df_measurements.reset_index().drop(["index"], axis=1)
    df_measurements.to_csv(pfi_measured_data)


if __name__ == "__main__":
    # pfi: path to file
    # pfo: path to folder
    root = os.path.dirname(__file__)
    data_folder = os.path.join(root, "data_new")

    if os.path.exists(data_folder):
        raise ValueError(
            f"Data folder {data_folder} already exist. Delete it and run again to re-create the data."
        )

    os.mkdir(data_folder)

    pfi_centers_ = os.path.join(data_folder, "centers.csv")
    pfi_physicians_ = os.path.join(data_folder, "physicians.csv")
    pfi_patients_list_ = os.path.join(data_folder, "patients_list.csv")

    print("\nGenerating centers...")
    generate_centers(pfi_centers_)
    print("\nGenerating physicians...")
    generate_physicians(pfi_physicians_, pfi_centers_)
    print("\nGenerating patients list...")
    generate_patients(
        pfi_patients_list_, pfi_centers=pfi_centers_, pfi_physicians=pfi_physicians_,
    )

    pfi_physicians_ = os.path.join(data_folder, "measurements.csv")

    print("\nGenerating patients data...")
    generate_data_for_each_patient(pfi_physicians_, pfi_patients_list_)
