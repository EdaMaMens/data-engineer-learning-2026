print("=== Week 1 Day 3: Master of 'for' Loop (Basic) ===")

# ====================================================
# 1. データの準備（リスト型：データの並び）
# ====================================================
# [ ]（角かっこ）で囲まれた、複数のデータが並んだ箱を「リスト」と呼びます [cite: 20, 389]。
target_areas = ['Tokyo', 'Kanagawa', 'Chiba', 'Saitama']

# ====================================================
# ２. 処理：forループによる自動繰り返し（データの動線）　
# ====================================================
# 💡 ここが心臓部です。
for area in target_areas:
    #インデント（字下げ）されたこの中身が、データの数（４回）だけ自動繰り返されます。
    print(f"📡 [LOOP_PROCESSING] Currently searching area: {area}")

print("\n🏆 SYS_STATUS: All loop processes completed successfully.")