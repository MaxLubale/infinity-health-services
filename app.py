import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate as tabulate_module 
from tabulate import tabulate as tabulate_function
from lib.base import Base
from lib.doctor import Doctor
from lib.nurse import Nurse
from lib.patient import Patient
from lib.ward import Ward
import logging


# Configure the logging level for SQLAlchemy
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING) 

# Create the engine
DATABASE_URL = "sqlite:///infinity_health.db"
engine = create_engine(DATABASE_URL, echo=True)

# Bind the engine to the metadata
Base.metadata.bind = engine

# Create a session
DBSession = sessionmaker(bind=engine)
session = DBSession()



@click.group()
def cli():
        """WELCOME TO INFINITY HEALTH SERVICES COMMAND-LINE INTERFACE."""
click.echo(click.style('\nWELCOME TO INFINITY HEALTH SERVICES COMMAND-LINE INTERFACE.\n', fg='green'))

# Command to Initialize the database.

def initdb():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)
    click.echo(click.style(f'Initialized the database.', fg='green'))

# Command to add a ward

@click.argument('name')
def add_ward(name):
    """Add a ward."""
    ward = Ward(name=name)
    session.add(ward)
    session.commit()
    click.echo(click.style(f'Ward {name} added successfully.', fg='green'))

# Command to list wards

def list_wards():
    """List all wards."""
    headers = ["ID", "Name"]
    wards = session.query(Ward).all()

    click.echo(click.style('List of Wards:', fg='green', bold=True))

    ward_data = [
        (ward.id, ward.name)
        for ward in wards
    ]

    click.echo(click.style(tabulate_module(ward_data, headers=headers, tablefmt="grid"), fg='green'))

# Command to add a doctor

@click.argument('name')
@click.argument('age', type=int)
def add_doctor(name, age):
    """Add a doctor."""
    doctor = Doctor(name=name, age=age)
    session.add(doctor)
    session.commit()
    click.echo(click.style(f'Doctor {name} added successfully.', fg='green'))

# Command to list wards

def list_doctors():
    """List all doctors."""
    headers = ["ID", "Name", "Age"]
    doctors = session.query(Doctor).all()

    click.echo(click.style('List of Doctors:', fg='green', bold=True))

    doctor_data = [
        (doctor.id, doctor.name, doctor.age)
        for doctor in doctors
    ]

    click.echo(click.style(tabulate_module(doctor_data, headers=headers, tablefmt="grid"), fg='green'))

    # Command to add a nurse

@click.argument('name')
@click.argument('age', type=int)
@click.argument('ward')
def add_nurse(name, age, ward):
    """Add a nurse."""
    # Check if the ward exists
    ward_obj = session.query(Ward).filter_by(name=ward).first()

    if not ward_obj:
        click.echo('Ward does not exist. Please add it first.')
        return

    nurse = Nurse(name=name, age=age, ward_id=ward_obj.id)
    session.add(nurse)
    session.commit()
    click.echo(click.style(f'Nurse {name} added successfully.', fg='green'))


# Command to list nurses

def list_nurses():
    """List all nurses."""
    headers = ["Name", "ID", "Age", "Ward"]
    nurses = session.query(Nurse).all()
    
    click.echo(click.style('List of Nurses:', fg='green', bold=True))

    nurse_data = [
        (nurse.name, nurse.id, nurse.age, nurse.ward.name if nurse.ward else 'N/A')
        for nurse in nurses
    ]

    click.echo(click.style(tabulate_module(nurse_data, headers=headers, tablefmt="grid"), fg='green'))

    # Command to add a patient

@click.argument('name')
@click.argument('age', type=int)
@click.argument('sex')
@click.argument('drugs')
@click.argument('ward')
@click.argument('diagnosis')
@click.argument('nurse')
def add_patient(name, age, sex, drugs, ward, diagnosis, nurse):
    """Add a patient."""
    # Check if the ward and nurse exist
    ward_obj = session.query(Ward).filter_by(name=ward).first()
    nurse_obj = session.query(Nurse).filter_by(name=nurse).first()

    if not ward_obj or not nurse_obj:
        click.echo('Ward or nurse does not exist. Please add them first.')
        return

    patient = Patient(
        name=name,
        age=age,
        sex=sex,
        drugs=drugs,
        ward_id=ward_obj.id,
        diagnosis=diagnosis,
        nurse_id=nurse_obj.id
    )
    session.add(patient)
    session.commit()
    click.echo(click.style(f'Patient {name} added successfully.', fg='green'))

    # Command to list patients

def list_patients():
    """List all patients."""
    headers = ["ID", "Name", "Age", "Sex", "Drugs", "Ward", "Diagnosis", "Nurse"]
    patients = session.query(Patient).all()

    click.echo(click.style('List of Patients:', fg='green', bold=True))

    patient_data = [
        (patient.id, patient.name, patient.age, patient.sex, patient.drugs, patient.ward.name if patient.ward else 'N/A', patient.diagnosis, patient.nurse.name if patient.nurse else 'N/A')
        for patient in patients
    ]

    click.echo(click.style(tabulate_module(patient_data, headers=headers, tablefmt="grid"), fg='green'))




# Command to list all patients in a ward

