## Intro 

As we already mentioned in the [Home](index.md) page: ***Arta** is a very simple python rules engine*, but what do we mean by *rules engine*?

* **rule** : a set of different conditions that can be `True` or `False` (i.e., we say *verified* or *not verified*) triggering an action (i.e., any python callable object).
* **engine** : some code used for combining and evaluating different rules on some input data.

## Quick example: The Superhero School :school: :superhero:

Imagine the following use case: 

*Your are managing a superhero school and you want to use some school rules in your python app.*

The rules are (intentionally simple):

!!! success "Admission rules"

    If the applicant has a school authorized power then he is admitted, 
    
    Else he is not.

!!! example "Course selection rules"

    If he is speaking french and his age is known then he must take the "french" course, 
    
    Else if his age is unknown (e.g., it's a very old superhero), then he must take the "senior" course,
    
    Else if he is not speaking french, then he must take the "international" course. 

!!! info "Send favorite meal rules"

    If he is admitted and has a prefered dish, then we send an email to the school cook with the dish name.

## Focus on a rule

If we focus on one rule:

> If the applicant has a school authorized power then he is admitted, else he is not.

Here we can identify:

* The condition: **has a school authorized power** (only one condition)
* The triggered action: **is admitted**

## Focus on a condition

Let's be more precise on the following condition:

> has a school authorized power

If we define a list of "school authorized powers" it will be easy to verify this condition for an applicant:

```python
authorized_powers = [
    "strength",
    "fly",
    "immortality",
]
```

## Focus on an action

Defining the action is probably the hardest part because it means defining the rules engine output, which depends on the use of the rules' results. 

Let's focus on the following *action*:

> he is admitted

Let's say that in our use case, a simple dictionary *key* is used for storing the admission status: `{"is_admitted": True}`

We previously mentioned that action are *python callable object*, so it could be a simple function as:

```python
def set_admission(value: bool, **kwargs: Any) -> dict[str, bool]:
    """Return a dictionary containing the admission result."""
    return {"is_admitted": value}
```

We will see later how the `value` argument is passed to this **action function**.

## Focus on the input data

The *rules engine* is responsible for evaluating the [configured rules](#quick-example-the-superhero-school) against some *data* (usually named *input data*). 

In our use case, the input data could be a list of applicants:

```python
applicants = [
    {
        "id": 1,
        "name": "Superman",
        "civilian_name": "Clark Kent",
        "age": None,
        "city": "Metropolis",
        "language": "french",
        "powers": ["strength", "fly"],
        "favorite_meal": "Spinach",
        "secret_weakness": "Kryptonite",
        "weapons": [],
    },
    {
        "id": 2,
        "name": "Batman",
        "civilian_name": "Bruce Wayne",
        "age": 33,
        "city": "Gotham City",
        "language": "english",
        "powers": ["bank_account", "determination", "strength"],
        "favorite_meal": None,
        "secret_weakness": "Feel alone",
        "weapons": ["Hands", "Batarang", "Batgrenade"],
    },
    {
        "id": 3,
        "name": "Wonder Woman",
        "civilian_name": "Diana Prince",
        "age": 5000,
        "city": "Island of Themyscira",
        "language": "french",
        "powers": ["strength", "greek_gods", "regeneration", "immortality"],
        "favorite_meal": None,
        "secret_weakness": "Lost faith in humanity",
        "weapons": ["Magic lasso", "Bulletproof bracelets", "Sword", "Shield"],
    },
]
```

## Focus on the results

We talked about *rules*, *conditions*, *actions* and then *input data*, it is the **rules engine** responsability to put all them together and output some results.

To do that we need only two things:

1. Instanciating a *rules engine* (by giving it the rules' definition).
2. Applying the rules on the *input data*.

The first task is explained in the [User Guide](how_to.md) section as the second but if you are curious you will find a simple example below of how to apply the rules on a data set.

Let's apply the rules on a single applicant of our data set:

```python
from arta import RulesEngine

eng = RulesEngine(config_path="/to/my/config/dir")  # (1)

result = eng.apply_rules(applicants[0])

print(result)  # (2)
# {
# "admission": {"is_admitted": True},
# "course_selection": {"course": "senior"},
# "send_dish": True
# }
```

1. Many possibilites for instanciation, we will explain them later
2. Print a single result for the first applicant

In the *rules engine* result, we have 3 outputs: 

* `"admission": {"is_admitted": True},`
* `"course_selection": {"course": "senior"},`
* `"send_dish": True` 

It's simple, each correpond to one [rule](#quick-example-the-superhero-school).

Then we can apply the rules to all the data set (only 3 applicants):

```python
from arta import RulesEngine

results = {applicant["name"]: eng.apply_rules(applicant) for applicant in applicants}

print(results)  # (1)
# {
#   "Superman": {
#       "admission": {"is_admitted": True}, 
#       "course_selection": {"course": "senior"}, 
#       "send_dish": True},
#   "Batman": {
#       "admission": {"is_admitted": True},
#       "course_selection": {"course": "international"},
#       "send_dish": False,
#       },
#   "Wonder Woman": {
#       "admission": {"is_admitted": True},
#       "course_selection": {"course": "french"},
#       "send_dish": False,
#       }
# }
```

1. Print the results of all applicants

!!! success "Human readable format of the result"

    Superman, Batman and Wonder Womam are all admitted to school. Superman to the "senior" course, Batman to the "international" course and Wonder Woman to the "french" one. An email has been sent to the cook with Superman's favorite meal 'spinach'.

Now, if you want to learn how to configure your rules, go to the [User Guide](how_to.md) section.