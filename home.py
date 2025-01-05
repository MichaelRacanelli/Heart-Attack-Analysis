from shiny import reactive
from shiny.express import input, render, ui

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('heart_attack_youth_vs_adult.csv', index_col=0)
cols_categorical = data.select_dtypes(include='object').columns
cols_numeric = data.select_dtypes(include='number').columns
data['Heart_Attack'] = data['Heart_Attack'].map({0: 'No', 1: 'Yes'})

ui.h1("Categorical data distribution")
ui.input_selectize(
    "var_cat", "Select variable",
    choices=cols_categorical.tolist()
)

ui.input_switch("sep_disease", "Separate by disease", False)


@render.plot
def pie():
    if input.sep_disease():
        fig, axes = plt.subplots(1, 2, figsize=(20, 7))
        
        # Create a consistent color mapping for the categories
        unique_categories = data[input.var_cat()].unique()
        colors = sns.color_palette('pastel', len(unique_categories))
        color_mapping = {category: color for category, color in zip(unique_categories, colors)}

        # Set a single title above the entire figure
        fig.suptitle(f'{input.var_cat()}', fontsize=20)

        for i, (title, subset) in enumerate(data.groupby(data['Heart_Attack'])):
            # Map colors to categories in the subset
            category_counts = subset[input.var_cat()].value_counts()
            category_colors = [color_mapping[category] for category in category_counts.index]
            
            # Plot pie chart
            category_counts.plot.pie(
                autopct='%1.1f%%',
                startangle=90,
                colors=category_colors,
                wedgeprops={'edgecolor': 'black'},
                textprops={'fontsize': 12},
                ax=axes[i]
            )
            # Set individual group titles for each pie chart
            axes[i].set_title(f'Heart Disease: {title}',                               fontsize=14, 
                              y=-0.2,  # Move title below the pie chart
                              loc='center')
            axes[i].set_ylabel('')  # Hide the y-label
            axes[i].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        plt.tight_layout()
    else:
        plt.figure(figsize=(10, 7))
        colors = sns.color_palette('pastel')[0:len(data[input.var_cat()].unique())]
        data[input.var_cat()].value_counts().plot.pie(
            autopct='%1.1f%%', 
            startangle=90, 
            colors=colors, 
            wedgeprops={'edgecolor': 'black'},
            textprops={'fontsize': 12}
        )
        plt.title(f'{input.var_cat()}', fontsize=20)
        plt.ylabel('')  # Hide the y-label
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
