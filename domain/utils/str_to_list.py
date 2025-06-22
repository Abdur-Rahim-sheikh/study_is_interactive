import streamlit as st


def strToList(value: str, sep=",", unit=float) -> list:
    value = value.strip().strip(sep)
    if not value:
        return []
    try:
        return [unit(i) for i in value.split(sep)]
    except ValueError:
        st.error(f"""আপনার কথাও ভুল হয়েছে  
                    - শব্দগুলি কমা (,) দিয়ে আলাদা করুন. 
                    - এক সাথে একাধিক কমা দেওয়া যাবে না 
                    - শব্দগুলি {unit} ফরম্যাটে হতে হবে।  
                     """)
        st.stop()
