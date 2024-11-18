You can use business objects (the instances of the classes from your business model) directly with the rule engine, without converting them to dictionaries.

**Arta** processes mappings in the rules and actions to inject data into functions, as you saw in the [simple example](a_simple_example.md) of this documentation.

## The problem with `dict` serialisation

Let’s consider the following example, representing a `Car` with its `Engine` which itself has attributes.

```python
class Engine:
    power: int
    consumption: int  
    
class Car:
    engine: Engine
```

When following the regular usage of Arta, one would convert an instance of a `Car` to a dictionary with a sort of serializer. A candidate code for this might be:

```python
from typing import Any

def serialize_car_to_dict(car: Car) -> dict[str, Any]:
    return {
        "engine": {
            "power": car.engine.power,
            "consumption": car.engine.consumption
        }
    }
```

!!! tip "When using Pydantic"

    If you use Pydantic, you might directly use the `model_dump` function in order to represent your object as a dictionnary object.

This way, you can write you conditions as follows:

```yaml
conditions:
  HAS_LOWER_CONSUMPTION:
    description: "Whether an engine as a low consumption".
    validation_function: is_value_below_threshold
    condition_parameters:
      value: input.engine.power
      threshold: 10
```

This is where the mapping is important: to go through the `engine` data and access the `power` attribute. We serialised the object in a custom code but there might be a better solution with less code…

## Transform any business object to a mapping

The solution to this issue is to use any business object as a mapping. In Python,  any object may behave as such by subclassing [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping) and implementing the abstract methods.

As an example, we provide the following mixin:

```python
from collections.abc import Mapping, Iterator
from typing import Any

class ObjectToMappingMixin(Mapping):
    def __iter__(self) -> Iterator[Any]:
        return iter(vars(self))

    def __len__(self) -> int:
        return len(vars(self))

    def __getitem__(self, key: str, /) -> Any:
        return getattr(self, key)
```

Now, we can make our business objects subclass this mixin:

```python
class Engine(ObjectToMappingMixin):
    power: int
    consumption: int  
    
class Car(ObjectToMappingMixin):
    engine: Engine
```

`Engine` and `Car` now behave as mapping and it’s possible to access the attributes of `Engine` from car using the dict’s `getitem` strategy, such as:

```python
engine = Engine(power=1, consumption= 12)
car = Car(engine=engine)

assert car["engine"]["power"] == 1
assert car["engine"]["consumption"] == 12
```

Finaly, when using the `RulesEngine.apply_rules` method, there is not longer need to convert your business objects to dictionaries, you can directly use them like:

```python
from arta import RulesEngine

eng = RulesEngine(config_path="/to/my/config/dir") 
result = eng.apply_rules(input_data={"car": car})
```