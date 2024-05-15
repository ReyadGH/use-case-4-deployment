import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import arabic_reshaper
from bidi.algorithm import get_display


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(
        "https://raw.githubusercontent.com/ReyadGH/use-case-5-deployment/main/data/clean.csv"
    )


def intro() -> None:
    st.title("Unveiling Job Market Trends in Saudi Arabia: The Treasure Hunt")
    st.markdown(
        """
        ---
        Discover the vibrant job market of Saudi Arabia, where hidden treasures await. Whether you're searching for your dream job, hiring top talent, or planning for the future, our insights will guide you through this dynamic landscape. 
        Let's embark on this thrilling treasure hunt and uncover the opportunities shaping the workforce.
        """
    )


def plot_top_job_titles(df: pd.DataFrame) -> None:
    job_counts = df["job_title"].value_counts().head(10).reset_index()
    job_counts.columns = ["Job Title", "Count"]
    job_counts["Percentage"] = (job_counts["Count"] / job_counts["Count"].sum()) * 100
    job_counts = job_counts.sort_values(by="Count", ascending=True)

    fig = go.Figure(
        go.Bar(
            x=job_counts["Count"],
            y=job_counts["Job Title"],
            orientation="h",
            text=job_counts["Percentage"].apply(lambda x: f"{x:.2f}%"),
            textposition="outside",
        )
    )

    fig.update_layout(
        title="Top Job Titles",
        yaxis_title=None,
        xaxis_title="Number of Job Listings",
        showlegend=False,
    )

    st.plotly_chart(fig)

    # Add sentence about the most frequent job
    most_frequent_job = job_counts.iloc[-1]
    st.markdown(
        f"The most frequent job is **{most_frequent_job['Job Title']}**, with **{most_frequent_job['Percentage']:.2f}%** of open jobs."
    )


def plot_word_cloud(df: pd.DataFrame) -> None:
    text = " ".join(df["job_title"])

    # Make text readable for a non-Arabic library like wordcloud
    text = arabic_reshaper.reshape(text)
    text = get_display(text)

    wordcloud = WordCloud(
        font_path="app/fonts/Amiri-Regular.ttf",  # Specify the path to your Arabic font file
        width=1200,
        height=600,
        background_color="white",
    ).generate(text)

    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)


def plot_top_average_salaries(df: pd.DataFrame) -> None:
    region_salaries = df.groupby("region")["salary"].mean().reset_index()
    region_salaries.columns = ["Region", "Average Salary"]
    top_regions = region_salaries.sort_values(
        by="Average Salary", ascending=False
    ).head(3)

    top_regions_text = (
        f"The top three regions with the highest average salaries are:\n\n"
        f"1. **{top_regions.iloc[0]['Region']}**: Average Salary of {top_regions.iloc[0]['Average Salary']:.2f}\n"
        f"2. **{top_regions.iloc[1]['Region']}**: Average Salary of {top_regions.iloc[1]['Average Salary']:.2f}\n"
        f"3. **{top_regions.iloc[2]['Region']}**: Average Salary of {top_regions.iloc[2]['Average Salary']:.2f}"
    )
    st.markdown(top_regions_text)

    region_salaries = region_salaries.sort_values(by="Average Salary", ascending=False)
    fig = px.bar(
        region_salaries,
        x="Region",
        y="Average Salary",
        title="Average Salaries by Region",
    )
    st.plotly_chart(fig)


def plot_experience_vs_salary(df: pd.DataFrame) -> None:
    top_jobs = df["job_title"].value_counts().head(10).index
    filtered_df = df[df["job_title"].isin(top_jobs)]
    job_experience_salary = (
        filtered_df.groupby(["job_title", "exper"])["salary"].mean().reset_index()
    )
    job_experience_salary.columns = ["Job Title", "Experience", "Average Salary"]

    fig = px.scatter(
        job_experience_salary,
        x="Experience",
        y="Average Salary",
        color="Job Title",
        title="Experience vs. Average Salary by Job Title",
        labels={
            "Experience": "Years of Experience",
            "Average Salary": "Average Salary",
        },
    )
    st.plotly_chart(fig)


def plot_gender_distribution(df: pd.DataFrame) -> None:
    gender_counts = df["gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]

    fig = px.pie(
        gender_counts,
        names="Gender",
        values="Count",
        title="Gender Distribution by Position",
        color_discrete_map={"M": "blue", "F": "pink", "both": "gray"},
    )
    st.plotly_chart(fig)


def body(df: pd.DataFrame) -> None:
    regions = df["region"].unique()
    selected_regions = st.multiselect("Select Regions", regions, default=regions)

    filtered_df = df[df["region"].isin(selected_regions)]

    st.markdown(
        """
        ## The Quest for the Hottest Jobs
        """
    )

    plot_word_cloud(filtered_df)
    st.markdown(
        """
        Chart your career path in Saudi Arabia with key insights. Focus on high-demand jobs, explore regions with top salaries, and understand how experience raises earnings. Consider workplace dynamics, like gender distribution, for a supportive environment. Use this information to find your next big opportunity. Happy hunting!
        """
    )
    plot_top_job_titles(filtered_df)

    st.markdown(
        """
        ## Unearthing Regional Goldmines

        Visualize a vibrant map of Saudi Arabia dotted with treasure markers. Riyadh and Jeddah sparkle the brightest, offering a wide array of roles. Meanwhile, Dammam stands out for its high-paying jobs in the oil and gas sector, a true goldmine. This map not only reveals where jobs are plentiful but also highlights where salaries are soaring.

        """
    )

    plot_top_average_salaries(filtered_df)
    st.markdown("""
                ## Charting Your Career Path
                """)
    plot_experience_vs_salary(filtered_df)
    st.markdown("""
        Ready to supercharge your career? Imagine a vibrant marketplace where your experience directly boosts your earning power. Sometimes, taking a job with lower pay now can lead to better opportunities as you gain experience. Employers often pay less for less experienced workers, but sticking with a job can be a smart investment in your future.    """)

    st.markdown("""
        ## Picking Your Crew Members

        Finding the right work environment is just as important as the job itself. In Saudi Arabia, cultural factors like gender dynamics can greatly influence job satisfaction. The best job may not be the best fit if you're uncomfortable with your coworkers.

        To give you an idea of the gender distribution in various positions, take a look at the pie chart below. Understanding the workplace demographics can help you choose a job where you'll thrive.
    """)

    plot_gender_distribution(filtered_df)


def conclusion():
    st.subheader("Conclusion: Crafting Your Treasure Map")
    st.markdown(
        """
        As you explore this landscape, imagine how each insight fits into your treasure map. From the most sought-after job titles to the regions brimming with opportunities, and from salary treasures to the most valuable skills, each piece brings you closer to uncovering your career treasure. Dive in and discover how the Saudi Arabian job market can lead you to your next big find.
        """
    )


def app() -> None:
    # handling issues gracefully
    try:
        # load the data
        df = load_data()

        # render the page sections
        intro()
        body(df)
        conclusion()
    except Exception as e:
        st.title("Error loading the page 🤕")
        st.write("Something went wrong", e)


if __name__ == "__main__":
    app()
