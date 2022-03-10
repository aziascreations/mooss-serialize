# Mooss - Serialize
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mooss-serialize.svg)](https://pypi.python.org/pypi/mooss-serialize/)
&nbsp;&nbsp;
[![PyPI status](https://img.shields.io/pypi/status/mooss-serialize.svg)](https://pypi.python.org/pypi/mooss-serialize/)
[![PyPi version](https://badgen.net/pypi/v/mooss-serialize/)](https://pypi.com/project/mooss-serialize)
&nbsp;&nbsp;
[![PyPI download month](https://img.shields.io/pypi/dm/mooss-serialize.svg)](https://pypi.python.org/pypi/mooss-serialize/)
&nbsp;&nbsp;
[![GitHub issues](https://img.shields.io/github/issues/aziascreations/mooss-serialize.svg)](https://GitHub.com/aziascreations/mooss-serialize/issues/)
&nbsp;&nbsp;
[![PyPI license](https://img.shields.io/pypi/l/mooss-serialize.svg)](https://pypi.python.org/pypi/mooss-serialize/)

**⚠️ This package is a work-in-progress, it is not suitable nor reliable for any applications yet ⚠️**

A Python package to help with serialization and deserialization of *dataclasses* through the help of a common interface
while also insuring the parsed data is properly typed and handled.

This package was created because I often found myself needing to deserialize nested dataclasses with *slightly complex*
value types, and because all other solutions I found were either too bloated or didn't work properly with what I had.

It is by no mean a replacement for other packages, but should suffice when dealing with *slightly complex* data
structures.

## Setup

### Requirements
* Python 3.9 or newer.&nbsp;&nbsp;&nbsp;&nbsp;<sub><sup>(CPython and PyPy are both supported !)</sup></sub>

### Installation
Run one of the following commands to install the package:
```bash
python -m pip install --upgrade mooss-serialize
pip install --upgrade mooss-serialize
```

## Usage
<!-- TODO: Add references to the IDeserializable class ! -->

In order to use this package, you simply have to create a class that extends the provided `ISerializable` interface
that also has the `dataclass` decorator, add some variable annotations with the desired types, and then use the
provided class methods to serialize and deserialize it easily.

See the examples below for more information

### Creating classes
The following classes have more complex and fluid typing for their variables that will help illustrate the main
advantage of this package over oneliners and other simpler deserializers.
```python
from dataclasses import dataclass
from typing import Optional, Union

from mooss.serialize.interface import ISerializable

@dataclass
class Address(ISerializable):
    country: str
    city: str
    zip_code: Optional[int]
    # TODO: Implement non-serializable fields  (has_multiple_mailboxes: bool)
    street: str = "Unknown"

@dataclass
class Person(ISerializable):
    name: str
    address: Union[Address, str, None]
```

### Preparing the raw data
We are preparing a dictionary that represent the non-deserialized data.
```python
# Representing the 'Person' and 'Address' classes.
# The 'zip_code' field can be removed and will be 'None' since it uses the 'Optional' annotation.
data_person_full: dict = {
    "name": "John Smith",
    "address": {
        "country": "Belgium",
        "city": "Brussels",
        "zip_code": 1000,
        "street": "Rue de la Tribune",
    },
}

# Only representing the 'Person' class and replacing the 'Address' class by a string.
data_person_simple: dict = {
    "name": "John Smith",
    "address": "Rue de la Tribune, 1000 Brussels, Belgium"
}
```
This data can also be represented as a JSON string when using `from_json` in the next step.

### Parsing the data
```python
person_full = Person.from_dict(data_person_full)

print(person_full)
```

### Other parameters
The `from_dict` and `from_json` methods features a couple of parameters that can help you influence the way it will react and process some
specific cases depending on your requirements.

<details>
    <summary>Click here to expand list of all the available parameters</summary>
    This information is also available in the methods' docstring.
    <table>
        <tr>
            <td><b>Parameter</b></td>
            <td><b>Type</b></td>
            <td><b>Description</b></td>
            <td><b>Default</b></td>
        </tr>
        <tr>
            <td><code>data_dict</code></td>
            <td><code>dict</code></td>
            <td>Data to be deserialized</td>
            <td><i>Required</i></td>
        </tr>
        <tr>
            <td><code>data_json</code></td>
            <td><code>dict</code></td>
            <td>Data to be parsed into a dict and be deserialized</td>
            <td><i>Required</i></td>
        </tr>
        <tr>
            <td><code>allow_unknown</code></td>
            <td><code>bool</code></td>
            <td>Allow unknown fields to be processed instead of raising a <code>ValueError</code> exception,
other parameters will determine their use if <code>True</code>.</td>
            <td><code>False</code></td>
        </tr>
        <tr>
            <td><code>add_unknown_as_is</code></td>
            <td><code>bool</code></td>
            <td>Adds unknown fields/values as-is in the final class if <code>allow_unknown</code> is also <code>True</code>.</td>
            <td><code>False</code></td>
        </tr>
        <tr>
            <td><code>allow_as_is_unknown_overloading</code></td>
            <td><code>bool</code></td>
            <td>Allow unknown fields/values to overload existing class attributes.</td>
            <td><code>False</code></td>
        </tr>
        <tr>
            <td><code>allow_missing_required</code></td>
            <td><code>bool</code></td>
            <td>TODO</td>
            <td><code>False</code></td>
        </tr>
        <tr>
            <td><code>allow_missing_nullable</code></td>
            <td><code>bool</code></td>
            <td>TODO</td>
            <td><code>False</code></td>
        </tr>
        <tr>
            <td><code>add_unserializable_as_dict</code></td>
            <td><code>bool</code></td>
            <td>TODO</td>
            <td><code>False</code></td>
        </tr>
        <tr>
            <td><code>validate_type</code></td>
            <td><code>bool</code></td>
            <td>Enables a strict type check between the class' serializable fields and the given data.</td>
            <td><code>True</code></td>
        </tr>
        <tr>
            <td><code>parsing_depth</code></td>
            <td><code>int</code></td>
            <td>The recursive depth to which the deserialization process will go.<br>(<code>-1</code> means infinite)</td>
            <td><code>-1</code></td>
        </tr>
        <tr>
            <td><code>do_deep_copy</code></td>
            <td><code>bool</code></td>
            <td>Performs a deep copy of the given 'data_dict' to prevent modifications from affecting other variables
that may reference it.</td>
            <td><code>False</code></td>
        </tr>
    </table>
</details>

## Type annotations
Since the `dataclass` decorator is required on any class that extends `ISerializable`, the methods can easily detect
and validate the different types for the given data, which in turn can help you reduce the amount of check you will
have to perform on the final deserialized data.

This approach was used due to the fact that many one-liners and small helpers available on the internet do not
implement this type of checks and usually leave you with potentially invalidly-typed data, or simply data that is not
deserialized properly in the case of nested deserializable classes.

It should be noted that undefined fields can also be supported and copied as-is if the right parameters are given
to the methods, but this isn't done by default to prevent silent errors and overloading existing attributes !

### Supported types
These types should cover 99% of the uses cases for this package, however, in the event you would wish to use
unsupported types, you can always do so by using the `Any` type to skip type checking for a given field.

* **Primitives:**<br>
`str`, `int`, `float`, `bool`
* **Simple sets:**<br>
`list`, `dict`, `tuple`, `set`
* **Composed sets\*:**<br>
`list[...]`, `dict[...]`, `tuple[...]`, `set[...]`
* **Variable types\*:**<br>
`Union`, `Optional`, `Any`

<sup>*: Has some limitations on what can be contained between the square brackets.</sup>

### Limitations
These limitations are put in place due to the fact that I don't have the time to implement a proper way to
support weird and unusual data types.

[...] If you want to handle these, you can either add support for it yourself or use a specialized and bulkier
package.

* Mixed complex types: list[ISerializable, primitive]
  * A mix of primitives and sets should work but should preferably not be used.

#### More specific and rare types
Types and utilities such as the ones listed below should be supported at some point, but since it is not urgent,
there is no set timeline for their implementation.

*List of types and utilities that may be supported:*<br>
`Set`, `Collection`, `NamedTuple`, `NewType`, `Mapping`, `Sequence`, `TypeVar` and `Iterable`.

## Contributing
If you want more information on how to contribute to this package, you should refer to [develop.md](develop.md).

## License
[Unlicense](LICENSE)
