import psycopg2
import sentop_config as config
from datetime import datetime
from util import globalutils
from util import sentop_log
from datetime import datetime
import re

class Database:
    def __init__(self):
        self.url = config.database["url"]
        self.db = config.database["database"]
        self.username = config.database["username"]
        self.pwd = config.database["password"]
        self.conn = None
        self.results_table_suffix = "_results"
        self.lda_words_table_suffix = "_lda_words"
        self.bertopic_words_table_suffix = "_bertopic_words"

    # -------------------------------- GENERAL ----------------------------------

    def open_connection(self):
        try:
            self.conn = psycopg2.connect(host=self.url, database=self.db, user=self.username, password=self.pwd)
            self.conn.autocommit = True
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)


    def close_connection(self):
        try:
            self.conn.close()
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)


    def execute_stmt(self, sql):
        sentlog = sentop_log.SentopLog() 

        try:
            # print("Executing: ", sql)
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            cur.close()
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(f"{sql}, {str(e)}")
            return str(e)


    def execute_stmt_data(self, sql, data):
        try:
            # print("Executing: ", sql)
            cur = self.conn.cursor()
            cur.execute(sql, data)
            self.conn.commit()
            cur.close()
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(f"{sql}, {str(e)}")
            return str(e)


    def table_exists(self, tablename):
        try:
            cur = self.conn.cursor()
            stmt = "SELECT 1 FROM information_schema.tables WHERE table_name = 'public' AND table_name = '" + tablename + "'"
            cur.execute(stmt)
            self.conn.commit()
            cur.close()
            return bool(cur.rowcount), None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return None, str(e)


    # Remove table
    def remove_table(self, tablename):
        try:
            stmt = "DROP TABLE " + tablename
            self.execute_stmt(stmt)
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            #globalutils.show_stack_trace(str(e))
            return str(e)

    '''
    # Remove all tables associated with ID
    def remove_all_tables(self, id):
        try:
            self.remove_table(id + self.results_table_suffix)
            self.remove_table(id + self.lda_words_table_suffix)
            self.remove_table(id + self.bertopic_words_table_suffix)
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)
    '''

    def add_result(self, tablename):
        try:
            print("Test")
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)


    def clear_table(self, tablename):
        print("Clearing table")
        try:
            stmt = "DELETE FROM " + tablename
            self.execute_stmt(stmt)
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)

   # ------------------------------ SUBMISSIONS -------------------------------

    def create_submissions_table(self):
        try:
            print("Creating submissions table.")
            stmt = "CREATE TABLE submissions (id text, annotation text, json_data text, file_url text, received_date timestamp, completed_date timestamp, status text, message text, PRIMARY KEY(id))"
            self.execute_stmt(stmt)
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)


    def add_submission(self, id, file_url):
        self.open_connection()
        exists, error = self.table_exists("submissions")
        if not exists:
            print("Table submissions does not exist")
            self.create_submissions_table()

        try:
            # Delete existing submission by both ID and file_url
            if id:
                stmt = ("DELETE FROM submissions WHERE id = '" +
                    id + "'")
                self.execute_stmt(stmt)
            elif file_url:
                stmt = ("DELETE FROM submissions WHERE file_url = '" +
                    file_url + "'")
                self.execute_stmt(stmt)
            # Add submission to submissions table
            stmt = """INSERT INTO submissions 
                (id, file_url, received_date, status) VALUES (%s,%s,%s,%s)"""
            data = (id, file_url, datetime.utcnow(), 'received')
            self.execute_stmt_data(stmt, data)
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)
        finally:
            self.close_connection()


    # Save JSON data to submissions table.
    def add_json_data(self, id, json_str):
        self.open_connection()
        try:
            stmt = ("UPDATE submissions SET json_data = '" +
                json_str + "' WHERE id = '" + id + "'")
            self.execute_stmt(stmt)
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)
        finally:
            self.close_connection()


    # Save Annotation data to submissions table.
    def add_annotation(self, id, annotation):
        self.open_connection()
        try:
            stmt = ("UPDATE submissions SET annotation = '" +
                annotation + "' WHERE id = '" + id + "'")
            self.execute_stmt(stmt)
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)
        finally:
            self.close_connection()


    def get_sentiment(self, id, sentiments):
        for sentiment in sentiments:
            if sentiment.id == id:
                return sentiment

   # -------------------------------- LDA WORDS ----------------------------------

    def create_lda_table(self, id, topics):
        sentlog = sentop_log.SentopLog() 

        tablename = str(id) + self.lda_words_table_suffix
        self.open_connection()
        exists, error = self.table_exists(tablename)
        if exists:
            error = self.remove_table(tablename)

        try:
            stmt = ("CREATE TABLE " + tablename +
                "(num int NOT NULL, topic int, word text, weight float, PRIMARY KEY (num))")
            error = self.execute_stmt(stmt)
            if error:
                return error
            sentlog.info_keyval(f"Created database table|{tablename}")

            num = 0
            for topic in topics:
                for i in range(len(topic.words)):
                    # Update submissions table
                    stmt = ("INSERT INTO " + tablename +
                        "(num, topic, word, weight) VALUES (%s,%s,%s,%s)")
                    data = (num, topic.topic_num, topic.words[i], topic.weights[i])
                    self.execute_stmt_data(stmt, data)
                    num = num + 1
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return error
        finally:
            self.close_connection()

    def create_lda_nooverlap_table(self, id, topics, lda_duplicate_words):
        sentlog = sentop_log.SentopLog() 
        tablename = str(id) + self.lda_words_table_suffix + "_nooverlap"
        self.open_connection()
        exists, error = self.table_exists(tablename)
        if exists:
            error = self.remove_table(tablename)

        try:
            stmt = ("CREATE TABLE " + tablename +
                "(num int NOT NULL, topic int, word text, weight float, PRIMARY KEY (num))")
            error = self.execute_stmt(stmt)
            if error:
                return error

            num = 0
            for topic in topics:
                for i in range(len(topic.words)):
                    if not topic.words[i] in lda_duplicate_words:
                        # Update submissions table
                        stmt = ("INSERT INTO " + tablename +
                            "(num, topic, word, weight) VALUES (%s,%s,%s,%s)")
                        data = (num, topic.topic_num, topic.words[i], topic.weights[i])
                        error = self.execute_stmt_data(stmt, data)
                        if error:
                            return error
                        num = num + 1

            sentlog.info_keyval(f"Created database table|{tablename}")
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)
        finally:
            self.close_connection()

    # -------------------------------- BERTOPIC WORDS ----------------------------------

    def create_bertopic_table(self, id, topics):
        sentlog = sentop_log.SentopLog() 
        tablename = str(id) + self.bertopic_words_table_suffix + "_nooverlap"

        self.open_connection()
        exists, error = self.table_exists(tablename)
        if exists:
            error = self.remove_table(tablename)

        try:
            stmt = ("CREATE TABLE " + tablename +
                " (num int NOT NULL, topic int, word text, weight float, PRIMARY KEY (num))")
            error = self.execute_stmt(stmt)
            if error:
                return error

            num = 0
            for topic in topics:
                for i in range(len(topic.words)):
                    # Update submissions table
                    stmt = ("INSERT INTO " + tablename +
                        "(num, topic, word, weight) VALUES (%s,%s,%s,%s)")
                    data = (num, topic.topic_num, topic.words[i], topic.weights[i])
                    error = self.execute_stmt_data(stmt, data)
                    if error:
                        return error
                    num = num + 1
            sentlog.info_keyval(f"Created database table|{tablename}")
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)
        finally:
            self.close_connection()

    def create_bertopic_nooverlap_table(self, id, topics, bert_duplicate_words):
        sentlog = sentop_log.SentopLog() 
        tablename = str(id) + self.bertopic_words_table_suffix

        self.open_connection()
        exists, error = self.table_exists(tablename)
        if exists:
            error = self.remove_table(tablename)

        try:
            stmt = ("CREATE TABLE " + tablename +
                " (num int NOT NULL, topic int, word text, weight float, PRIMARY KEY (num))")
            error = self.execute_stmt(stmt)
            if error:
                return error
            num = 0
            for topic in topics:
                for i in range(len(topic.words)):
                    # Update submissions table
                    if not topic.words[i] in bert_duplicate_words:
                        stmt = ("INSERT INTO " + tablename +
                            "(num, topic, word, weight) VALUES (%s,%s,%s,%s)")
                        data = (num, topic.topic_num, topic.words[i], topic.weights[i])
                        error = self.execute_stmt_data(stmt, data)
                        if error:
                            return error
                        num = num + 1
            sentlog.info_keyval(f"Created database table|{tablename}")
            return None
        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)
        finally:
            self.close_connection()


    def get_sentiment(self, id, sentiments):
        for sentiment in sentiments:
            if sentiment.id == id:
                return sentiment

    # -------------------------------- RESULTS ----------------------------------

    def create_result_table(self, id, id_list, data_list, sentiment_results, bertopic_results, lda_results, table_data, table_col_headers):
        sentlog = sentop_log.SentopLog() 

        bert_sentence_topics = None
        if bertopic_results:
            bert_sentence_topics = bertopic_results.topic_per_row
        lda_sentence_topics = None

        if lda_results:
            lda_sentence_topics = lda_results.topic_per_row
        tablename = str(id) + self.results_table_suffix
        self.open_connection()
        exists, error = self.table_exists(tablename)
        if exists:
            error = self.remove_table(tablename)

        class3 = self.get_sentiment('class3', sentiment_results)
        class5 = self.get_sentiment('class5', sentiment_results)
        emotion1 = self.get_sentiment('emotion1', sentiment_results)
        offensive1 = self.get_sentiment('offensive1', sentiment_results)
        emotion2 = self.get_sentiment('emotion2', sentiment_results)

        # Check if the original data must be replicated in the results. If so, this data will be stored in table_data and the column headers
        # will be stored in table_data_headers.
        table_data_headers_str = ""
        headers_insert_str = ""
        table_data_str = ""

        if table_col_headers:
            # Get the table headers
            for header in table_col_headers:
                #print(f"Header start: {header}")
                if header is None:
                    header = "\"na\""
                else:
                    header = header.replace("-","_")
                    header = header.replace(" ", "_")
                    header = re.sub("[^0-9a-zA-Z_]+", "", header)
                    header = '"' + header + '"'

                #print(f"Header end: {header}")
                table_data_headers_str = table_data_headers_str + header + " text" + ", "
                headers_insert_str = headers_insert_str + header + ", "
        else:
            # If JSON or other format
            table_data_headers_str = "\"Document\" text" + ", "
            headers_insert_str = "\"Document\", "

        try:
            create_stmt = ("CREATE TABLE " + tablename + 
                " (" + table_data_headers_str + "\"num\" text, \"class3\" text, \"class5\" text, \"emotion1\" text, \"emotion2\" text, \"offensive1\" text, \"lda\" text, \"bertopic\" text, PRIMARY KEY (num))")
            error = self.execute_stmt(create_stmt)
            if error:
                return error

            #sentlog.debug(f"len(data_list): {len(data_list)}")
            for i in range(len(data_list)):
                #print(f"i: {i}")
                bert_topic = None
                if bert_sentence_topics:
                    bert_topic = bert_sentence_topics[i]
                else:
                    bert_topic = "N/A"

                lda_topic = None
                if lda_sentence_topics:
                    lda_topic = lda_sentence_topics[i]
                else:
                    lda_topic = "N/A"

                #-----------------------------------------
                # Tables are only used for XLSX files.
                table_vals = ""
                table_row = None
                if table_data:
                    table_row = table_data[i]
                    #print(f"cols type: {type(table_row)}, cols length: {len(table_row)}, cols val: {table_row}")

                    for j in range (len(table_row)):
                        #print(f"j: {j}")
                        val = table_row[j]
                        if not val or val == 'None':
                            val = ""

                        val = str(val)  # Make sure val is converted to string
                        val = val.strip('"')  # Remove double quotes from string
                        val = val.replace('"', "") # Remove single quotes from string

                        # IMPORTANT! table_vals must be surrounded by SINGLE quotes to allow values that 
                        # start with a numeric value. In Postgres, this cannot be done using double quotes. 
                        val = val.replace("'", "''")  # Replace single quotes with two single quotes for Postgres.
                        table_vals = table_vals + "'" + str(val) + "', "  # Add double quotes around entire val

                    #print(f"Vals: {table_vals}")
                else:
                    # If JSON or other format
                    val = data_list[i]
                    val = str(val)  # Make sure val is converted to string
                    val = val.strip('"')  # Remove double quotes from string
                    val = val.replace('"', "") # Remove single quotes from string

                    # IMPORTANT! table_vals must be surrounded by SINGLE quotes to allow values that 
                    # start with a numeric value. In Postgres, this cannot be done using double quotes. 
                    val = val.replace("'", "''")  # Replace single quotes with two single quotes for Postgres.
                    table_vals = "'" + str(val) + "', "  # Add double quotes around entire val

                if not id_list:
                    id_list = list(range(1, len(data_list)+1))
                    sentlog.warn(f"id_list is None")
                if not class3.data_list:
                    sentlog.warn(f"class3.datalist is None")
                if not class5.data_list:
                    sentlog.warn(f"class5.data_list is None")
                if not emotion1.data_list:
                    sentlog.warn(f"emotion1.data_list is None")
                if not emotion2.data_list:
                    sentlog.warn(f"emotion2.data_list is None")
                if not offensive1.data_list:
                    sentlog.warn(f"offensive1.data_list is None")
                #if not lda_topic:   # Could mean that lda_topic = 0
                #    sentlog.warn(f"lda_topic is None")
                #if not bert_topic:  # Could mean that bert_topic = 0
                #    sentlog.warn(f"bert_topic is None")

                if (data_list[i]):
                    insert_stmt = ("INSERT INTO " + tablename + "(" + headers_insert_str + "\"num\", \"class3\", \"class5\", \"emotion1\", \"emotion2\", \"offensive1\", \"lda\", \"bertopic\") VALUES (" + table_vals + "'" + str(id_list[i]) + "', '" + str(class3.data_list[i]) + "', '" + str(class5.data_list[i]) + "', '" + str(emotion1.data_list[i]) + "', '" + str(emotion2.data_list[i]) + "', '" + str(offensive1.data_list[i]) + "', '" + str(lda_topic) + "', '" + str(bert_topic) + "')")                    
                    #sentlog.info_p(f"SQL INSERT: {insert_stmt}")
                    error = self.execute_stmt(insert_stmt)
                    if error:
                        return error


        except (Exception, psycopg2.DatabaseError) as e:
            globalutils.show_stack_trace(str(e))
            return str(e)
        finally:
            self.close_connection()
