# Description

The following is a simple implementation of a REST API with poor coding practices and no software design. Try to improve this code by applying everything you've learned about software design patterns, clean code, and SOLID principles.

# How to Run

1. **Download Python** from [Python Official Website](https://www.python.org/downloads/).

2. **Install Python** and set up the environment variable.

3. **Open Git Bash.** I recommend using Git Bash for the following steps.

4. **Clone this repository** or unzip the folder and go to the folder

5. **Create a virtual environment** using the following command:
   ```
   python -m venv venv
   ```

6. **Activate the virtual environment** with this command:
   ```
   source venv/bin/activate
   ```

7. **Install Flask** by running:
   ```
   pip install Flask
   ```

8. **Install Flask-RESTful** with the following command:
   ```
   pip install flask_restful
   ```

9. **Download Insomnia** from [Insomnia Website](https://insomnia.rest/download) or Postman


10. **Run** the Flask app with this command:
    ```
    python app.py
    ```

11. **Use Insomnia** or Postman to make requests to the URL provided by the Python app.

Certainly, here are the improved and corrected steps for your API endpoints:

# Endpoints

1. **Login**: Returns a fake token for authentication.
    - **Method**: POST
    - **Path**: /auth

2. **Products**:

   - **Get Products**
     ```
     {
         "method": "GET",
         "path": "/products",
         "authToken": "required"
     }
     ```

   - **Get Product**
     ```
     {
         "method": "GET",
         "path": "/products/productId",
         "authToken": "required"
     }
     ```

   - **Get Products by Category**
     ```
     {
         "method": "GET",
         "path": "/products?category=categoryName",
         "authToken": "required"
     }
     ```

   - **Create Product**
     ```
     {
         "method": "POST",
         "path": "/products",
         "authToken": "required",
         "body": {
             "name": "nameProduct",
             "category": "categoryProduct",
             "price": 9
         }
     }
     ```

3. **Categories**

   - **Get Categories**
     ```
     {
         "method": "GET",
         "path": "/categories",
         "authToken": "required"
     }
     ```

   - **Create Category**
     ```
     {
         "method": "POST",
         "path": "/categories",
         "authToken": "required",
         "body": {
             "name": "nameProduct"
         }
     }
     ```

   - **Delete Category**
     ```
     {
         "method": "DELETE",
         "path": "/categories",
         "authToken": "required",
         "body": {
             "name": "nameProduct"
         }
     }
     ```
