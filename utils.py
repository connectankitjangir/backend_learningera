import pandas as pd
import sqlite3



def initialize_db(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS original_data (
            answer_key_link TEXT UNIQUE,
            category TEXT,
            roll_number TEXT PRIMARY KEY,
            candidate_name TEXT,
            venue_name TEXT,
            exam_date TEXT,
            exam_time TEXT,
            total_marks REAL,
            section_data TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            roll_number TEXT PRIMARY KEY,
            category TEXT,
            candidate_name TEXT,
            venue_name TEXT,
            exam_date TEXT,
            exam_time TEXT,
            total_marks REAL,
            section_data TEXT,
            overall_rank INTEGER,
            category_rank INTEGER,
            shift_average REAL,
            shift_rank INTEGER,
            category_average REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS normalized (
            roll_number TEXT PRIMARY KEY,
            category TEXT,
            normalized_marks REAL,
            shift_median REAL,
            normalized_rank INTEGER,
            normalized_category_rank INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def fetch_original_data_df(database_path):
    conn = sqlite3.connect(database_path)
    df = pd.read_sql_query('SELECT * FROM original_data', conn)
    conn.close()
    return df
def fetch_candidates_df(database_path):
    conn = sqlite3.connect(database_path)
    df = pd.read_sql_query('SELECT * FROM candidates', conn)
    conn.close()
    return df
def fetch_normalized_df(database_path):
    conn = sqlite3.connect(database_path)
    df = pd.read_sql_query('SELECT * FROM normalized', conn)
    conn.close()
    return df

def is_roll_number_exists(database_path, roll_number):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM candidates WHERE roll_number = ?', (roll_number,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def is_roll_number_exists_in_normalized_table(database_path, roll_number):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM normalized WHERE roll_number = ?', (roll_number,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def calculate_rank(df, roll_number, category):
    print('before calculate_rank')
    df['overall_rank'] = df['total_marks_for_merit_list'].rank(ascending=False, method='min')
    print('after overall_rank')
    df['category_rank'] = df.groupby('category')['total_marks_for_merit_list'].rank(ascending=False, method='min')
    print('after category_rank')
    # category_df = df[df['category'] == category].copy()
    # category_df.loc[:, 'category_rank'] = category_df['total_marks'].rank(ascending=False, method='min')
    print("df",df)

    
    overall_rank = df.loc[df['roll_number'] == roll_number, 'overall_rank'].values[0]
    print('after overall_rank')
    category_rank = df.loc[(df['roll_number'] == roll_number), 'category_rank'].values[0]
    print('after category_rank')
    
    # category_rank = category_df.loc[category_df['roll_number'] == roll_number, 'category_rank'].values[0]

    return overall_rank, category_rank
# def calculate_rank(df, roll_number, category):
#     df['overall_rank'] = df['total_marks'].rank(ascending=False, method='min')

#     df['category_rank'] = df.groupby('category')['total_marks'].rank(ascending=False, method='min')

#     # category_df = df[df['category'] == category].copy()
#     # category_df.loc[:, 'category_rank'] = category_df['total_marks'].rank(ascending=False, method='min')

#     overall_rank = df.loc[df['roll_number'] == roll_number, 'overall_rank'].values[0]
#     category_rank = df.loc[(df['roll_number'] == roll_number) & (df['category'] == category), 'category_rank'].values[0]
#     # category_rank = category_df.loc[category_df['roll_number'] == roll_number, 'category_rank'].values[0]

#     return overall_rank, category_rank

def calculate_normalized_rank(df, roll_number, category):
    print('before normalized_rank')
    df['normalized_rank'] = df['normalized_marks'].rank(ascending=False, method='min')
    print('after normalized_rank')
    df['normalized_category_rank'] = df.groupby('category')['normalized_marks'].rank(ascending=False, method='min')
    print('after normalized_category_rank')
    overall_normalized_rank = df.loc[df['roll_number'] == roll_number, 'normalized_rank'].values[0]
    print("overall_normalized_rank",overall_normalized_rank)
    normalized_category_rank = df.loc[(df['roll_number'] == roll_number) & (df['category'] == category), 'normalized_category_rank'].values[0]
    print("normalized_category_rank inside calculate_normalized_rank",normalized_category_rank)

    return overall_normalized_rank, normalized_category_rank

def calculate_shift_averages_and_ranks(df):
    df['shift'] = df['exam_date'] + ' ' + df['exam_time']
    shift_averages = df.groupby('shift')['total_marks_for_merit_list'].mean()
    df['shift_average'] = df['shift'].map(shift_averages)
    df['shift_rank'] = df.groupby('shift')['total_marks_for_merit_list'].rank(ascending=False, method='min')
    shift_ranks = df.set_index('roll_number')['shift_rank'].to_dict()
    return shift_averages.to_dict(), shift_ranks

def calculate_averages(df):
    overall_average = df['total_marks_for_merit_list'].mean()
    category_averages = df.groupby('category')['total_marks_for_merit_list'].mean().to_dict()
    df['category_average'] = df['category'].map(category_averages)
    total_candidates = len(df)
    return overall_average, category_averages, total_candidates

def calculate_normalized_marks(df):
    try:
        df['shift'] = df['exam_date'] + ' ' + df['exam_time']

        shift_stats = df.groupby('shift')['total_marks_for_merit_list'].agg(['mean', 'std', 'median']).reset_index().rename(columns={'mean': 'shift_mean', 'std': 'shift_std', 'median': 'shift_median'})

        M_ti = df.groupby('shift')['total_marks_for_merit_list'].apply(lambda x: x.nlargest(max(1, len(x) // 1000)).mean()).reset_index().rename(columns={'total_marks_for_merit_list': 'shift_M_ti'})

        overall_mean = df['total_marks_for_merit_list'].mean()
        overall_std_dev = df['total_marks_for_merit_list'].std()
        M_tg = df['total_marks_for_merit_list'].nlargest(max(1, len(df) // 1000)).mean()

        df = df.merge(shift_stats, on='shift').merge(M_ti, on='shift')

        df['shift_M_iq'] = df['shift_mean'] + df['shift_std']

        Mg_q = overall_mean + overall_std_dev

        max_mean_shift = shift_stats.loc[shift_stats['shift_mean'].idxmax()]
        Mg_qm = max_mean_shift['shift_mean'] + max_mean_shift['shift_std']

        df['normalized_marks'] = ((M_tg - Mg_q) / (df['shift_M_ti'] - df['shift_M_iq'])) * (df['total_marks_for_merit_list'] - df['shift_M_iq']) + Mg_qm

        return df
    except Exception as e:
        print(f"Error in calculating normalized marks: {e}")
        return df

def update_db_with_normalized_marks(db_path, df):
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql('normalized', conn, if_exists='replace', index=False)
        conn.close()
    except Exception as e:
        print(f"Error updating database with normalized marks: {e}")
def update_db_with_raw_marks(db_path, df):
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql('candidates', conn, if_exists='replace', index=False)
        conn.close()
    except Exception as e:
        print(f"Error updating database with normalized marks: {e}")
# def initialize_db(database_path):
#     conn = sqlite3.connect(database_path)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS original_data (
#             answer_key_link TEXT UNIQUE,
#             category TEXT,
#             roll_number TEXT PRIMARY KEY,
#             candidate_name TEXT,
#             venue_name TEXT,
#             exam_date TEXT,
#             exam_time TEXT,
#             total_marks REAL,
#             section_data TEXT
#         )
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS candidates (
#             roll_number TEXT PRIMARY KEY,
#             category TEXT,
#             candidate_name TEXT,
#             venue_name TEXT,
#             exam_date TEXT,
#             exam_time TEXT,
#             total_marks REAL,
#             section_data TEXT,
#             overall_rank INTEGER,
#             category_rank INTEGER,
#             shift_average REAL,
#             shift_rank INTEGER,
#             category_average REAL
#         )
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS normalized (
#             roll_number TEXT PRIMARY KEY,
#             category TEXT,
#             normalized_marks REAL,
#             shift_median REAL,
#             normalized_rank INTEGER,
#             normalized_category_rank INTEGER
#         )
#     ''')
#     conn.commit()
#     conn.close()

# def fetch_original_data_df(database_path):
#     conn = sqlite3.connect(database_path)
#     df = pd.read_sql_query('SELECT * FROM original_data', conn)
#     conn.close()
#     return df
# def fetch_candidates_df(database_path):
#     conn = sqlite3.connect(database_path)
#     df = pd.read_sql_query('SELECT * FROM candidates', conn)
#     conn.close()
#     return df
# def fetch_normalized_df(database_path):
#     conn = sqlite3.connect(database_path)
#     df = pd.read_sql_query('SELECT * FROM normalized', conn)
#     conn.close()
#     return df

# def is_roll_number_exists(database_path, roll_number):
#     conn = sqlite3.connect(database_path)
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM candidates WHERE roll_number = ?', (roll_number,))
#     exists = cursor.fetchone() is not None
#     conn.close()
#     return exists

# def is_roll_number_exists_in_normalized_table(database_path, roll_number):
#     conn = sqlite3.connect(database_path)
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM normalized WHERE roll_number = ?', (roll_number,))
#     exists = cursor.fetchone() is not None
#     conn.close()
#     return exists

# def calculate_rank(df, roll_number, category):
#     df['overall_rank'] = df['total_marks'].rank(ascending=False, method='min')

#     df['category_rank'] = df.groupby('category')['total_marks'].rank(ascending=False, method='min')

#     # category_df = df[df['category'] == category].copy()
#     # category_df.loc[:, 'category_rank'] = category_df['total_marks'].rank(ascending=False, method='min')

#     overall_rank = df.loc[df['roll_number'] == roll_number, 'overall_rank'].values[0]
#     category_rank = df.loc[(df['roll_number'] == roll_number) & (df['category'] == category), 'category_rank'].values[0]
#     # category_rank = category_df.loc[category_df['roll_number'] == roll_number, 'category_rank'].values[0]

#     return overall_rank, category_rank

# def calculate_normalized_rank(df, roll_number, category):
#     print('before normalized_rank')
#     df['normalized_rank'] = df['normalized_marks'].rank(ascending=False, method='min')
#     print('after normalized_rank')
#     df['normalized_category_rank'] = df.groupby('category')['normalized_marks'].rank(ascending=False, method='min')
#     print('after normalized_category_rank')
#     overall_normalized_rank = df.loc[df['roll_number'] == roll_number, 'normalized_rank'].values[0]
#     normalized_category_rank = df.loc[(df['roll_number'] == roll_number) & (df['category'] == category), 'normalized_category_rank'].values[0]

#     return overall_normalized_rank, normalized_category_rank

# def calculate_shift_averages_and_ranks(df):
#     df['shift'] = df['exam_date'] + ' ' + df['exam_time']
#     shift_averages = df.groupby('shift')['total_marks'].mean()
#     df['shift_average'] = df['shift'].map(shift_averages)
#     df['shift_rank'] = df.groupby('shift')['total_marks'].rank(ascending=False, method='min')
#     shift_ranks = df.set_index('roll_number')['shift_rank'].to_dict()
#     return shift_averages.to_dict(), shift_ranks

# def calculate_averages(df):
#     overall_average = df['total_marks'].mean()
#     category_averages = df.groupby('category')['total_marks'].mean().to_dict()
#     df['category_average'] = df['category'].map(category_averages)
#     total_candidates = len(df)
#     return overall_average, category_averages, total_candidates

# def calculate_normalized_marks(df):
#     try:
#         df['shift'] = df['exam_date'] + ' ' + df['exam_time']

#         shift_stats = df.groupby('shift')['total_marks'].agg(['mean', 'std', 'median']).reset_index().rename(columns={'mean': 'shift_mean', 'std': 'shift_std', 'median': 'shift_median'})

#         M_ti = df.groupby('shift')['total_marks'].apply(lambda x: x.nlargest(max(1, len(x) // 1000)).mean()).reset_index().rename(columns={'total_marks': 'shift_M_ti'})

#         overall_mean = df['total_marks'].mean()
#         overall_std_dev = df['total_marks'].std()
#         M_tg = df['total_marks'].nlargest(max(1, len(df) // 1000)).mean()

#         df = df.merge(shift_stats, on='shift').merge(M_ti, on='shift')

#         df['shift_M_iq'] = df['shift_mean'] + df['shift_std']

#         Mg_q = overall_mean + overall_std_dev

#         max_mean_shift = shift_stats.loc[shift_stats['shift_mean'].idxmax()]
#         Mg_qm = max_mean_shift['shift_mean'] + max_mean_shift['shift_std']

#         df['normalized_marks'] = ((M_tg - Mg_q) / (df['shift_M_ti'] - df['shift_M_iq'])) * (df['total_marks'] - df['shift_M_iq']) + Mg_qm

#         return df
#     except Exception as e:
#         print(f"Error in calculating normalized marks: {e}")
#         return df

# def update_db_with_normalized_marks(db_path, df):
#     try:
#         conn = sqlite3.connect(db_path)
#         df.to_sql('normalized', conn, if_exists='replace', index=False)
#         conn.close()
#     except Exception as e:
#         print(f"Error updating database with normalized marks: {e}")
# def update_db_with_raw_marks(db_path, df):
#     try:
#         conn = sqlite3.connect(db_path)
#         df.to_sql('candidates', conn, if_exists='replace', index=False)
#         conn.close()
#     except Exception as e:
#         print(f"Error updating database with normalized marks: {e}")
