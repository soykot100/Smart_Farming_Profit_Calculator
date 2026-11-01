# -*- coding: utf-8 -*-
"""
translations.py
---------------
All the text shown on the website, in TWO languages: English and Bangla.
The user can switch between them with the EN / বাং button in the navbar.

How it works:
- TEXT is a dictionary. Key = short name, Value = {"en": ..., "bn": ...}
- In app.py we use get_text(key, lang) to pick the right language.
"""

TEXT = {
    "site_title":       {"en": "Smart Farming Profit Calculator",
                         "bn": "স্মার্ট কৃষি লাভ ক্যালকুলেটর"},
    "site_subtitle":    {"en": "Find out which land gives the highest profit using Matrix Multiplication",
                         "bn": "ম্যাট্রিক্স গুণ ব্যবহার করে জেনে নিন কোন জমিতে সবচেয়ে বেশি লাভ হবে"},
    "nav_home":         {"en": "Calculator", "bn": "ক্যালকুলেটর"},
    "nav_history":      {"en": "History", "bn": "ইতিহাস"},

    "step1_title":      {"en": "Step 1: Enter Crop Yield (kg)",
                         "bn": "ধাপ ১: ফসলের পরিমাণ দিন (কেজি)"},
    "step1_help":       {"en": "How much of each crop did each land produce?",
                         "bn": "প্রতিটি জমিতে প্রতিটি ফসলের কত পরিমাণ উৎপন্ন হয়েছে?"},
    "land":             {"en": "Land", "bn": "জমি"},

    "step2_title":      {"en": "Step 2: Enter Crop Price (Tk per kg)",
                         "bn": "ধাপ ২: ফসলের দাম দিন (প্রতি কেজি টাকা)"},
    "step2_help":       {"en": "Market selling price for each crop.",
                         "bn": "প্রতিটি ফসলের বাজার বিক্রয় মূল্য।"},

    "step3_title":      {"en": "Step 3: Enter Production Cost (Tk per land)",
                         "bn": "ধাপ ৩: উৎপাদন খরচ দিন (প্রতি জমি টাকা)"},
    "step3_help":       {"en": "Total cost (seed + fertilizer + labor) for each land.",
                         "bn": "প্রতিটি জমির মোট খরচ (বীজ + সার + শ্রম)।"},

    "step4_title":      {"en": "Step 4: Weather Simulation",
                         "bn": "ধাপ ৪: আবহাওয়া সিমুলেশন"},
    "step4_help":       {"en": "Choose a weather condition to see how it affects the profit.",
                         "bn": "আবহাওয়া কীভাবে লাভের উপর প্রভাব ফেলে তা দেখতে একটি আবহাওয়া নির্বাচন করুন।"},
    "weather_normal":   {"en": "Normal", "bn": "স্বাভাবিক"},
    "weather_good":     {"en": "Good Rain (+20%)", "bn": "ভালো বৃষ্টি (+২০%)"},
    "weather_drought":  {"en": "Drought (-30%)", "bn": "খরা (-৩০%)"},
    "weather_flood":    {"en": "Flood (-50%)", "bn": "বন্যা (-৫০%)"},

    "btn_calculate":    {"en": "Calculate", "bn": "হিসাব করুন"},
    "btn_save":         {"en": "Save Result", "bn": "ফলাফল সংরক্ষণ করুন"},
    "btn_export":       {"en": "Export CSV", "bn": "CSV ডাউনলোড"},
    "btn_print":        {"en": "Print / PDF", "bn": "প্রিন্ট / PDF"},
    "btn_delete":       {"en": "Delete", "bn": "মুছুন"},
    "btn_view":         {"en": "View", "bn": "দেখুন"},

    "result_title":     {"en": "Profit Analysis", "bn": "লাভ বিশ্লেষণ"},
    "kpi_best_land":    {"en": "Best Land", "bn": "সেরা জমি"},
    "kpi_mean_profit":  {"en": "Mean Profit", "bn": "গড় লাভ"},
    "kpi_std":          {"en": "Std Deviation", "bn": "মান বিচ্যুতি"},
    "kpi_risk":         {"en": "Risk Level", "bn": "ঝুঁকির মাত্রা"},
    "kpi_total_profit": {"en": "Total Profit", "bn": "মোট লাভ"},

    "chart_heatmap":    {"en": "Yield Heatmap", "bn": "ফলন হিটম্যাপ"},
    "chart_revenue":    {"en": "Revenue per Land (Tk)", "bn": "প্রতি জমির আয় (টাকা)"},
    "chart_profit":     {"en": "Profit per Land (Tk)", "bn": "প্রতি জমির লাভ (টাকা)"},

    "stat_title":       {"en": "Statistics (Profit)", "bn": "পরিসংখ্যান (লাভ)"},
    "stat_mean":        {"en": "Mean", "bn": "গড়"},
    "stat_median":      {"en": "Median", "bn": "মধ্যমা"},
    "stat_std":         {"en": "Std Dev", "bn": "মান বিচ্যুতি"},
    "stat_range":       {"en": "Range", "bn": "পরিসর"},

    "table_land":       {"en": "Land", "bn": "জমি"},
    "table_revenue":    {"en": "Revenue (Tk)", "bn": "আয় (টাকা)"},
    "table_profit":     {"en": "Profit (Tk)", "bn": "লাভ (টাকা)"},
    "table_best_crop":  {"en": "Best Crop", "bn": "সেরা ফসল"},

    "ttest_title":      {"en": "Fertilizer A/B Test (T-Test)",
                         "bn": "সারের A/B পরীক্ষা (T-Test)"},
    "ttest_help":       {"en": "Testing if a new organic fertilizer increases yield compared to traditional fertilizer.",
                         "bn": "নতুন জৈব সার পুরনো সারের চেয়ে ফলন বাড়ায় কিনা পরীক্ষা করা হচ্ছে।"},
    "ttest_old":        {"en": "Traditional (mean)", "bn": "পুরনো সার (গড়)"},
    "ttest_new":        {"en": "Organic (mean)", "bn": "জৈব সার (গড়)"},
    "ttest_tstat":      {"en": "T-Statistic", "bn": "T-স্ট্যাটিস্টিক"},
    "ttest_pval":       {"en": "P-Value", "bn": "P-মান"},
    "ttest_yes":        {"en": "The new fertilizer works! Yield increased significantly (p < 0.05).",
                         "bn": "নতুন সারটি কাজ করেছে! ফলন উল্লেখযোগ্যভাবে বেড়েছে (p < 0.05)।"},
    "ttest_no":         {"en": "The new fertilizer did NOT show a significant effect (p >= 0.05).",
                         "bn": "নতুন সারটি উল্লেখযোগ্য পরিবর্তন আনেনি (p >= 0.05)।"},

    "history_title":    {"en": "Saved Calculations", "bn": "সংরক্ষিত হিসাব"},
    "history_empty":    {"en": "No saved calculations yet.", "bn": "এখনও কোনো হিসাব সংরক্ষিত নেই।"},
    "history_date":     {"en": "Date", "bn": "তারিখ"},
    "history_total":    {"en": "Total Profit", "bn": "মোট লাভ"},
    "history_best":     {"en": "Best Land", "bn": "সেরা জমি"},
    "history_risk":     {"en": "Risk", "bn": "ঝুঁকি"},
    "history_actions":  {"en": "Actions", "bn": "কার্য"},

    "msg_saved":        {"en": "Result saved to history.", "bn": "ফলাফল ইতিহাসে সংরক্ষিত হয়েছে।"},
    "msg_deleted":      {"en": "Record deleted.", "bn": "রেকর্ড মুছে ফেলা হয়েছে।"},
    "msg_no_data":      {"en": "Please calculate something first.", "bn": "অনুগ্রহ করে প্রথমে হিসাব করুন।"},

    "footer":           {"en": "Simulation Project - Built with Python and Flask",
                         "bn": "সিমুলেশন প্রজেক্ট - Python এবং Flask দিয়ে তৈরি"},
    "language":         {"en": "Language", "bn": "ভাষা"},
}


def get_text(key, lang="en"):
    """Look up a text by its key in the chosen language. Falls back to English."""
    entry = TEXT.get(key, {})
    return entry.get(lang) or entry.get("en") or key
