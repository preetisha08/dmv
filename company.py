import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("company_dataset.csv")

## Data Cleaning

df['review_count'] = df['review_count'].str.replace('[(), Reviews]', '', regex=True)
df['review_count'] = df['review_count'].str.replace('k', '000')
df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')

df['years'] = df['years'].str.extract('(\d+)')
df['years'] = pd.to_numeric(df['years'], errors='coerce')

def clean_employees(emp):
    if pd.isna(emp):
        return None
    if "1 Lakh+" in emp:
        return 100000
    elif "50k-1 Lakh" in emp:
        return 75000
    elif "10k-50k" in emp:
        return 30000
    elif "5k-10k" in emp:
        return 7500
    elif "1k-5k" in emp:
        return 3000
    else:
        return None

df['employees_clean'] = df['employees'].apply(clean_employees)

df_clean = df.dropna(subset=['ratings', 'review_count', 'years', 'employees_clean'])


# 1. Pie Chart → Employees distribution across TOP companies

top_emp = df_clean.sort_values(by='employees_clean', ascending=False).head(5)

plt.figure(figsize=(6,6))
plt.pie(top_emp['employees_clean'], labels=top_emp['name'], autopct='%1.1f%%')
plt.title("Top Companies by Employee Distribution")
plt.show()


# 2. Funnel Chart → Rating-wise (Top 5 highest rated companies)

top_rating = df_clean.sort_values(by='ratings', ascending=False).head(5)

max_value = top_rating['ratings'].max()
widths = top_rating['ratings'] / max_value

plt.figure(figsize=(8,6))

for i, (name, value, width) in enumerate(zip(top_rating['name'], top_rating['ratings'], widths)):
    plt.barh(
        y=i,
        width=width,
        left=(1 - width) / 2,
        height=0.6
    )
    plt.text(0.5, i, f"{name} ({value})", 
             ha='center', va='center', color='white')

plt.yticks([])
plt.xlim(0, 1)
plt.title("Funnel Chart (Top 5 by Ratings)")
plt.gca().invert_yaxis()
plt.show()


# 3. Bar Chart → Companies vs Years

top_years = df_clean.sort_values(by='years', ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x='years', y='name', data=top_years)
plt.title("Top Companies by Years")
plt.xlabel("Years")
plt.ylabel("Company")
plt.show()


# 4. Line Chart → Company Type vs Average Ratings

ctype_group = df_clean.groupby('ctype')['ratings'].mean().reset_index()

plt.figure(figsize=(10,6))
plt.plot(ctype_group['ctype'], ctype_group['ratings'], marker='o')
plt.title("Company Type vs Average Ratings")
plt.xlabel("Company Type")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)
plt.show()


# 5. Histogram → Review Count Distribution

plt.figure(figsize=(8,5))
plt.hist(df_clean['review_count'], bins=10)
plt.title("Review Count Distribution")
plt.xlabel("Review Count")
plt.ylabel("Frequency")
plt.show()