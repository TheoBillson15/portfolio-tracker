from auth import hash_password

print("admin:", hash_password("fbi67"))
print("theo:", hash_password("pineapple342"))
print("guest:", hash_password("guest123"))

