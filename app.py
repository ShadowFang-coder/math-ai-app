import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Ultimate Quantum Math AI", layout="wide")

# ---------- STYLING ----------
st.markdown("""
<style>
body {background-color: #0e1117;}
.big-title {
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#4FC3F7;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 Ultimate Quantum Math AI</div>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("Navigate")
page = st.sidebar.radio("", ["🧮 Solver", "📈 Graph", "📊 Logarithm", "📐 Trigonometry"])

# ---------- INPUT PREPROCESS ----------
def preprocess(expr):
    expr = expr.replace("^", "**")
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    return expr

# ---------- ALGEBRA SOLVER ----------
def solve_linear(equation):
    x = sp.symbols('x')
    equation = preprocess(equation)

    if "=" not in equation:
        return ["Invalid equation"], None

    lhs, rhs = equation.split("=")
    lhs = sp.sympify(lhs)
    rhs = sp.sympify(rhs)

    steps = []
    steps.append(f"{lhs} = {rhs}")

    expr = sp.expand(lhs - rhs)
    a = expr.coeff(x)
    b = expr.subs(x, 0)

    if b != 0:
        steps.append(f"Move constant → {a}x = {-b}")

    if a != 0:
        result = float(-b / a)
        steps.append(f"Divide by {a} → x = {result}")
        return steps, result

    return ["No solution"], None

# ---------- SOLVER PAGE ----------
if page == "🧮 Solver":
    st.header("Algebra Solver")

    st.caption("Try: 2x + 5 = 15, 10x - 10 = 20")

    eq = st.text_input("Enter equation:")

    if st.button("Solve"):
        try:
            steps, ans = solve_linear(eq)

            st.subheader("🧠 Steps")
            for i, s in enumerate(steps, 1):
                st.write(f"{i}. {s}")

            if ans is not None:
                st.success(f"✅ Final Answer: x = {ans}")

        except Exception as e:
            st.error(e)

# ---------- GRAPH PAGE ----------
elif page == "📈 Graph":
    st.header("Graph Plotter")

    st.caption("Try: x**2, sin(x), 2*x+1")

    expr = st.text_input("Enter function (in x):")

    if st.button("Plot"):
        try:
            x = sp.symbols('x')
            expr = preprocess(expr)
            f = sp.lambdify(x, sp.sympify(expr), "numpy")

            xs = np.linspace(-10, 10, 400)
            ys = f(xs)

            fig, ax = plt.subplots()
            fig.patch.set_facecolor('#0e1117')
            ax.set_facecolor('#0e1117')

            ax.plot(xs, ys)
            ax.grid(True)

            st.pyplot(fig)

        except Exception as e:
            st.error(e)

# ---------- LOG PAGE ----------
elif page == "📊 Logarithm":
    st.header("Logarithm Solver")

    st.caption("Try: log(100,10), log(8,2)")

    expr = st.text_input("Enter log expression:")

    if st.button("Calculate"):
        try:
            expr = preprocess(expr)
            result = float(sp.sympify(expr))
            st.success(f"Answer: {result}")
        except Exception as e:
            st.error(e)

# ---------- TRIG PAGE ----------
elif page == "📐 Trigonometry":
    st.header("Trigonometry")

    st.caption("Try: sin(30), cos(60), tan(45)")

    expr = st.text_input("Enter trig expression:")

    if st.button("Solve Trig"):
        try:
            expr = preprocess(expr)

            # Convert degrees to radians
            expr = expr.replace("sin(", "sin(pi/180*")
            expr = expr.replace("cos(", "cos(pi/180*")
            expr = expr.replace("tan(", "tan(pi/180*")

            result = float(sp.N(sp.sympify(expr)))

            st.subheader("🧠 Steps")
            st.write("1. Convert degrees to radians")
            st.write("2. Apply trigonometric function")
            st.write("3. Compute value")

            st.success(f"Answer: {result}")

        except Exception as e:
            st.error(e)
