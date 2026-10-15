// Paste into a Blank Query's Advanced Editor in Power BI Desktop.
// Source fields remain text except the explicit numeric conversions below.
// Invalid numeric text produces a visible error rather than silently dropping records.
let
    Source = Parquet.Document(File.Contents("V:\Alcedo_atthis.parquet")),
    Typed = Table.TransformColumnTypes(Source, {
        {"decimalLatitude", type number},
        {"decimalLongitude", type number},
        {"coordinateUncertaintyInMeters", type number},
        {"year", Int64.Type},
        {"month", Int64.Type},
        {"day", Int64.Type}
    }, "en-US")
in
    Typed

