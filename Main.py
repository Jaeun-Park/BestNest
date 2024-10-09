import pandas as pd
import sys
import numpy as np
from Merge_dataset import MergeData
import matplotlib.pyplot as plt
import seaborn as sns # For heatmap
import matplotlib.gridspec as gridspec  # For complex grid layout

# Function to get user input for selecting parameters
def get_user_input():
    print("Please choose the parameters you want to include in your analysis:")
    print("1: Cost of Living")
    print("2: Literacy Rate")
    print("3: Crime Cost")
    print("4: Air Quality")

    # Get a list of chosen parameters from the user
    choices = input("Enter the numbers of the parameters you want to include, separated by commas (e.g., 1, 2, 3, 4): ")

    # Calling mergeData method to call scrapers and creating combined dataset.
    try:
        # Convert the input string to a list of integers
        choices_list = [int(choice.strip()) for choice in choices.split(",")]

        # Storing user choices in a CSV
        df_choices = pd.DataFrame(choices_list)
        df_choices.to_csv("Data_Files/User_Choices.csv", index=False)

        # Validate that choices are within the acceptable range
        if not all(choice in [1, 2, 3, 4] for choice in choices_list):
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter only numbers between 1 and 4, separated by commas.")
        return get_user_input()  # Prompt the user again in case of invalid input

    print("Merging data based on user choices...")
    MergeData.mergeData()

    return choices_list

# Function to filter and display the DataFrame based on user choices
def filter_dataframe(df, choices):
    columns = ['City']  # The 'City' column should always be included

    # Map the user choices to corresponding columns
    if 1 in choices:
        columns.extend(['Cost of Living Value', 'Cost of Living Score'])
    if 2 in choices:
        columns.extend(['Literacy Rate Value', 'Literacy Rate Score'])
    if 3 in choices:
        columns.extend(['Crime Cost Value', 'Crime Cost Score'])
    if 4 in choices:
        columns.extend(['Air Quality Value', 'Air Quality Score'])

    # Filter the DataFrame to only keep the selected columns
    filtered_df = df.loc[:, columns].copy()
    
    # Add total score and sort
    score_columns = [col for col in filtered_df.columns if 'Score' in col]
    filtered_df["Total Score"] = filtered_df[score_columns].sum(axis=1)
    filtered_df = filtered_df.sort_values(by="Total Score", ascending=False).reset_index(drop=True)
    filtered_df['Rank'] = filtered_df.index + 1

    # Function to generate a summary for the top-ranked city
    def generate_top_city_summary(df):
        # Assuming the DataFrame is already sorted by rank
        top_city = df.iloc[0]  # Get the first row (top 1 city)
        city_name = top_city['City']

        summary_parts = [f"Top 1 City: {city_name}"]
        if 'Cost of Living Value' in top_city:
            summary_parts.append(f"Cost of living (index in 2021, US average is 100): {top_city['Cost of Living Value']}")
        if 'Crime Cost Value' in top_city:
            summary_parts.append(f"Crime cost (cost per resident in 2022): ${top_city['Crime Cost Value']}")
        if 'Air Quality Value' in top_city:
            summary_parts.append(f"Air quality (number of good air quality days in 2024): {top_city['Air Quality Value']}")
        if 'Literacy Rate Value' in top_city:
            summary_parts.append(f"Literacy rate: {top_city['Literacy Rate Value']}%")

        # Join all parts into a final summary text
        summary_text = '\n'.join(summary_parts)
        return summary_text

    # Get the summary text and return
    top_city_summary = generate_top_city_summary(filtered_df)

    # Display the updated DataFrame
    print(filtered_df.head(10))

    # Save the filtered DataFrame in the same sorted order
    output_path = 'Data_Files/filtered_city_scores.csv'
    filtered_df.to_csv(output_path, index=False)
    print(f"\nFiltered data has been saved to '{output_path}' in the sorted order")

    return filtered_df, top_city_summary

