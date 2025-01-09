import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PALETTE = sns.color_palette('pastel')

def pie_chart(data, input):
    plt.figure(figsize=(10, 7))
    colors = PALETTE[0:len(data[input].unique())]
    data[input].value_counts().plot.pie(
    autopct='%1.1f%%', 
    startangle=90, 
    colors=colors, 
    wedgeprops={'edgecolor': 'black'},
    textprops={'fontsize': 12}
    )
    plt.title(f'{input}', fontsize=20)
    plt.ylabel('')  # Hide the y-label
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt

def pie_split(data, input, target):
    fig, axes = plt.subplots(1, 2, figsize=(20, 7))

    # Create a consistent color mapping for the categories
    unique_categories = data[input].unique()
    colors = PALETTE[:len(unique_categories)]
    color_mapping = {category: color for category, color in zip(unique_categories, colors)}

    # Set a single title above the entire figure
    fig.suptitle(f'{input}', fontsize=20)

    for i, (title, subset) in enumerate(data.groupby(target)):
        # Map colors to categories in the subset
        category_counts = subset[input].value_counts()
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
        axes[i].set_title(f'{target}: {title}',
                        fontsize=14, 
                        y=-0.2,  # Move title below the pie chart
                        loc='center')
        axes[i].set_ylabel('')  # Hide the y-label
        axes[i].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    plt.tight_layout()
    plt

def bar_chart(data, input):
    plt.figure(figsize=(10, 7))
    sns.countplot(x=input, data=data, legend=False, palette='pastel')
    plt.title(f'{input}', fontsize=20)
    plt.xlabel(f'{input}')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt

def bar_split(data, input, target):
    plt.figure(figsize=(10, 7))
    sns.countplot(x=input, hue=target, data=data, palette='pastel')
    plt.title(f'{input}', fontsize=20)
    plt.xlabel(f'{input}')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title=target, loc='upper right')
    plt