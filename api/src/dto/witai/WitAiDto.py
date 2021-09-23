class WitAiMessageParamsRequest :
    def __init__(self,
        text = None
    ) :
        self.q = text

class WitAiMessageResponse :
    def __init__(self,
        text = None,
        intents = None,
        entities = None,
        traits = None,
        originalResponse = None
    ) :
        self.text = text
        self.intentList = intents
        self.entityDictionary = entities
        self.traitDictionary = traits
        self.originalResponse = originalResponse
