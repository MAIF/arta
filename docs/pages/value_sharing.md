!!! note

    Only available with `arta>=0.10.0`.


It is possible to share some informations between **condition** and **action** implementations.

It can be usefull when an **action** needs some data that was computed in a **condition** (e.g., sanity check use cases).

In the following example, a **condition** is computing the *median* of some *input values* and checking it. Then, the **action** retrieves this *median* value and uses it.


**Two things have to be done for that:**

1. Add the `**kwargs` parameter in your functions' definition (**validation** and **action** functions) if not already there.
1. Set some new subkeys in the `input_data` key.


**Set the value (in a condition for example):**

```python hl_lines="4 9"
def is_median_above(
    values: list[float], 
    limit: float, 
    **kwargs: Any,  # (1)
    ) -> bool:
    """Check if the median of some values is above limit."""
    median = statistics.median(values)
    # Store the value for later use by an action function
    kwargs["input_data"]["median"] = median  # (2)
    kwargs["input_data"]["median_limit"] = limit
    return median > limit
```

1. Add the ****kwargs** parameter.
2. Set your value in the `input_data`.


**Get the value (in an action for example):**

```python hl_lines="1 4"
def alert_on_median(**kwargs: Any) -> str:  # (1)
    """Alert: "Median is too high: 13, limit is: 10."""
    return (
        f"Median is too high: {kwargs['input_data']['median']}, "  # (2)
        f"limit is: {kwargs['input_data']['median_limit']}."
    )
```

1. Add the ****kwargs** parameter.
2. Get the value.