import streamlit as st

def page_about():

    st.markdown("<h2></h2>", unsafe_allow_html=True)
    st.markdown("<h2></h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="margin-top: 100x;">MMaVVie</h1>
            <h1 style="margin-top: 100x;">The Music Source Separation Application</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<h2></h2>", unsafe_allow_html=True)
    st.markdown("<h2></h2>", unsafe_allow_html=True)

    st.header("PROJECT DESCRIPTION")
    st.write("""
    In the vast landscape of audio engineering and signal processing, the art of dissecting complex musical compositions 
    into their individual sonic components has witnessed a paradigm shift with the advent of music source separation. 
    This cutting-edge technology empowers us to unravel the intricate tapestry of sound, peeling back layers of 
    instruments and vocals from a mixed audio signal. The potential applications of music source separation are 
    far-reaching, spanning the realms of music production, content creation, academic research, and beyond.
    The motivation behind embarking on this music source separation project is rooted in the desire to democratize 
    the creative process, providing musicians, producers, and enthusiasts with a powerful toolset to reshape and 
    reimagine musical compositions. By isolating individual instruments, vocals, and other sound sources, we aim 
    to offer unprecedented control over the auditory experience, fostering creativity and innovation in music 
    production and beyond.
    Our music source separator will not only allow us to separate the vocals, but it will also allow us to separate 
    drums, bass. This will be a bonus to the music directors or enthusiasts to mix up vocals with the drumbeats 
    or the bass or even creating a different version of Karaoke from the original song which will let the end user 
    to try and test and be very innovatively creative.
    """)

    st.header("QUICK FACTS")
    st.write("""
    - User can search the song or upload an mp3/mp4/wav file or User can paste a Youtube link to get the song audio.
    - User can see the original audio and separated audio, and user can choose to download any source.
    - Once the original music audio is uploaded, all music sources which are present in the audio will be displayed. 
      For the source separation, source names will be displayed in the four categories: vocals, bass, drums, and other instruments 
      for the uploaded music.
    """)

    st.header("RESEARCH CONCLUSIONS")
    st.write("""
    - The project successfully demonstrates the potential of music source separation technology in dissecting complex musical 
      compositions into individual sonic components.
    - The technology provides a powerful toolset for musicians, producers, and enthusiasts, democratizing the creative process.
    - The ability to separate vocals, drums, and bass from a mixed audio signal opens up new possibilities for music production 
      and content creation.
    """)

    st.header("DEVELOPMENT")
    st.write("""
    - The project is in the planning phase, with development not yet started.
    - The application will support mp3/WAV/mp4 file formats, ensuring accessibility and convenience for users.
    - The vocal separation feature is a key focus, allowing users to mix vocals with other musical elements creatively.
    - The drum/bass/other instrument separation feature is also planned, aiming to offer more versatility in music production.
    - The Karaoke feature is the special feature that makes our product standalone.
    """)

    st.header("SUMMARY / COMMENTS")
    st.write("""
    - The Music Source Separation project represents a significant advancement in audio engineering and signal processing.
    - By enabling detailed separation of musical components, the project promises to revolutionize music production, study, and enjoyment.
    - Future developments aim to enhance the tool’s efficiency and expand its applications across various domains of the music industry.
    - This project inspires music enthusiasts and people who do not have access to high-level tools used in the music industry to 
      recreate and feel the joy of innovation with the help of easily accessible tools.
    """)

    st.header("STUDENTS")
    st.write("""
        - Moumita Patra
        - Massinissa Zekrini
        - Viet Thai Nguyen
        - Oluwatimileyin Victor Adedigba
        """)

    st.header("ADVISORS")
    st.write("""
        - Prof. Bill MANOS
        - Prof. Alaa BAKHTI
        """,
        unsafe_allow_html=True
    )
    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image("images/logo.png", width=300)
