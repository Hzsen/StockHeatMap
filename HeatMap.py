import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from data import percentage_changes_df, holdings

# Merging the DataFrames to get the 'Market Value' and 'Percentage Change' in one DataFrame
heatmap_df = holdings.merge(percentage_changes_df, on='Ticker')

# Normalize the square sizes based on market value
max_market_value = heatmap_df['Market Value'].max()
heatmap_df['Square Size'] = heatmap_df['Market Value'] / max_market_value


# Define the color mapping based on the percentage change
def get_color(percentage_change):
    if percentage_change > 3:
        return 'darkgreen'
    elif percentage_change > 2:
        return 'green'
    elif percentage_change > 1:
        return 'lightgreen'
    elif percentage_change < -3:
        return 'darkred'
    elif percentage_change < -2:
        return 'red'
    elif percentage_change < -1:
        return 'lightcoral'
    else:
        return 'grey'


# Apply the color mapping
heatmap_df['Color'] = heatmap_df['Percentage Change'].apply(get_color)

# Now, let's visualize the heatmap
# Setting up the figure and axis
fig, ax = plt.subplots(figsize=(15, 10))

# Initialize the x position for the squares
x_pos = 0

# Loop through the DataFrame and create a square for each ticker
for index, row in heatmap_df.iterrows():
    size = row['Square Size'] * 100  # Scale up the size for visibility
    color = row['Color']
    ticker = row['Ticker']

    # Create a rectangle with the size and color
    rect = patches.Rectangle((x_pos, 0), size, size, color=color)
    ax.add_patch(rect)

    # Add the ticker text inside the rectangle
    ax.text(x_pos + size / 2, size / 2, ticker,
            horizontalalignment='center', verticalalignment='center',
            fontsize=9, color='white' if color in ['darkgreen', 'green', 'darkred', 'red'] else 'black')

    # Increment the x position for the next rectangle
    x_pos += size

# Set the limits of the plot
ax.set_xlim(0, x_pos)
ax.set_ylim(0, max(heatmap_df['Square Size']) * 100)  # Scale up the size for visibility

# Remove the axes for a cleaner look
ax.axis('off')

# Show the plot
plt.show()
