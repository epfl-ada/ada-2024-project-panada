import numpy as np
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import gzip
from matplotlib.dates import DateFormatter, YearLocator
from scipy import stats

def create_color_mapping(df):
   
    # Get categories ordered by their frequency
    category_counts = df['category_cc'].value_counts()
    ordered_categories = category_counts.index.tolist()
    n_colors = len(ordered_categories)
    
    # Generate colors 
    colors = sns.color_palette("viridis", n_colors)
    
    # Dictionary for color mapping
    color_map = dict(zip(ordered_categories, colors))
    
    return color_map, colors

def plot_category_distribution(df, color_map):

    # Calculate percentages
    category_counts = df['category_cc'].value_counts()
    category_percentages = (category_counts / len(df) * 100).round(2)
    
    # Generate the bar plot
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        x=category_percentages.index,
        y=category_percentages.values,
        hue=category_percentages.index,
        palette=color_map,
        legend=False
    )
    
    # Labels
    plt.title('Distribution of Categories (%)')
    plt.xlabel('Category')
    plt.ylabel('Percentage (%)')
    plt.xticks(rotation=-45, ha='left')
    
    # Add percentage labels 
    for i, v in enumerate(category_percentages.values):
        ax.text(i, v, f'{v:.1f}%', ha='center', va='bottom')
    
    plt.tight_layout()
    
    return plt.gcf()

def plot_monetization_shares(df, columns, color_map):

    # 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Channel Category Monetization Strategies Shares', y=1.05)
    
    # Their Titles 
    titles = {
        "has_merchandise": "Merchandise",
        "has_affiliate": "Affiliation",
        "has_sponsorships": "Sponsorship"
    }
    
    # Create 3 pie charts
    for idx, column in enumerate(columns):
        ax = axes[idx]
        
        # Calculate percentages for this monetization type
        temp_df = df[df[column]==True]
        counts = temp_df['category_cc'].value_counts(normalize=True) * 100
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            counts.values,
            labels=counts.index,
            colors=[color_map[cat] for cat in counts.index],
            autopct='%1.1f%%',
            textprops={'fontsize': 8}
        )
        
        ax.set_title(titles[column])
    
    plt.tight_layout()
    return fig

def plot_stacked_distributions(data, color_map):

    # 3 Subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Distribution of Frequencies by Type and Category', y=1.05)
    
    # Monetization types
    types = ['merch_frequency', 'sponsorship_frequency', 'affiliate_frequency']
    titles = ['Merch Frequency', 'Sponsorship Frequency', 'Affiliate Frequency']
    
    # Create histograms
    for idx, (type_name, title) in enumerate(zip(types, titles)):
        ax = axes[idx]
        
        # Plot histograms for each category
        for category in color_map.keys():
            cat_data = data[
                (data['category_cc'] == category) & 
                (data[type_name] > 0)
            ][type_name]
            
            if not cat_data.empty:
                sns.histplot(
                    data=cat_data,
                    bins=30,
                    alpha=0.5,
                    color=color_map[category],
                    ax=ax,
                    label=category
                )
        
        ax.set_title(title)
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Count (log scale)' if idx == 0 else '')
        ax.set_yscale('log')
        ax.set_xlim(0, 1)
    
    plt.tight_layout()
    return fig

# 

def plot_time_series_grid(df_analysis, terms=['http', 'ad', 'shop', 'support']):

    # 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Convert upload_date to datetime if not already
    df_analysis['upload_date'] = pd.to_datetime(df_analysis['upload_date'])
    
    # Filter data up to september 2019 as in previous RQ
    end_date = pd.to_datetime('2019-09-30')
    df_filtered = df_analysis[df_analysis['upload_date'] <= end_date]
    
    colors = {
        'scatter': 'blue',
        'line': 'red',
        'fill': 'red'
    }
    
    # Create plots for each term
    for idx, term in enumerate(terms):
        row = idx // 2
        col = idx % 2
        ax = axes[row, col]
        
        # Calculate daily percentages
        daily_total = df_filtered.groupby('upload_date').size()
        daily_with_term = df_filtered[df_filtered[f'has_{term}'] == 1].groupby('upload_date').size()
        daily_percentage = (daily_with_term / daily_total * 100)
        
        # Calculate rolling statistics
        window = 30
        rolling_mean = daily_percentage.rolling(window=window).mean()
        rolling_std = daily_percentage.rolling(window=window).std()
        
        # Plot scatter points
        ax.scatter(daily_percentage.index, daily_percentage.values, 
                  color=colors['scatter'], alpha=0.1, s=2, label='Daily')
        
        # Plot rolling mean
        ax.plot(rolling_mean.index, rolling_mean.values, 
                color=colors['line'], linewidth=2, label=f'{window}-day Avg')
        
        # Plot confidence interval
        ax.fill_between(rolling_mean.index,
                       rolling_mean - rolling_std,
                       rolling_mean + rolling_std,
                       color=colors['fill'], alpha=0.2, label='±1σ')

        # Labels
        ax.set_title(f"Videos with '{term}'")
        ax.set_xlabel('Date')
        ax.set_ylabel('Percentage' if col == 0 else '')
        ax.set_ylim(0, 100)
        ax.set_xlim(df_filtered['upload_date'].min(), end_date)
        
        ax.tick_params(axis='x', rotation=45)
        
        # Only show legend for the first subplot otherwise too much
        if idx == 0:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
                     borderaxespad=0., frameon=True,
                     fancybox=True, shadow=True)
    
    # Add title at the bottom
    plt.figtext(0.5, 0.02, 'Percentage of Videos Containing Terms Over Time (Through September 2019)',
                ha='center', fontsize=12)
    
    # Adjust layout to make room for bottom title
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    
    return fig

