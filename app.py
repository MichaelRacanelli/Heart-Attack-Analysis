from shiny import reactive
from shiny.express import input, render, ui
from shiny.ui import page_navbar
from shinyswatch import theme

from functools import partial

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ui.page_opts(
    title="Data Analysis",
    theme=theme.cerulean,  
    page_fn=partial(page_navbar, id="page"),  
)
with ui.nav_panel('Home'):
    ui.h1("Data Analysis of Heart Attacks in Youth vs Adults")
    ui.markdown("""This dashboard provides an interactive way to explore and visualize data on heart attacks in youth vs adults. 
                \nThe data was sourced from [Kaggle](https://www.kaggle.com/datasets/ankushpanday1/heart-attack-in-youth-vs-adult-in-americastate/) and contains information on heart attacks in youth and adults in America.
                \nPlease use the navigation panel to explore.
                """)

with ui.nav_panel('EDA'):
    ui.h1("Exploratory Data Analysis")
    ui.markdown("""""")

    data = pd.read_csv('heart_attack_youth_vs_adult.csv', index_col=0)
    data['Heart_Attack'] = data['Heart_Attack'].map({0: 'No', 1: 'Yes'})

    cols_categorical = data.select_dtypes(include='object').columns
    cols_numeric = data.select_dtypes(include='number').columns

    with ui.accordion(id='acc', open='Data preview'):
        with ui.accordion_panel('Data preview'):
            @render.text  
            def text():
                return str(data.shape[0]) + " rows"
            @render.data_frame  
            def data_render():
                # Extract information from the DataFrame
                info_dict = {
                    'Column': data.columns,
                    'Dtype': data.dtypes
                }
                
                # Create a DataFrame from the extracted information
                info_df = pd.DataFrame(info_dict)
                
                # Reset index for a clean table
                info_df.reset_index(drop=True, inplace=True)
                return render.DataGrid(info_df)

        with ui.accordion_panel('Categorical data distribution'):
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
                        axes[i].set_title(f'Heart Attack: {title}',                               fontsize=14, 
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
        with ui.accordion_panel('Numerical data distribution'):  
            ui.input_selectize(
                "var_num", "Select variable",
                choices=cols_numeric.tolist()
            )