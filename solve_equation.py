from sympy import *

theta = 2
x = Symbol('x')
y = Symbol('y')
kd = 0.95
bbw = 0.025



result = solve([(1+0.0005*theta)*x+4.259*(1-0.265*bbw/y)*(1-0.52*exp(-10.8*x))*y - kd, x-2*y], [x, y])
print(result)
