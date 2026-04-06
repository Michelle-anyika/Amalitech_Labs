-- =============================================================================
-- Sample Data for E-Commerce Database
-- Insert test data into categories, customers, products, orders
-- =============================================================================

-- Insert Categories
INSERT INTO categories (name, description) VALUES
    ('Electronics', 'Electronic devices and gadgets'),
    ('Clothing', 'Apparel and accessories'),
    ('Books', 'Physical and digital books'),
    ('Home & Garden', 'Home and garden products'),
    ('Sports', 'Sports and outdoor equipment')
ON CONFLICT DO NOTHING;

-- Insert Customers
INSERT INTO customers (first_name, last_name, email, phone, address, city, country) VALUES
    ('John', 'Doe', 'john.doe@example.com', '+1234567890', '123 Main St', 'New York', 'USA'),
    ('Jane', 'Smith', 'jane.smith@example.com', '+0987654321', '456 Oak Ave', 'Los Angeles', 'USA'),
    ('Bob', 'Johnson', 'bob.johnson@example.com', '+1122334455', '789 Pine Rd', 'Chicago', 'USA'),
    ('Alice', 'Williams', 'alice.williams@example.com', '+5566778899', '321 Elm St', 'Houston', 'USA'),
    ('Charlie', 'Brown', 'charlie.brown@example.com', '+9988776655', '654 Maple Dr', 'Phoenix', 'USA')
ON CONFLICT DO NOTHING;

-- Insert Products with JSONB metadata
INSERT INTO products (name, category_id, price, stock_quantity, description, metadata) VALUES
    (
        'Laptop Pro',
        1,
        999.99,
        50,
        'High-performance laptop',
        '{"brand": "TechBrand", "processor": "Intel i7", "ram": "16GB", "colors": ["silver", "black"]}'::jsonb
    ),
    (
        'Wireless Earbuds',
        1,
        79.99,
        100,
        'Premium wireless earbuds',
        '{"brand": "AudioPro", "battery": "8 hours", "colors": ["black", "white", "blue"]}'::jsonb
    ),
    (
        'Cotton T-Shirt',
        2,
        29.99,
        200,
        'Comfortable cotton t-shirt',
        '{"material": "100% cotton", "sizes": ["S", "M", "L", "XL"], "colors": ["red", "blue", "green"]}'::jsonb
    ),
    (
        'Denim Jeans',
        2,
        59.99,
        150,
        'Classic blue denim jeans',
        '{"material": "Denim", "sizes": ["28", "30", "32", "34", "36"], "colors": ["blue", "black"]}'::jsonb
    ),
    (
        'Python Programming',
        3,
        39.99,
        75,
        'Learn Python programming basics',
        '{"author": "Expert Developer", "pages": 500, "format": ["hardcover", "ebook"]}'::jsonb
    ),
    (
        'Garden Tool Set',
        4,
        45.99,
        60,
        'Complete garden tool set',
        '{"tools": ["shovel", "rake", "hoe", "spade"], "material": "stainless steel"}'::jsonb
    ),
    (
        'Running Shoes',
        5,
        89.99,
        100,
        'Professional running shoes',
        '{"brand": "SportBrand", "sizes": ["6", "7", "8", "9", "10", "11", "12"], "colors": ["black", "white", "red"]}'::jsonb
    )
ON CONFLICT DO NOTHING;

-- Insert Orders
INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
    (1, NOW() - INTERVAL '30 days', 1079.98, 'delivered'),
    (1, NOW() - INTERVAL '20 days', 150.00, 'delivered'),
    (2, NOW() - INTERVAL '25 days', 89.99, 'shipped'),
    (2, NOW() - INTERVAL '10 days', 179.98, 'confirmed'),
    (3, NOW() - INTERVAL '15 days', 299.96, 'delivered'),
    (4, NOW() - INTERVAL '8 days', 45.99, 'pending'),
    (5, NOW() - INTERVAL '5 days', 1159.97, 'confirmed')
ON CONFLICT DO NOTHING;

-- Insert Order Items (line items)
INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
    (1, 1, 1, 999.99, 999.99),
    (1, 2, 1, 79.99, 79.99),
    (2, 3, 5, 29.99, 149.95),
    (3, 7, 1, 89.99, 89.99),
    (4, 4, 3, 59.99, 179.97),
    (5, 5, 2, 39.99, 79.98),
    (5, 6, 3, 45.99, 137.97),
    (5, 7, 1, 89.99, 89.99),
    (6, 6, 1, 45.99, 45.99),
    (7, 1, 1, 999.99, 999.99),
    (7, 3, 5, 29.99, 149.95),
    (7, 4, 1, 59.99, 59.99)
ON CONFLICT DO NOTHING;

-- Insert Order Status History
INSERT INTO order_status_history (order_id, status, changed_at, notes) VALUES
    (1, 'pending', NOW() - INTERVAL '30 days', 'Order created'),
    (1, 'confirmed', NOW() - INTERVAL '29 days', 'Payment confirmed'),
    (1, 'shipped', NOW() - INTERVAL '28 days', 'Shipped with carrier'),
    (1, 'delivered', NOW() - INTERVAL '26 days', 'Delivered to customer'),
    (2, 'pending', NOW() - INTERVAL '20 days', 'Order created'),
    (2, 'confirmed', NOW() - INTERVAL '19 days', 'Payment confirmed'),
    (2, 'shipped', NOW() - INTERVAL '18 days', 'Shipped'),
    (2, 'delivered', NOW() - INTERVAL '17 days', 'Delivered'),
    (3, 'pending', NOW() - INTERVAL '25 days', 'Order created'),
    (3, 'confirmed', NOW() - INTERVAL '24 days', 'Payment confirmed'),
    (3, 'shipped', NOW() - INTERVAL '22 days', 'In transit'),
    (4, 'pending', NOW() - INTERVAL '10 days', 'Order created'),
    (4, 'confirmed', NOW() - INTERVAL '9 days', 'Payment confirmed'),
    (5, 'pending', NOW() - INTERVAL '15 days', 'Order created'),
    (5, 'confirmed', NOW() - INTERVAL '14 days', 'Payment confirmed'),
    (5, 'shipped', NOW() - INTERVAL '12 days', 'Shipped'),
    (5, 'delivered', NOW() - INTERVAL '10 days', 'Delivered'),
    (6, 'pending', NOW() - INTERVAL '8 days', 'Order created'),
    (7, 'pending', NOW() - INTERVAL '5 days', 'Order created'),
    (7, 'confirmed', NOW() - INTERVAL '4 days', 'Payment confirmed')
ON CONFLICT DO NOTHING;

