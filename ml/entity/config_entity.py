from dataclasses import dataclass


@dataclass
class DataIngestionConfig:

    data_path: str

    feature_store_path: str

    train_path: str

    test_path: str

    train_test_split_ratio: float = 0.2