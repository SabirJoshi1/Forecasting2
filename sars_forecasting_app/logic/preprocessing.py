def apply_filters(df, region, store_type, location_type):
    return df[
        (df['Region_Code'] == region) &
        (df['Store_Type'] == store_type) &
        (df['Location_Type'] == location_type)
    ]