# Heatmap function with inversed color and custom labels
def heatmap_chart(ax, df, score_columns):
    data_to_plot = df[score_columns].set_index(df['City'])

    # Inverse the color by using 'coolwarm_r' colormap (red for 0, blue for 10), extend the scale to 0
    sns.heatmap(data_to_plot, annot=True, cmap='coolwarm_r', cbar_kws={'ticks': [0, 5, 10]}, ax=ax, vmin=0, vmax=10)
    ax.set_title('Heatmap of Scores for Top Cities', fontsize=12, weight='bold')

    # Customize the colorbar to include 'High score' and 'Low score'
    colorbar = ax.collections[0].colorbar
    colorbar.set_ticks([0, 5, 10])
    colorbar.set_ticklabels(['0 (Low score)', '5', '10 (High score)'])

# Visualization function
def create_combined_visualization(df, top_city_summary, choices, top_n=10):
    top_cities = df.head(top_n)

    # Calculate the dynamic total score
    total_score = 10 * len(choices)  # 10 points per user choice

    # Create a figure with gridspec layout
    fig = plt.figure(figsize=(12, 8))
    
    # Define a 3-row grid where the first row is for the summary, second row for the table, third for the heatmap
    gs = gridspec.GridSpec(3, 1, height_ratios=[0.1, 1.5, 2], figure=fig)

    # Add the summary box in the first row
    ax_summary = fig.add_subplot(gs[0, 0])
    ax_summary.axis('off')  # No axes for the summary box
    ax_summary.text(
        0.5, 3.5, top_city_summary, fontsize=12, fontweight='bold', 
        bbox=dict(facecolor='lightblue', alpha=0.5), ha='center', va='center'
    )

    # Table in the second row
    ax_table = fig.add_subplot(gs[1, 0])
    ax_table.axis('off')
    ax_table.set_title("Table of the Top 10 Cities", fontsize=12, pad=5, weight='bold')

    table_data = top_cities[["Rank", "City", "Total Score"]].values.tolist()
    column_labels = ["Rank", "City", f"Overall Score (Total {total_score})"]

    # Create the table
    table = ax_table.table(cellText=table_data, colLabels=column_labels, loc='center', cellLoc='center', bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Set height for all rows
    for (row, col), cell in table.get_celld().items():
        cell.set_height(0.1)

    # Set the background color of the header row to gray
    for (row, col), cell in table.get_celld().items():
        if row == 0:  # This refers to the header row
            cell.set_fontsize(10)
            cell.set_text_props(weight='bold')  # Set header text bold
            cell.set_facecolor('lightgray')  # Set header row color to gray

    # Define the score columns to use for heatmap, excluding 'Total Score'
    score_columns = [col for col in df.columns if 'Score' in col and col != 'Total Score']

    # Heatmap in the third row
    ax_heatmap = fig.add_subplot(gs[2, 0])
    heatmap_chart(ax_heatmap, top_cities, score_columns)

    # Add equal padding between summary, table, and heatmap
    plt.subplots_adjust(hspace=0.3)

    # Save the figure as a PNG image
    file_path = 'output_visualization.png'
    plt.savefig(file_path, format="png")
    print(f"Visualization saved as {file_path}")

    plt.show()

# Main function to handle the entire process
if __name__ == "__main__":
    # Step 1: Get user input
    user_choices = get_user_input()

    # Load the merged CSV file with 47 cities and their corresponding values
    file_path = 'Data_Files/Combined.csv'
    try:
        df_merged = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"CSV file not found at: {file_path}. Please ensure the merge process was completed successfully.")
        sys.exit()

    # Step 2: Filter the DataFrame based on user input and display/save it
    final_df, top_city_summary = filter_dataframe(df_merged, user_choices)

    # Step 3: Display table, Heatmap for top 10 cities with summary
    create_combined_visualization(final_df, top_city_summary, user_choices, top_n=10)