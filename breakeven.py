import streamlit as st
import matplotlib.pyplot as plt

# Function to calculate breakeven point
def calculate_breakeven(sales_price, variable_cost, fixed_cost):
    breakeven_quantity = fixed_cost / (sales_price - variable_cost)
    breakeven_amount = breakeven_quantity * sales_price
    return breakeven_quantity, breakeven_amount

# Function to calculate target quantity for desired profit
def calculate_target_quantity(sales_price, variable_cost, fixed_cost, desired_profit):
    target_quantity = (fixed_cost + desired_profit) / (sales_price - variable_cost)
    return target_quantity

# Streamlit user interface
st.title("Breakeven Point and Target Quantity Calculator")

# Input fields
sales_price = st.number_input("Sales Price per Unit", min_value=0.0, step=0.01)
variable_cost = st.number_input("Variable Cost per Unit", min_value=0.0, step=0.01)
fixed_cost = st.number_input("Fixed Cost", min_value=0.0, step=0.01)
desired_profit = st.number_input("Desired Profit", min_value=0.0, step=0.01)

# Calculate breakeven point
if sales_price > 0 and variable_cost > 0 and fixed_cost > 0:
    breakeven_quantity, breakeven_amount = calculate_breakeven(sales_price, variable_cost, fixed_cost)

    # Display breakeven results
    st.write(f"Breakeven Point (Quantity): {breakeven_quantity:.2f} units")
    st.write(f"Breakeven Point (Amount): ${breakeven_amount:.2f}")

    # Calculate target quantity for desired profit
    if desired_profit > 0:
        target_quantity = calculate_target_quantity(sales_price, variable_cost, fixed_cost, desired_profit)
        st.write(f"Target Quantity for Desired Profit (${desired_profit}): {target_quantity:.2f} units")

        # Plotting the breakeven and target quantity graph
        quantities = range(int(target_quantity) + 20)  # Extended range to include target quantity
    else:
        # Plotting only the breakeven graph if desired profit is not provided
        quantities = range(int(breakeven_quantity) * 2)

    total_cost = [fixed_cost + variable_cost * q for q in quantities]
    total_revenue = [sales_price * q for q in quantities]

    plt.figure(figsize=(10, 6))
    plt.plot(quantities, total_cost, label='Total Cost')
    plt.plot(quantities, total_revenue, label='Total Revenue')
    plt.axvline(breakeven_quantity, color='r', linestyle='--', label='Breakeven Point')
    plt.axhline(breakeven_amount, color='g', linestyle='--')

    if desired_profit > 0:
        plt.axvline(target_quantity, color='b', linestyle='--', label='Target Quantity')
    
    plt.xlabel('Quantity')
    plt.ylabel('Amount ($)')
    plt.title('Breakeven and Target Quantity Analysis')
    plt.legend()
    plt.grid(True)

    # Display the plot
    st.pyplot(plt.gcf())
else:
    st.write("Please enter positive values for sales price, variable cost, and fixed cost.")
