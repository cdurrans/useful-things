
public static string findFileToLoad()
{
    string excelfilepath = "";
    Thread t = new Thread((ThreadStart)(() =>
            {
                OpenFileDialog fbd = new OpenFileDialog();
                if (fbd.ShowDialog() == DialogResult.OK)
                {
                    excelfilepath = fbd.FileName;
                }
                if (excelfilepath == "")
                {
                    throw new System.ArgumentException("Parameter cannot be empty", "excelfilepath");
                }
            }));
            
            // Run your code from a thread that joins the STA Thread
            t.SetApartmentState(ApartmentState.STA);
            t.Start();
            t.Join();
    return excelfilepath;
}


public static void loadExcelOrCsvFileIntodb(string excelFilePath, string excelSheetName, string destinationConnectionString, string tableToLoad, string excelOrcsv = "excel")
    {
        string sexcelconnectionstring = "";
        string myexceldataquery = "";
        if (excelOrcsv.ToLower() == "excel")
        {
            sexcelconnectionstring = @"Provider=Microsoft.ACE.OLEDB.12.0;data source=" + excelFilePath + ";Extended Properties = \"Excel 12.0 Macro;HDR=YES\"; ";
            myexceldataquery = "select * from [" + excelSheetName + "$]";
        }
        if (excelOrcsv.ToLower() == "csv")
        {
            sexcelconnectionstring = @"Provider=Microsoft.ACE.OLEDB.12.0;data source=" + excelFilePath + ";Extended Properties = \"text;HDR=YES;FMT=Delimited\"";
            myexceldataquery = "select * from [" + excelSheetName + "]";
        }

        System.Data.OleDb.OleDbConnection oledbconn = new System.Data.OleDb.OleDbConnection(sexcelconnectionstring);
        System.Data.OleDb.OleDbCommand oledbcmd = new System.Data.OleDb.OleDbCommand(myexceldataquery, oledbconn);
        oledbconn.Open();
        System.Data.OleDb.OleDbDataReader dr = oledbcmd.ExecuteReader();
        SqlBulkCopy bulkcopy = new SqlBulkCopy(destinationConnectionString);
        bulkcopy.DestinationTableName = tableToLoad;
        bulkcopy.BulkCopyTimeout = 900;
        bulkcopy.WriteToServer(dr);
        //cnnExcel.Close();
        Console.WriteLine("Bulk copied data file.");
    }


public static void saveSqlReaderToCSV(string saveFilePath, SqlDataReader reader)
    {
        StringBuilder sb = new StringBuilder();
        StreamWriter sw = new StreamWriter(saveFilePath);

        var columnNames = Enumerable.Range(0, reader.FieldCount)
                .Select(reader.GetName) //OR .Select("\""+  reader.GetName"\"") 
                .ToList();

        //Create headers
        sb.Append(string.Join(",", columnNames));
        //Append Line
        sb.AppendLine();

        while (reader.Read())
        {
            for (int i = 0; i < reader.FieldCount; i++)
            {
                string value = reader[i].ToString();
                if (value.Contains(","))
                    value = "\"" + value + "\"";
                sb.Append(value.Replace(Environment.NewLine, " ") + ",");
            }
            sb.Length--; // Remove the last comma
            sb.AppendLine();
        }
        sw.Write(sb.ToString());
        sw.Close();
        Console.WriteLine("Csv saved to " + saveFilePath);
    }
