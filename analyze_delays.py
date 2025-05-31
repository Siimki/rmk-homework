import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Load the CSV file
file_path = "bus_events.csv"
df = pd.read_csv(file_path)

# Convert timestamp to datetime object
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter only 'arrived_zoo' and 'arrived_toompark' events
df = df[df['event'].isin(['arrived_zoo', 'arrived_toompark'])]

# Define scheduled times for zoo and toompark as {hour: [minute list]}
scheduled_zoo = {
    5: [8, 23, 37, 49],
    6: [0, 11, 19, 27, 35, 43, 51],
    7: [0, 9, 17, 26, 35, 45, 54],
    8: [5, 16, 28, 38, 48, 59],
    9: [11, 23, 36, 49],
    10: [2, 15, 30, 45, 56],
    11: [10, 24, 38, 52],
    12: [6, 20, 33, 47],
    13: [1, 15, 29, 43, 57],
    14: [10, 22, 33, 44, 57],
    15: [6, 16, 26, 36, 47, 57],
    16: [7, 16, 26, 38, 51],
    17: [3, 15, 26, 37, 48],
    18: [1, 14, 27, 41, 56],
    19: [10, 25, 40, 54],
    20: [8, 23, 38, 54],
    21: [9, 25, 42, 59],
    22: [16, 32, 49],
    23: [6, 26],
}

scheduled_toompark = {
    5: [17, 32, 46, 58],
    6: [12, 23, 31, 39, 47, 55],
    7: [3, 13, 22, 30, 39, 48, 58],
    8: [7, 18, 30, 41, 51],
    9: [1, 12, 24, 36, 49],
    10: [2, 15, 28, 43, 58],
    11: [9, 23, 37, 51],
    12: [5, 19, 33, 46],
    13: [0, 14, 28, 42, 56],
    14: [11, 24, 36, 47, 58],
    15: [11, 20, 30, 40, 50],
    16: [1, 12, 22, 31, 41, 53],
    17: [6, 18, 30, 41, 52],
    18: [3, 16, 29, 40, 54],
    19: [9, 23, 38, 53],
    20: [6, 20, 35, 50],
    21: [6, 21, 37, 54],
    22: [10, 27, 43],
    23: [0, 16, 35]
}

# Function to get closest scheduled time
def get_closest_scheduled(dt, schedule_dict):
    hour = dt.hour
    if hour not in schedule_dict:
        return None
    scheduled_minutes = schedule_dict[hour]
    closest_minute = min(scheduled_minutes, key=lambda m: abs((dt.minute + dt.second / 60) - m))
    scheduled_time = dt.replace(minute=closest_minute, second=0, microsecond=0)
    return scheduled_time

# Apply matching
df['scheduled_time'] = df.apply(
    lambda row: get_closest_scheduled(
        row['timestamp'], scheduled_zoo if row['event'] == 'arrived_zoo' else scheduled_toompark
    ),
    axis=1
)

# Calculate delay in seconds
df['delay_s'] = (df['timestamp'] - df['scheduled_time']).dt.total_seconds().round().astype(int)

df['timestamp_pretty'] = df['timestamp'].dt.strftime('%H:%M:%S')
df['scheduled_time_pretty'] = df['scheduled_time'].dt.strftime('%H:%M:%S')

# Select relevant columns
result_df = df[['timestamp_pretty', 'scheduled_time_pretty', 'delay_s', 'vehicle_id', 'event']]
# Round delay to seconds for clarity
df['delay_sec'] = (df['timestamp'] - df['scheduled_time']).dt.total_seconds().round()

# Group by event type for separate stats
stats = df.groupby('event')['delay_sec'].agg(
    count='count',
    mean_delay='mean',
    median_delay='median',
    std_delay='std',
    max_delay='max',
    min_delay='min'
).round(1)

print("\nDelay Statistics by Event:")
print(stats)
# Flag delays greater than 10 minutes
df['outlier'] = df['delay_sec'].abs() > 600  
outlier_count = df['outlier'].sum()
print(f"\nNumber of major outliers (delay > 10 min): {outlier_count}")


# Optional: save to CSV
result_df.to_csv("bus_delay_analysis.csv", index=False)
