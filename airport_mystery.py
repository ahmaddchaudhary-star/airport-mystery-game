import mysql.connector
import random

print("====================================")
print(" AIRPORT MYSTERY: PHANTOM TRAVELER ")
print("====================================")

player = input("Enter your agent name: ")

print(f"\nWelcome Agent {player}.\n")

print("MISSION BRIEFING:")
print("Interpol has issued a global alert about a mysterious criminal known")
print("as 'The Phantom Traveler'. The suspect has been rapidly moving between")
print("international airports to avoid capture.\n")

print("Your mission is to track the suspect and intercept them.")
print("Each round you can gather information or investigate airports.")
print("Use your resources wisely.\n")

input("Press ENTER to begin the investigation...")

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
ORDER BY RAND()
LIMIT 50
""")

airports = cursor.fetchall()

rounds = 5
fuel = 10
time_left = 10
companion_help = 2

criminal_airport = random.choice(airports)

for round_number in range(1, rounds + 1):

    print("\n----------------------------")
    print("Round", round_number)
    print("Fuel:", fuel, "| Time:", time_left)
    print("----------------------------")

    print("\nWhat do you want to do?")
    print("1. Investigate an airport")
    print("2. Check flight records (cost: 1 time)")
    print("3. Ask companion for intelligence (cost: 3 fuel + 3 time)")
    print("4. Skip this round")

    action = input("Choose action: ")

    # Flight records hint
    if action == "2":

        time_left -= 1

        continent = criminal_airport[3]

        continent_names = {
            "EU": "Europe",
            "AS": "Asia",
            "AF": "Africa",
            "NA": "North America",
            "SA": "South America",
            "OC": "Oceania"
        }

        print("\nFlight records show the suspect boarded a plane heading to:",
              continent_names.get(continent, "Unknown region"))

    # Companion intelligence
    elif action == "3" and companion_help > 0:

        companion_help -= 1
        fuel -= 3
        time_left -= 3

        continent = criminal_airport[3]

        print("\nCompanion Intel:")
        print("Interpol satellite tracking suggests the suspect is somewhere in", continent)

    # Investigate airports
    elif action == "1":

        fuel -= 2
        time_left -= 2

        options = random.sample(airports, 4)

        print("\nAirports to investigate:\n")

        for i, airport in enumerate(options):

            city = airport[1].split("(")[0].split("-")[0].strip()
            country = airport[2]

            print(i+1, "-", city + ",", country)

        choice = int(input("\nChoose airport (1-4): "))
        selected = options[choice-1]

        city = selected[1].split("(")[0].split("-")[0].strip()
        country = selected[2]

        print("\nYou investigated:", city + ",", country)

        if selected == criminal_airport:

            print("\nYou found the criminal!")
            print("MISSION COMPLETE")
            break

        else:
            print("\nWrong lead. The suspect already left.")

    # Skip round
    elif action == "4":

        print("\nYou waited for more information.")

    else:
        print("Invalid choice.")

    # Criminal moves
    criminal_airport = random.choice(airports)

    if fuel <= 0 or time_left <= 0:

        print("\nYou ran out of resources.")
        print("The Phantom Traveler escaped.")
        break