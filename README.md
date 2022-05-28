# MDO

`M`y `D`ata `O`bject - a [python][python] class to simplify the handling of data objects. It is [JSON][json]-based. The class is mainly designed to be used for configuration files.

The source code is published [here][mdo].

## For users

This class was designed to be a base class. This allows the user to use all the possibilities through inheritance. In its source code is what is really important for the user, everything else is encapsulated in the base class.

Like an [INI][ini] file, there are `sections`, `keys` and `values` - so the user has some structure in his data. To allow the user to use multiple identical keys for different sections, the unique variable name is always the combination of `<section>_<key>`, all in lower case.

The usage is ridiculously simple. Just create a class, inherit from `MDO` and override the `setup` method. In the `setup` method, the `add` method is called.

### Defining the values

It is really simple:

```python
def setup(self: object) -> bool:
    self.addConfigParameter('section1', 'key1', 'value')
    self.addConfigParameter('section2', 'key1', 'value')
    self.save()
```

### Accessing the values

Based on the above definition, it is done this way:

```python
# Read values
mydata1 = ThisIsMyConfig.section1_key1
mydata2 = ThisIsMyConfig.section2_Key1

# Set new values
ThisIsMyConfig.section1_key1 = newValue1
ThisIsMyConfig.section2_key1 = newValue2
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
from MCO.MCO import MCO

# Inherit from the base class
class ThisIsMyConfig(MCO):

    # Override the setup method
    def setup(self: object) -> bool:
        # define the 'key' parameter
        # in the group 'section
        # and the default value 'value
        self.addConfigParameter('section', 'key', 'value')
        # Make the setting persistent
        self.save()

if __name__ == '__main__':
    # instantiate the object with the file name for persistence.
    myConfigObject: ThisIsMyConfig = ThisIsMyConfig('config.json')

    # Read the configuration settings from the 'config.json' file
    myConfigObject.load()

    # read the value from config
    mydata = myConfigObject.section_key

    # Set a new value
    myConfigObject.section_key = newValue

    # Save the configuration settings in the file 'config.json'.
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
