
# Type
import sqlite3

# Connect to the old and new databases
conn_old = sqlite3.connect('old_database.db')
conn_new = sqlite3.connect('db/database.db')
cur_old = conn_old.cursor()
cur_new = conn_new.cursor()

# Fetch all flavors from the old database
old_flavors = cur_old.execute("SELECT Flavors.* FROM Flavors join IceCreamType on Flavors.id == IceCreamType.flavor_id where IceCreamType.type = 'Sundae';").fetchall()
print(old_flavors)
# Insert data into the new database
for old_flavor in old_flavors:
    # Use parameterized queries to avoid SQL injection
    cur_new.execute(
        """
        INSERT INTO Flavors (flavor_name, is_deleted,is_activated,  is_sundae )
                VALUES (?, ?, ?, ?);
        """,
        (old_flavor[0], old_flavor[2], old_flavor[3], 1)  # Map the correct indices

    )

# Commit the changes to the new database
conn_new.commit()

# Verify the inserted data
new_flavors = cur_new.execute("SELECT * FROM Flavors where is_sundae = 1;").fetchall()
for flavor in new_flavors:
    print(flavor)

# Close the connections
conn_old.close()
conn_new.close()
