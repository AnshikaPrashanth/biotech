import streamlit as st
import cv2
import torch
import numpy as np
st.title('Test App')
st.write('cv2 version: ' + cv2.__version__)
st.write('torch version: ' + torch.__version__)
st.success('App loaded OK!')
