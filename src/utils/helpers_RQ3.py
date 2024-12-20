import numpy as np
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import gzip
import plotly.graph_objects as go
from matplotlib.dates import DateFormatter, YearLocator
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors
from scipy import stats

## Codes for RQ3.1

# THIS COLOR MAPPING IS USED TRHOUGH THE ENTIRE PLOTS SO THAT NO CONFUSION IS MADE
def create_color_mapping(df, color_scale):

    # Get categories ordered by their frequency - aligned with RQ3.1 data
    category_counts = df['category_cc'].value_counts()
    ordered_categories = category_counts.index.tolist()
    n_colors = len(ordered_categories)
    
    # Generate colors using the provided colorscale
    colors = plotly.colors.sample_colorscale(color_scale, [i/(n_colors-1) for i in range(n_colors)])
    
    # Create the color mapping based on frequency order from RQ3.1
    color_map = dict(zip(ordered_categories, colors))
    
    return color_map, colors

# Bar charts
def plot_category_distribution(df, color_map):
    category_counts = df['category_cc'].value_counts()
    category_percentages = (category_counts / len(df) * 100).round(2)
    
    plot_df = pd.DataFrame({
        'Category': category_percentages.index,
        'Percentage': category_percentages.values
    })
    
    fig = px.bar(
        plot_df,
        x='Category',
        y='Percentage',
        color='Category',
        color_discrete_sequence=[color_map[cat] for cat in plot_df['Category']],
        text=plot_df['Percentage'].apply(lambda x: f'{x:.1f}%')
    )
    
    fig.update_layout(
        title='Distribution of Categories (%)',
        xaxis_title='Category',
        yaxis_title='Percentage (%)',
        showlegend=False,
        xaxis_tickangle=-45,
        width=800,
        height=500
    )
    
    fig.update_traces(
        textposition='outside',
        textfont=dict(size=12)
    )
    
    return fig

