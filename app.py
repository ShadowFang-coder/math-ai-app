import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import re
import math

x = sp.symbols('x')

# -------- SESSION MEMORY --------
if "history" not in st.session_state:
    st.session_state.history = []

if "selected_query" not in st.session_state:
    st.session_state.selected_query = ""

# -------- SEO --------
st.set_page_config(
    page_title="Free Math Solver with Steps | Ultimate Math AI",
    page_icon="⚡",
    layout="wide"
)

# -------- UI --------
st.markdown("""
<style>
body { background-color: #0f172a; }
.big-title { font-size: 42px; font-weight: 800; color: #38bdf8; }
.subtitle { font-size: 18px; color: #94a3b8; margin-bottom: 20px; }
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}
.stButton>button {
    background: linear-gradient(90deg,#38bdf8,#0ea5e9);
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------- HERO --------
st.markdown('<div class="big-title">⚡ Ultimate Math AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Solve. Visualize. Learn. Like a Pro 🚀</div>', unsafe_allow_html=True)

# -------- SMART INPUT --------
def smart_input(expr):
    expr = expr.replace("^", "**")
    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    expr = re.sub(r'(sin|cos|tan)(\d+)', r'\1(\2)', expr)
    return expr

# -------- SIDEBAR --------
st.sidebar.title("🧠 History")

for i, item in enumerate(st.session_state.history[::-1]):
    if st.sidebar.button(item["query"], key=i):
        st.session_state.selected_query = item["query"]

section = st.sidebar.radio("Navigate", [
    "🧮 Solver",
    "📊 Graph",
    "📘 Logarithm",
    "📐 Trigonometry"
])

# -------- SOLVER --------
if section == "🧮 Solver":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Algebra Solver")

    default_val = st.session_state.selected_query

    user_input = st.text_input(
        "Enter your problem:",
        value=default_val,
        placeholder="Try: 2x + 5 = 15  OR  2(x+3)=10  OR  x^2+4x+4=0"
    )

    if st.button("Solve"):
        try:
            expr = smart_input(user_input)

            if "=" in expr:
                l, r = expr.split("=")

                left = sp.sympify(l)
                right = sp.sympify(r)

                eq = sp.Eq(left, right)
                sol = sp.solve(eq, x)

                result = f"x = {sol}"

                st.markdown(f"""
### 🧠 Steps

1. {left} = {right}  
2. Convert into equation form  
3. Solve using algebra  

### ✅ Final Answer: {result}
""")
            else:
                exp = sp.sympify(expr)
                result = str(sp.simplify(exp))
                st.success(result)

            # SAVE HISTORY
            st.session_state.history.append({
                "query": user_input,
                "result": result
            })

        except:
            st.error("Invalid input. Try formats like 2x+5=10 or x^2+4x=0")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- GRAPH --------
elif section == "📊 Graph":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Graph Plotter")

    expr_input = st.text_input(
        "Enter function:",
        placeholder="Try: x^2, sin(x), x^3 - 2x"
    )

    if st.button("Plot Graph"):
        try:
            expr = sp.sympify(smart_input(expr_input))
            f = sp.lambdify(x, expr)

            xv = np.linspace(-10, 10, 400)
            yv = f(xv)

            fig, ax = plt.subplots()
            ax.plot(xv, yv)
            ax.grid()

            st.pyplot(fig)

            st.session_state.history.append({
                "query": expr_input,
                "result": "Graph plotted"
            })

        except:
            st.error("Invalid function")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- LOG --------
elif section == "📘 Logarithm":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Log Calculator")

    expr = st.text_input(
        "Enter log:",
        placeholder="Try: log(10), log(100,10), ln(5)"
    )

    if st.button("Calculate"):
        try:
            val = eval(expr.replace("log", "math.log").replace("ln", "math.log"))
            st.success(val)

            st.session_state.history.append({
                "query": expr,
                "result": val
            })

        except:
            st.error("Invalid log format")

    st.markdown('</div>', unsafe_allow_html=True)

# -------- TRIG --------
elif section == "📐 Trigonometry":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Trigonometry Solver")

    expr = st.text_input(
        "Enter trig:",
        placeholder="Try: sin30, cos60, tan45"
    )

    if st.button("Calculate"):
        try:
            expr = smart_input(expr)
            match = re.match(r'(sin|cos|tan)\((\d+)\)', expr)

            if not match:
                st.error("Use: sin30, cos60, tan45")
            else:
                func, angle = match.group(1), int(match.group(2))

                values = {
                    "sin": {30:"1/2",45:"1/√2",60:"√3/2"},
                    "cos": {30:"√3/2",45:"1/√2",60:"1/2"},
                    "tan": {30:"1/√3",45:"1",60:"√3"}
                }

                result = values[func][angle]

                st.markdown(f"""
### 🧠 Steps

1. {func}({angle}°)  
2. Convert to radians  
3. Apply identity  

### ✅ Final Answer: {result}
""")

                st.session_state.history.append({
                    "query": expr,
                    "result": result
                })

        except:
            st.error("Invalid trig input")

    st.markdown('</div>', unsafe_allow_html=True)