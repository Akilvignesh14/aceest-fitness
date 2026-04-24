# ACEest Fitness & Gym: Automated CI/CD Pipeline
**Course:** Introduction to DevOps (CSIZG514/SEZG514/SEUSZG514)  
**Student Name:** Akil Vignesh L  
**Student ID:** 2025HT66023  
**Git URL:** https://github.com/Akilvignesh14/aceest-fitness
---

## Project Overview
ACEest is a professional-grade Gym Management System transitioned from a foundational Python script to a robust, containerized Flask web application. This project serves as a comprehensive demonstration of modern DevOps methodologies, including Version Control (Git), Unit Testing (Pytest), Containerization (Docker), and CI/CD Orchestration (GitHub Actions & Jenkins).

## Core Phase Implementations

### 1. Application Development & Modularization
The system has been refactored into a **Flask Web Service**. It exposes critical service endpoints for fitness management, including a foundational status check and a modular client-retrieval system powered by a relational SQLite backend.

### 2. Version Control System (VCS) Strategy
The repository follows industry-standard semantic versioning (v1.0.0 through v3.2.4). Each milestone is documented with descriptive commit messages, and a strict tagging strategy is used to mark stable release candidates.

### 3. Unit Testing & Validation Framework
Integrated the **Pytest** framework to validate internal logic. The test suite includes:
* **Positive Testing:** Validating successful 200 OK responses and data integrity.
* **Negative Testing:** Ensuring robust 404 error handling for non-existent records.
* **Database Isolation:** Using an idempotent test-database fixture to ensure environmental purity.

### 4. Containerization with Docker
The application is encapsulated in an optimized **Docker Image** (`python:3.9-slim`). This ensures "write once, run anywhere" consistency, effectively eliminating the "it works on my machine" syndrome during deployment.

### 5. Automated CI/CD via GitHub Actions & Jenkins
The project implements a dual-layer build strategy:
* **GitHub Actions:** Triggers on every `push` or `pull_request` to execute the **Build & Lint**, **Automated Testing**, and **Docker Assembly** stages.
* **Jenkins Quality Gate:** Configured to serve as the primary BUILD environment, pulling the latest code from GitHub to perform a secondary validation layer, ensuring code integrity in a controlled build environment.

---

## Local Setup & Execution Instructions

1. **Clone the Repository:**
   ```bash
   git clone <your-public-repo-url>
   cd aceest-fitness