# Pie charts
def plot_monetization_shares(df, columns, color_map):

    # Get categories in the same order as color_map
    ordered_categories = list(color_map.keys())
    
    # Calculate pie data
    pies_data = []
    for column in columns:
        temp_df = df[df[column]==True]
        counts = temp_df[["category_cc", column]].value_counts(normalize=True)
        counts.index = counts.index.droplevel(column)
        pies_data.append(counts)
    
    titles = {
        "has_merchandise": "Merchandise",
        "has_affiliate": "Affiliation",
        "has_sponsorships": "Sponsorship"
    }
    
    fig = make_subplots(
        rows=2, cols=3,
        specs=[
            [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
            [{'type': 'xy', 'colspan': 3}, None, None]
        ],
        row_heights=[0.8, 0.2],
        vertical_spacing=0.1
    )
    
    # Add pie charts
    for idx, (pie_data, column) in enumerate(zip(pies_data, columns)):
        present_categories = pie_data.index
        values = pie_data.values * 100
        pie_colors = [color_map[cat] for cat in present_categories]
        
        fig.add_trace(
            go.Pie(
                values=values,
                labels=present_categories,
                name=titles[column],
                marker=dict(colors=pie_colors),
                hovertemplate="<b>%{label}</b><br>" +
                             "Percentage: %{value:.1f}%<br>" +
                             "<extra></extra>",
                textinfo='percent',
                textposition='auto',
                showlegend=False,
                title=dict(
                    text=titles[column],
                    position="top center"
                )
            ),
            row=1, col=idx+1
        )
    
    # Create color legend as a horizontal bar chart using ordered_categories
 
    #fig.add_trace(
    #    go.Bar(
    #        x=ordered_categories,  # Use ordered categories here
    #        y=[1] * len(ordered_categories),
    #        marker_color=[color_map[cat] for cat in ordered_categories],  # Colors in the same order
    #        showlegend=False,
    #        hovertemplate="Category: %{x}<extra></extra>"
    #    ),
    #    row=2, col=1
    #)


    
    fig.update_layout(
        title_text="Channel Category Monetization Strategies Shares",
        title_x=0.5,
        height=400,
        width=650,
        margin=dict(t=80, b=100, l=50, r=50)
    )
    
    fig.update_xaxes(
        row=2, col=1,
        tickangle=45,
        title_text="Channel Categories",
        tickfont=dict(size=10)
    )
    fig.update_yaxes(
        row=2, col=1,
        visible=False,
        showticklabels=False,
        range=[0, 1]
    )
    
    fig.update_traces(
        textfont_size=12,
        selector=dict(type='pie')
    )
    
    return fig

def plot_stacked_distributions(data, color_map):

    # Create figure 
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=('Merch Frequency', 'Sponsorship Frequency', 'Affiliate Frequency', ''),
        horizontal_spacing=0.08,
        vertical_spacing=0.2,
        row_heights=[0.85, 0.15],  # Slightly reduced height for legend
        specs=[
            [{'type': 'xy'}, {'type': 'xy'}, {'type': 'xy'}],
            [{'type': 'xy', 'colspan': 3}, None, None]
        ]
    )

    # Monetization types from Youtube API
    types = ['merch_frequency', 'sponsorship_frequency', 'affiliate_frequency']
    
    # Create histograms for each type
    for idx, type_name in enumerate(types, 1):
        categories = list(color_map.keys())
        
        for category in categories:
            cat_data = data[
                (data['category_cc'] == category) & 
                (data[type_name] > 0)
            ]
            
            histogram = go.Histogram(
                x=cat_data[type_name],
                name=category,
                marker_color=color_map[category],
                showlegend=False,
                opacity=0.75,
                nbinsx=30,
                autobinx=False,
                xbins=dict(
                    start=0,
                    end=1,
                    size=1/30
                )
            )
            
            fig.add_trace(histogram, row=1, col=idx)

    # Add legend as a compact bar chart
    fig.add_trace(
        go.Bar(
            x=list(color_map.keys()),
            y=[0.3] * len(color_map),  # Reduced height of bars
            marker_color=list(color_map.values()),
            showlegend=False,
            hovertemplate="Category: %{x}<extra></extra>",
            width=0.7  # Make bars narrower
        ),
        row=2, col=1
    )

    # Update layout 
    for i in range(1, 4):
        fig.update_yaxes(
            type='log',
            range=[0, 4],
            title_text='Frequency (log scale)' if i == 1 else '',
            row=1, col=i
        )
        
        fig.update_xaxes(
            title_text='Frequency',
            range=[0, 1],
            dtick=0.2,
            row=1, col=i
        )

    # Update legend bar appearance
    fig.update_xaxes(
        row=2, col=1,
        tickangle=45,
        title_text="Channel Categories",
        tickfont=dict(size=10)
    )
    fig.update_yaxes(
        row=2, col=1,
        visible=False,
        showticklabels=False,
        range=[0, 1]  # Fix the range to make bars appear smaller
    )

    # Update overall layout
    fig.update_layout(
        height=600,
        width=1000,
        barmode='stack',
        bargap=0.1,
        title_text="Distribution of Frequencies by Type and Category",
        title_x=0.5,
        showlegend=False,
        margin=dict(l=80, r=50, t=100, b=100),
        paper_bgcolor='white',
        plot_bgcolor='rgba(240,240,240,0.5)'
    )

    return fig


