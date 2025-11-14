# Infrastructure as Code with AI: Building Cloud Infrastructure

## Learning Objective
Learn how to use AI assistance to create, manage, and deploy cloud infrastructure using Infrastructure as Code (IaC) tools like Terraform, Docker, Kubernetes, and CI/CD pipelines.

## What is Infrastructure as Code?

Infrastructure as Code (IaC) means managing and provisioning infrastructure through code rather than manual processes:
- **Reproducible** - Same code = same infrastructure
- **Version Controlled** - Track changes like application code
- **Automated** - No manual clicking in consoles
- **Documented** - The code IS the documentation

## Prerequisites
- Basic cloud computing concepts (AWS, Azure, or GCP)
- Docker installed
- Kubernetes (minikube or Docker Desktop) installed
- Terraform installed
- GitHub account for CI/CD
- GitHub Copilot or similar AI assistant

---

## Part 1: Docker - Containerization Basics

### Exercise 1.1: Creating a Dockerfile

**Scenario:** Containerize a Python Flask application

**Application Code (app.py):**
```python
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Docker!',
        'environment': os.getenv('ENV', 'development')
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Exercise:** Ask AI to create a Dockerfile

**Prompt:**

```txt
Create a production-ready Dockerfile for this Flask application:

Requirements:
- Use Python 3.11
- Multi-stage build (smaller final image)
- Non-root user for security
- Minimal base image (alpine)
- Layer caching optimization
- Health check
- Environment variable support

Application requirements:
- flask==3.0.0
- gunicorn==21.2.0
```

**Expected Dockerfile:**

```dockerfile
# Build stage
FROM python:3.11-alpine AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-alpine

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application
COPY --chown=appuser:appuser app.py .

# Set user
USER appuser

# Environment
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV ENV=production

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

**Build and Run:**

```bash
# Build
docker build -t flask-app:latest .

# Run
docker run -d -p 5000:5000 --name flask-app flask-app:latest

# Test
curl http://localhost:5000

# Check logs
docker logs flask-app

# Stop
docker stop flask-app
docker rm flask-app
```

---

### Exercise 1.2: Docker Compose for Multi-Container Apps

**Scenario:** Web app + PostgreSQL + Redis

**Prompt:**

```txt
Create a docker-compose.yml for a full-stack application:

Services:
1. Web (Flask app from above)
    - Depends on db and cache
    - Environment: production
    - Restart policy: always

1. PostgreSQL database
    - Version: 15-alpine
    - Volume for persistence
    - Environment variables for credentials
    - Health check

1. Redis cache
    - Version: 7-alpine
    - Volume for persistence

1. Nginx reverse proxy
    - Route traffic to web service
    - SSL termination
    - Rate limiting

Include:
- Named volumes
- Custom network
- Health checks
- Resource limits
- Logging configuration
```

**Expected docker-compose.yml:**

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    networks:
      - frontend
    restart: always
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 128M

  web:
    build: .
    environment:
      - ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/appdb
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    networks:
      - frontend
      - backend
    restart: always
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    restart: always
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - backend
    restart: always
    command: redis-server --appendonly yes
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

**Usage:**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Scale web service
docker-compose up -d --scale web=5

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Part 2: Kubernetes - Container Orchestration

### Exercise 2.1: Kubernetes Deployment

**Scenario:** Deploy Flask app to Kubernetes

**Prompt:**

```txt
Create Kubernetes manifests for the Flask application:

1. Deployment
   - 3 replicas
   - Rolling update strategy (maxUnavailable: 1, maxSurge: 1)
   - Resource requests: 100m CPU, 128Mi memory
   - Resource limits: 500m CPU, 512Mi memory
   - Liveness and readiness probes
   - Environment variables from ConfigMap and Secret

1. Service
   - Type: ClusterIP
   - Port 80 -> Container port 5000

1. ConfigMap
   - Application configuration

1. Secret
   - Database credentials (base64 encoded)

1. HorizontalPodAutoscaler
   - Min: 3, Max: 10 replicas
   - Target CPU: 70%

Use proper labels and selectors.
```

**deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
  labels:
    app: flask-app
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
        version: v1
    spec:
      containers:
      - name: flask-app
        image: flask-app:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5000
          name: http
          protocol: TCP

        env:
        - name: ENV
          valueFrom:
            configMapKeyRef:
              name: flask-config
              key: environment
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: flask-secrets
              key: database-url

        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi

        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3

        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          successThreshold: 1
          failureThreshold: 3

        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true

      restartPolicy: Always
```

**service.yaml:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
  labels:
    app: flask-app
spec:
  type: ClusterIP
  selector:
    app: flask-app
  ports:
  - name: http
    port: 80
    targetPort: 5000
    protocol: TCP
  sessionAffinity: None
```

**configmap.yaml:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: flask-config
data:
  environment: "production"
  log_level: "INFO"
  workers: "4"
```

**secret.yaml:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: flask-secrets
type: Opaque
data:
  # echo -n 'postgresql://user:pass@db:5432/app' | base64
  database-url: cG9zdGdyZXNxbDovL3VzZXI6cGFzc0BkYjo1NDMyL2FwcA==
```

