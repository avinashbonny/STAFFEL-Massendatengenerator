import pandas as pd
import random
# Library to create dummy data
from faker import Faker
# Library to calculate geometric distance
import geopy.distance
from datetime import datetime, timedelta
# Library to provide visual interface for data input by user
import tkinter as tk
from tkinter import simpledialog

fake = Faker()

# Defining major German cities. Please add additional cities here
german_cities = {
    "Berlin": (52.5200, 13.4050),
    "Munich": (48.1372, 11.5755),
    "Hamburg": (53.5511, 9.9937),
    "Cologne": (50.9375, 6.9603),
    "Frankfurt": (50.1109, 8.6821),
    "Stuttgart": (48.7758, 9.1829),
    "Düsseldorf": (51.2277, 6.7735),
    "Dortmund": (51.5136, 7.4653),
    "Essen": (51.4556, 7.0116),
    "Leipzig": (51.3397, 12.3731),
    "Bremen": (53.0793, 8.8017),
    "Dresden": (51.0504, 13.7373),
    "Hanover": (52.3759, 9.7320),
    "Nuremberg": (49.4521, 11.0767),
    "Duisburg": (51.4344, 6.7623),
    "Bonn": (50.7374, 7.0982),
    "Münster": (51.9607, 7.6261),
    "Karlsruhe": (49.0069, 8.4037),
    "Mannheim": (49.4896, 8.4677),
    "Augsburg": (48.3705, 10.8978),
    "Wiesbaden": (50.0782, 8.2390),
    "Gelsenkirchen": (51.5177, 7.0857),
    "Mönchengladbach": (51.1805, 6.4428),
    "Braunschweig": (52.2689, 10.5268),
    "Chemnitz": (50.8278, 12.9214),
    "Kiel": (54.3233, 10.1228),
    "Aachen": (50.7753, 6.0839),
    "Halle (Saale)": (51.4829, 11.9676),
    "Magdeburg": (52.1205, 11.6276),
    "Freiburg im Breisgau": (47.9961, 7.8494),
    "Krefeld": (51.3388, 6.5853),
    "Lübeck": (53.8650, 10.6866),
    "Oberhausen": (51.4964, 6.8514),
    "Erfurt": (50.9848, 11.0299),
    "Mainz": (49.9929, 8.2473),
    "Rostock": (54.0924, 12.0991),
    "Kassel": (51.3155, 9.4924),
    "Hagen": (51.3671, 7.4633),
    "Hamm": (51.6747, 7.8150),
    "Saarbrücken": (49.2402, 6.9969),
    "Potsdam": (52.3906, 13.0645),
    "Ludwigshafen am Rhein": (49.4816, 8.4351),
    "Oldenburg": (53.1434, 8.2146),
    "Leverkusen": (51.0456, 7.0048),
    "Osnabrück": (52.2799, 8.0476),
    "Solingen": (51.1657, 7.0832),
    "Heidelberg": (49.3988, 8.6724),
    "Herne": (51.5388, 7.2257),
    "Neuss": (51.2044, 6.6874)
}

# Defining a list of dummy companies
companies = ["Company A", "Company B", "Company C", "Company D", "Company E",
             "Company F", "Company G", "Company H", "Company I", "Company J"]

# Generating distances between cities
city_combinations = [(city1, city2) for city1 in german_cities for city2 in german_cities if city1 != city2]
city_distances = {(city1, city2): geopy.distance.geodesic(german_cities[city1], german_cities[city2]).kilometers
                  for city1, city2 in city_combinations}

# Filtering city pairs by distance currently set to the range 300-500. Please adjust the range here
filtered_city_pairs = {key: value for key, value in city_distances.items() if 300 <= value <= 500}

# User prompt to enter the number of records to generate
root = tk.Tk()
root.withdraw()  # Hide the main window
num_records = simpledialog.askinteger("Input", "Enter the number of shipments to be generated:", parent=root)

# Selecting random city pairs for origin and destination based on the user input
origin_destinations = random.sample(list(filtered_city_pairs.keys()), num_records)

# Defining pallet types. Please add/modify relevant pallet types here
pallet_types = ["Wooden Pallet", "Plastic Pallet", "Metal Pallet"]

# Generating random shipments
shipments_data = []
for i, (origin, destination) in enumerate(origin_destinations[:num_records]):
    # Generating departure and arrival dates
    start_date = datetime.now() + timedelta(weeks=random.randint(8, 10))
    departure_date = fake.date_time_between_dates(start_date, start_date + timedelta(days=7))
    arrival_date = departure_date + timedelta(days=random.randint(2, 5))

    # Generating addresses fields
    start_address = fake.street_address()
    start_postal_code = fake.zipcode()
    start_city = fake.city()
    start_country = "Germany"

    destination_address = fake.street_address()
    destination_postal_code = fake.zipcode()
    destination_city = fake.city()
    destination_country = "Germany"

    # Generating pallet details
    pallet_type = random.choice(pallet_types)
    pallet_amount = random.randint(1, 10)

    # Generating shipment data
    shipments_data.append({
        "Shipment Number": f"S{datetime.now().year}{i + 1}",
        "Tour Number": f"T{datetime.now().year}{i // 10 + 1}",
        "Customer Name": random.choice(companies),
        "Departure Date": departure_date.strftime("%Y%m%d %H:%M:%S"),
        "Origin Company": random.choice(companies),
        "Start Street Address": start_address,
        "Start Postal Code": start_postal_code,
        "Start City": start_city,
        "Start Country": start_country,
        "Arrival Date": arrival_date.strftime("%Y%m%d %H:%M:%S"),
        "Destination Company": random.choice(companies),
        "Destination Street Address": destination_address,
        "Destination Postal Code": destination_postal_code,
        "Destination City": destination_city,
        "Destination Country": destination_country,
        "Goods Description": fake.sentence(nb_words=6, variable_nb_words=True),
        "Pallet Type": pallet_type,
        "Pallet Amount": pallet_amount,
        "Total Weight": random.randint(100, 1000),
        # Please add/modify special equipments here
        "Special Equipment": random.choice([None, "Gabelstapler", "Kran", "Kühlcontainer"])
    })

# Converting shipment data to DataFrame
df = pd.DataFrame(shipments_data)

# Writing DataFrame to Excel file
df.to_excel("Logistics.xlsx", index=False)

print("Data generated successfully!")
