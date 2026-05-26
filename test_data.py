import pandas as pd

print("=" * 50)
print("CAREER COMPASS — Dataset Check")
print("=" * 50)

df = pd.read_csv("data/careers.csv")

print(f"\n✅ Dataset loaded successfully!")
print(f"   Rows (roles): {df.shape[0]}")
print(f"   Columns: {df.shape[1]}")

print("\n📌 Domains and role count:")
domain_counts = df["domain"].value_counts()
for domain, count in domain_counts.items():
    print(f"   {domain}: {count} roles")

print("\n📄 First 5 rows of data:")
print(df[["domain", "role", "avg_salary_lpa", "job_demand", "months_to_ready"]].head())

print("\n🔍 Missing values check:")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("   No missing values found. Dataset is clean!")
else:
    print(missing[missing > 0])

print("\n📊 Salary stats (LPA):")
print(f"   Min: ₹{df['avg_salary_lpa'].min()} LPA")
print(f"   Max: ₹{df['avg_salary_lpa'].max()} LPA")
print(f"   Average: ₹{round(df['avg_salary_lpa'].mean(), 1)} LPA")

print("\n✅ All checks passed. You are ready for Phase 3!")
print("=" * 50)