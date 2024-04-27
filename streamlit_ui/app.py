import json
import streamlit as st
import websockets
import asyncio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

websocket_url = "ws://public-ties-sniff.loca.lt/:8765/"

def to_matrix(data):
    values = np.array(data)
    size = int(np.sqrt(len(values)))
    return values.reshape(size, size)

def create_heatmap(data):
    plt.close('all')
    matrix_df = pd.DataFrame(data)
    fig, ax = plt.subplots()
    sns.heatmap(matrix_df, annot=True, fmt="d", cmap='coolwarm', cbar=False, ax=ax)
    ax.axis('off')
    return fig

async def receive_and_display_updates():
    async with websockets.connect(websocket_url) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            matrix_data = pd.DataFrame(to_matrix(data))
            if not matrix_data.empty:
                fig = create_heatmap(matrix_data)
                placeholder.pyplot(fig)
            await asyncio.sleep(1)

def main():
    st.title('Place Occupancy')
    global placeholder
    placeholder = st.empty()

    asyncio.run(receive_and_display_updates())

if __name__ == "__main__":
    main()
