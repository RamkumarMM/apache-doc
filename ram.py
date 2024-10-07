import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

## Sample Node MDS Data ##
df = pd.read_excel("sample_data.xlsx", sheet_name="MDS")
html_table = df.to_html()

## Sample Utilization Data  (CPU, Memory, Disk uage ##
df_util = pd.read_excel("sample_data.xlsx", sheet_name="Utilization")
df_util['Time'] = pd.to_datetime(df_util['Time'])

## Sample Incident data ##
df_ticket = pd.read_excel("sample_data.xlsx", sheet_name="Ticket")
df_ticket['Time'] = pd.to_datetime(df_ticket['Time'])

## Sample AAAS Data ##
df_aaas = pd.read_excel("sample_data.xlsx", sheet_name="AAAS")
df_aaas['Time'] = pd.to_datetime(df_aaas['Time'])

## Sample SNOW Change Data ##
df_change = pd.read_excel("sample_data.xlsx", sheet_name="Change")
df_change['Time'] = pd.to_datetime(df_change['Time'])

## Sample Config Mgmt Data ##
df_config = pd.read_excel("sample_data.xlsx", sheet_name="Config")
df_config['Time'] = pd.to_datetime(df_config['Time'])

# Create a figure with the original data (line chart for df1)
fig = go.Figure()

# Add line traces for CPU, Memory, and Disk from df1
fig.add_trace(go.Scatter(x=df_util['Time'], y=df_util['CPU'], mode='lines', name='CPU Usage'))
fig.add_trace(go.Scatter(x=df_util['Time'], y=df_util['Memory'], mode='lines', name='Memory Usage'))
fig.add_trace(go.Scatter(x=df_util['Time'], y=df_util['Disk'], mode='lines', name='Disk Usage'))

# Now map the incidents to the CPU values (or any other metric like Memory, Disk)
# For simplicity, I will plot the incidents as dots on the CPU line
# Below code will represent as DOT 
"""
fig.add_trace(go.Scatter(x=df_ticket['Time'], y=[10] * len(df_ticket['Time']),  # Y-value corresponds to CPU usage at 10
                         mode='markers+text', name='Incidents',
                         text=df_ticket['INC_NO'], textposition="top center",
                         marker=dict(size=10, color='red')))
"""

# Below code will represent as BAR
 # Add bar traces for Incidents (df2)
fig.add_trace(go.Bar(x=df_ticket['Time'], y=[15] * len(df_ticket),  # Arbitrary y-value for the height of the bars
                     name='Incidents', text=df_ticket['INC_NO'], textposition='auto',
                     marker=dict(color='rgba(255, 0, 0, 0.6)', line=dict(color='rgba(255, 0, 0, 1.0)', width=1))))


# Add MS_ID markers from df_aaas (Mapping to CPU line for simplicity, you can change it)
fig.add_trace(go.Scatter(x=df_aaas['Time'], y=[10] * len(df_aaas['Time']),  # Mapping to CPU (value 10)
                         mode='markers+text', name='MS_IDs',
                         text=df_aaas['MS_ID'], textposition="bottom center",
                         marker=dict(size=10, color='blue')))

# Add SNOW Change markers from df_change (Mapping to CPU line for simplicity, you can change it)
fig.add_trace(go.Scatter(x=df_change['Time'], y=[10] * len(df_change['Time']),  # Mapping to CPU (value 10)
                         mode='markers+text', name='CHG_NO',
                         text=df_change['CHG_NO'], textposition="bottom center",
                         marker=dict(size=10, color='pink')))

# Add ConfigMgmt markers from df_config (Mapping to CPU line for simplicity, you can change it)
fig.add_trace(go.Scatter(x=df_config['Time'], y=[10] * len(df_config['Time']),  # Mapping to CPU (value 10)
                         mode='markers+text', name='Config_Resource',
                         text=df_config['Config_Resource'], textposition="bottom center",
                         marker=dict(size=10, color='orange')))

# Customize layout
fig.update_layout(title='Resource Usage with Incident, AAAS Exection',
                  xaxis_title='Time',
                  yaxis_title='Usage (CPU, Memory, Disk)',
                  barmode='overlay',  ## This will play a bar for INCIDENT in the chart 
                  template='plotly_white')

# Get the raw HTML for the chart
chart_html = pio.to_html(fig, full_html=False)


# Full HTML structure including both the table and chart
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>DataFrame and Chart</title>
    <style>
        table {{
            width: 50%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 18px;
            text-align: left;
        }}
        th, td {{
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            text-align: center;
            border-bottom: 2px solid black;
        }}
        tr:hover {{background-color: #f5f5f5;}}
    </style>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h2><u>Server Details</u></h2>
    <br>
    {html_table}
    <br>
    <h2><u>Sample Chart</u></h2>
    <h2>Chart with Utiliation, Incidents, Change, AAAS & Config Mgmt Data</h2>
    {chart_html}
</body>
</html>
"""

# Write to an HTML file
with open("DemoPage.html", "w") as file:
    file.write(html_content)