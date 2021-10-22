import io
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
import logging
from . import log_util


def generate_excel(id, annotation, row_id_list, docs, sentiments, lda_results, bertopic_results, RESULTS_DIR):
    logger = logging.getLogger('xlsx_util')

    try:
        bert_sentence_topics = None
        bert_topics = None
        bert_duplicate_words = None

        if bertopic_results:
            bert_sentence_topics = bertopic_results.topic_per_row
            logger.info(f"BERTopic rows: {len(bert_sentence_topics)}")
            bert_topics = bertopic_results.topics_list
            bert_duplicate_words = bertopic_results.duplicate_words_across_topics

        lda_sentence_topics = None
        lda_topics = None
        lda_duplicate_words = None

        if lda_results:
            lda_sentence_topics = lda_results.topic_per_row
            print(f"LDA rows: {len(lda_sentence_topics)}")
            lda_topics = lda_results.topics_list
            lda_duplicate_words = lda_results.duplicate_words_across_topics

        output_dir_path = RESULTS_DIR

        class3 = sentiments.class3
        class5 = sentiments.star5
        emotion1 = sentiments.emotion1
        emotion2 = sentiments.emotion2
        offensive1 = sentiments.offensive1

        # Create results data
        rows = []
        for i in range(len(docs)):
            row_data = []
            if (docs[i]):
                # Write row ID
                if row_id_list:
                    row_data.append(row_id_list[i])
                else:
                    row_data.append(i)

                # Write preprocessed document
                row_data.append(docs[i])

                # Write BERTopic topic
                if bert_sentence_topics:
                    row_data.append(bert_sentence_topics[i])
                else:
                    row_data.append("N/A")

                # Write LDA topic
                if lda_sentence_topics:
                    row_data.append(lda_sentence_topics[i])
                else:
                    row_data.append("N/A")

                # Write class3
                if class3:
                    row_data.append(class3[i])
                else:
                    row_data.append("N/A")    

                # Write class 5
                if class5:
                    row_data.append(class5[i])
                else:
                    row_data.append("N/A") 

                # Write emotion1
                if emotion1:
                    row_data.append(emotion1[i])
                else:
                    row_data.append("N/A")  

                # Write emotion2
                if emotion2:
                    row_data.append(emotion2[i])
                else:
                    row_data.append("N/A") 

                # Write offensive1
                if offensive1:
                    row_data.append(offensive1[i])
                else:
                    row_data.append("N/A") 

                '''
                if table_data:
                    table_row = table_data[i]
                
                    #print(f"cols type: {type(table_row)}, cols length: {len(table_row)}, cols val: {table_row}")
                    vals = ""
                    for j in range (len(table_row)):
                        #print(f"j: {j}")
                        val = table_row[j]
                        if not val or val == 'None':
                            val = ""
                        
                        val = str(val)  # Make sure val is converted to string
                        val = val.strip('"')  # Remove double quotes from string
                        val = val.replace('"', "") # Remove single quotes from string
                        vals = vals + "\"" + str(val) + "\","  # Add double quotes around entire val
                        row_data.append(val)
                        #print(f"Vals: {vals}")
                '''

                rows.append(row_data)

        # Create results XLSX
        wb = Workbook()
        xlsx_out = RESULTS_DIR + "\\" + id + "_results.xlsx"
        ws1 = wb.active
        ws1.title = "Results"

        # Create column headers
        '''
        headers = []
        if table_col_headers:
            # Get the table headers
            for header in table_col_headers:
                #print(f"Header start: {header}")
                if header is None:
                    header = "na"
                else:
                    header = header.replace("-","_")
                    header = header.replace(" ", "_")
                    header = re.sub("[^0-9a-zA-Z_]+", "", header)
        '''
        result_headers = ['ID', 'Document', 'BERTopic Topic', 'LDA Topic', 'Class-3', 'Class-5', 'Emotion-1', 'Emotion-2', 'Offensive-1']
        #result_headers.extend(headers)
        ws1.append(result_headers)

        ws1['A1'].font = Font(bold=True)
        ws1['B1'].font = Font(bold=True)

        # Topic columns
        ws1['C1'].fill = PatternFill(start_color='FF66FF66', end_color='FF66FF66', fill_type='solid')
        ws1['C1'].font = Font(bold=True)
        ws1['D1'].fill = PatternFill(start_color='FF66FF66', end_color='FF66FF66', fill_type='solid')
        ws1['D1'].font = Font(bold=True)

        # Polarity sentiment columns
        ws1['E1'].fill = PatternFill(start_color='FF66FFFF', end_color='FF66FFFF', fill_type='solid')
        ws1['E1'].font = Font(bold=True)
        ws1['F1'].fill = PatternFill(start_color='FF66FFFF', end_color='FF66FFFF', fill_type='solid')
        ws1['F1'].font = Font(bold=True)

        # Emotion sentiment columns
        ws1['G1'].fill = PatternFill(start_color='FFFFFF99', end_color='FFFFFF99', fill_type='solid')
        ws1['G1'].font = Font(bold=True)
        ws1['H1'].fill = PatternFill(start_color='FFFFFF99', end_color='FFFFFF99', fill_type='solid')
        ws1['H1'].font = Font(bold=True)
        ws1['I1'].fill = PatternFill(start_color='FFFFFF99', end_color='FFFFFF99', fill_type='solid')
        ws1['I1'].font = Font(bold=True)

        for i in range(len(rows)):
            ws1.append(rows[i])

        # Create Annotation XLSX sheet
        ws4 = wb.create_sheet(title="Annotation")
        fields = ['Annotation']
        annotation_list = []
        annotation_list.append(annotation)
        ws4.append(annotation_list)

        # Create BERTopic topics data
        if bert_topics:
            rows = []

            for i in range(len(bert_topics)):
                for j in range(len(bert_topics[i].words)):
                    row_data = []
                    row_data.append(bert_topics[i].topic_num)
                    row_data.append(bert_topics[i].words[j])
                    row_data.append(float(bert_topics[i].weights[j]))
                    rows.append(row_data)

            # Create BERTopic topics data XLSX sheet
            ws2 = wb.create_sheet(title="BERTopic")
            ws2.append(['Topic', 'Top Words', 'Weight'])
            for i in range(len(rows)):
                ws2.append(rows[i])

            # Create BERTopic non-overlapping topic words data
            rows = []
            for i in range(len(bert_topics)):
                for j in range(len(bert_topics[i].words)):
                    if not bert_topics[i].words[j] in bert_duplicate_words:
                        row_data = []
                        row_data.append(bert_topics[i].topic_num)
                        row_data.append(bert_topics[i].words[j])
                        row_data.append(float(bert_topics[i].weights[j]))
                        rows.append(row_data)

            # Create BERTopic non-overlapping topics data XLSX sheet
            ws2 = wb.create_sheet(title="BERTopic Non-Overlapping Topics")
            ws2.append(['Topic', 'Top Words', 'Weight'])
            for i in range(len(rows)):
                ws2.append(rows[i])  

        # Create LDA topics data
        if lda_topics:
            rows = []
            for i in range(len(lda_topics)):
                #print("LDA i: ", i)
                for j in range(len(lda_topics[i].words)):
                    #print("LDA j: ", j)
                    row_data = []
                    row_data.append(lda_topics[i].topic_num)
                    row_data.append(lda_topics[i].words[j])
                    row_data.append(float(lda_topics[i].weights[j]))
                    rows.append(row_data)

            # Create LDA topics data XLSX sheet
            ws3 = wb.create_sheet(title="LDA")
            fields = ['Topic', 'Top Words', 'Weight']
            ws3.append(fields)
            for i in range(len(rows)):
                ws3.append(rows[i])

            # Create LDA non-overlapping topics words data
            rows = []
            for i in range(len(lda_topics)):
                #print("LDA i: ", i)
                for j in range(len(lda_topics[i].words)):
                    if not lda_topics[i].words[j] in lda_duplicate_words:
                        row_data = []
                        row_data.append(lda_topics[i].topic_num)
                        row_data.append(lda_topics[i].words[j])
                        row_data.append(float(lda_topics[i].weights[j]))
                        rows.append(row_data)

            # Create LDA topics data XLSX sheet
            ws3 = wb.create_sheet(title="LDA Non-Overlapping Topics")
            fields = ['Topic', 'Top Words', 'Weight']
            ws3.append(fields)
            for i in range(len(rows)):
                ws3.append(rows[i])

        # Save XLSX
        wb.save(filename = xlsx_out)

        logger.info(f"Wrote Excel results to: {xlsx_out}")
    except Exception as e:
        log_util.show_stack_trace(e)
        return None, str(e)