**hpa.yaml:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**Deploy:**

```bash
# Apply all manifests
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml

# Check status
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get hpa

# Check logs
kubectl logs -l app=flask-app -f

# Port forward to test
kubectl port-forward service/flask-app-service 8080:80

# Test
curl http://localhost:8080
```

---

### Exercise 2.2: Kubernetes Ingress

**Prompt:**

```txt
Create an Ingress resource for the Flask app:

Requirements:
- Host: api.example.com
- Path: /api/v1
- TLS enabled with cert-manager
- Rate limiting: 100 req/min per IP
- CORS headers
- Request timeout: 30s

Also create:
- Certificate resource (cert-manager)
- NetworkPolicy (allow ingress from nginx only)
```

**ingress.yaml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: flask-app-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/limit-rps: "10"
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "*"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "30"
spec:
  tls:
  - hosts:
    - api.example.com
    secretName: flask-app-tls
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /api/v1
        pathType: Prefix
        backend:
          service:
            name: flask-app-service
            port:
              number: 80
```

**certificate.yaml:**
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: flask-app-cert
spec:
  secretName: flask-app-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - api.example.com
```

**networkpolicy.yaml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: flask-app-netpol
spec:
  podSelector:
    matchLabels:
      app: flask-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 5000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
```

---

## Part 3: Terraform - Cloud Infrastructure

### Exercise 3.1: AWS Infrastructure with Terraform

**Scenario:** Deploy a 3-tier web application on AWS

**Prompt:**

```txt
Create Terraform configuration for AWS:

1. VPC
   - CIDR: 10.0.0.0/16
   - 3 public subnets (web tier)
   - 3 private subnets (app tier)
   - 3 private subnets (db tier)
   - Across 3 availability zones

1. EC2 instances
   - Auto Scaling Group for web servers
   - Application Load Balancer
   - Launch template with user data

1. RDS PostgreSQL
   - Multi-AZ deployment
   - Encrypted storage
   - Automated backups

1. ElastiCache Redis
   - Replication group
   - Automatic failover

1. S3 bucket
   - For static assets
   - CloudFront distribution

1. Security groups
   - Proper ingress/egress rules
   - Least privilege

Include proper tagging, variables, and outputs.
```

**main.tf:**
```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "Terraform"
    }
  }
}
```

**variables.tf:**
```hcl
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "flask-app"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.medium"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}
```

**vpc.tf:**
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.project_name}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = [
    "10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24",  # App tier
    "10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24" # DB tier
  ]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]  # Web tier

  enable_nat_gateway = true
  single_nat_gateway = false  # One NAT per AZ for HA

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Terraform = "true"
    Environment = var.environment
  }

  public_subnet_tags = {
    Tier = "web"
  }

  private_subnet_tags = {
    Tier = "app-db"
  }
}
```

**security_groups.tf:**

```hcl
# ALB Security Group
resource "aws_security_group" "alb" {
  name_prefix = "${var.project_name}-alb-"
  description = "Security group for Application Load Balancer"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP from internet"
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS from internet"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# EC2 Security Group
resource "aws_security_group" "web" {
  name_prefix = "${var.project_name}-web-"
  description = "Security group for web servers"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5000
    to_port         = 5000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
    description     = "HTTP from ALB"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# RDS Security Group
resource "aws_security_group" "rds" {
  name_prefix = "${var.project_name}-rds-"
  description = "Security group for RDS PostgreSQL"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
    description     = "PostgreSQL from web servers"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Redis Security Group
resource "aws_security_group" "redis" {
  name_prefix = "${var.project_name}-redis-"
  description = "Security group for ElastiCache Redis"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
    description     = "Redis from web servers"
  }

  lifecycle {
    create_before_destroy = true
  }
}
```

**rds.tf:**
```hcl
resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet"
  subnet_ids = slice(module.vpc.private_subnets, 3, 6)  # DB tier subnets

  tags = {
    Name = "${var.project_name}-db-subnet"
  }
}

resource "aws_db_instance" "postgresql" {
  identifier     = "${var.project_name}-postgres"
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = var.db_instance_class

  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = "appdb"
  username = var.db_username
  password = var.db_password

  multi_az               = true
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  deletion_protection = true
  skip_final_snapshot = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot"

  tags = {
    Name = "${var.project_name}-postgresql"
  }
}
```

**elasticache.tf:**
```hcl
resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.project_name}-cache-subnet"
  subnet_ids = slice(module.vpc.private_subnets, 0, 3)  # App tier subnets
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id       = "${var.project_name}-redis"
  replication_group_description = "Redis cluster for ${var.project_name}"

  engine               = "redis"
  engine_version       = "7.0"
  node_type            = "cache.t3.medium"
  num_cache_clusters   = 2

  port                 = 6379
  parameter_group_name = "default.redis7"

  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis.id]

  automatic_failover_enabled = true
  multi_az_enabled          = true

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true

  snapshot_retention_limit = 5
  snapshot_window         = "03:00-05:00"

  tags = {
    Name = "${var.project_name}-redis"
  }
}
```

