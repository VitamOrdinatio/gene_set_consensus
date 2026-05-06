from abc import ABC, abstractmethod
import pandas as pd

class SourceAdapter(ABC):

    @abstractmethod
    def load(self, path):
        pass

    @abstractmethod
    def validate(self, df):
        pass

    @abstractmethod
    def transform(self, df):
        pass

    def run(self, path):

        df = self.load(path)

        self.validate(df)

        transformed = self.transform(df)

        if not isinstance(transformed, pd.DataFrame):
            raise TypeError(
                "Adapter transform() must return a pandas DataFrame"
            )

        return transformed
