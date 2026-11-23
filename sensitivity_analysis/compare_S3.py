"""
S3 post-run comparison — CANDIDATE implementation (S3 protocol v1.0). NOT AUTHORISED TO RUN on S3 outputs.

Reads only: frozen canonical S0 OOF, frozen S2 OOF/metrics, and (after authorised execution) results_sensitivity_S3/.
Writes only into results_sensitivity_S3/comparison/ (no-overwrite). Fits no model, generates no prediction.

Implements:
  E1  controls/S0 OOF vs canonical S0 OOF            max |diff| <= 1e-9
  E2  controls/S2 OOF + metrics vs frozen S2          max |diff| <= 1e-9
  E3  S3 Cr OOF vs frozen S2 Cr OOF (D4)              max |diff| <= 1e-9
  6.1 18-row table S0 / S2 / S3, delta S3-S2 (primary) and S3-S0 (secondary)
  5   paired-null skill per population and geometry
  6.2 matched-record decomposition (evaluation-set vs retraining effect)
  D3  frozen materiality rules (materiality_row / materiality_geometry)
  D5  descriptive S2 OOF errors on the 11 B2 records (frozen S2 OOF only; no training)
"""
import os, sys, numpy as np, pandas as pd

TOL = 1e-9  # approved; must not be changed
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PKG_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
REPO = os.path.abspath(os.path.join(PKG_ROOT, '../..'))
B = os.path.join(REPO, 'phase3', 'model_development', 'domain_B_carbon')
CAN = {'Cr': os.path.join(B, 'results', 'CARB_CR_CANDIDATE_OOF_PREDICTIONS.csv'), 'Pb': os.path.join(B, 'results', 'CARB_PB_CANDIDATE_OOF_PREDICTIONS.csv')}
S2D = os.path.join(B, 'results_sensitivity_S2')
S3D = os.path.join(B, 'results_sensitivity_S3')
Y = 'Kinetic_Capacity_qt_mg_g'
B2_IDS = [27, 31, 86, 87, 88, 89, 258, 271, 770, 776, 781]
PAIRED_NULL = {'Cr(VI)': 'CARB_BASE_01_Cr_LOSO', 'Grouped': 'CARB_BASE_01_Pb_AlignedGrouped', 'LOSO15': 'CARB_BASE_01_Pb_LOSO15'}

# ---------------- D3: frozen materiality thresholds (S3_PROTOCOL_APPROVAL_RECEIPT.md section 3) ----------------
D3_DR2 = 0.05          # |delta R2_OOD| >= 0.05
D3_DSKILL_PTS = 5.0    # change in paired-null MAE reduction >= 5 percentage points
D3_DMAE_FRAC = 0.10    # |delta MAE| >= 10 % of S2 MAE

def materiality_row(r2_s2, r2_s3, skill_s2, skill_s3, mae_s2, mae_s3):
    """Return (label, triggered_criteria) for one model row, S3 vs S2, same geometry."""
    crit = []
    if abs(r2_s3 - r2_s2) >= D3_DR2: crit.append('dR2')
    if abs(skill_s3 - skill_s2) >= D3_DSKILL_PTS: crit.append('dSkill')
    if abs(mae_s3 - mae_s2) >= D3_DMAE_FRAC * mae_s2: crit.append('dMAE')
    return ('MATERIALLY_CHANGED' if crit else 'ESSENTIALLY_UNCHANGED'), crit

def materiality_geometry(mae_s2: dict, mae_s3: dict, skill_s2: dict, skill_s3: dict):
    """Geometry conclusion: best model by pooled MAE changes, or any paired-null skill changes sign."""
    best2, best3 = min(mae_s2, key=mae_s2.get), min(mae_s3, key=mae_s3.get)
    sign_flip = [m for m in skill_s2 if np.sign(skill_s2[m]) != np.sign(skill_s3[m])]
    changed = best2 != best3 or bool(sign_flip)
    return ('MATERIALLY_CHANGED' if changed else 'ESSENTIALLY_UNCHANGED'), dict(best_S2=best2, best_S3=best3, skill_sign_flips=sign_flip)

def skill(metric_model, metric_null):
    return 100.0 * (1.0 - metric_model / metric_null)

def geometry_of(model_id, analyte):
    if analyte == 'Cr(VI)': return 'Cr(VI)'
    return 'LOSO15' if model_id.endswith('_LOSO15') else 'Grouped'

