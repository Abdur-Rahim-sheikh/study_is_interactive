import streamlit as st


def strToList(value, sep=","):
    value = value.strip().strip(",")
    if not value:
        return []
    try:
        return [int(i) for i in value.split(sep)]
    except ValueError:
        st.error(f"Invalid input. Please enter integers separated by ({sep}).")
