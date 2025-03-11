import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"day.csv")

df["dteday"] = pd.to_datetime(df["dteday"])
df["year"] = df["dteday"].dt.year
df["month"] = df["dteday"].dt.month

# Sidebar untuk memilih tahun
st.sidebar.header("🔍 Filter Data")
year_options = ["2011", "2012", "2011 & 2012"]
selected_option = st.sidebar.radio("Pilih Tahun", year_options)

st.title("🚲 Dashboard Penyewaan Sepeda")

# Plot grafik
fig, ax = plt.subplots(figsize=(10, 5))

if selected_option == "2011":
    st.subheader(f"📅 Tren Penyewaan Sepeda pada tahun 2011")
    df_selected = df[df["year"] == 2011].groupby("month")["cnt"].sum()
    ax.plot(df_selected.index, df_selected.values, marker="o", linestyle="-", color="tab:blue", label="Tahun 2011")

elif selected_option == "2012":
    st.subheader(f"📅 Tren Penyewaan Sepeda pada tahun 2012")
    df_selected = df[df["year"] == 2012].groupby("month")["cnt"].sum()
    ax.plot(df_selected.index, df_selected.values, marker="o", linestyle="-", color="tab:orange", label="Tahun 2012")

else:
    st.subheader(f"📅 Perbandingan Tren Penyewaan Sepeda pada tahun 2011 vs 2012")
    df_2011 = df[df["year"] == 2011].groupby("month")["cnt"].sum()
    df_2012 = df[df["year"] == 2012].groupby("month")["cnt"].sum()

    ax.plot(df_2011.index, df_2011.values, marker="o", linestyle="-", color="tab:blue", label="Tahun 2011")
    ax.plot(df_2012.index, df_2012.values, marker="o", linestyle="-", color="tab:orange", label="Tahun 2012")


ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.7)

st.pyplot(fig)

st.sidebar.info("Pilih tahun untuk melihat tren penyewaan sepada")

# Bar Chart total penyewaan sepeda per bulan
st.subheader("📊 Total Penyewaan Sepeda per Bulan")

fig_bar, ax_bar = plt.subplots(figsize=(10, 5))
sns.barplot(x='month', y='cnt', data=df, estimator=sum, palette="Blues", ax=ax_bar)

ax_bar.set_xticks(range(0, 12))
ax_bar.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax_bar.set_xlabel("Bulan")
ax_bar.set_ylabel("Total Penyewaan Sepeda")
ax_bar.set_title("Total Penyewaan Sepeda per Bulan", fontsize=14, fontweight="bold", color="darkblue")

st.pyplot(fig_bar)

# Pie chart Penyewaan Berdasarkan Musim
st.subheader("🌦️ Persentase Penyewaan Sepeda Berdasarkan Musim")

musim = df.groupby('season')['cnt'].sum()
labels = ["Spring (Semi)", "Summer (Panas)", "Fall (Gugur)", "Winter (Dingin)"]
colors = plt.cm.Set2.colors

explode = [0.08 if i == musim.idxmax() else 0 for i in musim.index]

fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax_pie.pie(
    musim, labels=labels, autopct='%1.1f%%', colors=colors, 
    startangle=140, explode=explode, shadow=True, wedgeprops={'edgecolor': 'black'},
    textprops={'fontsize': 12, 'weight': 'bold'}
)

for autotext in autotexts:
    autotext.set_fontsize(14)
    autotext.set_color("darkblue")
    autotext.set_weight("bold")

ax_pie.set_title("Persentase Penyewaan Sepeda Berdasarkan Musim", fontsize=14, fontweight="bold", color="darkred")

st.pyplot(fig_pie)

# Heatmap Korelasi Faktor Cuaca dengan Penyewaan Sepeda
st.subheader("🔥 Korelasi antara Faktor Cuaca dan Penyewaan Sepeda")

korelasi = df[['cnt', 'temp', 'hum', 'atemp', 'windspeed']].corr()

fig_heatmap, ax_heatmap = plt.subplots(figsize=(8, 6))
sns.heatmap(
    korelasi, annot=True, fmt=".2f", cmap="coolwarm", linewidths=2, 
    linecolor="white", square=True, cbar=True, annot_kws={"size": 12}, ax=ax_heatmap
)

ax_heatmap.set_title("Heatmap Korelasi", fontsize=14, fontweight="bold", color="darkred")

st.pyplot(fig_heatmap)

st.success("Dashboard pertamaku! 🚀")