def plot_time_series_grid(df_analysis, terms=['http', 'ad', 'shop', 'support']):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[f"Videos with '{term}'" for term in terms]
    )
    
    df_analysis['upload_date'] = pd.to_datetime(df_analysis['upload_date'])
    
    end_date = pd.to_datetime('2019-09-30')
    df_filtered = df_analysis[df_analysis['upload_date'] <= end_date]
    
    colors = {
        'scatter': 'rgba(0, 0, 255, 0.1)',
        'line': 'red',
        'fill': 'rgba(255, 0, 0, 0.2)'
    }
    
    for idx, term in enumerate(terms):
        row = (idx // 2) + 1
        col = (idx % 2) + 1
        
        daily_total = df_filtered.groupby('upload_date').size()
        daily_with_term = df_filtered[df_filtered[f'has_{term}'] == 1].groupby('upload_date').size()
        daily_percentage = (daily_with_term / daily_total * 100)
        
        window = 30
        rolling_mean = daily_percentage.rolling(window=window).mean()
        rolling_std = daily_percentage.rolling(window=window).std()
        
        fig.add_trace(
            go.Scatter(
                x=daily_percentage.index,
                y=daily_percentage.values,
                mode='markers',
                name='Daily',
                marker=dict(size=2, color=colors['scatter']),
                showlegend=(idx == 0),
                hovertemplate='Date: %{x}<br>Percentage: %{y:.1f}%<extra></extra>'
            ),
            row=row, col=col
        )
        
        fig.add_trace(
            go.Scatter(
                x=rolling_mean.index,
                y=rolling_mean.values,
                mode='lines',
                name=f'{window}-day Avg',
                line=dict(color=colors['line'], width=2),
                showlegend=(idx == 0),
                hovertemplate='Date: %{x}<br>Average: %{y:.1f}%<extra></extra>'
            ),
            row=row, col=col
        )
        
        fig.add_trace(
            go.Scatter(
                x=rolling_mean.index.tolist() + rolling_mean.index.tolist()[::-1],
                y=(rolling_mean + rolling_std).tolist() + (rolling_mean - rolling_std).tolist()[::-1],
                fill='toself',
                fillcolor=colors['fill'],
                line=dict(color='rgba(255,255,255,0)'),
                name='±1σ',
                showlegend=(idx == 0),
                hovertemplate='Date: %{x}<br>Range: %{y:.1f}%<extra></extra>'
            ),
            row=row, col=col
        )
        
        fig.update_xaxes(
            title_text="Date",
            row=row, col=col,
            tickangle=45,
            range=[df_filtered['upload_date'].min(), end_date]
        )
        fig.update_yaxes(
            title_text="Percentage",
            range=[0, 100],
            row=row, col=col
        )
    
    fig.update_layout(
        height=500,
        width=800,
        title_text="Percentage of Videos Containing Terms Over Time (Through September 2019)",
        title_y=0.95,
        showlegend=True,
        legend=dict(
            yanchor="bottom",
            y=0.45,
            xanchor="right",
            x=0.48,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        hovermode='x unified'
    )
    
    return fig


def plot_time_series_grid_cat(df_analysis, terms=['http', 'ad', 'shop', 'support'], color_scale='viridis'):
    # Convert to datetime
    df_analysis['upload_date'] = pd.to_datetime(df_analysis['upload_date'])
    
    # Filter data up to September 2019 as justificated in RQ1
    end_date = pd.to_datetime('2019-09-30')
    df_filtered = df_analysis[df_analysis['upload_date'] <= end_date]
    
    # Get color mapping
    color_map, colors = create_color_mapping(df_filtered, color_scale)
    
    # Get categories in their frequency-ordered sequence
    categories = list(color_map.keys())
    
    # Create figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[f"Videos with '{term}' by Category" for term in terms],
        vertical_spacing=0.12  # Increase spacing to make room for legend
    )
    
    for idx, term in enumerate(terms):
        # Calculate row and column position
        row = (idx // 2) + 1
        col = (idx % 2) + 1
        
        # Plot line for each category in the order of frequency
        for category in categories:
            # Filter for category
            df_cat = df_filtered[df_filtered['category_cc'] == category]
            
            # Calculate daily percentages for this category
            daily_total = df_cat.groupby('upload_date').size()
            daily_with_term = df_cat[df_cat[f'has_{term}'] == 1].groupby('upload_date').size()
            daily_percentage = (daily_with_term / daily_total * 100)
            
            # Calculate rolling mean (30-day window)
            rolling_mean = daily_percentage.rolling(window=30, min_periods=1).mean()
            
            # Add line for this category
            fig.add_trace(
                go.Scatter(
                    x=rolling_mean.index,
                    y=rolling_mean.values,
                    mode='lines',
                    name=category,
                    line=dict(color=color_map[category]),
                    showlegend=(idx == 0),  # Show legend only for first subplot
                    hovertemplate=f'{category}<br>Date: %{{x}}<br>30-day Avg: %{{y:.1f}}%<extra></extra>'
                ),
                row=row, col=col
            )
        
        # Update axes for this subplot
        fig.update_xaxes(
            title_text="Date",
            row=row, col=col,
            tickangle=45,
            range=[df_filtered['upload_date'].min(), end_date]  # Set x-axis range
        )
        fig.update_yaxes(
            title_text="Percentage",
            range=[0, 100],
            row=row, col=col
        )
    
    # Update layout with legend at the bottom
    fig.update_layout(
        height=900, 
        width=1200,
        title_text="Percentage of Videos Containing Terms Over Time by Category (Through September 2019)",
        title_y=0.95,
        showlegend=True,
        legend=dict(
            orientation="h",    
            yanchor="top",     
            y=-0.15,         
            xanchor="center", 
            x=0.5,
            font=dict(size=10) 
        ),
        margin=dict(b=100),   
        hovermode='x unified'
    )
    
    return fig


def prepare_data(df_cross, df_sizes):
    # Merge data for latter normalization in category sizes
    return pd.merge(df_cross, df_sizes, on='category_cc')

def create_scatter_trace(df_cat, x_val, y_val, color, size, category, show_legend):
    return go.Scatter(
        x=df_cat[x_val],
        y=df_cat[y_val],
        mode='markers',
        marker=dict(
            size=size,
            color=color,
            opacity=0.6,
            line=dict(width=1, color='white'),
            # trendline="ols"
        ),
        name=category,
        text=category,
        hovertemplate=(
            f"<b>{category}</b><br>" +
            f"{x_val.replace('has_', '')}: %{{x}}<br>" +
            f"{y_val.replace('has_', '')}: %{{y}}<br>" +
            "Total: %{marker.size:,.0f}<br>" +
            "<extra></extra>"
        ),
        showlegend=show_legend
    )


def add_regression_line(df_cat, x_val, y_val):

    x = np.log10(df_cat[x_val].values)  # Log transforms
    y = np.log10(df_cat[y_val].values)
    weights = df_cat['count'].values  
    
    # Pounderated regression
    coef = np.polyfit(x, y, 1, w=weights)
    slope, intercept = coef[0], coef[1]
    
    # R^2
    y_pred = slope * x + intercept
    residuals = y - y_pred
    ss_res = np.sum(weights * residuals**2)
    ss_tot = np.sum(weights * (y - np.average(y, weights=weights))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # Line computation
    x_line = np.array([min(x), max(x)])
    y_line = slope * x_line + intercept
    
    # 
    x_line = 10**x_line
    y_line = 10**y_line
    
    return go.Scatter(
        x=x_line,
        y=y_line,
        mode='lines',
        line=dict(color='black', width=1, dash='dot'),
        name='Weighted Regression',
        showlegend=False,
        hovertemplate=(
            f"Weighted R² = {r_squared:.3f}<br>" +
            f"Weighted Slope = {slope:.3f}<br>" +
            "<extra></extra>"
        )
    )


def create_visualization(df: pd.DataFrame, metrics_config, color_norm: str):
   
    x_cols = ['has_merchandise', 'has_affiliate', 'has_sponsorships']
    
    categories = df['category_cc'].unique()
    colors = px.colors.qualitative.Alphabet[:len(categories)]
    color_dict = dict(zip(categories, colors))
    
    color_dict, _ = create_color_mapping(df, color_norm)
    
    figures = {}
    
    for metric, title in metrics_config.items():
        fig = make_subplots(
            rows=1,
            cols=3,
            subplot_titles=[f'{x.replace("has_", "").capitalize()} vs {title}' for x in x_cols],
            horizontal_spacing=0.01
        )
        
        size = df['count'] / df['count'].max() * 50 + 10
        
        for idx, x_col in enumerate(x_cols, 1):
            
            for category in categories:
                df_cat = df[df['category_cc'] == category]
                
                trace = create_scatter_trace(
                    df_cat=df_cat,
                    x_val=x_col,
                    y_val=metric,
                    color=color_dict[category],
                    size=size[df['category_cc'] == category],
                    category=category,
                    show_legend=(idx == 3)
                )
                
                fig.add_trace(trace, row=1, col=idx)
            
           
            regression_trace = add_regression_line(df, x_col, metric)
            fig.add_trace(regression_trace, row=1, col=idx)
        
        # Update layout
        fig.update_layout(
            height=400,
            width=1200,
            title=f'Relationship between Monetization Methods and {title}',
            showlegend=True,
            template="plotly_white",
        )
        
        # Update axes
        fig.update_xaxes(type="log", title_text="Number of videos")
        for i in range(1, 4):
            if i == 1:
                fig.update_yaxes(type="log", title_text="Number of videos", col=i)
            else:
                fig.update_yaxes(type="log", title_text="", col=i, showticklabels=False)
        
        figures[metric] = fig
    
    return figures

def print_regression_stats(df, x_val, y_val):
    x = np.log10(df[x_val].values)
    y = np.log10(df[y_val].values)
    weights = df['count'].values
    
    coef = np.polyfit(x, y, 1, w=weights)
    slope, intercept = coef[0], coef[1]
    
    y_pred = slope * x + intercept
    residuals = y - y_pred
    
    ss_res = np.sum(weights * residuals**2)
    ss_tot = np.sum(weights * (y - np.average(y, weights=weights))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    n = len(df)
    std_err = np.sqrt(np.sum(weights * residuals**2) / (n - 2))
    
    x_mean = np.average(x, weights=weights)
    x_var = np.average((x - x_mean)**2, weights=weights)
    std_err_slope = std_err / np.sqrt(n * x_var)
    
    t_stat_slope = slope / std_err_slope
    
    from scipy import stats
    p_value_slope = 2 * (1 - stats.t.cdf(abs(t_stat_slope), n-2))
    
    print(f"\nRegression stats for {x_val} vs {y_val}:")
    print(f"Weighted R²: {r_squared:.4f}")
    print(f"P-value: {p_value_slope:.4e}")
    
    return {
        'r_squared': r_squared,
        'p_value': p_value_slope
    }

def analyze_all_regressions(df, metrics_config):
    x_cols = ['has_merchandise', 'has_affiliate', 'has_sponsorships']
    
    for metric in metrics_config.keys():
        print(f"\nAnalyzing regressions for {metrics_config[metric]}:")
        print("=" * 50)
        
        for x_col in x_cols:
            stats = print_regression_stats(df, x_col, metric)


def create_monetization_heatmap(merged_dataset):
    """
    Create a correlation heatmap for monetization methods
    """
    # Select the monetization columns
    monetization_cols = ["has_merchandise", "has_affiliate", "has_sponsorships"]
    
    # Calculate correlation matrix
    corr_matrix = merged_dataset[monetization_cols].corr()
    
    # Create figure
    plt.figure(figsize=(5, 4))
    
    # Create heatmap
    sns.heatmap(
        corr_matrix,
        annot=True,  # Show numbers in cells
        cmap='coolwarm',  # Color scheme from blue (negative) to red (positive)
        vmin=-1, vmax=1,  # Fix scale from -1 to 1
        center=0,  # Center the colormap at 0
        square=True,  # Make cells square
        fmt='.2f',  # Round numbers to 2 decimal places
        cbar_kws={'label': 'Correlation Coefficient'}
    )
    
    # Customize plot
    plt.title('Correlation between Monetization Methods', pad=20)
    plt.tight_layout()
    plt.show()
    
    return corr_matrix

def create_words_heatmap(df_analysis):
    """
    Create a correlation heatmap for word usage in descriptions
    """
    # Select the word usage columns
    word_cols = ['has_http', 'has_ad', 'has_shop', 'has_support']
    
    # Create nicer labels for the display
    label_map = {
        'has_http': 'URLs',
        'has_ad': 'Ad',
        'has_shop': 'Shop',
        'has_support': 'Support'
    }
    
    # Calculate correlation matrix
    corr_matrix = df_analysis[word_cols].corr()
    
    # Rename indices and columns for better display
    corr_matrix = corr_matrix.rename(index=label_map, columns=label_map)
    
    # Create figure
    plt.figure(figsize=(5, 4))
    
    # Create heatmap
    sns.heatmap(
        corr_matrix,
        annot=True,  # Show numbers in cells
        cmap='coolwarm',  # Color scheme from blue (negative) to red (positive)
        vmin=-1, vmax=1,  # Fix scale from -1 to 1
        center=0,  # Center the colormap at 0
        square=True,  # Make cells square
        fmt='.2f',  # Round numbers to 2 decimal places
        cbar_kws={'label': 'Correlation Coefficient'}
    )
    
    # Customize plot
    plt.title('Correlation between Word Usage in Descriptions', pad=20)
    plt.tight_layout()
    plt.show()
    
    return corr_matrix


def plot_distribution_grid_with_red_average(df_analysis, terms=['http', 'ad', 'shop', 'support']):
    """
    Create a 2x2 grid of line plots with light red average line using Plotly
    """
    # Extract year
    df_analysis['year'] = pd.to_datetime(df_analysis['upload_date']).dt.year
    years = sorted(df_analysis['year'].unique())
    
    # Color palette
    colors = [
        '#E69F00', '#56B4E9', '#009E73', '#CC79A7', '#0072B2', 
        '#D55E00', '#F0E442', '#999999', '#44AA99', '#882255',
        '#661100', '#6699CC', '#AA4499', '#332288'
    ]
    
    # Line styles (Plotly dash patterns)
    line_styles = ['solid', 'dash', 'dot', 'dashdot']
    
    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[f"Distribution of '{term}' (Excluding Zeros)" for term in terms],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    for idx, term in enumerate(terms):
        row = (idx // 2) + 1
        col = (idx % 2) + 1
        
        # Calculate average distribution across all years
        all_counts = {}
        for year in years:
            year_data = df_analysis[
                (df_analysis['year'] == year) & 
                (df_analysis[f'count_{term}'] > 0)
            ][f'count_{term}']
            
            if len(year_data) > 0:
                counts = year_data.value_counts().sort_index()
                proportions = (counts / len(year_data) * 100)
                
                for count, prop in proportions.items():
                    if count not in all_counts:
                        all_counts[count] = []
                    all_counts[count].append(prop)
        
        # Calculate average for each count
        avg_counts = {k: np.mean(v) for k, v in all_counts.items()}
        
        # Plot individual year lines
        for i, year in enumerate(years):
            year_data = df_analysis[
                (df_analysis['year'] == year) & 
                (df_analysis[f'count_{term}'] > 0)
            ][f'count_{term}']
            
            if len(year_data) > 0:
                counts = year_data.value_counts().sort_index()
                proportions = (counts / len(year_data) * 100)
                
                fig.add_trace(
                    go.Scatter(
                        x=counts.index,
                        y=proportions,
                        mode='lines+markers',
                        name=str(year),
                        line=dict(
                            color=colors[i % len(colors)],
                            dash=line_styles[i % len(line_styles)],
                            width=1.5
                        ),
                        marker=dict(size=4),
                        opacity=0.7,
                        showlegend=(idx == 0),  # Show legend only for first subplot
                        hovertemplate=f"Year {year}<br>Count: %{{x}}<br>Percentage: %{{y:.2f}}%<extra></extra>"
                    ),
                    row=row, col=col
                )
        
        # Plot average line in light red
        avg_x = sorted(avg_counts.keys())
        avg_y = [avg_counts[x] for x in avg_x]
        fig.add_trace(
            go.Scatter(
                x=avg_x,
                y=avg_y,
                mode='lines',
                name='Average',
                line=dict(color='#fa6169', width=5),
                opacity=1,
                showlegend=(idx == 0),
                hovertemplate="Average<br>Count: %{x}<br>Percentage: %{y:.2f}%<extra></extra>"
            ),
            row=row, col=col
        )
        
        # Update axes
        fig.update_xaxes(
            title_text="Number of Occurrences",
            range=[0, 20],
            tickmode='linear',
            dtick=5,
            minor=dict(tickmode='linear', dtick=1),
            row=row, col=col
        )
        
        fig.update_yaxes(
            title_text="% of Videos with Term (log)",
            type='log',
            range=[-1, 3],  # 10^-1 to 10^3
            row=row, col=col
        )
    
    # Update layout
    fig.update_layout(
        height=800,
        width=1200,
        title_text="Distribution of Term Occurrences by Year<br>(Only showing videos containing terms)",
        title_y=0.95,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        margin=dict(b=100),
        hovermode='closest'
    )
    
    return fig

