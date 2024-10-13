from typing import Any, Optional, Type
from gentopia.tools.basetool import BaseTool, BaseModel, Field
from transformers import MarianMTModel, MarianTokenizer

class TranslationParameters(BaseModel):
    source_language: str = Field(..., description="Source language code (e.g., 'en' for English)")
    target_language: str = Field(..., description="Target language code (e.g., 'fr' for French)")
    text_to_translate: str = Field(..., description="Text to be translated")


# Class to provide Translation Functionality
class Translator(BaseTool):
    """A tool designed to translate text between languages."""
    name = "translator"
    description = "Translates text from a specified source language to a target language."

    args_schema: Optional[Type[BaseModel]] = TranslationParameters

    # Method for performing translation
    def _run(self, source_language: str, target_language: str, text_to_translate: str) -> str:
        # Initialize model and tokenizer with MarianMT library
        model_name = f'Helsinki-NLP/opus-mt-{source_language}-{target_language}'
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        # Encode input text into tokens
        input_tokens = tokenizer.encode(text_to_translate, return_tensors='pt')
        # Generate translation using the model
        output_tokens = model.generate(input_tokens)
        # Decode tokens to get the translated text
        translated_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
        return translated_text

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Asynchronous execution is not available.")

if __name__ == "__main__":
    # Example of using TranslationTool to translate text
    translation_params = TranslationParameters(
        source_language="en",
        target_language="fr",
        text_to_translate="Hello, how are you?"
    )

    # Create an instance of TranslationTool
    translation_tool = Translator()
    # Perform translation
    translated_text = translation_tool._run(**translation_params.dict())
    # Output the translated text
    print(f"Translated text: {translated_text}")

