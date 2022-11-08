# MDO

`M`y `D`ata `O`bject - a [python][python] class to simplify the handling of data objects. It is [JSON][json]-based. The class is mainly designed to be used for configuration files.

The source code is published [here][mdo].

## For users

This class was designed to be a base class. This allows the user to use all the possibilities through inheritance. In users source code are the parts important for the user, everything else is encapsulated in the the `MDO` class.

Like an [INI][ini] file, there are `sections`, `keys` and `values` - so the user has some structure in his configuration data. To allow the user to use multiple identical keys for different sections, the unique variable name is always the combination of `<section>_<key>`, all in lower case. If there are spaces inside a section or a key name, they will be removed.

The usage is ridiculously simple. Just create a class, inherit from `MDO` and override the `setup` method. In the `setup` method, the `add` method is called.

**HINT:** Never ever use the `save` method in the `setup` method. If you do so, you will always have the default values. Each time the object is created, possible changes are reset to the default values.

**HINT:** In case you already have a git project and you don't want to copy this to your project, just add this as submodule. In the following example this project is added as submodule to `vendor/MDO`. To import and use `MDO` in your own module, you need to extend the `sys` path:

```python
# This is the config file of your module. You have the following file structure
# + Project root directory
# +--mymodule - directory of your module
# +--vendor - git sumodules
#   + MDO - git submodule of MDO
#     + MDO - Python module of MDO

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../vendor/MDO/MDO/"))

from MDO import MDO

class MyModuleConfig(MDO):
    def setup(self: object) -> bool:
        self.add("section1", "key1", "value")
        self.add("section2", "key1", "value")
```

I already use this in another project, [TaRen][taren], so you might want to have a closer look there.

### Defining the values

It is really simple:

```python
def setup(self: object) -> bool:
    self.add("section1", "key1", "value")
    self.add("section2", "key1", "value")
```

**HINT:** The internal required removal of blanks might be the source of problems:

```python
def setup(self: object) -> bool:
    self.add("sectiona", "keyb", "value")
    self.add("section a", "keyb", "value")
    self.add("sectiona", "key b", "value")
    self.add("section a", "key b", "value")
```

The specification of this attributes are different, but they will always be the same. `MDO` cannot differentiate between them!

### Accessing the values

Based on the above definition, it is done this way:

```python
# Get the attribute name
attribute1 = MDO.getPropertyName('section1', 'key1')
attribute2 = MDO.getPropertyName('section2', 'key1')
# Read values
mydata1 = attrget(ThisIsMyConfig, attribute1)
mydata2 = attrget(ThisIsMyConfig, attribute2)

# Set new values
setattr(ThisIsMyConfig, attribute1, 42)
setattr(ThisIsMyConfig, attribute1, "newValue2")
```

### Persistence

You can also `load` and/or `store` the data.

```python
# Load the data
ThisIsMyConfig.load()

# Save the data
ThisIsMyConfig.save()
```

### A complete example

```python
# get access to the base class
from MDO.MDO import MDO

# Inherit from the base class
class ThisIsMyConfig(MDO):

    # Override the setup method
    def setup(self: object) -> bool:
        # in the group "section"
        # the "key" parameter
        # and the default value "value"
        self.add("section", "key", "value")

if __name__ == "__main__":
    # instantiate the object with the file name.
    myConfigObject: ThisIsMyConfig = ThisIsMyConfig("config.json")

    # Read the configuration settings from the "config.json" file
    # Up to now they don't exists, so only the defaults are available
    myConfigObject.load()

    # read the value from config
    mydata = attrget(myConfigObject, MDO.getPropertyName("section", "key"))

    # Set a new value
    attrset(myConfigObject, MDO.getPropertyName("section", "key"), newValue)

    # Save the configuration settings in the file "config.json".
    myConfigObject.save()
```

## Inside

The class uses the [JSON][json] module of [python][python]. Internally, a two-dimensional dictionary is used with `sections`, `keys` and the corresponding `default`. Using this dictionary, a check is performed in the `load` and `save` methods. So it is not possible to use more than the defined entries.

On the one hand with the `add` function the section and the key are entered into the internal dictionary with the default value. This internal dictionary contains the structure of the data. Secondly, an attribute name is created from the name of the `section` and the `key` according to the scheme `<section>_<key>` and the attribute is dynamically added to the class.

Maybe it is possible to do some things in a more pythonic way. But hey, it works, so what the heck?

[ini]: https://en.wikipedia.org/wiki/INI_file
[json]: https://www.json.org/
[mdo]: https://www.github.com/ThirtySomething/MDO
[python]: https://www.python.org/
[taren]: https://github.com/ThirtySomething/TaRen
