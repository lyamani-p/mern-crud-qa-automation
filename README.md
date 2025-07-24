\# MERN CRUD Auth Project with Automated Tests
\## Project Overview : This repository contains a MERN (MongoDB, Express, React, Node.js) application with:

\- User registration and login with JWT authentication  
\- Task CRUD operations (Create, Read, Update, Delete)  
\- Frontend React app for interacting with tasks  
\- Backend Express API server  
\- Automated UI tests with Playwright (Python)  
\- Automated API tests with Python `requests` library

\## Tech Stack
\- \*\*Backend:\*\* Node.js, Express, MongoDB  
\- \*\*Frontend:\*\* React  
\- \*\*Testing:\*\* Python, Playwright, Requests, Pytest  
\- \*\*Database:\*\* MongoDB (local instance required)  

\## Prerequisites

\- \Node.js
\- \npm
\- \Python 3.10+
\- \MongoDB running locally on default port `27017`  

\## Setup and Run
\### 1. Start Backend Server

```bash
cd mern-crud-auth-master
npm install
npm run dev
This will start the Express backend API server.

2\. Start Frontend Server
Open a new terminal tab/window and run:

```bash
cd mern-crud-auth-master/client
npm install
npm run dev
This will start the React frontend app.

3\. Setup Python Environment and Install Dependencies
Open another terminal window/tab and run:

```bash
cd qa-tests
pip install -r requirements.txt
playwright install

This sets up Python dependencies and Playwright browsers required for UI testing.

Running Tests
UI Tests (Playwright)
To run automated UI tests in headed Chromium browser, run:
```bash
pytest tests/UI --headed

API Tests (Python Requests)
To run the backend API tests, run:
```bash
pytest tests/API/test\_api\_crud.py

These tests cover user registration, login, task CRUD operations, and negative scenarios like invalid inputs and authorization errors.
