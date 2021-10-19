from . import sentop_log

class DataIn:

    """The incoming data.

    Attributes:
        kms_id              The KMS ID (not used for file URLs).
        sentop_id           The SENTOP ID.
        row_id_list         The list of row IDs.
        data_list           The corpus (i.e., list of documents) to be analyzed.
        all_stop_words      The list of all stop words including user-defined stop words.
        annotation          The user-defined annotation.
    """

    def __init__(self, data_type, kms_id, sentop_id, row_id_list, data_list, all_stop_words, annotation):
        self.data_type = data_type
        self.kms_id = kms_id
        self.sentop_id = sentop_id
        self.row_id_list = row_id_list  
        self.data_list = data_list  # Corpus (list of documents to be analyzed).
        self.all_stop_words = all_stop_words
        self.annotation = annotation

    def show_info(self):
        sentlog = sentop_log.SentopLog()
        sentlog.info_h2(f"Data Summary")
        if self.data_type:
            sentlog.info_keyval(f"Data Type|{self.data_type}")
        else:
            sentlog.error("No data type for this object.")

        if self.kms_id:
            sentlog.info_keyval(f"KMS ID|{self.kms_id}")
        else:
            sentlog.error("No KMS ID for this data.")

        if self.sentop_id:
            sentlog.info_keyval(f"SENTOP ID|{self.sentop_id}")
        else:
            sentlog.error("No SENTOP ID for this data.")

        #if self.row_id_list:
        #    sentlog.info_keyval(f"Num Valid Data IDs|{len(self.row_id_list)}")
        #else:
        #   sentlog.error("No row ID list for this data.")

        if self.data_list:
            sentlog.info_keyval(f"Num Valid Data|{len(self.data_list)}")
        else:
            sentlog.error("No data list for this data.")

        if self.all_stop_words:
            sentlog.info_keyval(f"All stop words|{len(self.all_stop_words)}")
        else:
            sentlog.error("No stop words for this data.")

        if self.annotation:
            sentlog.info_keyval(f"Annotation|{self.annotation}")
        else:
            sentlog.error("No annotation for this data.")

        sentlog.info_p(f"")
