# RMA/RTV Case Management Tool
A prototype supply chain case management tool for analysing return-related transactions and tracking potential RMA/RTV cases.

## Live Demo
[Open the live demo](https://rma-case-tool-1020.streamlit.app/)

## Project Overview
This project transforms return-related transaction data into a structured case management dataset.

The application allows users to review case types, statuses, processing days and potential return values through a Streamlit web interface.

## Features
- View total, RMA and RTV case counts
- Filter cases by case type and status
- Search cases by Case ID
- View individual case details
- Analyse case status distribution
- Compare potential return values by case type
- Store case data in a SQLite database
- Display charts with Plotly

## Technical Implementation
- Used Python and Pandas to clean and transform transaction data
- Identified potential return-related records using cancellation indicators and negative quantities
- Calculated return quantities and potential return values
- Created Case IDs and structured case records
- Used SQLite to store case data in a `cases` table
- Used SQL queries with `COUNT`, `SUM` and `GROUP BY` for case analysis
- Used Streamlit to build the web interface
- Used Plotly to display case status and return value charts

## Technologies
- Python
- Pandas
- SQL
- SQLite
- Streamlit
- Plotly

## Key Results
- 10,624 potential return-related transaction lines
- 8,499 simulated RMA cases
- 2,125 simulated RTV cases
- Potential return values calculated from return quantities and unit prices

## Data Note
The original public dataset did not contain confirmed RMA or RTV information.
Therefore, the RMA/RTV case types, statuses, priorities and processing days were simulated for this prototype.
The results should be interpreted as a demonstration of a supply chain case management workflow, rather than confirmed business records.
