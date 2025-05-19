
from concurrent.futures import ThreadPoolExecutor
from itertools import (
        repeat,
        zip_longest
)

from pandas import DataFrame
from pyodbc import connect
from tqdm import tqdm

from ..utils.logger_config import SLOG


def insert_df(df : DataFrame, cs : str, tb : str, th : int = 0) -> None:
    """Insert DataFrame (df) rows into a table (tb) in DB, opening a connection with
    it via a connection string (cs), multithreading, unless is specified to not thread
    it (th = 1).

    :param df : DataFrame to be inserted
    :param cs : Connection string to be used when connecting to DB
    :param tb : Table from DB to be inserted 
    :param th : Number of threads to be used
    """
    
    n_rows = df.shape[0]
    n_columns = df.shape[1]
    columns = ", ".join(df.columns.values)
    values = ", ".join(repeat("?", n_columns))
    SLOG.debug(f"DATAFRAME\n\tROWS : {n_rows}\n\tCOLUMNS : {columns}\n\tVALUES : {values}")

    query = f"INSERT INTO {tb} ({columns}) VALUES ({values})"
    SLOG.debug(f"Query : {query}")

    rows = df.itertuples(index=False, name=tb)
    SLOG.debug(f"ITERTUPLES :\n\t{rows}")

    con = connect(cs)
    SLOG.debug(f"Connection established with {con}")

    iter = zip_longest(repeat(con, n_rows), rows)
    SLOG.debug(f"Zipped iterator with connection objects and row values")

    def init_cursor(iter):
        SLOG.debug(f"init function args: {iter}")
        cursor = iter[0].cursor()
        return cursor.execute(query, iter[1])

    if th < 1:
        try:
            with ThreadPoolExecutor() as executor:
                list(tqdm(executor.map(init_cursor, iter), total=n_rows, desc=f"Inserting rows into table {tb}: "))
        except Exception as e:
            SLOG.exception(f"\n=============================================\n{e}\n=============================================\n")
        else:
            con.commit()
            SLOG.debug(f"Rows commited into table {tb}")
        finally:
            con.close()
            SLOG.debug(f"Connection closed")


def insert_dtabular(b : dict, cs : str, tb : str, th : int = 0) -> None:
    """Insert rows from a tabular dictionary buffer (b) into a DB, opening a connection
    with it via a connection string (cs), multithreading, unless is specified to not 
    thread it (threads = 1).

    :param b : Buffer with data to be inserted
    :param cs : Connection string to be used when connecting to DB
    :param tb : Table from DB to be inserted 
    :param th : Number of threads to be used
    """

    columns = ", ".join(list(b.keys()))
    n_columns = len(b.keys())
    n_rows = len(list(b.values())[0])
    values = ", ".join(repeat("?", n_columns))
    SLOG.debug(f"DATAFRAME\n\tROWS : {n_rows}\n\tCOLUMNS : {columns}\n\tVALUES : {values}")

    query = f"INSERT INTO {tb} ({columns}) VALUES ({values})"
    SLOG.debug(f"Query : {query}")

    rows = []

    for i in range(n_rows):
        row = []
        for k in b.keys():
            row.append(b[k][i])

        rows.append(tuple(row))
    SLOG.debug(f"ROWS :\n\t{rows}")

    con = connect(cs)
    SLOG.debug(f"Connection established with {con}")

    iter = zip_longest(repeat(con, n_rows), rows)
    SLOG.debug(f"Zipped iterator with connection objects and row values")

    def init_cursor(iter):
        SLOG.debug(f"init function args: {iter}")
        cursor = iter[0].cursor()
        return cursor.execute(query, iter[1])

    if th < 1:
        try:
            with ThreadPoolExecutor() as executor:
                list(tqdm(executor.map(init_cursor, iter), total=n_rows, desc=f"Inserting rows into table {tb}: "))
        except Exception as e:
            SLOG.exception(f"\n=============================================\n{e}\n=============================================\n")
        else:
            con.commit()
            SLOG.debug(f"Rows commited into table {tb}")
        finally:
            con.close()
            SLOG.debug(f"Connection closed")


if __name__ == "__main__":
    buffer = {
        "c1" : [1, 2, 3, 4],
        "c2" : ["um", "dois", "tres", "quatro"],
        "c3" : ["algumtrem", "outrotrem", "maisalgumtrem", "maisoutrotrem"]
    }

    df = DataFrame(buffer)

    connection_string = "DRIVER={Sqlite3 ODBC Driver};DATABASE=C:/Users/Sakamoto/trampo/nibo/test.db"

    con = connect(connection_string)
    insert_dtabular(buffer, connection_string, "tabela")
