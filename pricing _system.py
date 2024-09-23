import streamlit as st
import numpy as np
from fpdf import FPDF

# Define the base rate
base_rate = 450  # EGP per visit

# Add the title to the main page
st.image("Med Right logo.png")
st.title("In-House Pricing System")

# Sidebar for all configuration inputs
st.sidebar.title("Configuration")

# Sidebar input boxes for the input factors
client_name = st.sidebar.text_input("Client Name", " ")
branches = st.sidebar.number_input("Number of Branches", min_value=1, max_value=10, step=1, value=3)
members = st.sidebar.number_input("Active Members", min_value=1, max_value=40000, step=10, value=100)  # Updated range for members
hours_per_visit = st.sidebar.number_input("Hours per Visit", min_value=1, max_value=24, step=1, value=2)  # Updated range for hours
weekly_visits = st.sidebar.number_input("Weekly Visits", min_value=1, max_value=7, step=1, value=1)
location = st.sidebar.selectbox("Location", options=["Near", "Remote"], index=0)

# Sidebar sliders for management fees and taxes
add_tax = st.sidebar.toggle("Add Tax", value=True)
tax_percentage = st.sidebar.slider("Tax (%)", min_value=5, max_value=30, step=1, value=10)
add_management_fee = st.sidebar.toggle("Add Management Fee", value=True)
management_fee = st.sidebar.slider("Management Fee (%)", min_value=5, max_value=30, step=5, value=10)

# Define a function to assign weights based on the number of active members
def get_member_weight(members):
    if members <= 50:
        return 1.0
    elif 51 <= members <= 100:
        return 1.1
    elif 101 <= members <= 200:
        return 1.2
    elif 201 <= members <= 500:
        return 1.3
    elif 501 <= members <= 1000:
        return 1.4
    elif 1001 <= members <= 5000:
        return 1.5
    elif 5001 <= members <= 10000:
        return 1.6
    elif 10001 <= members <= 20000:
        return 1.7
    elif 20001 <= members <= 40000:
        return 1.8
    else:
        return 1.0

# Define a function to assign weights based on the number of weekly visits
def get_visit_weight(weekly_visits):
    if weekly_visits == 1:
        return 1.0
    elif 2 <= weekly_visits <= 3:
        return 1.15
    elif 4 <= weekly_visits <= 5:
        return 1.35
    else:
        return 1.45

# Define a function to assign weights based on the hours per visit
def get_hour_weight(hours_per_visit):
    if hours_per_visit <= 2:
        return 1.0
    elif 3 <= hours_per_visit <= 4:
        return 1.2
    elif 5 <= hours_per_visit <= 8:
        return 1.4
    elif 9 <= hours_per_visit <= 16:
        return 1.6
    else:
        return 1.8

# Define a function to calculate the total price per visit, including management fees if selected
def calculate_price_per_visit(members, weekly_visits, hours_per_visit, location, add_tax, tax_percentage, add_management_fee, management_fee_percentage):
    # Assign weights based on the inputs
    member_weight = get_member_weight(members)
    visit_weight = get_visit_weight(weekly_visits)
    hour_weight = get_hour_weight(hours_per_visit)
    
    # Location weight remains the same
    if location == "Near":
        location_weight = 1.0
    else:
        location_weight = 1.35
    
    # Add tax to the base rate if selected
    if add_tax:
        adjusted_base_rate = base_rate * (1 + tax_percentage / 100)
    else:
        adjusted_base_rate = base_rate
    
    # Calculate the total price per visit
    total_price_per_visit = adjusted_base_rate * member_weight * visit_weight * hour_weight * location_weight
    
    # Add management fee to the cost per visit if selected
    if add_management_fee:
        total_price_per_visit *= (1 + management_fee_percentage / 100)
    
    return np.round(total_price_per_visit, 2)

# Define a function to calculate the annual cost
def calculate_annual_cost(total_price_per_visit, weekly_visits):
    # Calculate the number of annual visits (48 weeks per year)
    annual_visits = 48 * weekly_visits
    # Calculate the annual cost
    annual_cost = total_price_per_visit * annual_visits
    return np.round(annual_cost, 2)

# Calculate cost per visit, including management fees
cost_per_visit = calculate_price_per_visit(members, weekly_visits, hours_per_visit, location, add_tax, tax_percentage, add_management_fee, management_fee)

# Calculate the total annual cost
annual_cost = calculate_annual_cost(cost_per_visit, weekly_visits)

# Display the client name, cost per visit, and final annual price on the main page
st.write(f"**Client Name:** {client_name}")
st.write(f"**Cost per Visit:**  {cost_per_visit} EGP ")
st.write(f"**Total Annual Cost with MGT:**  {annual_cost} EGP ")
st.write(f"**MGT fees Percentage:**  {management_fee} % ")

