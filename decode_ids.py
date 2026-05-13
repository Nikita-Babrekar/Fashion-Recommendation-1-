import pandas as pd

# Load the attributes
df = pd.read_csv("data/fashion_data.csv", usecols=['p_attributes'], nrows=1000)

# Create a dictionary to count occurrences
id_to_shape = {}

for attr in df['p_attributes'].dropna():
    # Convert string representation of dict to real dict
    try:
        d = eval(attr) 
        shape_ids = d.get('Body Shape ID', '')
        top_shape = d.get('Top Shape', d.get('Shape', 'Unknown'))
        
        if shape_ids:
            for s_id in shape_ids.split(','):
                key = s_id.strip()
                if key not in id_to_shape: id_to_shape[key] = []
                id_to_shape[key].append(top_shape)
    except:
        continue

# Print the findings
for s_id, shapes in id_to_shape.items():
    unique_shapes = set(shapes)
    print(f"ID {s_id} is associated with these shapes: {unique_shapes}")