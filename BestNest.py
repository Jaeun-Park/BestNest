import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from Merge_dataset import MergeData  # Make sure MergeData is working as expected

# Clear the cache
st.cache_data.clear()

# Function to filter and display the DataFrame based on user choices
def filter_dataframe(df, choices):
    columns = ['City']  # The 'City' column should always be included

    # Mapping user choices to possible columns
    column_mapping = {
        1: ['Cost of Living Value', 'Cost of Living Score'],
        2: ['Literacy Rate Value', 'Literacy Rate Score'],
        3: ['Crime Cost Value', 'Crime Cost Score'],
        4: ['Air Quality Value', 'Air Quality Score']
    }

    # Add columns to the list only if they exist in the DataFrame
    for choice in choices:
        if choice in column_mapping:
            valid_columns = [col for col in column_mapping[choice] if col in df.columns]
            columns.extend(valid_columns)

    # Check if any columns are selected
    if len(columns) <= 1:  # Only 'City' is included
        raise ValueError("No valid columns selected based on user input.")

    # Filter the DataFrame to only keep the selected columns
    filtered_df = df.loc[:, columns].copy()

    # Add total score and sort
    score_columns = [col for col in filtered_df.columns if 'Score' in col]
    filtered_df["Total Score"] = filtered_df[score_columns].sum(axis=1)
    filtered_df = filtered_df.sort_values(by="Total Score", ascending=False).reset_index(drop=True)
    filtered_df['Rank'] = filtered_df.index + 1

    return filtered_df

# Generate a summary for the top-ranked city
def generate_top_city_summary(df):
    top_city = df.iloc[0]  # Get the first row (top 1 city)
    city_name = top_city['City']

    summary_parts = [f"The Top 1 City has..."]
    if 'Cost of Living Value' in top_city:
        summary_parts.append(f"Cost of living (index in 2021, US average is 100): {top_city['Cost of Living Value']}")
    if 'Crime Cost Value' in top_city:
        summary_parts.append(f"Crime cost (cost per resident in 2022): ${top_city['Crime Cost Value']}")
    if 'Air Quality Value' in top_city:
        summary_parts.append(f"Air quality (number of good air quality days in 2024): {top_city['Air Quality Value']}")
    if 'Literacy Rate Value' in top_city:
        summary_parts.append(f"Literacy rate: {top_city['Literacy Rate Value']}%")

    # Final summary text
    summary_text = '\n'.join(summary_parts)
    return city_name, summary_text

# Heatmap function with inversed color and custom labels, increasing font size for both annotations and scales
def heatmap_chart(df, score_columns):
    fig, ax = plt.subplots(figsize=(18, 10))  # Set the size

    data_to_plot = df[score_columns].set_index(df['City'])

    # Increase annotation size, x/y tick label size, and colorbar label size
    sns.heatmap(data_to_plot, annot=True, cmap='coolwarm_r', 
                cbar_kws={'ticks': [0, 5, 10], 'label': 'Score'},  # Add label for colorbar
                ax=ax, vmin=0, vmax=10, annot_kws={"size": 25},  # Increase annotation font size
                linewidths=0.5)

    # Adjust font sizes for axes and colorbar
    ax.tick_params(axis='x', which='major', labelsize=15)  # x-axis tick label size
    ax.tick_params(axis='y', which='major', labelsize=20)  # y-axis label size
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=25)  # Increase colorbar tick label size
    cbar.set_label('Score', size=25)  # Set colorbar label and increase its font size

    ax.set_ylabel('')  # Hide the 'City' label on the y-axis
    st.pyplot(fig)


# Streamlit Interface
st.title("Best Nest")
st.write('Our product helps you find the perfect city to live in, tailored just for you!\n'
         'Choose what matters most to you from various factors like cost of living, literacy rate, crime cost, and air quality.\n'
         'We will recommend the "Best Nest" city that aligns with your preferences!')

# Step 1: User Input via Streamlit
user_choices = st.multiselect(
    "Select parameters most important to you:",
    options=[1, 2, 3, 4],
    format_func=lambda x: ["Cost of Living", "Literacy Rate", "Crime Cost", "Air Quality"][x-1]
)

if st.button("Analyze"):
    # Step 1: Capture User Input and Save to CSV
    if user_choices:
        # Convert the user choices to a DataFrame and set the column name as '0'
        user_choices_df = pd.DataFrame(user_choices, columns=['0'])

        # Save the DataFrame to a CSV file with column '0' as header and without an index
        user_choices_file_path = 'Data_Files/User_Choices.csv'
        user_choices_df.to_csv(user_choices_file_path, index=False)
            
        try:
            MergeData.mergeData()  # Ensure this method is invoked properly
        except Exception as e:
            st.error(f"Data merging failed: {str(e)}")
            st.stop()

        # Check if the Combined.csv file has been created
        file_path = 'Data_Files/Combined.csv'
        if not os.path.exists(file_path):
            st.error(f"Combined CSV file was not created. Please check the merging process.")
            st.stop()

        # Load the merged dataset
        try:
            df_merged = pd.read_csv(file_path)
            # st.write("Merged data loaded successfully.")
        except FileNotFoundError:
            st.error(f"CSV file not found at: {file_path}.")
            st.stop()

        # Step 2: Filter the DataFrame
        try:
            final_df = filter_dataframe(df_merged, user_choices)
        except ValueError as e:
            st.error(str(e))
            st.stop()

        # Generate summary for the top city
        top_city_name, top_city_summary = generate_top_city_summary(final_df)

        # Step 3: Display components individually

        # Display top city summary
        st.subheader(f"Your Best Nest City: {top_city_name}")
        st.text(top_city_summary)

        # Display top 10 cities in a table (Rank, City, Total Score only)
        st.subheader("Top 10 Cities based on selected parameters")
        total_sum_score = 10 * len(user_choices)

        # Select the relevant columns and rename the "Total Score" column
        top_10_table = final_df[['Rank', 'City', 'Total Score']].head(10)
        top_10_table = top_10_table.rename(columns={'Total Score': f'Overall Score (Out of Total {total_sum_score})'})

        # Convert the "Overall Score" column to integer
        top_10_table[f'Overall Score (Out of Total {total_sum_score})'] = top_10_table[f'Overall Score (Out of Total {total_sum_score})'].astype(int)

        # Hide the index column by resetting the index and passing it to st.dataframe
        # st.dataframe(top_10_table.reset_index(drop=True), hide_index=True)

        # Debug. st.dataframe() function does not recognize the hide_index parameter, which was introduced in a more recent version of Streamlit.
        st.dataframe(top_10_table.reset_index(drop=True))

        # Display heatmap separately
        st.subheader("Heatmap for your Top 10 Cities")
        score_columns = [col for col in final_df.columns if 'Score' in col and col != 'Total Score']
        heatmap_chart(final_df.head(10), score_columns)
    else:
        st.error("Please select at least one parameter.")
