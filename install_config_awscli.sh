#!/bin/bash

# Configuring the Container
apt-get update
apt install sudo

# Install AWS CLI
echo "Installing AWS CLI..."
sudo apt update
sudo apt install -y awscli

# Configure AWS access key and secret access key
if [[ -z "$AWS_ACCESS_KEY_ID" || -z "$AWS_SECRET_ACCESS_KEY" ]]; then
  echo "Error: AWS access key or secret access key not set in environment variables."
  exit 1
fi

echo "Configuring AWS access key and secret access key..."
aws configure set aws_access_key_id "$AWS_ACCESS_KEY"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set default.region us-east-1
aws configure set default.output json

echo "AWS CLI installation and configuration completed successfully."
