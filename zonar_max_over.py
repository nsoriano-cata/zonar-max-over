import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file):
    # Read CSV file, skipping the first 4 rows as headers start from row 5
    df = pd.read_csv(file, skiprows=4)
    return df

def process_data(df):
    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Group by date and sum 'Max Over(mph)'
    daily_sum = df.groupby('Date')['Max Over(mph)'].sum().reset_index()
    
    # Format the date as requested (e.g., 9/1/2024)
    daily_sum['Date'] = daily_sum['Date'].dt.strftime('%m/%d/%Y')
    
    return daily_sum

def plot_data(data):
    fig = px.line(data, x='Date', y='Max Over(mph)', 
                  title='Total Max Over(mph) by Date',
                  labels={'Max Over(mph)': 'Total Max Over (mph)'})
    
    fig.update_traces(mode='lines+markers')
    fig.update_layout(hovermode='x unified')
    
    # Customize hover template to show formatted date
    fig.update_traces(hovertemplate='Date: %{x}<br>Total Max Over (mph): %{y:.2f}<extra></extra>')
    
    # Adjust x-axis to show all dates without overlapping
    fig.update_xaxes(tickangle=45)
    
    return fig

def main():
    st.title('CSV Data Analysis and Visualization')

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        processed_data = process_data(data)
        
        st.subheader('Processed Data')
        st.write(processed_data)
        
        fig = plot_data(processed_data)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()