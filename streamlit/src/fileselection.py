import streamlit as st
from .common import *  # Importing common functionalities from the 'common' module
import pandas as pd

patterns = [
    ["m/z", "mz", "mass over charge"],
    ["rt", "retention time", "retention-time", "retention_time"],
]

allowed_formats = "Allowed formats: csv (comma separated), tsv (tab separated), txt (tab separated), xlsx (Excel file)."

def string_overlap(string, options):
    """
    Check if any of the given options are present in the string.
    Exclude any string containing "mzml".

    Parameters:
    string (str): The string to be checked.
    options (list): A list of substrings to search for in the string.

    Returns:
    bool: True if any option is found in the string and "mzml" is not present, False otherwise.
    """
    for option in options:
        if option in string and "mzml" not in string:
            return True
    return False

def load_example():
    """
    Load example datasets into Streamlit's session state.
    """
    # Reset session state data
    for key in ['ft', 'md', 'nw', 'an_gnps', 'an_analog']:
        st.session_state[key] = None
        
    st.session_state['ft'] = open_df("example-data/FeatureMatrix.csv")
    st.session_state['md'] = open_df("example-data/MetaData.txt").set_index("filename")
    st.session_state['nw'] = open_df("example-data/NetworkNodePairs.tsv")
    st.session_state['an_gnps'] = open_df("example-data/GNPSannotations.tsv")
    st.session_state['an_analog'] = open_df("example-data/Analogannotations.tsv")

@st.cache_data  # Corrected cache decorator
def load_from_gnps(task_id):
    """
    Load data from GNPS based on a given task ID.

    Parameters:
    task_id (str): The GNPS task ID.

    Returns:
    tuple: A tuple of dataframes corresponding to feature table, metadata, network edges, and annotations.
    """
    # Reset session state data
    for key in ['ft', 'md', 'nw', 'an_gnps', 'an_analog']:
        st.session_state[key] = None

    # Define URLs for each file type based on the task ID
    ft_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=quantification_table_reformatted/&block=main"
    md_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=metadata_merged/&block=main"
    nw_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=networkedges_selfloop/&block=main"
    an_gnps_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=DB_result/&block=main"
    an_analog_url = f"https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={task_id}&file=DB_analogresult/&block=main"
    
    # Load data from URLs
    ft = pd.read_csv(ft_url)
    md = pd.read_csv(md_url, sep="\t", index_col="filename")
    nw = pd.read_csv(nw_url, sep="\t")
    an_gnps = pd.read_csv(an_gnps_url, sep="\t")
    an_analog = pd.read_csv(an_analog_url, sep="\t")

    return ft, md, nw, an_gnps, an_analog

def load_ft(ft_file):
    """
    Load and process the feature table.

    Parameters:
    ft_file (file): The feature table file.

    Returns:
    DataFrame: Processed feature table.
    """
    ft = open_df(ft_file)
    ft = ft.dropna(axis=1)  # Drop columns with missing values
    return ft

def load_md(md_file):
    """
    Load and process metadata. Set 'filename' as the index if present.

    Parameters:
    md_file (file): The metadata file.

    Returns:
    DataFrame: Processed metadata.
    """
    md = open_df(md_file)
    return md

def load_nw(network_file):
    """
    Load and process network pair file. 
    """
    nw = open_df(network_file)
    return nw

def load_annotation(annotation_file):
    """
    Load and process annotation file 
    """
    an_gnps = open_df(annotation_file)
    return an_gnps

def display_dataframe_with_toggle(df_key, display_name):
    if df_key in st.session_state and isinstance(st.session_state[df_key], pd.DataFrame):
        st.write(f"### {display_name}")

        col1, col2 = st.columns([0.8, 0.2])

        # Show dimensions
        num_rows, num_cols = st.session_state[df_key].shape
        col1.write(f"Dimension: {num_rows} rows × {num_cols} columns")

        view_all = col2.checkbox("View all", key=f"{df_key}_toggle")

        if view_all:
            st.dataframe(st.session_state[df_key])  # Show full dataframe
        else:
            st.dataframe(st.session_state[df_key].head())  # Show header
