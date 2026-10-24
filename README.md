# Zero-Trust Secure Payment Gateway API Architecture on Microsoft Azure

A production-grade, micro-segmented cloud infrastructure deployment hosting a Python (Flask) Mock Payment API linked to an isolated Azure SQL Database backend. This deployment enforces a strict defense-in-depth layout utilizing Private Endpoints, Regional Virtual Network Integration, Network Security Groups, and Azure RBAC Key Vault secret injection.

## 🏗️ Architectural Topology Diagram & Design
All system components communicate securely inside a non-routable private network fabric (`10.0.0.0/16`), preventing all raw public internet exposure to high-risk database data planes and credentials:

*   **`app-subnet` (10.0.1.0/24):** Outbound VNet Integration for App Service compute instances.
*   **`data-subnet` (10.0.2.0/24):** Inbound Private Endpoint connection (`pe-azuresql`) pointing to the database on Port 1433.
*   **`kv-subnet` (10.0.3.0/24):** Inbound Private Endpoint connection (`pe-keyvault`) safeguarding connection string values on Port 443.

## 🛡️ Key "Wow Factor" Enterprise Implementations
*   **Zero-Trust Secrets Lifecycle:** App configuration files contain absolutely no hardcoded SQL server connection details, administrative usernames, or raw passwords. At runtime, the App Service authenticates securely over its private endpoint using a **System-Assigned Managed Identity (RBAC)** to extract configuration keys out of Azure Key Vault memory spaces dynamically.
*   **Micro-Perimeter Network Defense:** Network Security Groups (NSGs) are locked down to isolate internal traffic. `nsg-data-subnet` drops all inbound packets by default unless they originate explicitly from within the application's subnet range on database port 1433.

## ⚙️ Automated CI/CD Pipeline Integration
This repository integrates an automated continuous integration and continuous deployment (**CI/CD**) automation pipeline leveraging **GitHub Actions** (`.github/workflows/azure-deploy.yml`). Upon running a `git push` execution code sequence into the `main` branch, the workflow automatically:
1. Provisions an isolated Ubuntu container engine runner environment.
2. Installs Python 3.10 and validates dependency files (`requirements.txt`).
3. Uses an encrypted Azure Publish Profile token secret to build and hot-deploy the fresh codebase to the live production Azure Web App instances seamlessly.

## 🚀 Technical Core Capabilities Tested
*   Cloud Infrastructure Architecture & Network Partitioning
*   Private Endpoint Interconnection & Private DNS Resolution Routing
*   Network Security Group (NSGs) Stateful Rule Isolation
*   Managed Identity Integration & Cryptographic Secret Access Roles
*   Automated Workflow Pipeline Configuration (GitHub Actions CI/CD)
