import subprocess
import sys


def run(cmd):
    result = subprocess.run(cmd, shell=True)
    return result.returncode


def detect_conflict():
    result = subprocess.run(
        "git diff --name-only --diff-filter=U",
        shell=True,
        capture_output=True,
        text=True
    )

    files = result.stdout.strip().split("\n")
    return [f for f in files if f]


def auto_fix(files, strategy="ours"):

    for f in files:
        if strategy == "ours":
            subprocess.run(f"git checkout --ours {f}", shell=True)
        else:
            subprocess.run(f"git checkout --theirs {f}", shell=True)

        subprocess.run(f"git add {f}", shell=True)


def commit_fix():

    subprocess.run(
        'git commit -m "Auto fixed merge conflict"',
        shell=True
    )


def main():

    files = detect_conflict()

    if not files:
        print("No merge conflicts found")
        sys.exit(0)

    print("Conflicts found in:", files)

    auto_fix(files, "ours")

    commit_fix()

    print("Conflicts auto resolved")


if __name__ == "__main__":
    main()