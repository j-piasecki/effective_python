import argparse
import sympy
import numpy as np 

parser = argparse.ArgumentParser(description='Finds roots of a polynomial using Newton\'s method.')
parser.add_argument('polynomial', metavar='P', type=str, nargs='+', help='polynomial to find roots of')
parser.add_argument('-i', '--iterations', metavar='I', type=int, default=100, help='number of iterations to run')
parser.add_argument('-e', '--epsilon', metavar='E', type=float, default=0.0001, help='epsilon value for convergence')

args = parser.parse_args()

x = sympy.Symbol('x')
input_polynomial = sympy.polys.polytools.poly_from_expr(args.polynomial[0])[0]

polynomial = np.polynomial.Polynomial(input_polynomial.coeffs()[::-1])
derivative = polynomial.deriv()

def newton(x, coefs):
    return x - polynomial(x) / derivative(x)

def newton_iterate(x, coefs, iterations, epsilon):
    for i in range(iterations):
        x = newton(x, coefs)
        if abs(polynomial(x)) < epsilon:
            return x
    return x

def newton_roots(coefs, iterations, epsilon):
    roots = []
    for i in range(len(coefs) - 1):
        roots.append(newton_iterate(0, coefs, iterations, epsilon))
        coefs = np.polynomial.polynomial.polydiv(coefs, np.array([-roots[-1], 1]))[0]
    return roots

print(newton_roots(polynomial.coef, args.iterations, args.epsilon))