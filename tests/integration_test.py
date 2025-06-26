import pandas as pd
from datetime import datetime
import os

# Set dummy AWS credentials
os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'

# Set S3 endpoint URL
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'http://localhost:4566')
os.environ['S3_ENDPOINT_URL'] = S3_ENDPOINT_URL

# Set input and output file patterns
input_file_pattern = "s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
output_file_pattern = "s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
os.environ['INPUT_FILE_PATTERN'] = input_file_pattern
os.environ['OUTPUT_FILE_PATTERN'] = output_file_pattern

# Prepare test data
def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]
columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df_input = pd.DataFrame(data, columns=columns)

# Save test data to S3
input_file = input_file_pattern.format(year=2023, month=1)
options = {
    'client_kwargs': {
        'endpoint_url': S3_ENDPOINT_URL
    }
}
df_input.to_parquet(
    input_file,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)

# Run the batch script
os.system("python homework/batch.py 2023 1")

# Read the output file and verify the result
output_file = output_file_pattern.format(year=2023, month=1)
df_output = pd.read_parquet(output_file, storage_options=options)

print(f"Sum of predicted durations: {df_output['predicted_duration'].sum()}")