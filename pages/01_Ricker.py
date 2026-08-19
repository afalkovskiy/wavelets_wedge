import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
import math

st.set_page_config(layout="wide")

pi = math.pi
nTraces = 20
trace_arr =[]
refl_arr =[]

st.title(r"Ricker wavelet: Wedge model")


def ricker(f, length=0.512, dt=0.001):
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))
    y = (1.-2.*(np.pi**2)*(f**2)*(t**2))*np.exp(-(np.pi**2)*(f**2)*(t**2))
    return t, y


col100, col200, col300 = st.columns(3)
with col100:
         f = st.slider('Frequency from [1, 240] Hz', value=25., min_value=1., max_value=240., step=1., format="%.1f")   
with col200:
        phi = st.slider('Phase rotation angle (deg)', value=0.0, min_value=0., max_value=360., step=45., format="%.1f")
with col300:
    envelope = st.checkbox('Envelope')    

str1 = "Ricker " + str(int(f + 0.5)) + " Hz, Phase = " + str(int(phi+0.5)) + "°"
# st.subheader(str1)

col1, col2, col3 = st.columns(3)
# with col1:
#     f = st.slider('Select wavelet frequency from [1, 240] Hz', value=30., min_value=1., max_value=240., step=1., format="%.1f")

t, y = ricker (f)

with col1:
    # envelope = st.checkbox('Envelope')
    st.subheader(str1)
    st.latex(r'''
    A(t) = (1-2\pi^2 f^2 t^2)e^{-\pi^2 f^2 t^2}
    ''') 

    
    z= hilbert(y) #form the analytical signal
    inst_amplitude = np.abs(z) #envelope extraction
    inst_phase = np.unwrap(np.angle(z))#inst phase
    
    phase = phi * pi/180
    x_rotate = math.cos(phase)*z.real - math.sin(phase)*z.imag

with col1:
    if envelope:
        chart_data = pd.DataFrame(
           {
               "t": t,
               #"y": y
               "y": x_rotate,
               "y_env2": inst_amplitude,
               "y_env3": -1*inst_amplitude
           }
        )
        st.line_chart(chart_data, x="t", y=["y", "y_env2", "y_env3"], color=["#d62728", "#D3D3D3", "#D3D3D3"], width=450, height=450)
    
    else:
        chart_data = pd.DataFrame(
           {
               "t": t,
               "y": x_rotate
           }
        )

        st.line_chart(chart_data, x="t", y=["y"], color=["#d62728"])

    dr = 0.001 * st.slider('Reflector interval (ms)', value=100, min_value=10, max_value=200, step=1) #, format="%.2f")
    wedge_shift = st.slider('Wedge shift per trace (ms)', min_value=0, max_value=20, value=3, step=1)

length1 = 0.6
dt1=0.001
x1 = np.linspace(0, length1, int(length1/dt1))
y1 = 0.* x1
 
ns = int(dr/dt1)
wedge_samples = int(wedge_shift/(dt1*1000.))

for j in range(nTraces):
    y1 = 0.* x1
 
    ns = int(dr/dt1)
    # st.write('dr =', dr, ' dt = ', dt1, ' ns = ', ns)
    # y1[ns] = -1.
    for i in range(int(length1/dr)):
        ni = ns*(i + 1) + int(j*ns/20)

        rf = -1 
        res = i%6      
        if res == 0:
            rf = -0.5
            ni = ns*(i + 1)
        if res == 1:
            rf = 0.5
            ni = ns*(i + 1)
        if res == 2:
            rf = -0.5
            ni = ns*(i + 1)
        if res == 3:
            rf = 0.5  
            # ni = ns*(i + 1) + int(j*ns/20) - ns
            ni = ns*(i + 1) + j*wedge_samples - ns + 1
        if res == 4:
            rf = -0.5 
            # ni = ns*(i + 1) + int(j*ns/20) - ns
            ni = ns*(i + 1) + j*wedge_samples - ns + 1
        if res == 5:
            rf = 0.5  
            # ni = ns*(i + 1) + int(j*ns/20) -ns
            ni = ns*(i + 1) + j*wedge_samples - ns + 1

        if ni > len(y1) - 1:
            ni = len(y1)
            rf = 0.
            break

        y1[ni] = rf

    refl_arr.append(y1)
    y2 = 1.5*np.convolve(refl_arr[j], x_rotate, mode='same')

    # print('y1 size: ', y1.size)
    # print('y2 size: ', y2.size)
    # print('x_rotate size: ', x_rotate.size)




    trace_arr.append(y2)
# reflectivity plot
fig1 = plt.figure(figsize=(4,4))

plt.subplot(111)
# plt.plot(y1, x1)

for i in range(nTraces):
    plt.plot(refl_arr[i] + i, 1000*x1, color='tab:orange')


plt.gca().invert_yaxis()
plt.xlabel("Reflectivity")
plt.ylabel("Two-way time (ms)")

# trace display
fig2 = plt.figure(figsize=(4,4), alpha=.45)
# fig2.suptitle('Convolved')
plt.xlabel("Synthetic trace")
plt.ylabel("Two-way time (ms)")

plt.subplot(111)
# plt.plot(y2, x1)
# plt.plot(y2 + 1., x1, color='tab:blue')

# y2pos = np.maximum(0,y2)
 
# plt.fill_betweenx(x1, y2pos, 0,  color='navy', alpha=.6)
# plt.fill_betweenx(x1, y2pos + 1., 1.,  color='navy', alpha=.6)

for i in range(nTraces):
    plt.plot(trace_arr[i] + i, 1000*x1, color='tab:blue', alpha=.45)
    y2pos = np.maximum(0,trace_arr[i])
    plt.fill_betweenx(1000*x1, y2pos + i, i,  color='tab:blue', alpha=.45)


plt.gca().invert_yaxis()

with col2:
    st.subheader('Reflectivity')
    st.pyplot(fig1) 

with col3:
    st.subheader('Synthetic trace')
    st.pyplot(fig2)



url1 = "https://www.rmseismic.com/lasviewer.html"
st.write("More geophysical apps: [rmseismic.com](%s)" % url1)
