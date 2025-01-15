import sqlite3

# Connect to the old and new databases
conn_old = sqlite3.connect('../old_database.db')
conn_new = sqlite3.connect('../db/database.db')
cur_old = conn_old.cursor()
cur_new = conn_new.cursor()

# cur_new.execute("Update Flavors set flavor_name = 'Mix Vanilla-Ube' where id = 3")
# conn_new.commit()
# exit()

# Fetch all flavors from the old database
old_flavors = cur_old.execute("SELECT * FROM BillItems;").fetchall()
# Insert data into the new database
for old_flavor in old_flavors:
    print("**************************************************")
    bill_id = old_flavor[1]
    old_bill = cur_old.execute(f"SELECT * FROM Bill where id = {bill_id};").fetchone()
    new_bill = cur_new.execute(f"select * from bill where id = {bill_id};").fetchone()
    print(f"Old Bill is {old_bill}")
    print(f"New Bill is {new_bill}")
    print(f"Match {new_bill == old_bill}")

    flavor_type = old_flavor[3]
    old_flavor_type = cur_old.execute(f"Select type from IceCreamType where id = {flavor_type}").fetchone()
    new_flavor_type = old_flavor_type[0]


    flavor_id = old_flavor[2]
    if new_flavor_type == "Cone":
        where_clause = "and is_sundae = 0"
    else:
        where_clause = "and is_sundae = 1"
    old_flavor_name = cur_old.execute(f"Select flavor_name from Flavors where id = {flavor_id}").fetchone()
    new_flavor_name = cur_new.execute(f"select id from Flavors where flavor_name = '{old_flavor_name[0]}' {where_clause}").fetchone()
    flavor_id = new_flavor_name[0]
    print(f"Old flavor = {old_flavor_name}")
    print(f"New flavor = {new_flavor_name}")
    print(f"New Flavor type {new_flavor_type}")


    flavor_size = old_flavor[4]
    old_flavor_size = cur_old.execute(f"Select name from IceCreamSize where id = {flavor_size}").fetchone()
    new_flavor_size = cur_new.execute(f"Select id from IceCreamSize where flavor_id = {flavor_id} and name = '{old_flavor_size[0]}'").fetchone()
    flavor_size = new_flavor_size[0]
    print(f"Old flavor size {old_flavor_size}")
    print(f"New flavor size {new_flavor_size}")
    
    # Use parameterized queries to avoid SQL injection
    cur_new.execute(
        """
        INSERT INTO BillItems (id, bill_id, flavor_id, flavor_type,  flavor_size, base_price, total_price, created_at  )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (old_flavor[0],bill_id,flavor_id,new_flavor_type,flavor_size, old_flavor[5], old_flavor[6], old_flavor[7])  # Map the correct indices
    )
    print("Executedd")

# Commit the changes to the new database
conn_new.commit()

# Verify the inserted data
new_flavors = cur_new.execute("SELECT Count(*) FROM BillItems;").fetchone()
# old_flavors = cur_old.execute("SELECT Count(*) FROM BillItems;").fetchone()
print(old_flavor)
print(new_flavors)

# Close the connections
conn_old.close()
conn_new.close()


