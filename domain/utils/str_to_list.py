import streamlit as st


def strToList(value: str, sep=","):
    value = value.strip().strip(sep)
    if not value:
        return []
    try:
        return [float(i) for i in value.split(sep)]
    except ValueError:
        st.error("""আপনার কথাও ভুল হয়েছে  
                    - সংখ্যা গুলি কমা (,) দিয়ে আলাদা করুন. 
                    - এক সাথে একাধিক কমা দেওয়া যাবে না 
                    - সংখ্যা গুলি ইংরেজিতে হতে হবে 
                    - সংখ্যা ও অংক বাদে অন্য কিছু দেওয়া যাবে না
                     """)
        st.stop()
