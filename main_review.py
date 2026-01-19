from g1.g1_main import run_g1
from g3.g3_main import run_g3
from g4.g4_main import run_g4
from g5.g5_main import run_g5


def main():
    print("====================================")
    print("Starting Review Integration Pipeline")
    print("====================================")

    print("\n>>> G1 review started")
    run_g1()
    print("<<< G1 review completed")

    print("\n>>> G3 review started")
    run_g3()
    print("<<< G3 review completed")

    print("\n>>> G4 review started")
    run_g4()
    print("<<< G4 review completed")

    print("\n>>> G5 review started")
    run_g5()
    print("<<< G5 review completed")

    print("\n====================================")
    print("Pipeline completed successfully")
    print("====================================")


if __name__ == "__main__":
    main()
