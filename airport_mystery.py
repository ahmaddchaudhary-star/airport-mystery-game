import mysql.connector
import random

print("====================================")
print(" AIRPORT MYSTERY: PHANTOM TRAVELER ")
print("====================================")

player = input("Enter your agent name: ")

print(f"\nWelcome Agent {player}.\n")

print("MISSION BRIEFING:")
print("A criminal known as 'The Phantom Traveler' is moving between")
print("international airports trying to disappear.")
print()
print("Your mission is to investigate airports, gather clues,")
print("and capture the suspect before they escape.")
print()
print("You have limited resources.")
print("Fuel: 10 | Time: 10\n")

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
LIMIT 60
""")

airports = cursor.fetchall()

rounds = 6
fuel = 10
time_left = 10

# Criminal travel route
criminal_route = random.sample(airports, rounds)

caught = False

for round_number in range(1, rounds + 1):

    criminal_airport = criminal_route[round_number - 1]

    print("\n==============================")
    print("Round", round_number)
    print("Fuel:", fuel, "| Time:", time_left)
    print("==============================")

    actions_used = 0

    while True:

        print("\nChoose an action:")
        print("1 Check passenger records (cost 1 time)")
        print("2 Analyze flight paths (cost 1 fuel)")
        print("3 Airport CCTV search (cost 2 time)")
        print("4 Investigate airport (cost 2 fuel + 2 time)")

        action = input("Action: ")

        if action == "1":

            if time_left < 1:
                print("Not enough time.")
                continue

            time_left -= 1
            actions_used += 1

            continent = criminal_airport[3]

            continents = {
                "EU": "Europe",
                "AS": "Asia",
                "AF": "Africa",
                "NA": "North America",
                "SA": "South America",
                "OC": "Oceania"
            }

            print("\nPassenger records indicate the suspect flew to:",
                  continents.get(continent, "unknown region"))

        elif action == "2":

            if fuel < 1:
                print("Not enough fuel.")
                continue

            fuel -= 1
            actions_used += 1

            print("\nFlight path analysis suggests a long international flight.")

        elif action == "3":

            if time_left < 2:
                print("Not enough time.")
                continue

            time_left -= 2
            actions_used += 1

            city = criminal_airport[1]
            city = city.split("(")[0].split("-")[0].strip()

            print("\nAirport CCTV spotted a suspicious traveler")
            print("passing through:", city)

        elif action == "4":

            if fuel < 2 or time_left < 2:
                print("Not enough resources.")
                continue

            fuel -= 2
            time_left -= 2

            # Build investigation options (1 correct + 3 random)
            options = [criminal_airport]

            while len(options) < 4:
                candidate = random.choice(airports)
                if candidate not in options:
                    options.append(candidate)

            random.shuffle(options)

            print("\nAirports to investigate:\n")

            for i, airport in enumerate(options):

                city = airport[1].split("(")[0].split("-")[0].strip()
                country = airport[2]

                print(i+1, "-", city + ",", country)

            try:
                choice = int(input("\nChoose airport (1-4): "))

                if choice < 1 or choice > 4:
                    print("Invalid airport.")
                    continue

            except:
                print("Invalid input.")
                continue

            selected = options[choice - 1]

            city = selected[1].split("(")[0].split("-")[0].strip()
            country = selected[2]

            print("\nYou investigated:", city + ",", country)

            if selected == criminal_airport:

                print("\nYou found the criminal!")
                print("MISSION COMPLETE")

                caught = True
                break

            else:

                print("\nWrong lead. The suspect escaped again.")
                break

        else:
            print("Invalid action.")
            continue

        if actions_used >= 3:
            print("\nYou must make a move now.")
            continue

        if fuel <= 0 or time_left <= 0:
            break

    if caught or fuel <= 0 or time_left <= 0:
        break


print("\n==============================")
print("MISSION SUMMARY")
print("==============================")

if caught:

    print("Result: SUCCESS")
    print("You captured the Phantom Traveler.")

else:

    print("Result: FAILURE")
    print("The suspect escaped.")

print("\nFuel remaining:", fuel)
print("Time remaining:", time_left)

score = fuel + time_left

if score >= 12:
    rating = "EXCELLENT INVESTIGATOR"
elif score >= 7:
    rating = "GREAT DETECTIVE"
elif score >= 3:
    rating = "GOOD EFFORT"
else:
    rating = "BARELY SURVIVED"

print("Rating:", rating)