import streamlit as st
from streamlit.components.v1 import html

st.title('Seismic Wavelets: Wedge Model v.4.1')
st.subheader('Alex Falkovskiy')
url = "https://www.rmseismic.com"
st.write("RM Seismic Software [rmseismic.com](%s)" % url)
st.write('This web app is a tool which helps to visualise how classical wedge model would look like on a seismic section.')
st.write('It convolves any of selected wavelets with reflectivity series and calculates a synthetic traces for a wedge model.')
st.write('You can select wavelet and vary model parameters and see how your seismic section would change on the fly.')

st.write('Here is the list of wavelets you can display and calculate a synthetic trace:')
st.write('**Ricker, Ormsby, Klauder, Butterworth**. Use a left side menu to select a wavelet and sliders to change parameters.')
st.write('Wavelet equations are from a paper by Harold Ryan: Ricker, Ormsby; Klauder, Butterworth - A Choice of wavelets, publised in CSEG Recorder, September 1994.')
st.write('This classical work provides math foundation for the wedge model: Widess, M. B., 1973, How thin is a thin bed?: Geophysics, 38, 1176-1180.')

url1 = "https://www.rmseismic.com/lasviewer.html"
st.write("More geophysical apps: [rmseismic.com](%s)" % url1)
st.write("A.F., August 2026")

google_js = """
<!-- Google tag (gtag.js) --><script async src="https://www.googletagmanager.com/gtag/js?id=G-VBX865DFKL"></script><script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-VBX865DFKL');
</script>
"""

#html1 = f"{google_js}"
 
