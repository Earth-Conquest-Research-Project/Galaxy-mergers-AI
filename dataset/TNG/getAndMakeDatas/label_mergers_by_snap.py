import os
import h5py
import numpy as np
import pandas as pd

# 분석할 snapshot 리스트
target_snapshots = list(range(1, 100))
snapshot_tolerance = 10   # ±0.5 Gyr ≈ 10 snapshots
nonmerger_margin = 60     # ±3 Gyr ≈ 60 snapshots
max_per_class = 4000      # 클래스별 최대 저장 수

data_dir = './dataset/TNG/mergerHistoryData'
file_list = sorted([f for f in os.listdir(data_dir) if f.endswith('.hdf5')])

print(f"총 파일 수: {len(file_list)}")
print("첫 5개 파일 이름:", file_list[:5])

records = []

for current_snapshot in target_snapshots:
    print(f"\n🌀 Processing snapshot {current_snapshot}...")

    merger_labels = []
    nonmerger_labels = []

    for fname in file_list:
        path = os.path.join(data_dir, fname)
        try:
            with h5py.File(path, 'r') as f:
                print(f"  🔍 파일: {fname}")
                print("   └ keys:", list(f.keys()))

                # 구조 확인
                if 'SnapNumLastMerger' not in f or 'SubhaloID' not in f:
                    print("   ❌ 필요한 키 없음: SnapNumLastMerger 또는 SubhaloID")
                    continue

                snap_last_merger = f['SnapNumLastMerger'][:]
                galaxy_ids = f['SubhaloID'][:]

                print(f"   ✅ SnapNumLastMerger shape: {snap_last_merger.shape}")
                print(f"   ✅ SubhaloID shape: {galaxy_ids.shape}")

                # 병합 조건
                is_merger = (snap_last_merger >= 0) & (np.abs(current_snapshot - snap_last_merger) <= snapshot_tolerance)
                is_nonmerger = ((snap_last_merger == -1) | (np.abs(current_snapshot - snap_last_merger) > nonmerger_margin))

                merger_idx = np.where(is_merger)[0]
                nonmerger_idx = np.where(is_nonmerger)[0]

                print(f"   📈 merger 조건 만족: {len(merger_idx)}개")
                print(f"   📉 non-merger 조건 만족: {len(nonmerger_idx)}개")

                # merger 기록
                for i in merger_idx:
                    if len(merger_labels) >= max_per_class:
                        break
                    merger_labels.append((int(galaxy_ids[i]), current_snapshot, 1))

                # non-merger 기록
                for i in nonmerger_idx:
                    if len(nonmerger_labels) >= max_per_class:
                        break
                    nonmerger_labels.append((int(galaxy_ids[i]), current_snapshot, 0))

                # 조기 종료 조건
                if len(merger_labels) >= max_per_class and len(nonmerger_labels) >= max_per_class:
                    print(f"   ⏹ Reached max limit for snapshot {current_snapshot}")
                    break

        except Exception as e:
            print(f"   ⚠️ 파일 오류 발생: {fname} - {e}")
            continue

    # 병합
    snapshot_records = merger_labels + nonmerger_labels
    print(f"✅ Snapshot {current_snapshot}: Merger={len(merger_labels)}, Non-merger={len(nonmerger_labels)}")
    records.extend(snapshot_records)

# DataFrame 저장
df = pd.DataFrame(records, columns=['GalaxyID', 'Snapshot', 'Label'])
output_path = './dataset/TNG/merger_labels_selected_snapshots.csv'
df.to_csv(output_path, index=False)
print(f'\n🧾 Total labeled galaxies: {len(df)}')
print(f'📂 Saved to: {output_path}')