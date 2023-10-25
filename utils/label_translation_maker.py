import pandas as pd
from pathlib import Path
import pickle 

labels_path = Path('data/Compravo_Classification_082023.xlsx')
label_columns = pd.read_excel(labels_path)[['Kategorieebene 1','Kategorieebene 2','Kategorieebene 3','Kategorieebene 4']]

labels_list = [
    label_columns['Kategorieebene 1'].unique().tolist(), # product categories
    label_columns['Kategorieebene 2'].unique().tolist(), # product categories
    label_columns['Kategorieebene 3'].unique().tolist(),
    label_columns['Kategorieebene 4'].unique().tolist()
]
# remove none value
labels_list = [
    [item for item in sublist if not isinstance(item, float)] 
    for sublist in labels_list
]

english_product_labels_1 = [
    'Kitchen & Enjoyment',
    'At Home',
    'Play & Leisure',
    'Baby & Co.',
    'School & Office',
    'Fashion'
]
english_product_labels_2 = [
    'Cooking & Baking', 'Food Preparation & Storage', 'Kitchen Appliances', 'Food & Drink',
    'Organization & Cleanliness', 'Household Appliances & Personal Care', 'Decoration & Living', 'Balcony & Garden',
    'Books & Co.', 'Toys', 'Games', 'Puzzles', 'Model Building', 'Railway', 'Decoration & Seasonal',
    'Creative & Crafts', 'Sports & Outdoors', 'Audio, Photo, and Games', 'Learning & Play',
    'On the Go & Mobile', 'Furniture & Living', 'Care & Nutrition', 'Writing Tools & Markers',
    'Stationery', 'Drawing, Painting, Crafts', 'Organizing & Filing', 'Office Equipment & School Supplies',
    'Bags & Backpacks', 'Men', 'Babies and Children'
]
english_product_labels_3 = [
    "Baking Molds & Cookie Cutters", "Oven Accessories", "Baking Accessories", "Canning", "Cooking Pots",
    "Oven Forms", "Pans", "Cooking Accessories", "Storage", "Bar Accessories", "Kitchen Helpers", "Knives",
    "Kitchen Accessories", "Weighing & Measuring", "Seasoning & Enhancing", "Slicers", "Egg Cookers",
    "Juicers & Citrus Presses", "Deep Fryers", "Coffee Machines", "Kitchen Machines", "Microwaves", "Blenders",
    "Food Mills", "Raclette, Table Grills & Fondue", "Toasters", "Kettles", "Waffle Irons",
    "Donut & Crêpes Makers", "Other Kitchen Appliances", "Cutlery", "Dishes", "Glasses & Jugs",
    "Jugs, Bottles & Containers", "Serving", "Trash Bins", "Vacuum Cleaners", "Bathroom", "Personal Care",
    "Decoration & Accessories", "Wipers & Cleaning", "Planting & Garden Decor", "Laundry & Ironing Boards",
    "Picnic & Cooling", "Garden Furniture & Accessories", "Grilling", "Hair Care", "Stools & Ladders",
    "Lighting", "Home Textiles", "Shopping", "Irons", "Fans & Air Conditioners", "Dental Care",
    "Other Household Appliances", "Baby & Toddler Books", "Picture Books", "Comics", "Friend Books",
    "Gift Books", "Globes & Atlases", "Children & Youth Books", "Learning Books, School Start & Preschool",
    "Song Books", "Mini Books", "Puzzle Books & Activities", "Non-Fiction and First Knowledge Books",
    "Diaries", "Building & Constructing", "Experimenting & Discovering", "Vehicles & Flyers",
    "Small Items & Novelty Items", "Kitchen & Play Shop", "Plush Toys", "Dolls & Doll Accessories",
    "Race Tracks", "Role Playing Toys", "Musical Instruments", "Collectible Cards and Sets",
    "Game Worlds and Figures", "Technology & Co.", "Board Games", "Chess", "Single Player Games",
    "Educational Games", "Building Puzzles", "3D Puzzles", "up to 50 Pieces", "up to 200 Pieces",
    "up to 500 Pieces", "up to 1000 Pieces", "over 1000 Pieces", "Dice Puzzles", "Other Puzzles",
    "Model Building Aviation & Space", "Model Building Vehicles & Accessories", "Model Building Aircraft",
    "Model Building Buildings", "Model Building Ships", "RC Model Building", "Wooden Railway",
    "Model Railways Gauge 1 & Gauge 0", "Model Railways Gauge H0", "Model Railways Gauge N",
    "Model Railways Gauge Z & Gauge TT", "Model Railway Accessories", "Costumes & Dressing Up",
    "Easter", "Party & Decorations", "Christmas", "Home Accessories & Decorations", "Piggy Banks",
    "Fan Articles", "Travel Suitcases and Toiletry Bags", "Craft & Creative Sets", "Craft Books",
    "Craft Materials & Accessories", "Crafting with Wood and Accessories", "Kneading & Modeling",
    "Creative Activities", "Painting & Accessories", "Jewelry & Cosmetics", "Bead Sets", "Ball Sports",
    "Darts & Archery", "Skill Games", "Children's Vehicles", "Sand & Water Toys", "Toys for Outdoors",
    "Other Outdoor Items", "Sports & Fitness", "Winter Sports", "Audio Devices and Accessories",
    "Movies & Music", "Photo & Video Cameras", "Audiobooks and Audio Plays", "Learning Computers and Tablets",
    "Game Consoles & Games", "Baby & Toddler Toys", "Books & Puzzles", "Walking Aids", "Plush",
    "Ride-Ons & Rocking Animals", "Mobiles", "Car Seats & Co.", "Baby Carriers & Wraps",
    "Strollers & Buggies", "Travel Beds", "Diaper Bags", "Bike Trailers and Bicycle Seats",
    "Children's Furniture & Accessories", "Baby Bouncers & Rocking Animals", "Decoration & Gifts",
    "Mattresses & Bedding", "Play Mats", "Baby Protection", "Bathing & Washing", "Feeding & Eating",
    "Care", "Pacifiers & Accessories", "Breastfeeding", "Changing", "Pencils", "Fountain Pens", "Rollerball Pens",
    "Ink Cartridges", "Ballpoint Pens", "Replacement Leads", "Highlighters", "Chalk Markers", "Felt-Tip Pens",
    "Flipchart and Permanent Markers", "Fineliners and Transparency Markers", "Pads & Notebooks",
    "Notebooks and Sticky Notes", "Calendars & Posters", "Copy Paper and Multifunctional Paper",
    "Letterhead Paper", "Mailing Bags and Envelopes", "Forms and Form Books", "Application Folders",
    "Stickers & Decals", "Replacement Inserts", "Watercolor Sets and Brushes", "Colored Pencils", "Felt Pens",
    "Crayons", "Fabric Pens and Textile Markers", "Drawing Pads", "Chalk & Boards", "Glue & Adhesive",
    "Scissors", "Cardboard & Paperboard", "Rulers & Protractors", "Other Drawing Tools",
    "Binders and Dividers", "Ring Binders and Ring Folders", "Quick Binders and Staple Strips",
    "Corner Fastener Folders", "Index Card Boxes", "Storage Boxes", "Upright Files", "Hole Punches and Staplers",
    "Clear Sleeves and Document Sleeves", "Paper Clips", "Collecting Folders", "Project Folders", "Pen Holders",
    "Calculators", "Ink & Toner", "Sharpeners & Pencil Sharpeners", "Erasers and Correction Rollers",
    "Compasses", "Desk Pads", "Folder Covers", "Tapes and Adhesive Strips",
    "Paper Clips and Tacking Pins", "Magnets and Pins", "Labels", "Other Desk Accessories",
    "School Backpacks & Bags", "Pencil Cases & Pouches", "School Cones", "Bags & Pouches", "Backpacks & School Bags",
    "Shirts & Polos", "Shirts", "Sweatshirts & Hoodies", "Jackets", "Coats", "Pants & Shorts",
    "Suits & Blazers", "Baby Clothing", "Bodies & Jumpsuits", "Tops", "Pants", "Dresses, Skirts",
    "Pajamas", "Rainwear", "Swimwear", "Socks & Tights", "Snowsuits", "Underwear and Nightwear",
    "Accessories", "Shoes", "Jugs & Insulated Containers"
]
english_product_labels_4 = [
    "Cookie Cutters & Pastry Presses", "Bread Baking Forms", "Molds", "Cake Baking Molds", "Baking Sheets & Grates",
    "Baking Accessories", "Decorations", "Pralines & Chocolates", "Mixing Bowls & Measuring Cups", "Preserving Appliances",
    "Preserving Accessories", "Glasses & Bottles", "Roasting Pots", "Cooking Pots", "Milk Pots", "Pressure Cookers",
    "Special Cooking Pots", "Sauce Pans", "Pot Sets", "Universal Cooking Pots", "Kettles", "Baking Dishes", "Roasting Pans",
    "Clay Pots", "Frying Pans", "Grill Pans", "Braisers", "Serving Pans", "Special Pans", "Woks", "Splatter Guards",
    "Lids", "Strainers", "Splash Guards", "Other Cooking Accessories", "Storage Accessories", "Bread Boxes",
    "Food Storage Containers", "Pastry Tins", "Lunch Boxes", "Cake & Pastry Stands", "Storage Jars", "Cocktail Shakers & Accessories",
    "Flasks", "Bottle Pourers & Closures", "Bottle Coolers & Ice Cubes", "Corkscrews & Bottle Openers", "Drinking Straws",
    "Forks & Tongs", "Cookbooks", "Cooking Spoons", "Kitchen Textiles", "Pasta Machines", "Openers & Graters",
    "Presses & Mashers", "Graters & Slicers", "Salad Spinners", "Peelers & Cutters", "Whisks", "Scoops & Lifters",
    "Special Tools", "Utility Knives", "Bread Knives", "Vegetable Knives", "Cheese Knives", "Chef's Knives", "Knife Blocks",
    "Knife Sharpeners", "Knife Sets", "Peeling Knives", "Scissors", "Special Knives", "Pocket Knives", "Stove Covers",
    "Kitchen Utensils", "Cutting Boards", "Kitchen Scales", "Measuring Cups", "Thermometers", "Timers", "Vinegar & Oil Dispensers",
    "Mortars", "Grinders", "Shakers", "Coffee Machines", "Filter Coffee Machines", "Espresso Machines", "Capsule Machines",
    "Coffee Grinders", "Tea Machines", "Coffee Machine Accessories", "Microwaves & Mini Ovens", "Microwave Dishes",
    "Hand Mixers", "Blenders", "Hand Blenders", "Choppers", "Raclette Sets", "Fondue Sets", "Electric Grills",
    "Cutlery Sets", "Steak Cutlery Sets", "Children's Cutlery Sets", "Salad Cutlery Sets", "Forks", "Cake Lifters", "Spoons",
    "Knives", "Butter Dishes", "Tableware Sets", "Egg Cups", "Breakfast Boards & Plates", "Coffee Sets", "Children's Tableware",
    "Milk Jugs & Sugar Bowls", "Bowls & Soup Cups", "Cups & Mugs", "Coffee & Tea Saucers", "Plates", "Beer & Wheat Glasses",
    "Punch Bowls", "Cocktail Glasses", "Long Drink Glasses", "Carafes & Decanters", "Jugs", "Children's Cups & Mugs",
    "Champagne Glasses", "Special Glasses", "Stemmed Glasses & Liqueur Glasses", "Water Glasses", "Wine Glasses", "Whisky Glasses",
    "Coffee Pots", "Coffee Makers", "Milk Frothers", "Teapots & Accessories", "Insulated Jugs", "Insulated Containers",
    "Drinking Bottles", "Coasters", "Bread & Fruit Baskets", "Finger Food & Appetizers", "Plates & Charger Plates",
    "Sauce Boats", "Bowls & Dishes", "Napkins", "Serving Utensils", "Warming Plates & Dishes", "Trays & Tiered Stands",
    "Waste Bins", "Cordless Vacuum Cleaners", "Bathroom Accessories", "Beard Trimmers", "Side Tables and Chairs",
    "Brooms & Dustpans", "Picture Frames & Pictures", "Artificial Plants & Wreaths", "Flower Care", "Flower Pots & Boxes",
    "Upright Vacuum Cleaners", "Boxes", "Ironing Boards", "Camping Dishes", "Christmas Tree Stands", "Decorative Figures",
    "Decorative Materials", "Buckets", "Epilators", "Window Cleaners", "Figurines & Decorative Hangings", "Garden Lighting",
    "Garden Furniture", "Gas Grill", "Watering Cans & Sprayers", "Grill Accessories", "Greeting Cards", "Hair Straighteners",
    "Hair Dryers", "Hand & Bath Towels", "Handheld Vacuum Cleaners", "Stools & Chairs", "Charcoal Grill", "Insect Protection",
    "Candles", "Candle Holders", "Cushions & Blankets", "Crates", "Clothes Hangers", "Baskets", "Personal Care", "Cosmetic Bins",
    "Cool Bags & Boxes", "Lamps", "Lanterns", "LED Lighting", "Candlesticks", "String Lights", "Curling Irons",
    "Magnetic Boards & Key Rails", "Trash Bags", "Trash Systems", "Nose Hair Trimmers", "Party & Decorations", "Scales",
    "Picnic Baskets", "Cleaning Cloths & Co.", "Razors", "Smoking Accessories", "Room Fragrances", "Robot Vacuum Cleaners",
    "Umbrellas & Stands", "Snow Shovels", "Soap Dispensers", "Piggy Banks", "Vacuum Cleaner Bags", "Dusters", "Step Ladders",
    "Bags & Blankets", "Tealights & Lanterns", "Carpets & Mats", "Tablecloths", "Placemats & Runners", "Step Ladders",
    "Door Stoppers & Hooks", "Clocks & Alarm Clocks", "Vases & Bowls", "Bird Food & Houses", "Hot Water Bottles & Pillows",
    "Clothespins & Co.", "Laundry Baskets & Tubs", "Clothes Dryers", "Toilet Brushes", "Weather Stations & Thermometers",
    "Candle Lanterns", "Wipers & Covers", "Picture Books Series", "Stroller Books", "Vehicles, Construction, Farm", "Finger Puppet Books & Books with Motor Elements",
    "For Big Little Kids", "Good Night", "Kiddilight", "Sound Books", "Soft & Sensory Books", "Animals & Nature",
    "Search-and-Find Picture Books", "Dictionaries", "Movie Tie-In Books", "Seasonal Books", "Our Favorites", "Read-Aloud Books",
    "Early Reader Books", "Reading Fun from 8 Years", "Reading Fun from 9 Years", "Reading Fun from 10 Years",
    "Reading Fun for Experienced Readers", "(Wooden) Building Blocks", "Other Building Kits", "Marble Runs", "LEGO®",
    "Metal Construction Kits", "Magnetic Construction Kits", "Interlocking Building Blocks", "Detective Equipment",
    "Experiment Kits", "Binoculars & Telescopes", "Research Equipment", "Microscopes and Magnifying Glasses",
    "Toy Phones & Walkie-Talkies", "Magic Kits", "Toy Cars and Trailers", "Toy Car Accessories", "Planes and Aircraft",
    "Model Vehicles & Miniatures", "RC Model Building", "Bruder", "Parking Garages", "Tops", "Yo-Yos", "Keychains",
    "Snow Globes", "Party Favors and Small Gifts", "Practical Jokes & Miscellaneous", "Play Store and Accessories",
    "Children's Kitchen and Accessories", "Play Food", "Children's Kitchen Appliances", "Plush Toy Keychains", "Magnetic Animals",
    "Stuffed Animals", "Plush Toys with Functions", "Plush Toys from Film & Television", "Steiff Collectibles", "Dress-Up Dolls",
    "Baby Dolls", "Puppet Theatres and Hand Puppets", "Miscellaneous Dolls", "Doll Clothing", "Dollhouses and Accessories",
    "Doll Prams and Buggies", "Doll Accessories and Furniture", "Makeup Heads and Accessories", "Fabric Dolls", "Carrera",
    "Darda", "Hot Wheels", "Siku Racing", "Others", "Doctor's Kits", "Toolkits", "Riders", "Children's Household Appliances",
    "School", "Other Role-Playing Toys", "Wind Instruments", "BoogieBee", "Doremini", "Guitars and Ukuleles",
    "Percussion Instruments", "Keyboards and Keyboards", "Music Accessories", "Bullyland", "Dinosaurs", "Heroes and Action Figures",
    "Playmobil", "Schleich", "Various Play Worlds", "Action Toys", "Batteries & Chargers", "Electronic Toys",
    "Adult Games and Party Games", "Children's Games", "Memory Games", "Card Games and Travel Games", "Family Games",
    "Game Collections", "Escape Games", "Game Accessories", "RC Boats", "RC Vehicles", "RC Aircraft", "Other RC Vehicles & RC Accessories",
    "Vehicles & Characters", "Accessories", "Trains", "Model Railway Electronics", "Model Railway Landscapes", "Costumes for Children",
    "Costumes for Adults", "Cowboys & Indians", "Costume Accessories", "Wigs and Headgear", "Knights", "Masks", "Face Paint",
    "Birthday Candles", "Gift Wrapping", "Party Decorations and Tableware", "Bubbles", "Invitations", "Gift Items",
    "Advent Calendars", "Christmas Articles", "Children's Room Decoration", "Children's Watches and Lighting", "Play Mats",
    "Fretwork, Sawing", "Tools", "Paint by Numbers", "Coloring Books and Puzzle Books", "Painting Accessories",
    "Hair & Nails", "Necklaces & Jewelry", "Other Beauty Items", "Ironing Beads", "Aquabeads", "Beads",
    "Badminton", "Basketball & Volleyball", "Balls", "Soccer", "Foosball & Co.", "Street Hockey", "Tennis", "Table Tennis",
    "Archery", "Darts", "Bocce", "Golf and Croquet", "Other Skill Games", "Stilts", "Marbles", "Bobby Cars and Ride-On Vehicles",
    "Tricycles", "Electric Vehicles", "Bicycles and Accessories", "Inline Skates and Roller Skates", "Balance Bikes",
    "Scooters", "Skateboards", "Foot-Powered Vehicles", "Children's Vehicle Accessories", "Inflatable Animals and Air Mattresses",
    "Swimming Aids", "Wading Pools and Pools", "Sand Toys", "Diving Goggles and Swim Goggles", "Other Water Toys",
    "Sandboxes", "Nets", "Water Balls", "Water Guns and Super Soakers", "Air Pumps and Inflating Accessories",
    "Garden Toys", "Wheelbarrows", "Playhouses and Tents", "Slides & Rockers", "Swings & Accessories", "Kites and Flying Games",
    "Pinwheels", "Soft Dart Blasters and Nerf", "Sidewalk Chalk and Miscellaneous", "Trampolines", "Umbrellas",
    "Flashlights", "Camping Equipment", "Ice Skating", "Sleds & Bobs", "Snow Shovels", "Winter Articles Miscellaneous",
    "Snowboards", "Tonies", "CDs", "Balls & Dice", "Trains and Vehicles", "Grasping Toys & Rattles", "Wooden Toys",
    "Spinning Tops", "Motor Skills Toys and Learning Games", "Play Arches & Play Mats", "Hand & Finger Puppets",
    "Bath Toys (Baby)", "Baby Stacking Games", "Baby Swings and Rocking Animals", "Baby Books", "Non-Fiction & Advice Books",
    "Peg Puzzles", "Cuddly Toys (Baby)", "Comfort Blankets & Snuggle Dolls", "Music Boxes", "Child Seats", "Baby Carriers",
    "Baby Wraps", "Carrier Accessories", "Buggies & Sports Strollers", "Twin and Sibling Strollers", "Combination Strollers",
    "Joggers", "Stroller Accessories", "Footmuffs and Lambskins", "Bike Trailers & Accessories", "Bike Helmets",
    "Bike Seats & Accessories", "Co-Sleepers", "Bed Canopies and Canopy Rods", "Cribs & Accessories", "High Chairs & Accessories",
    "Children's Chairs & Tables", "Children's Room Furniture", "Playpens & Inserts", "Cradles and Moses Baskets",
    "Crawling Mats", "Changing Tables and Dressers", "Storage Boxes", "Baby Albums", "Imprint Sets", "Children's Room Decor",
    "Baby Bedding", "Blankets & Pillows", "Snuggle Blankets & Bed Rolls", "Mattresses", "Night Lights", "Bumpers", "Sleeping Bags",
    "Baby Monitors", "Baby Safety", "Door Gates and Stair Gates", "Bed Rails and Bed Guards", "Bath Toys", "Bath Thermometers",
    "Bathtubs", "Towels & Washcloths", "Potties & Toilet Seats", "Step Stools (Baby)", "Spoons & Cutlery for Babies",
    "Bottles & Nipples", "Baby Dinnerware Sets", "Bibs", "Bowls & Plates", "Sterilizers & Baby Food Warmers",
    "Drinking Cups & Mugs", "Teething Rings & Chains", "Fever Thermometers and Accessories", "Grain Pillows & Hot Water Bottles",
    "Nasal Aspirators", "Grooming Sets", "Baby Tooth Care", "Baby Guides", "Pacifiers", "Pacifier Cases", "Pacifier Chains",
    "Breast Pumps", "Breastfeeding Pillows", "Breastfeeding Pads", "Breastfeeding Accessories", "Radiant Heaters",
    "Molton Cloths and Muslin Diapers", "Changing Pads", "Diaper Pails", "Diapers", "From 1st Grade", "From 5th Grade",
    "Changeable Motifs and Patches", "Magazine Files", "School Bag Accessories", "Pencil Cases", "Pen Holders and Pencil Cases",
    "Sports Bags", "Pouches and Wallets", "Gym Bags", "Scarves & Shawls", "Hats & Caps", "Gloves", "Children's Sunglasses",
    "Baby & Toddler Shoes", "Rain Boots up to Size 30", "Slippers up to Size 30", "Children's Shoes up to Size 30",
    "Crawling Shoes", "Chopsticks", "Bottle Protection & Accessories"]

translated_labels_list = [english_product_labels_1,english_product_labels_2,english_product_labels_3,english_product_labels_4]

print( [len(x) for x in translated_labels_list])
asd

with open('utils/labels_list.pkl', 'wb') as f:
    pickle.dump(labels_list, f)

with open('utils/labels_list_translated.pkl', 'wb') as f:
    pickle.dump(translated_labels_list, f)

with open ('utils/labels_list_translated.pkl','rb') as f:
    labels_list_translated = pickle.load(f)

with open ('utils/labels_list.pkl','rb') as f:
    labels_list = pickle.load(f)

if __name__ == "__main__":
    print(labels_list_translated[3][1])
    print(labels_list[3][1])