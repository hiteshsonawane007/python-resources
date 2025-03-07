def calculate_order_total(items, tax_rate, discount_rate):
    # Initialize total cost
    total = 0  
    
    # Loop through items to calculate cost
    #for key, value in items:
        #print(key, value)
    
    for i in items:
        # Add item cost
        for key,value in i.items():
            print(key,value)
        total = total + (i['price'] * i['quantity'])
    
    # Apply discount
    discount = total * discount_rate  
    total = total - discount  
    
    # Calculate tax
    tax = total * tax_rate  
    total = total + tax  
    
    # Check if free shipping applies
    if total > 100:
        shipping_cost = 0  # Free shipping for orders over $100
    else:
        shipping_cost = 5  # Standard shipping cost
    
    # Add shipping cost
    total = total + shipping_cost  
    
    # Print total cost
    print("The total order cost is:", total)  
    
    # Return total cost
    return total 

items = [{'price': 10, "quantity":5}, {'price': 10, "quantity":5}] 
tax_rate = 0.10
discount_rate = 0.05
calculate_order_total(items, tax_rate, discount_rate)