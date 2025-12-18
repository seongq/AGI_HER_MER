import subprocess
import random

# 설정
devmode = "siljunmode"
folders = ["01", "02", "03", "04", "05"]
normalizations = ["true", "false"]
num_trials_per_setting = 10  # 각 조합별 몇 번 반복할지

# 실행 목록 생성
execution_list = []
for folder in folders:
    for normalization in normalizations:
        for _ in range(num_trials_per_setting):
            seed = random.randint(1, 100000)
            execution_list.append({
                "folder": folder,
                "normalization": normalization,
                "seed": seed
            })

# 🔀 실행 순서를 무작위로 섞음
random.shuffle(execution_list)

# 🚀 실행
for config in execution_list:
    command = [
        "python", "train_test.py",
        "--MKD", "True",
        "--MKD_modals", "tva",
        "--MKD_student_modals", "tva",
        "--MULTITASK_MKD", "tva",
        "--devmode", devmode,
        "--seed", str(config["seed"]),
        "--folder", config["folder"],
        "--normalization", config["normalization"]
    ]
    print("🔹 Running:", " ".join(command))
    subprocess.run(command)
