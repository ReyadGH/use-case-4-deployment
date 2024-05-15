import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt


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
        f"The most frequent job is **{most_frequent_job['Job Title']}**, with {most_frequent_job['Percentage']:.2f}% market share."
    )


def plot_word_cloud(df: pd.DataFrame) -> None:
    text = " ".join(df["job_title"])
    wordcloud = WordCloud(
        font_path="https://raw.githubusercontent.com/ReyadGH/use-case-5-deployment/main/app/fonts/Amiri-Regular.ttf",  # Specify the path to your Arabic font file
        width=1200,
        height=600,
        background_color="white",
    ).generate(text)

    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)


def plot_job_distribution(df: pd.DataFrame) -> None:
    city_counts = df["city"].value_counts().reset_index()
    city_counts.columns = ["City", "Count"]

    fig = px.choropleth(
        city_counts,
        locations="City",
        locationmode="ISO-3",
        geojson="https://raw.githubusercontent.com/wjdanalharthi/GeoJSON-of-Saudi-Arabia-Regions/master/data/SA_regions.json",
        featureidkey="properties.name",
        color="Count",
        hover_name="City",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Job Distribution Across Cities",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)


def plot_average_salaries(df: pd.DataFrame) -> None:
    city_salaries = df.groupby("city")["salary"].mean().reset_index()
    city_salaries.columns = ["City", "Average Salary"]

    fig = px.bar(
        city_salaries, x="City", y="Average Salary", title="Average Salaries by City"
    )
    st.plotly_chart(fig)


def body(df: pd.DataFrame) -> None:
    st.markdown(
        """
        ## The Quest for the Hottest Jobs
        """
    )

    plot_word_cloud(df)
    st.markdown(
        """
        Imagine stepping into a bustling treasure trove of job opportunities. The job market in Saudi Arabia is rich with a variety of roles, each with its own unique appeal. The word cloud above showcases the diversity of job titles available, giving a visual representation of the most common positions.
        """
    )
    plot_top_job_titles(df)
    st.markdown(
        """
        ## Unearthing Regional Goldmines

        Explore the vibrant job markets across different cities in Saudi Arabia. The distribution of job listings reveals key hotspots, with Riyadh and Jeddah sparkling the brightest. These cities offer a wide array of roles, drawing talent from across the country. Meanwhile, Dammam stands out for its high-paying jobs in the oil and gas sector, making it a true goldmine.

        Our analysis uncovers where jobs are plentiful and where salaries are soaring, giving you a clear view of the regional opportunities. Visualize the job distribution and average salaries across various cities to better understand the landscape.
        """
    )
    plot_job_distribution(df)
    plot_average_salaries(df)


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
    except:
        st.title("Error loading the page 🤕")
        st.write("Something went wrong")


if __name__ == "__main__":
    app()