**outputs.tf:**
```hcl
output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = aws_db_instance.postgresql.endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
  sensitive   = true
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}
```

**Usage:**

```bash
# Initialize
terraform init

# Plan
terraform plan -var="db_username=admin" -var="db_password=SecurePass123!"

# Apply
terraform apply -var="db_username=admin" -var="db_password=SecurePass123!"

# Show outputs
terraform output

# Destroy
terraform destroy
```

---

## Part 4: CI/CD Pipelines

### Exercise 4.1: GitHub Actions Pipeline

**Prompt:**

```txt
Create a complete CI/CD pipeline using GitHub Actions:

Stages:
1. Lint (Python black, flake8)
2. Test (pytest with coverage)
3. Security scan (bandit, safety)
4. Build Docker image
5. Push to registry (Docker Hub)
6. Deploy to staging (Kubernetes)
7. Integration tests
8. Deploy to production (manual approval)

Requirements:
- Matrix build (Python 3.10, 3.11)
- Cache dependencies
- Artifacts for coverage reports
- Notifications on failure
- Deploy only on main branch
- Semantic versioning for releases
```

**.github/workflows/ci-cd.yml:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ created ]

env:
  REGISTRY: docker.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    name: Lint Code
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: Install dependencies
      run: |
        pip install black flake8 isort mypy

    - name: Run Black
      run: black --check .

    - name: Run Flake8
      run: flake8 . --max-line-length=88

    - name: Run isort
      run: isort --check-only .

    - name: Run mypy
      run: mypy . --ignore-missing-imports

  test:
    name: Test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml --cov-report=html

    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

    - name: Archive coverage reports
      uses: actions/upload-artifact@v3
      with:
        name: coverage-reports
        path: htmlcov/

  security:
    name: Security Scan
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install security tools
      run: |
        pip install bandit safety

    - name: Run Bandit
      run: bandit -r . -ll

    - name: Check dependencies
      run: safety check --json

    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: Upload Trivy results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [lint, test, security]
    if: github.event_name != 'pull_request'

    steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.example.com

    steps:
    - uses: actions/checkout@v4

    - name: Set up kubectl
      uses: azure/setup-kubectl@v3

    - name: Configure kubectl
      run: |
        echo "${{ secrets.KUBECONFIG_STAGING }}" | base64 -d > kubeconfig.yaml
        export KUBECONFIG=kubeconfig.yaml

    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/flask-app \
          flask-app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          --namespace=staging

        kubectl rollout status deployment/flask-app \
          --namespace=staging \
          --timeout=300s

    - name: Run smoke tests
      run: |
        sleep 30
        curl -f https://staging.example.com/health || exit 1

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://api.example.com

    steps:
    - uses: actions/checkout@v4

    - name: Set up kubectl
      uses: azure/setup-kubectl@v3

    - name: Configure kubectl
      run: |
        echo "${{ secrets.KUBECONFIG_PROD }}" | base64 -d > kubeconfig.yaml
        export KUBECONFIG=kubeconfig.yaml

    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/flask-app \
          flask-app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
          --namespace=production

        kubectl rollout status deployment/flask-app \
          --namespace=production \
          --timeout=300s

    - name: Run smoke tests
      run: |
        sleep 30
        curl -f https://api.example.com/health || exit 1

    - name: Notify on success
      if: success()
      uses: slackapi/slack-github-action@v1
      with:
        webhook-url: ${{ secrets.SLACK_WEBHOOK }}
        payload: |
          {
            "text": "Production deployment successful: ${{ github.sha }}"
          }

    - name: Notify on failure
      if: failure()
      uses: slackapi/slack-github-action@v1
      with:
        webhook-url: ${{ secrets.SLACK_WEBHOOK }}
        payload: |
          {
            "text": "Production deployment failed: ${{ github.sha }}"
          }
```

---

## Success Criteria

After completing this exercise, you should be able to:

- [ ] Create production-ready Dockerfiles
- [ ] Write docker-compose configurations
- [ ] Deploy applications to Kubernetes
- [ ] Write Terraform configurations for cloud infrastructure
- [ ] Create CI/CD pipelines with GitHub Actions
- [ ] Implement security best practices in IaC
- [ ] Use AI effectively for infrastructure code generation
- [ ] Understand infrastructure scaling and HA patterns

## Reflection Questions

1. How does IaC improve infrastructure management?
1. What challenges did you face with AI-generated configs?
1. How would you secure sensitive values in production?
1. What monitoring would you add to this setup?
1. How would you handle disaster recovery?

## Further Practice

- Add monitoring with Prometheus and Grafana
- Implement blue-green deployments
- Create multi-region infrastructure
- Add disaster recovery procedures
- Implement Infrastructure testing (Terratest, conftest)
- Set up logging aggregation (ELK stack)

Remember: **Infrastructure as Code is about reproducibility, automation, and treating infrastructure like software!**
