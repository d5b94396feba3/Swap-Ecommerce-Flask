## Swap Ecommerce Flask

Ecommerce web application using python and flask framework.In this project SQLAlchemy used for database, Stripe used for payment gateway, and flask-mail used for mail.


### Features

1. Fully Functional Dashboard (user and admin)
2. Fully Responsive
3. Account Managements (user and admin)
4. Cart Managements
5. Mail Verifications
6. Stripe Payment Gateway
7. More....


### Demo 

YouTube : https://youtu.be/wgJmhHc3aTc


### ScreenShot

<table align="center">
    <tr>
        <td align="center">
         <p>Home Page</p>
        <img src="src/static/demos/Home_page.png" alt="Screenshot Home" width="395px" />   
        </td>
        <td align="center">
        <p>Search Results</p>
         <img src="src/static/demos/search.png" alt="Screenshot Search" width="386px" height="506"/>
        </td>
    </tr>
    <tr>
        <td align="center">
           <p>Order Page</p>
           <img src="src/static/demos/customer_carts.png" alt="Screenshot Order" width="300px" height="200"/>
        </td>
	 <td align="center">
        	         <p>Admin dashboard</p>
                <img src="src/static/demos/admin_dashboard.png" alt="Screenshot Admin Dashboard" width="300px" height="200"/>
        </td>
    </tr>
    <tr>
        <td align="center">
        	         <p>Dashboard Products</p>
                <img src="src/static/demos/product_dashboard.png" alt="Screenshot Products" width="300px" height="200"/>
        </td>
        <td align="center">
        	         <p>Dashboard Orders</p>
                <img src="src/static/demos/order_dashboard.png" alt="Screenshot Order List" width="300px" height="200"/>
        </td>
    </tr>
    <tr>
        <td align="center">
        	         <p>Confirm Order</p>
                <img src="src/static/demos/confirm_orders.png" alt="Screenshot Confirm Order" width="300px" height="200"/>
        </td>
        <td align="center">
        	         <p>Dashboard Users</p>
                <img src="src/static/demos/admin_users.png" alt="Screenshot Users" width="300px" height="200"/>
        </td>
    </tr>
</table>

### Usage

1. Requirements

    * <strong>Python</strong> (version 3.0 or above)

2. Installation
```
    pip install -r requirements.txt
```

3. Setup
	
```
  Mail Configuration : 
  
      MAIL_SERVER='smtp.gmail.com' # mail server default gmail 
      MAIL_USERNAME='' # mail server username
      MAIL_PASSWORD='' # mail server password
      MAIL_PORT=465
      MAIL_USE_SSL=True
      MAIL_USE_TLS=False    
```

```
  Stripe Configuration : 
  
      publishable_key='' # publishable_key
      stripe.api_key=''  # stripe api key
```

4. Running
```
     python run.py
```
