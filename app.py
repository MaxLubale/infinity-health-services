import click
import tabulate 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabulate import tabulate as tabulate_module 
from tabulate import tabulate as tabulate_function
from lib.base import Base
from lib.doctor import Doctor
from lib.nurse import Nurse
from lib.patient import Patient
from lib.ward import Ward



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
    


    

def print_table(records, headers):
    rows = []
    for record in records:
        row_data = []
        for header in headers:
            if header.lower() == 'id':
                value = getattr(record, 'id', '')
            elif header.lower() == 'ward':
                
                ward_obj = getattr(record, 'ward', None)
                value = getattr(ward_obj, 'name', '') if ward_obj else ''
            elif hasattr(record, header.lower()):
                value = getattr(record, header.lower())
            else:
                value = ''
            row_data.append(value)

        rows.append(row_data)

    click.echo(tabulate.tabulate(rows, headers, tablefmt="grid"))
  

@cli.command()
def initdb():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)
    click.echo(click.style(f'Initialized the database.', fg='green'))

@cli.command()
@click.argument('name')
def add_ward(name):
    """Add a ward."""
    ward = Ward(name=name)
    session.add(ward)
    session.commit()
    click.echo(click.style(f'Ward {name} added successfully.', fg='green'))

@cli.command()
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


@cli.command()
@click.argument('name')
@click.argument('age', type=int)
def add_doctor(name, age):
    """Add a doctor."""
    doctor = Doctor(name=name, age=age)
    session.add(doctor)
    session.commit()
    click.echo(click.style(f'Doctor {name} added successfully.', fg='green'))

@cli.command()
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
@cli.command()
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

@cli.command()
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
@cli.command()
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

@cli.command()
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





@cli.command()
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

@cli.command()
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



@cli.command()
@click.argument('patient_name')
def delete_patient(patient_name):
    """Delete a patient by name."""
    patient = session.query(Patient).filter_by(name=patient_name).first()

    if not patient:
        click.echo(f'Patient with name {patient_name} not found.')
        return

    session.delete(patient)
    session.commit()
    click.echo(click.style(f'Patient with name {patient_name} deleted successfully.', fg='green'))


@cli.command()
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


@cli.command()
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
    cli()
    