#Code for RQ2.2

def plot_time_series_grid(df_analysis, terms=['http', 'ad', 'shop', 'support']):

    # 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Convert upload_date to datetime if not already
    df_analysis['upload_date'] = pd.to_datetime(df_analysis['upload_date'])
    
    # Filter data up to september 2019 as in previous RQ
    end_date = pd.to_datetime('2019-09-30')
    df_filtered = df_analysis[df_analysis['upload_date'] <= end_date]
    
    colors = {
        'scatter': 'blue',
        'line': 'red',
        'fill': 'red'
    }
    
    # Create plots for each term
    for idx, term in enumerate(terms):
        row = idx // 2
        col = idx % 2
        ax = axes[row, col]
        
        # Calculate daily percentages
        daily_total = df_filtered.groupby('upload_date').size()
        daily_with_term = df_filtered[df_filtered[f'has_{term}'] == 1].groupby('upload_date').size()
        daily_percentage = (daily_with_term / daily_total * 100)
        
        # Calculate rolling statistics
        window = 30
        rolling_mean = daily_percentage.rolling(window=window).mean()
        rolling_std = daily_percentage.rolling(window=window).std()
        
        # Plot scatter points
        ax.scatter(daily_percentage.index, daily_percentage.values, 
                  color=colors['scatter'], alpha=0.1, s=2, label='Daily')
        
        # Plot rolling mean
        ax.plot(rolling_mean.index, rolling_mean.values, 
                color=colors['line'], linewidth=2, label=f'{window}-day Avg')
        
        # Plot confidence interval
        ax.fill_between(rolling_mean.index,
                       rolling_mean - rolling_std,
                       rolling_mean + rolling_std,
                       color=colors['fill'], alpha=0.2, label='±1σ')

        # Labels
        ax.set_title(f"Videos with '{term}'")
        ax.set_xlabel('Date')
        ax.set_ylabel('Percentage' if col == 0 else '')
        ax.set_ylim(0, 100)
        ax.set_xlim(df_filtered['upload_date'].min(), end_date)
        
        ax.tick_params(axis='x', rotation=45)
        
        # Only show legend for the first subplot otherwise too much
        if idx == 0:
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
                     borderaxespad=0., frameon=True,
                     fancybox=True, shadow=True)
    
    # Add title at the bottom
    plt.figtext(0.5, 0.02, 'Percentage of Videos Containing Terms Over Time (Through September 2019)',
                ha='center', fontsize=12)
    
    # Adjust layout to make room for bottom title
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    
    return fig


# Code for RQ2.3

def prepare_data(df_cross, df_sizes):
    # Merge data for latter normalization in category sizes
    return pd.merge(df_cross, df_sizes, on='category_cc')

def create_scatter_plot(ax, df_cat, x_val, y_val, color, size, category):
    scatter = ax.scatter(
        df_cat[x_val],
        df_cat[y_val],
        s=size,
        c=[color],
        alpha=0.6,
        edgecolor='white',
        linewidth=1,
        label=category
    )
    return scatter

def add_regression_line(ax, df_cat, x_val, y_val):
    x = np.log10(df_cat[x_val].values)
    y = np.log10(df_cat[y_val].values)
    weights = df_cat['count'].values

    # Weighted regression
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

    # Convert back from log scale
    x_line = 10**x_line
    y_line = 10**y_line

    # Plot regression line
    ax.plot(x_line, y_line, 'k:', linewidth=1, 
            label=f'R² = {r_squared:.3f}\nSlope = {slope:.3f}')

def create_visualization(df, metrics_config, color_norm):
    x_cols = ['has_merchandise', 'has_affiliate', 'has_sponsorships']
    categories = df['category_cc'].unique()
    
    # Recall from RQ2.1
    color_dict, colors = create_color_mapping(df)

    figures = {}
    
    for metric, title in metrics_config.items():
        # Create figure with subplots
        fig = plt.figure(figsize=(15, 5))
        gs = GridSpec(1, 3, figure=fig)
        gs.update(wspace=0.3)

        # Calculate sizes for scatter points
        size = df['count'] / df['count'].max() * 200 + 50

        for idx, x_col in enumerate(x_cols):
            ax = fig.add_subplot(gs[idx])
            
            # Plot scatter points for each category
            for category in categories:
                df_cat = df[df['category_cc'] == category]
                scatter = create_scatter_plot(
                    ax=ax,
                    df_cat=df_cat,
                    x_val=x_col,
                    y_val=metric,
                    color=color_dict[category],
                    size=size[df['category_cc'] == category],
                    category=category
                )
            
            # Add regression line
            add_regression_line(ax, df, x_col, metric)

            # Set scales and labels
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_title(f'{x_col.replace("has_", "").capitalize()} vs {title}')
            
            if idx == 0:
                ax.set_ylabel('Number of videos')
            ax.set_xlabel('Number of videos')

        # Add legend to the right of the last subplot
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles[:len(categories)], labels[:len(categories)], 
                  loc='center left', bbox_to_anchor=(1.0, 0.5))

        plt.suptitle(f'Relationship between Monetization Methods and {title}')
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