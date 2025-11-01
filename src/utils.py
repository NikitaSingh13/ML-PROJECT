# here the code is written(common functionality) that'll be used in the entire project
# for example like code for cloud uploading, database connection

import os
import sys
import dill # help us create the pickle file

import numpy as np
import pandas as pd

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exceptiona as e:
        raise CustomException(e, sys)