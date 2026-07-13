import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Universal Data Visualizer", layout="wide")

st.title("📊 Universal Data Visualizer")
st.write("Upload any CSV or Excel dataset to explore and visualize it instantly.")

# 1. File Upload Section
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load data based on file type
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("File uploaded successfully!")
        
        # 2. Data Preview Section
        st.subheader("🧐 Dataset Overview")
        st.dataframe(df.head(10))
        
        # Display basic metadata
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", df.shape[0])
        col2.metric("Total Columns", df.shape[1])
        col3.metric("Missing Values", df.isna().sum().sum())
        
        # Filter columns by data type for easy plotting
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        all_cols = df.columns.tolist()

        st.markdown("---")
        
        # 3. Visualization Section
        st.subheader("📈 Interactive Visualizations")
        
        chart_type = st.selectbox(
            "Select Chart Type", 
            ["Scatter Plot", "Line Chart", "Bar Chart", "Distribution / Histogram", "Correlation Heatmap"]
        )
        
        # Handle visualizations dynamically
        if chart_type == "Scatter Plot":
            if len(numeric_cols) >= 2:
                x_axis = st.selectbox("X Axis (Numeric)", numeric_cols, index=0)
                y_axis = st.selectbox("Y Axis (Numeric)", numeric_cols, index=min(1, len(numeric_cols)-1))
                color_by = st.selectbox("Color By (Optional)", [None] + categorical_cols)
                
                fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by, title=f"{y_axis} vs {x_axis}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Scatter plot requires at least 2 numeric columns.")
                
        elif chart_type == "Line Chart":
            if numeric_cols:
                x_axis = st.selectbox("X Axis", all_cols)
                y_axis = st.selectbox("Y Axis (Numeric)", numeric_cols)
                color_by = st.selectbox("Color By (Optional)", [None] + categorical_cols)
                
                fig = px.line(df, x=x_axis, y=y_axis, color=color_by, title=f"{y_axis} over {x_axis}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Line chart requires at least 1 numeric column.")
                
        elif chart_type == "Bar Chart":
            x_axis = st.selectbox("X Axis (Categorical/Group)", all_cols)
            y_axis = st.selectbox("Y Axis (Numeric Value/Aggregation)", numeric_cols)
            color_by = st.selectbox("Color By (Optional)", [None] + categorical_cols)
            
            fig = px.bar(df, x=x_axis, y=y_axis, color=color_by, title=f"{y_axis} by {x_axis}", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "Distribution / Histogram":
            if numeric_cols:
                target_col = st.selectbox("Select Column to View Distribution", numeric_cols)
                nbins = st.slider("Number of Bins", min_value=5, max_value=100, value=30)
                
                fig = px.histogram(df, x=target_col, nbins=nbins, title=f"Distribution of {target_col}", marginal="box")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Histograms require at least 1 numeric column.")
                
        elif chart_type == "Correlation Heatmap":
            if len(numeric_cols) >= 2:
                corr = df[numeric_cols].corr()
                fig = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix", color_continuous_scale='RdBu_r')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Correlation Matrix requires at least 2 numeric columns.")

    except Exception as e:
        st.error(f"Error parsing file: {e}")
        
else:
    st.info("💡 Please upload a CSV or Excel file to get started.")