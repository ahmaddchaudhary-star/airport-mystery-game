import mysql.connector
import random

print("====================================")
print(" AIRPORT MYSTERY: PHANTOM TRAVELER ")
print("====================================")

player = input("Enter your agent name: ")

print(f"\nWelcome Agent {player}.")
print("A criminal is escaping through international airports.")
print("Track them before they disappear.\n")

# connect to database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="flight_game"
)

cursor = connection.cursor()

cursor.execute("""
SELECT name, municipality, iso_country
FROM airport
WHERE type='large_airport'
GROUP BY iso_country
ORDER BY RAND()
LIMIT 10
""")

airports = cursor.fetchall()

print("\nAirports loaded from database:\n")

for airport in airports:
    print(airport)