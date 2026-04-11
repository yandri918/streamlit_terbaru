"""
Reusable Altair chart components for data visualization
"""
import altair as alt
import pandas as pd

# Color schemes
COLOR_SCHEME = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#48bb78',
    'danger': '#f56565',
    'warning': '#ed8936',
    'info': '#4299e1',
    'light': '#f7fafc',
    'dark': '#2d3748'
}

def create_line_chart(data, x, y, title="", color=None, width=700, height=400):
    """Create an interactive line chart"""
    chart = alt.Chart(data).mark_line(
        point=True,
        strokeWidth=2
    ).encode(
        x=alt.X(x, title=x.replace('_', ' ').title()),
        y=alt.Y(y, title=y.replace('_', ' ').title()),
        color=alt.value(color) if color else alt.value(COLOR_SCHEME['primary']),
        tooltip=[x, y]
    ).properties(
        width=width,
        height=height,
        title=title
    ).interactive()
    
    return chart

def create_candlestick_chart(data, date_col, open_col, high_col, low_col, close_col, 
                              width=800, height=400):
    """Create a candlestick chart for stock data"""
    # Create the base chart
    base = alt.Chart(data).encode(
        x=alt.X(f'{date_col}:T', title='Date'),
        color=alt.condition(
            f"datum.{open_col} <= datum.{close_col}",
            alt.value(COLOR_SCHEME['success']),
            alt.value(COLOR_SCHEME['danger'])
        )
    )
    
    # High-Low lines
    rule = base.mark_rule().encode(
        y=alt.Y(f'{low_col}:Q', title='Price', scale=alt.Scale(zero=False)),
        y2=f'{high_col}:Q'
    )
    
    # Open-Close bars
    bar = base.mark_bar(size=5).encode(
        y=f'{open_col}:Q',
        y2=f'{close_col}:Q'
    )
    
    chart = (rule + bar).properties(
        width=width,
        height=height,
        title='Stock Price Candlestick Chart'
    ).interactive()
    
    return chart

def create_bar_chart(data, x, y, title="", color=None, width=700, height=400):
    """Create an interactive bar chart"""
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(x, title=x.replace('_', ' ').title()),
        y=alt.Y(y, title=y.replace('_', ' ').title()),
        color=alt.value(color) if color else alt.value(COLOR_SCHEME['primary']),
        tooltip=[x, y]
    ).properties(
        width=width,
        height=height,
        title=title
    ).interactive()
    
    return chart

def create_scatter_plot(data, x, y, color=None, title="", width=700, height=400):
    """Create an interactive scatter plot"""
    chart = alt.Chart(data).mark_circle(size=60).encode(
        x=alt.X(x, title=x.replace('_', ' ').title()),
        y=alt.Y(y, title=y.replace('_', ' ').title()),
        color=color if color else alt.value(COLOR_SCHEME['primary']),
        tooltip=[x, y] + ([color] if color and isinstance(color, str) else [])
    ).properties(
        width=width,
        height=height,
        title=title
    ).interactive()
    
    return chart

def create_histogram(data, column, bins=30, title="", width=700, height=400):
    """Create a histogram"""
    chart = alt.Chart(data).mark_bar(
        opacity=0.7,
        binSpacing=1
    ).encode(
        x=alt.X(f'{column}:Q', bin=alt.Bin(maxbins=bins), 
                title=column.replace('_', ' ').title()),
        y=alt.Y('count()', title='Frequency'),
        color=alt.value(COLOR_SCHEME['primary']),
        tooltip=['count()']
    ).properties(
        width=width,
        height=height,
        title=title
    ).interactive()
    
    return chart

def create_heatmap(data, x, y, color, title="", width=600, height=500):
    """Create a correlation heatmap"""
    chart = alt.Chart(data).mark_rect().encode(
        x=alt.X(f'{x}:O', title=''),
        y=alt.Y(f'{y}:O', title=''),
        color=alt.Color(f'{color}:Q', 
                       scale=alt.Scale(scheme='redblue', domain=[-1, 1]),
                       title='Correlation'),
        tooltip=[x, y, color]
    ).properties(
        width=width,
        height=height,
        title=title
    )
    
    return chart

def create_area_chart(data, x, y, title="", color=None, width=700, height=400):
    """Create an area chart"""
    chart = alt.Chart(data).mark_area(
        opacity=0.7,
        line=True
    ).encode(
        x=alt.X(x, title=x.replace('_', ' ').title()),
        y=alt.Y(y, title=y.replace('_', ' ').title()),
        color=alt.value(color) if color else alt.value(COLOR_SCHEME['primary']),
        tooltip=[x, y]
    ).properties(
        width=width,
        height=height,
        title=title
    ).interactive()
    
    return chart

def create_multi_line_chart(data, x, y_columns, title="", width=700, height=400):
    """Create a multi-line chart for comparing multiple metrics"""
    # Melt the dataframe for multiple lines
    melted = data.melt(id_vars=[x], value_vars=y_columns, 
                       var_name='Metric', value_name='Value')
    
    chart = alt.Chart(melted).mark_line(point=True).encode(
        x=alt.X(f'{x}:T', title='Date'),
        y=alt.Y('Value:Q', title='Value'),
        color=alt.Color('Metric:N', 
                       scale=alt.Scale(range=[COLOR_SCHEME['primary'], 
                                             COLOR_SCHEME['warning'],
                                             COLOR_SCHEME['success']])),
        tooltip=[x, 'Metric', 'Value']
    ).properties(
        width=width,
        height=height,
        title=title
    ).interactive()
    
    return chart

def create_boxplot(data, x, y, title="", width=700, height=400):
    """Create a box plot"""
    chart = alt.Chart(data).mark_boxplot(
        size=40,
        color=COLOR_SCHEME['primary']
    ).encode(
        x=alt.X(f'{x}:N', title=x.replace('_', ' ').title()),
        y=alt.Y(f'{y}:Q', title=y.replace('_', ' ').title()),
        tooltip=[x, y]
    ).properties(
        width=width,
        height=height,
        title=title
    )
    
    return chart
