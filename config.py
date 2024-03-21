import json

def main(plugins: list) -> None:
    print(f"\nПереданы плагины:\n\t{plugins}")
    with open("config.json") as f:
        data = json.load(f)

    for i, _ in enumerate(data["pawn"]["legacy_plugins"]):
        if plugins[i]:
            data["pawn"]["legacy_plugins"][i] = plugins[i]

    with open("config.json", mode="w") as f:
        json.dump(data, f, indent=4)

    print(f"\nПлагины в config.json (обновлены):\n\t{data['pawn']['legacy_plugins']}")

if __name__ == "__main__":
    plugins = input("Введите плагины через запятую: ")
    main(plugins.split(","))
