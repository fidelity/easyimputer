# EasyImputer

[EasyImputer] is an abstract library for missing value imputation based on missing data statistics.

Currently supported data types
- Cross sectional numeric data only


## Features

- Works for cross sectional datasets having missing values in one or more columns
- Easy to use. Takes away the need to switch between many different kinds of imputation, by acting as a one stop shop.
- It provides flexibility by allowing the user to force the kind of imputation desired.

# Table of contents

<!--ts-->
- [EasyImputer](#easy-imputer)
  - [Features](#features)
- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
  - [Quick Start](#quick-start)
  - [Real Dataset Examples](#real-dataset-examples)
  - [Support and Contributions](#support-and-contributions)
  - [Acknowledgement](#acknowledgement)
  - [License](#license)
 
# Installation

Assuming that anaconda environment is already installed,

- EasyImputer can be installed from PyPI using 

```
pip install EasyImputer
```



# Usage
  
## Quick Start
Supports imputation on all numeric cross sectional data.

```python

from EasyImputer import CSDImputer

imputer = CSDImputer()
statistics, imputed_values, comments = imputer.impute(input_df)
```

Use models = [] to override the imputation strategy. Alowd imputation techniques can be obtained from constant.py

## Real Dataset Examples

Refer to datasets folder


## Support and Contributions

Please submit bug reports and feature requests as Issues.
Contributions are very welcome. 

For additional questions and feedback, please contact us at EasyImputer@fmr.com

## Acknowledgement

EasyImputer is developed by Emerging Tech Team at Fidelity Investments.
The part of the package was developed as part of an internship program at Fidelity. We thank [Ambika Sadhu] for her contribution to the package.

## License

EasyImputer is licensed under the [GPL License 3.0.](LICENSE.md)