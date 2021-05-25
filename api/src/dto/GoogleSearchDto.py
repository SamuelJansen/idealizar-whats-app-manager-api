class GoogleSearchResponseDto:
    def __init__(self,
        title = None,
        url = None,
        snippet = None,
        suggestedText = None,
        screenshotName = None
    ) :
        self.title = title
        self.url = url
        self.snippet = snippet
        self.suggestedText = suggestedText
        self.screenshotName = screenshotName
