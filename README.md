# Flight Delay Analysis Tool

This is a project created as part of the Masterschool curriculum.

## Overview
This Python project provides an interactive command-line tool for querying and analyzing flight delay data using SQLite. It enables users to:
- Retrieve flight details by ID
- Retrieve flights by a specific date
- Get delayed flights by airline
- Get delayed flights by origin airport

## Features
- Query flight details using an SQLite database
- Identify delayed flights (flights delayed by 20 minutes or more)
- Simple and efficient command-line interface

## Installation
### Prerequisites
- Python 3.x
- SQLite3
- Install dependencies using:

```sh
pip install -r requirements.txt
```

## Usage
Run the tool using:

```sh
python main.py
```

### Menu Options:
1. Show flight by ID
2. Show flights by date
3. Delayed flights by airline
4. Delayed flights by origin airport
5. Exit

## File Structure
```
/Sky-SQL
│── data/
│   ├── flights.sqlite3  # Database file
│── main.py              # Main application logic
│── data.py              # Database interaction layer
│── requirements.txt     # Project dependencies
│── README.md            # Project documentation
```

## Dependencies
The required dependencies are listed in `requirements.txt`. Install them using:

```sh
pip install -r requirements.txt
```

### **Main Dependencies**
- `sqlalchemy` - To interact with the SQLite database

## License
This project is open-source and available for use.

## Acknowledgments
Special thanks to Masterschool for providing the guidance and resources for this project.
