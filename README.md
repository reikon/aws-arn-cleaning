
# AWS Resource Cleanup Tool

A Python script that automatically deletes AWS resources by their ARNs (Amazon Resource Names). The script handles resource dependencies and deletes them in the correct order.

## Prerequisites

### AWS Setup

1. Install AWS CLI:
```bash
# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# MacOS
brew install awscli

# Windows
# Download AWS CLI installer from AWS website
```

2. Set up AWS credentials:
```bash
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region
- Output format (use json)

### Required Software

- Python 3.x
- Boto3: `pip install boto3`

## Usage

1. Save your AWS ARNs in a text file (`arns.txt`):
```
arn:aws:ec2:region:account:resource/id
arn:aws:ec2:region:account:resource/id
```

2. Run:
```bash
cat arns.txt | python arnclean.py
```

## What It Deletes

Deletes these resources in order:
1. Subnets
2. Internet Gateways
3. Route Tables
4. Network ACLs
5. Security Groups
6. VPCs
7. DHCP Options

## ⚠️ Warning

This script permanently deletes AWS resources. Double-check your ARNs before running!

## License

MIT License

Copyright (c) 2025 reikon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author

reikon (GitHub)

## Support

Open an issue on GitHub if you need help or find a bug.
```
