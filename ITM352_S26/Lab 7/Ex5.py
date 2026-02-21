# Create tuples of celebrities and their ages
celebrities_tuple = ("Taylor Swift", "Lionel Messi", "The Weeknd", "Keanu Reeves", "Angelina Jolie")
ages_tuple = (36, 38, 36, 61, 50)

# Create a dictionary with the tuples converted to lists
celebrity_data = {
    "celebrities": list(celebrities_tuple),
    "ages": list(ages_tuple)
}

print(celebrity_data)