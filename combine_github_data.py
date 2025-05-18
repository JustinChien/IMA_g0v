import pandas as pd
import os

def print_data_statistics(df, name):
    print(f"\n=== Statistics for {name} ===")
    print(f"Total number of rows: {len(df)}")
    print(f"Total number of columns: {len(df.columns)}")
    print("\nColumn-wise statistics:")
    for col in df.columns:
        non_null = df[col].count()
        null_count = df[col].isna().sum()
        unique_count = df[col].nunique()
        print(f"\n{col}:")
        print(f"  - Non-null values: {non_null}")
        print(f"  - Null values: {null_count}")
        print(f"  - Unique values: {unique_count}")
        if null_count > 0:
            print(f"  - Null percentage: {(null_count/len(df)*100):.2f}%")

def combine_github_data():
    # Read the files
    print("Reading files...")
    contributors_df = pd.read_csv('contributors.csv')
    github_users_df = pd.read_excel('github_users_processed_v2.xlsx')

    # Print initial statistics
    print("\n=== Initial Data Statistics ===")
    print_data_statistics(contributors_df, "contributors.csv")
    print_data_statistics(github_users_df, "github_users_processed_v2.xlsx")

    # Rename columns in contributors_df to match github_users_df format
    column_mapping = {
        'contributor': 'username',
        'contributor_name': 'name',
        'contributor_location': 'location',
        'contributor_email': 'email',
        'contributor_bio': 'bio',
        'contributor_company': 'company',
        'contributor_blog': 'blog',
        'contributor_twitter': 'twitter_username',
        'contributor_public_repos': 'public_repos',
        'contributor_public_gists': 'public_gists',
        'contributor_followers': 'followers',
        'contributor_following': 'following',
        'contributor_created_at': 'created_at',
        'contributor_updated_at': 'updated_at',
        'contributor_url': 'html_url',
        'contributor_avatar_url': 'avatar_url'
    }
    
    contributors_df = contributors_df.rename(columns=column_mapping)

    # Check for duplicate usernames in each dataset
    print("\n=== Duplicate Analysis ===")
    contributors_dupes = contributors_df['username'].duplicated().sum()
    github_users_dupes = github_users_df['username'].duplicated().sum()
    print(f"Duplicate usernames in contributors.csv: {contributors_dupes}")
    print(f"Duplicate usernames in github_users_processed_v2.xlsx: {github_users_dupes}")

    # Merge the dataframes on the username field
    print("\nMerging data...")
    merged_df = pd.merge(
        github_users_df,
        contributors_df,
        on='username',
        how='outer',
        suffixes=('', '_contributors')
    )

    # Print merge statistics
    print("\n=== Merge Statistics ===")
    print(f"Number of rows in github_users_df: {len(github_users_df)}")
    print(f"Number of rows in contributors_df: {len(contributors_df)}")
    print(f"Number of rows in merged_df: {len(merged_df)}")
    
    # Calculate overlap statistics
    github_users_set = set(github_users_df['username'])
    contributors_set = set(contributors_df['username'])
    overlap = github_users_set.intersection(contributors_set)
    
    print("\n=== Username Overlap Analysis ===")
    print(f"Total unique usernames in github_users: {len(github_users_set)}")
    print(f"Total unique usernames in contributors: {len(contributors_set)}")
    print(f"Number of overlapping usernames: {len(overlap)}")
    print(f"Usernames only in github_users: {len(github_users_set - contributors_set)}")
    print(f"Usernames only in contributors: {len(contributors_set - github_users_set)}")

    # Remove duplicate columns (those with _contributors suffix)
    duplicate_columns = [col for col in merged_df.columns if col.endswith('_contributors')]
    merged_df = merged_df.drop(columns=duplicate_columns)

    # Print final statistics
    print("\n=== Final Combined Data Statistics ===")
    print_data_statistics(merged_df, "combined_github_data.csv")

    # Save the combined data
    print("\nSaving combined data...")
    output_file = 'combined_github_data.csv'
    merged_df.to_csv(output_file, index=False)
    print(f"Combined data saved to {output_file}")

    # Print final columns
    print("\nFinal columns in the combined file:")
    for col in merged_df.columns:
        print(f"- {col}")

if __name__ == "__main__":
    combine_github_data() 