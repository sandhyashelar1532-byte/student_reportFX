
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Student Analytics Studio",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

df = pd.read_csv("cleaned_student_data.csv")

# ---------------- COLOR PALETTE ----------------

COLORS = [
    "#7899E8",
    "#B69AD9",
    "#83C9B5",
    "#F2C28D",
    "#E9A6B8"
]

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background-color: #F8FAFD;
    color: #263449;
}

[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E4EAF2;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

/* Headings */

h1, h2, h3, h4 {
    color: #172B4D !important;
    font-weight: 750 !important;
}

/* Normal text */

p, label, .stMarkdown,
[data-testid="stCaptionContainer"] {
    color: #34445B !important;
}

/* Sidebar */

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #172B4D !important;
}

/* KPI Cards */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E1E8F2;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 14px rgba(35,55,90,0.05);
}

[data-testid="stMetricValue"] {
    color: #315DB5 !important;
    font-weight: 750 !important;
}

[data-testid="stMetricLabel"] {
    color: #40516B !important;
}

/* Chart Cards */

div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E5EAF2;
    border-radius: 16px;
    padding: 12px;
    box-shadow: 0 4px 14px rgba(35,55,90,0.04);
}

/* Buttons */

.stButton button,
.stDownloadButton button {
    background: #4776E6;
    color: #FFFFFF !important;
    border-radius: 9px;
    border: none;
    font-weight: 600;
}

/* Data Table */

[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border-radius: 12px;
}

/* Dividers */

hr {
    border-color: #E2E8F0;
}

</style>
""", unsafe_allow_html=True)

# ---------------- CHART DESIGN ----------------

def style_chart(fig):

    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FAFBFE",

        font=dict(
            family="Arial",
            color="#263449",
            size=13
        ),

        title_font=dict(
            size=19,
            color="#172B4D"
        ),

        margin=dict(
            l=25,
            r=25,
            t=65,
            b=35
        ),

        legend_title_font_color="#263449"
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#E5EAF2"
    )

    fig.update_yaxes(
        gridcolor="#E8EDF5",
        zeroline=False
    )

    return fig


# ---------------- SIDEBAR ----------------

st.sidebar.markdown("# 📊 SAS")
st.sidebar.caption("STUDENT ANALYTICS STUDIO")

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Student Analytics",
        "Data Explorer"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### Dataset Status")
st.sidebar.success("Sample data loaded")
st.sidebar.caption("Portfolio Project | Demo Dataset")


# ---------------- MAIN HEADER ----------------



st.title("Student Performance Dashboard")

st.markdown(
    "A smart platform to explore academic performance "
    "and attendance insights."
)

st.divider()


# ==================================================
#                  OVERVIEW PAGE
# ==================================================

if page == "Overview":

    st.subheader("Performance Overview")

    # KPI CARDS

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "👨‍🎓 Total Students",
        len(df)
    )

    c2.metric(
        "📘 Average Math",
        f"{df['Math_Score'].mean():.1f}"
    )

    c3.metric(
        "🔬 Average Science",
        f"{df['Science_Score'].mean():.1f}"
    )

    c4.metric(
        "📅 Attendance",
        f"{df['Attendance'].mean():.1f}%"
    )

    st.divider()

    # FIRST ROW CHARTS

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            df,
            x="Student",
            y="Math_Score",
            color="Student",
            color_discrete_sequence=COLORS,
            title="📘 Mathematics Performance",
            text_auto=True
        )

        fig.update_layout(showlegend=False)

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with right:

        fig = px.scatter(
            df,
            x="Attendance",
            y="Math_Score",
            color="Gender",
            size="Science_Score",
            hover_name="Student",
            color_discrete_sequence=[
                "#7899E8",
                "#E9A6B8"
            ],
            title="📈 Attendance vs Math Performance"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.divider()

    # SECOND ROW CHARTS

    left, right = st.columns(2)

    with left:

        subject_data = pd.DataFrame({
            "Subject": [
                "Mathematics",
                "Science"
            ],
            "Average Score": [
                df["Math_Score"].mean(),
                df["Science_Score"].mean()
            ]
        })

        fig = px.pie(
            subject_data,
            names="Subject",
            values="Average Score",
            hole=0.55,
            color_discrete_sequence=[
                "#7899E8",
                "#83C9B5"
            ],
            title="📊 Subject Score Distribution"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with right:

        fig = px.histogram(
            df,
            x="Attendance",
            nbins=6,
            color_discrete_sequence=["#B69AD9"],
            title="📅 Attendance Distribution"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


# ==================================================
#               STUDENT ANALYTICS PAGE
# ==================================================

elif page == "Student Analytics":

    st.subheader("Detailed Student Analytics")

    gender = st.selectbox(
        "Filter Students by Gender",
        ["All"] + sorted(df["Gender"].unique().tolist())
    )

    filtered = (
        df if gender == "All"
        else df[df["Gender"] == gender]
    )

    st.info(f"Showing {len(filtered)} students")

    # SUBJECT PERFORMANCE

    fig = px.line(
        filtered,
        x="Student",
        y=["Math_Score", "Science_Score"],
        markers=True,
        color_discrete_sequence=[
            "#7899E8",
            "#E9A6B8"
        ],
        title="📚 Subject-wise Performance"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

    # ATTENDANCE

    fig = px.bar(
        filtered,
        x="Student",
        y="Attendance",
        color="Gender",
        color_discrete_sequence=[
            "#83C9B5",
            "#F2C28D"
        ],
        title="📅 Student Attendance"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

    # STUDENT RECORDS

    st.subheader("Student Records")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
#                 DATA EXPLORER PAGE
# ==================================================

else:

    st.subheader("Dataset Explorer")

    st.write(
        "Explore and download the cleaned student dataset."
    )

    st.metric(
        "Total Records",
        len(df)
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        label="⬇ Download Cleaned Dataset",
        data=df.to_csv(index=False),
        file_name="cleaned_student_data.csv",
        mime="text/csv"
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Student Analytics Studio | "
    "Built with Python, Pandas, Streamlit & Plotly | "
    "Synthetic Demo Data"
)
