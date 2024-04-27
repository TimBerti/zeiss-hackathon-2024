import streamlit as st
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

API_URL = 'http://localhost:5000/data'

def fetch_data():
    return {'occupation_states': np.round(np.random.rand(9))}
    response = requests.get(API_URL)
    data = response.json()
    return data

def json_to_matrix(json_data):
    values = np.array(json_data['occupation_states'])
    size = np.floor(np.sqrt(len(values))).astype(int)
    matrix_data = values[:size*size].reshape(size, size)
    return pd.DataFrame(matrix_data)

def main():
    st.title("Status")
    with st.empty():
        while True:
            data = fetch_data()
            matrix_df = json_to_matrix(data)
            plt.close('all')
            fig, ax = plt.subplots()
            annotations = matrix_df.map(lambda x: "occupied" if x == 1 else "free")
            sns.heatmap(matrix_df, annot=annotations, fmt="", cmap='coolwarm', cbar=False, ax=ax)
            ax.axis('off')
            st.pyplot(fig)
            time.sleep(2)

if __name__ == "__main__":
    main()
