import pandas as pd

# Create sample data for Edinburgh Cashmere
data = {
    'product_name': [
        'DC Scott Black Scarf',
        'DC Check Red Scarf', 
        'Merino Wrap',
        'Cashmere Jumper',
        'Wool Shawl',
        'Lambswool Scarf',
        'Tartan Scarf'
    ],
    'price': [65, 65, 55, 120, 75, 60, 70],
    'category': ['Cashmere', 'Wool', 'Merino', 'Cashmere', 'Wool', 'Lambswool', 'Wool'],
    'rating': [5, 5, 4, 5, 4, 4, 5],
    'purchases': [450, 380, 290, 210, 320, 280, 350]
}

df = pd.DataFrame(data)
df.to_csv('products.csv', index=False)
print("Data file created: products.csv")