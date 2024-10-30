import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_data(file):
    df = pd.read_csv(file)
    print("Columns:", df.columns)
    print("\nFirst few rows:")
    print(df.head())
    return df

def process_data(df):
    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate daily summaries
    daily_sum = df.groupby('Date')['Max Over(mph)'].sum().reset_index()
    daily_count = df.groupby('Date').agg({
        'Max Over(mph)': lambda x: sum(x > 5)
    }).reset_index()
    daily_count.columns = ['Date', 'Violations_Over_5mph']
    
    # Format dates to M/DD format
    daily_sum['Date'] = daily_sum['Date'].dt.strftime('%-m/%-d')
    daily_count['Date'] = daily_count['Date'].dt.strftime('%-m/%-d')
    
    # Round values
    daily_sum['Max Over(mph)'] = daily_sum['Max Over(mph)'].round(2)
    
    return daily_sum, daily_count

def create_plots(daily_sum, daily_violations):
    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Total Max Over(mph) by Date', 'Daily Count of Violations Over 5mph'),
        vertical_spacing=0.2
    )
    
    # Add first trace - Total Max Over
    fig.add_trace(
        go.Scatter(
            x=daily_sum['Date'],
            y=daily_sum['Max Over(mph)'],
            mode='lines+markers+text',
            text=daily_sum['Max Over(mph)'],
            textposition='top center',
            name='Total Max Over',
            hovertemplate='Date: %{x}<br>Total Max Over (mph): %{y:.2f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add second trace - Violation Counts
    fig.add_trace(
        go.Scatter(
            x=daily_violations['Date'],
            y=daily_violations['Violations_Over_5mph'],
            text=daily_violations['Violations_Over_5mph'],
            mode='lines+markers+text',
            textposition='top center',
            name='Violations > 5mph',
            hovertemplate='Date: %{x}<br>Violations: %{yL.2f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=900,
        showlegend=False,
        margin=dict(t=60, b=50, l=50, r=50)
    )
    
    # Update x-axes
    fig.update_xaxes(tickangle=45, row=1, col=1)
    fig.update_xaxes(tickangle=45, row=2, col=1)
    
    # Update y-axes
    fig.update_yaxes(rangemode='tozero', row=1, col=1)
    fig.update_yaxes(rangemode='tozero', row=2, col=1)
    
    return fig

def main():
    st.title('CSV Data Analysis and Visualization')

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        
        required_columns = ['Date', 'Max Over(mph)']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            st.error(f"Error: The following required columns are missing: {', '.join(missing_columns)}")
            st.write("Available columns:", ', '.join(data.columns))
        else:
            daily_sum, daily_violations = process_data(data)
            
            st.subheader('Speed Analysis')
            col1, col2 = st.columns(2)
            with col1:
                st.write("Daily Total Max Over")
                st.write(daily_sum)
            with col2:
                st.write("Daily Violations > 5mph")
                st.write(daily_violations)
            
            fig = create_plots(daily_sum, daily_violations)
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()