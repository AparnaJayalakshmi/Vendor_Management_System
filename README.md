# vendor-management-system-django

Develop a Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics

## Prerequisites

- Python (version3.11.1)
- Django (version 5.0.4)
- Django REST Framework

## Installation

# 1. Clone the repository:
   bash:  
   git clone https://github.com/AparnaJayalakshmi/Vendor_Management_System.git  

# 2.Create a virtual environment:
python -m venv venv  
source venv/bin/activate  # For Linux/Mac  
venv\Scripts\activate     # For Windows

cd project-directory (vendor_management_system)

# 3.Database setup:

python manage.py makemigrations  

python manage.py migrate  

# 4.User

py manage.py createsuperuser

## Usage
# 1.Start the server:
python manage.py runserver  

# 2.Access API endpoints:

Vendor API: /vendor/

Purchase Order API: /purchaseorder/  

Historical Performance API: /vendor/performancehistory

Postman is used to test API.

## API Endpoints

Token Authentication
1.Obtain a token:
  .Send a POST request to /api/token/ with your username and password to get a token.
  
●POST /api/token/
Content-Type: application/json
{
    "username": "your_username",
    "password": "your_password"
}

2.Use the token to access endpoints:
  Include the token in the Authorization header of your requests.

●GET /api/vendors/
Authorization: Bearer your_token_here

Vendor API  
● POST /api/vendors/: Create a new vendor. 
 Example Request Body: {
    "name": "ABC Company",
    "contact_details": "1234567890",
    "address": "123 Main Street"
}
● GET /api/vendors/: List all vendors.  
● GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.  
● PUT /api/vendors/{vendor_id}/: Update a vendor's details.  
● DELETE /api/vendors/{vendor_id}/: Delete a vendor 

Purchase Order API  
● POST /api/purchaseorders/: Create a purchase order.  
 Example Request Body:{
    "vendor": 7,
    "items": [{"item": "Item1","price" : 150,"quantity":3}],
   
}
● GET /api/purchaseorders/: List all purchase orders with an option to filter by vendor.
 - Example: `GET /api/purchase_orders/?vendor_id=1`
● GET /api/purchaseorders/{po_id}/: Retrieve details of a specific purchase order.  
● PUT /api/purchaseorders/{po_id}/: Update a purchase order.  
● DELETE /api/purchaseorders/{po_id}/: Delete a purchase order

Update Acknowledgment Endpoint:  
● GET /api/purchaseorders/{po_id}/acknowledge for vendors to acknowledge POs.

Vendor Performance Evaluation  
● GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics  

Historical Performance API  
GET /vendors/<vendor_id>/performancehistory/: Retrieve historical performance for a specific vendor.  
