# Logs structure

TO-DO: Organize all the logs and this read me

Each folder name is standardized as follows:

{Run_type}_{Total_rounds}

- Run_type:

    _Fixed_: The order of operations is fixed (One sequence)

    _Random_: The order of operations is randomized (Fuzzed sequences)

- Total_rounds:

    Number of fuzzing rounds of the parameters

New standard

{Run_type}_{Sequence_or_Single_Op}__{Oracles_no}_{Rounds}

- Run_type:

    _Fixed_: The parameters are fixed

    _Fuzzed_: The parameters are fuzzed

- Sequence_or_Single_Op

    _Seq_: Sequence of operations are run

    _One_: Single operation is run

- Oracle_no

    Number of oracles (Either 1 or 3)

- Rounds

    Number of rounds
