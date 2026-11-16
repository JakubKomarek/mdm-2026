"""Cesky 'Index nezbytnosti' po vzoru United For ALICE Essentials Index.
Vahy = kos MDM 2025 (bez uspor). Ceny = index spotrebitelskych cen CSU (CPI, COICOP 2018),
otevrena data CEN0101E, bazicky index 2025=100, domacnosti celkem, Cesko.
Rocni prumery 2015-2025; rok 2026 = prumer dostupnych mesicu 2026 vs stejne mesice 2025."""
import csv, json, collections
COD = lambda r: r["CZCOICOP2.CZCOP23"] or r["CZCOICOP2.CZCOP1"]
m = collections.defaultdict(dict)
for r in csv.DictReader(open("cpi_cz.csv", encoding="utf-8-sig")):
    t = r["CASMKMQRM12"]
    if r["TYPUDAJE4A"] == "IZ2025" and r["UZ02P"] == "CZ" and r["EKAKTIOCDS"] == "0" and len(t) == 7:
        m[COD(r)][t] = float(r["Hodnota"])
W = {"041": 15342*.6, "045": 15342*.4*.85, "044": 15342*.4*.15, "01": 8286,
     "03": 1247, "07": 2208, "06": 1730, "08": 1378, "09": 4030}
tot = sum(W.values()); W = {k: v/tot for k, v in W.items()}
Z = ["041", "045", "044", "01", "07"]   # zakladni nezbytnosti
zt = sum(W[k] for k in Z)
CODES = list(W) + ["0", "0722", "10"]
mon26 = sorted(t[5:] for t in m["0"] if t.startswith("2026") and t[5:].isdigit())
def avg(k, y, months=None):
    v = [m[k][f"{y}-{mm:02d}"] for mm in range(1, 13) if f"{y}-{mm:02d}" in m[k] and (months is None or f"{mm:02d}" in months)]
    return sum(v)/len(v)
A = {k: {y: avg(k, y) for y in range(2015, 2026)} for k in CODES}
for k in CODES:  # 2026: rust leden-posledni mesic vs stejne mesice 2025
    A[k][2026] = A[k][2025] * avg(k, 2026) / avg(k, 2025, mon26)
b = 2015; Y = sorted(A["0"])
I = lambda k, y: 100*A[k][y]/A[k][b]
rows = [{"rok": y, "essentials": round(sum(W[k]*I(k, y) for k in W), 1),
         "zaklad": round(sum(W[k]*I(k, y) for k in Z)/zt, 1), "cpi": round(I("0", y), 1)} for y in Y]
n = 2025 - b
g = lambda a, c: round(100*((a/c)**(1/n)-1), 2)
r25 = next(r for r in rows if r["rok"] == 2025)
out = {"zdroj": "CSU CEN0101E (CPI, COICOP 2018)", "zaklad_rok": b, "mesice_2026": f"01-{mon26[-1]}",
       "rady": rows, "vahy_pct": {k: round(100*v, 1) for k, v in W.items()},
       "rocne_2015_2025": {"essentials": g(r25["essentials"], 100), "zaklad": g(r25["zaklad"], 100), "cpi": g(r25["cpi"], 100)},
       "slozky_kumul_2015_2025": {k: round(I(k, 2025)-100, 1) for k in CODES},
       "zmena_2026_pct": {k: round(100*(A[k][2026]/A[k][2025]-1), 1) for k in CODES}}
json.dump(out, open("essentials.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "rady"}, ensure_ascii=False, indent=1)); print(rows[-3:])
