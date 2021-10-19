Specifying the portion of text to be read as input data is possible
for Microsoft file. Other files assume that the entire content of
the file will be used as input data.

- XLSX: Requires SENTOP Config sheet and ID column header font color in standard RED.
- DOCX: Requires cells to be used as data to be highlighted. Do not
  highlight section headings, diagrams, or any other part of the
  document that should not be considered in the data.
- JSON: Requires each text data to be defined by a keyword-value
  pair using keyword 'text'. NOTE: Highlighting
  of JSON files is not supported.
- PDF: Not available yet.
- PPTX: Requires all text objects to be used as data to be highlighted.
- TXT: Assumes each line in the text file is data. NOTE: Highlighting
  of TXT files is not supported.
- XLSX: Requires cells to be used as data to be highlighted (without headers)
