# Dictionaries
# Used to store data values in key value pairs
band = {
    "vocals": "Plant",
    "guitar": "Page"
} 

band2 = dict(vocals="Plant", guitar= "Page")
print(band)
print(band2)
print(type(band))
print(len(band))

# Access items
print(band["vocals"])
print(band.get("guitar"))

# List all keys
print(band.keys())

# list all values
print(band.values())

# list of key/value pairs as tuples
print(band.items())

# Verify a key exists
print("guitar" in band) 
print("triangle" in band) 

# Change values
band["vocals"] = "Coverdale"
band.update({"bass": "JPJ"})
print(band)

# Remove items
print(band.pop("bass"))
print(band) 

band["drums"] = "Bonham"
print(band)
# tuple
print(band.popitem()) 
print(band)
