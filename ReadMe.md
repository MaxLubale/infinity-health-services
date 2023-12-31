# Infinity Health Services

Welcome to Infinity Health Services! This command-line interface (CLI) allows you to manage information related to doctors, nurses, patients, and wards in a healthcare setting.

## Getting Started

To use Infinity Health Services, follow the instructions below.

### Prerequisites

- Python 3.x
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

    - python3 app.py list-doctors

 * Add a patient:

   - python3 app.py add-patient --name "Harry Styles" --age 35 --sex "Male" --drugs "Aspirin, Ibuprofen" --ward "St Luke" --diagnosis "Heart Disease"

 * Search for a specific patient:

   - python3 app.py search-patient "Harry Styles"
   
 * Note
   - Replace python3 with your specific Python version.

## License
 - This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
  - The Infinity Health Services CLI is built using Click.

## Feel free to contribute, report issues, or suggest improvements!

## Happy Coding!