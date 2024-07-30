EXTRACTION_PROMPT_V1: str = (
    """Extract the time stamps and their titles from the following video """
    """description. Only include valid time stamps.\n{format_instructions}\n video """
    """id: ```{video_id}```\video description: ```{video_description}`"""
)