import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="DVD Rental Analysis Dashboard",
    page_icon="💿",
    layout="wide"
)

@st.cache_data #Decorator to speed up the app
def load_data():
    try:
        df = pd.read_csv("data/cleaned_unified_data.csv")
        return df
    except FileExistsError as e:
        st.warning(f'Error!: {e}')

def sidebar_filters(df):
    st.sidebar.header("Film Filters")

    df["Rental_Date"] = pd.to_datetime(df["Rental_Date"])
    df["Payment_Date"] = pd.to_datetime(df["Payment_Date"])

    start_date = st.sidebar.date_input(
        "Start Date",
        df["Rental_Date"].min().date()
    )

    end_date = st.sidebar.date_input(
        "End Date",
        df["Rental_Date"].max().date()
    )

    category = st.sidebar.multiselect(
        'Choose Category',
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )

    store = st.sidebar.multiselect(
        "Select Store",
        options=df['Store_ID'].unique(),
        default=df['Store_ID'].unique()
    )

    country = st.sidebar.multiselect(
        "Choose Country",
        options=df['Country'].unique(),
        default=df['Country'].unique()
    )
    
    return country, category, start_date, end_date, store

def filtered_data(df, country, category, start_date, end_date, store):
    filtered_df = df[
        (df["Rental_Date"].dt.date >= start_date) &
        (df["Rental_Date"].dt.date <= end_date) &
        (df["Category"].isin(category)) &
        (df["Store_ID"].isin(store)) &
        (df["Country"].isin(country))
    ]
    return filtered_df

def display_metrics(filtered_df):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🎥 Films", f"{filtered_df['Film_ID'].nunique():,}")
    
    with col2:
        st.metric("👥Total Customers", f"{filtered_df['Customer_ID'].nunique():,}")

    with col3:
        avg_rev = filtered_df['Payment_Amount'].mean() if len(filtered_df) > 0 else 0
        st.metric("💰Average Revenue", f'${avg_rev:,.2f}')

    with col4:
        tot_rents = filtered_df['Total_Rents'].sum() if len(filtered_df) > 0 else 0
        st.metric("🎬 Total Rentals", f'${tot_rents:,.2f}')

    with col5:
        top_cat = filtered_df['Category'].mode()[0] if len(filtered_df) > 0 else 0
        st.metric('🚙 Top Category', top_cat)     
            
def charts(filtered_df):
    if len(filtered_df) == 0:
        st.warning("Please Select Filters")
        return
    
def executive_overview(filtered_df):
    st.header("👨‍💼 Executive Overview")
        
    col1, col2 = st.columns(2)
    
    with col1:
        total_revenue = filtered_df["Payment_Amount"].sum() if len(filtered_df) > 0 else 0
        st.metric("💰 Total Revenue",f"${total_revenue:,.2f}")
    
    with col2:
        total_rentals = filtered_df["Rental_ID"].nunique() if len(filtered_df) > 0 else 0
        st.metric("🎬 Total Rentals",f"{total_rentals:,}")
    
    col3, col4 = st.columns(2)

    with col3:
        active_customers = filtered_df["Customer_ID"].nunique()if len(filtered_df) > 0 else 0
        st.metric("👥 Active Customers",f"{active_customers:,}")
    
    with col4:
        monthly_growth = (filtered_df.groupby("Rental_Month")["Payment_Amount"].sum().pct_change().mean() * 100) if len(filtered_df) > 0 else 0    
        st.metric("📈 Monthly Growth",f"{monthly_growth:.2f}%")

    
