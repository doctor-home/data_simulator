# Data simulator
To create simulated patient's data.

<p align="center"> 
<img src="https://github.com/Doctor@home/data_simulator/blob/master/docs/doctor_at_home_architecture_overview.png" width="350">
</p>

Developed as part of Doctor@Home group during #CodeVsCovid19 72 hours hackaton.

<p align="center"> 
<img src="https://github.com/doctor-home/data_simulator/blob/master/docs/oximeter.jpg" width="250">
</p>


Real data are collected via Oxymeter and Thermometer from patients' home, automatically triaged via ML algorithm
and the consequent diagnosis is sent to the monitoring hospital. The resulting DB would also form a source of
information to study the impact of the virus according to age/previous conditions, and how symptoms evolve over time.  

## Install and run

```pip install -r requirements.txt```

```python data_generator.py```


## Data Files

### Organizations
The organizations / hospitals are stored in ```data_new/centers.csv```.
There are a total of 10 organizations in there. Each of them has the following attributes:
 - ```center_name``` : The name of the organization / hospital (string)
 - ```center_uuid``` : A unique identifier for each organization (string)

### Clinicians
The doctors/physicians are stored in ```data_new/physicians.csv```.
There are a total of 500 physicians in there. Each of them has the following attributes:
 - ```physician_name``` : The name of the doctor (string)
 - ```physician_uuid``` : A unique identifier for each doctor (string)
 - ```physician_username``` : usrename of each doctor (string)
 - ```physician_password``` : password each doctor (string)
 - ```center_name``` : The name of the doctor's hospital (string)
 - ```center_uuid``` : A unique identifier for each doctor's hospital (string)

### Patients
The patients are stored in ```data/patients_list.csv```.
There are a total of 5'000 patients in there. Each of them has the following attributes:
 - ```patientID``` : unique identifier of each patient (string)
 - ```name``` : First name of patient (string)
 - ```surname``` : Last name of patient (string)
 - ```phone``` : Phone number of patient (string)
 - ```city``` : City, where the patient lives (string)
 - ```language``` : prefered language (string)
 - ```age``` : Age of the patient (int)
 - ```preconditions``` : Existing preconditions (string - [None, Arthritis, Hypertension, Asthma, Cancer]) 
 - ```fitness``` : self assessed fitness score from 0 to 10 (int - [0,10])
 - ```smoker``` : is smoker or not? (bool)
 - ```clinician``` : List of Doctors responsible for the patient (List of string)
 - ```clinicianID``` : List of unique identifiers of responsible doctors (List of string)
 - ```organization``` : List of organizations responsible for the patient (List of string)
 - ```organizationID``` : List of unique identifiers of responsible organizations (List of string)

 ### Measurements
The monitored health records of 5000 patients are stored in ```data_new/measurements.csv```.
Each of them has the following attributes:
 - ```patientID``` : unique identifier of each patient (string).
 - ```timestamp``` : time, when the health data was recorded (timedate)
 - ```heart_beat``` : Heartbeat of patient at timestamp (int)
 - ```oxygenation``` : Level of Oxygen at timestamp (float)
 - ```temperature``` : Temperature at timestamp (float)
 - ```breathing_rate``` : Respiratory rate at timestamp (int)
 - ```triage_level``` : Severity of Sickness (int - [1,5])

