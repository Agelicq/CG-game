def load_map(planet_name):
    path = f"level/maps/{planet_name}.txt"
    with open(path, "r") as f:
        return [list(row.strip()) for row in f.readlines()]
