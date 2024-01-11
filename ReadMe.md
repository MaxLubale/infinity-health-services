# Infinity Health Services

Welcome to Infinity Health Services! This command-line interface (CLI) allows you to manage information related to doctors, nurses, patients, and wards in a healthcare setting.

## Getting Started

To use Infinity Health Services, follow the instructions below.

### Prerequisites

- Python 3.10.12
- SQLAlchemy

### Installation

1. Clone the repository:
  - git clone https://github.com/MaxLubale/infinity-health-services

2. Change into the project directory:
  - cd infinity-health-services

3. Install the required dependencies:
  - pipenv install

4. Initialize the database:
  - python app.py initdb


## Usage
### Command-Line Interface

* The command-line interface provides various commands to interact with the healthcare database.

    - (infinity-health-services) max@max-HP-EliteBook-840-G5:~/path/to/infinity-health-services$ python3 app.py

* For a list of available commands, run:

    - python3 app.py 

### Examples
 * List all doctors:

    - press option 5
 * Add a patient:

   - press option 8: Name: Harry Styles    Age: 35   Sex: Male   Drugs: Aspirin, Ibuprofen  Ward: St Luke   Diagnosis: Heart Disease

 * Search for a specific patient:

   - press option 11: search-patient Nmae: Harry Styles
   
 * Note
   - Replace python3 with your specific Python version.

## Author
  - Name : MAXWELL CLIFF LUBALE
  - Github : https://github.com/MaxLubale

## License
 - This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
  - The Infinity Health Services CLI is built using Click.

## Feel free to contribute, report issues, or suggest improvements!

## Happy Coding!