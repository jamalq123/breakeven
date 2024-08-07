import streamlit as st
import numpy as np
from scipy.optimize import newton
import matplotlib.pyplot as plt

# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Valuation", "Breakeven Point", "WACC and Cost of Equity Calculator", "Bond Valuation"])

# Valuation Section
if section == "Valuation":
    st.title("Financial Metrics Calculator")

    # Inputs for FCFF of Year 0 and the next five years
    st.header("Input Free Cash Flow to Firm (FCFF) for Year 0 and the Next Five Years")
    fcff = []
    fcff.append(st.number_input("Year 0 FCFF (Initial Investment)", value=0.0))
    for i in range(1, 6):
        fcff.append(st.number_input(f"Year {i} FCFF", value=0.0))

    # Input for perpetuity growth rate and discount rate
    st.header("Input Growth Rate (g) and Discount Rate (r)")
    g = st.number_input("Growth Rate (g)", value=0.0)
    r = st.number_input("Discount Rate (r)", value=0.0)

    # Input for current year cash and most liquid assets, and current year bank loan
    st.header("Input Current Year Financial Data")
    current_cash = st.number_input("Current Year Cash and Bank", value=0.0)
    most_liquid_assets = st.number_input("Most Liquid Assets", value=0.0)
    current_bank_loan = st.number_input("Current Year Bank Loan", value=0.0)
    outstanding_shares = st.number_input("Outstanding Shares", value=1)

    # Calculate Perpetuity Value based on the 5th year FCFF
    perpetuity_value = fcff[-1] * (1 + g) / (r - g) if r != g else 0

    # Calculate NPV
    npv = sum([fcff[i] / (1 + r) ** i for i in range(1, 6)]) + perpetuity_value / (1 + r) ** 5 - fcff[0]

    # Function to calculate IRR
    def calculate_irr(fcff, perpetuity_value):
        def npv_func(rate):
            return sum([fcff[i] / (1 + rate) ** i for i in range(1, 6)]) + perpetuity_value / (1 + rate) ** 5 - fcff[0]
        try:
            irr = newton(npv_func, 0.1)
        except RuntimeError:
            irr = np.nan
        return irr

    # Calculate IRR
    irr = calculate_irr(fcff, perpetuity_value)

    # Calculate Profitability Index
    initial_investment = abs(fcff[0])
    profitability_index = (npv + initial_investment) / initial_investment if initial_investment != 0 else np.nan

    # Calculate Equity Value and Fair Value per Share
    equity_value = current_cash + most_liquid_assets - current_bank_loan + npv
    fair_value_per_share = equity_value / outstanding_shares if outstanding_shares != 0 else np.nan

    # Display Results
    st.header("Results")
    st.write(f"Perpetuity Value: ${perpetuity_value:,.2f}")
    st.write(f"Net Present Value (NPV): ${npv:,.2f}")
    st.write(f"Internal Rate of Return (IRR): {irr:.2%}")
    st.write(f"Profitability Index: {profitability_index:.2f}")
    st.write(f"Equity Value: ${equity_value:,.2f}")
    st.write(f"Fair Value per Share: ${fair_value_per_share:,.2f}")

# Breakeven Point Section
elif section == "Breakeven Point":
    st.title("Breakeven Point and Target Quantity Calculator")

    # Input fields
    sales_price = st.number_input("Sales Price per Unit", min_value=0.0, step=0.01)
    variable_cost = st.number_input("Variable Cost per Unit", min_value=0.0, step=0.01)
    fixed_cost = st.number_input("Fixed Cost", min_value=0.0, step=0.01)
    desired_profit = st.number_input("Desired Profit", min_value=0.0, step=0.01)

    # Function to calculate breakeven point
    def calculate_breakeven(sales_price, variable_cost, fixed_cost):
        breakeven_quantity = fixed_cost / (sales_price - variable_cost)
        breakeven_amount = breakeven_quantity * sales_price
        return breakeven_quantity, breakeven_amount

    # Function to calculate target quantity for desired profit
    def calculate_target_quantity(sales_price, variable_cost, fixed_cost, desired_profit):
        target_quantity = (fixed_cost + desired_profit) / (sales_price - variable_cost)
        return target_quantity

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

# WACC and Cost of Equity Section
elif section == "WACC and Cost of Equity Calculator":
    st.title("WACC and Cost of Equity Calculator")

    # CAPM Parameters
    rf = st.number_input("Risk-free Rate (Rf)", value=0.03, min_value=0.0, max_value=1.0, format="%.5f")
    beta = st.number_input("Beta (β)", value=1.0, min_value=0.0, max_value=10.0, format="%.5f")
    rm = st.number_input("Expected Market Return (Rm)", value=0.08, min_value=0.0, max_value=1.0, format="%.5f")

    # WACC Parameters
    E = st.number_input("Market Value of Equity (E)", value=1000000.0, min_value=0.0)
    D = st.number_input("Market Value of Debt (D)", value=500000.0, min_value=0.0)
    rd = st.number_input("Cost of Debt (Rd)", value=0.05, min_value=0.0, max_value=1.0, format="%.5f")
    tax_rate = st.number_input("Corporate Tax Rate", value=0.21, min_value=0.0, max_value=1.0, format="%.5f")

    # Calculate Cost of Equity using CAPM
    def calculate_cost_of_equity(rf, beta, rm):
        return rf + beta * (rm - rf)

    # Calculate WACC
    def calculate_wacc(E, D, re, rd, tax_rate):
        V = E + D
        wacc = (E / V) * re + (D / V) * rd * (1 - tax_rate)
        return wacc

    if st.button("Calculate"):
        cost_of_equity = calculate_cost_of_equity(rf, beta, rm)
        wacc = calculate_wacc(E, D, cost_of_equity, rd, tax_rate)

        st.write(f"Cost of Equity (Re) using CAPM: {cost_of_equity:.2f}")
        st.write(f"Weighted Average Cost of Capital (WACC): {wacc:.2f}")

# Bond Valuation Section
elif section == "Bond Valuation":
    st.title("Bond Valuation Calculator")

    def calculate_bond_value(face_value, coupon_rate, market_rate, years, frequency):
        # Calculate the coupon payment
        periods = {'Yearly': 1, 'Half-Yearly': 2, 'Quarterly': 4}
        n_periods = periods[frequency]
        coupon_payment = face_value * coupon_rate / n_periods
        bond_value = 0
        
        # Calculate the present value of the coupon payments
        for t in range(1, years * n_periods + 1):
            bond_value += coupon_payment / (1 + market_rate / n_periods) ** t
        
        # Calculate the present value of the face value
        bond_value += face_value / (1 + market_rate / n_periods) ** (years * n_periods)
        
        return bond_value

    # Input fields
    face_value = st.number_input("Face Value", value=1000.0)
    coupon_rate = st.number_input("Coupon Rate (in %)", value=5.0) / 100
    market_rate = st.number_input("Market Rate (in %)", value=3.0) / 100
    years = st.number_input("Number of Years", value=10, min_value=1)
    frequency = st.selectbox("Coupon Payment Frequency", ['Yearly', 'Half-Yearly', 'Quarterly'])

    # Calculate bond value
    if st.button("Calculate Bond Value"):
        bond_value = calculate_bond_value(face_value, coupon_rate, market_rate, years, frequency)
        st.write(f"The value of the bond is: ${bond_value:.2f}")
