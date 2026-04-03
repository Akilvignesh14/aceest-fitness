# ACEest Fitness & Performance Management System (v3.2.4)

## Project Overview
ACEest is a professional-grade Performance Management System designed for fitness coaches. It transitions from basic data entry to a **Relational ERP (Enterprise Resource Planning)** model, featuring automated AI-style program generation, time-series progress tracking, and PDF report exporting.

## Core Features
* **Role-Based Access Control (RBAC):** Secure login system with Admin and Coach roles.
* **Relational Persistence:** Powered by SQLite with a normalized 5-table schema (Clients, Workouts, Exercises, Metrics, Progress).
* **Data Visualization:** Dynamic Matplotlib integration for tracking client adherence and weight trends.
* **AI Program Generator:** Randomized logic-based workout creation based on client experience levels.
* **Professional Reporting:** Automated PDF generation using the FPDF library.

## Technical Architecture & SRE Practices
This project follows a **Rigorous Software Lifecycle** with a focus on environmental resilience:
* **CI/CD Pipeline:** Automated testing via GitHub Actions (Ubuntu-latest).
* **Environment Awareness:** The application detects "Headless" environments (like CI runners) and automatically switches to an **In-Memory SQLite DB** and bypasses UI-blocking dialogs to ensure 100% build stability.
* **Containerization Readiness:** Includes a Docker-ready workflow for consistent deployment.

## Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd aceest-fitness