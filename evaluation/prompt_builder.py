"""
Few-shot prompt builder for temporal QA
"""

class PromptBuilder:
    """Builds few-shot prompts for temporal QA evaluation"""
    
    def __init__(self):
        pass
    
    def create_prompt(self, question: str, examples: list = None) -> str:
        """Create few-shot prompt"""
        if not examples:
            return self._create_zero_shot_prompt(question)
        else:
            return self._create_few_shot_prompt(question, examples)
    
    def _create_zero_shot_prompt(self, question: str) -> str:
        """Create zero-shot prompt"""
        return (
            "Answer this question with a short, precise answer (1-3 words maximum).\n\n"
            f"Question: {question}\n"
            "Answer:"
        )
    
    def _create_few_shot_prompt(self, question: str, examples: list) -> str:
        """Create few-shot prompt with examples"""
        prompt = "Answer questions with short, precise answers (1-3 words maximum). Examples:\n\n"
        
        # Add examples
        for example in examples:
            prompt += f"Question: {example['question']}\n"
            prompt += f"Answer: {example['answer']}\n\n"
        
        # Add target question
        prompt += f"Question: {question}\n"
        prompt += "Answer:"
        
        return prompt
    
    def create_instruction_prompt(self, question: str, examples: list = None) -> str:
        """Create instruction-following prompt"""
        instruction = (
            "You are a helpful assistant that answers temporal questions accurately. "
            "Provide short, factual answers."
        )
        
        if examples:
            prompt = f"{instruction}\n\nExamples:\n"
            for example in examples:
                prompt += f"Q: {example['question']}\nA: {example['answer']}\n\n"
            prompt += f"Q: {question}\nA:"
        else:
            prompt = f"{instruction}\n\nQ: {question}\nA:"
        
        return prompt
    
    def create_chat_prompt(self, question: str, examples: list = None) -> str:
        """Create chat-style prompt"""
        if examples:
            prompt = "Here are some example questions and answers:\n\n"
            for example in examples:
                prompt += f"Human: {example['question']}\n"
                prompt += f"Assistant: {example['answer']}\n\n"
            prompt += f"Human: {question}\n"
            prompt += "Assistant:"
        else:
            prompt = f"Human: {question}\nAssistant:"
        
        return prompt
