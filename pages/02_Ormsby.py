import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert
import math
import plotly.graph_objects as go

st.set_page_config(layout="wide")

pi = math.pi
nTraces = 20
trace_arr =[]
refl_arr =[]

st.title(r"Ormsby wavelet: Wedge model")
st.latex(r'''
    A(t) = \frac{\pi f_4^2 sinc^2 (\pi f_4 t) - \pi f_3^2 sinc^2 (\pi f_3 t)}{f_4 - f_3} 
    - \frac{\pi f_2^2 sinc^2 (\pi f_2 t) - \pi f_1^2 sinc^2 (\pi f_1 t)}{f_2 - f_1}
    ''') 

def ricker(f, length=0.512, dt=0.001):
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))
    y = (1.-2.*(np.pi**2)*(f**2)*(t**2))*np.exp(-(np.pi**2)*(f**2)*(t**2))
    return t, y

def ORMSBY(f1=5., f2=10., f3=40., f4=45., length=0.512, dt=0.001):
    p = np.pi
    t = np.linspace(-length/2, (length-dt)/2, int(length/dt))

    y = p*f4**2 * (np.sinc(f4*t))**2/(f4-f3) - p*f3**2 * (np.sinc(f3*t))**2/(f4-f3) - \
        p*f2**2 * (np.sinc(f2*t))**2/(f2-f1) +  p*f1**2 * (np.sinc(f1*t))**2/(f2-f1)

    y = y / np.amax(abs(y))

    return t, y

col100, col200, col300 = st.columns(3)
with col100:
    st.subheader("Wavelet parameters")
    envelope = st.checkbox('Envelope')
    # f = st.slider('Frequency from [1, 240] Hz', value=25., min_value=1., max_value=240., step=1., format="%.1f") 
    # phi = st.slider('Phase rotation angle (deg)', value=0.0, min_value=0., max_value=360., step=45., format="%.1f") 
    if "f" not in st.session_state:
        st.session_state["f"] = 25.
    f = st.session_state["f"]  

    if "phi" not in st.session_state:
        st.session_state["phi"] = 0.
    phi = st.session_state["phi"]  


    if "f12" not in st.session_state:
        st.session_state["f12"] = (5., 10.)
    f1, f2 = st.session_state["f12"]  

    if "f34" not in st.session_state:
        st.session_state["f34"] = (60., 70.)
    f3, f4 = st.session_state["f34"] 

            
with col200:      
    st.subheader('Reflectivity')
    dr = 0.001 * st.slider('Reflector interval (ms)', value=100, min_value=10, max_value=200, step=1) #, format="%.2f")

with col300:
    st.subheader('Synthetic traces')
    # envelope = st.checkbox('Envelope')
    wedge_shift = st.slider('Wedge shift per trace (ms)', min_value=0, max_value=20, value=3, step=1)
    # scl = st.slider('Trace scalar', value=1.3, min_value=0.2, max_value=10., step=0.1, format="%.1f")
    # scl = st.number_input('Display trace scalar', min_value=0.2, max_value=10., value=1.3, step=0.1)    
if "scl" not in st.session_state:
    st.session_state["scl"] = 1.3 
          
scl = st.session_state["scl"]

# str1 = "Ricker " + str(int(f + 0.5)) + " Hz, φ = " + str(int(phi+0.5)) + "°"
str1 = "Ormsby " + str(int(f1 + 0.5)) + " - " + str(int(f2 + 0.5))  + " - " + str(int(f3 + 0.5)) + " - " + str(int(f4 + 0.5)) + " Hz, Phase " + str(int(phi+0.5)) + "°"
# st.subheader(str1)

col1, col2, col3 = st.columns(3)
# with col1:
#     f = st.slider('Select wavelet frequency from [1, 240] Hz', value=30., min_value=1., max_value=240., step=1., format="%.1f")

# t, y = ricker (f)
t, y = ORMSBY(f1, f2, f3, f4, 0.512, 0.001)

with col1:
    # envelope = st.checkbox('Envelope')


    
    z= hilbert(y) #form the analytical signal
    inst_amplitude = np.abs(z) #envelope extraction
    inst_phase = np.unwrap(np.angle(z))#inst phase
    
    phase = phi * pi/180
    x_rotate = math.cos(phase)*z.real - math.sin(phase)*z.imag

# fig = go.Figure()
fig0 = plt.figure(figsize=(4,1.7), alpha=.45)
with col100:

    # st.latex(r'''
    #     A(t) = \frac{\pi f_4^2 sinc^2 (\pi f_4 t) - \pi f_3^2 sinc^2 (\pi f_3 t)}{f_4 - f_3} \\
    #     - \frac{\pi f_2^2 sinc^2 (\pi f_2 t) - \pi f_1^2 sinc^2 (\pi f_1 t)}{f_2 - f_1}
    #     ''') 
    st.subheader(f"**{str1}**")

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
        # st.line_chart(chart_data, x="t", y=["y", "y_env2", "y_env3"], color=["#d62728", "#D3D3D3", "#D3D3D3"], width=450, height=450)

        plt.plot(chart_data['t'], chart_data['y'], color='tab:red', alpha=.45)
        plt.plot(chart_data['t'], chart_data['y_env2'], color='tab:grey', alpha=.45)
        plt.plot(chart_data['t'], chart_data['y_env3'], color='tab:grey', alpha=.45)      
    
    else:
        chart_data = pd.DataFrame(
           {
               "t": t,
               "y": x_rotate
           }
        )

        plt.plot(chart_data['t'], chart_data['y'], color='tab:red', alpha=.45)
    plt.grid()
    st.pyplot(fig0) 



    st.slider('Wavelet phase rotation (deg)', key="phi", min_value=0., max_value=360., step=45., format="%.1f")  
    # st.slider('Dominant requency [1, 240] Hz', key="f", min_value=1., max_value=240., step=1., format="%.1f") 
    st.slider(' f1 - f2 (Hz)', key="f12", min_value=1., max_value=120., step=1., format="%.1f")
    st.slider(' f3 - f4 (Hz)', key="f34", min_value=f2, max_value=120., step=1., format="%.1f")


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
    y2 = scl*np.convolve(refl_arr[j], x_rotate, mode='same')


    trace_arr.append(y2)
# reflectivity plot
fig1 = plt.figure(figsize=(4,2.7))

plt.subplot(111)
# plt.plot(y1, x1)

for i in range(nTraces):
    plt.plot(refl_arr[i] + i, 1000*x1, color='tab:orange')


plt.gca().invert_yaxis()
# plt.xlabel("Reflectivity")
plt.ylabel("Two-way time (ms)")

# trace display
fig2 = plt.figure(figsize=(4,2.7), alpha=.45)
# fig2.suptitle('Convolved')
# plt.xlabel("Trace #")
plt.ylabel("Two-way time (ms)")

plt.subplot(111)


for i in range(nTraces):
    plt.plot(trace_arr[i] + i, 1000*x1, color='tab:blue', alpha=.45)
    y2pos = np.maximum(0,trace_arr[i])
    plt.fill_betweenx(1000*x1, y2pos + i, i,  color='tab:blue', alpha=.45)


plt.gca().invert_yaxis()

with col2:
    st.pyplot(fig1) 

with col3:
    st.pyplot(fig2)
    st.slider('Trace scalar', key="scl", min_value=0.2, max_value=10., step=0.1, format="%.1f")


    # st.markdown("<br>", unsafe_allow_html=True)
    url1 = "https://www.rmseismic.com/lasviewer.html"
    st.write("More geophysical apps: [rmseismic.com](%s)" % url1)