# ---------------- reproduction controls ----------------
def max_abs_diff(a, b, key='Record_ID'):
    a = a.sort_values(key).reset_index(drop=True); b = b.sort_values(key).reset_index(drop=True)
    assert (a[key].values == b[key].values).all(), 'record sets differ'
    cols = [c for c in a.columns if c in b.columns and (c.startswith('Pred') or c.startswith('Null') or c == 'Cr_Pred_Median_Baseline')]
    assert cols, 'no comparable prediction columns'
    return max(float(np.abs(a[c] - b[c]).max()) for c in cols), cols

def controls():
    res = {}
    for an in ('Cr', 'Pb'):
        d, _ = max_abs_diff(pd.read_csv(CAN[an]), pd.read_csv(os.path.join(S3D, 'controls', 'S0', f'S0_{an.upper()}_OOF_PREDICTIONS.csv')))
        res[f'E1_{an}'] = d
        d, _ = max_abs_diff(pd.read_csv(os.path.join(S2D, 'S2', f'S2_{an.upper()}_OOF_PREDICTIONS.csv')),
                            pd.read_csv(os.path.join(S3D, 'controls', 'S2', f'S2_{an.upper()}_OOF_PREDICTIONS.csv')))
        res[f'E2_{an}'] = d
    m2 = pd.read_csv(os.path.join(S2D, 'S2', 'S2_METRICS_18_ROWS.csv')); m2c = pd.read_csv(os.path.join(S3D, 'controls', 'S2', 'S2_METRICS_18_ROWS.csv'))
    num = ['Pooled_MAE', 'Pooled_RMSE', 'Pooled_R2_OOD', 'Pooled_MedAE', 'Mean_Fold_MAE', 'Mean_Fold_RMSE']
    res['E2_metrics'] = float(np.abs(m2[num].values - m2c[num].values).max())
    d, _ = max_abs_diff(pd.read_csv(os.path.join(S2D, 'S2', 'S2_CR_OOF_PREDICTIONS.csv')), pd.read_csv(os.path.join(S3D, 'S3', 'S3_CR_OOF_PREDICTIONS.csv')))
    res['E3_Cr_S3_vs_S2'] = d
    res['ALL_PASS'] = all(v <= TOL for k, v in res.items() if k != 'ALL_PASS')
    return res

# ---------------- D5: descriptive B2 errors from frozen S2 OOF only ----------------
def d5_table():
    pb = pd.read_csv(os.path.join(S2D, 'S2', 'S2_PB_OOF_PREDICTIONS.csv'))
    pcols = [c for c in pb.columns if c.startswith('Pred_Pb_')]
    rows = []
    for c in pcols:
        err = (pb[c] - pb[Y]).abs()
        for rid in B2_IDS:
            r = pb[pb.Record_ID == rid].iloc[0]
            same = pb[(pb.Literature_Reference == r.Literature_Reference) & ~pb.Record_ID.isin(B2_IDS)]
            rows.append(dict(Record_ID=rid, Study=r.Literature_Reference, Fold=int(r.Study_Grouped_Fold), Prediction_Column=c,
                             Observed=r[Y], Predicted_S2=r[c], AbsError_S2=abs(r[c] - r[Y]),
                             Study_nonB2_MAE_S2=float(err[same.index].mean()), Study_nonB2_N=len(same)))
    return pd.DataFrame(rows)

