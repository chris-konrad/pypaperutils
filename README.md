Pypaperutils - Useful functions for creating paper-ready figures in python
==============================

A personal collection of funcions for creating nice figures that can be exported to latex. 
- Colors of the TU Delft corporate image
- Export values as tex-commands and create tex-tables from Python lists.
- Parse a config.yaml to conveniently maintain constant format across figures created by multiple scripts. 

![Example plot with colors of the TU Delft corporate design](./demo/example_plot.png)

### Disclaimer

The package is under development. It may contain bugs and sections of unused or insensible code. Major changes to this package are planned for the time to come. A proper API documentation is still missing. 

## Installation

1. Clone this repository. 
   
   ```
   git clone  https://github.com/chris-konrad/pypaperutils.git
   ```

2. Install the package and it's dependencies. Refer to `pyproject.toml` for an overview of the dependencies. 
   
   ```
   cd ./pypaperutils
   pip install . 
   ```

## Authors

- Christoph M. Konrad, c.m.konrad@tudelft.nl

License
--------------------

This package is licensed under the terms of the [MIT license](https://github.com/chris-konrad/cyclistsocialforce/blob/main/LICENSE).

## Project Organization

```
.
├── pyproject.toml
├── LICENSE
├── README.md
└── src
    ├── config
    ├── design
    ├── io
    ├── measure    
    └── tex
```
