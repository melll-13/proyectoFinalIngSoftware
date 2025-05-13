# Dental Clinic Management System - Final Project

A web-based application designed to streamline operations within dental clinics by digitizing and centralizing clinic management processes. This system facilitates appointment scheduling, patient admissions, billing, and discharge processes, enhancing efficiency for administrators, doctors, and patients alike.

---

## Features

- **Role-Based Access Control**: Interfaces and permissions for Admins, Doctors, and Patients  
- **Appointment Management**: Patients can request appointments; Admins can approve or reject them  
- **Patient Admissions**: Admins can admit new patients and assign them to doctors  
- **Billing and Invoicing**: Automated invoice generation upon patient discharge  
- **Doctor-Patient Assignment**: Doctors can view and manage their assigned patients  
- **User-Friendly Interface**: Intuitive dashboards tailored to each user role  

---

## Technology Stack

- **Backend**: Django (Python)  
- **Database**: SQLite (via Django ORM)  
- **Frontend**: HTML & CSS  
- **No JavaScript used**  

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/melll-13/proyectoFinalIngSoftware.git
   cd proyectoFinalIngSoftware

2. **Apply Migrations**
    ```bash
    python manage.py migrate
   
3. **Run the Development Server**
    ```bash
    python manage.py runserver

4. **Access the App**
   Open your browser and go to: http://127.0.0.1:8000/

## Usage 
- **Admin**: Log in with  credentials. Manage doctors, patients, appointments, and invoices
- **Doctor**: Log in after admin approval. View assigned patients and appointments
- **Patient**: Register and wait for approval. Request appointments and view/download invoices




  
