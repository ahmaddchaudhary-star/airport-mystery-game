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
SELECT airport.name,
       airport.municipality,
       country.name,
       airport.continent
FROM airport
JOIN country ON airport.iso_country = country.iso_country
WHERE airport.type='large_airport'
GROUP BY airport.iso_country
ORDER BY RAND()
LIMIT 20
""")

airports = cursor.fetchall()

rounds = 5
fuel = 20
time_left = 20
companion_help = 2

continent_names = {
    "EU": "Europe",
    "AS": "Asia",
    "AF": "Africa",
    "NA": "North America",
    "SA": "South America",
    "OC": "Oceania"
}

for round_number in range(1, rounds + 1):

    print("\n----------------------------")
    print("Round", round_number)
    print("Fuel:", fuel, "| Time:", time_left, "| Companion Help:", companion_help)
    print("----------------------------")

    options = random.sample(airports, 4)
    criminal_airport = random.choice(options)

    criminal_continent = criminal_airport[3]

    print("\nCLUE:")
    print("The suspect was last seen somewhere in", continent_names.get(criminal_continent, "an unknown region"))

    print("\nPossible airports to investigate:\n")

    for i, airport in enumerate(options):
        city = airport[1].split("(")[0].split("-")[0].strip()
        country = airport[2]
        print(i+1, "-", city + ",", country)

    use_help = input("\nUse companion help? (y/n): ")

    extra_guess = False

    if use_help.lower() == "y" and companion_help > 0:
        companion_help -= 1
        fuel -= 3
        time_left -= 3
        extra_guess = True
        print("\nYour companion analyzes surveillance footage. You get TWO guesses.")

    choice = int(input("\nChoose an airport to investigate (1-4): "))
    selected_airport = options[choice - 1]

    city = selected_airport[1].split("(")[0].split("-")[0].strip()
    country = selected_airport[2]

    print("\nYou chose to investigate:", city + ",", country)

    if selected_airport == criminal_airport:
        print("\nYou found the criminal! Mission success.")
        fuel -= 1
        time_left -= 1
    else:
        print("\nWrong lead.")

        if extra_guess:
            guess2 = int(input("Second guess (1-4): "))
            selected_airport2 = options[guess2 - 1]

            if selected_airport2 == criminal_airport:
                print("\nYou found the criminal! Mission success.")
                fuel -= 1
                time_left -= 1
            else:
                print("\nStill wrong. The criminal escaped.")
                fuel -= 2
                time_left -= 2
        else:
            print("The criminal escaped this airport.")
            fuel -= 2
            time_left -= 2

    if fuel <= 0 or time_left <= 0:
        print("\nYou ran out of resources.")
        print("The Phantom Traveler escaped.")
        break