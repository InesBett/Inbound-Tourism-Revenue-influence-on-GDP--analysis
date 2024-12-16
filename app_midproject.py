import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Fancy Title Design
st.markdown("""
    <style>
    .title {
        font-size: 50px;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #47FF64;
        text-align: center;
        background: linear-gradient(90deg, rgba(72, 61, 139, 0.8), rgba(0, 128, 128, 0.8));
        padding: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.2);
    }
    </style>
    <div class="title">🚀 My Streamlit App 🚀</div>
""", unsafe_allow_html=True)


st.write("Hello, this is my Streamlit app! Visualizations from my Mid Project, welcome 😊")

file_path = 'test_clean.csv'  # Replace this with your actual file path
df_clean = pd.read_csv(file_path)
st.write("Here is the data set being analyzed 📊")

st.dataframe(df_clean.head(5))

# Create frequency and proportion tables
frequency_table_region = df_clean.region.value_counts().reset_index()
frequency_table_region.columns = ['region', 'absolute_frequency']

proportion_table_region = df_clean.region.value_counts(normalize=True).round(2).reset_index()
proportion_table_region.columns = ['region', 'relative_frequency']

# Merge the two tables into region_table
region_table = pd.merge(frequency_table_region, proportion_table_region, on='region')

# Display the region_table
st.write("### Region Table")
st.dataframe(region_table)

# Create and display the barplot
st.write("### Barplot of Absolute Frequency by Region 🌍")
fig, ax = plt.subplots()
sns.barplot(x="region", y="absolute_frequency", data=region_table, palette="Greens", ax=ax)
ax.set_title("Absolute Frequency by Region")
st.pyplot(fig)

#pieplot
st.write("### Pie Chart of Absolute Frequency by Region")
fig_pie, ax_pie = plt.subplots()
region_table.set_index('region')['absolute_frequency'].plot.pie(autopct='%1.2f%%', startangle=90, colors=sns.color_palette('Set2'), ax=ax_pie)
ax_pie.set_ylabel('')  # Hide the ylabel for a cleaner look
st.pyplot(fig_pie)

#checking for distributions
numerical= df_clean.select_dtypes(include="number")
st.write("### Variables Distribution")
color = '#3CB371'
nrows, ncols = 5, 5  # adjust for your number of features
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(30, 20))
axes = axes.flatten()
# Plot each numerical feature
for i, ax in enumerate(axes):
    if i >= len(numerical.columns):
        ax.set_visible(False)  # hide unesed plots
        continue
    ax.hist(numerical.iloc[:, i], bins=30, color=color, edgecolor='black')
    ax.set_title(numerical.columns[i])
plt.tight_layout()
st.pyplot(fig)

#outliers
st.write("### Checking for outliers")
color = '#3CB371'
nrows, ncols = 5, 5
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(20, 16))
axes = axes.flatten()
for i, ax in enumerate(axes):
    if i >= len(numerical.columns):
        ax.set_visible(False)
        continue
    ax.boxplot(numerical.iloc[:, i].dropna(), vert=False, patch_artist=True,
               boxprops=dict(facecolor=color, color='black'),
               medianprops=dict(color='yellow'), whiskerprops=dict(color='black'),
               capprops=dict(color='black'), flierprops=dict(marker='o', color='red', markersize=5))
    ax.set_title(numerical.columns[i], fontsize=10)
    ax.tick_params(axis='x', labelsize=8)
plt.tight_layout()
st.pyplot(fig)


st.write("## Let's check for correlations! 🤝")

correlation_matrix= numerical.corr()
plt.figure(figsize=(8, 6))  # Adjust figure size as needed
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)

plt.title("Correlation Representation Heatmap")

st.pyplot(plt)

#evolution by year
st.write("### Evolution Inbound Tourism and GDP by year")
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot GDP on the first y-axis
sns.lineplot(data=df_clean, x='year', y='gdp', ax=ax1, color='b', label='GDP')
ax1.set_ylabel('GDP', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Create a second y-axis for Tourism Inbound
ax2 = ax1.twinx()
sns.lineplot(data=df_clean, x='year', y='tourism_inbound', ax=ax2, color='g', label='Tourism Inbound')
ax2.set_ylabel('Tourism Inbound', color='g')
ax2.tick_params(axis='y', labelcolor='g')

# Title and grid settings
plt.title('Evolution of GDP and Tourism Inbound over the Years')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Show legends for both axes
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Display the plot in Streamlit
st.pyplot(fig)

st.write("                      Hope you enjoyed my streamlit app! 😎")