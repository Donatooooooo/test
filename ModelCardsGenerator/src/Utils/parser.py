from Utils.exceptions import ParserError
import re

def parser():
    pattern = re.compile(r"^integrate (.+)$")
    
    data = {}
    current = None
    parsing = False
    with open("ModelCardsGenerator/Data/main.md", "r") as main:
        for line in main:
            line = line.strip()
            
            if line == "## Your Commands Below":
                parsing = True
                continue

            if parsing and not line:
                continue

            if parsing:
                match = pattern.match(line)
                if match:
                    current = match.group(1)
                    data[current] = []
                elif current and line.startswith("/"):
                    data[current].append(line[1:])
                    if "/" in line[1:]:  
                        raise ParserError(f"check line -> {line}")
                elif not current:
                    raise ParserError(f"check command -> {line}") 
                elif not line.startswith("/"):
                    raise ParserError(f"check line -> {line}")

        for model in data:
            if not data[model]:
                raise ParserError(f"No files specified for Model Card '{model}'")
            for file in data[model]:
                try:
                    open(f"ModelCardsGenerator/Data/{file}", 'r')
                except FileNotFoundError as e:
                    raise ParserError(f"{file} doesn't exist")
                
    return data