def customer_analytics(filtered_df):
    st.header("👥 Customer Analytics")
    if len(filtered_df) == 0:
        st.warning("Please Select Filters")
        return
    
    col1 = st.columns(1)[0]

    with col1:
        st.subheader("🏆 Top 10 Customers by Revenue")

        top_customers = (
            filtered_df.groupby("Customer_Name")["Payment_Amount"]
            .sum()
            .sort_values(ascending=True)
            .tail(10)
    )
    fig1 = px.bar(
        x=top_customers.values,
        y=top_customers.index,
        orientation="h" 
    )
    
    fig1.update_layout(
        xaxis_title="Amount_Paid",
        yaxis_title="Customer"
    )

    st.plotly_chart(fig1, use_container_width=True)


    col2 = st.columns(1)[0]
    with col2:
        st.subheader("🧑🏻‍🤝‍🧑🏾 Customer Retention")
        customer_rentals = filtered_df.groupby("Customer_ID")["Rental_ID"].count().reset_index(name="Total_Rentals")
        retained_customers = customer_rentals[customer_rentals["Total_Rentals"] > 1].shape[0]
        total_customers = filtered_df["Customer_ID"].nunique() # Fixed uppercase
        retention_rate = (retained_customers / total_customers) * 100 if total_customers > 0 else 0
    
        col5, col6 = st.columns(2)
        with col5:
            st.metric("🔁 Returning Customers", f"{retained_customers:,}")
        with col6:
            st.metric("📊 Retention Rate", f"{retention_rate:.2f}%")

    col3 = st.columns(1)[0]

    with col3:
        st.subheader("⚠️ Churn Risk Customers")
        cus_last_rental = filtered_df.groupby("Customer_ID")["Rental_Date"].max().reset_index()
        gen_latest_date = filtered_df["Rental_Date"].max()
        
        cus_last_rental["Inactive_Days"] = (gen_latest_date - cus_last_rental["Rental_Date"]).dt.days
        churn_risk = cus_last_rental[cus_last_rental["Inactive_Days"] > 90]
        
        
        total_customers = len(cus_last_rental)
        churn_count = len(churn_risk)
        active_count = total_customers - churn_count

        summary_df = pd.DataFrame({
            "Status": ["Active (<90d)", "Churn Risk (>90d)"],
            "Count": [active_count, churn_count]
        })

        fig = px.pie(
            summary_df, 
            values="Count", 
            names="Status", 
            hole=0.4,
            color="Status",
            color_discrete_map={"Active (<90d)": "lightgreen", "Churn Risk (>90d)": "crimson"}
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write(f"Inactive for >90 days: **{len(churn_risk):,}**")
        st.dataframe(
            churn_risk.sort_values("Inactive_Days", ascending=False), 
            use_container_width=True,
            hide_index=True
        )


def film_category_performance(filtered_df):
    st.header("🎬 Film & Category Performance")
    if len(filtered_df) == 0:
        st.warning("Please Select Filters")
        return
    
    col1 = st.columns(1)[0]
    with col1:
        st.subheader("🏆 Top 10 Films")
        top_films = (
            filtered_df.groupby("Film_Title")["Payment_Amount"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        
        fig1 = px.bar(
            x=top_films.values,
            y=top_films.index,
            orientation="h" 
        )
        
        fig1.update_layout(
            xaxis_title="Revenue Generated",
            yaxis_title="Film"
        )
    
        st.plotly_chart(fig1, use_container_width=True)
        

    col2 = st.columns(1)[0]
    with col2:
        st.subheader("📂 Revenue by Category")
        category_revenue = (
            filtered_df.groupby("Category")["Payment_Amount"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig2 = px.pie(
            category_revenue, 
            names="Category", 
            values="Payment_Amount", 
            title="Categorical Revenue Contribution",
        hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)

    
    col3 = st.columns(1)[0]
    with col3:
        st.subheader("💽 Inventory Risk Analysis")
        inventory_risk = (
            filtered_df.groupby("Film_Title")
            .agg(rentals=("Rental_ID", "count"),inventory=("Inventory_ID", "nunique")).reset_index()
        )
        inventory_risk["rental_pressure"] = (
            inventory_risk["rentals"] /
            inventory_risk["inventory"]
        )
        high_risk = (inventory_risk.sort_values("rental_pressure", ascending=False).head(10))
        
        st.write("Comparison between High Rental Demand Films and Available Inventory:")
        
        st.dataframe(high_risk, use_container_width=True)


        fig1 = px.bar(
            high_risk,
            x="rental_pressure",
            y="Film_Title",
            orientation="h",
            title="Top 10 Films by Inventory Rental Pressure",
            labels={"rental_pressure": "Rental Pressure (Rentals per Copy)", "Film_Title": ""},
            color="rental_pressure",
            color_continuous_scale="Reds"
        )
        fig1.update_layout(
            yaxis={'categoryorder':'total ascending'}, 
            showlegend=False)

        st.plotly_chart(fig1, use_container_width=True)


def store_staff_performance(filtered_df):
    st.header("🏬 Store & Staff Performance")

    store_comparison = (
        filtered_df.groupby("Store_ID")
            .agg(
             total_revenue=("Payment_Amount", "sum"),
                total_rentals=("Rental_ID", "count"),
                customers=("Customer_ID", "nunique")
            )
            .reset_index()
    )

    fig2 = px.pie(
        store_comparison,
        names="Store_ID",
        values="total_revenue",
        title="Staff Performance Comparison",
        hole=0.4
        )
    st.plotly_chart(fig2, use_container_width=True)

    
    st.subheader("👨‍💼 Staff Efficiency")


    staff_efficiency = (
        filtered_df.groupby(
            ["Staff_ID", "Staff_Name"]
        )
        .agg(
            total_revenue=("Payment_Amount", "sum"),
            rentals_processed=("Rental_ID", "count"),
            customers_served=("Customer_ID", "nunique")
        )
        .reset_index()
    )


    staff_efficiency["revenue_per_rental"] = (
        staff_efficiency["total_revenue"] /
        staff_efficiency["rentals_processed"]
    )

    fig2 = px.bar(
        staff_efficiency.sort_values(
            "total_revenue",
            ascending=False
        ).head(10),
        x="Staff_Name",
        y="total_revenue",
        title="Staff Performance by Revenue",
        text="total_revenue"
    )
    st.plotly_chart(fig2, use_container_width=True)

def geographic_insights(filtered_df):
    st.header("🌍 Geographic Insights")

    st.subheader("🌎 Revenue by Country")
    country_revenue = (filtered_df.groupby("Country")["Payment_Amount"].sum().reset_index().sort_values("Payment_Amount", ascending=False).head(15))

    fig1 = px.bar(
        country_revenue,
        x="Country",
        y="Payment_Amount",
        title="Top 15 Countries by Revenue",
        text="Payment_Amount"
    )


    st.plotly_chart(fig1, use_container_width=True)


    st.subheader("🏙 Revenue by City")
    city_revenue = (filtered_df.groupby("City")["Payment_Amount"].sum().reset_index().sort_values("Payment_Amount", ascending=False).head(20))

    fig2 = px.bar(
        city_revenue,
        x="City",
        y="Payment_Amount",
        title="Top 20 Cities by Revenue",
        text="Payment_Amount"
    )

    st.plotly_chart(fig2, use_container_width=True)


    st.subheader("🛐 Regional Customer Preferences")
    regional_preferences = (
        filtered_df.groupby("Country")
        .agg(
            customers=("Customer_ID", "nunique"),
            rentals=("Rental_ID", "count"),
            revenue=("Payment_Amount", "sum")
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    regional_preferences["average_customer_value"] = (
        regional_preferences["revenue"] /
        regional_preferences["customers"]
    )

    fig2 = px.scatter(
        regional_preferences.head(15), 
        x="customers",
        y="revenue",
        size="average_customer_value",
        color="Country",
        hover_name="Country",
        title="Top 15 Countries: Volume vs. Value Breakdown",
        labels={
            "customers": "Unique Customers",
            "revenue": "Total Revenue ($)",
            "average_customer_value": "Avg Value per Customer"
        },
        size_max=40
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(regional_preferences, use_container_width=True)


def download_data(filtered_df):

    st.sidebar.markdown("---")

    st.sidebar.subheader("⬇️ Download Filtered Data")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.sidebar.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="DVD_Rental_Analysis_Report.csv",
        mime="text/csv"
    )


#Control Function
def main():
    #load data
    df = load_data()

    if df is None:
        st.error("Dataset could not be loaded.")
        return


    # Sidebar Navigation

    page = st.sidebar.radio(
        "📌 Dashboard Pages",
        [
            "Executive Overview",
            "Customer Analytics",
            "Film & Category Performance",
            "Store & Staff Performance",
            "Geographic Insights"
        ]
    )

    #sidebar call
    country, category, start_date, end_date, store = sidebar_filters(df)

    #filter connection
    filtered_df = filtered_data(df, country, category, start_date, end_date, store)

    st.title('DVD Rental Analysis Dashboard')
    st.markdown('---')

    #Download data
    download_data(filtered_df)

    #Display pages
    if page == "Executive Overview":
        display_metrics(filtered_df) 
        executive_overview(filtered_df)
        
    elif page == "Customer Analytics":
        display_metrics(filtered_df)
        customer_analytics(filtered_df)
        
    elif page == "Film & Category Performance":
        display_metrics(filtered_df)
        film_category_performance(filtered_df)
        
    elif page == "Store & Staff Performance":
        display_metrics(filtered_df)
        store_staff_performance(filtered_df)
        
    elif page == "Geographic Insights":
        display_metrics(filtered_df)
        geographic_insights(filtered_df)

main()