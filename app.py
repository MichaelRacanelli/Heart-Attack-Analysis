from shiny import reactive
from shiny.express import input, render, ui
from shiny.ui import page_navbar
from shinyswatch import theme
from shinywidgets import output_widget, render_widget

from functools import partial

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from categorical_plots import pie_chart, pie_split, bar_chart, bar_split
from numerical_plots import create_distribution_plot

from palmerpenguins import load_penguins
data = load_penguins()

# data = pd.read_csv('heart_attack_youth_vs_adult.csv', index_col=0)
# data['Heart_Attack'] = data['Heart_Attack'].map({0: 'No', 1: 'Yes'})

cols_categorical = data.select_dtypes(include='object').columns
cols_numeric = data.select_dtypes(include='number').columns

ui.page_opts(
    title="Data Analyze",
    theme=theme.cerulean,  
    page_fn=partial(page_navbar, id="page"),  
)
with ui.nav_panel('Home'):
    ui.h1("Dataset Selection")
    ui.markdown("""This dashboard provides an interactive way to explore and visualize datasets of your choosing. 
                \nTo get started, select a dataset from the dropdown menu below.
                \nPlease use the navigation panel to explore the data and generate visualizations.
                """)

with ui.nav_panel('EDA'):
    ui.h1("Exploratory Data Analysis")
    ui.markdown("""""")

    # with ui.card():
    #     ui.card_header('Data preview')
    #     @render.text  
    #     def text():
    #         return str(data.shape[0]) + " rows"
    #     @render.data_frame  
    #     def data_render():
    #         # Extract information from the DataFrame
    #         info_dict = {
    #             'Column': data.columns,
    #             'Dtype': data.dtypes
    #         }
            
    #         # Create a DataFrame from the extracted information
    #         info_df = pd.DataFrame(info_dict)
            
    #         # Reset index for a clean table
    #         info_df.reset_index(drop=True, inplace=True)
    #         return render.DataGrid(info_df)

    with ui.card():
        ui.card_header('Categorical data distribution')
        with ui.layout_sidebar():  
            with ui.sidebar(bg="#f8f8f8"):  
                ui.input_radio_buttons(  
                    "chart_type",  
                    "Select chart type",  
                    {"pie": "Pie", "bar": "Bar"},  
                )  
                ui.input_selectize(
                    "var_cat", "Select variable",
                    choices=cols_categorical.tolist()
                )

                ui.input_selectize(
                    "var_target", "Select target variable",
                    choices=cols_categorical.tolist()
                )

                ui.input_switch("sep_target", "Separate by target", False)


            @render_widget
            def chart_cat():
                if input.chart_type() == 'pie':
                    if input.sep_target():
                        return pie_split(data, input.var_cat(), input.var_target())
                    else:
                        return pie_chart(data, input.var_cat())
                elif input.chart_type() == 'bar':
                    if input.sep_target():
                        return bar_split(data, input.var_cat(), input.var_target())
                    else:
                        return bar_chart(data, input.var_cat())

    with ui.card():
        ui.card_header('Numerical data distribution')
        with ui.layout_sidebar():  
            with ui.sidebar(bg="#f8f8f8"):
                ui.input_selectize(
                    "var_num", "Select variable",
                    choices=cols_numeric.tolist()
                )
                ui.input_selectize(
                    "var_hue", "Select hue variable",
                    choices=cols_categorical.tolist()
                )
            @render_widget
            def chart_num():
                return create_distribution_plot(data, input.var_num(), input.var_hue())
        