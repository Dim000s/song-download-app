import streamlit as st
# Import libraries
import matplotlib.pyplot as plt
import numpy as np
 
# Creating vectors X and Y
x = np.linspace(-100, 100, 1000)
y = x ** 2
 
fig = plt.figure(figsize = (10, 5))
plt.plot(x, y)
st.pyplot(fig=fig)

def integrate(lim1, lim2):
    area_under_graph = ((lim2**3)/3) - ((lim1**3)/3)
    return abs(round(area_under_graph, 0))

def trapezium_rule(lim1, lim2, n):
    height = (lim2-lim1)/n
    area = 0
    # get all x values between lim1 and lim2
    x = lim1
    x_vals = []
    while not x >= lim2:
        x += height
        x_vals.append(x)
    y_vals = []
    for x_val in x_vals:
        y_val = x_val ** 2
        y_vals.append(y_val)
    y_sum = sum(y_vals)
    y0 = lim1 ** 2
    y1 = lim2 ** 2
    area = (height/2) * (y0 + y1 + (2 * y_sum))
    return abs(round(area, 0))

lim1 = st.slider("Limit 1", min_value=-100.0, max_value=100.0, step=0.1)
lim2 = st.slider("Limit 2", min_value=-100.0, max_value=100.0, step=0.1)
n = st.slider("Subdivisions of graph", min_value=1.0, max_value=1000.0, step=1.0)

area_integration = integrate(lim1, lim2)
area_trapezium = trapezium_rule(lim1, lim2, n)
st.write(f"Area using integration is {area_integration}")
st.write(f"Area using trapezium with {n} subdivisions is {area_trapezium}")
st.write(f"Difference is {abs(area_integration - area_trapezium)}")