@click.argument('ward')
def list_patients_in_ward(ward):
    """List all patients in a ward showing their names and nurses."""
    ward_obj = session.query(Ward).filter_by(name=ward).first()

    if not ward_obj:
        click.echo(click.style('Ward does not exist.', fg='red'))
        return

    patients = session.query(Patient).filter_by(ward_id=ward_obj.id).all()

    if not patients:
        click.echo(click.style(f'No patients in the {ward} ward.', fg='red'))
        return

    patient_data = [
        (patient.id, patient.name, patient.nurse.name if patient.nurse else 'N/A')
        for patient in patients
    ]

    headers = ["Patient ID", "Name", "Nurse"]

    click.echo(click.style(tabulate_module(patient_data, headers=headers, tablefmt="grid"), fg='green'))

    # Command to search for a patient

@click.argument('name')
def search_patient(name):
    """Search for a specific patient by name."""
    patient = session.query(Patient).filter_by(name=name).first()

    if not patient:
        click.echo(f'Patient with name {name} not found.')
        return

    headers = ["Attribute", "Value"]
    patient_data = [
        ("ID", patient.id),
        ("Name", patient.name),
        ("Age", patient.age),
        ("Sex", patient.sex),
        ("Drugs", patient.drugs),
        ("Ward", patient.ward.name),
        ("Diagnosis", patient.diagnosis),
    ]

    click.echo(click.style('Patient Details:', fg='blue', bold=True))
    
    click.echo(click.style(tabulate_function(patient_data, headers=headers, tablefmt="grid"), fg='green'))

    if patient.nurse:
        nurse_data = [
            ("Nurse ID", patient.nurse.id),
            ("Nurse Name", patient.nurse.name),
            ("Nurse Age", patient.nurse.age),
        ]

        click.echo(click.style('Nurse Details:', fg='blue', bold=True))
        
        click.echo(click.style(tabulate_function(nurse_data, headers=headers, tablefmt="grid"), fg='green'))


# Command to discharge a patient

@click.argument('patient_name')
def delete_patient(patient_name):
    """Discharge a patient by name."""
    patient = session.query(Patient).filter_by(name=patient_name).first()

    if not patient:
        click.echo(f'Patient with name {patient_name} not found.')
        return

    session.delete(patient)
    session.commit()
    click.echo(click.style(f'Patient with name {patient_name} discharged successfully.', fg='green'))

# Command to delete a nurse

@click.argument('nurse_name')
def delete_nurse(nurse_name):
    """Delete a nurse by name."""
    nurse = session.query(Nurse).filter_by(name=nurse_name).first()

    if not nurse:
        click.echo(f'Nurse with name {nurse_name} not found.')
        return

    session.delete(nurse)
    session.commit()
    click.echo(click.style(f'Nurse with name {nurse_name} deleted successfully.', fg='green'))

# Command to delete a doctor

@click.argument('doctor_name')
def delete_doctor(doctor_name):
    """Delete a doctor by name."""
    doctor = session.query(Doctor).filter_by(name=doctor_name).first()

    if not doctor:
        click.echo(f'Doctor with name {doctor_name} not found.')
        return

    session.delete(doctor)
    session.commit()
    click.echo(click.style(f'Doctor with name {doctor_name} deleted successfully.', fg='green'))

if __name__ == '__main__':
    while True:
        print("\n" + "="*58 + "\n")
        print("\nChoose an option:")
        print("1. Initialize the database")
        print("2. Add a ward")
        print("3. List all wards")
        print("4. Add a doctor")
        print("5. List all doctors")
        print("6. Add a nurse")
        print("7. List all nurses")
        print("8. Add a patient")
        print("9. List all patients")
        print("10. List all patients in a ward")
        print("11. Search for a patient")
        print("12. Discharge a patient")
        print("13. Delete a nurse")
        print("14. Delete a doctor")
        print("15. Quit")

        choice = input("Enter the number of your choice: ")

        if choice == '1':
            Base.metadata.create_all(bind=engine)
            print('Initialized the database.')
        elif choice == '2':
            name = input("Enter the ward name: ")
            add_ward(name)
        elif choice == '3':
            list_wards()
        elif choice == '4':
            name = input("Enter the doctor name: ")
            age = input("Enter the doctor age: ")
            add_doctor(name, age)
        elif choice == '5':
            list_doctors()
        elif choice == '6':
            name = input("Enter the nurse name: ")
            age = input("Enter the nurse age: ")
            ward = input("Enter the ward name: ")
            add_nurse(name, age, ward)
        elif choice == '7':
            list_nurses()
        elif choice == '8':
            name = input("Enter the patient name: ")
            age = input("Enter the patient age: ")
            sex = input("Enter the patient sex: ")
            drugs = input("Enter the patient drugs: ")
            ward = input("Enter the ward name: ")
            diagnosis = input("Enter the patient diagnosis: ")
            nurse = input("Enter the nurse name: ")
            add_patient(name, age, sex, drugs, ward, diagnosis, nurse)
        elif choice == '9':
            list_patients()
        elif choice == '10':
            ward = input("Enter the ward name: ")
            list_patients_in_ward(ward)
        elif choice == '11':
            name = input("Enter the patient name: ")
            search_patient(name)
        elif choice == '12':
            patient_name = input("Enter the patient name to discharge: ")
            delete_patient(patient_name)
        elif choice == '13':
            nurse_name = input("Enter the nurse name to delete: ")
            delete_nurse(nurse_name)
        elif choice == '14':
            doctor_name = input("Enter the doctor name to delete: ")
            delete_doctor(doctor_name)
        elif choice == '15':
            print("\nGOODBYE!\n")
            print("\n" + "="*58 + "\n")
            break
        else:
            print("Invalid choice. Please enter a valid number.")


