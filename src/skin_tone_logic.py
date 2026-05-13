import pandas as pd

def get_pro_recommendation(skin_tone, body_type, data_path="data/fashion_data.csv"):
    color_map = {
        "fair": ["Blue", "Navy Blue", "Silver", "Purple", "Lavender", "Pink", "Fuchsia", "Teal", "Turquoise Blue", "Grey", "Charcoal", "Burgundy", "Off White", "Wine", "Magenta", "Violet", "Rose", "Mauve", "Grey Melange", "Champagne"],
        "medium": ["Mustard", "Olive", "Rust", "Camel Brown", "Coffee Brown", "Tan", "Beige", "Peach", "Gold", "Orange", "Copper", "Khaki", "Green", "Maroon", "Bronze", "Nude", "Taupe", "Rose Gold", "Sea Green", "Yellow"],
        "deep": ["White", "Black", "Red", "Royal Blue", "Coral", "Cream", "Fluorescent Green", "Lime Green", "Tangerine", "Assorted", "Multi", "Turquoise Blue"]
    }
    
    shape_map = {
        "pear": ["Anarkali", "A-Line", "Flared", "High Rise", "Wide Leg"],
        "rectangle": ["Straight", "Regular", "Boxy", "Slim Fit"],
        "inverted_triangle": ["V-Neck", "Halter", "Sleeveless", "Bootcut", "Flared"],
        "apple": ["Empire", "Straight", "Front Slit", "Relaxed Fit"]
    }

    target_colors = color_map.get(skin_tone.lower(), [])
    target_shapes = shape_map.get(body_type.lower(), ["Straight"])

    # INCREASED SEARCH AREA: Looking at 500,000 rows now
    df = pd.read_csv(data_path, usecols=['name', 'colour', 'img', 'brand', 'p_attributes'], nrows=500000)

    color_filtered = df[df['colour'].isin(target_colors)]
    
    # Categories to find
    categories = ['Jacket', 'Top', 'Jeans', 'Tshirt', 'Dress', 'Kurta', 'Shirt', 'Trouser']
    final_list = []
    
    for cat in categories:
        # Find category matches
        cat_matches = color_filtered[color_filtered['name'].str.contains(cat, case=False, na=False)]
        
        def matches_shape(attr_str):
            attr_str = str(attr_str)
            return any(shape.lower() in attr_str.lower() for shape in target_shapes)
        
        shaped_matches = cat_matches[cat_matches['p_attributes'].apply(matches_shape)]
        
        # Grab up to 15 per category to reach that 50+ total
        if not shaped_matches.empty:
            final_list.append(shaped_matches.head(15))
        else:
            final_list.append(cat_matches.head(10))

    if final_list:
        final_results = pd.concat(final_list).drop_duplicates()
    else:
        final_results = color_filtered.head(60)

    # FINAL LIMIT: Set to 60 for a big grid
    return final_results.head(60)