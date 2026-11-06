from gettext import install

import pip
import streamlit as st
import pandas as pd
import plotly.express as px 
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Marketing Dashboard", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<h1 style="
text-align:center;
color:#5A4632;
font-family:Georgia;
">
AI in Education Analytics Dashboard
</h1>
""",unsafe_allow_html=True)
st.title("“From Adoption to Impact: Understanding AI in Education.”")
st.markdown("<h1 style='text-align:left; font-style:italic; color:grey; font-size:25px;'>Interactive Global AI Adoption & Education Insights (2015–2026)</h1>",
             unsafe_allow_html=True
            )
#1. dat load
@st.cache_data
def load_data():
    data = pd.read_csv("ai_education_usage_global_2015_2026 (2).csv")
    return data
df = load_data()

# creating sliderbar

with st.sidebar:
    selected = option_menu(
        menu_title="AI Education Analytics",
        options=[
            "Dashboard",
            "Dataset",
            "EDA",
            "Country Analysis",
            "Region Analysis",
            "Time Series",
            "SQL Insights",
            "Correlation",
            "Insights",
            "About"
        ],
        icons=[
            "house",
            "table",
            "bar-chart",
            "globe",
            "map",
            "graph-up",
            "database",
            "activity",
            "lightbulb",
            "info-circle"
        ],
        menu_icon="robot",
        default_index=0,
    )
if selected == "Dashboard":
    st.subheader("🔍 Filters")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        country = st.selectbox(
                "🌍 Country",["All"] + sorted(df["country"].unique().tolist())
        )
    with col2:
        region = st.selectbox(
            "🌎 Region",
            ["All"] + sorted(df["region"].unique().tolist())
        )
    with col3:
        year = st.selectbox(
            "📅 Year",
            ["All"] + sorted(df["year"].unique().tolist())
            )
    month_mapping = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }
    df["month_name"] = df["month"].map(month_mapping)
    month_order = (
        df[["month", "month_name"]]
        .drop_duplicates()
        .sort_values("month")["month_name"]
        .tolist()
    )
    with col4:
        month = st.selectbox(
            "📆 Month",["All"] + month_order
        )
    filtered_df = df.copy()
    if country != "All":
        filtered_df = filtered_df[
            filtered_df["country"] == country
        ]
    if region != "All":
        filtered_df = filtered_df[
            filtered_df["region"] == region
        ]
    if year != "All":
        filtered_df = filtered_df[
            filtered_df["year"] == year
        ]
    if month != "All":
        filtered_df = filtered_df[
            filtered_df["month_name"] == month
        ]
    st.subheader("📊 KPI Cards")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_stud_usage = filtered_df['student_ai_usage_pct'].mean() 
        with st.container(border=True):
            st.metric(
                label="👨‍🎓 Average Student AI Usage (%)",
                value=f"{avg_stud_usage:.2f}%"
            )
    with col2:
        avg_teac_usage = filtered_df['teacher_ai_usage_pct'].mean()
        with st.container(border=True):
            st.metric(
                label="👨‍🏫 Average Teacher AI Usage (%)",
                value=f"{avg_teac_usage:.2f}%"
            )
    with col3:
        avg_school_usage = filtered_df['schools_ai_adoption_pct'].mean()
        with st.container(border=True):
            st.metric(
                label="🏫 Average School AI Adoption (%)",
                value=f"{avg_school_usage:.2f}%"
            )
    with col4:
        avg_internet_pen = filtered_df['internet_penetration_pct'].mean()
        with st.container(border=True):
            st.metric(
                label="🌐 Average Internet Penetration Rate (%)",
                value=f"{avg_internet_pen:.2f}%"
            )
    st.markdown("---")
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        import plotly.express as px
        student_usage_trend = (
            filtered_df.groupby("region")["student_ai_usage_pct"].mean().sort_values(ascending=False).reset_index()
        )
        fig = px.bar(
            student_usage_trend,
            x="student_ai_usage_pct",
            y="region",
            orientation="h",
            color="student_ai_usage_pct",
            text_auto=".1f",
            title="Average Student AI Usage by Region"
        )
        fig.update_layout(
            xaxis_title="Average AI Usage (%)",
            yaxis_title="",
            yaxis=dict(categoryorder="total ascending"),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    with chart_col2:
        country_AI_usage_trend = (
            filtered_df.groupby("country")["schools_ai_adoption_pct"].mean().sort_values(ascending=False).head(10).reset_index()
        )
        fig = px.bar(
            country_AI_usage_trend,
            x="country",
            y="schools_ai_adoption_pct",
            color="schools_ai_adoption_pct",
            color_continuous_scale="Viridis",
            text_auto=".1f",
            title="Average School AI Adoption by Country"
        )
        fig.update_layout(
            xaxis_title="Country",
            yaxis_title="Average School AI Adoption (%)",
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        tool_counts = (
        filtered_df["top_ai_tool"]
        .value_counts()
        .head(5)
        .reset_index()
    )

    tool_counts.columns = ["AI Tool", "Count"]

    fig = px.pie(
        tool_counts,
        names="AI Tool",
        values="Count",
        title="Top 5 AI Tools",
        hole=0.4
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    latest_year = filtered_df["year"].max()

    latest_df = filtered_df[
        filtered_df["year"] == latest_year
    ]
    st.subheader(f"📅 Latest Snapshot ({latest_year})")
    chart_col1, chart_col2, chart_col3 = st.columns(3)
    with chart_col1:
        latest_df = filtered_df[filtered_df["year"] == latest_year]
        country_ai_usage = (
            latest_df.groupby("country")["schools_ai_adoption_pct"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig = px.bar(
        country_ai_usage,
        x="country",
        y="schools_ai_adoption_pct",
        color="schools_ai_adoption_pct",
        color_continuous_scale="ice",
        text_auto=".1f",
        title=f"Top 10 Countries by School AI Adoption in {latest_year}"
        )

        fig.update_layout(
            xaxis_title="Country",
            yaxis_title="School AI Adoption (%)",
            xaxis_tickangle=-45,
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)
    with chart_col2:
        region_ai_usage = (
            latest_df.groupby("region")["student_ai_usage_pct"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        fig = px.bar(
            region_ai_usage,
            x="region",
            y="student_ai_usage_pct",
            color="student_ai_usage_pct",
            text_auto=".1f",
            title=f"Average Student AI Usage by Region in {latest_year}"
        )
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Student AI Usage (%)",
            xaxis_tickangle=-45,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    with chart_col3:
        region_teacher_usage = (
            latest_df.groupby("region")["teacher_ai_usage_pct"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        fig = px.bar(
            region_teacher_usage,
            x="region",
            y="teacher_ai_usage_pct",
            color="teacher_ai_usage_pct",
            text_auto=".1f",
            title=f"Average Teacher AI Usage by Region in {latest_year}"
        )
        fig.update_layout(
            xaxis_title="Region",
            yaxis_title="Teacher AI Usage (%)",
            xaxis_tickangle=-45,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
elif selected == "Dataset":
    st.subheader("📋 Raw Dataset")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", f"{df.shape[1]}")
    c3.metric("Countries", f"{df['country'].nunique()}")
 
    search = st.text_input("🔎 Search (matches any column value, e.g. country name)")
    view_df = df.copy()
    if search:
        mask = view_df.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False))
        view_df = view_df[mask.any(axis=1)]
 
    st.dataframe(view_df, use_container_width=True, height=450)
 
    st.download_button(
        "⬇️ Download filtered data as CSV",
        data=view_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_ai_education_data.csv",
        mime="text/csv",
    )
 
elif selected == "EDA":
    st.subheader("📊 Exploratory Data Analysis (EDA)")
    st.write("This section provides visual insights into the dataset.")
    st.markdown("---")
    import plotly.express as px
    numeric_cols = [
                "student_ai_usage_pct",
                "teacher_ai_usage_pct",
                "schools_ai_adoption_pct",
                "internet_penetration_pct",
            ]
    stats_col = st.selectbox(
                        "Choose a feature for statistic analysis",
                        numeric_cols,
                        key="stats_col"
                    )
    st.subheader(f"📊 Statistics for {stats_col}")
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Mean",f"{df[stats_col].mean():.2f}")
    c2.metric("Median",f"{df[stats_col].median():.2f}")
    c3.metric("Std Dev",f"{df[stats_col].std():.2f}")
    c4.metric("Min",f"{df[stats_col].min():.2f}")
    c5.metric("Max",f"{df[stats_col].max():.2f}")

    st.subheader("📚 Dataset Information")

    with st.expander("📊 Column Summary"):
        st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

    with st.expander("📝 Data Types"):
        datatype_df = pd.DataFrame({
            "Column": df.columns,
            "Datatype": df.dtypes.astype(str)
        })
        st.dataframe(datatype_df, use_container_width=True)

    with st.expander("❓ Missing Values"):
        missing_df = pd.DataFrame({
            "Column": df.columns,
            "Missing Values": df.isnull().sum().values
        })
        st.dataframe(missing_df, use_container_width=True)

    with st.expander("🔢 Unique Values"):
        unique_df = pd.DataFrame({
            "Column": df.columns,
            "Unique Values": df.nunique().values
        })
        st.dataframe(unique_df, use_container_width=True)

    selected_col = st.selectbox("Choose a feature", numeric_cols)
    c1, c2 = st.columns(2)
    with c1:
        import plotly.express as px
        st.subheader("1.📊 Distribution of AI Usage (%)")
        fig = px.histogram(
            df,
            x=selected_col,
            nbins=20,
            color_discrete_sequence=["#8A6B47"]
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("2.📦 Box Plot (Outlier Detection)")

        fig = px.box(
            df,
            y=selected_col,
            color_discrete_sequence=["#8A6B47"]
        )

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)
            
    col1, col2 = st.columns(2)
    with col1:
        Q1 = df[selected_col].quantile(0.25)
        Q3 = df[selected_col].quantile(0.75)

        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[
            (df[selected_col] < lower) |
            (df[selected_col] > upper)
        ]

        st.write(f"Number of Outliers: {len(outliers)}")
        st.dataframe(outliers)
        if len(outliers) == 0:
            st.success("✅ No outliers detected.")
        else:
            st.write(f"Number of Outliers: {len(outliers)}")
            st.dataframe(outliers)
elif selected == "Country Analysis":
    st.subheader("🌍 Country Analysis")
    country = st.selectbox(
        "Select a Country",
        sorted(df["country"].unique().tolist())
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        country_df = df[df["country"] == country]
        avg_student_usage = country_df["student_ai_usage_pct"].mean()
        with st.container(border=True):
            st.metric("Average Student AI Usage (%)", f"{avg_student_usage:.2f}%")
    with col2:
        avg_teacher_usage = country_df["teacher_ai_usage_pct"].mean()
        with st.container(border=True):
            st.metric("Average Teacher AI usage(%)",f"{avg_teacher_usage:.2f}%")
    with col3:
        avg_school_adoption = country_df["schools_ai_adoption_pct"].mean()
        with st.container(border=True):
            st.metric("Average School AI Adoption (%)", f"{avg_school_adoption:.2f}%")
    with col4:
        avg_internet_penetration = country_df["internet_penetration_pct"].mean()
        with st.container(border=True):
            st.metric("Average Internet Penetration Rate (%)", f"{avg_internet_penetration:.2f}%")
    st.subheader("🌎 Country vs Global Average")
    import plotly.express as px 
    comparison = pd.DataFrame({
        "Metric": [
            "Student AI Usage",
            "Teacher AI Usage",
            "School AI Adoption",
            "Internet Penetration"
        ],
        "selected_country": [
            country_df["student_ai_usage_pct"].mean(),
            country_df["teacher_ai_usage_pct"].mean(),
            country_df["schools_ai_adoption_pct"].mean(),
            country_df["internet_penetration_pct"].mean()
        ],
        "Global Average": [
            df["student_ai_usage_pct"].mean(),
            df["teacher_ai_usage_pct"].mean(),
            df["schools_ai_adoption_pct"].mean(),
            df["internet_penetration_pct"].mean()
        ]
    })

    comparison_long = comparison.melt(
        id_vars="Metric",
        var_name="Group",
        value_name="Average (%)"
    )

    fig = px.bar(
        comparison_long,
        x="Metric",
        y="Average (%)",
        color="Group",
        barmode="group"
    )
    st.plotly_chart(fig, use_container_width=True)    

    st.subheader(f"📈 AI Usage Trend")

    trend = (
        country_df
        .groupby("year")[
            [
                "student_ai_usage_pct",
                "teacher_ai_usage_pct",
                "schools_ai_adoption_pct"
            ]
        ]
        .mean()
        .reset_index()
    )

    trend_long = trend.melt(
        id_vars="year",
        var_name="Metric",
        value_name="Usage (%)"
    )

    fig = px.line(
        trend_long,
        x="year",
        y="Usage (%)",
        color="Metric",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)


    st.subheader("🏆 Country Ranking")

    ranking = (
        df.groupby("country")[
            [
                "student_ai_usage_pct",
                "teacher_ai_usage_pct",
                "schools_ai_adoption_pct"
            ]
        ]
        .mean()
        .reset_index()
    )

    ranking["Overall AI Score"] = ranking[
        [
            "student_ai_usage_pct",
            "teacher_ai_usage_pct",
            "schools_ai_adoption_pct"
        ]
    ].mean(axis=1)

    ranking = ranking.sort_values(
        "Overall AI Score",
        ascending=False
    )

    ranking["Rank"] = range(1, len(ranking) + 1)

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )
elif selected == "Region Analysis":
    st.subheader("🌎 Region Analysis")
    region = st.selectbox(
        "Select a Region",
        sorted(df["region"].unique().tolist())
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        region_df = df[df["region"] == region]
        avg_student_usage = region_df["student_ai_usage_pct"].mean()
        with st.container(border=True):
            st.metric("Average Student AI Usage (%)", f"{avg_student_usage:.2f}%")
    with col2:
        avg_teacher_usage = region_df["teacher_ai_usage_pct"].mean()
        with st.container(border=True):
            st.metric("Average Teacher AI usage(%)",f"{avg_teacher_usage:.2f}%")
    with col3:
        avg_school_adoption = region_df["schools_ai_adoption_pct"].mean()
        with st.container(border=True):
            st.metric("Average School AI Adoption (%)", f"{avg_school_adoption:.2f}%")
    with col4:
        avg_internet_penetration = region_df["internet_penetration_pct"].mean()
        with st.container(border=True):
            st.metric("Average Internet Penetration Rate (%)", f"{avg_internet_penetration:.2f}%")
    st.subheader("📊 AI Adoption Across Regions")

    region_summary = (
        df.groupby("region")[
            [
                "student_ai_usage_pct",
                "teacher_ai_usage_pct",
                "schools_ai_adoption_pct"
            ]
        ]
        .mean()
        .reset_index()
    )
    
    region_long = region_summary.melt(
        id_vars="region",
        var_name="Metric",
        value_name="Average (%)"
    )

    fig = px.bar(
        region_long,
        x="region",
        y="Average (%)",
        color="Metric",
        color_discrete_sequence=["#7E6649", "#907750", "#877056"],
        barmode="group"
    )

    fig.update_layout(
        xaxis_title="Region",
        yaxis_title="Average (%)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("gov_ai_policy")
    policy_region = (
    df.groupby(["region", "government_ai_policy"])
      .size()
      .reset_index(name="Policy Count")
    )
    fig = px.bar(
        policy_region,
        x="Policy Count",
        y="region",
        color="government_ai_policy",
        color_discrete_sequence=["#9F7E58", "#D4B483", "#C1A17D"],
        orientation="h",
        barmode="stack",
        title="Government AI Policy Status by Region",
    )
    fig.update_layout(
    xaxis_title="Number of Policies",
    yaxis_title="Region",
    legend_title="Policy Status"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Regional Performance")

    ranking_region = (
            df.groupby("region")[
                [
                    "student_ai_usage_pct",
                    "teacher_ai_usage_pct",
                    "schools_ai_adoption_pct"
                ]
            ]
            .mean()
            .reset_index()
        )
    ranking_region["Overall AI Score"] = ranking_region[
            [
                "student_ai_usage_pct",
                "teacher_ai_usage_pct",
                "schools_ai_adoption_pct"
            ]
        ].mean(axis=1)
    
    ranking_region = ranking_region.sort_values(
            "Overall AI Score",
            ascending=False
        )
    
    ranking_region["Rank"] = range(1, len(ranking_region) + 1)
    
    st.dataframe(
            ranking_region,
            use_container_width=True,
            hide_index=True
        )
elif selected == "Time Series":
    st.title("📅 Time Analysis")
    st.write("Tracking the pace and growth of AI adoption over time.")
    st.subheader("1. 📊 2015 vs Latest Year")

    first_year = df["year"].min()
    latest_year = df["year"].max()

    comparison = df[df["year"].isin([first_year, latest_year])].groupby("year")[
        [
            "student_ai_usage_pct",
            "teacher_ai_usage_pct",
            "schools_ai_adoption_pct",
            "internet_penetration_pct"
        ]
    ].mean().reset_index()

    comparison_melted = comparison.melt(
        id_vars="year",
        var_name="Metric",
        value_name="Percentage"
    )

    fig = px.bar(
        comparison_melted,
        x="Metric",
        y="Percentage",
        color="year",
        barmode="group",
        text_auto=".1f",
        title=f"{first_year} vs {latest_year}"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.subheader("2. 📈 Year-over-Year Growth")

    growth_col = st.selectbox(
        "Select Metric",
        [
            "student_ai_usage_pct",
            "teacher_ai_usage_pct",
            "schools_ai_adoption_pct",
            "internet_penetration_pct"
        ],
        key="growth_metric"
    )

    yearly = (
        df.groupby("year")[growth_col]
        .mean()
        .reset_index()
    )

    yearly["YoY Growth (%)"] = (
        yearly[growth_col].pct_change() * 100
    )

    growth_df = yearly.dropna()

    fig = px.bar(
        growth_df,
        x="year",
        y="YoY Growth (%)",
        text_auto=".1f",
        title=f"Year-over-Year Growth: {growth_col}"
    )

    st.plotly_chart(fig, use_container_width=True)


    # -------------------------------
    # 3. Top 5 Growth Years
    # -------------------------------
    st.subheader("3. 🚀 Top 5 Highest-Growth Years")

    top_growth = (
        growth_df
        .sort_values("YoY Growth (%)", ascending=False)
        .head(5)
    )

    fig = px.bar(
        top_growth.sort_values("YoY Growth (%)"),
        x="YoY Growth (%)",
        y="year",
        orientation="h",
        text_auto=".1f",
        title="Top 5 Years by Growth"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("4. ⚡ Growth Acceleration / Deceleration")

    yearly["Acceleration (%)"] = (
        yearly["YoY Growth (%)"].diff()
    )

    acceleration_df = yearly.dropna()

    fig = px.bar(
        acceleration_df,
        x="year",
        y="Acceleration (%)",
        text_auto=".1f",
        title=f"Growth Acceleration / Deceleration: {growth_col}"
    )

    st.plotly_chart(fig, use_container_width=True)

# PAGE: SQL Insights
# ---------------------------------------------------------------------------

elif selected == "SQL Insights":
    import sqlite3
    conn = sqlite3.connect("education conn.db")

    df.to_sql("education",
        conn,
        if_exists="replace",
        index=False
    )
    st.title("🗄️ SQL Insights")
    query_option = st.selectbox(
        "Choose SQL Analysis",
        [
            "total records by countries and religions",
            "average student ai usage by country",
            "average teacher ai usage by country",
            "Top 10 Countries by School AI Adoption",
            "Average daily AI usage by Region",
            "Yearly AI Adoption Trend",
            "Monthly AI Usage Trend",
            "AI Usage by Government Policy",
            "AI Usage by AI Curriculum",
            "Urban-Rural Gap by Country",
            "Countries with AI Usage above Global Average",
            "Top 5 Countries in each Region",
            "Highest AI Adoption in each Year",
            "Year-over-Year Growth using lag()",
            "Rank Countries by Student AI Usage (DENSE_RANK())",
            "Countries with Highest Gender Gap in AI Usage",
            "Countries with high Education Index but low School AI Adoption.",
            "Countries above the global average Student AI Usage.",
            "Count of Countries with AI Curriculum.",
        ]
    )
    if query_option == "total records by countries and religions":
        query = """
        SELECT country, region, year,
        COUNT(student_ai_usage_pct) AS total_records , COUNT(teacher_ai_usage_pct) as total_teacher_record
        FROM education 
        GROUP BY country, region,year;"""
        st.markdown("**SQL Query:**")
        st.code("""SELECT country, region, year,"
        "COUNT(student_ai_usage_pct) AS total_records , COUNT(teacher_ai_usage_pct) as total_teacher_record"
        "FROM education "
        "GROUP BY country, region,year;""",language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result, use_container_width=True)
        fig = px.bar(
        result,
        x="country",
        y="total_records",
        color="total_records",
        color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "average student ai usage by country":
        query ="""Select country, avg(student_ai_usage_pct) as avg_student_ai_uasage
        from education
        group by country;"""
        st.markdown("**SQL Query:**")
        st.code("""Select country, avg(student_ai_usage_pct) as avg_student_ai_uasage
        from  education 
        group by country;""", language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="country",
            y="avg_student_ai_uasage",
            color="avg_student_ai_uasage",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "average teacher ai usage by country":
        query = """select country, avg(teacher_ai_usage_pct) as avg_teacher_ai_usage
        from education
        group by country;"""
        st.markdown("**SQL Query:**")
        st.code("""select country, avg(teacher_ai_usage_pct) as avg_teacher_ai_usage
        from education
        group by country;""", language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="country",
            y="avg_teacher_ai_usage",
            color="avg_teacher_ai_usage",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Top 10 Countries by School AI Adoption":
        query = """select country, avg(schools_ai_adoption_pct) as avg_school_ai_adoption
        from education
        group by country
        order by avg_school_ai_adoption desc
        limit 10;"""
        st.markdown("**SQL Query:**")
        st.code("""select country, avg(schools_ai_adoption_pct) as avg_school_ai_adoption
        from education
        group by country
        order by avg_school_ai_adoption desc
        limit 10;""", language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="country",
            y="avg_school_ai_adoption",
            color="avg_school_ai_adoption",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Average daily AI usage by Region":
        query = """select region,avg(avg_daily_ai_usage_min)avg_daily_ai_usage_min
        from education
        group by region;"""
        st.markdown("**SQL Query:**")
        st.code("""select region,avg(avg_daily_ai_usage_min)avg_daily_ai_usage_min
        from education
        group by region;""", language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="region",
            y="avg_daily_ai_usage_min",
            color="avg_daily_ai_usage_min",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Yearly AI Adoption Trend":
        query = """select year, avg(student_ai_usage_pct) as student_ai_usage_pct
        from education
        group by year;"""
        st.markdown("**SQL Query:**")
        st.code("""select year, avg(student_ai_usage_pct) as student_ai_usage_pct
        from education
        group by year;""", language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.line(
            result,
            x="year",
            y="student_ai_usage_pct",
            markers=True,
            color_discrete_sequence=["#8A6B47"]
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Monthly AI Usage Trend":
        query = """select year, month, avg(student_ai_usage_pct) as student_ai_usage_pct
        from education
        group by year, month;"""
        st.markdown("**SQL Query:**")
        st.code("""select year, month, avg(student_ai_usage_pct) as student_ai_usage_pct
        from education
        group by year, month;""", language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.line(
            result,
            x="month",
            y="student_ai_usage_pct",
            markers=True,
            color_discrete_sequence=["#8A6B47"]
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "AI Usage by Government Policy":
        query = """select government_ai_policy,count(top_ai_tool) as total_ai_in_gov_policy
        from education
        group by government_ai_policy;"""
        st.markdown("**SQL Query:**")
        st.code("""select government_ai_policy,count(top_ai_tool) as total_ai_in_gov_policy
        from education
        group by government_ai_policy;""", language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        policy_status = (
        df["government_ai_policy"]
        .value_counts()
        .reset_index()
        )
        policy_status.columns = ["Policy Status", "Count"]

        fig = px.pie(
            policy_status,
            names="Policy Status",
            values="Count",
            title="Government AI Policy Status"
        )

        fig.update_traces(
            textinfo="percent+label"
        )

        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "AI Usage by AI Curriculum":
        query = """select ai_in_curriculum,count(top_ai_tool) as total_ai_in_curriculum
        from education
        group by ai_in_curriculum;"""
        st.markdown("**SQL Query:**")
        st.code("""select ai_in_curriculum,count(top_ai_tool) as total_ai_in_curriculum
        from education
        group by ai_in_curriculum;""", language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="ai_in_curriculum",
            y="total_ai_in_curriculum",
            color="total_ai_in_curriculum",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Urban-Rural Gap by Country":
        query = """SELECT
        country,region,
        ROUND(AVG(urban_ai_usage_pct),2) AS Urban_AI_Usage,
        ROUND(AVG(rural_ai_usage_pct),2) AS Rural_AI_Usage,
        ROUND(AVG(urban_ai_usage_pct)-AVG(rural_ai_usage_pct),2) AS Usage_Gap
        from education
        GROUP BY country,region
        ORDER BY Usage_Gap DESC;"""
        st.markdown("**SQL Query:**")
        st.code("""SELECT
        country,region,
        ROUND(AVG(urban_ai_usage_pct),2) AS Urban_AI_Usage,
        ROUND(AVG(rural_ai_usage_pct),2) AS Rural_AI_Usage,
        ROUND(AVG(urban_ai_usage_pct)-AVG(rural_ai_usage_pct),2) AS Usage_Gap
        from education
        GROUP BY country,region
        ORDER BY Usage_Gap DESC;""", language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="country",
            y="Usage_Gap",
            color="Usage_Gap",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Countries with AI Usage above Global Average":
        query = """SELECT country, region,
        AVG(student_ai_usage_pct) AS avg_student_ai_usage,
        AVG(teacher_ai_usage_pct) AS avg_teacher_ai_usage,
        AVG(schools_ai_adoption_pct) AS avg_school_ai_adoption
        FROM education
        GROUP BY country, region
        HAVING AVG(student_ai_usage_pct) > (SELECT AVG(student_ai_usage_pct) FROM education)
        OR AVG(teacher_ai_usage_pct) > (SELECT AVG(teacher_ai_usage_pct) FROM education)
        OR AVG(schools_ai_adoption_pct) > (SELECT AVG(schools_ai_adoption_pct) FROM education);"""
        st.markdown("**SQL Query:**")
        st.code("""SELECT country, region,
        AVG(student_ai_usage_pct) AS avg_student_ai_usage,
        AVG(teacher_ai_usage_pct) AS avg_teacher_ai_usage,
        AVG(schools_ai_adoption_pct) AS avg_school_ai_adoption
        FROM education
        GROUP BY country, region
        HAVING AVG(student_ai_usage_pct) > (SELECT AVG(student_ai_usage_pct) FROM education)
        OR AVG(teacher_ai_usage_pct) > (SELECT AVG(teacher_ai_usage_pct) FROM education)
        OR AVG(schools_ai_adoption_pct) > (SELECT AVG(schools_ai_adoption_pct) FROM education);""", language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="country",
            y="avg_student_ai_usage",
            color="avg_student_ai_usage",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Top 5 Countries in each Region":
        query = """WITH CountryRank AS (
            SELECT
                region,
                country,
                ROUND(AVG(schools_ai_adoption_pct), 2) AS avg_ai_adoption,
                ROW_NUMBER() OVER (
                    PARTITION BY region
                    ORDER BY AVG(schools_ai_adoption_pct) DESC
                ) AS rn
            FROM education
            GROUP BY region, country
        )
        SELECT
            region,
            country,
            avg_ai_adoption
        FROM CountryRank
        WHERE rn <= 5
        ORDER BY region, avg_ai_adoption DESC;"""
        st.markdown("**SQL Query:**")
        st.code("""WITH CountryRank AS (
            SELECT
                region,
                country,
                ROUND(AVG(schools_ai_adoption_pct), 2) AS avg_ai_adoption,
                ROW_NUMBER() OVER (
                    PARTITION BY region
                    ORDER BY AVG(schools_ai_adoption_pct) DESC
                ) AS rn
            FROM education
            GROUP BY region, country
        )
        SELECT
            region,
            country,
            avg_ai_adoption
        FROM CountryRank;
        WHERE rn <= 5
        ORDER BY region, avg_ai_adoption DESC;""",language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="country",
            y="avg_ai_adoption",
            color="avg_ai_adoption",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Highest AI Adoption in each Year":
        query = """select year,country,avg(schools_ai_adoption_pct) as ai_adoptation
        FROM education
        group by year,country;"""
        st.markdown("**SQL Query:**")
        st.code("""select year,country,avg(schools_ai_adoption_pct) as ai_adoptation
        FROM education
        group by year,country;""",language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.line(
            result,
            x="ai_adoptation",
            y="year",
            markers=True,
            color_discrete_sequence=["#8A6B47"]
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Year-over-Year Growth using lag()":
        query = """with yearoveryear as(
        select year, round(avg(schools_ai_adoption_pct),2) as ai_adoption,
        round(LAG(avg(schools_ai_adoption_pct)) OVER (ORDER BY year),2) as previous_year_ai_adoptation
        FROM education
        GROUP BY year
        )
        select year,ai_adoption,previous_year_ai_adoptation,
        round(ai_adoption- previous_year_ai_adoptation,2)as absolute_growth,
        round(((ai_adoption - previous_year_ai_adoptation)
                / NULLIF(previous_year_ai_adoptation, 0)) * 100,
                2
            ) AS yoy_growth_pct
        from yearoveryear
        order by year;"""
        st.markdown("**SQL Query:**")
        st.code(query, language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.line(
            result,
            x="year",
            y="yoy_growth_pct",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Rank Countries by Student AI Usage (DENSE_RANK())":
        query = """select year,country, SUM(student_ai_usage_pct) as total_student_ai_uasage,
        dense_rank() over(ORDER BY SUM(student_ai_usage_pct) ASC) as denserank
        from education
        group by year,country;"""
        st.markdown("**SQL Query:**")
        st.code(query, language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="country",
            y="total_student_ai_uasage",
            color="total_student_ai_uasage",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Countries with Highest Gender Gap in AI Usage":
        query = """select year,country,max(gender_gap_ai_usage_pct) as max_gender_gap,min(gender_gap_ai_usage_pct) as min_gender_gap
        from education
        group by year,country;"""
        st.markdown("**SQL Query:**")
        st.code(query, language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="country",
            y="max_gender_gap",
            color="max_gender_gap",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Countries with high Education Index but low School AI Adoption.":
        query = """WITH CountryStats AS (
        SELECT
            country,
            ROUND(AVG(education_index), 2) AS avg_education_index,
            ROUND(AVG(schools_ai_adoption_pct), 2) AS avg_school_ai_adoption
        FROM education
        GROUP BY country
        ),
        Thresholds AS (
            SELECT
                AVG(avg_education_index) AS avg_education_index,
                AVG(avg_school_ai_adoption) AS avg_school_ai_adoption
            FROM CountryStats
        )
        SELECT
            c.country,
            c.avg_education_index,
            c.avg_school_ai_adoption
        FROM CountryStats c
        CROSS JOIN Thresholds t
        WHERE c.avg_education_index > t.avg_education_index
        AND c.avg_school_ai_adoption < t.avg_school_ai_adoption
        ORDER BY c.avg_education_index DESC;"""
        st.markdown("**SQL Query:**")
        st.code(query, language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="country",
            y="avg_education_index",
            color="avg_education_index",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Countries above the global average Student AI Usage.":
        query = """select country,avg(student_ai_usage_pct) as avg_student_ai_usage
        from education
        group by country
        having avg(student_ai_usage_pct) > (select avg(student_ai_usage_pct) from education);"""
        st.markdown("**SQL Query:**")
        st.code(query, language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="country",
            y="avg_student_ai_usage",
            color="avg_student_ai_usage",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif query_option == "Count of Countries with AI Curriculum.":
        query = """select ai_in_curriculum,count(country) as total_countries_with_ai_curriculum
        from education
        group by ai_in_curriculum;"""
        st.markdown("**SQL Query:**")
        st.code(query, language="sql")
        result = pd.read_sql(query,conn)
        st.dataframe(result,use_container_width=True)
        fig=px.bar(
            result,
            x="ai_in_curriculum",
            y="total_countries_with_ai_curriculum",
            color="total_countries_with_ai_curriculum",
            color_continuous_scale="Brwnyl"
        )
        st.plotly_chart(fig, use_container_width=True)
elif selected == "Correlation":

    st.title("🔗 Correlation Analysis")
    st.write("Explore relationships between AI adoption and education-related indicators.")

    numeric_cols = [
        "student_ai_usage_pct",
        "teacher_ai_usage_pct",
        "schools_ai_adoption_pct",
        "internet_penetration_pct"
    ]

    corr = df[numeric_cols].corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        title="Correlation Matrix",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1
    )

    st.plotly_chart(fig, use_container_width=True)
    st.subheader("📈 Relationship Between Variables")
    col1, col2 = st.columns(2)

    with col1:
        x_var = st.selectbox(
            "Select X Variable",
            numeric_cols,
            key="corr_x"
        )

    with col2:
        y_options = [col for col in numeric_cols if col != x_var]

        y_var = st.selectbox(
            "Select Y Variable",
            y_options,
            key="corr_y"
        )
    correlation = df[x_var].corr(df[y_var])
    st.metric(
        "Pearson Correlation",
        f"{correlation:.2f}"
    )

    fig = px.scatter(
        df,
        x=x_var,
        y=y_var,
        trendline="ols",
        title=f"{x_var} vs {y_var}"
    )

    st.plotly_chart(fig, use_container_width=True)
elif selected == "Insights":

    st.title("💡 Key Insights")
    st.write(
        "Key findings from the analysis of global AI adoption in education "
        "between 2015 and 2026."
    )

    st.markdown("---")
    st.subheader("📈 Growth trend")
    st.markdown("""
    1. **Steady, near-linear global growth:** Student AI usage rose from ~5% (2015) to ~61% (2026) — about +5 points/year, with no sign of acceleration or plateau.

    2. **School adoption trails usage slightly:** From ~3% to ~59% over the same period — schools consistently lag student usage by 1–2 points.

    3. **Every region grew at virtually the same rate:** All six regions started 2015 between 4–6% and converged to 59–63% by 2026 — Europe finishes highest (62.5%), South America lowest (60%).

    4. **Urban-rural convergence over time:** Rural usage went from ~0% (2015) to ~51% (2026), while urban rose from ~8% to ~64% — both grew, but the ~12–13 point gap never closed.
""")
    st.subheader("🌍 Country/region comparisons (mostly flat)")
    st.markdown("""
    1.**Countries are nearly indistinguishable in usage:**student usage ranges only 30.6%-31.6% across all 10 countries — a ~1 point spread, despite huge disparities in real-world education index (0.52-0.94) and internet access (42%-96%).

    2. **Same flatness for teachers, school adoption, and gender gap:**every country sits within ~1-1.5 points of the global mean on each metric.

    3. **Canada and Australia show the highest average daily AI usage minutes (35.5 and 34.4 min/day);**Brazil and the US the lowest (30.3 and 30.2 min/day) — but differences are small and inconsistent with other metrics.

    4. **Teachers consistently trail students slightly:**teacher usage runs ~1.1 points below student usage on average, most pronounced in the US (-1.65) and Nigeria (-1.3), smallest in Germany (-0.53).

    5. **AI usage metrics show ~0.00 correlation with education_index —**countries with far better education systems show no more AI adoption.

    6. **AI usage also shows ~0.00 correlation with internet penetration —**surprising, since internet access is normally a precondition for AI tool use.

    7. **Education index and internet penetration correlate strongly with each other (0.98) as expected in the real world —**so those two "background" columns behave realistically, while the AI usage columns appear to be generated independently of them.

    8. **Regional education index and internet penetration do reflect real-world patterns:**Oceania/Europe/North America (~0.91-0.93 index, 92-96% internet) far outpace Africa (0.52 index, 42% internet) — but this real disparity doesn't show up anywhere in AI usage numbers.

""")
    st.header("Internal consistency (these correlations are strong — the AI columns move together)")
    st.markdown("""
    1. **Student, teacher, school-adoption, urban, and rural usage are all highly correlated with each other (0.97-0.99) —**they appear to be generated from one underlying "usage level" per record rather than independent phenomena.

    2. **Gender gap is uncorrelated with everything (~0.00 across the board), including usage level itself —**high-usage and low-usage country-months show the same gender gap on average.

""")
    st.header("Seasonality")
    st.markdown("""
    1. **Slight seasonal dip mid-year:**usage peaks Jan-Apr (~32.4-32.6%) and dips May-Jul (~29.8-30.0%), a modest ~2.5 point swing — could reflect school calendar effects, though given point 9-11 this may also just be noise.

    2. **. Gender gap fluctuates 5.05-5.91 across years with no clear trend —**no evidence AI adoption is closing or widening the gender gap over time.

""")
    st.header("Policy & curriculum")
    st.markdown("""
    1. **Government AI policy status barely moves the needle:**"Draft" policy countries actually show the highest average usage (31.96%) and adoption (30.49%), edging out "Active" (30.36%/28.59%) — counter to what you'd expect, and the spread is small enough to be noise.

    2. **Curriculum inclusion has a marginal positive association:**countries with AI in curriculum average 31.34% student usage vs 30.63% without — a <1 point difference.

""")
    st.header("Tool & structural notes")
    st.markdown("""
    1. **Preferred AI tool varies by region without a clear driver:**ChatGPT leads in Asia, Europe, and South America; Khanmigo leads in North America and Oceania; Microsoft Copilot leads in Africa — tool adoption ties to region more than to usage level, tool choice doesn't correlate with daily-usage minutes in any meaningful way (31.7-34.1 min range across tools).

    2. **Region sample sizes are uneven (Asia has 408 records from 3 countries; Africa/Oceania/South America each have only 136 from a single country) —**any region-level comparison is implicitly weighted by how many countries represent it, which could bias region-level averages, especially for Asia.
""")
elif selected == "About":
    st.title("ℹ️ About This Project")
    st.write("AI in Education Analytics Dashboard is an interactive data analytics project that explores global trends in artificial intelligence adoption in education from 2015 to 2026.")
    st.markdown("----")
    st.subheader("🎯 Project Objective")
    st.markdown("""The objective of this project is to analyze AI usage among students and teachers, school-level AI adoption, internet penetration, and differences across countries and regions.""")
    st.subheader("📊 What This Dashboard Includes")
    st.markdown("""------
        ## 📊 Dashboard Sections
        - 🏠 Dashboard
        - 📋 Dataset
        - 📊 Exploratory Data Analysis
        - 🌍 Country Analysis
        - 🗺️ Region Analysis
        - 📈 Time Series Analysis
        - 🗄️ SQL Insights
        - 🔗 Correlation Analysis
        - 💡 Key Insights
        ---

        ## 🛠️ Technologies Used

        - Python
        - Pandas
        - Streamlit
        - Plotly
        - SQLite
        - SQL

        ---
        """)
    st.subheader("📌 Key Features")
    st.markdown("""-----
       -Interactive filters
        -KPI cards
        -data visualization
        -statistical analysis
        -outlier detection
        -correlation analysis
        -SQL queries
        -geographical comparisons
    """)
    st.subheader("🎓 Project Conclusion")
    st.markdown("""his project demonstrates how data analytics and interactive visualization
    can be used to understand patterns and trends in AI adoption in education
    across different countries, regions, and years""")
    
