# parts through the portion of an email address

#method 1: using split() to separate username an domain
email = input("Enter your email address: ")

parts = email.split("@")
username = parts[0]
domain = parts[1]

print("Username:", username)
print("Domain:", domain)

#method 2: Using index() and slicing
at_symbol_index = email.index("@")
username_manual = email[:at_symbol_index]
domain_manual = email[at_symbol_index + 1:]

print("Username (manual):", username_manual)
print("Domain (manual):", domain_manual)




