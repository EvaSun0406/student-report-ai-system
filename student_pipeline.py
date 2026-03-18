"""
Module 1: Student Performance Intelligence Pipeline
====================================================
Author: Eva Sun Guizi | Portfolio Project for SG Secondary School Data Scientist Role
Description:
    Simulates a realistic Singapore secondary school dataset (500 students),
    performs data cleaning, feature engineering, and generates a risk-tiered
    analytics-ready dataset for dashboard and AI reporting (Modules 2 & 3).

Data domains:
    - Academic: subject scores across 6 subjects
    - Attendance: absence tracking over 2 semesters
    - CCA: participation hours and leadership roles
    - Pastoral: disciplinary incidents, teacher concern flags
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)
N = 500

# ─────────────────────────────────────────────
# 1. GENERATE STUDENT MASTER DATA
# ─────────────────────────────────────────────
print("=" * 55)
print("STEP 1: Generating student master records...")
print("=" * 55)

levels = ["Sec 1", "Sec 2", "Sec 3", "Sec 4"]
classes = {
    "Sec 1": ["1E1", "1E2", "1N1", "1N2"],
    "Sec 2": ["2E1", "2E2", "2N1", "2N2"],
    "Sec 3": ["3E1", "3E2", "3N1", "3N2"],
    "Sec 4": ["4E1", "4E2", "4N1", "4N2"],
}

student_ids      = [f"SGS{str(i).zfill(4)}" for i in range(1, N + 1)]
assigned_levels  = np.random.choice(levels, N, p=[0.28, 0.27, 0.25, 0.20])
assigned_classes = [np.random.choice(classes[lvl]) for lvl in assigned_levels]

df = pd.DataFrame({
    "student_id": student_ids,
    "level":      assigned_levels,
    "class":      assigned_classes,
})

print(f"  ✓ {N} student records created across {len(levels)} levels\n")

# ─────────────────────────────────────────────
# 2. GENERATE ACADEMIC SCORES
# ─────────────────────────────────────────────
print("STEP 2: Simulating academic performance...")

subjects    = ["English", "Mathematics", "Science", "Mother_Tongue", "Humanities", "Art"]
base_scores = np.random.normal(65, 8, N)

for subj in subjects:
    noise     = np.random.normal(0, 10, N)
    subj_bias = np.random.uniform(-5, 5)
    df[f"score_{subj}"] = np.clip(base_scores + noise + subj_bias, 0, 100).round(1)

score_cols             = [f"score_{s}" for s in subjects]
df["avg_score"]        = df[score_cols].mean(axis=1).round(1)
df["score_std"]        = df[score_cols].std(axis=1).round(1)
df["failing_subjects"] = (df[score_cols] < 50).sum(axis=1)

print(f"  ✓ Scores generated for {len(subjects)} subjects")
print(f"  ✓ Class average: {df['avg_score'].mean():.1f}  |  Std dev: {df['avg_score'].std():.1f}\n")

# ─────────────────────────────────────────────
# 3. GENERATE ATTENDANCE DATA
# ─────────────────────────────────────────────
print("STEP 3: Simulating attendance records...")

SCHOOL_DAYS   = 100
absence_rates = np.clip(0.04 + np.random.normal(0, 0.02, N), 0.0, 0.25)

df["days_absent_sem1"] = np.random.binomial(SCHOOL_DAYS, absence_rates)
df["days_absent_sem2"] = np.random.binomial(SCHOOL_DAYS, absence_rates * 1.05)
df["total_absences"]   = df["days_absent_sem1"] + df["days_absent_sem2"]
df["attendance_rate"]  = (
    (2 * SCHOOL_DAYS - df["total_absences"]) / (2 * SCHOOL_DAYS) * 100
).round(1)
df["chronic_absent"]   = df["attendance_rate"] < 85

print(f"  ✓ Attendance rate: mean={df['attendance_rate'].mean():.1f}%")
print(f"  ✓ Chronic absentees: {df['chronic_absent'].sum()} students "
      f"({df['chronic_absent'].mean()*100:.1f}%)\n")

# ─────────────────────────────────────────────
# 4. GENERATE CCA DATA
# ─────────────────────────────────────────────
print("STEP 4: Simulating CCA participation...")

cca_list    = ["Band", "Choir", "Debate", "Basketball", "Swimming",
               "Robotics Club", "Drama", "Badminton",
               "Environmental Club", "Student Council", "Art Club"]
cca_weights = [0.11, 0.09, 0.08, 0.10, 0.08,
               0.09, 0.08, 0.08, 0.08, 0.07, 0.14]

df["cca"]              = np.random.choice(cca_list, N, p=cca_weights)
df["has_cca"]          = True
df["cca_hours_weekly"] = np.clip(np.random.normal(4, 1.5, N), 1, 10).round(1)

leadership_prob      = np.where(df["avg_score"] > 75, 0.30, 0.08)
df["cca_leadership"] = np.random.binomial(1, leadership_prob).astype(bool)

print(f"  ✓ CCA participation: 100% (all Singapore secondary students have CCA)")
print(f"  ✓ Leadership roles: {df['cca_leadership'].sum()} students\n")

# ─────────────────────────────────────────────
# 5. GENERATE PASTORAL / BEHAVIOURAL FLAGS
# ─────────────────────────────────────────────
print("STEP 5: Simulating pastoral concerns...")

disc_prob = np.clip(
    0.08 + np.where(df["avg_score"] < 55, 0.08, 0) + np.random.normal(0, 0.02, N),
    0, 1
)
df["discipline_incidents"] = np.random.binomial(3, disc_prob)
df["teacher_concern_flag"] = (
    (df["avg_score"] < 55) |
    (df["attendance_rate"] < 88) |
    (df["discipline_incidents"] >= 2)
).astype(int)

print(f"  ✓ Teacher concern flags: {df['teacher_concern_flag'].sum()} students\n")

# ─────────────────────────────────────────────
# 6. RISK SCORING ENGINE
# ─────────────────────────────────────────────
print("STEP 6: Computing composite risk score...")
print("        (Weighted model — weights informed by educational research)")

risk_score = (
    # Academic domain (50%)
    0.30 * (1 - df["avg_score"] / 100) +
    0.20 * (df["failing_subjects"] / len(subjects)) +
    # Attendance domain (30%)
    0.20 * (1 - df["attendance_rate"] / 100) +
    0.10 * df["chronic_absent"].astype(float) +
    # Behavioural domain (20%)
    0.08 * (df["discipline_incidents"] / 3) +
    0.07 * (~df["has_cca"]).astype(float) +
    0.05 * df["teacher_concern_flag"].astype(float)
)

df["risk_score"] = (
    (risk_score - risk_score.min()) /
    (risk_score.max() - risk_score.min()) * 100
).round(1)

df["risk_tier"] = pd.cut(
    df["risk_score"],
    bins=[0, 30, 60, 100],
    labels=["Low", "Medium", "High"],
    include_lowest=True
)

tier_counts = df["risk_tier"].value_counts()
print(f"  ✓ Risk scoring complete:")
for tier in ["High", "Medium", "Low"]:
    n = tier_counts.get(tier, 0)
    print(f"      {tier:8s}: {n:3d} students ({n/N*100:.1f}%)")
print()

# ─────────────────────────────────────────────
# 7. DATA QUALITY CHECKS
# ─────────────────────────────────────────────
print("STEP 7: Data quality checks...")

checks = {
    "No null values":                 df.isnull().sum().sum() == 0,
    "Scores in valid range (0-100)":  ((df[score_cols] >= 0) & (df[score_cols] <= 100)).all().all(),
    "Attendance rate in valid range": ((df["attendance_rate"] >= 0) & (df["attendance_rate"] <= 100)).all(),
    "Risk scores normalised (0-100)": ((df["risk_score"] >= 0) & (df["risk_score"] <= 100)).all(),
    "Student IDs unique":             df["student_id"].nunique() == N,
}

for check, passed in checks.items():
    print(f"  {'✓' if passed else '✗'} {check}")
print()

# ─────────────────────────────────────────────
# 8. EXPORT DATASETS
# ─────────────────────────────────────────────
print("STEP 8: Exporting datasets...")

output_cols = [
    "student_id", "level", "class",
    *score_cols, "avg_score", "score_std", "failing_subjects",
    "days_absent_sem1", "days_absent_sem2", "total_absences",
    "attendance_rate", "chronic_absent",
    "cca", "has_cca", "cca_hours_weekly", "cca_leadership",
    "discipline_incidents", "teacher_concern_flag",
    "risk_score", "risk_tier"
]

df_export    = df[output_cols].copy()
df_high_risk = df[df["risk_tier"] == "High"].copy()
df_class     = df.groupby(["level", "class"]).agg(
    n_students           =("student_id",           "count"),
    avg_score            =("avg_score",            "mean"),
    attendance_rate      =("attendance_rate",      "mean"),
    high_risk_count      =("risk_tier",            lambda x: (x == "High").sum()),
    teacher_concern_count=("teacher_concern_flag", "sum"),
    cca_participation    =("has_cca",              "mean"),
).round(2).reset_index()

df_export.to_csv("student_analytics.csv",     index=False)
df_high_risk.to_csv("high_risk_students.csv", index=False)
df_class.to_csv("class_summary.csv",          index=False)

print(f"  ✓ student_analytics.csv      ({len(df_export)} rows, {len(output_cols)} columns)")
print(f"  ✓ high_risk_students.csv     ({len(df_high_risk)} students flagged)")
print(f"  ✓ class_summary.csv          ({len(df_class)} class records)")

# ─────────────────────────────────────────────
# 9. SUMMARY
# ─────────────────────────────────────────────
print()
print("=" * 55)
print("PIPELINE COMPLETE — SUMMARY")
print("=" * 55)
print(f"  Total students processed : {N}")
print(f"  School levels            : {', '.join(levels)}")
print(f"  Features engineered      : {len(output_cols)}")
print(f"  High-risk students       : {len(df_high_risk)}")
print(f"  Mean academic score      : {df['avg_score'].mean():.1f}/100")
print(f"  Mean attendance rate     : {df['attendance_rate'].mean():.1f}%")
print()
print("  Ready for:")
print("  → Module 2 : ReportReady Dashboard (student_analytics.csv)")
print("  → Module 3 : AI Letter Generation  (high_risk_students.csv)")
print("=" * 55)
