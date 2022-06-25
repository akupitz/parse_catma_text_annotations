import os

from catma.archives_unpacking import CatmaUnpacking
from catma.dataset_creation.speaker_level_dataset_creation import SpeakerLevelDatasetCreator
from configuration.general_config import ITAY_CATMA_CONFIG


def test_speaker_extraction():
    catma_config = ITAY_CATMA_CONFIG
    catma_unpacking = CatmaUnpacking(tar_gzs_dir=catma_config.input_catma_tar_gzs_data_path,
                                     unpacked_protocol_archives_dir=catma_config.unpacked_protocol_archives_path)
    catma_unpacking.unpack_tar_gz_files()
    valid_protocol_dirs = catma_unpacking.get_valid_unpacked_protocol_dirs()
    protocol_dir = [protocol_dir for protocol_dir in valid_protocol_dirs if
                    os.path.basename(protocol_dir) == "פרוטוקול_מספר_42_parts"][
        0]  # work on "ועדת הכספים חלקי דיון"-> "פרוטוקול מספר 42
    speaker_level_dataset_creator = SpeakerLevelDatasetCreator(
        remove_new_line_and_tab=ITAY_CATMA_CONFIG.remove_new_line_and_tab)
    temp_df = speaker_level_dataset_creator.get_df_from_protocol_dir(protocol_dir)
    row_to_test = temp_df[temp_df["speaker_name_start_char"] == 950]
    assert row_to_test["speaker_text_start_char"].iloc[0] == 983
    assert row_to_test["speaker_end_char"].iloc[0] == 1025
    assert " ".join(row_to_test["speaker_name"].iloc[0].split()) == "אורלי לוי אבקסיס (ישראל ביתנו):"
    assert row_to_test["speaker_name_start_char"].iloc[0] == 950
    row_to_test = temp_df[temp_df["speaker_name_start_char"] == 5291]
    assert row_to_test["speaker_text_start_char"].iloc[0] == 5308
    assert row_to_test["speaker_end_char"].iloc[0] == 5332
    assert " ".join(row_to_test["speaker_name"].iloc[0].split()) == 'היו"ר משה גפני:'
    assert " ".join(row_to_test["speaker_text"].iloc[0].split()) == 'זה לא יעמוד בבג"ץ.'
    print("VVV\nPassed speaker extraction test")


if __name__ == "__main__":
    test_speaker_extraction()