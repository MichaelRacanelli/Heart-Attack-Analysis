import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def pie_chart(data, input):
    # Generate the pie chart using Plotly
    fig = px.pie(
        data, 
        names=input, 
        title=f'{input}', 
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_traces(
        textinfo='percent+label', 
        hoverinfo='label+percent',
        pull=[0.05]*len(data[input].unique())
    )
    fig.update_layout(title_font_size=20)
    return fig

def pie_split(data, input, target):
    # Split data into subgroups and create pie charts
    unique_targets = data[target].unique()
    colors = px.colors.qualitative.Pastel  # Specify a specific color sequence
    
    # Create a consistent color map for the unique values of the input column
    unique_values = data[input].unique()
    color_map = {val: colors[j % len(colors)] for j, val in enumerate(unique_values)}
    
    fig = make_subplots(
        rows=1, 
        cols=len(unique_targets), 
        specs=[[{'type':'domain'}]*len(unique_targets)],
        subplot_titles=[f'{target}: {val}' for val in unique_targets]
    )
    
    for i, value in enumerate(unique_targets):
        subset = data[data[target] == value]
        fig.add_trace(
            go.Pie(
                labels=subset[input].value_counts().index,
                values=subset[input].value_counts().values,
                name=f'{target}: {value}',
                pull=[0.05]*len(subset[input].unique()),
                marker=dict(colors=[color_map[val] for val in subset[input].value_counts().index])
            ),
            row=1,
            col=i+1
        )

    fig.update_layout(
        title_text=f'{input}',
        title_font_size=20,
        annotations=[
            dict(text=f'{target}: {val}', x=0.5/len(unique_targets)*(2*i+1), y=1.1, showarrow=False) 
            for i, val in enumerate(unique_targets)
        ]
    )
    return fig

def bar_chart(data, input):
    # Create bar chart using Plotly Express
    value_counts = data[input].value_counts().reset_index()
    value_counts.columns = [input, 'count']
    fig = px.bar(
        value_counts,
        x=input,
        y='count',
        labels={input: input, 'count': 'Count'},
        title=f'{input}',
        color=input,  # Use the input column to assign different colors
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        title_font_size=20,
        xaxis_title=f'{input}',
        yaxis_title='Count'
    )
    return fig

def bar_split(data, input, target):
    # Create grouped bar chart using Plotly Express
    fig = px.histogram(
        data,
        x=input,
        color=target,
        barmode='group',
        title=f'{input}',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(
        title_font_size=20,
        xaxis_title=f'{input}',
        yaxis_title='Count'
    )
    return fig
