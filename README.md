# MDO

`M`y `D`ata `O`bject - a [Python][python] class to simplify the handling of data objects. It is [JSON][json]-based. The class is mainly designed for configuration files.

The source code is published [here on GitHub][mdo].

## For users

This class was designed as a base class. This allows the user to use all possibilities through inheritance. In user source code, only the parts important for the user remain; everything else is encapsulated in the `MDO` class.

Like an [INI][ini] file, there are `sections`, `keys`, and `values`, so the user has structure in configuration data.

Usage is straightforward. Create a class, inherit from `MDO`, and override the `setup` method. In the `setup` method, call `add`.

**HINT:** Never use the `save` method in the `setup` method. If you do, you will always get the default values. Each time the object is created, possible changes are reset to defaults.

**HINT:** If you already have a git project and do not want to copy this into your project, just add it as a submodule. In the following example, this project is added as a submodule to `vendor/MDO`. To import and use `MDO` in your own module, you need to extend the `sys` path:

```python
# This is the config file of your module. You have the following file structure
# + Project root directory
# +--mymodule - directory of your module
# +--vendor - git submodules
#   + MDO - git submodule of MDO
#     + MDO - Python module of MDO

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../vendor/MDO/MDO/"))

from MDO import MDO

class MyModuleConfig(MDO):
    def setup(self) -> bool:
        self.add("section1", "key1", "value")
        self.add("section2", "key1", "value")
```

This class is also used in another project, [TaRen][taren], which may be useful as an additional reference.

### Defining the values

This can be defined as follows:

```python
def setup(self) -> bool:
    self.add("section1", "key1", "value")
    self.add("section2", "key1", "value")
```

**HINT:** The section name is always converted to uppercase internally. Both section and key are stripped of leading and trailing whitespace.

### Accessing the values

Based on the definition above, access works like this:

```python
# Read values
mydata1 = myConfigObject.value_get("section1", "key1")
mydata2 = myConfigObject.value_get("section1", "key2")

# Set new values
myConfigObject.value_set("section1", "key1", "value")
myConfigObject.value_set("section1", "key2", 42)
```

### Persistence

You can also `load` and/or `save` the data.

By default, the constructor calls `load()` automatically. If you want to separate object creation from persistence, instantiate the object with `auto_load=False` and call `load()` explicitly later.

```python
# Load the data
myConfigObject.load()

# Save the data
myConfigObject.save()
```

```python
# Skip automatic loading during initialization
myConfigObject = ThisIsMyConfig("config.json", auto_load=False)

# Load later when persistence should be applied
myConfigObject.load()
```

### A complete example

```python
# Get access to the base class
from MDO.MDO import MDO

# Inherit from the base class
class ThisIsMyConfig(MDO):

    # Override the setup method
    def setup(self) -> bool:
        # in the group "section"
        # the "key" parameter
        # and the default value "value"
        self.add("section", "key", "value")

if __name__ == "__main__":
    # Instantiate the object with the file name.
    myConfigObject: ThisIsMyConfig = ThisIsMyConfig("config.json")

    # Read the configuration settings from the "config.json" file
    # Up to now it does not exist, so only the defaults are available.
    myConfigObject.load()

    # Read the value from config
    mydata = myConfigObject.value_get("section", "key")

    # Set a new value
    myConfigObject.value_set("section", "key", newValue)

    # Save the configuration settings in the file "config.json".
    myConfigObject.save()
```

## Inside

The class uses the [JSON][json] module of [Python][python]. Internally, there are two two-dimensional dictionaries used with `sections`, `keys`, and the corresponding `default`. The first one stores defaults; the second one handles real data. Using the defaults dictionary, a check is performed in the `save` method. So it is not possible to persist more than the defined entries. But during runtime, you can add as many entries as you like.

With the `add` function, the section and key are entered into the internal dictionary with the default value. This internal dictionary contains the structure of the data. Some parts may be implemented in a more Pythonic style, but the current implementation is stable and practical.

[ini]: https://en.wikipedia.org/wiki/INI_file
[json]: https://www.json.org/
[mdo]: https://www.github.com/ThirtySomething/MDO
[python]: https://www.python.org/
[taren]: https://github.com/ThirtySomething/TaRen
