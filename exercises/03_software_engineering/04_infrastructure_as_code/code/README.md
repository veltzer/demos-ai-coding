# Infrastructure as Code - Code Files

This directory contains IaC configuration files for Docker, Kubernetes, Terraform, and CI/CD.

## Directory Structure

```txt
code/
+-- docker/              # Docker configuration
|   +-- app.py                  # Flask application
|   +-- Dockerfile              # Multi-stage Docker build
|   +-- docker-compose.yml      # Multi-container setup
|   +-- requirements.txt        # Python dependencies
+-- kubernetes/          # Kubernetes manifests
|   +-- deployment.yaml         # Application deployment
|   +-- service.yaml            # Service definition
|   +-- configmap.yaml          # Configuration
|   +-- secret.yaml             # Secrets
|   +-- hpa.yaml                # Auto-scaling
+-- terraform/           # Terraform configuration
    +-- main.tf                 # Provider configuration
    +-- variables.tf            # Variable definitions
```

## How to Use

### Docker

```bash
cd docker/

# Build image
docker build -t flask-app:latest .

# Run container
docker run -p 5000:5000 flask-app:latest

# Use Docker Compose
docker-compose up -d
```

### Kubernetes

```bash
cd kubernetes/

# Apply all manifests
kubectl apply -f .

# Check status
kubectl get pods
kubectl get services
```

### Terraform

```bash
cd terraform/

# Initialize
terraform init

# Plan
terraform plan

# Apply
terraform apply
```

See the main `exercise.md` file for detailed instructions.
