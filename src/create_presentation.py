"""
create_presentation.py - Professional Slide Deck Generator (Fixed for python-pptx API)
========================================================================================
Generates Dengue_Forecasting_Presentation.pptx at the root level.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


def build_presentation():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    FIG_DIR = os.path.join(BASE_DIR, "figures")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    NAVY = RGBColor(16, 44, 87)
    BLUE = RGBColor(30, 86, 160)
    DARK_GRAY = RGBColor(50, 50, 50)
    WHITE = RGBColor(255, 255, 255)
    
    blank_layout = prs.slide_layouts[6]
    
    def add_header(slide, title_text, category_text="MACHINE LEARNING RESEARCH"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = 'Arial'
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE
        p_cat.space_after = Pt(4)
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = 'Arial'
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

    # SLIDE 1: TITLE SLIDE
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY
    
    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.0), Inches(4.5))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "EXPLAINABLE SHORT-TERM DENGUE CASE FORECASTING"
    p.font.name = 'Arial'
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(8)
    
    p2 = tf1.add_paragraph()
    p2.text = "Using Weather and Epidemiological Indicators with Multi-Horizon ML & SHAP"
    p2.font.name = 'Calibri'
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(160, 200, 240)
    p2.space_after = Pt(48)
    
    p3 = tf1.add_paragraph()
    p3.text = "Candidate: [Student Name]  |  Roll Number: [Student Roll Number]\nSupervisor: [Professor / Project Guide Name]\nDepartment of Computer Science & Engineering"
    p3.font.name = 'Calibri'
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(220, 220, 220)

    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Operational Problem & Healthcare Motivation")
    tb2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    points2 = [
        ("The Global Burden:", "Dengue fever infects hundreds of millions annually. In tropical cities like San Juan, Puerto Rico, epidemics rapidly overwhelm intensive care units and blood banks."),
        ("The Operational Lead Time Gap:", "Municipal health departments cannot react to same-day notifications. They require actionable 1-to-4 week operational advance warning:\n  • 1-Week Ahead: Emergency triage and hospital nurse/bed reallocation.\n  • 2 to 4-Weeks Ahead: Targeted municipal insecticide spraying, larvicide treatment, and public awareness campaigns."),
        ("Limitations of Existing Systems:", "Conventional methods rely on reactive reporting, ignore biological incubation delays between weather and disease, or use 'black-box' algorithms that doctors cannot interpret.")
    ]
    for title, desc in points2:
        p = tf2.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(15)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(14)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(16)

    # SLIDE 3: BIOLOGICAL DELAY MECHANISM
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Biological Mechanisms Driving Delayed Weather Effects")
    tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    points3 = [
        ("Why Weather is Lagged (Not Instant):", "Today's weather does not determine today's recorded hospital cases. There is a strict multi-week physical delay:"),
        ("Stage 1: Larval Habitat Generation (1 to 2 Weeks):", "Rainfall creates standing water pools. Aedes aegypti eggs hatch, progress through 4 larval instars, and emerge as adult mosquitoes."),
        ("Stage 2: Extrinsic Incubation Period (EIP) (1 to 2 Weeks):", "An adult mosquito bites an infected human. The virus requires 8 to 14 days of warm temperatures (26–30°C) to replicate inside the mosquito gut and reach salivary glands."),
        ("Stage 3: Intrinsic Human Incubation (4 to 10 Days):", "Once an infectious mosquito bites a human, viral replication takes 4 to 10 days before febrile symptoms manifest and hospital records are logged."),
        ("Core Takeaway:", "Meteorological conditions from 2 to 8 weeks ago govern current dengue transmission. Feature engineering must model these delays.")
    ]
    for title, desc in points3:
        p = tf3.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(14)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(12)

    # SLIDE 4: DATASET & BENCHMARK AUDIT
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Dataset & Benchmark Overview: San Juan, Puerto Rico")
    tb4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    points4 = [
        ("Surveillance Scope:", "San Juan, Puerto Rico (18 continuous years, 1990 to 2008). 936 weekly observations."),
        ("Disease Target:", "Weekly laboratory-confirmed dengue case counts (total_cases). Median: 19 cases; Peak Outbreak: 461 cases."),
        ("Environmental Telemetry:", "20 continuous features including ground station temperature/rainfall, NOAA atmospheric reanalysis (specific humidity, dew point), and satellite NDVI vegetation indices."),
        ("Causal Imputation:", "Applied strict forward-fill (ffill) time-series imputation to eliminate missing values without lookahead data leakage.")
    ]
    for title, desc in points4:
        p = tf4.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(14)
    fig_f1 = os.path.join(FIG_DIR, "eda_case_timeline.png")
    if os.path.exists(fig_f1):
        s4.shapes.add_picture(fig_f1, Inches(6.9), Inches(1.8), Inches(5.8))

    # SLIDE 5: EXPLORATORY DATA ANALYSIS & SEASONALITY
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Exploratory Data Analysis: Annual Transmission Seasonality")
    fig_f2 = os.path.join(FIG_DIR, "eda_seasonal_cycle.png")
    if os.path.exists(fig_f2):
        s5.shapes.add_picture(fig_f2, Inches(0.8), Inches(1.8), Inches(6.2))
    tb5 = s5.shapes.add_textbox(Inches(7.2), Inches(1.8), Inches(5.3), Inches(5.0))
    tf5 = tb5.text_frame
    tf5.word_wrap = True
    points5 = [
        ("High Transmission Window:", "Dengue cases consistently concentrate between Weeks 34 and 46 (late August to November), peaking at an average of ~65 cases/week."),
        ("Dry Season Baselines:", "Cases hit minimal troughs during late spring (Weeks 10 to 18, March–May), hovering around 10–15 cases/week."),
        ("Mathematical Encoding:", "Annual seasonality was encoded using cyclical sine and cosine coordinates, ensuring smooth circular transition between Week 52 and Week 1.")
    ]
    for title, desc in points5:
        p = tf5.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(14)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(16)

    # SLIDE 6: EMPIRICAL PROOF OF LAGGED WEATHER
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Empirical Validation: Lagged Cross-Correlation")
    fig_f4 = os.path.join(FIG_DIR, "eda_lagged_cross_correlation.png")
    if os.path.exists(fig_f4):
        s6.shapes.add_picture(fig_f4, Inches(0.8), Inches(1.8), Inches(6.2))
    tb6 = s6.shapes.add_textbox(Inches(7.2), Inches(1.8), Inches(5.3), Inches(5.0))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    points6 = [
        ("The Empirical Breakthrough:", "Pearson correlation between dengue cases and weather does NOT peak at Lag 0 (concurrent weather)."),
        ("2-to-8 Week Peak:", "Correlation with Specific Humidity and Night Minimum Temperature steadily increases with backward lag, peaking at delays of 3 to 6 weeks!"),
        ("Scientific Confirmation:", "This mathematically confirms our biological hypothesis: lagged weather features carry superior predictive signals compared to unlagged readings.")
    ]
    for title, desc in points6:
        p = tf6.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(14)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(16)

    # SLIDE 7: FEATURE ENGINEERING PIPELINE
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Systematic Feature Engineering Architecture")
    tb7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.2))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    feats = [
        ("1. Autoregressive Disease Momentum:", "Cases at t-1, t-2, t-3, t-4, and t-8 representing active human virus carriers."),
        ("2. Moving Window Trends:", "4-week and 8-week moving averages, standard deviation, and short-term acceleration velocity (trend_4)."),
        ("3. Cyclical Calendar Encodings:", "sin(2*pi*week/52) and cos(2*pi*week/52) preventing artificial integer boundary jumps."),
        ("4. Biologically Lagged Weather:", "Specific humidity, dew point, minimum temperature, and rainfall lagged at t-1, t-2, t-3, t-4, t-6, and t-8 weeks."),
        ("5. Cumulative Ecological Drivers:", "4-week rolling precipitation (standing water breeding pools) and sustained humidity."),
        ("Total Feature Matrix:", "61 high-dimensional engineered features with 0 missing values across 924 dense training weeks.")
    ]
    for title, desc in feats:
        p = tf7.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(10)

    # SLIDE 8: CHRONOLOGICAL DATA SPLIT
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Out-of-Time Chronological Train-Test Split")
    tb8 = s8.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    splits = [
        ("Zero Shuffling (Mandatory):", "Standard random k-fold shuffling leaks future data into the training set, causing artificial memorization. In temporal forecasting, chronological splitting is mandatory."),
        ("Historical Training Partition (80%):", "June 1990 to September 2004 (739 consecutive weeks, ~14.2 years). Captures long-term climate cycles and historic epidemic peaks."),
        ("Holdout Evaluation Partition (20%):", "September 2004 to March 2008 (185 consecutive weeks, ~3.6 years). Completely untouched during feature extraction and training."),
        ("Direct Multi-Horizon Modeling:", "Trained 4 independent estimators (h=1, 2, 3, 4) to eliminate compounding error across multi-step lead times.")
    ]
    for title, desc in splits:
        p = tf8.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(14)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(16)

    # SLIDE 9: MODEL BENCHMARKING RESULTS
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Experimental Benchmarking Across Lead Times")
    fig_f5 = os.path.join(FIG_DIR, "forecast_vs_actual_h1_to_h4.png")
    if os.path.exists(fig_f5):
        s9.shapes.add_picture(fig_f5, Inches(0.8), Inches(1.8), Inches(6.4))
    tb9 = s9.shapes.add_textbox(Inches(7.4), Inches(1.8), Inches(5.1), Inches(5.0))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    bench_pts = [
        ("Winning Architecture: XGBoost", "Achieved the lowest overall average MAE across all four horizons (10.54 cases/week)."),
        ("Horizon 2 Superiority:", "At 2 weeks ahead, XGBoost achieved an RMSE of 14.22 (beating baseline 15.18) and R² of 0.7942 (beating baseline 0.7653)."),
        ("Random Forest & LightGBM:", "Provided robust competitive performance but exhibited slight over-smoothing on extreme outbreak peaks.")
    ]
    for title, desc in bench_pts:
        p = tf9.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(14)

    # SLIDE 10: FEATURE ABLATION STUDY
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Feature Ablation Study: Validating Weather Signals")
    fig_abl = os.path.join(FIG_DIR, "ablation_comparison_mae.png")
    if os.path.exists(fig_abl):
        s10.shapes.add_picture(fig_abl, Inches(0.8), Inches(1.8), Inches(6.4))
    tb10 = s10.shapes.add_textbox(Inches(7.4), Inches(1.8), Inches(5.1), Inches(5.0))
    tf10 = tb10.text_frame
    tf10.word_wrap = True
    abl_pts = [
        ("The Research Question:", "Does weather improve forecasting over previous case counts alone?"),
        ("Controlled 5-Stage Progression:", "E1 (Cases Only) -> E2 (+ Lags/Rolling) -> E3 (+ Seasonal) -> E4 (+ Current Weather) -> E5 (+ Lagged Weather)."),
        ("The Empirical Verdict:", "E5 (Full Lagged Weather) achieved the lowest Average RMSE (12.83) and highest Average R² (0.8304) among all experiments!"),
        ("Horizon 2 Impact:", "Lagged weather reduced Horizon 2 RMSE from 15.12 to 14.22, proving that delayed climate features protect against peak outbreak misses.")
    ]
    for title, desc in abl_pts:
        p = tf10.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(12)

    # SLIDE 11: SHAP EXPLAINABILITY - GLOBAL BEESWARM
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Explainable AI: Global SHAP Feature Importances")
    fig_shap1 = os.path.join(FIG_DIR, "shap_summary_beeswarm.png")
    if os.path.exists(fig_shap1):
        s11.shapes.add_picture(fig_shap1, Inches(0.8), Inches(1.8), Inches(6.0))
    tb11 = s11.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(5.0))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    shap1_pts = [
        ("Cooperative Game Theory:", "SHAP assigns a fair additive payout to every feature, satisfying local accuracy and consistency."),
        ("Directional Impact (Color):", "Red dots represent high feature values; blue represents low values. X-axis shows impact on predicted cases."),
        ("Key Environmental Drivers:", "High specific humidity (lag 3) and elevated minimum temperatures (lag 4) consistently exert positive SHAP values, driving case predictions higher."),
        ("Clinical Trust:", "Transforms an opaque ML model into a biologically transparent early warning tool for healthcare officials.")
    ]
    for title, desc in shap1_pts:
        p = tf11.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(14)

    # SLIDE 12: SHAP EXPLAINABILITY - LOCAL OUTBREAK WATERFALL
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Explainable AI: Explaining Epidemic Spikes Locally")
    fig_shap2 = os.path.join(FIG_DIR, "shap_outbreak_waterfall.png")
    if os.path.exists(fig_shap2):
        s12.shapes.add_picture(fig_shap2, Inches(0.8), Inches(1.8), Inches(6.0))
    tb12 = s12.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.5), Inches(5.0))
    tf12 = tb12.text_frame
    tf12.word_wrap = True
    shap2_pts = [
        ("Local Outbreak Decomposition:", "Explains Week 39 of 2007 (actual cases: 170)."),
        ("Baseline to Prediction:", "Shows how the baseline expected value (~30 cases) was pushed upward by each specific environmental factor:"),
        ("Step-by-Step Drivers:", "\n  1. Active disease momentum (cases_lag1 = 120 -> +75 cases)\n  2. Favorable annual seasonality (sin_week -> +10 cases)\n  3. Elevated specific humidity 3 weeks prior (+8 cases)\n  4. Warm night-time temperatures 4 weeks prior (+5 cases)"),
        ("Final Output:", "Sum of SHAP contributions accurately reaches predicted caseload (155 cases).")
    ]
    for title, desc in shap2_pts:
        p = tf12.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(12)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(12)

    # SLIDE 13: LIMITATIONS & FUTURE SCOPE
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Academic Limitations & Future Research Directions")
    tb13 = s13.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf13 = tb13.text_frame
    tf13.word_wrap = True
    limits = [
        ("Lack of Entomological Trap Data:", "The public dataset lacks direct mosquito larval indices (Breteau index) or adult trap counts. The model relies on meteorological proxies for mosquito abundance."),
        ("Dengue Serotype Dynamics (DENV 1–4):", "Prior infection with one serotype creates partial immunity but increases susceptibility to severe dengue via Antibody-Dependent Enhancement (ADE). Circulating serotype proportions were unavailable."),
        ("Future Scope 1: Spatio-Temporal Graph Networks:", "Extend the architecture to multi-city Graph Neural Networks (GNNs) capturing inter-regional human mobility across Puerto Rico and Latin America."),
        ("Future Scope 2: Satellite Radar Remote Sensing:", "Integrate Synthetic Aperture Radar (SAR) imagery to directly detect standing water pooling in urban drainage basins.")
    ]
    for title, desc in limits:
        p = tf13.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(14)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(14)

    # SLIDE 14: CONCLUSION & SUMMARY
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Conclusion & Project Summary")
    tb14 = s14.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf14 = tb14.text_frame
    tf14.word_wrap = True
    concls = [
        ("Fully Operational Multi-Horizon Pipeline:", "Successfully built and benchmarked a 1-to-4 week ahead forecasting system on 18 years of San Juan epidemiological data."),
        ("Rigorous Scientific Methodology:", "Implemented causal forward-fill imputation, biological lag feature engineering, and strict chronological out-of-time train-test partitioning."),
        ("Empirical Confirmation of Weather Value:", "The 5-stage feature ablation study demonstrated that incorporating lagged weather in E5 yields the lowest Average RMSE (12.83) and highest Average R² (0.8304)."),
        ("XGBoost Superiority:", "XGBoost delivered the lowest overall average MAE (10.54 cases/week) and demonstrated superior resilience during sudden epidemic outbreaks."),
        ("Transparent Clinical Explainability:", "TreeSHAP unmasked model reasoning, proving that specific humidity and minimum temperature at 3 to 4 week delays are the primary environmental drivers.")
    ]
    for title, desc in concls:
        p = tf14.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {title} "
        run1.font.bold = True
        run1.font.size = Pt(14)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = DARK_GRAY
        p.space_after = Pt(12)

    # SLIDE 15: THANK YOU & Q&A
    s15 = prs.slides.add_slide(blank_layout)
    bg15 = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg15.fill.solid()
    bg15.fill.fore_color.rgb = NAVY
    bg15.line.color.rgb = NAVY
    
    t_box15 = s15.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.3), Inches(3.5))
    tf15 = t_box15.text_frame
    tf15.word_wrap = True
    
    p = tf15.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "THANK YOU!"
    p.font.name = 'Arial'
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(16)
    
    p2 = tf15.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Questions & Answers Welcome"
    p2.font.name = 'Calibri'
    p2.font.size = Pt(22)
    p2.font.color.rgb = RGBColor(160, 200, 240)
    p2.space_after = Pt(28)
    
    p3 = tf15.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "Complete Source Code, Models, Documentation & Report Ready for Submission"
    p3.font.name = 'Calibri'
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(220, 220, 220)

    output_pptx = os.path.join(PROJECT_ROOT, "Dengue_Forecasting_Presentation.pptx")
    prs.save(output_pptx)
    print(f"Presentation generated successfully: {output_pptx} ({os.path.getsize(output_pptx):,} bytes)")


if __name__ == '__main__':
    build_presentation()
