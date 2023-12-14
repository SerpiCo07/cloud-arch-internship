# cloud-arch-internship
This repository is dedicated to the development of a comprehensive cloud architecture designed during my internship program. The project aims to build a serverless scalable, robust and secure  distributed system to compute the long-running executions

Architecture Overview

Application → API Gateway:
The application sends a REST API request to Amazon API Gateway / Google API Gateway

API Gateway → 1st Lambda Function/ Google Function:
The API Gateway routes the request to the 1st Lambda function.

1st Function → EKS/GKE or 3rd  Function:
The 1st  function decides the task type and forwards it to either EKS/GKE (for long-lived tasks) or another function (for short-lived tasks).

EKS/GKE → The 2nd Function (for Long-lived Tasks):
Post-processing, EKS/GKE sends the results to the 2nd  function.

3rd Function → 2nd  Function (for Short-lived Tasks):
The 3rd  function directly sends the processed result to the 2nd function.

2nd  Function → API Gateway:
The 2nd  function sends the final result back to the API Gateway.

API Gateway → Application:
The API Gateway then sends the response back to the application.

Technologies

Cloud Provider: Google Cloud Platform
Scripting: Python

Collaboration Guidelines

Code Reviews: All merges require pull requests and code reviews.
Commit Conventions: Use conventional commits for a clear history and easy navigation

Contact

Intern Developer: Mohammad Tayebi - Mo.tayebi@outlook.com
