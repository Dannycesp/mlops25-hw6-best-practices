#!/bin/bash
set -euo pipefail

# Set dummy AWS credentials
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

# Set S3 endpoint URL
export S3_ENDPOINT_URL=http://localhost:4566

# Set input and output file patterns
export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"

# Activate the Python environment
source ~/environments/.env_dataeng/bin/activate

# Run the integration test
python tests/integration_test.py
