# Week 6 — Deploying Containers

## Required Homework/Tasks

## Going to early tag and fill this out after Week 8

### ECS Fargate (Part 1)
- Provision ECS Cluster
- Create ECR repo and push image for backend-flask
- Deploy Backend Flask app as a service to Fargate


### ECS Fargate (Part 2)
- Create ECR repo and push image for fronted-react-js
- Deploy Frontend React JS app as a service to Fargate
- Provision and configure Application Load Balancer along with target groups
- Manage your domain useing Route53 via hosted zone
- Create an SSL cerificate via ACM
- Setup a record set for naked domain to point to frontend-react-js
- Setup a record set for api subdomain to point to the backend-flask
- Configure CORS to only permit traffic from our domain


### Securing Flask
- Secure Flask by not running in debug mode


### Implement Refresh Token Cognito
- Implement Refresh Token for Amazon Cognito


#### Fix Messaging In Production
- Refactor bin directory to be top level

### Fargate - Configuring for Container Insights
- Configure task defintions to contain x-ray and turn on Container Insights
- Change Docker Compose to explicitly use a user-defined network
- Create Dockerfile specfically for production use case
- Using ruby generate out env dot files for docker using erb templates



## Homework Challenges

I did not make time to this week to complete anything extra.
