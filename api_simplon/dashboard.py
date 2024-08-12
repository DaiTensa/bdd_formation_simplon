import streamlit as st
import requests
from utils.dpt_region_var import localisation_default

# Define the FastAPI backend URL
backend_url = "http://127.0.0.1:8000"

# Function to fetch formations by department
def get_formations_by_department(departments, skip=0, limit=10):
    # Create a dictionary of query parameters
    params = [("department", dept) for dept in departments]
    params.append(("offset", skip))
    params.append(("limit", limit))
    
    # Send a GET request to the backend to fetch formations by department
    response = requests.get(f"{backend_url}/formations/department/", params=params)
    return response.json()

# Function to fetch formations by formacode
def get_formations_by_formacode(formacodes, skip=0, limit=10):
    # Send a GET request to the backend to fetch formations by formacode
    params = [("formacode", formacode) for formacode in formacodes]
    params.append(("offset", skip))
    params.append(("limit", limit))

    response = requests.get(f"{backend_url}/formations/formacode/", params=params)
    return response.json()

# Function to fetch distinct formacodes
def get_distinct_formacodes():
    # Send a GET request to the backend to fetch distinct formacodes
    response = requests.get(f"{backend_url}/distinct_formacodes/")
    return response.json()

# Streamlit app
st.title("Formations Dashboard")

# Department filter
# Create a dictionary mapping department display names to their codes
departments_dict = {f"{key} - {value['nom']}": key for key, value in localisation_default["departements"].items()}

# Multi-select widget for selecting departments
departments = st.multiselect("Select department codes (e.g., 75):", options=list(departments_dict.keys()))
# Number input for selecting the page number for department formations
department_page = st.number_input("Department Page Number", min_value=1, step=1, value=1)
if st.button("Get Formations by Department"):
    # Get the selected department codes
    selected_departments = [departments_dict[dept] for dept in departments]
    # Calculate the offset for pagination
    skip = (department_page - 1) * 10
    # Fetch formations by department
    formations = get_formations_by_department(selected_departments, skip=skip, limit=10)
    # Display the fetched formations
    st.write(formations)

# Formacode filter
# Fetch distinct formacodes
options_distinct_formacodes = get_distinct_formacodes()
# Multi-select widget for selecting formacodes
formacodes = st.multiselect("Select formacodes:", options=[option["Formacode"] for option in options_distinct_formacodes])
# Number input for selecting the page number for formacode formations
formacode_page = st.number_input("Formacode Page Number", min_value=1, step=1, value=1)
if st.button("Get Formations by Formacode"):
    # Get the selected formacodes
    selected_formacodes = formacodes
    # Calculate the offset for pagination
    skip = (formacode_page - 1) * 10
    # Fetch formations by formacode
    formations = get_formations_by_formacode(selected_formacodes, skip=skip, limit=10)
    # Display the fetched formations
    st.write(formations)