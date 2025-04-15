# Change Request Management System

A web-based application built with Python and Panel for submitting and querying change requests, integrated with a backend database and AI-powered query processing.

## Table of Contents

*   [Overview](#overview)
*   [Features](#features)
*   [Installation](#installation)
*   [Usage](#usage)

## Overview

The Change Request Management System is designed to streamline the process of submitting and analyzing change requests for projects. It provides two main interfaces:

*   **Change Request Form**: Allows users to submit detailed change requests with cost items, which are sent to a backend API.
*   **Database Query**: Enables users to query the change request database using natural language, powered by an AI model via the Together API.

The application features a user-friendly interface built with Panel, a Python library for creating web-based dashboards.

## Features

*   **Form Submission**:
    *   Input fields for project details, requester information, and change descriptions.
    *   Dynamic cost item entries with hours and dollar impacts.
    *   Automatic generation of unique change request numbers.
    *   Validation for required fields and success/error notifications.
*   **Database Query**:
    *   Chat-based interface for querying change request data.
    *   Integration with Together API for natural language processing.
    *   Caching of responses to improve performance.
*   **Custom Theme**:
    *   Customizable CSS for branding and styling.
*   **Responsive Design**: Adapts to different screen sizes using Panel's layout system.

## Installation

Follow these steps to set up the project locally:

1.  **Clone the Repository**:
    
    ```
    git clone https://github.com/your-username/change-request-system.git
    cd change-request-system
    ```
    
2.  **Create a Virtual Environment**:
    
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
    
3.  **Install Dependencies**:
    
    ```
    pip install -r requirements.txt
    ```
    
4.  **Set Up Environment Variables**:
    
    Create a `.env` file in the project root and add your Together API key:
    
    ```
    TOGETHER_API_KEY=your-api-key-here
    ```
    
5.  **Backend Setup**:
    
    Ensure the backend API is running at `http://127.0.0.1:8000/change_requests` and the SQLite database (`change_requests.db`) is available at `../backend/database/change_requests.db`.
    

## Usage

To run the application:

1.  **Start the Backend API** (if not already running):
    
    Refer to your backend documentation for starting the API server.
    
2.  **Run the Panel Application**:
    
    ```
    python main.py
    ```
    
    This will launch a web server, typically at `http://localhost:5006`.
    
3.  **Access the Application**:
    
    Open your browser and navigate to `http://localhost:5006`.
    
4.  **Using the Interfaces**:
    *   **Change Request Form**:
        
        Fill in project details, add cost items, and submit the form. You'll receive a notification on success or error.
        
    *   **Database Query**:
        
        Enter natural language questions about the change request database (e.g., "How many change requests are there?") and receive AI-generated responses.
  
