# Open the kingfisher dataset in Power BI

No Python or coding is required.

1. Download this repository with **Code → Download ZIP**. Right-click the ZIP and select **Extract All**.
2. Open **Power BI Desktop**.
3. Select **Home → Get data → More → Parquet → Connect**.
4. Open the extracted **data** folder. Right-click **Alcedo_atthis.parquet → Copy as path**. Paste this into the connection box, removing surrounding quotation marks.
5. Select **Transform Data**.
6. Change `year`, `month`, and `day` to **Whole number**. Change coordinates to **Decimal number** using **English (United States)** locale. Keep identifiers such as `gbifID` and `speciesKey` as text.
7. Click **Close & Apply**.

## Make your first chart

Add a column chart with `year` on the X-axis and **Count of gbifID** on the Y-axis. Add a year slicer and a card with **Count of gbifID**.
The full dataset has **429,646 records**. All have country code **NL**. These are records, not population estimates.

For maps, set the coordinate data categories to **Latitude** and **Longitude** and select **Don't summarize**. Map availability can depend on your organisation's settings.

## Troubleshooting

- **File not found:** extract the ZIP first and copy the file path from your own computer.
- **Numbers look wrong:** use **Change Type → Using Locale → English (United States)**. Source decimals use a dot.
- **Date conversion errors:** leave `eventDate` as text. Some values contain date ranges.
- **No Parquet connector:** update Power BI Desktop. You can open `reports/by_year.csv` through **Get data → Text/CSV**.

The optional `powerbi/Alcedo_atthis.pq` file is for Advanced Editor users. Replace its example path with yours.
Power BI Service refresh of local files requires a configured gateway. Start in Power BI Desktop.

[Microsoft's Parquet connector documentation](https://learn.microsoft.com/en-us/power-query/connectors/parquet)
