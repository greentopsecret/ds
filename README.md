# Medium Squared Error

## Installation
```
pip install -r requirements.txt
```

## Usage
Calculate smallest MSE, closest slope and intercept for points from ./datapoints.csv file
```
./mse.py --source ./datapoints.csv
```

Run with debug info
```
./mse.py --verbose
```

Run and draw a plot
```
./mse.py --plot
```

## Optimisation
There are two loops - outer that iterates through possible slope values and inner that iterates through possible intercept values.   
Inside the inner loop we can break once we noticed that MSE started to grow (that optimisation is already implemented).  
Similarly, we can break the outer loop once we noticed that MSE-value returned by inner loop started to grow (that optimisation is not implemented as it will make code less readable).