def open_file(filename):
    return open(filename, "r")


def write_file(n_pizzas, team_pizzas, filename):
    file_writer = open(filename, "w")

    file_writer.write(f"{n_pizzas}\n")

    for team in team_pizzas:
        pizzas = ""
        for pizza in team["pizzas"]:
            pizzas += f"{pizza} "
        file_writer.write(f"{team['team_size']} {pizzas}\n")
    file_writer.close()


def parse_line(line, pizza_id):
    split_line = line.split(" ")
    return {
        "id": pizza_id,
        "n_ingredients": int(split_line[0]),
        "ingredients": split_line[1:]
    }


def process_best_match(repited, pizzas, teams, n_pizzas):
    pizzas.sort(key=lambda x: -x["n_ingredients"])

    team_pizza = []

    to_process = {
        2: 2 * teams[2],
        3: 3 * teams[3],
        4: 4 * teams[4],
    }

    tmp_pizzas = n_pizzas

    while tmp_pizzas:
        for team_size, team_quantity in teams.items():

            if not pizzas:
                break

            for quantity in range(team_quantity):
                if team_size in to_process:
                    team = {
                        "team_size": team_size,
                        "pizzas": []
                    }

                    flag = False
                    for tp in team_pizza:
                        if tp["team_size"] > len(tp["pizzas"]) and tp["team_size"] == team_size:
                            tp["pizzas"].append(pizzas[0]["id"])
                            flag = True

                    if not flag:
                        team["pizzas"].append(pizzas[0]["id"])
                        team_pizza.append(team)

                    to_process[team_size] -= 1

                    if not to_process[team_size]:
                        to_process.pop(team_size)

                    pizzas.pop(0)
        tmp_pizzas -= 1
    return len(team_pizza), team_pizza


def process_lines(lines, teams, pizzas):
    repited = []

    # for pizza in lines:
    #    for compared_pizza in lines[pizza["id"]:]:
    #        if pizza["id"] == compared_pizza["id"]:
    #            continue
    #        for ingredient in compared_pizza["ingredients"]:
    #            if ingredient in pizza["ingredients"]:
    #                repited.append((pizza["id"], compared_pizza["id"], ingredient))

    return process_best_match(repited, lines, teams, pizzas)


def get_teams_pizzas(n_teams, n_pizzas, team_size, output):
    if not n_pizzas or n_teams[2] + n_teams[3] + n_teams[4] == 0:
        return output, n_pizzas
    for _ in range(n_teams[team_size]):
        if n_pizzas - team_size == 1:
            continue
        if n_pizzas - team_size >= 0:
            n_pizzas -= team_size
            output.append(team_size)
        n_teams[team_size] -= 1
    if n_pizzas >= 4 and n_teams[4] >= 1:
        return get_teams_pizzas(n_teams, n_pizzas, 4, output)
    return get_teams_pizzas(n_teams, n_pizzas, 2, output)


def select_team_to_deliver(n_pizzas, teams):
    teams, processed_pizzas = get_teams_pizzas(teams, n_pizzas, 3, [])

    type_teams = {
        2: 0,
        3: 0,
        4: 0
    }

    for t in teams:
        type_teams[t] += 1

    return type_teams, n_pizzas - processed_pizzas


def parse_header(header):
    header_data = header.split(" ")
    try:
        header_data.remove("\n")
    except:
        ...

    teams_size = [2, 3, 4]

    n_pizzas = int(header_data[0])

    teams = header_data[1:]
    team_pos = 0
    total_people = 0

    parsed_teams = {
        2: 0,
        3: 0,
        4: 0,
    }

    for team in teams:
        for p in range(int(team)):
            total_people += teams_size[team_pos]
        parsed_teams[teams_size[team_pos]] += int(team)
        team_pos += 1
    return select_team_to_deliver(n_pizzas, parsed_teams)


def read_file(lines):
    is_header = True

    parsed_lines = []

    type_teams = {}
    n_pizzas = 0

    counter = 0
    for line in lines:
        if is_header:
            type_teams, n_pizzas = parse_header(line)
            is_header = False
        else:
            parsed_lines.append(parse_line(line, counter))
            counter += 1
    return process_lines(parsed_lines, type_teams, n_pizzas)


if __name__ == '__main__':
    files = [
        "a_example",
        "b_little_bit_of_everything.in",
        "c_many_ingredients.in",
        "d_many_pizzas.in",
        "e_many_teams.in"
    ]
    for f in files:
        file = open_file(f"datasets/{f}")
        n_pizzas, team_pizzas = read_file(file.readlines())
        write_file(n_pizzas, team_pizzas, f"results/{f}.out")
        print(f"Finished file: {f}")
    print("Finished!")
