from langchain_community.utilities import SQLDatabase

# Initialize SQL Database connection
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
print("Chinok db->",db)
print("Dialect->", db.dialect)
# Print available table names in the database
print("Tables names-> ",db.get_usable_table_names())

# Execute some test queries to inspect the database content
print("Album-> ",db.run("SELECT * FROM album LIMIT 2")) # AlbumId, Title, ArtistId
print("Artist-> ",db.run("SELECT * FROM artist LIMIT 2")) #ArtistId, Name
print(db.run("SELECT * FROM Invoice AS inv JOIN Customer AS c ON inv.CustomerId=c.CustomerId LIMIT 1"))