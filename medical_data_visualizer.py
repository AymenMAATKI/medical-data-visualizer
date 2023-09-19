import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] =  ((df['weight']/(df['height']/100)**2)>25).astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df[['cholesterol', 'gluc']]=df[['cholesterol', 'gluc']].replace({1: 0, 2: 1, 3: 1})

# Draw Categorical Plot
def draw_cat_plot():

  
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'],id_vars=['cardio'])
    
  
  # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat_grouped = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    df_cat_grouped.rename(columns={'value': 'variable_value'}, inplace=True)

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(
        x='variable', hue='variable_value', col='cardio',
        data=df_cat_grouped, kind='count'
    )

    # Set plot titles and axis labels
    # Set plot titles and axis labels
    g.set_axis_labels('variable', 'total')
    g.set_titles('Cardio = {col_name}')

    # Save the figure
    fig = g.fig
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():

  
    #clean data filter invalid patient data 
    df_clean = df[
        (df['ap_hi'] >= df['ap_lo']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

  
    # Calculate the correlation matrix
    corr = df_clean.corr()

  
    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

  
    # Set up the Matplotlib figure and axes for the heatmap
    fig, ax = plt.subplots(figsize=(10, 8))

  
    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, annot=True, fmt=".1f", cmap="coolwarm", mask=mask, cbar=True, square=True, ax=ax)
    

    # saving the figure
    fig.savefig('heatmap.png')
    return fig
