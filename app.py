import sympy as sp
from flask import Flask, jsonify, request, render_template
from sympy import symbols, diff, integrate, limit, sympify, oo, pi, Eq, latex
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application
)
from math import isclose, factorial, comb
import re

app = Flask(__name__)
x, y = sp.symbols('x y')
transformations = (standard_transformations + (implicit_multiplication_application,))

def parse_input(expr):
    return parse_expr(expr, transformations=transformations)

@app.route('/differentiate', methods=['POST'])
def differentiate():
    expr_str = request.json['expr']
    expr = parse_input(expr_str)
    derivative = diff(expr, x)
    return jsonify({'latex': f"d/dx ({latex(expr)}) = {latex(derivative)}"})

@app.route('/integrate', methods = ['POST'])
def Indefinte_Integral():
    expr_str = request.json['expr']
    expr = parse_input(expr_str)
    integral = integrate(expr, x)
    return jsonify({'latex': f"\int ({latex(expr)}) dx = {latex(integral)} + C"})

@app.route('/definite_integral', methods=['POST'])
def definite_integral():
    expr_str = request.json['expr']
    a = parse_input(request.json['a'])
    b = parse_input(request.json['b'])
    expr = parse_input(expr_str)
    result = integrate(expr, (x, a, b))
    return jsonify({'latex': f"\int_{{{{{latex(a)}}}}}^{{{{{latex(b)}}}}} {latex(expr)} \\, dx = {latex(result)}"})

@app.route('/Limits', methods=['POST'])
def Limit():
    expr_str = request.json['expr']
    point = parse_input(request.json['point'])
    direction = request.json.get('direction', None)
    expr = parse_input(expr_str)
    if direction == 'left':
        result = limit(expr, x, point, dir='-')
    elif direction == 'right':
        result = limit(expr, x, point, dir='+')
    else:
        result = limit(expr, x, point)
    return jsonify({'latex': f"\\lim_{{x \\to {latex(point)}}} {latex(expr)} = {latex(result)}"})

@app.route('/Taylor_Series', methods=['POST'])
def taylor_series():
    expr_str = request.json['expr']
    a = parse_input(request.json['a'])
    n = int(request.json['n'])
    result = 0
    expr = parse_input(expr_str)
    for i in range(n + 1):
        term = (diff(expr, x, i).subs(x, a) / factorial(i)) * (x - a) ** i
        result += term
    return jsonify({'latex': f"T_{{{n}}}(latex(expr), {latex(a)}) = {latex(result)}"})

@app.route('/First-Order_Linear_ODE', methods=['POST'])
def first_order_linear_ode():
    expr_str = request.json['expr']
    expr = parse_input(expr_str)
    y = symbols('y', cls=sp.Function)
    ODE = Eq(diff(y(x), x) + expr * y(x), 0)
    solution = sp.dsolve(ODE, y(x))
    return jsonify({'latex': f"dy/dx + {latex(expr)}y = 0 \\Rightarrow y(x) = {latex(solution.rhs)}"})

@app.route('/Second-Order_Linear_ODE', methods=['POST'])
def second_order_linear_ode():
    expr_str = request.json['expr']
    expr = parse_input(expr_str)
    y = symbols('y', cls=sp.Function)
    ODE = Eq(diff(y(x), x, 2) + expr * diff(y(x), x) + expr * y(x), 0)
    solution = sp.dsolve(ODE, y(x))
    return jsonify({'latex': f"d^2y/dx^2 + {latex(expr)}dy/dx + {latex(expr)}y = 0 \\Rightarrow y(x) = {latex(solution.rhs)}"})

@app.route('/Simpson\'s_Rule', methods=['POST'])
def simpsons_rule():
    expr_str = request.json['expr']
    a = parse_input(request.json['a'])
    b = parse_input(request.json['b'])
    n = int(request.json['n'])
    if n % 2 == 1:
        return jsonify({'error': 'n must be even for Simpson\'s Rule'}), 400
    else:
        expr = parse_input(expr_str)
        h = (b - a) / n
        result = expr.subs(x, a) + expr.subs(x, b)
        for i in range(1, n, 1):
            coeff = 4 if i & 1 else 2
            result += coeff * expr.subs(x, a + i * h)
            result *= h / 3
    return jsonify({'latex': f"\\int_{{{latex(a)}}}^{{{latex(b)}}} {latex(expr)} \\, dx = \\approximate {latex(result)}"})

@app.route('/Volumes_of_Revolution', methods=['POST'])
def volumes_of_revoltion():
    expr_str = request.json['expr']
    a = parse_input(request.json['a'])
    b = parse_input(request.json['b'])
    axis = request.json.get('axis', 'x')
    expr = parse_input(expr_str)
    if axis == 'x':
        result = pi * integrate(expr ** 2, (x, a, b))
        return jsonify({'latex': f"Volume = \\pi \\int_{{{latex(a)}}}^{{{latex(b)}}} ({latex(expr)})^2 \\, dx = {latex(result)}"})
    elif axis == 'y':
        y = symbols('y')
        expr_inv = sp.dsolve(Eq(y, expr), x)[0].rhs
        result = pi * integrate(expr_inv ** 2, (y, a, b))
        return jsonify({'latex': f"Volume = \\pi \\int_{{{latex(a)}}}^{{{latex(b)}}} ({latex(expr_inv)})^2 \\, dy = {latex(result)}"})

@app.route('/Summations', methods=['POST'])
def summations():
    expr_str = request.json['expr']
    n = symbols('n', float=True)
    expr = parse_input(expr_str)
    summation = sp.summation(expr, (n, 1, oo))
    return jsonify({'latex': f"\\sum_{{n - 1}}^{{\\infty}} {latex(expr)} = {latex(summation)}"})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

    