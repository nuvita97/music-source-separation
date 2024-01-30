import streamlit as st

def page_about():
    st.markdown(
        "<h1>About</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ## Introduction

        In the vast landscape of audio engineering and signal processing, the art of dissecting complex musical compositions into their individual sonic components has witnessed a paradigm shift with the advent of music source separation. This cutting-edge technology empowers us to unravel the intricate tapestry of sound, peeling back layers of instruments and vocals from a mixed audio signal. The potential applications of music source separation are far-reaching, spanning the realms of music production, content creation, academic research, and beyond.

        The motivation behind embarking on this music source separation project is rooted in the desire to democratize the creative process, providing musicians, producers, and enthusiasts with a powerful toolset to reshape and reimagine musical compositions. By isolating individual instruments, vocals, and other sound sources, we aim to offer unprecedented control over the auditory experience, fostering creativity and innovation in music production and beyond.

        Our music source separator will not only allow us to separate the vocals it will also allow to separate drums, bass. This will be a bonus to the music directors or enthusiasts to mix up vocals with the drumbeats or the bass or even creating a different version of Karaoke from the original song which will let the end user to try and test and be very innovatively creative.

        ## Architecture

        The architecture of our application is delineated by three integral components, each playing a pivotal role within the framework.

        - **User Interface (Streamlit):** This constituent serves as the interface through which end-users engage with our model. Users have the capability to select and separate tracks of choice, either uploaded or selected from YouTube, in addition to adjusting the pitch of a source in any desired direction. The implementation of these functionalities is facilitated through CSS embedding.

        - **Application Programming Interface (API) - FAST API:** Serving as the crucial link between the separation model and the user interface (Streamlit), the API boasts a designated "separate" endpoint. This endpoint triggers the model to perform the separation task, with the resulting components conveyed back to the user interface for consumption by end-users. This structured communication between the API and user interface ensures seamless functionality.

        - **The Model:** At the core of our architecture is the model responsible for source separation. Operating exclusively through the API, this component allows for modifications without impacting the end-user experience. This strategic design choice facilitates adaptability and scalability as needed.

        ## Students

        - Moumita Patra
        - Massinissa Zekrini
        - Viet Thai Nguyen
        - Oluwatimileyin Victor Adedigba

        ## Advisors

        - Prof. Bill MANOS
        - Prof. Alaa BAKHTI
        """,
        unsafe_allow_html=True
    )