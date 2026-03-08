import mysql.connector
import random

print("====================================")
print(" AIRPORT MYSTERY: PHANTOM TRAVELER ")
print("====================================")

player = input("Enter your agent name: ")

print(f"\nWelcome Agent {player}.")
print("A criminal is escaping through international airports.")
print("Track them before they disappear.\n")

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
LIMIT 20
""")

airports = cursor.fetchall()

rounds = 5
fuel = 20
time_left = 20

for round_number in range(1, rounds + 1):

    print("\n----------------------------")
    print("Round", round_number)
    print("Fuel:", fuel, "| Time:", time_left)
    print("----------------------------")

    options = random.sample(airports, 4)
    criminal_airport = random.choice(options)

    print("\nPossible airports to investigate:\n")

    for i, airport in enumerate(options):
        print(i+1, "-", airport[0], "(", airport[1], ",", airport[2], ")")

    choice = int(input("\nChoose an airport to investigate (1-4): "))

    selected_airport = options[choice - 1]

    print("\nYou chose to investigate:")
    print(selected_airport[0], "in", selected_airport[1], ",", selected_airport[2])

    if selected_airport == criminal_airport:
        print("\nYou found the criminal! Mission success.")
        fuel -= 1
        time_left -= 1
    else:
        print("\nWrong lead. The criminal escaped this airport.")
        fuel -= 2
        time_left -= 2

    if fuel <= 0 or time_left <= 0:
        print("\nYou ran out of resources.")
        print("The Phantom Traveler escaped.")
        break