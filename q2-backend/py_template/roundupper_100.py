from dataclasses import dataclass
from enum import Enum
from typing import Union, NamedTuple, List
from flask import Flask, request

# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int

# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType

# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system
@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location

# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []

# the POST /entity endpoint adds an entity to your global space database
@app.route('/entity', methods=['POST'])
def create_entity():
    entities = request.get_json()["entities"]
    for entity in entities:
        metadata = None
        if entity["type"] == "space_cowboy":
            metadata = SpaceCowboy(entity["metadata"]["name"], entity["metadata"]["lassoLength"])
        elif entity["type"] == "space_animal":
            metadata = SpaceAnimal(entity["metadata"]["type"])
        location = SpaceEntity.Location(entity["location"]["x"], entity["location"]["y"])
        spaceEntity = SpaceEntity(metadata, location)
        space_database.append(spaceEntity)
    return {}

def pythagoreanDistance(entityA, entityB):
    aX = entityA.location.x
    aY = entityA.location.y
    bX = entityB.location.x
    bY = entityB.location.y
    return ((aX - bX) ** 2 + (aY - bY) ** 2) ** 0.5

def cowboyFromName(name):
    for entity in space_database:
        if type(entity.metadata) is SpaceCowboy and entity.metadata.name == name:
            return entity

# lasooable returns all the space animals a space cowboy can lasso given their name
@app.route('/lassoable', methods=['GET'])
def lassoable():
    name = request.get_json()["cowboy_name"]
    cowboy = cowboyFromName(name)
    lassoableList = []
    for entity in space_database:
        if type(entity.metadata) is SpaceAnimal and pythagoreanDistance(entity, cowboy) <= cowboy.metadata.lassoLength:
            lassoableList.append({
                "location": {
                    "x": entity.location.x,
                    "y": entity.location.y
                },
                "type": entity.metadata.type
            })
    return {"space_animals": lassoableList}

# DO NOT TOUCH ME, thanks :D
if __name__ == '__main__':
    app.run(debug=True, port=8080)