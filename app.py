import subprocess
import streamlit as st

st.set_page_config(page_title="Wi-Fi Password Viewer", page_icon="📶", layout="centered")

st.title("📶 Wi-Fi Password Viewer")
st.markdown(
    """
    Easily view saved Wi-Fi profiles and their passwords on your Windows device.<br>
    <span style='color:gray; font-size: 0.9em;'>For educational and personal use only.</span>
    """,
    unsafe_allow_html=True,
)

def get_wifi_passwords():
    try:
        data = (
            subprocess.check_output(["netsh", "wlan", "show", "profiles"])
            .decode("utf-8", errors="ignore")
            .split("\n")
        )
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        wifi_list = []
        for i in profiles:
            results = (
                subprocess
                .check_output(["netsh", "wlan", "show", "profile", i, "key=clear"])
                .decode("utf-8", errors="ignore")
                .split("\n")
            )
            password_lines = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            password = password_lines[0] if password_lines else "N/A"
            wifi_list.append({"SSID": i, "Password": password})
        return wifi_list
    except Exception as e:
        st.error(f"Error: {e}")
        return []

if st.button("🔍 Show Wi-Fi Passwords"):
    with st.spinner("Fetching Wi-Fi profiles..."):
        wifi_passwords = get_wifi_passwords()
        if wifi_passwords:
            st.success("Found Wi-Fi profiles!")
            st.dataframe(wifi_passwords, use_container_width=True)
        else:
            st.warning("No Wi-Fi profiles found or access denied.")

st.markdown(
    """
    <hr>
    <div style='text-align:center; color:gray; font-size:0.9em;'>
        Made with ❤️ using Streamlit<br>
        <b>Note:</b> This app works only on Windows and requires appropriate permissions.
    </div>
    """,
    unsafe_allow_html=True,
)