def main():
    assert os.path.isdir(os.path.join(S3D, 'S3')), 'S3 outputs absent: execution has not been authorised/run'
    out = os.path.join(S3D, 'comparison'); os.makedirs(out, exist_ok=False)
    ctl = controls(); pd.Series(ctl).to_csv(os.path.join(out, 'S3_REPRODUCTION_CONTROLS.csv'))
    if not ctl['ALL_PASS']:
        sys.exit(f'Reproduction control failure (tolerance {TOL} not met): {ctl}. Investigate; do not adjust tolerance.')
    d5_table().to_csv(os.path.join(out, 'S3_D5_B2_RECORD_ERRORS_UNDER_S2.csv'), index=False)
    # 18-row tables, skill, matched decomposition and materiality are assembled here from the three metric files
    # and the OOF files (S0 canonical, S2 frozen, S3 new), restricted to S3 records for section 6.2.
    m = {p: pd.read_csv(f) for p, f in [('S0', os.path.join(S3D, 'controls', 'S0', 'S0_METRICS_18_ROWS.csv')),
                                         ('S2', os.path.join(S2D, 'S2', 'S2_METRICS_18_ROWS.csv')),
                                         ('S3', os.path.join(S3D, 'S3', 'S3_METRICS_18_ROWS.csv'))]}
    rows = []
    for _, r in m['S3'].iterrows():
        g = geometry_of(r.Model_Identifier, r.Analyte); row = dict(Model_Identifier=r.Model_Identifier, Analyte=r.Analyte, Geometry=g)
        for p in ('S0', 'S2', 'S3'):
            x = m[p].set_index('Model_Identifier').loc[r.Model_Identifier]
            row.update({f'N_{p}': x.N, f'MAE_{p}': x.Pooled_MAE, f'RMSE_{p}': x.Pooled_RMSE, f'R2_{p}': x.Pooled_R2_OOD})
            if not r.Model_Identifier.startswith('CARB_BASE'):
                nl = m[p].set_index('Model_Identifier').loc[PAIRED_NULL[g]]
                row[f'SkillMAE_{p}'] = skill(x.Pooled_MAE, nl.Pooled_MAE); row[f'SkillRMSE_{p}'] = skill(x.Pooled_RMSE, nl.Pooled_RMSE)
        row['dMAE_S3_minus_S2'] = row['MAE_S3'] - row['MAE_S2']; row['dMAE_S3_minus_S0'] = row['MAE_S3'] - row['MAE_S0']
        if r.Analyte == 'Pb(II)' and not r.Model_Identifier.startswith('CARB_BASE'):
            row['D3_Label'], row['D3_Criteria'] = materiality_row(row['R2_S2'], row['R2_S3'], row['SkillMAE_S2'], row['SkillMAE_S3'], row['MAE_S2'], row['MAE_S3'])
        rows.append(row)
    t = pd.DataFrame(rows); t.to_csv(os.path.join(out, 'S3_COMPARISON_18_ROWS.csv'), index=False)
    # D3 geometry-level conclusions (Pb only)
    geo = []
    for g in ('Grouped', 'LOSO15'):
        x = t[(t.Geometry == g) & ~t.Model_Identifier.str.startswith('CARB_BASE')].set_index('Model_Identifier')
        lab, info = materiality_geometry(x.MAE_S2.to_dict(), x.MAE_S3.to_dict(), x.SkillMAE_S2.to_dict(), x.SkillMAE_S3.to_dict())
        geo.append(dict(Geometry=g, D3_Geometry_Label=lab, **info))
    pd.DataFrame(geo).to_csv(os.path.join(out, 'S3_D3_GEOMETRY_CONCLUSIONS.csv'), index=False)
    matched_decomposition(m).to_csv(os.path.join(out, 'S3_MATCHED_DECOMPOSITION.csv'), index=False)

def matched_decomposition(m):
    """Section 6.2: on S3 records only, split delta into evaluation-set and retraining effects (MAE, RMSE, R2)."""
    from sklearn.metrics import r2_score
    oof = {('S0', 'Cr'): CAN['Cr'], ('S0', 'Pb'): CAN['Pb'],
           ('S2', 'Cr'): os.path.join(S2D, 'S2', 'S2_CR_OOF_PREDICTIONS.csv'), ('S2', 'Pb'): os.path.join(S2D, 'S2', 'S2_PB_OOF_PREDICTIONS.csv'),
           ('S3', 'Cr'): os.path.join(S3D, 'S3', 'S3_CR_OOF_PREDICTIONS.csv'), ('S3', 'Pb'): os.path.join(S3D, 'S3', 'S3_PB_OOF_PREDICTIONS.csv')}
    f = lambda y, p: dict(MAE=float(np.mean(np.abs(y - p))), RMSE=float(np.sqrt(np.mean((y - p) ** 2))), R2=float(r2_score(y, p)))
    rows = []
    for _, r in m['S3'].iterrows():
        an = 'Cr' if r.Analyte == 'Cr(VI)' else 'Pb'
        s3 = pd.read_csv(oof[('S3', an)]); ids = set(s3.Record_ID); col = r.Prediction_Column
        for ref in ('S2', 'S0'):
            d = pd.read_csv(oof[(ref, an)])
            if col not in d.columns: continue   # canonical S0 file lacks null columns; null rows decomposed vs S2 only
            full = f(d[Y].values, d[col].values); sub = d[d.Record_ID.isin(ids)]; on = f(sub[Y].values, sub[col].values)
            new = f(s3[Y].values, s3[col].values)
            for k in ('MAE', 'RMSE', 'R2'):
                rows.append(dict(Model_Identifier=r.Model_Identifier, Analyte=r.Analyte, Reference=ref, Metric=k,
                                 Ref_full=full[k], Ref_on_S3_records=on[k], S3=new[k], Delta_total=new[k] - full[k],
                                 Evaluation_set_effect=on[k] - full[k], Retraining_effect=new[k] - on[k], N_matched=len(sub)))
    return pd.DataFrame(rows)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--authorized':
        main()
    else:
        sys.exit('Refusing: S3 comparison runs only after authorised S3 execution (--authorized).')
