-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- Insert default categories
INSERT INTO categories (name, description) VALUES
    ('Soft Drinks', 'Carbonated soft drinks and colas'),
    ('Soda', 'Soda water and carbonated beverages'),
    ('Coffee', 'Coffee and coffee-based beverages'),
    ('Beverages', 'General beverages'),
    ('Beer', 'Beer and alcoholic beverages'),
    ('Creamers', 'Coffee creamers and dairy alternatives'),
    ('Mineral Water', 'Mineral and spring water'),
    ('Juice', 'Fruit juices and juice drinks'),
    ('Tea', 'Bottled and canned tea'),
    ('Milk', 'Dairy milk and milk-based drinks'),
    ('Dairy', 'Other dairy products like yogurt drinks and kefir'),
    ('Energy Drinks', 'Energy and sports drinks'),
    ('Other', 'Other types of beverages')
ON CONFLICT(name) DO NOTHING; 