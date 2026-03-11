import mysql.connector
import random

print("====================================")
print(" AIRPORT MYSTERY: PHANTOM TRAVELER ")
print("====================================")

player = input("Enter your agent name: ")

fuel = 20
time_left = 20
criminals_caught = 0
rounds = 5

last_action = None

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="flight_game"
)

cursor = connection.cursor()

def get_airports(continent):

    cursor.execute("""
    SELECT airport.name,
           airport.municipality,
           country.name,
           airport.continent
    FROM airport
    JOIN country ON airport.iso_country = country.iso_country
    WHERE airport.type='large_airport'
    AND airport.continent = %s
    ORDER BY RAND()
    LIMIT 10
    """, (continent,))

    return cursor.fetchall()


current_location = ("Helsinki Airport","Helsinki","Finland","EU")

route = ["EU","AS","NA","EU","RANDOM"]

for r in range(rounds):

    print("\n==============================")
    print("ROUND", r+1, "/ 5")
    print("Location:", current_location[1] + ", " + current_location[2])
    print("Fuel:", fuel, "| Time:", time_left)
    print("Criminals caught:", criminals_caught)
    print("==============================")

    if route[r] == "RANDOM":

        cursor.execute("""
        SELECT airport.name,
               airport.municipality,
               country.name,
               airport.continent
        FROM airport
        JOIN country ON airport.iso_country = country.iso_country
        WHERE airport.type='large_airport'
        ORDER BY RAND()
        LIMIT 10
        """)

        airports = cursor.fetchall()

    else:

        airports = get_airports(route[r])

    criminal_airport = random.choice(airports)

    options = random.sample(airports,4)

    if criminal_airport not in options:
        options[0] = criminal_airport

    random.shuffle(options)

    actions = {
        "1": "Passenger Records (cost 2 time)",
        "2": "Flight Path Analysis (cost 2 fuel + 6 time)",
        "3": "Airport CCTV (cost 2 fuel + 2 time)",
        "4": "Informant Tip (cost 6 fuel + 4 time)"
    }

    print("\nChoose ONE investigation:\n")

    for key in actions:
        if key != last_action:
            print(key, actions[key])

    action = input("Action: ")

    if action == last_action or action not in actions:
        print("Invalid investigation.")
        continue

    if action == "1":

        if time_left < 2:
            print("Not enough time.")
            continue

        time_left -= 2

        continent_names = {
            "EU":"Europe",
            "AS":"Asia",
            "NA":"North America",
            "SA":"South America",
            "AF":"Africa",
            "OC":"Oceania"
        }

        print("\nPassenger records show travel to:",
              continent_names.get(criminal_airport[3],"Unknown"))

    elif action == "2":

        if fuel < 2 or time_left < 6:
            print("Not enough resources.")
            continue

        fuel -= 2
        time_left -= 6

        print("\nFlight analysis shows a long international route.")

    elif action == "3":

        if fuel < 2 or time_left < 2:
            print("Not enough resources.")
            continue

        fuel -= 2
        time_left -= 2

        city = criminal_airport[1].split("(")[0].split("-")[0].strip()

        print("\nCCTV spotted the suspect heading toward:", city)

    elif action == "4":

        if fuel < 6 or time_left < 4:
            print("Not enough resources.")
            continue

        fuel -= 6
        time_left -= 4

        country = criminal_airport[2]
        letter = country[0]

        print("\nInformant tip: destination country starts with:", letter)

    last_action = action

    print("\nPossible destinations:\n")

    for i, airport in enumerate(options):

        city = airport[1].split("(")[0].split("-")[0].strip()
        country = airport[2]

        print(i+1,"-",city+",",country)

    try:
        choice = int(input("\nChoose airport (1-4): "))
    except:
        print("Invalid input")
        continue

    if choice < 1 or choice > 4:
        print("Invalid choice")
        continue

    selected = options[choice-1]

    fuel -= 2
    time_left -= 2

    city = selected[1].split("(")[0].split("-")[0].strip()
    country = selected[2]

    print("\nTraveling to:",city+",",country)

    if selected == criminal_airport:

        print("✔ Criminal captured!")
        criminals_caught += 1

    else:

        correct_city = criminal_airport[1]
        correct_country = criminal_airport[2]

        print("✖ Wrong location.")
        print("Criminal was in:",correct_city+",",correct_country)

    current_location = selected

    if fuel <= 0 or time_left <= 0:
        print("\nYou ran out of resources.")
        break


print("\n==============================")
print("MISSION SUMMARY")
print("==============================")

print("Criminals caught:",criminals_caught)
print("Fuel remaining:",fuel)
print("Time remaining:",time_left)

if criminals_caught == 5:
    rating = "LEGENDARY AGENT"
elif criminals_caught >= 4:
    rating = "ELITE AGENT"
elif criminals_caught >= 3:
    rating = "GOOD AGENT"
elif criminals_caught >= 2:
    rating = "ROOKIE AGENT"
else:
    rating = "FIRED"

print("Rating:",rating)