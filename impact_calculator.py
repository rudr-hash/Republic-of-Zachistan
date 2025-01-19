import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calculate_metrics(adoption_rate):
    # Constants from the data
    TOTAL_POTENTIAL_LIVES = 14227
    CHILDREN_POTENTIAL_LIVES = 9647
    ADULT_POTENTIAL_LIVES = 4580
    
    # Cost constants (in USD)
    HUFFSTATIN_TOTAL_COST = 3329170
    CLAIRADOL_TOTAL_COST = 3348239
    COST_DIFFERENCE = CLAIRADOL_TOTAL_COST - HUFFSTATIN_TOTAL_COST  # Should be 19069
    
    # Age group costs with Huffstatin
    HUFFSTATIN_CHILDREN_COST = 2407888
    HUFFSTATIN_ADULT_COST = 921283
    
    # Age group costs with Clairadol
    CLAIRADOL_CHILDREN_COST = 2182241
    CLAIRADOL_ADULT_COST = 1165998
    
    # Calculate based on adoption rate
    actual_rate = adoption_rate / 100
    
    # Lives saved calculations
    lives_saved = {
        'children': round(CHILDREN_POTENTIAL_LIVES * actual_rate),
        'adults': round(ADULT_POTENTIAL_LIVES * actual_rate),
        'total': round(TOTAL_POTENTIAL_LIVES * actual_rate)
    }
    
    # Cost calculations
    costs = {
        'huffstatin': {
            'total': HUFFSTATIN_TOTAL_COST * (1 - actual_rate),
            'children': HUFFSTATIN_CHILDREN_COST * (1 - actual_rate),
            'adults': HUFFSTATIN_ADULT_COST * (1 - actual_rate)
        },
        'clairadol': {
            'total': CLAIRADOL_TOTAL_COST * actual_rate,
            'children': CLAIRADOL_CHILDREN_COST * actual_rate,
            'adults': CLAIRADOL_ADULT_COST * actual_rate
        }
    }
    
    total_cost = costs['huffstatin']['total'] + costs['clairadol']['total']
    
    # Calculate cost per life saved with proper precision
    cost_per_life_saved = (COST_DIFFERENCE * actual_rate) / lives_saved['total'] if lives_saved['total'] > 0 else 0
    baseline_cost_per_life = COST_DIFFERENCE / TOTAL_POTENTIAL_LIVES  # Should be 1.34
    
    return lives_saved, costs, total_cost, cost_per_life_saved, COST_DIFFERENCE, baseline_cost_per_life

def create_lives_saved_chart(lives_saved):
    fig = go.Figure(data=[
        go.Bar(name='Current Lives Saved', 
               x=['Children', 'Adults'], 
               y=[lives_saved['children'], lives_saved['adults']],
               marker_color=['rgb(59, 130, 246)', 'rgb(16, 185, 129)']),
        go.Bar(name='Potential at 100%', 
               x=['Children', 'Adults'], 
               y=[9647, 4580],
               marker_color='rgb(229, 231, 235)')
    ])
    
    fig.update_layout(
        title='Lives Saved by Age Group',
        barmode='group',
        height=400
    )
    
    return fig

def create_cost_chart(costs):
    fig = go.Figure(data=[
        go.Bar(name='Huffstatin Cost', 
               x=['Children', 'Adults'], 
               y=[costs['huffstatin']['children'], costs['huffstatin']['adults']],
               marker_color='rgb(251, 191, 36)'),
        go.Bar(name='Clairadol Cost', 
               x=['Children', 'Adults'], 
               y=[costs['clairadol']['children'], costs['clairadol']['adults']],
               marker_color='rgb(239, 68, 68)')
    ])
    
    fig.update_layout(
        title='Treatment Costs by Age Group',
        barmode='group',
        height=400
    )
    
    return fig

def main():
    st.set_page_config(page_title="Clairadol Impact Calculator", layout="wide")
    
    st.title("Clairadol Impact Calculator for Zachistan")
    
    # Sidebar
    st.sidebar.header("Settings")
    adoption_rate = st.sidebar.slider(
        "Clairadol Adoption Rate (%)",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
    )
    
    # Calculate metrics
    lives_saved, costs, total_cost, cost_per_life_saved, cost_difference, baseline_cost_per_life = calculate_metrics(adoption_rate)
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Children's Lives Saved", f"{lives_saved['children']:,}")
    with col2:
        st.metric("Adult Lives Saved", f"{lives_saved['adults']:,}")
    with col3:
        st.metric("Total Lives Saved", f"{lives_saved['total']:,}")
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["Lives Saved Analysis", "Cost Analysis"])
    
    with tab1:
        st.plotly_chart(create_lives_saved_chart(lives_saved), use_container_width=True)
        
        st.subheader("Mortality Reduction Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.info("Children mortality reduction: 2.4% (10.9% → 8.5%)")
        with col2:
            st.info("Adult mortality reduction: 7.0% (22% → 15%)")
    
    with tab2:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Treatment Cost", f"${total_cost:,.2f}")
        with col2:
            st.metric("Additional Cost", f"${(cost_difference * adoption_rate/100):,.2f}")
        with col3:
            st.metric("Cost per Life Saved", f"${cost_per_life_saved:.2f}")  # Ensuring 2 decimal places
        
        st.plotly_chart(create_cost_chart(costs), use_container_width=True)
        
        st.subheader("Cost Analysis Details")
        st.info(f"""
        - Base cost difference: ${cost_difference:,.2f}
        - Cost per life saved at 100% adoption: ${baseline_cost_per_life:.2f}
        - Total potential lives saved: 14,227
        """)

if __name__ == "__main__":
    main()
