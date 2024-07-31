from huggingface_hub import DatasetCard, DatasetCardData

youtube_card_data = DatasetCardData(
    language='en',
    license='mit',
    annotations_creators=['@lyleokoth'],
    task_categories=['text-classification'],
    task_ids=['text-scoring'],
    multilinguality='monolingual',
    pretty_name='YouTube Videos Timestamps extraction dataset',
)

youtube_card = DatasetCard.from_template(
    youtube_card_data,
    pretty_name=youtube_card_data.pretty_name,
)